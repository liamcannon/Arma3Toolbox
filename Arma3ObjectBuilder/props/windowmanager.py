import bpy

from . import object as objectprops
from ..utilities import data


def mesh_object_poll(self,object):
    return object.type == 'MESH'


class A3OB_PG_common_proxy(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty (
        name = "Name",
        description = "Descriptive name of the common proxy",
        default = ""
    )
    path: bpy.props.StringProperty (
        name = "Path",
        description = "File path of the proxy model",
        default = ""
    )


class A3OB_PG_mass_editor(bpy.types.PropertyGroup):
    enabled: bpy.props.BoolProperty (
        name = "Enable Vertex Mass Tools",
        description = "Dynamic calculation of the vertex masses can be performace heavy on large meshes",
        default = False
    )
    source: bpy.props.EnumProperty (
        name = "Source",
        description = "Type of source for mass calculations",
        items = (
            ('MASS', "Mass", "The masses are calculated from discrete mass values"),
            ('DENSITY', "Density", "The masses are calculated from volumetric density")
        ),
        default = 'MASS'
    )
    density: bpy.props.FloatProperty (
        name = "Density",
        description = "Volumetric density of mesh (kg/m3)",
        default = 1.0,
        min = 0.1,
        max = 1000000,
        soft_max = 1000,
        step = 10,
        precision = 3
    )
    mass: bpy.props.FloatProperty (
        name = "Mass",
        description = "Mass to set equally or distribute",
        default = 0.0,
        unit = 'MASS',
        min = 0,
        max = 1000000,
        soft_max = 100000,
        step = 10,
        precision = 3
    )


class A3OB_PG_hitpoint_generator(bpy.types.PropertyGroup):
    source: bpy.props.PointerProperty (
        type=bpy.types.Object,
        name = "Source",
        description = "Mesh object to use as source for point cloud generation",
        poll = mesh_object_poll
    )
    target: bpy.props.PointerProperty (
        type=bpy.types.Object,
        name = "Target",
        description = "Mesh object to write generate point cloud to\n(leave empty to create new object)",
        poll = mesh_object_poll
    )
    spacing: bpy.props.FloatVectorProperty (
        name = "Spacing",
        description = "Space between generated points",
        subtype = 'XYZ',
        unit = 'LENGTH',
        min = 0.01,
        default = (0.2, 0.2, 0.2),
        size = 3
    )
    bevel_offset: bpy.props.FloatProperty (
        name = "Bevel Offset",
        description = "Offset value of bevel to apply to every edge of the source object",
        min = 0,
        default = 0.1
    )
    bevel_segments: bpy.props.IntProperty (
        name = "Bevel Segments",
        description = "Number of segments of bevel to apply to every edge of the source object",
        min = 1,
        max = 10,
        default = 4
    )
    triangulate: bpy.props.EnumProperty (
        name = "Triangulation Order",
        description = "Triangulate before, or after bevelling",
        items = (
            ('BEFORE', "Before", "Apply triangulation before the bevel"),
            ('AFTER', "After", "Apply triangulation after the bevel")
        ),
        default = 'AFTER'
    )
    selection: bpy.props.StringProperty (
        name = "Selection",
        description = "Vertex group to add the generated points to",
        default = ""
    )


class A3OB_PG_validation(bpy.types.PropertyGroup):
    detect: bpy.props.BoolProperty (
        name = "Detect Type",
        description = "Detect LOD type when set",
        default = True
    )
    lod: bpy.props.EnumProperty (
        name = "Type",
        description = "Type of LOD",
        items = data.enum_lod_types_validation,
        default = '4'
    )
    warning_errors: bpy.props.BoolProperty (
        name = "Warnings Are Errors",
        description = "Treat warnings as errors during validation",
        default = True
    )
    
    
class A3OB_PG_keyframes(bpy.types.PropertyGroup):
    mode: bpy.props.EnumProperty (
        name = "Mode",
        description = "List mode",
        items = (
            ('TIMELINE', "Timeline", "Add keyframes from animation timeline"),
            ('RANGE', "Range", "Add keyframes in range")
        ),
        default = 'RANGE'
    )
    clear: bpy.props.BoolProperty (
        name = "Clear Existing",
        description = "Clear existing frames before adding new",
        default = False
    )
    range_start: bpy.props.IntProperty (
        name = "Start",
        description = "Start of frame range",
        default = 0,
        min = 0
    )
    range_end: bpy.props.IntProperty (
        name = "End",
        description = "End of frame range",
        default = 100,
        min = 0
    )
    range_step: bpy.props.IntProperty (
        name = "Step",
        description = "Step in frame range",
        default = 5,
        min = 1
    )
    
    
class A3OB_PG_conversion(bpy.types.PropertyGroup):
    use_selection: bpy.props.BoolProperty (
        name = "Selected Only",
        description = "Convert only selected objects",
        default = False
    )
    types: bpy.props.EnumProperty (
        name = "Object Types",
        description = "Only convert object of the selected types",
        items = (
            ('MESH', "LOD", ""),
            ('DTM', "DTM", ""),
            ('ARMATURE', "Armature", "")
        ),
        options = {'ENUM_FLAG'},
        default = {'MESH', 'DTM', 'ARMATURE'}
    )
    dynamic_naming: bpy.props.BoolProperty (
        name = "Dynamic Object Naming",
        description = "Enable Dynamic Object Naming for LOD and proxy objects",
        default = True
    )
    cleanup: bpy.props.BoolProperty (
        name = "Cleanup",
        description = "Cleanup the ArmaToolbox-style settings and properties",
        default = True
    )


class A3OB_PG_renamable(bpy.types.PropertyGroup):
    path: bpy.props.StringProperty (
        name = "From",
        description = "File path",
        default = ""
    )


class A3OB_PG_renaming(bpy.types.PropertyGroup):
    source_filter: bpy.props.EnumProperty (
        name = "Filter",
        description = "",
        items = (
            ('TEX', "Texture", "Show paths to textures"),
            ('RVMAT', "RVMAT", "Show paths to RVMATs"),
            ('PROXY', "Proxy", "Show paths to proxies")
        ),
        options = {'ENUM_FLAG'},
        default = {'TEX','RVMAT', 'PROXY'}
    )
    path_list: bpy.props.CollectionProperty (
        type = A3OB_PG_renamable
    )
    path_list_index: bpy.props.IntProperty (
        name = "Selection Index",
        default = -1
    )
    new_path: bpy.props.StringProperty (
        name = "To",
        description = "New file path",
        default = "",
        subtype = 'FILE_PATH'
    )
    root_old: bpy.props.StringProperty (
        name = "From",
        description = "Path root to change",
        default = "",
        subtype = 'FILE_PATH'
    )
    root_new: bpy.props.StringProperty (
        name = "To",
        description = "Path to change root to",
        default = "",
        subtype = 'FILE_PATH'
    )
    vgroup_old: bpy.props.StringProperty (
        name = "From",
        description = "Vertex group to rename",
        default = ""
    )
    vgroup_new: bpy.props.StringProperty (
        name = "To",
        description = "New vertex group name"
    )
    vgroup_match_whole: bpy.props.BoolProperty (
        name = "Whole Name",
        description = "Only replace if the whole name matches",
        default = True
    )


classes = (
    A3OB_PG_common_proxy,
    A3OB_PG_mass_editor,
    A3OB_PG_hitpoint_generator,
    A3OB_PG_validation,
    A3OB_PG_keyframes,
    A3OB_PG_conversion,
    A3OB_PG_renamable,
    A3OB_PG_renaming
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.WindowManager.a3ob_proxy_common = bpy.props.CollectionProperty(type=A3OB_PG_common_proxy)
    bpy.types.WindowManager.a3ob_proxy_common_index = bpy.props.IntProperty(name="Selection Index", default = -1)
    bpy.types.WindowManager.a3ob_namedprops_common = bpy.props.CollectionProperty(type=objectprops.A3OB_PG_properties_named_property)
    bpy.types.WindowManager.a3ob_namedprops_common_index = bpy.props.IntProperty(name="Selection Index", default = -1)
    bpy.types.WindowManager.a3ob_mass_editor = bpy.props.PointerProperty(type=A3OB_PG_mass_editor)
    bpy.types.WindowManager.a3ob_hitpoint_generator = bpy.props.PointerProperty(type=A3OB_PG_hitpoint_generator)
    bpy.types.WindowManager.a3ob_validation = bpy.props.PointerProperty(type=A3OB_PG_validation)
    bpy.types.WindowManager.a3ob_keyframes = bpy.props.PointerProperty(type=A3OB_PG_keyframes)
    bpy.types.WindowManager.a3ob_conversion = bpy.props.PointerProperty(type=A3OB_PG_conversion)
    bpy.types.WindowManager.a3ob_renaming = bpy.props.PointerProperty(type=A3OB_PG_renaming)
    
    print("\t" + "Properties: window manager")
    
    
def unregister():
    del bpy.types.WindowManager.a3ob_renaming
    del bpy.types.WindowManager.a3ob_conversion
    del bpy.types.WindowManager.a3ob_validation
    del bpy.types.WindowManager.a3ob_keyframes
    del bpy.types.WindowManager.a3ob_hitpoint_generator
    del bpy.types.WindowManager.a3ob_mass_editor
    del bpy.types.WindowManager.a3ob_namedprops_common_index
    del bpy.types.WindowManager.a3ob_namedprops_common
    del bpy.types.WindowManager.a3ob_proxy_common_index
    del bpy.types.WindowManager.a3ob_proxy_common
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    print("\t" + "Properties: window manager")