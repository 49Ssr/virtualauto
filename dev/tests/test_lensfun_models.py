from __future__ import annotations

import math
import unittest

from virtualauto.lensfun_models import (
    ReverseLensProfile,
    float32_le_sha256,
    generate_reverse_maps,
    modifier_normalization,
    rescale_ptlens,
)

PROFILE = ReverseLensProfile(
    focal_length_mm=85.0,
    crop_factor=1.0,
    calibration_aspect_ratio=1.5,
    ptlens_a=0.00984,
    ptlens_b=-0.0325,
    ptlens_c=0.0316,
    tca_vr=0.9999438,
    tca_vb=0.9999330,
    vignette_k1=-0.1757052864,
    vignette_k2=-0.0263920790,
    vignette_k3=0.0396991339,
)


class LensfunModelTests(unittest.TestCase):
    def test_normalization_matches_pinned_source_equation(self) -> None:
        scale, center_x, center_y = modifier_normalization(
            960,
            540,
            focal_length_mm=85.0,
            crop_factor=1.0,
        )
        self.assertAlmostEqual(scale, 0.0004621338661092104, places=15)
        self.assertAlmostEqual(center_x, 0.22159318879936638, places=15)
        self.assertAlmostEqual(center_y, 0.1245450769164322, places=15)

    def test_ptlens_rescaling_is_not_direct_database_polynomial(self) -> None:
        coefficients = rescale_ptlens(
            0.00984,
            -0.0325,
            0.0316,
            focal_length_mm=85.0,
            calibration_crop_factor=1.0,
            calibration_aspect_ratio=1.5,
        )
        expected = (
            3.6250027919958545,
            -1.675169959521534,
            0.22788978898810133,
        )
        for actual, target in zip(coefficients, expected, strict=True):
            self.assertAlmostEqual(actual, target, places=13)

    def test_small_reverse_maps_are_finite_symmetric_and_channel_ordered(self) -> None:
        maps = generate_reverse_maps(PROFILE, width=16, height=10)
        for values in maps.values():
            self.assertEqual(len(values), 16 * 10 * 4)
            self.assertTrue(all(math.isfinite(value) for value in values))
        red_corner = maps["red"][0]
        green_corner = maps["green"][0]
        blue_corner = maps["blue"][0]
        self.assertLess(blue_corner, red_corner)
        self.assertLess(red_corner, green_corner)
        opposite = ((10 - 1) * 16 + (16 - 1)) * 4
        self.assertAlmostEqual(
            maps["green"][opposite],
            1.0 - green_corner,
            places=6,
        )
        self.assertLess(maps["vignette"][0], 1.0)

    def test_f40_profile_960x540_has_frozen_source_exact_hashes(self) -> None:
        maps = generate_reverse_maps(PROFILE, width=960, height=540)
        expected = {
            "red": "02c9f3c8ad33900a2ce23d5d153f44f944dfa2d88bff7cf62d5c372e22fb46cd",
            "green": "63701f2fbf654981fecf3fde0fe91b734dbe69847bf2c788abb67119038e9b69",
            "blue": "77f7a127f88712aad21bf593e2a25b981b562c18b3efa006d807f8c65961665b",
            "vignette": (
                "2de60846a8384807cb9d99801524916c"
                "bec53eca0e5e5dd487cfa8bd0bee09a1"
            ),
        }
        for channel, target in expected.items():
            self.assertEqual(
                float32_le_sha256(maps[channel]),
                target,
            )


if __name__ == "__main__":
    unittest.main()
