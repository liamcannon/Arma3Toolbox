import os
import struct

import bpy
import mathutils

from ..utilities import generic as utils
from ..utilities import proxy as proxyutils
from ..io import import_p3d


class A3OB_OT_proxy_realign_ocs(bpy.types.Operator):
    """Realign the proxy object coordinate system with proxy directions"""
    
    bl_idname = "a3ob.proxy_realign_ocs"
    bl_label = "Realign Coordinate System"
    bl_options = {'UNDO'}
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.mode == 'OBJECT' and len(context.selected_objects) == 1 and obj.type == 'MESH' and obj.a3ob_properties_object_proxy.is_a3_proxy
    
    def execute(self, context):
        obj = context.active_object
        import_p3d.transform_proxy(obj)
            
        return {'FINISHED'}


class A3OB_OT_proxy_align(bpy.types.Operator):
    """Align the proxy object to another selected object"""
    
    bl_idname = "a3ob.proxy_align"
    bl_label = "Align To Object"
    bl_options = {'UNDO'}
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        selected = context.selected_objects
        
        if not obj or len(selected) != 2:
            return False
            
        selected.remove(obj)
        return obj.mode == 'OBJECT' and selected[0] and selected[0].mode == 'OBJECT' and selected[0].a3ob_properties_object_proxy.is_a3_proxy
    
    def execute(self, context):
        obj = context.active_object
        selected = context.selected_objects.copy()
        selected.remove(obj)
        proxy = selected[0]
        
        proxy.matrix_world = obj.matrix_world
        proxy.scale = mathutils.Vector((1, 1, 1))
                    
        return {'FINISHED'}


class A3OB_OT_proxy_align_object(bpy.types.Operator):
    """Align an object to a selected proxy object"""
    
    bl_idname = "a3ob.proxy_align_object"
    bl_label = "Align To Proxy"
    bl_options = {'UNDO'}
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        selected = context.selected_objects
        
        if not obj or len(selected) != 2:
            return False
            
        selected.remove(obj)
        return obj.mode == 'OBJECT' and obj.a3ob_properties_object_proxy.is_a3_proxy and selected[0] and selected[0].mode == 'OBJECT'
    
    def execute(self, context):
        proxy = context.active_object
        selected = context.selected_objects.copy()
        selected.remove(proxy)
        obj = selected[0]
        
        obj.matrix_world = proxy.matrix_world
        obj.scale = mathutils.Vector((1, 1, 1))
                    
        return {'FINISHED'}


class A3OB_OT_proxy_extract(bpy.types.Operator):
    """Import 1st LOD of proxy model in place of proxy object"""
    
    bl_idname = "a3ob.proxy_extract"
    bl_label = "Extract Proxy"
    bl_options = {'UNDO'}
    
    enclose: bpy.props.BoolProperty (
        default = False
    )
    groupby: bpy.props.EnumProperty (
        default = 'NONE',
        items = (
            ('NONE', "", ""),
        )
    )
    additional_data_allowed: bpy.props.BoolProperty (
        default = True
    )
    additional_data: bpy.props.EnumProperty (
        options = {'ENUM_FLAG'},
        items = (
            ('NORMALS', "", ""),
            ('PROPS', "Named Properties", ""),
            ('MASS', "", ""),
            ('SELECTIONS', "", ""),
            ('UV', "", ""),
            ('MATERIALS', "", "")
        ),
        default = {'NORMALS', 'PROPS', 'MASS', 'SELECTIONS', 'UV', 'MATERIALS'}
    )
    validate_meshes: bpy.props.BoolProperty (
        default = True
    )
    proxy_action: bpy.props.EnumProperty (
        items = (
            ('SEPARATE', "", ""),
        ),
        default = 'SEPARATE'
    )
    dynamic_naming: bpy.props.BoolProperty (
        default = False
    )
    first_lod_only: bpy.props.BoolProperty (
        default = True
    )
    filepath: bpy.props.StringProperty (
        default = ""
    )
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        path = utils.abspath(obj.a3ob_properties_object_proxy.proxy_path)
        return obj and obj.type == 'MESH' and len(context.selected_objects) == 1 and obj.a3ob_properties_object_proxy.is_a3_proxy and os.path.exists(path) and os.path.splitext(path)[1].lower() == '.p3d'
    
    def execute(self, context):
        proxy_object = context.active_object
        self.filepath = utils.abspath(proxy_object.a3ob_properties_object_proxy.proxy_path)
        with open(self.filepath, "rb") as file:
            try:
                lod_data = import_p3d.read_file(self, context, file, self.first_lod_only)
                self.report({'INFO'}, "Succesfully extracted proxy (check the logs in the system console)")
            except struct.error as ex:
                self.report({'ERROR'}, "Unexpected EndOfFile (check the system console)")
                traceback.print_exc()
            except Exception as ex:
                self.report({'ERROR'}, "%s (check the system console)" % str(ex))
                traceback.print_exc()
        
        imported_object = lod_data[0][0]
        imported_object.matrix_world = proxy_object.matrix_world
        imported_object.name = os.path.basename(self.filepath)
        imported_object.data.name = os.path.basename(self.filepath)
        bpy.data.meshes.remove(proxy_object.data)
            
        return {'FINISHED'}


class A3OB_PT_proxies(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Object Builder"
    bl_label = "Proxies"
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        return True
        
    def draw_header(self, context):
        if not utils.get_addon_preferences(context).show_info_links:
            return
            
        layout = self.layout
        row = layout.row(align=True)
        row.operator("wm.url_open", text="", icon='HELP').url = "https://mrcmodding.gitbook.io/arma-3-object-builder/tools/proxies"
        
    def draw(self, context):
        layout = self.layout
        
        col_align = layout.column(align=True)
        col_align.operator("a3ob.proxy_align", icon='CUBE')
        col_align.operator("a3ob.proxy_align_object", icon='EMPTY_DATA')
        layout.operator("a3ob.proxy_realign_ocs", icon='ORIENTATION_GLOBAL')
        layout.operator("a3ob.proxy_extract", icon='IMPORT')


classes = (
    A3OB_OT_proxy_align,
    A3OB_OT_proxy_align_object,
    A3OB_OT_proxy_realign_ocs,
    A3OB_OT_proxy_extract,
    A3OB_PT_proxies
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    print("\t" + "UI: Proxies")


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    print("\t" + "UI: Proxies")