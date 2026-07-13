'''

Energy constant models an eye-safe system, whereas a peak power constant models when the
limit is instantaneous (not predetermined) for example for driver current limits, fibre nonlinearities, and diode limits.

FWHM, \tau = 2*sqrt(2*ln(2))*\sigma
          
'''

import numpy as np
import matplotlib.pyplot as plt

def gaussian_pulse(t, E, t0, sigma):
    """Gaussian optical pulse, energy-normalised.

    Parameters
    ----------
    t : array, time grid [s]
    E : float, pulse energy [J]
    t0 : float, pulse centre time [s]
    sigma : float, RMS width [s]. FWHM = 2*sqrt(2*ln 2)*sigma.

    Returns
    -------
    array, instantaneous power P(t) [W]. Integrates to E.
    Peak power = E / (sigma * sqrt(2*pi)).
    """
    return (E / (sigma * np.sqrt(2 * np.pi))) * np.exp(-(t - t0)**2 / (2 * sigma**2))

t = np.linspace(-50e-9, 50e-9, 10001)
P = gaussian_pulse(t, E=1e-6, t0=0, sigma=5e-9)
print(np.trapz(P, t))

plt.plot(t * 1e9, P)
plt.xlabel("Time (ns)")
plt.ylabel("P(t) (W)")
plt.grid()
plt.title("Gaussian pulse, E = 1 μJ, σ = 5 ns")
plt.savefig("Gaussian pulse")
plt.show()


