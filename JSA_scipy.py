import sympy
from sympy import diff
from sympy import pi
from sympy.physics.units import speed_of_light
from sympy.physics.units import nanometer, micrometer, millimeter, meter, second
from sympy.physics.units import convert_to
sympy.init_printing()

pump = 405.4358                                     # nanometer
signal = sympy.symbols(names='signal', real=True)
idler = sympy.symbols(names='idler', real=True)
temp = 109.88                                       # degrees celsius
length = 10e6                                       # millimeter
period = 9.825e3                                    # micrometer

length = length*(1 + 6.7e-6*(temp-25) + 11e-9*(temp-25)**2)     # thermal expansion

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
        return GeneralFunction.refractive_index(w, t)*t/299792485e9


k_p = GeneralFunction.wavevector(w=pump, t=temp)
k_s = GeneralFunction.wavevector(w=signal, t=temp)
k_i = GeneralFunction.wavevector(w=idler, t=temp)

if __name__ == '__main__':
    pump_spectrum = sympy.exp(1)

    wavevector = GeneralFunction.wavevector
    wavevector_mismatch = (
        k_p - k_s
        - k_i + (2*pi/period)
    )
    phase_matching = sympy.sinc(wavevector_mismatch*length/2)
    sympy.plotting.plot3d(phase_matching, (signal, 2*pi*299792485e9/700, 2*pi*299792485e9/920), (idler, 2*pi*299792485e9/700, 2*pi*299792485e9/920))
