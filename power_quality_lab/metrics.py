"""Electrical measurements for equally spaced voltage and current samples."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import sqrt
from statistics import fmean
from typing import Sequence


@dataclass(frozen=True)
class ElectricalMetrics:
    voltage_rms: float
    current_rms: float
    active_power_w: float
    apparent_power_va: float
    power_factor: float
    frequency_hz: float | None
    condition: str

    def to_dict(self) -> dict[str, float | str | None]:
        return asdict(self)


def _validate_samples(voltage: Sequence[float], current: Sequence[float]) -> None:
    if len(voltage) != len(current):
        raise ValueError("voltage and current must contain the same number of samples")
    if len(voltage) < 8:
        raise ValueError("at least eight samples are required")


def rms(samples: Sequence[float]) -> float:
    if not samples:
        raise ValueError("samples cannot be empty")
    return sqrt(fmean(sample * sample for sample in samples))


def estimate_frequency(voltage: Sequence[float], sample_rate_hz: float) -> float | None:
    if sample_rate_hz <= 0:
        raise ValueError("sample_rate_hz must be positive")
    crossings: list[float] = []
    for index in range(1, len(voltage)):
        previous = voltage[index - 1]
        present = voltage[index]
        if previous <= 0 < present:
            fraction = -previous / (present - previous) if present != previous else 0.0
            crossings.append((index - 1 + fraction) / sample_rate_hz)
    if len(crossings) < 2:
        return None
    periods = [later - earlier for earlier, later in zip(crossings, crossings[1:])]
    mean_period = fmean(periods)
    return 1.0 / mean_period if mean_period > 0 else None


def classify_condition(
    voltage_rms: float,
    power_factor: float,
    nominal_voltage: float,
) -> str:
    if voltage_rms < nominal_voltage * 0.90:
        return "voltage_sag"
    if voltage_rms > nominal_voltage * 1.10:
        return "voltage_swell"
    if power_factor < 0.80:
        return "low_power_factor"
    return "normal"


def analyse_window(
    voltage: Sequence[float],
    current: Sequence[float],
    sample_rate_hz: float,
    nominal_voltage: float = 120.0,
) -> ElectricalMetrics:
    _validate_samples(voltage, current)
    if nominal_voltage <= 0:
        raise ValueError("nominal_voltage must be positive")

    voltage_rms = rms(voltage)
    current_rms = rms(current)
    active_power = fmean(v * i for v, i in zip(voltage, current))
    apparent_power = voltage_rms * current_rms
    power_factor = abs(active_power) / apparent_power if apparent_power else 0.0
    power_factor = min(1.0, power_factor)
    frequency = estimate_frequency(voltage, sample_rate_hz)
    condition = classify_condition(voltage_rms, power_factor, nominal_voltage)

    return ElectricalMetrics(
        voltage_rms=round(voltage_rms, 3),
        current_rms=round(current_rms, 3),
        active_power_w=round(active_power, 3),
        apparent_power_va=round(apparent_power, 3),
        power_factor=round(power_factor, 4),
        frequency_hz=round(frequency, 3) if frequency is not None else None,
        condition=condition,
    )

