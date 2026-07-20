"""Shared Blender-hosted asset inventory logic for UI and headless use."""

from __future__ import annotations

from pathlib import Path

import bpy


def vector(values: object) -> list[float]:
    return [round(float(value), 9) for value in values]


def object_record(object_: bpy.types.Object) -> dict[str, object]:
    entry: dict[str, object] = {
        "name": object_.name,
        "type": object_.type,
        "parent": object_.parent.name if object_.parent else None,
        "collections": sorted(
            collection.name for collection in object_.users_collection
        ),
        "location": vector(object_.location),
        "rotation_euler": vector(object_.rotation_euler),
        "scale": vector(object_.scale),
        "matrix_determinant": round(float(object_.matrix_world.determinant()), 9),
        "modifiers": [
            {"name": modifier.name, "type": modifier.type}
            for modifier in object_.modifiers
        ],
        "custom_properties": sorted(set(object_.keys()) - {"_RNA_UI"}),
    }
    if object_.type != "MESH":
        return entry

    mesh = object_.data
    entry["mesh"] = {
        "name": mesh.name,
        "vertices": len(mesh.vertices),
        "edges": len(mesh.edges),
        "polygons": len(mesh.polygons),
        "loops": len(mesh.loops),
        "uv_layers": [layer.name for layer in mesh.uv_layers],
        "color_attributes": [
            {
                "name": attribute.name,
                "data_type": attribute.data_type,
                "domain": attribute.domain,
            }
            for attribute in mesh.color_attributes
        ],
        "attributes": [
            {
                "name": attribute.name,
                "data_type": attribute.data_type,
                "domain": attribute.domain,
                "count": len(attribute.data),
            }
            for attribute in mesh.attributes
            if not attribute.is_internal
        ],
        "materials": [
            material.name if material else None for material in mesh.materials
        ],
        "shape_keys": (
            [block.name for block in mesh.shape_keys.key_blocks]
            if mesh.shape_keys
            else []
        ),
    }
    return entry


def build_inventory(*, active_only: bool = False) -> dict[str, object]:
    if active_only:
        objects = [bpy.context.active_object] if bpy.context.active_object else []
    else:
        objects = sorted(bpy.data.objects, key=lambda item: item.name)
    source = Path(bpy.data.filepath).resolve() if bpy.data.filepath else None
    return {
        "inventory_version": "1.0.0",
        "blender_version": bpy.app.version_string,
        "source_basename": source.name if source else None,
        "scene": {
            "name": bpy.context.scene.name,
            "unit_system": bpy.context.scene.unit_settings.system,
            "unit_scale_length": bpy.context.scene.unit_settings.scale_length,
            "object_count": len(objects),
        },
        "objects": [object_record(object_) for object_ in objects],
        "materials": sorted(material.name for material in bpy.data.materials),
        "images": sorted(
            (
                {
                    "name": image.name,
                    "source": image.source,
                    "basename": Path(image.filepath).name if image.filepath else None,
                }
                for image in bpy.data.images
            ),
            key=lambda item: item["name"],
        ),
        "scope": "non-mutating structural inventory; no visual-quality claim",
    }
