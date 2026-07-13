'''
As a laser beam travels towards an object, the light spreads, is absorbed by the atmosphere, and is reflected from the target.

For atmospheric absorption, the Beer-Lambert law is applied: dP = -alphaPdr
which integrates into P(r) = P0 e^(-alphar)

The irradiance on a patch of the target is the power per unit area:
Einc = power/area = Pte^(-alphar)/Aspot

A Lambertian surface is defined by having constant radiance in every direction. The radiance L is given by
L = (1/costheta)*d^2P/dAdOmega

When integrated over the hemisphere, the total emitted power per unit area becomes M = pi L

Suppose the incoming irradiance is Einc. Only a fraction ρ is reflected, therefore
therefore M = rhoE = pi L, so L = rhoE/pi

For a small receiver aperture Ar, the solid angle subtended by the receiver is Omega_r = A_r/r^2

The power collected, P = LA_spotOmega_r which simplifies into
P = rhoP_te^(-alphar)Ar/pir^2

The reflected light must then travel back through the atmosphere, so the same attenuation occurs again, introducing another factor of e^-alphar

Therefore, the received power is P_r(r) = rhoP_te^(-2alphar)Ar/pir^2
          
'''

import numpy as np
import matplotlib.pyplot as plt


def received_power(P_t, r, rho, A_r, alpha, eta_r = 1.0):
    """
    Calculates the received optical power for a LiDAR system with a Lambertian target.

    The received power is computed using

        P_r = (rho * P_t * eta_r * A_r / (pi * r^2)) * exp(-2 * alpha * r)

    where the exponential term accounts for atmospheric attenuation on
    both the outbound and return paths.

    Parameters
    ----------
    P_t : float or ndarray
        Transmitted optical power (W).
    r : float or ndarray
        Target range (m).
    rho : float
        Target reflectivity (0 <= rho <= 1).
    A_r : float
        Receiver aperture area (m²).
    alpha : float
        Atmospheric extinction coefficient (m⁻¹).
    eta_r : float, optional
        Receiver optical efficiency (default is 1.0).

    Returns
    -------
    float or ndarray
        Received optical power (W).
    """
    return (rho*P_t*eta_r*np.exp(-2*alpha*r)*A_r)/(np.pi*r**2)


def main():
    r = np.linspace(10, 1000, 500)

    Pr_100 = received_power(80, 100, 0.1, 5e-4, 0)
    print(f"P_r at 100 m: {Pr_100:.3e} W")

    #Validating that log - log slope must be -2 when alpha = 0
    Pr_vac = received_power(80, r, 0.1, 5e-4, 0)
    slope = np.polyfit(np.log(r), np.log(Pr_vac), 1)[0]
    print(f"Slope (alpha=0): {slope:.6f}")

    #Real world case with atmospheric extinc
    # Extinction: Koschmieder alpha = 3.912/V with V = 26 km gives 0.15 /km at 550 nm.
    # Used unscaled at 905 nm -> conservative (slightly hazy) estimate,
    # since Kruse scaling would reduce it by about (550/905)^1.3.
    alpha = 1.5e-4 #alpha = 0.15 /km, clear air @ 905 nm, from
    Pr_atm = received_power(80, r, 0.1, 5e-4, alpha)

    plt.figure(figsize=(6, 4))
    plt.loglog(r, Pr_vac, label=r"$\alpha = 0$ (vacuum)")
    plt.loglog(r, Pr_atm, label=r"$\alpha = 1.5\times10^{-4}\,\mathrm{m^{-1}}$")
    plt.xlabel("Range (m)")
    plt.ylabel("Received Power (W)")
    plt.title("Received Power vs Range")
    plt.grid(True, which="both")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
