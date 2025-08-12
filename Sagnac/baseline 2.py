import time
import numpy as np
from pylablib.devices import Thorlabs
from TimeTagger import createTimeTagger, Coincidence, CoincidenceTimestamp, Counter, freeTimeTagger
from scipy.optimize import minimize


motor_serials = ["83836223", "83836935", "83854766", "83857392"]
measure_time = 1  # sec

basis_to_angles = {
    'H': (0, 0),
    'V': (45, 0),
    'D': (22.5, 45),
    'A': (-22.5, 45),
    'R': (0, 45),
    'L': (45, 45)
}

target_pairs = [
    ("H", "H"),  # HH
    ("V", "V"),  # VV
    ("L", "H"),  # LH
    ("L", "V"),  # LV
    ("A", "H"),  # AH
    ("A", "V"),  # AV
]


def measure_single_pair(baseline_angles, top_state, bottom_state):
    tagger = createTimeTagger()
    ch_a, ch_b = 1, 2
    coincidence_window_ps = 10000
    coinc = Coincidence(tagger, [ch_a, ch_b], coincidenceWindow=coincidence_window_ps, timestamp=CoincidenceTimestamp.ListedFirst)
    coinc_channel = coinc.getChannel()

    try:
        top_hwp_offset, top_qwp_offset = basis_to_angles[top_state]
        bottom_hwp_offset, bottom_qwp_offset = basis_to_angles[bottom_state]

        angles = [
            baseline_angles[0] + top_hwp_offset,
            baseline_angles[1] + top_qwp_offset,
            baseline_angles[2] + bottom_hwp_offset,
            baseline_angles[3] + bottom_qwp_offset
        ]

        motors = [Thorlabs.kinesis.KinesisMotor(sn, scale='stage') for sn in motor_serials]
        for motor, angle in zip(motors, angles):
            motor.move_to(angle)
        for motor in motors:
            motor.wait_move()
            motor.close()

        binwidth_ps = int(1e9)
        n_values = int(measure_time * 1000)
        counter = Counter(tagger, [ch_a, ch_b, coinc_channel], binwidth=binwidth_ps, n_values=n_values)
        time.sleep(measure_time)

        counts = counter.getData()
        single_a = int(np.sum(counts[0]))
        single_b = int(np.sum(counts[1]))
        coin_val = int(np.sum(counts[2]))
        acc = measure_time * 2 * (single_a / measure_time) * (single_b / measure_time) * coincidence_window_ps * 1e-12
        real_coin = coin_val - acc

        label = f"{top_state}{bottom_state}"
        print(f"{label} | Single A = {single_a}, Single B = {single_b}, Coinc = {coin_val}, real_coin = {real_coin:.3f}")

        return real_coin

    finally:
        freeTimeTagger(tagger)

def cost_function(baseline_angles):
    hh = measure_single_pair(baseline_angles, "H", "H")
    vv = measure_single_pair(baseline_angles, "V", "V")
    lh = measure_single_pair(baseline_angles, "L", "H")
    lv = measure_single_pair(baseline_angles, "L", "V")
    ah = measure_single_pair(baseline_angles, "A", "H")
    av = measure_single_pair(baseline_angles, "A", "V")

    cost = (10 * hh) ** 2 + (10 * vv) ** 2 + (lh - lv) ** 2 + (ah - av) ** 2
    print(f"\n>>> Cost: {cost:.4f} @ angles: {baseline_angles}")
    return cost


x0 = [7.9000, 204.6000, 35.5000, 218.8850]
result = minimize(
    cost_function,
    x0,
    method='Nelder-Mead',
    options={
        'maxiter': 15,
        'xatol': 0.1,
        'fatol': 1.0,
        'disp': True
    }
)
print(result)
