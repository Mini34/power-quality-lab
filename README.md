# Power Quality Lab

[![Tests](https://github.com/Mini34/power-quality-lab/actions/workflows/test.yml/badge.svg)](https://github.com/Mini34/power-quality-lab/actions/workflows/test.yml)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)

A standard-library electrical engineering project that converts sampled voltage and
current waveforms into measurable power-quality evidence.

## What it measures

- RMS voltage and current
- Active and apparent power
- Power factor from simultaneous voltage/current samples
- Frequency using interpolated positive-going zero crossings
- Voltage sag, voltage swell, and low-power-factor conditions

## Run it

```powershell
python -m pip install .
power-quality --scenario normal
power-quality --scenario sag

# The module form works without installation from the repository root.
python -m power_quality_lab.cli --scenario normal
python -m power_quality_lab.cli --scenario sag
python -m power_quality_lab.cli --scenario low-pf
python -m unittest discover -s tests -v
```

Example:

```json
{
  "scenario": "normal",
  "voltage_rms": 120.0,
  "current_rms": 5.0,
  "active_power_w": 563.816,
  "apparent_power_va": 600.0,
  "power_factor": 0.9397,
  "frequency_hz": 60.0,
  "condition": "normal"
}
```

| Classification | Explicit threshold at 120 V nominal |
| --- | --- |
| Voltage sag | Below 108 V RMS |
| Normal voltage | 108–132 V RMS |
| Voltage swell | Above 132 V RMS |
| Low power factor | Below 0.80 when voltage is within range |

## Engineering decisions

- Simultaneous samples preserve the phase relationship needed for active power and power factor.
- Interpolated crossings reduce frequency error compared with using sample indices alone.
- Classification thresholds are explicit and easy to replace with a utility or standards-based profile.
- Synthetic signals are deterministic, making failures reproducible in tests and CI.

## Limitations and next hardware step

This repository is a simulation and signal-processing lab, not a certified power-quality
instrument. It does not model ADC quantization, sensor isolation, harmonics, calibration
drift, or electrical safety. A physical version would require isolated voltage/current
sensing, protection, calibration against a trusted meter, and a safe low-voltage test
setup before any mains-connected work.
