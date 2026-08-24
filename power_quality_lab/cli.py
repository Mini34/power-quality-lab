"""Command-line demonstration for the power-quality lab."""

from __future__ import annotations

import argparse
import json

from .metrics import analyse_window
from .synthetic import generate_ac_waveforms

SCENARIOS = {
    "normal": (120.0, 20.0),
    "sag": (95.0, 20.0),
    "swell": (140.0, 20.0),
    "low-pf": (120.0, 55.0),
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyse a deterministic AC waveform")
    parser.add_argument("--scenario", choices=SCENARIOS, default="normal")
    parser.add_argument("--frequency", type=float, default=60.0)
    parser.add_argument("--sample-rate", type=float, default=4_000.0)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    voltage_rms, phase_degrees = SCENARIOS[args.scenario]
    voltage, current = generate_ac_waveforms(
        voltage_rms=voltage_rms,
        phase_degrees=phase_degrees,
        frequency_hz=args.frequency,
        sample_rate_hz=args.sample_rate,
    )
    result = analyse_window(voltage, current, args.sample_rate)
    print(json.dumps({"scenario": args.scenario, **result.to_dict()}, indent=2))


if __name__ == "__main__":
    main()

