bl_info = {
    "name": "Viewport Preset Switcher",
    "author": "Jeremie Ferreira",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > UI > View",
    "description": "Switch between different viewport camera clipping presets in the 3D View.",
    "warning": "",
    "doc_url": "",
    "category": "3D View",
}

import bpy

class ViewportPresetProperties(bpy.types.PropertyGroup):
    close_clip_start: bpy.props.FloatProperty(
        name="Close Start",
        description="Start clipping distance for close camera",
        precision=3,
        default=0.01,
        min=0.001,
        max=100
    )
    close_clip_end: bpy.props.FloatProperty(
        name="Close End",
        description="End clipping distance for close camera",
        precision=3,
        default=100,
        min=1,
        max=1000
    )
    distant_clip_start: bpy.props.FloatProperty(
        name="Distant Start",
        description="Start clipping distance for distant camera",
        default=1,
        min=1,
        max=100
    )
    distant_clip_end: bpy.props.FloatProperty(
        name="Distant End",
        description="End clipping distance for distant camera",
        default=1000,
        min=100,
        max=5000
    )

class VIEW3D_PT_camera_presets(bpy.types.Panel):
    bl_label = "Camera Presets"
    bl_idname = "VIEW3D_PT_camera_presets"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'View'

    def draw(self, context):
        layout = self.layout

        props = context.scene.camera_preset_properties

        row = layout.row(align=True)
        row.label(text="Close")
        row.prop(props, "close_clip_start", text="Start")
        row.prop(props, "close_clip_end", text="End")
        
        row = layout.row(align=True)
        row.label(text="Distant")
        row.prop(props, "distant_clip_start", text="Start")
        row.prop(props, "distant_clip_end", text="End")
        
        layout.operator("view3d.set_viewport_camera", text="Close Camera").preset_type = 'CLOSE'
        layout.operator("view3d.set_viewport_camera", text="Distant Camera").preset_type = 'DISTANT'

class VIEW3D_OT_set_viewport_camera(bpy.types.Operator):
    bl_idname = "view3d.set_viewport_camera"
    bl_label = "Set Viewport Camera"

    preset_type: bpy.props.EnumProperty(
        items=[
            ('CLOSE', "Close", "Use close camera settings"),
            ('DISTANT', "Distant", "Use distant camera settings")
        ],
        name="Preset Type"
    )

    def execute(self, context):
        props = context.scene.camera_preset_properties

        # Get the current viewport's region 3D view settings
        viewport = context.space_data

        # Set the camera clip settings for close view
        if self.preset_type == 'CLOSE':
            viewport.clip_start = props.close_clip_start
            viewport.clip_end = props.close_clip_end
        else:
            viewport.clip_start = props.distant_clip_start
            viewport.clip_end = props.distant_clip_end

        return {'FINISHED'}


def register():
    bpy.utils.register_class(ViewportPresetProperties)
    bpy.types.Scene.camera_preset_properties = bpy.props.PointerProperty(type=ViewportPresetProperties)

    bpy.utils.register_class(VIEW3D_PT_camera_presets)
    bpy.utils.register_class(VIEW3D_OT_set_viewport_camera)

def unregister():
    bpy.utils.unregister_class(ViewportPresetProperties)
    del bpy.types.Scene.camera_preset_properties

    bpy.utils.unregister_class(VIEW3D_PT_camera_presets)
    bpy.utils.unregister_class(VIEW3D_OT_set_viewport_camera)

if __name__ == "__main__":
    register()