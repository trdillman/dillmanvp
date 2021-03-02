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

import bpy, platform, os, sys
from bpy.app.handlers import persistent
OSTYPE = platform.system()


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

        if not DO_CAPTURE:
            layout.operator("dillmanvp.main", text="Start Server", emboss=True, depress=False)

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

## Streaming Server ##
HTTPD = None
DO_CAPTURE = False
#STREAM_MODE = 'webp'  ## note: there is a bug in firefox 'load' not getting called at right time
STREAM_MODE = 'jpg'
CAP_RATE = 0.04
JS_RATE  = 35
if '10fps' in sys.argv:
    CAP_RATE = 0.1
    JS_RATE  = 100
elif '20fps' in sys.argv:
    CAP_RATE = 0.05
    JS_RATE  = 50

if '--https' in sys.argv:
    JS_RATE += 5

## iphonex 375x812
CAP_WIDTH = 375
CAP_HEIGHT = 812
CAP_FUDGE_X = 135
CAP_FUDGE_Y = 20

import bpy, bgl, gpu
from bpy.utils import register_class, unregister_class
from bpy.types import AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty

import http.server, socketserver, threading, subprocess, platform
from http import HTTPStatus
SimpleHTTPServer = http.server
SocketServer = socketserver

TMP_PNG = '/tmp/stream.png'
TMP_JPG = '/tmp/stream.jpg'
TMP_JPG_WRITE = '/tmp/__stream__.jpg'
TMP_MINI_JPG = '/tmp/stream.min.jpg'
TMP_WEBP = '/tmp/stream.webp'
if OSTYPE=='Windows':
    TMP_PNG = 'C:\\tmp\\stream.png'
    TMP_JPG = 'C:\\tmp\\stream.jpg'
    TMP_MINI_JPG = 'C:\\tmp\\stream.min.jpg'
    TMP_WEBP = 'C:\\tmp\\stream.webp'


## https://blender.stackexchange.com/questions/176548/how-do-you-use-the-gpu-offscreen-render-api-in-2-8
'''The main caveat is that the currently offscreen.draw_view3d() is called within draw() using bpy.types.SpaceView3D.draw_handler_add. 
This has a few consequences: one must ensure that the 3D view is redrawn, for example by clicking onto some object in the 3D view
the function is called multiple times - Mr.Epic Fail
'''
## https://blender.stackexchange.com/questions/190140/copy-framebuffer-of-3d-view-into-custom-frame-buffer
'''
The blender internal GPUOffscreen.draw_view3d functionality unfortunately takes 10 to 50 ms per call - reg.cs
'''

def resize_capture(width, height):
    global CAP_WIDTH, CAP_HEIGHT
    print("resize_capture:", width, height)
    CAP_WIDTH = width
    CAP_HEIGHT = height
    scene = bpy.data.scenes[0]
    scene.render.resolution_x = CAP_WIDTH
    scene.render.resolution_y = CAP_HEIGHT
    scene.render.resolution_percentage = 100
    scene.render.filepath = TMP_JPG_WRITE
    scene.render.image_settings.file_format = "JPEG"
    scene.render.image_settings.quality = 70
    scene.eevee.taa_render_samples = 16
    scene.eevee.use_taa_reprojection = False
    try:
        os.unlink(TMP_JPG)
    except:
        pass


resize_capture( CAP_WIDTH, CAP_HEIGHT )



TESTPAGE = '''
<html>
<head>
<script>
var A = new Image();
var B = new Image();
A.hidden = true;
B.hidden = false;
A.style.position='absolute';
B.style.position='absolute';
A.style.left='0px';
B.style.left='0px';
A.style.top='0px';
B.style.top='0px';
A.is_ready = true;
B.is_ready = true;

var RA = 0;
var RB = 0;
var RG = 0;
var MX = 0;
var MY = 0;
var MZ = 0;

var C = true;
var READY = true;
A.addEventListener('load', function() {
        if (A.complete && A.naturalHeight !== 0){
            B.is_ready = true;
            //A.hidden=false;
            A.style.zIndex=10;
            B.style.zIndex=9;
            READY=true; 
        }
    }
); 
B.addEventListener('load', function() {
        if (B.complete && B.naturalHeight !== 0) {
            B.is_ready = true;
            //B.hidden=false;
            B.style.zIndex=10;
            A.style.zIndex=9;
            READY=true;
        }
    }
);
function loop() {
    var img, other;
    var div = document.getElementById("STREAM");
    //while (div.firstChild) {div.removeChild(div.firstChild);}
    if (C) {
        C = false;
        img = A;
        other = B;
    } else {
        C = true;
        img = B;
        other = A;
    }
    //if (img.hidden) {
    //if (READY && img.hidden && !other.hidden) {
    if (READY && img.is_ready) {
        READY = false;
        img.is_ready = false;
        //img.hidden = true;
        //img.src = "";
        img.complete = false;
        // this ?+Math.random() hack is a workaround for the browser cache
        img.src = "/stream.<MODE>?" + Math.random() +'|'+ MX+','+MY+','+MZ+',' + RA+','+RB+','+RG;
    }
}
function start() {
    /*
    A.style.width=window.innerWidth;
    A.style.height=window.innerHeight;
    B.style.width=window.innerWidth;
    B.style.height=window.innerHeight;
    */
    A.style.width='100%';
    A.style.height='100%';
    B.style.width='100%';
    B.style.height='100%';

    var div = document.getElementById("STREAM");
    div.appendChild( A );
    div.appendChild( B );

    /*
    if (window.DeviceOrientationEvent) {
        window.addEventListener('deviceorientation', deviceOrientationHandler);
        alert('dev orientation event OK');
    }
    if (window.DeviceMotionEvent) {
        window.addEventListener('devicemotion', deviceMotionHandler);
        alert('dev motion event OK');
    }
    */
    setTimeout(
        function() {
            send_cmd('window_size?' + window.innerWidth + ',' + window.innerHeight );
        },
        1000
    );

    setInterval(loop, <RATE>);

}
function toggle_play(btn) {
    if (btn.value=='play') btn.value = 'stop';
    else btn.value = 'play';
    req = new XMLHttpRequest();
    req.open("GET", "/command.toggle_play", true);
    req.setRequestHeader( 'Access-Control-Allow-Origin', '*');
    //req.onreadystatechange = onreply
    req.send();
}
function send_cmd(cmd) {
    req = new XMLHttpRequest();
    req.open("GET", "/command." + cmd, true);
    req.setRequestHeader( 'Access-Control-Allow-Origin', '*');
    req.send();
}

function deviceOrientationHandler(evt) {
    //console.log(evt);
    if (evt.alpha != null) RA = evt.alpha;
    if (evt.beta  != null) RB = evt.beta;
    if (evt.gamma != null) RG = evt.gamma;
    // why this only sends cmd once? and evt.alpha is null
    //send_cmd('dev_rotate?' + evt.alpha);
}
var _motion_ticker = 0;
function deviceMotionHandler(evt) {
    // this was a bad idea, sending an extra http request is really slow on some mobile devices //
    /*
    if (evt.acceleration.x==0 && evt.acceleration.y==0 && evt.acceleration.z==0) {
        _motion_ticker = 5;
        return;
    }
    if (_motion_ticker >= 5) {
        send_cmd('dev_move?' + evt.acceleration.x + ',' + evt.acceleration.y + ',' + evt.acceleration.z );
        _motion_ticker = 0;
    } else {
        _motion_ticker += 1;
    }
    */
    // instead send the data along with the jpg stream request! //
    MX = evt.acceleration.x;
    MY = evt.acceleration.y;
    MZ = evt.acceleration.z;
}
</script>
</head>
<body onload="start()">
<div style="position:absolute; left:10px; top:5px; z-index:100">
    Dillman VP
    <input type="button" onclick="send_cmd('goto_start')" value="start"></input>
    <input type="button" onclick="toggle_play(this)" value="play"></input>
    <input type="button" onclick="send_cmd('goto_end')" value="end"></input>
</div>
<div id="STREAM"/></div>
</body>
</html>'''.replace( '<MODE>', STREAM_MODE).replace('<RATE>', str(JS_RATE))

PREV_FRAME_DATA = b''
COMMANDS = []
DEVCAM = None

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPServer.SimpleHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        #self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Headers", 'Access-Control-Allow-Origin')
        self.end_headers()

    def do_GET(self):
        global PREV_FRAME_DATA, DEVCAM
        #print(self.path)
        self.send_response(200)
        if self.path.endswith('.html') or self.path=='/':
            self.send_header('Content-type', 'text/html')
        elif self.path.endswith('.json'):
            self.send_header('Content-type', 'application/json')
        elif self.path.startswith('/stream.webp'):
            self.send_header('Content-type', 'image/webp')
        else:
            self.send_header('Content-type', 'image/jpeg')
        self.end_headers()

        if self.path.startswith('/command'):
            COMMANDS.append( self.path )
        elif self.path.startswith('/stream.webp'):
            if os.path.isfile(TMP_WEBP):
                data = open(TMP_WEBP, 'rb').read()
                if len(data):
                    os.unlink(TMP_WEBP)
                    print('streaming webp bytes:', len(data))
                    try:
                        self.wfile.write( data )
                    except:
                        pass

        elif self.path.startswith('/stream.jpg'):
            if '|' in self.path:
                devtrans = self.path.split('|')[-1]
                print('devtrans:', devtrans)
                DEVCAM = [float(f) for f in devtrans.split(',')]

            data = b''
            if os.path.isfile(TMP_JPG):
                try:
                    data = open(TMP_JPG, 'rb').read()
                except:
                    print("WARN: temp jpeg removed while trying to read it")
                try:
                    os.unlink(TMP_JPG)
                except:
                    pass
                PREV_FRAME_DATA = data
            else:
                data = PREV_FRAME_DATA

            print('streaming jpg bytes:', len(data))

            try:
                self.wfile.write( data )
            except:
                ## BrokenPipeError
                pass
        else:
            print('testing TESTPAGE')
            self.wfile.write( TESTPAGE.encode('utf-8') )

httpd = None
def run_http():
    global httpd
    if httpd:
        print("WARN: httpd is already running")
        return
    try:
        httpd = SocketServer.TCPServer(("", 8081), Handler)
    except OSError:
        ## [Errno 98] Address already in use
        httpd = None
    if httpd:
        threading._start_new_thread( httpd.serve_forever, tuple([]) )
        print('running http on localhost:8081')
    else:
        print('ERROR: failed to run http on localhost:8081')
        sys.exit(1)
def run_https():
    global httpd
    import ssl
    try:
        httpd = SocketServer.TCPServer(("", 4443), Handler)
    except OSError:
        ## [Errno 98] Address already in use
        httpd = None
    if httpd:
        pem = os.path.join(directory,'server.pem')
        if not os.path.isfile(pem):
            openssl = 'openssl'
            if OSTYPE == 'Windows':
                openssl = os.path.join(directory, 'openssl.exe')
            subprocess.check_call([openssl, 'req', '-new', '-x509', '-keyout', pem, '-out', pem, '-days', '365', '-nodes'])

        httpd.socket = ssl.wrap_socket(
            httpd.socket, 
            certfile=pem, 
            server_side=True
        )
        threading._start_new_thread( httpd.serve_forever, tuple([]) )
        print('running http on https://localhost:4443')
    else:
        print('ERROR: failed to run http on https://localhost:4443')
        sys.exit(1)


_mainloop_timer = None

# https://blender.stackexchange.com/questions/190140/copy-framebuffer-of-3d-view-into-custom-frame-buffer
# https://stackoverflow.com/questions/60138184/passing-float-value-texture-to-fragment-shader-returns-incorrect-value
#buffer = bgl.Buffer(bgl.GL_INT, 320 * 240 * 4)
#buffer = bgl.Buffer(bgl.GL_BYTE, 320 * 240 * 4)
## note: must read as GL_FLOAT because a blender Image is 32bits, or glReadPixels only works properly with GL_FLOAT.
buffer = bgl.Buffer(bgl.GL_FLOAT, CAP_WIDTH * CAP_HEIGHT * 4)

buffer_image = bpy.data.images.new('__FRAME_BUFFER__', CAP_WIDTH, CAP_HEIGHT)
#buffer_image.depth = 24  ## readonly, must use the default of RGBA, anyways the screen frame buffer is 32bits
buffer_image.filepath = TMP_JPG
buffer_image.file_format = 'JPEG'
buffer_image.use_fake_user = True

## note: if a grease pencil object is selected, performance drops, and blender prints this error:
##LLVM triggered Diagnostic Handler: Illegal instruction detected: VOP* instruction violates constant bus restriction
##renamable $vgpr2 = V_CNDMASK_B32_e32 32768, killed $vgpr2, implicit killed $vcc, implicit $exec
##LLVM failed to compile shader
## note: workaround is not streaming if a grease pencil object is selected
## note: this bug may only appear on Ubuntu20.04 with Radeon drivers.

class MainLoop(bpy.types.Operator):
    "screen capture mainloop"
    bl_idname = "dillmanvp.main"
    bl_label = "start capture"
    bl_options = {'REGISTER'}

    def modal(self, context, event):
        global COMMANDS
        #print(event.type)
        if event.type == "TIMER":
            if DO_CAPTURE:
                if not os.path.isfile(TMP_JPG):
                    bpy.ops.render.opengl(animation=False, render_keyed_only=False, sequencer=False, write_still=True, view_context=False)
                    ## is os.rename atomic on Windows?
                    #https://bugs.python.org/issue8828
                    os.rename(TMP_JPG_WRITE, TMP_JPG)

            for cmd in COMMANDS:
                if cmd == '/command.toggle_play':
                    bpy.ops.screen.animation_play()
                elif cmd == '/command.goto_start':
                    bpy.ops.screen.frame_jump(end=False)
                elif cmd.startswith('/command.goto_end'):
                    bpy.ops.screen.frame_jump(end=True)
                elif cmd.startswith('/command.dev_rotate?'):  ## bad idea
                    args = cmd.split('?')[-1]
                    print('dev_rotate:', args)
                elif cmd.startswith('/command.dev_move?'):    ## bad idea
                    args = cmd.split('?')[-1]
                    print('dev_move:', args)
                    x,y,z = [float(f) for f in args.split(',')]
                    bpy.data.objects['Camera'].location.x += x * 0.1
                    bpy.data.objects['Camera'].location.z += y * 0.1
                elif cmd.startswith('/command.window_size'):
                    args = cmd.split('?')[-1]
                    x,y = [int(f) for f in args.split(',')]
                    resize_capture(x,y)

            COMMANDS = []

            if DEVCAM is not None:
                assert len(DEVCAM)==6
                mx,my,mz, ra,rb,rg = DEVCAM
                cam = bpy.data.objects['Camera']
                cam.location.x += mx * 0.1
                cam.location.z += my * 0.1

        return {'PASS_THROUGH'}  ## will not supress event bubbles

    def invoke(self, context, event):
        global _mainloop_timer, DO_CAPTURE
        DO_CAPTURE = True
        resize_capture( CAP_WIDTH, CAP_HEIGHT )
        if _mainloop_timer is None:
            if '--https' in sys.argv:
                run_https()
            else:
                run_http()

            _mainloop_timer = self._timer = context.window_manager.event_timer_add(
                #time_step=0.0333,  ## this crashes my machine
                time_step=CAP_RATE,
                window=context.window
            )
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        return {'FINISHED'}

    def execute(self, context):
        return self.invoke(context, None)



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# REGISTER / UNREGISTER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def register():
    try:
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


        bpy.utils.register_class(MainLoop)

    except:
        print("WARN: vp.py register stuff failed")


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
