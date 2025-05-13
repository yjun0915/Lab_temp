import sympy
from sympy.physics.units import speed_of_light as c
from sympy.physics.units import meter, second
from sympy.physics.units import convert_to
sympy.init_printing()

pump = sympy.symbols(names='pump', real=True)
signal = sympy.symbols(names='signal', real=True)
idler = sympy.symbols(names='idler', real=True)
temp = sympy.symbols(names='temp', real=True)
length = sympy.symbols(names='L', real=True)
period = sympy.symbols(names='Λ', real=True)

joint_spectral_amplitude = sympy.Function(name='A')(signal, idler, temp)
pump_spectrum = sympy.Function(name='α')(signal, idler)
phase_matching = sympy.Function(name='Φ')(length, signal, idler, temp)
wavevector_mismatch = sympy.Function(name='Δk')(signal, idler, temp)

class GeneralFunction(sympy.Function):
    @classmethod
    def refractive_index(cls, w, t):
        wavelength_um = w / 1000.0
        ΔT = t - 25.0

        A0, A1 = 1.14886, 1e-4
        B0, B1 = 5.69293, 1e-3
        C0, C1 = -2.42924, 1e-3

        A = A0 + A1 * ΔT
        B = B0 + B1 * ΔT
        C = C0 + C1 * ΔT

        λ2 = wavelength_um**2
        n_squared = A + B / (λ2 - C)
        return n_squared**0.5
    @classmethod
    def wavevector(cls, w, t):
        return GeneralFunction.refractive_index(w, t)*t/convert_to(expr=c, target_units=[meter, second])

if __name__ == '__main__':
    global pump, signal, idler, temp, length, period
    global joint_spectral_amplitude, pump_spectrum, phase_matching, wavevector_mismatch

    wavevector = GeneralFunction.wavevector

    wavevector_mismatch = (
        wavevector(pump, temp) - wavevector(pump/2, temp)
        - wavevector(pump/2, temp)
    )
    phase_matching = sympy.sinc(wavevector_mismatch*length/2)

    sympy.pprint(wavevector_mismatch)