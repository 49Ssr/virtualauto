"""Small, source-pinned Lensfun model reproductions used by VirtualAuto.

This module does not wrap Lensfun or claim general profile support. It preserves
the coordinate normalization, PTLens, poly3 TCA, and PA vignetting equations
audited at Lensfun commit 698a39eea69be00f4f25b6da6c1ad34b1f162b50.
"""

from __future__ import annotations

import hashlib
import math
import sys
from array import array
from dataclasses import dataclass

NEWTON_EPSILON = 0.00001
FULL_FRAME_DIAGONAL_MM = math.hypot(36.0, 24.0)


def float32_le_sha256(values: array) -> str:
    """Hash native float32 values using a canonical little-endian byte order."""
    canonical = values
    if sys.byteorder != "little":
        canonical = array("f", values)
        canonical.byteswap()
    return hashlib.sha256(canonical.tobytes()).hexdigest()


@dataclass(frozen=True)
class ReverseLensProfile:
    focal_length_mm: float
    crop_factor: float
    calibration_aspect_ratio: float
    ptlens_a: float
    ptlens_b: float
    ptlens_c: float
    tca_vr: float
    tca_vb: float
    vignette_k1: float
    vignette_k2: float
    vignette_k3: float


def modifier_normalization(
    width: int,
    height: int,
    *,
    focal_length_mm: float,
    crop_factor: float,
) -> tuple[float, float, float]:
    """Return Lensfun NormScale and the default centred lens origin."""
    if width < 2 or height < 2:
        raise ValueError("Lensfun maps require width and height of at least two")
    if focal_length_mm <= 0 or crop_factor <= 0:
        raise ValueError("Focal length and crop factor must be positive")
    pixel_width = float(width - 1)
    pixel_height = float(height - 1)
    norm_scale = (
        FULL_FRAME_DIAGONAL_MM
        / crop_factor
        / math.hypot(pixel_width + 1.0, pixel_height + 1.0)
        / focal_length_mm
    )
    return (
        norm_scale,
        pixel_width / 2.0 * norm_scale,
        pixel_height / 2.0 * norm_scale,
    )


def rescale_ptlens(
    a: float,
    b: float,
    c: float,
    *,
    focal_length_mm: float,
    calibration_crop_factor: float,
    calibration_aspect_ratio: float,
) -> tuple[float, float, float]:
    """Reproduce Lensfun's focal-preserving PTLens coefficient scaling."""
    hugin_scale_mm = (
        FULL_FRAME_DIAGONAL_MM
        / calibration_crop_factor
        / math.hypot(calibration_aspect_ratio, 1.0)
        / 2.0
    )
    hugin_scaling = focal_length_mm / hugin_scale_mm
    d = 1.0 - a - b - c
    if d == 0:
        raise ValueError("PTLens coefficients produce a singular d term")
    return (
        a * hugin_scaling**3 / d**4,
        b * hugin_scaling**2 / d**3,
        c * hugin_scaling / d**2,
    )


def rescale_poly3_tca(
    vr: float,
    vb: float,
    *,
    focal_length_mm: float,
    calibration_crop_factor: float,
    calibration_aspect_ratio: float,
    cr: float = 0.0,
    cb: float = 0.0,
    br: float = 0.0,
    bb: float = 0.0,
) -> tuple[float, float, float, float, float, float]:
    hugin_scale_mm = (
        FULL_FRAME_DIAGONAL_MM
        / calibration_crop_factor
        / math.hypot(calibration_aspect_ratio, 1.0)
        / 2.0
    )
    hugin_scaling = focal_length_mm / hugin_scale_mm
    return (
        vr,
        vb,
        cr * hugin_scaling,
        cb * hugin_scaling,
        br * hugin_scaling**2,
        bb * hugin_scaling**2,
    )


def rescale_pa_vignetting(
    k1: float,
    k2: float,
    k3: float,
    *,
    focal_length_mm: float,
    calibration_crop_factor: float,
) -> tuple[float, float, float]:
    hugin_scale_mm = (
        FULL_FRAME_DIAGONAL_MM / calibration_crop_factor / 2.0
    )
    hugin_scaling = focal_length_mm / hugin_scale_mm
    return (
        k1 * hugin_scaling**2,
        k2 * hugin_scaling**4,
        k3 * hugin_scaling**6,
    )


def inverse_ptlens_radius(
    distorted_radius: float,
    coefficients: tuple[float, float, float],
) -> float:
    """Reproduce ModifyCoord_UnDist_PTLens and its iteration boundary."""
    if distorted_radius == 0.0:
        return 0.0
    a, b, c = coefficients
    undistorted = distorted_radius
    for step in range(7):
        value = (
            undistorted
            * (
                a * undistorted**3
                + b * undistorted**2
                + c * undistorted
                + 1.0
            )
            - distorted_radius
        )
        if -NEWTON_EPSILON <= value < NEWTON_EPSILON:
            break
        if step > 5:
            return distorted_radius
        derivative = (
            4.0 * a * undistorted**3
            + 3.0 * b * undistorted**2
            + 2.0 * c * undistorted
            + 1.0
        )
        undistorted -= value / derivative
    return undistorted if undistorted >= 0.0 else distorted_radius


def inverse_poly3_radius(
    distorted_radius: float,
    *,
    v: float,
    c: float,
    b: float,
) -> float:
    """Reproduce one channel of ModifyCoord_UnTCA_Poly3."""
    if distorted_radius == 0.0:
        return 0.0
    undistorted = distorted_radius
    for step in range(7):
        radius_squared = undistorted * undistorted
        value = (
            b * radius_squared * undistorted
            + c * radius_squared
            + v * undistorted
            - distorted_radius
        )
        if -NEWTON_EPSILON <= value < NEWTON_EPSILON:
            break
        if step > 5:
            return distorted_radius
        undistorted -= value / (
            3.0 * b * radius_squared + 2.0 * c * undistorted + v
        )
    return undistorted if undistorted > 0.0 else distorted_radius


def generate_reverse_maps(
    profile: ReverseLensProfile,
    *,
    width: int,
    height: int,
) -> dict[str, array]:
    """Generate Lensfun-reverse R/G/B UV maps and PA transmission.

    UV coordinates follow Blender Map UV's expected red/green representation;
    blue and alpha remain one. Lensfun transforms pixel-centre coordinates in
    the 0..width-1 / 0..height-1 domain. Blender Map UV encodes those centres
    as (x + 0.5) / width and (y + 0.5) / height; an identity-map experiment in
    Blender 5.2 reproduced the source exactly with that convention.
    """
    norm_scale, center_x, center_y = modifier_normalization(
        width,
        height,
        focal_length_mm=profile.focal_length_mm,
        crop_factor=profile.crop_factor,
    )
    ptlens = rescale_ptlens(
        profile.ptlens_a,
        profile.ptlens_b,
        profile.ptlens_c,
        focal_length_mm=profile.focal_length_mm,
        calibration_crop_factor=profile.crop_factor,
        calibration_aspect_ratio=profile.calibration_aspect_ratio,
    )
    vr, vb, cr, cb, br, bb = rescale_poly3_tca(
        profile.tca_vr,
        profile.tca_vb,
        focal_length_mm=profile.focal_length_mm,
        calibration_crop_factor=profile.crop_factor,
        calibration_aspect_ratio=profile.calibration_aspect_ratio,
    )
    vignette = rescale_pa_vignetting(
        profile.vignette_k1,
        profile.vignette_k2,
        profile.vignette_k3,
        focal_length_mm=profile.focal_length_mm,
        calibration_crop_factor=profile.crop_factor,
    )

    maps = {
        "red": array("f"),
        "green": array("f"),
        "blue": array("f"),
        "vignette": array("f"),
    }
    inverse_scale = 1.0 / norm_scale

    for row in range(height):
        y = row * norm_scale - center_y
        for column in range(width):
            x = column * norm_scale - center_x
            distorted_radius = math.hypot(x, y)
            base_radius = inverse_ptlens_radius(distorted_radius, ptlens)
            base_scale = (
                base_radius / distorted_radius if distorted_radius else 1.0
            )
            base_x = x * base_scale
            base_y = y * base_scale

            channel_data = (
                ("red", vr, cr, br),
                ("green", 1.0, 0.0, 0.0),
                ("blue", vb, cb, bb),
            )
            for name, v, c, b in channel_data:
                channel_distorted_radius = math.hypot(base_x, base_y)
                channel_radius = inverse_poly3_radius(
                    channel_distorted_radius,
                    v=v,
                    c=c,
                    b=b,
                )
                channel_scale = (
                    channel_radius / channel_distorted_radius
                    if channel_distorted_radius
                    else 1.0
                )
                pixel_x = (base_x * channel_scale + center_x) * inverse_scale
                pixel_y = (base_y * channel_scale + center_y) * inverse_scale
                maps[name].extend(
                    (
                        (pixel_x + 0.5) / width,
                        (pixel_y + 0.5) / height,
                        1.0,
                        1.0,
                    )
                )

            radius_squared = x * x + y * y
            k1, k2, k3 = vignette
            transmission = (
                1.0
                + k1 * radius_squared
                + k2 * radius_squared**2
                + k3 * radius_squared**3
            )
            maps["vignette"].extend(
                (transmission, transmission, transmission, 1.0)
            )
    return maps
