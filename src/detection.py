import numpy as np
from scipy.constants import c
from scipy.special import erfcinv
import matplotlib.pyplot as plt
from pulse import gaussian_pulse

def range_from_tof(t):
    """
    Convert one way time of flight to range.

    Parameters:
    t: time (s)
    """

    return (c / 2.0) * t

def matched_filter(waveform, template, dt):
    """
    Discrete matched filter and correlation

    Returns
    corr: ndarray
        Full corellation output
    lag_times : ndarray
        Time corresponding to each correlation sample
    
    """

    waveform = np.asarray(waveform)
    template = np.asarray(template)

    corr = np.correlate(waveform, template, mode = "full")

    n = len(waveform)
    m = len(template)

    # For mode='full', correlation index k maps to
    #
    #     L = k - (m - 1)
    #
    # where L is the lag of template element 0.
    #
    # The template centre is at index (m - 1)/2, so when the
    # pulse centre aligns with the template centre:
    #
    #     t_ToF = L*dt + ((m - 1)/2)*dt
    #
    # Here the template spans -5*sigma_p ... +5*sigma_p,
    # so ((m - 1)/2)*dt = 5*sigma_p.
    #
    # Therefore, after finding k_hat:
    #
    #     L_hat = k_hat - (m - 1)
    #     t_hat = L_hat*dt + ((m - 1)/2)*dt

    lags = np.arange(-(m - 1), n) * dt
    return corr, lags


def threshold_detect(waveform, V, dt):
    """
    Returns the first threshold crossing time

    Rturns None if never detects threshold cross
    """
    crossings = np.flatnonzero(waveform >= V)
    if len(crossings) == 0:
        return None
    first = crossings[0]
    return first * dt

def main():

    sigma_p = 10e-9
    dt = 0.5e-9 #sampling


    true_range = 100.0
    true_tof = 2.0 * true_range / c

    t_end = true_tof + 6.0 * sigma_p
    t = np.arange(0.0, t_end, dt)

    E = 1.0
    clean_waveform = gaussian_pulse(
        t,
        t0=true_tof,
        sigma=sigma_p,
        E=E,
    )

    template_t = np.arange(
        -5.0 * sigma_p,
        5.0 * sigma_p + dt,
        dt,
    )

    template = gaussian_pulse(
        template_t,
        t0=0.0,
        sigma=sigma_p,
        E=E,
    )

    P_peak = E / (sigma_p * np.sqrt(2.0 * np.pi))

    target_SNR = 20

    # SNR = P_peak / sigma_n
    sigma_n = P_peak / target_SNR
    M = len(t)

    target_window_PFA = 1e-2

    # Small-P approximation:
    #     P_FA,window ~= M * P_FA,sample
    # therefore
    #     P_FA,sample ~= P_FA,window / M
    per_sample_PFA = target_window_PFA / M

    # P_FA = 1/2 erfc(k/sqrt(2))
    # Therefore:
    #     k = sqrt(2) * erfcinv(2 * P_FA)
    k = np.sqrt(2.0) * erfcinv(2.0 * per_sample_PFA)

    V = k * sigma_n


    print("--- Simulation setup ---")
    print(f"True range:              {true_range:.3f} m")
    print(f"Pulse width sigma_p:     {sigma_p * 1e9:.2f} ns")
    print(f"Sampling interval dt:    {dt * 1e9:.2f} ns")
    print(f"Peak amplitude:          {P_peak:.6g}")
    print(f"Target SNR:              {target_SNR:.1f}")
    print(f"Noise sigma:             {sigma_n:.6g}")
    print(f"Samples/window M:        {M}")
    print(f"Target window P_FA:      {target_window_PFA:.3g}")
    print(f"Per-sample P_FA:         {per_sample_PFA:.3g}")
    print(f"Threshold k:             {V / sigma_n:.2f}")
    print(f"Threshold V:             {V:.6g}")


#-------------------------Monte Carlo-------------------------------

    n_shots = 5000

    threshold_ranges = []
    threshold_times = []
    matched_ranges = []
    matched_times = []

    rng = np.random.default_rng(1)

    true_detection_ranges = []
    false_alarm_ranges = []

    for _ in range(n_shots):
        noise = rng.normal(
            loc=0.0,
            scale=sigma_n,
            size=len(t),
        )        

        waveform = clean_waveform + noise


        threshold_t = threshold_detect(waveform, V, dt)

        if threshold_t is not None:
            threshold_times.append(threshold_t)

            threshold_range = range_from_tof(threshold_t)
            threshold_ranges.append(threshold_range)

            # A detection is considered true if it occurs within
            # +/- 10 sigma_p of the expected pulse arrival.
            if abs(threshold_t - true_tof) <= 10.0 * sigma_p:
                true_detection_ranges.append(threshold_range)
            else:
                false_alarm_ranges.append(threshold_range)


        corr, lag_times = matched_filter(waveform, template, dt)
        k_hat = np.argmax(corr)

        # Sub-sample peak interpolation:
        # standard three-point parabolic-vertex formula (looked up).
        y_minus = corr[k_hat - 1]
        y_zero = corr[k_hat]
        y_plus = corr[k_hat + 1]

        denom = y_minus - 2.0 * y_zero + y_plus

        if denom != 0.0:
            delta = 0.5 * (y_minus - y_plus) / denom
        else:
            delta = 0.0

        # lag_times[k_hat] is the lag referenced to
        # template element 0. Add the template-centre
        # offset to obtain the pulse-centre ToF.
        template_centre_offset = (
            (len(template) - 1) / 2.0
        ) * dt

        matched_t = (
            lag_times[k_hat]
            + delta * dt
            + template_centre_offset
        )

        matched_times.append(matched_t)
        matched_ranges.append(
            range_from_tof(matched_t)
        )
    threshold_ranges = np.asarray(threshold_ranges)
    matched_ranges = np.asarray(matched_ranges)
    matched_times = np.asarray(matched_times)

    true_detection_ranges = np.asarray(true_detection_ranges)
    false_alarm_ranges = np.asarray(false_alarm_ranges)
    threshold_times = np.asarray(threshold_times)

    print("\nThreshold detector (true detections vs false alarms):")
    print(f"  true detections: {len(true_detection_ranges)}")
    print(f"  false alarms:    {len(false_alarm_ranges)}")

    if len(true_detection_ranges) > 1:
        print(
            f"  cluster mean:    "
            f"{np.mean(true_detection_ranges):.4f} m"
        )
        print(
            f"  cluster sigma_R: "
            f"{np.std(true_detection_ranges, ddof=1):.4f} m"
        )

    print(
        f"  FA rate:          "
        f"{len(false_alarm_ranges) / n_shots:.4f}"
    )


    plt.figure()
    plt.hist(threshold_ranges, bins=80)
    plt.axvline(
        true_range,
        linestyle="--",
        label="true range",
    )
    plt.xlabel("Estimated range (m)")
    plt.ylabel("Count")
    plt.title("Threshold detections: true detections + false alarms")
    plt.legend()
    plt.show()

    print("\n--- Monte Carlo results ---")

    if len(threshold_ranges):
        threshold_mean = np.mean(threshold_ranges)
        threshold_std = np.std(
            threshold_ranges,
            ddof=1,
        )

        print("\nThreshold detector (all detections, including false alarms):")
        print(f"  detections: {len(threshold_ranges)}/{n_shots}")
        print(f"  mean range: {threshold_mean:.4f} m")
        print(
            f"  bias:       "
            f"{threshold_mean - true_range:.4f} m"
        )
        print(f"  sigma_R:    {threshold_std:.4f} m")

    matched_mean = np.mean(matched_ranges)
    matched_std = np.std(
        matched_ranges,
        ddof=1,
    )

    matched_bias_mm = (matched_mean - true_range) * 1e3
    matched_se_mm = matched_std / np.sqrt(n_shots) * 1e3

    print("\nMatched filter:")
    print(f"  mean range: {matched_mean:.4f} m")
    print(f"  bias:       {matched_bias_mm:.2f} ± {matched_se_mm:.2f} mm")
    print(f"  sigma_R:    {matched_std * 1e3:.2f} mm")

    u = np.sqrt(2.0 * np.log(P_peak / V))
    predicted_sigma_t = np.sqrt((sigma_p / (target_SNR * u * np.exp(-u**2 / 2.0)))**2 + dt**2 / 12.0)

    predicted_sigma_R = range_from_tof(
        predicted_sigma_t)

    measured_sigma_t = (
        np.std(true_detection_ranges, ddof=1)
        / (c / 2.0) )
    signal_derivative = (
        (t - true_tof)
        / sigma_p**2
        * clean_waveform
    )

    fisher_information = (
        np.sum(signal_derivative**2)
        / sigma_n**2
    )

    crlb_sigma_t = 1.0 / np.sqrt(fisher_information)

    crlb_sigma_R = range_from_tof(
        crlb_sigma_t
    )

    print("\nCramér-Rao lower bound:")
    print(
        f"  sigma_t:    "
        f"{crlb_sigma_t * 1e9:.4f} ns"
    )
    print(
        f"  sigma_R:    "
        f"{crlb_sigma_R:.4f} m"
    )

    print("\nMatched filter / CRLB:")
    print(
        f"  ratio:      "
        f"{matched_std / crlb_sigma_R:.3f}x"
    )
    print(
        f"  trials:     "
        f"{n_shots}"
    )


    print("\nEdge-trigger prediction:")
    print(
        f"  predicted sigma_t: "
        f"{predicted_sigma_t * 1e9:.4f} ns"
    )
    print(
        f"  measured sigma_t:  "
        f"{measured_sigma_t * 1e9:.4f} ns"
    )
    print(
        f"  predicted sigma_R: "
        f"{predicted_sigma_R:.4f} m"
    )

if __name__ == "__main__":
    main()

