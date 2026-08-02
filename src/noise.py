import numpy as np
from scipy.constants import h, c



def photons_from_energy(E, lam):
    """
    Converts a pulse energy into photon number

    Parameters
    ----------
    E : float
        Optical pulse energy [J].
    lam : float
        Photon wavelength [m].

    Returns
    -------
    n : float
        Expected number of photons [counts, dimensionless].

    The photon number is calculated using:

        n = E * λ / (h * c)
    """
    n = (E*lam)/(h * c)
    return n


def detected_counts(mu_s, mu_d, mu_b, sigma_th, rng, size=None):
    """
    Generate simulated detector measurements including independent noise sources.

    Parameters
    ----------
    mu_s : float
        Mean signal photon count [counts, dimensionless].

    mu_d : float
        Mean dark count contribution [counts, dimensionless].

    mu_b : float
        Mean background photon count contribution [counts, dimensionless].

    sigma_th : float
        Thermal noise standard deviation [equivalent counts].
        Thermal variance contribution is sigma_th^2.

    rng : numpy.random.Generator
        Random number generator.

    size : int or tuple, optional
        Number of detector samples to generate. If None, returns a single
        detector measurement.

    Returns
    -------
    N : ndarray or float
        Simulated detector output [counts, dimensionless].

    Notes
    -----
    Photon contributions are independent Poisson processes:

        N_photon ~ Poisson(mu_s + mu_d + mu_b)

    Thermal noise is Gaussian:

        N_thermal ~ Normal(0, sigma_th)

    Total variance:

        σ² = μ_s + μ_d + μ_b + σ²_th
    """

    photon_counts = rng.poisson(mu_s + mu_d + mu_b, size=size)
    thermal_noise = rng.normal(0, sigma_th, size=size)

    return photon_counts + thermal_noise


def main():
    """
    Run a Monte Carlo simulation of detector count statistics.

    Generates repeated detector measurements using fixed parameters and
    compares the sampled mean and variance against theoretical expectations.

    The detector variance follows:

        σ² = μ_s + μ_d + μ_b + σ²_th

    mu_d = 10 counts is chosen as a representative value, rather than fixed constant
    mu_b = 100, moderate background level

    where each contribution can be independently zeroed by setting its
    corresponding mean count or noise parameter to zero.
    """
    seed = 1
    rng = np.random.default_rng(seed)

    mu_s = 6800
    mu_d = 10
    mu_b = 100
    sigma_th = 50

    samples = 10**5

    counts = detected_counts(
        mu_s,
        mu_d,
        mu_b,
        sigma_th,
        rng,
        size=samples
    )

    # Signal only: Poisson fingerprint, mean ≈ variance ≈ mu_s
    counts_s = detected_counts(6800, 0, 0, 0, rng, size=samples)
    print(f"signal-only  mean={np.mean(counts_s):.1f}  var={np.var(counts_s, ddof=1):.1f}  (expect ~6800 for both)")

    # Thermal only: pure Gaussian, mean ≈ 0, var ≈ sigma_th²
    counts_t = detected_counts(0, 0, 0, 50, rng, size=samples)
    print(f"thermal-only mean={np.mean(counts_t):.2f}  var={np.var(counts_t, ddof=1):.1f}  (expect 0, 2500)")

    print("Detected counts")
    print(f"Sample mean     = {np.mean(counts):.2f}")
    print(f"Sample variance = {np.var(counts, ddof=1):.2f}")

    print("\nExpected values")
    print(f"Mean            = {mu_s + mu_d + mu_b}")
    print(f"Variance        = {mu_s + mu_d + mu_b + sigma_th**2}")

if __name__ == "__main__":
    main()