"""Deterministic synthetic AC waveforms for demonstrations and tests."""

from __future__ import annotations

from math import pi, sin, sqrt
from random import Random


def generate_ac_waveforms(
    duration_s: float = 0.5,
    sample_rate_hz: float = 4_000.0,
    frequency_hz: float = 60.0,
    voltage_rms: float = 120.0,
    current_rms: float = 5.0,
    phase_degrees: float = 20.0,
    noise_rms: float = 0.0,
    seed: int = 7,
) -> tuple[list[float], list[float]]:
    if min(duration_s, sample_rate_hz, frequency_hz, voltage_rms) <= 0:
        raise ValueError("duration, rate, frequency, and voltage must be positive")
    if current_rms < 0 or noise_rms < 0:
        raise ValueError("current and noise RMS values cannot be negative")
    sample_count = max(8, round(duration_s * sample_rate_hz))
    voltage_peak = voltage_rms * sqrt(2.0)
    current_peak = current_rms * sqrt(2.0)
    phase_radians = phase_degrees * pi / 180.0
    rng = Random(seed)
    voltage: list[float] = []
    current: list[float] = []
    for index in range(sample_count):
        time_s = index / sample_rate_hz
        angle = 2.0 * pi * frequency_hz * time_s
        voltage.append(voltage_peak * sin(angle) + rng.gauss(0.0, noise_rms))
        current.append(current_peak * sin(angle - phase_radians))
    return voltage, current
