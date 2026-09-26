# LiDAR Range Simulator

A simulator for investigating the limits of a pulsed LiDAR range estimation, using optical pulse generation, atmospheric/target propagation, detector noise, and time-of-flight estimation.


The optical pulse generation uses a energy normalised gaussian laser pulse. The atmospheric/target propagation uses a Lambertian target with geometric spreadng and atmospheric extinction. The photon-counting and electronic noise sources and range estimation uses thershold detection and matched filtering.
This project is connected to statistical estimation using Monte Carlo measurements to compare analytical timing-jitter limits and the Cramer-Rao lower bound. The matched-filter estimator achieves timing jitter close to the CRLB in the tested SNR regime. This reproduces the expected behaviour of an optimal waveform-based estimator.

## Overview

The simulator is compiled through four modules deliberately separated so the signal, propagation loss, detector statistics, and estimation can be developed and tseted independently.

Pulse model, pulse.py |
Propagation, propagation.py |
Noise, noise.py |
Detection, detection.py

## 1. Pulse model — `src/pulse.py`

The transmitted LiDAR pulse is modelled as a Gaussian optical pulse
$$P(t) = \frac{E}{\sigma_p\sqrt{2\pi}} \exp\left[-\frac{(t-t_0)^2}{2\sigma_p^2}\right]$$

where $E$ is the pulse energy, 

$t_0$ the pulse centre,

 and $\sigma_p$ the RMS width, 

so that $\int P(t)\,dt = E$,
$P_\text{peak} = E/(\sigma_p\sqrt{2\pi})$ and 

$\text{FWHM} = 2\sqrt{2\ln 2}\,\sigma_p$.

## 2. Propagation model — `src/propagation.py`


## 3. Detector noise — `src/noise.py`

### Photon statistics


### Range dependence


## 4. Detection and estimation — `src/detection.py`

### Threshold detection


### Matched filtering


# Key result

## Timing precision and range


## Analytical scaling


## Repository structure

### `src/pulse.py`

Generates energy-normalised Gaussian optical pulses.

### `src/propagation.py`

Models target reflection, geometric spreading and atmospheric extinction.

### `src/noise.py`

Models photon statistics, dark counts, background photons and Gaussian thermal noise.

### `src/detection.py`

Implements threshold detection, matched filtering, sub-sample timing estimation and Monte Carlo performance analysis.

### `docs/module4-theory.md`

Contains the analytical derivations behind timing jitter, threshold statistics, pulse-width scaling, time walk and matched-filter estimation.

## Running the simulator


## Example simulation parameters


## Current scope


## Future work

## Motivation

The aim of the project is not simply to simulate whether a LiDAR pulse can be detected. It is to investigate **how accurately the arrival time can fundamentally be estimated from a noisy optical return**, and how that precision follows from the underlying physics and statistics.

