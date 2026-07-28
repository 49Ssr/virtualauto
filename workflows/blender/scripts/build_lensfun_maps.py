"""Build source-pinned Lensfun reverse maps as packed Blender images.

The script only creates or deliberately overwrites named generated images. It
does not wire compositor nodes, save the blend file, or qualify visual output.
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from virtualauto import lensfun_models  # noqa: E402

# Blender keeps imported Python modules alive across Text Editor/MCP runs.
# Reload deliberately so an iterative generator run cannot silently use stale
# equations from an earlier repository revision.
lensfun_models = importlib.reload(lensfun_models)
ReverseLensProfile = lensfun_models.ReverseLensProfile
generate_reverse_maps = lensfun_models.generate_reverse_maps
float32_le_sha256 = lensfun_models.float32_le_sha256


def parse_args() -> argparse.Namespace:
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", required=True)
    parser.add_argument("--overwrite-existing", action="store_true")
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args()
    contract_path = Path(args.contract)
    if not contract_path.is_absolute():
        contract_path = ROOT / contract_path
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    lensfun = contract["lensfun"]
    if lensfun["source_commit"] != "698a39eea69be00f4f25b6da6c1ad34b1f162b50":
        raise SystemExit("This builder is qualified only for the audited commit")
    if not lensfun["reverse"]:
        raise SystemExit("This builder implements Lensfun reverse simulation only")

    distortion = lensfun["distortion"]
    tca = lensfun["tca"]
    vignette = lensfun["vignetting"]
    profile = ReverseLensProfile(
        focal_length_mm=float(contract["camera"]["focal_length_mm"]),
        crop_factor=float(lensfun["crop_factor"]),
        calibration_aspect_ratio=float(lensfun["calibration_aspect_ratio"]),
        ptlens_a=float(distortion["a"]),
        ptlens_b=float(distortion["b"]),
        ptlens_c=float(distortion["c"]),
        tca_vr=float(tca["vr"]),
        tca_vb=float(tca["vb"]),
        vignette_k1=float(vignette["k1"]),
        vignette_k2=float(vignette["k2"]),
        vignette_k3=float(vignette["k3"]),
    )
    width, height = (int(value) for value in lensfun["map_resolution"])
    maps = generate_reverse_maps(profile, width=width, height=height)

    records = {}
    for channel, values in maps.items():
        image_name = lensfun["image_names"][channel]
        image = bpy.data.images.get(image_name)
        if image is not None:
            if not args.overwrite_existing:
                raise SystemExit(
                    f"Generated image exists; pass --overwrite-existing: {image_name}"
                )
            if tuple(image.size) != (width, height):
                image.scale(width, height)
        else:
            image = bpy.data.images.new(
                image_name,
                width=width,
                height=height,
                alpha=True,
                float_buffer=True,
            )
        image.colorspace_settings.name = "Non-Color"
        image.alpha_mode = "STRAIGHT"
        image.pixels.foreach_set(values)
        image.update()
        image.pack()
        image["va_generator"] = "virtualauto.lensfun_models.generate_reverse_maps"
        image["va_lensfun_commit"] = lensfun["source_commit"]
        image["va_contract_id"] = contract["id"]
        pixel_hash = float32_le_sha256(values)
        image["va_float32_sha256_native_little_endian"] = pixel_hash
        records[channel] = {
            "image": image_name,
            "size": [width, height],
            "float32_sha256_native_little_endian": pixel_hash,
            "minimum": min(values),
            "maximum": max(values),
        }

    report = {
        "status": "generated_not_wired_or_visually_qualified",
        "contract_id": contract["id"],
        "source_commit": lensfun["source_commit"],
        "records": records,
    }
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
