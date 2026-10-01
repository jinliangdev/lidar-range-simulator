# Pulsed LiDAR Range Simulator
A modular Python simulator to study the limits of pulsed time of flight LiDAR ranging. This simulator attempts to characterise the arrival time of a noisy optical return to a degree of accuracy using underlying physics and statistics.

## Motivation

The aim of the project is not simply to simulate whether a LiDAR pulse can be detected. It is to investigate **how accurately the arrival time can fundamentally be estimated from a noisy optical return**, and how that precision follows from the underlying physics and statistics.

## Introduction
The optical pulse generation uses an energy normalised Gaussian laser pulse. The atmospheric/target propagation uses a Lambertian target with geometric spreading and atmospheric extinction. The signal, dark counts, and background noise are Poisson, thermal/electrical noise is Gaussian, and the range estimation is done through threshold detection and matched filtering.
This project uses Monte Carlo trials to compare analytical timing jitter limits and the Cramér-Rao lower bound. 

## Key Result
At SNR = 20, σ_p = 10 ns, and Δt = 0.5 ns, the matched filter achieved a 17.8mm range precision $\sigma_R$, which is 1.002 $\pm$ 0.010 $\times$ the CRLB over N = 5000 Monte Carlo trials. This has a bias of 0.3 $\pm$ 0.25mm in comparison to the fixed threshold detector with approximately 2.8m of bias and a 22$\times$ larger detection jitter.

In other words, this means that the matched filter is statistically efficient. It extracts all the timing information the physics allows whilst the simple threshold detector only focuses on a clipped amount.

To reproduce these results:

pip install -r requirements.txt
cd src
python detection.py


## Repository structure

The simulator is organised through four modules deliberately separated so the signal, propagation loss, detector statistics, and estimation can be developed and tested independently.

- `src/pulse.py` Gaussian pulse model
- `src/propagation.py` 	Radiometric link budget — Lambertian target, geometric spreading, Beer–Lambert attenuation
- `src/noise.py` Shot, dark count, background (Poission), and thermal (Gaussian) noise with a Monte Carlo check of each component.
- `src/detection.py` Threshold and matched filter estimation with a Monte Carlo benchmark and CRLB comparison.

## 1. Pulse model — `src/pulse.py`

The transmitted LiDAR pulse is modelled as a Gaussian optical pulse
$$P(t) = \frac{E}{\sigma_p\sqrt{2\pi}} \exp\left[-\frac{(t-t_0)^2}{2\sigma_p^2}\right]$$

where $E$ is the pulse energy, $t_0$ the pulse centre, and $\sigma_p$ the RMS width, 

so that $\int P(t)\,dt = E$,
$P_\text{peak} = E/(\sigma_p\sqrt{2\pi})$ and $\text{FWHM} = 2\sqrt{2\ln 2}\,\sigma_p$.

## 2. Propagation model — `src/propagation.py`
The propagation module analytically calculates the optical power returned from a diffuse Lambertian target, modelling diffuse reflection.

The received power is modelled as

$$P_r = \frac{
\rho P_t \eta_r A_r
}{
\pi r^2
}
e^{-2\alpha r}
$$

where 

- $P_t$ — transmitted optical power

- r — target range

- $\rho$ — target reflectivity

- $A_r$ — receiver aperture area

- $\eta_r$ — receiver optical efficiency

- $\alpha$ — atmospheric extinction coefficient

With the inverse square law representing geometric spreading through returned radiation, and the $e^{-2\alpha r}$ term representing atmospheric attenuation on both outward and inward paths.

Without atmospheric attenuation, the simulator numerically verifies that
$P_r\propto r^{-2}$. However, this is only valid when the beam lies entirely on the target, a target smaller than the beam footprint would give $\propto r^{-4}$

## 3. Detector noise — `src/noise.py`
The detector module uses independent photon counting and electronic noise sources

### Photon statistics
The expected number of detected signal photons $$\mu_s = \eta_q E_r \lambda/hc$$ and all means are counts per time bin, and $\sigma_{th}$ is in photoelectron units.

The detected signal however contains dark counts and background photons, which are treated as independent Poissonian events.
$$N_{\mathrm{photon}}
\sim
\mathrm{Poisson}
(\mu_s+\mu_d+\mu_b).$$

Therefore the model accounts for:

Signal photons - photons returned from target

Dark counts - thermally generated carriers

Background photons - from ambient optical background

Thermal electronic noise - modelled as Gaussian


This results in a detector output $N_{\mathrm{photon}} + N_{\mathrm{thermal}}$ with variance $\mu_s+\mu_d+\mu_b+\sigma_{\mathrm{th}}^2$


### Range dependence

Range dependence arises from the inverse square geometric spreading, with the signal decreasing approximately as $P_r\propto\frac{1}{r^2e^{2\alpha r}}$.

Whilst the simulator assumes that background and electronic noise is completely independent of range, the SNR falls with range because the signal falls against a range independent noise floor.

The key result is that $SNR \propto \frac{1}{r}$ when shot noise dominates, and $\propto \frac{1}{r^2}$ when background/thermal noise dominates. 

This leads to the motivation in studying the maximum usable detection range and detection statistics

## 4. Detection and estimation — `src/detection.py`

The detection module converts the measured flight time into a range, and compares two different timing estimators.

### Threshold detection
The simpler estimator records the first sample where
$x(t)\geq V$
The range is then obtained through 
$R=\frac{ct}{2}$.

The threshold detection is computationally simple, but the timing precision depends on the local pulse slope and threshold level. Noise can cause the threshold to be crossed earlier or later than the true pulse arrival.

For a Gaussian pulse, the linearised crossing gives

$$\sigma_t
\approx
\frac{\sigma_n}{|s'(t)|}$$

$$\sigma_t = \frac{\sigma_p}{\text{SNR}\,u\,e^{-u^2/2}}, \qquad u=\sqrt{2\ln(A/V)}$$
Note that $u=1$ gives $\sqrt{e}\,\sigma_p/\text{SNR}$.

Although a fixed threshold gives a bias dependent on amplitude, and therefore range, this inital estimation allows for an analytical comparison for the Monte Carlo simulation.
### Matched filtering

The second estimator correlates the received waveform with a known pulse template.

$$y[k] =\sum_n x[n]h[n-k]$$

then the estimated arrival time can be obtained from the max of the correlation
$\arg\max_k (y[k])$
and the CRLB on arrival time is 
$$\sigma_t = \frac{\sigma_p}{\text{SNR}}\sqrt{\frac{2\,\Delta t}{\sqrt{\pi}\,\sigma_p}}$$

This technique depends on the whole wave shape, not just a local slope which is efficient (attaining the CRLB) for known shape pulses in the presence of Gaussian noise, approximately so when signal dependent shot noise dominates.

## Status
This is an actively developed independent project and the core physics and main results are complete and reproducible. The below items are planned extensions to this project

Parameter sweeping for
SNR vs range,
,pulse width vs range resolution, and
background limited max range to test the performance of this simulator

Writeup for this project

Hardware validation using electronic components for a crude measurement to compare against simulation.

## Requirements

Python 3.10, with numpy, scipy, matplotlib (see requirements.txt)


