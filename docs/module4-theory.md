# Module 4 Theory

## 1. Timing jitter derivation

Pulse:

$$
s(t)=P_{\text{peak}}\exp\left(-\frac{(t-t_0)^2}{2\sigma_p^2}\right)
$$

with

$$
P_{\text{peak}}=\frac{E}{\sigma_p\sqrt{2\pi}}.
$$

Derivative:

$$
\frac{ds}{dt}
=
P_{\text{peak}}
\exp\left(-\frac{(t-t_0)^2}{2\sigma_p^2}\right)
\frac{t_0-t}{\sigma_p^2}.
$$

The magnitude of slope is max at the inflection points

$$
t=t_0\pm\sigma_p.
$$

Therefore,

$$
\left|\frac{ds}{dt}\right|_{\max}
=
\frac{P_{\text{peak}}e^{-1/2}}{\sigma_p}.
$$

Linearised timing jitter:

$$
\sigma_t\approx
\frac{\sigma_n}{|ds/dt|}.
$$

At the maximum-slope point,

$$
\sigma_t
\approx
\frac{\sigma_n\sigma_p}
{P_{\text{peak}}e^{-1/2}}
=
\sqrt e\,\sigma_p
\frac{\sigma_n}{P_{\text{peak}}}.
$$

Defining

$$
\mathrm{SNR}\equiv\frac{P_{\text{peak}}}{\sigma_n},
$$

gives

$$
\boxed{
\sigma_t=\sqrt e\,\frac{\sigma_p}{\mathrm{SNR}}
}
$$

and

$$
\sigma_R=\frac{c}{2}\sigma_t.
$$

For a crossing at a general fraction \(f\) of the peak,

$$
\sigma_t=
\frac{\sigma_n}{|s'(t_f)|}.
$$

The \(\sqrt e\) constant is the \(f=e^{-1/2}\) special case corresponding to the maximum-slope crossing.

---

## 2. Scaling predictions, fixed \(E\)

### Shot limited

With fixed \(E\), the detected signal photon number \(N_s\) is fixed. Therefore the shot noise level is fixed while

$$
P_{\text{peak}}\propto\frac{N_s}{\sigma_p}.
$$

Hence

$$
\mathrm{SNR}\propto\frac{1}{\sigma_p},
$$

and

$$
\sigma_R\propto
\frac{\sigma_p}{\mathrm{SNR}}
\propto\sigma_p^2.
$$

$$
\boxed{\sigma_R\propto\sigma_p^2}
$$

### Background-limited

For a detection window whose duration scales with pulse width,

$$
\sigma_n\propto\sqrt{\sigma_p}.
$$

Since

$$
P_{\text{peak}}\propto\frac{N_s}{\sigma_p},
$$

then

$$
\mathrm{SNR}\propto
\frac{N_s/\sigma_p}{\sqrt{\sigma_p}}
=
\frac{N_s}{\sigma_p^{3/2}}.
$$

Therefore

$$
\sigma_R\propto
\frac{\sigma_p}{\mathrm{SNR}}
\propto\sigma_p^{5/2}.
$$

$$
\boxed{\sigma_R\propto\sigma_p^{5/2}}
$$

**These are predictions to be tested in the parameter sweeps.**

---

## 3. Threshold statistics

For no signal present,

$$
X=N_P+N_{\text{th}},
$$

where

$$
N_P\sim\operatorname{Poisson}(110),
\qquad
N_{\text{th}}\sim\mathcal N(0,50^2).
$$

The Poisson standard deviation is

$$
\sigma_P=\sqrt{110}\approx10.5.
$$

Compared with the threshold-noise standard deviation,

$$
\frac{\sigma_P}{\sigma_{\text{th}}}
=
\frac{\sqrt{110}}{50}
\approx0.21.
$$

Thus the Poisson fluctuation is only about **21%** of the Gaussian threshold-noise standard deviation, and the total is well approximated by a Gaussian:

$$
X\approx\mathcal N(110,2610).
$$

Therefore,

$$
\mu_{\text{noise}}=110,
$$

$$
\sigma_{\text{noise}}
=
\sqrt{110+50^2}
=
\sqrt{2610}
\approx51.1.
$$

For threshold \(V\),

$$
P_{\text{FA}}
=
P(X>V)
=
\frac12
\operatorname{erfc}
\left(
\frac{V-\mu_{\text{noise}}}
{\sqrt2\,\sigma_{\text{noise}}}
\right).
$$

Writing

$$
V=\mu_{\text{noise}}+k\sigma_{\text{noise}},
$$

gives

$$
\boxed{
P_{\text{FA}}
=
\frac12\operatorname{erfc}
\left(\frac{k}{\sqrt2}\right)
}
$$

and inversion gives

$$
\boxed{
k=\sqrt2\,\operatorname{erfcinv}(2P_{\text{FA}})
}.
$$

For

$$
P_{\text{FA}}=10^{-4},
$$

$$
\boxed{k=3.72}.
$$

For \(M\) independent samples in a detection window,

$$
\boxed{
P_{\text{FA,win}}
\approx
M P_{\text{FA,sample}}
}
$$

in the small-probability limit.

---

## 4. Matched filter commitments

### Discrete operation

Correlate the sampled received waveform \(x[n]\) with the known sampled pulse template \(h[n]\):

$$
y[k]
=
\sum_n x[n]h[n-k].
$$

### ToF extraction

Find the lag corresponding to the maximum correlator output:

$$
\hat{k}=\arg\max_k y[k].
$$

Convert the peak lag to the pulse-centre ToF, including the template-centre offset.

### Predicted effect on \(\sigma_R\)

The matched filter should give a **smaller \(\sigma_R\) constant than the \(\sqrt e\) edge-trigger result**, because it uses the information in the **whole waveform** rather than a single threshold crossing.

### Walk error

The threshold detector is expected to have a negative bias because it triggers on the rising edge before \(t_0\). For

$$
V=0.217P_{\text{peak}},
$$

the clean Gaussian crossing satisfies

$$
e^{-u^2/(2\sigma_p^2)}=0.217,
$$

so

$$
\frac{|u|}{\sigma_p}
=
\sqrt{-2\ln(0.217)}
\approx1.75.
$$

For \(\sigma_p=10\,\mathrm{ns}\),

$$
\Delta R_{\text{walk}}
=
-\frac{c}{2}(1.75\sigma_p)
\approx-2.6\,\mathrm{m}.
$$

The measured bias can be more negative because of noise-induced early triggering.

### False-alarm mixture

False alarms occurring before the true pulse produce early range estimates. Mixing these rare catastrophic errors with genuine detections can dominate the measured \(\sigma_R\), so **detection statistics and conditional estimation precision must be reported separately**.
