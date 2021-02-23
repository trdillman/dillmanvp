# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This addon was generated with the Visual Scripting Addon.
# You can find the addon under https://blendermarket.com/products/serpens
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
sn_tree_name = "NodeTree"
addon_keymaps = []

bl_info = {
    "name": "Virtual Production Addon",
    "author": "Tyler Dillman",
    "description": "Create a camera for OSC interaction in VP",
    "location": "",
    "doc_url": "",
    "warning": "",
    "category": "General",
    "blender": (2, 90, 0),
    "version": (1, 0, 0)
}

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# IMPORTS
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import bpy
from bpy.app.handlers import persistent


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# UTILITY FUNCTIONS
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def sn_print(*text):
    text = ', '.join(map(str, text))
    print(text)  # actual print command
    try:  # try to find the area in which the addon is opened and add the print text
        for area in bpy.context.screen.areas:
            if area.type == "NODE_EDITOR":
                if area.spaces[0].node_tree:
                    if area.spaces[0].node_tree.bl_idname == "ScriptingNodesTree":
                        if sn_tree_name == area.spaces[0].node_tree.name:
                            bpy.context.scene.sn_properties.print_texts.add().text = str(text)

        for area in bpy.context.screen.areas:
            area.tag_redraw()
    except:
        pass


def get_enum_identifier(enumItems, name):
    for item in enumItems:
        if item.name == name:
            return item.identifier

    return ''


def report_sn_error(self, error):
    self.report({"ERROR"},
                message="There was an error when running this operation! It has been printed to the console.")
    print("START ERROR | Node Name: ", self.name,
          " | (If you are this addons developer you might want to report this to the Serpens team) ")
    print("")
    print(error)
    print("")
    print("END ERROR - - - - ")
    print("")


def get_python_filepath():
    path = os.path.dirname(bpy.data.filepath)
    try:
        __file__
        exported = True
    except:
        exported = False
    if exported:
        path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    return path


def cast_int(cast):
    int_string = ""
    if type(cast) == str:
        for char in cast:
            if char.isnumeric():
                int_string += char
    else:
        return cast[0]
    if int_string.isnumeric():
        int_string = int(int_string)
        return int_string
    return 0


def cast_float(cast):
    float_string = ""
    if type(cast) == str:
        for char in cast:
            if char.isnumeric() or char == ".":
                float_string += char
    else:
        return cast[0]
    if float_string != "" and float_string != ".":
        float_string = float(float_string)
        return float_string
    return 0


def cast_vector(cast):
    if type(cast) == bool:
        if cast:
            return (1.0, 1.0, 1.0)
        else:
            return (0.0, 0.0, 0.0)
    elif type(cast) == int:
        return (float(cast), float(cast), float(cast))
    elif type(cast) == float:
        return (cast, cast, cast)
    elif type(cast) == str:
        cast = cast_float(cast)
        return (cast, cast, cast)
    return (0, 0, 0)


def cast_four_vector(cast, four):
    if type(cast) == bool:
        if cast:
            return (1.0, 1.0, 1.0, four)
        else:
            return (0.0, 0.0, 0.0, four)
    elif type(cast) == int:
        return (float(cast), float(cast), float(cast), four)
    elif type(cast) == float:
        return (cast, cast, cast, four)
    elif type(cast) == str:
        cast = cast_float(cast)
        return (cast, cast, cast, four)
    return (0, 0, 0)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# CLASSES
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Create Array Collection for use in PROPERTIES
class ArrayCollection_UID_Wedsjpol(bpy.types.PropertyGroup):
    string: bpy.props.StringProperty()
    string_filepath: bpy.props.StringProperty(subtype='FILE_PATH')
    string_dirpath: bpy.props.StringProperty(subtype='DIR_PATH')
    bool: bpy.props.BoolProperty()

    int: bpy.props.IntProperty()
    int_pixel: bpy.props.IntProperty(subtype="PIXEL")
    int_unsigned: bpy.props.IntProperty(subtype="UNSIGNED")
    int_percentage: bpy.props.IntProperty(subtype="PERCENTAGE")
    int_factor: bpy.props.IntProperty(subtype="FACTOR")
    int_angle: bpy.props.IntProperty(subtype="ANGLE")
    int_time: bpy.props.IntProperty(subtype="TIME")
    int_distance: bpy.props.IntProperty(subtype="DISTANCE")

    float: bpy.props.FloatProperty()
    float_pixel: bpy.props.FloatProperty(subtype="PIXEL")
    float_unsigned: bpy.props.FloatProperty(subtype="UNSIGNED")
    float_percentage: bpy.props.FloatProperty(subtype="PERCENTAGE")
    float_factor: bpy.props.FloatProperty(subtype="FACTOR")
    float_angle: bpy.props.FloatProperty(subtype="ANGLE")
    float_time: bpy.props.FloatProperty(subtype="TIME")
    float_distance: bpy.props.FloatProperty(subtype="DISTANCE")

    vector: bpy.props.FloatVectorProperty()
    four_vector: bpy.props.FloatVectorProperty(size=4)
    color: bpy.props.FloatVectorProperty(subtype='COLOR')
    four_color: bpy.props.FloatVectorProperty(subtype='COLOR', size=4)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# CODE
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class SNA_OT_Operator_98368dbebf(bpy.types.Operator):
    bl_idname = "scripting_nodes.sna_ot_operator_98368dbebf"
    bl_label = "Create Camera"
    bl_description = "My Operators description"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        try:

            pass
            bpy.context.scene.render.resolution_y = 375
            bpy.context.scene.render.resolution_x = 812

            bpy.ops.object.camera_add('INVOKE_DEFAULT', enter_editmode=False, location=(0.0, 0.0, 0.0),
                                      rotation=(0.0, 0.0, 0.0), scale=(0.0, 0.0, 0.0), align='WORLD')

            exec(r"bpy.context.object.rotation_mode = 'QUATERNION'")
            exec(r"bpy.context.object.rotation_quaternion[1] = 0.707107")
            exec(r"bpy.context.object.rotation_quaternion[0] = 0.707107")
            bpy.context.active_object.name = r"VP Camera"

            bpy.context.active_object.delta_location = (
                0.0, 0.0, float(bpy.context.scene.sn_generated_addon_properties_UID_Wedsjpol.Camera_Height))
            #bpy.context.active_object.data.lens = int(
                #bpy.context.scene.sn_generated_addon_properties_UID_Wedsjpol.Focal_Length)
            exec(r"bpy.context.scene.camera = bpy.context.active_object")
            bpy.data.window_managers[
                r"WinMan"].vpt_osc_udp_in = bpy.context.scene.sn_generated_addon_properties_UID_Wedsjpol.Local_IP
            bpy.data.window_managers[r"WinMan"].vpt_osc_port_in = int(
                bpy.context.scene.sn_generated_addon_properties_UID_Wedsjpol.Port)
            bpy.data.window_managers[r"WinMan"].vpt_osc_in_enable = True

        except Exception as exc:
            report_sn_error(self, exc)
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout


class SNA_OT_BTN_5284383e90(bpy.types.Operator):
    bl_idname = 'scripting_nodes.sna_ot_btn_5284383e90'
    bl_label = r"Create Virtual Production Camera"
    bl_description = r"Create Virtual Production Camera"
    bl_options = {"REGISTER", "INTERNAL"}

    def execute(self, context):
        try:
            pass
            import bpy
            # Purge all VPT props
            for i in range(10):
                try:
                    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                    bpy.ops.vpt.removeprop(n=x[i])
                except:
                    pass
            # Purge all VP empties
            try:
                object_to_delete = bpy.data.objects["VP Orientation Correction"]
                bpy.data.objects.remove(object_to_delete, do_unlink=True)
            except:
                pass
            # Purge all VP Cameras
            try:
                object_to_delete = bpy.data.objects["VP Camera"]
                bpy.data.objects.remove(object_to_delete, do_unlink=True)
            except:
                pass
            # Purge all .###'s
            for i in range(10):
                try:
                    object_to_delete = bpy.data.objects["VP Orientation Correction.00{}".format(i)]
                    bpy.data.objects.remove(object_to_delete, do_unlink=True)
                    for i in range(10):
                        try:
                            object_to_delete = bpy.data.objects["VP Camera.00{}".format(i)]
                            bpy.data.objects.remove(object_to_delete, do_unlink=True)
                        except:
                            pass
                except:
                    pass

            # Purge orphaned data

            try:
                bpy.ops.outliner.orphans_purge()
            except:
                pass

            try:
                ob = bpy.context.active_object
                drivers_data = ob.animation_data.drivers
                for dr in drivers_data:
                    ob.driver_remove(dr.data_path, -1)
            except:
                pass

            exec(r"bpy.context.scene.unit_settings.system = 'METRIC'")
            bpy.ops.scripting_nodes.sna_ot_operator_98368dbebf('INVOKE_DEFAULT')

        except Exception as exc:
            report_sn_error(self, exc)
        return {"FINISHED"}


class SNA_PT_b6a4a58563(bpy.types.Panel):
    bl_label = "VP Camera Setup"
    bl_idname = "SNA_PT_b6a4a58563"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "VP Tools"

    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        layout.prop(bpy.context.scene.sn_generated_addon_properties_UID_Wedsjpol, 'Camera_Height', emboss=True,
                    text=r"Camera Height", slider=False)
        layout.prop(bpy.context.scene.sn_generated_addon_properties_UID_Wedsjpol, 'Focal_Length', emboss=True,
                    text=r"Focal Length", slider=False)
        layout.prop(bpy.context.scene.sn_generated_addon_properties_UID_Wedsjpol, 'Local_IP', emboss=True,
                    text=r"Local IP ")
        layout.prop(bpy.context.scene.sn_generated_addon_properties_UID_Wedsjpol, 'Port', emboss=True,
                    text=r"Set OSC Port", slider=False)
        layout.prop(bpy.context.scene.sn_generated_addon_properties_UID_Wedsjpol, 'Record', toggle=True, emboss=True,
                    text=r"Record")
        layout.operator("scripting_nodes.sna_ot_btn_5284383e90", text=r"Create Virtual Production Camera", emboss=True,
                        depress=False)
        layout.operator("scripting_nodes.sna_ot_btn_9a2fd396ce", text=r"Add OSC Routes to Camera", emboss=True,
                        depress=False)

        layout.label(text=r"Camera Offset:")
        layout.prop(bpy.context.scene.sn_generated_addon_properties_UID_Wedsjpol, 'X_Position', emboss=True, text=r"",
                    slider=False)
        layout.prop(bpy.context.scene.sn_generated_addon_properties_UID_Wedsjpol, 'Y_Position', emboss=True, text=r"",
                    slider=False)
        layout.prop(bpy.context.scene.sn_generated_addon_properties_UID_Wedsjpol, 'Z_Position', emboss=True, text=r"",
                    slider=False)


class SNA_OT_BTN_9a2fd396ce(bpy.types.Operator):
    bl_idname = 'scripting_nodes.sna_ot_btn_9a2fd396ce'
    bl_label = r"Add OSC Routes to Camera"
    bl_description = r""
    bl_options = {"REGISTER", "INTERNAL"}

    def execute(self, context):
        try:
            pass
            import bpy

            # Delete any previous VP Tools
            try:
                object_to_delete = bpy.data.objects["VP Orientation Correction"]
                bpy.data.objects.remove(object_to_delete, do_unlink=True)
            except:
                pass

            try:
                object_to_delete = bpy.data.objects["VP Camera Offset"]
                bpy.data.objects.remove(object_to_delete, do_unlink=True)
            except:
                pass

            for i in range(10):
                try:
                    object_to_delete = bpy.data.objects["VP Orientation Correction.00{}".format(i)]
                    bpy.data.objects.remove(object_to_delete, do_unlink=True)
                    for i in range(10):
                        try:
                            object_to_delete = bpy.data.objects["VP Camera.00{}".format(i)]
                            bpy.data.objects.remove(object_to_delete, do_unlink=True)
                        except:
                            pass
                except:
                    pass

            for i in range(10):
                try:
                    object_to_delete = bpy.data.objects["VP Camera Offset.00{}".format(i)]
                    bpy.data.objects.remove(object_to_delete, do_unlink=True)
                    for i in range(10):
                        try:
                            object_to_delete = bpy.data.objects["VP Camera.00{}".format(i)]
                            bpy.data.objects.remove(object_to_delete, do_unlink=True)
                        except:
                            pass
                except:
                    pass

            try:
                bpy.ops.outliner.orphans_purge()
            except:
                pass

                ##########

            # Add Empty For Orientation
            bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0))
            bpy.context.object.rotation_mode = 'QUATERNION'
            emt = bpy.context.object.name = "VP Orientation Correction"
            bpy.ops.object.hide_view_set(unselected=False)

            # Add Empty for Offset
            off = bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0))
            bpy.context.object.rotation_euler[0] = 1.5708
            off = bpy.context.object.name = "VP Camera Offset"
            bpy.data.objects["VP Camera"].parent = bpy.data.objects["VP Camera Offset"]
            bpy.ops.object.hide_view_set(unselected=False)

            # UUID Variable
            uid = bpy.context.scene.sn_generated_addon_properties_UID_Wedsjpol.UUID
            # Add new route for location
            bpy.ops.vpt.addprop()
            bpy.context.scene.VPT_Items[0].id.objects = bpy.data.objects["VP Orientation Correction"]
            bpy.context.scene.VPT_Items[0].data_path = "location"
            bpy.context.scene.VPT_Items[0].engine = 'OSC'
            bpy.context.scene.VPT_Items[0].mode = 'Receive'
            bpy.context.scene.VPT_Items[0].osc_address = "/osc/pos"
            bpy.context.scene.VPT_Items[0].is_multi = True
            bpy.context.scene.VPT_Items[0].use_array = True
            bpy.context.scene.VPT_Items[0].osc_select_n = 3
            bpy.context.scene.VPT_Items[0].VAR_use = 'dp'
            varBL = bpy.data.scenes['Scene'].sn_generated_addon_properties_UID_Wedsjpol.Record
            bpy.context.scene.VPT_Items[0].record = varBL

            # Add new route for rotation
            bpy.ops.vpt.addprop()
            bpy.context.scene.VPT_Items[1].id.objects = bpy.data.objects["VP Orientation Correction"]
            bpy.context.scene.VPT_Items[1].data_path = "rotation_quaternion"
            bpy.context.scene.VPT_Items[1].engine = 'OSC'
            bpy.context.scene.VPT_Items[1].mode = 'Receive'
            bpy.context.scene.VPT_Items[1].osc_address = "/osc/quat"
            bpy.context.scene.VPT_Items[1].is_multi = True
            bpy.context.scene.VPT_Items[1].use_array = True
            bpy.context.scene.VPT_Items[1].osc_select_n = 4
            bpy.context.scene.VPT_Items[1].VAR_use = 'dp'
            bpy.context.scene.VPT_Items[1].record = varBL

            # Add route for Focal Length
            bpy.ops.object.select_camera()
            bpy.context.object.data.name = "VP Camera"
            bpy.ops.vpt.addprop()
            bpy.context.scene.VPT_Items[2].id_type = 'cameras'
            bpy.context.scene.VPT_Items[2].id.cameras = bpy.data.cameras["VP Camera"]
            bpy.context.scene.VPT_Items[2].data_path = "lens"
            bpy.context.scene.VPT_Items[2].engine = 'OSC'
            bpy.context.scene.VPT_Items[2].mode = 'Receive'
            bpy.context.scene.VPT_Items[2].osc_address = "/osc/focal"
            bpy.context.scene.VPT_Items[2].is_multi = False
            bpy.context.scene.VPT_Items[2].VAR_use = 'dp'
            bpy.context.scene.VPT_Items[2].record = varBL


            # Delete all drivers
            try:
                ob = bpy.context.active_object
                drivers_data = ob.animation_data.drivers
                for dr in drivers_data:
                    ob.driver_remove(dr.data_path, -1)
            except:
                pass

            ## Add Drivers (For Offset)

            # X_Position Offset Driver
            valDrive = bpy.data.objects['VP Camera Offset'].driver_add('location', 0)
            valDrive.driver.type = 'AVERAGE'
            drvVar = valDrive.driver.variables.new()
            drvVar.name = ''
            drvVar.targets[0].id_type = 'SCENE'
            drvVar.targets[0].id = bpy.data.scenes['Scene']
            drvVar.targets[0].data_path = 'sn_generated_addon_properties_UID_Wedsjpol.X_Position'

            ##Y_Position Offset Driver
            valDrive = bpy.data.objects['VP Camera Offset'].driver_add('location', 1)
            valDrive.driver.type = 'AVERAGE'
            drvVar = valDrive.driver.variables.new()
            drvVar.name = ''
            drvVar.targets[0].id_type = 'SCENE'
            drvVar.targets[0].id = bpy.data.scenes['Scene']
            drvVar.targets[0].data_path = 'sn_generated_addon_properties_UID_Wedsjpol.Y_Position'

            ##Z_Position Offset Driver
            valDrive = bpy.data.objects['VP Camera Offset'].driver_add('location', 2)
            valDrive.driver.type = 'AVERAGE'
            drvVar = valDrive.driver.variables.new()
            drvVar.name = ''
            drvVar.targets[0].id_type = 'SCENE'
            drvVar.targets[0].id = bpy.data.scenes['Scene']
            drvVar.targets[0].data_path = 'sn_generated_addon_properties_UID_Wedsjpol.Z_Position'

            # Drivers Function (For Camera)

            def add_driver(
                    source, target, prop, dataPath,
                    index=-1, negative=False, func=''
            ):
                ''' Add driver to source prop (at index), driven by target dataPath '''

                if index != -1:
                    d = source.driver_add(prop, index).driver
                else:
                    d = source.driver_add(prop).driver

                v = d.variables.new()
                v.name = prop
                v.targets[0].id = target
                v.targets[0].data_path = dataPath

                d.expression = func + "(" + v.name + ")" if func else v.name
                d.expression = d.expression if not negative else "-1 * " + d.expression

            # Create Drivers
            camera = bpy.context.scene.objects['VP Camera']
            empty = bpy.context.scene.objects['VP Orientation Correction']
            offset = bpy.context.scene.objects['VP Camera Offset']

            try:
                add_driver(camera, empty, 'location', 'location.x', 0)
                add_driver(camera, empty, 'location', 'location.y', 2)
                add_driver(camera, empty, 'location', 'location.z', 1)

                bpy.data.objects["VP Camera"].animation_data.drivers[2].driver.expression = '-location'

                # Rotation

                add_driver(camera, empty, 'rotation_quaternion', 'rotation_quaternion.w', 1)
                add_driver(camera, empty, 'rotation_quaternion', 'rotation_quaternion.x', 2)
                add_driver(camera, empty, 'rotation_quaternion', 'rotation_quaternion.y', 3)
                add_driver(camera, empty, 'rotation_quaternion', 'rotation_quaternion.z', 0)
            except:
                pass
            # Offset



        except Exception as exc:
            report_sn_error(self, exc)
        return {"FINISHED"}


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# PROPERTIES
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Store the addons variables
class GeneratedAddonProperties_UID_Wedsjpol(bpy.types.PropertyGroup):
    set_default: bpy.props.BoolProperty(default=True)

    def update_Port(self, context):
        pass

    def update_Focal_Length(self, context):
        pass

    def update_Camera_Height(self, context):
        pass

    def update_UUID(self, context):
        pass

    def update_Local_IP(self, context):
        pass

    def update_X_Position(self, context):
        pass

    def update_Y_Position(self, context):
        pass

    def update_Z_Position(self, context):
        pass

    def update_Record(self, context):
        pass

    Port: bpy.props.IntProperty(name='Port', description='Set OSC Port', default=9001, subtype='NONE',
                                update=update_Port)
    Focal_Length: bpy.props.FloatProperty(name='Focal_Length', description='Set Camera Focal Length', default=35.0,
                                          subtype='NONE', update=update_Focal_Length, min=12.0)
    Camera_Height: bpy.props.FloatProperty(name='Camera_Height', description='', default=0.0, subtype='NONE',
                                           update=update_Camera_Height)
    UUID: bpy.props.StringProperty(name='UUID', description='here', default='blender', subtype='NONE',
                                   update=update_UUID)
    Local_IP: bpy.props.StringProperty(name='Local_IP', description='Set ip address', default='0.0.0.0', subtype='NONE',
                                       update=update_Local_IP)
    X_Position: bpy.props.FloatProperty(name='X_Position', description='Camera Offset X Position', default=0.0,
                                        subtype='NONE', update=update_X_Position)
    Y_Position: bpy.props.FloatProperty(name='Y_Position', description='Camera Offset Y Position', default=0.0,
                                        subtype='NONE', update=update_Y_Position)
    Z_Position: bpy.props.FloatProperty(name='Y_Position', description='Camera Offset Z Position', default=0.0,
                                        subtype='NONE', update=update_Y_Position)
    Record: bpy.props.BoolProperty(name='Record', description='', default=False, update=update_Record)


# Check and set if the variable default values
@persistent
def check_variables(dummy):
    if bpy.context.scene.sn_generated_addon_properties_UID_Wedsjpol.set_default:
        bpy.context.scene.sn_generated_addon_properties_UID_Wedsjpol.set_default = False
        set_variables()


# Set the addons array variables
def set_variables():
    pass


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# REGISTER / UNREGISTER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
try:
    def register():
        # Register variables
        bpy.utils.register_class(ArrayCollection_UID_Wedsjpol)
        bpy.utils.register_class(GeneratedAddonProperties_UID_Wedsjpol)
        bpy.types.Scene.sn_generated_addon_properties_UID_Wedsjpol = bpy.props.PointerProperty(
            type=GeneratedAddonProperties_UID_Wedsjpol)
        bpy.app.handlers.load_post.append(check_variables)

        bpy.utils.register_class(SNA_OT_Operator_98368dbebf)
        bpy.utils.register_class(SNA_OT_BTN_5284383e90)
        bpy.utils.register_class(SNA_PT_b6a4a58563)
        bpy.utils.register_class(SNA_OT_BTN_9a2fd396ce)
except:
    pass


def unregister():
    global addon_keymaps
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    # Unregister variables
    bpy.utils.unregister_class(ArrayCollection_UID_Wedsjpol)
    bpy.utils.unregister_class(GeneratedAddonProperties_UID_Wedsjpol)
    # del bpy.types.Scene.sn_generated_addon_properties_UID_Wedsjpol
    bpy.app.handlers.load_post.remove(check_variables)

    bpy.utils.unregister_class(SNA_OT_Operator_98368dbebf)
    bpy.utils.unregister_class(SNA_OT_BTN_5284383e90)
    bpy.utils.unregister_class(SNA_PT_b6a4a58563)
    bpy.utils.unregister_class(SNA_OT_BTN_9a2fd396ce)
