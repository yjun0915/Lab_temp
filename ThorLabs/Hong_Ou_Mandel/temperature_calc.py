import numpy as np
import matplotlib.pyplot as plt

def sellmeier_o(lambda_um, T):
    A, B, C, D, E, F = 3.29100, 0.04140, 0.03978, 0.000298, 0, 1.1e-5
    n2 = A + B / (lambda_um**2 - C) - D * lambda_um**2 + E * lambda_um**4
    n = np.sqrt(n2) + F * (T - 25)
    return n

def sellmeier_e(lambda_um, T):
    A, B, C, D, E, F = 3.45018, 0.04341, 0.04597, 0.000298, 0, 1.3e-5
    n2 = A + B / (lambda_um**2 - C) - D * lambda_um**2 + E * lambda_um**4
    n = np.sqrt(n2) + F * (T - 25)
    return n

lambda_p = 0.4049  # μm
lambda_s = 0.810   # μm
lambda_i = 0.810   # μm
Lambda = 9.825     # μm

def phase_mismatch(T):
    kp = sellmeier_e(lambda_p, T) / lambda_p
    ks = sellmeier_e(lambda_s, T) / lambda_s
    ki = sellmeier_o(lambda_i, T) / lambda_i
    dq = kp - ks - ki - 1/Lambda
    return dq

temps = np.linspace(20, 100, 500)
mismatch = [phase_mismatch(T) for T in temps]

# 찾기
T_opt = temps[np.argmin(np.abs(mismatch))]
print(f"위상 일치 온도 ≈ {T_opt:.2f} °C")
