import math
import unittest

from power_quality_lab.metrics import analyse_window, estimate_frequency, rms
from power_quality_lab.synthetic import generate_ac_waveforms


class PowerQualityTests(unittest.TestCase):
    def test_rms_matches_known_sine_wave(self) -> None:
        samples = [math.sqrt(2) * math.sin(2 * math.pi * index / 1_000) for index in range(1_000)]
        self.assertAlmostEqual(rms(samples), 1.0, places=4)

    def test_normal_waveform_measurements(self) -> None:
        voltage, current = generate_ac_waveforms(phase_degrees=20.0)
        result = analyse_window(voltage, current, 4_000.0)
        self.assertAlmostEqual(result.voltage_rms, 120.0, delta=0.2)
        self.assertAlmostEqual(result.current_rms, 5.0, delta=0.05)
        self.assertAlmostEqual(result.power_factor, math.cos(math.radians(20)), delta=0.01)
        self.assertAlmostEqual(result.frequency_hz or 0.0, 60.0, delta=0.1)
        self.assertEqual(result.condition, "normal")

    def test_sag_and_swell_detection(self) -> None:
        sag_v, sag_i = generate_ac_waveforms(voltage_rms=95.0)
        swell_v, swell_i = generate_ac_waveforms(voltage_rms=140.0)
        self.assertEqual(analyse_window(sag_v, sag_i, 4_000.0).condition, "voltage_sag")
        self.assertEqual(analyse_window(swell_v, swell_i, 4_000.0).condition, "voltage_swell")

    def test_low_power_factor_detection(self) -> None:
        voltage, current = generate_ac_waveforms(phase_degrees=55.0)
        self.assertEqual(analyse_window(voltage, current, 4_000.0).condition, "low_power_factor")

    def test_frequency_requires_two_crossings(self) -> None:
        self.assertIsNone(estimate_frequency([1.0] * 20, 1_000.0))

    def test_synthetic_rms_inputs_cannot_be_negative(self) -> None:
        with self.assertRaises(ValueError):
            generate_ac_waveforms(current_rms=-1.0)
        with self.assertRaises(ValueError):
            generate_ac_waveforms(noise_rms=-0.1)


if __name__ == "__main__":
    unittest.main()
