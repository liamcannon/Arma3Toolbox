import traceback
import os

import bpy
import bpy_extras

from ..io import import_mcfg, export_mcfg
from ..utilities import generic as utils


class A3OB_OP_import_mcfg(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    """Import Arma 3 skeleton definition"""

    bl_idname = "a3ob.import_mcfg"
    bl_label = "Import Skeletons"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}
    filename_ext = "model.cfg"
    
    filter_glob: bpy.props.StringProperty(
        default = "*.cfg",
        options = {'HIDDEN'}
    )
    force_lowercase: bpy.props.BoolProperty(
        name = "Force Lowercase",
        description = "Import all bone names as lowercase",
        default = True
    )

    @classmethod
    def poll(cls, context):
        exepath = os.path.join(utils.abspath(utils.get_addon_preferences().a3_tools), "cfgconvert/cfgconvert.exe")
        return os.path.isfile(exepath)

    def draw(self, context):
        pass

    def execute(self, context):
        scene_props = context.scene.a3ob_rigging
        
        count_skeletons = 0
        try:
            data = import_mcfg.read_mcfg(utils.abspath(self.filepath))

            if data:
                skeletons = import_mcfg.get_skeletons(data)
                count_skeletons = len(skeletons)
                for skelly in skeletons:
                    new_skelly = scene_props.skeletons.add()
                    new_skelly.name = skelly.name.lower() if self.force_lowercase else skelly.name
                    
                    cfgbones = import_mcfg.get_bones_compiled(data, skelly.name)
                    if self.force_lowercase:
                        cfgbones = [bone.to_lowercase() for bone in cfgbones]

                    for bone in cfgbones:
                        new_bone = new_skelly.bones.add()
                        new_bone.name = bone.name
                        new_bone.parent = bone.parent

        except Exception as ex:
            self.report({'ERROR'}, "%s (check the system console)" % str(ex))
            traceback.print_exc()
        
        if count_skeletons > 0:
            self.report({'INFO'}, "Successfully imported %d skeleton(s)" % count_skeletons)
        
        return {'FINISHED'}


class A3OB_PT_import_mcfg_main(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Main"
    bl_parent_id = "FILE_PT_operator"
    bl_options = {'HIDE_HEADER'}
    
    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        
        return operator.bl_idname == "A3OB_OT_import_mcfg"
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        sfile = context.space_data
        operator = sfile.active_operator

        layout.prop(operator, "force_lowercase")


class A3OB_OP_export_mcfg(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    """Export Arma 3 skeleton definition"""

    bl_idname = "a3ob.export_mcfg"
    bl_label = "Export Skeleton"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}
    filename_ext = "model.cfg"
    
    filter_glob: bpy.props.StringProperty(
        default = "*.cfg",
        options = {'HIDDEN'}
    )
    force_lowercase: bpy.props.BoolProperty(
        name = "Force Lowercase",
        description = "Export all bone names as lowercase",
        default = True
    )
    skeleton_index: bpy.props.IntProperty(
        name = "Skeleton To Export",
        default = 0
    )

    @classmethod
    def poll(cls, context):
        scene_props = context.scene.a3ob_rigging
        return len(scene_props.skeletons) > 0
    
    def draw(self, context):
        pass

    def execute(self, context):
        scene_props = context.scene.a3ob_rigging
        skeleton = scene_props.skeletons[self.skeleton_index]
        success = False

        temppath = self.filepath + ".temp"
        with open(temppath, "w") as file:
            try:
                success = export_mcfg.write_file(self, skeleton, file)
            except Exception as ex:
                self.report({'ERROR'}, "%s (check the system console)" % str(ex))
                traceback.print_exc()
        
        if success:
            if os.path.isfile(self.filepath):
                os.remove(self.filepath)
                
            os.rename(temppath, os.path.splitext(temppath)[0])
            self.report({'INFO'}, "Succesfully exported model.cfg")
        
        elif not success and not utils.get_addon_preferences().preserve_faulty_output:
            os.remove(temppath)

        return {'FINISHED'}


class A3OB_PT_export_mcfg_main(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Main"
    bl_parent_id = "FILE_PT_operator"
    bl_options = {'HIDE_HEADER'}
    
    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        
        return operator.bl_idname == "A3OB_OT_export_mcfg"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        sfile = context.space_data
        operator = sfile.active_operator
        scene_props = context.scene.a3ob_rigging

        layout.template_list("A3OB_UL_rigging_skeletons_protected", "A3OB_armature_skeletons", scene_props, "skeletons", operator, "skeleton_index", rows=3)
        layout.prop(operator, "force_lowercase")


classes = (
    A3OB_OP_import_mcfg,
    A3OB_PT_import_mcfg_main,
    A3OB_OP_export_mcfg,
    A3OB_PT_export_mcfg_main
)


def menu_func_import(self, context):
    self.layout.operator(A3OB_OP_import_mcfg.bl_idname, text="Arma 3 skeletons (model.cfg)")


def menu_func_export(self, context):
    self.layout.operator(A3OB_OP_export_mcfg.bl_idname, text="Arma 3 skeleton (model.cfg)")


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    
    print("\t" + "UI: MCFG Import / Export")


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    
    print("\t" + "UI: MCFG Import / Export")