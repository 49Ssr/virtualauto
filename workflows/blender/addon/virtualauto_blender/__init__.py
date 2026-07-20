"""VirtualAuto development add-on for non-destructive asset archaeology."""

from __future__ import annotations

import json
from pathlib import Path

import bpy
from bpy.props import BoolProperty, StringProperty
from bpy_extras.io_utils import ExportHelper

from .inventory import build_inventory

bl_info = {
    "name": "VirtualAuto Asset Audit",
    "author": "VirtualAuto contributors",
    "version": (0, 1, 0),
    "blender": (5, 0, 1),
    "location": "3D View > Sidebar > VirtualAuto",
    "description": "Export a non-destructive structural inventory of automotive assets",
    "category": "3D View",
}


class VA_OT_export_inventory(bpy.types.Operator, ExportHelper):
    bl_idname = "virtualauto.export_inventory"
    bl_label = "Export Asset Inventory"
    bl_description = "Write structure and attribute metadata without editing the asset"

    filename_ext = ".json"
    filter_glob: StringProperty(default="*.json", options={"HIDDEN"})
    active_only: BoolProperty(
        name="Active Object Only",
        description="Inspect only the active object instead of the complete scene",
        default=False,
    )

    def execute(self, _context: bpy.types.Context) -> set[str]:
        destination = Path(self.filepath).expanduser().resolve()
        if destination.exists():
            self.report({"ERROR"}, "Refusing to overwrite an existing inventory")
            return {"CANCELLED"}
        report = build_inventory(active_only=self.active_only)
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_suffix(destination.suffix + ".tmp")
        temporary.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        temporary.replace(destination)
        self.report({"INFO"}, f"Inventory written: {destination.name}")
        return {"FINISHED"}


class VA_PT_asset_audit(bpy.types.Panel):
    bl_label = "Asset Audit"
    bl_idname = "VA_PT_asset_audit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "VirtualAuto"

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        layout.label(text="Blender baseline: 5.0.1")
        object_ = context.active_object
        if object_ is None:
            layout.label(text="No active object", icon="INFO")
        else:
            box = layout.box()
            box.label(text=object_.name, icon="OBJECT_DATA")
            box.label(text=f"Type: {object_.type}")
            if object_.type == "MESH":
                mesh = object_.data
                box.label(text=f"Polygons: {len(mesh.polygons):,}")
                box.label(text=f"UV layers: {len(mesh.uv_layers)}")
                box.label(text=f"Material slots: {len(mesh.materials)}")
            if any(abs(value - 1.0) > 1.0e-6 for value in object_.scale):
                box.label(text="Unapplied object scale", icon="ERROR")
            if object_.matrix_world.determinant() < 0.0:
                box.label(text="Negative transform determinant", icon="ERROR")

        operator = layout.operator(
            VA_OT_export_inventory.bl_idname,
            text="Export Scene Inventory",
            icon="EXPORT",
        )
        operator.active_only = False
        if object_ is not None:
            operator = layout.operator(
                VA_OT_export_inventory.bl_idname,
                text="Export Active Object",
            )
            operator.active_only = True


CLASSES = (VA_OT_export_inventory, VA_PT_asset_audit)


def register() -> None:
    for class_ in CLASSES:
        bpy.utils.register_class(class_)


def unregister() -> None:
    for class_ in reversed(CLASSES):
        bpy.utils.unregister_class(class_)
