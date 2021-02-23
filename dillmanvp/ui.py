# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#  Copyright (C) 2019 JPfeP
#
# ##### END GPL LICENSE BLOCK #####


import bpy
from bpy.utils import register_class, unregister_class
from bpy.types import Panel
from bpy.types import Menu
from data import generate_dict
import g_vars


class VIEW3D_PT_VPT_MIDI_Config(Panel):
    bl_category = "OSC"
    bl_idname = "VIEW3D_PT_vpt_config_midi"
    bl_label = "MIDI Config"
    bl_space_type = "EMPTY"
    bl_region_type = "UI"
    # bl_context = "objectmode"



class VIEW3D_PT_VPT_OSC_Config(Panel):
    bl_category = "OSC"
    bl_idname = "VIEW3D_PT_vpt_config_osc"
    bl_label = "OSC Config"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"


    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        row = col.row(align=True)
        row.alert = bpy.context.window_manager.vpt_osc_alert and bpy.context.window_manager.vpt_osc_in_enable
        row.prop(bpy.context.window_manager, 'vpt_osc_udp_in', text="Listen on ")
        row.prop(bpy.context.window_manager, 'vpt_osc_port_in', text="Input port")
        row.prop(bpy.context.window_manager, 'vpt_osc_in_enable', text="")

        col2 = layout.column(align=True)
        row2 = col2.row(align=True)
        row2.prop(bpy.context.window_manager, 'vpt_osc_udp_out', text="Destination address")
        row2.prop(bpy.context.window_manager, 'vpt_osc_port_out', text="Outport port")
        row2.prop(bpy.context.window_manager, 'vpt_osc_out_enable', text="")

        col3 = layout.column()
        row3 = col3.row(align=True)
        row3.prop(bpy.context.window_manager, 'vpt_osc_debug', text='Debug')


class VIEW3D_PT_VPT_Remote_Config(Panel):
    bl_category = "OSC"
    bl_idname = "VIEW3D_PT_vpt_config_remote"
    bl_label = "Remote Config"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        row = col.row(align=True)
        row.alert = bpy.context.window_manager.vpt_remote_alert
        row.prop(bpy.context.window_manager, 'vpt_remote_udp_in', text="Listen on ")
        row.prop(bpy.context.window_manager, 'vpt_remote_port_in', text="Input port")

        col2 = layout.column(align=True)
        row2 = col2.row(align=True)
        row2.prop(bpy.context.window_manager, 'vpt_remote_udp_out', text="Destination address")
        row2.prop(bpy.context.window_manager, 'vpt_remote_port_out', text="Outport port")


class VIEW3D_PT_VPT_Tools(Panel):
    bl_category = "OSC"
    bl_idname = "VIEW3D_PT_vpt_tools"
    bl_label = "VPT TOOLS PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        row = col.row(align=True)
        row.prop(context.scene, 'VPT_catenum')
        row.operator('vpt.addcat', icon='ADD', text='')
        row.operator('vpt.removecat', icon='PANEL_CLOSE', text='')

        row = col.row(align=True)
        row.operator('vpt.renamecat')
        row.operator('vpt.copycat')

        col = layout.column()
        col.label(text='Routes sorting:')
        row = col.row(align=True)
        row.prop(context.scene, 'VPT_sorting', expand=True)

        box = layout.box()
        box.label(text="Extra route parameters:")
        box.prop(context.scene, 'show_postprocess')
        box.prop(context.scene, 'show_categories')
        box.prop(context.scene, 'show_routes_number')


class VIEW3D_PT_VPT_Routes(Panel):
    bl_category = "OSC"
    bl_label = "Routes"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_idname = "VIEW3D_PT_VPT_routes"
    # bl_context = "objectmode"


    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        layout.operator("vpt.addprop", text='Add route')

        for i, item in enumerate(bpy.context.scene.VPT_Items):
             if (item.category == context.scene.VPT_catenum and context.scene.VPT_sorting == 'Category') or context.scene.VPT_sorting == 'None':
                box = layout.box()

                # line 1
                if context.window_manager.vpt_osc_debug or context.window_manager.vpt_midi_debug or context.scene.show_routes_number:
                    box.label(text='Route #'+str(i))

                row = box.row()
                if item.alert is True and item.mode != 'Off':
                    box.alert = True

                row.prop(item, 'id_type', icon_only=True)


                #Note: arg1= target ID pointer, arg2= name of the according prop, arg3= obvious, arg4= ID cat of the scene
                if item.is_multi and (item.VAR_use == 'name'):
                    row.prop(item, 'name_var')
                else:
                    row.prop_search(item.id, item.id_type, bpy.data, item.id_type, text='')

                row.operator("vpt.copyprop", icon='ADD', text='').n = i
                row.operator("vpt.removeprop", icon='PANEL_CLOSE', text='').n = i

                # line 2
                split = box.split(factor=.8)
                row_dp = split.row(align=True)
                row_dp.prop(item, 'data_path')

                split2 = box.split(factor=0.8)
                row_e = split2.row(align=True)
                row_e.prop(item, 'engine', expand=True)
                row_e2 = split2.row(align=True)
                if item.engine != 'Remote':
                    row_e2.prop(item, 'bl_switch', text='BL')
                else:
                    row_e2.prop(item, 'record', text='Rec', icon='RADIOBUT_ON')

                row_dp2 = split.row(align=True)
                if item.is_array:
                    if item.engine == 'MIDI' or item.engine == 'Remote':
                        row_dp.prop(item, 'array', text="")
                    elif item.engine == 'OSC':
                        if item.use_array is False:
                            row_dp.prop(item, 'array', text='')
                        row_dp2.prop(item, 'use_array')
                if item.is_angle:
                    row_dp2.prop(item, 'rad2deg')

                row = box.row()
                if item.engine == 'MIDI':

                    row.prop(item, 'channel')
                    row.prop(item, 'cont_type', text='')

                    # Events with filter option
                    if item.f_show :
                        row.prop(item, 'filter')

                    # If filter on
                    if item.filter:
                        box.prop(item, 'controller', text='Select')

                    col3 = box.column(align=True)
                    col3.label(text='Rescale:')
                    row3 = col3.row(align=True)
                    row3.prop(item, 'rescale_mode', expand=True)
                    if item.rescale_mode != 'Auto' and item.rescale_mode != 'Direct':
                        row3 = col3.row(align=True)
                        row3.label(text='MIDI')
                        row3.prop(item, 'rescale_outside_low')
                        row3.prop(item, 'rescale_outside_high')
                    if item.rescale_mode != 'Direct':
                        row4 = col3.row(align=True)
                        row4.label(text='Blender')
                        row4.prop(item, 'rescale_blender_low')
                        row4.prop(item, 'rescale_blender_high')

                # For OSC
                elif item.engine == 'OSC':
                    row.prop(item, 'osc_address')
                    row.operator("vpt.osc_pick", text='Pick').n = i

                    split = box.split(factor=0.8)
                    row = split.row(align=True)
                    #row.prop(item, 'filter', text='Extract')
                    row.prop(item, 'osc_select_rank')
                    row.prop(item, 'osc_select_n')
                    row = split.row()
                    row.alignment = 'CENTER'
                    if item.is_array and item.use_array:
                        row.label(text='(' + str(item.len) + ')')
                    else:
                        row.label(text='(1)')

                if item.engine != 'Remote':
                    row = box.row()
                    row.prop(item, 'mode', expand=True)
                    row.prop(item, 'record', text='Rec', icon='RADIOBUT_ON')

                row = box.row()
                if item.record:
                    row.label(text='Keyframes settings:')
                    row = box.row()
                    row.prop(item, 'kf_needed', text='Needed')
                    row.prop(item, 'kf_visual', text='Visual')
                    row.prop(item, 'kf_rgb', text='XYZ to RGB')
                    row = box.row()
                    row.prop(item, 'kf_replace', text='Replace')
                    row.prop(item, 'kf_available', text='Available')
                    row.prop(item, 'kf_cycle', text='Cycle aware')
                    box.prop(item, 'kf_group', text='Group')

                if context.scene.show_postprocess:
                    row = box.row()
                    row.label(text='Envelope settings:')
                    row.prop(item, 'env_attack', text='Attack')
                    row.prop(item, 'env_release', text='Release')
                    row = box.row()
                    row.prop(item, 'env_auto')
                    row.operator("vpt.midienv", text='Apply Envelope').n = i

                row = box.row()
                row.prop(item, 'eval_mode')
                if item.eval_mode == 'expr':
                    row = box.row()
                    row.prop(item, 'eval_expr')

                if item.engine == 'MIDI' or item.engine == 'OSC':
                    row = box.row()
                    row.prop(item, 'is_multi')
                    if item.is_multi:
                        row.prop(item, 'number')
                        row = box.row()
                        row.prop(item, 'VAR_use')
                        row.prop(item, 'offset')

                if context.scene.show_categories:
                    row = box.row()
                    row.prop(item, 'category')

                # this is for Remote, later
                if item.bl_switch or item.engine == 'Remote':
                    box = box.box()
                    box.label(text='Remote slider:')
                    row = box.row()
                    row.prop(item, 'bl_min')
                    row.prop(item, 'bl_max')

        if bpy.context.scene.VPT_Items:
            layout.operator("vpt.addprop", text='Add route')


class VPT_AddProp(bpy.types.Operator):
    '''Add a route'''
    bl_idname = "vpt.addprop"
    bl_label = "VPT Add Route"

    def execute(self, context):
        my_item = bpy.context.scene.VPT_Items.add()
        my_item.cont_type = 'key_on'
        return{'FINISHED'}


class VPT_RemoveProp(bpy.types.Operator):
    '''Remove route'''
    bl_idname = "vpt.removeprop"
    bl_label = "VPT Remove Route"
    #bl_options = {'UNDO'}

    n: bpy.props.IntProperty()
    
    def execute(self, context):
        bpy.context.scene.VPT_Items.remove(self.n)
        generate_dict(self, context)
        return{'FINISHED'}


class VPT_CopyProp(bpy.types.Operator):
    '''Copy a route'''
    bl_idname = "vpt.copyprop"
    bl_label = "Copy Route"

    n: bpy.props.IntProperty()

    def execute(self, context):
        my_item = bpy.context.scene.VPT_Items.add()
        for k, v in bpy.context.scene.VPT_Items[self.n].items():
            my_item[k] = v
        generate_dict(self, context)
        return{'FINISHED'}


def highest_rank(scene):
    highest = 0
    for item in scene.VPT_categories:
        if item.rank > highest:
            highest = item.rank
    return highest + 1


def list_scenes(self, context):
    result = []
    for sce in bpy.data.scenes:
        result.append((sce.name, sce.name, ''))
    return result


class VPT_CopyCategory(bpy.types.Operator):
    '''Copy a whole category to another scene'''
    bl_idname = "vpt.copycat"
    bl_label = "Copy to a scene"
    bl_property = "enumsce"
    #n: bpy.props.IntProperty()
    #targetsce : bpy.props.StringProperty()
    enumsce : bpy.props.EnumProperty(items=list_scenes)

    def invoke(self, context, event):
        wm = context.window_manager
        wm.invoke_search_popup(self)
        return {'FINISHED'}

    def execute(self, context):
        sce = bpy.data.scenes[self.enumsce]
        # first check is a similar category exist there
        if sce.VPT_categories.find(context.scene.VPT_catenum) == -1:
            new = sce.VPT_categories.add()
            new.name = context.scene.VPT_catenum
            new.rank = highest_rank(sce)

        for item in bpy.context.scene.VPT_Items:
            if item.category == context.scene.VPT_catenum:
                my_item = sce.VPT_Items.add()
                for k, v in item.items():
                    if k != 'category':
                        my_item[k] = v
                    else:
                        my_item[k] = sce.VPT_categories[context.scene.VPT_catenum].rank
        return{'FINISHED'}


class VPT_CreateCategory(bpy.types.Operator):
    '''Create a category'''
    bl_idname = "vpt.addcat"
    bl_label = "Create a category"

    name: bpy.props.StringProperty(default='New Category')

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        new = context.scene.VPT_categories.add()
        new.name = self.name
        new.rank = highest_rank(context.scene)

        return{'FINISHED'}


class VPT_RenameCategory(bpy.types.Operator):
    '''Rename a category'''
    bl_idname = "vpt.renamecat"
    bl_label = "Rename"

    name: bpy.props.StringProperty(default='New Category')

    def invoke(self, context, event):
        if context.scene.VPT_catenum == 'Default':
            self.report({'INFO'}, "'Default' cannot be renamed !")
            return{'FINISHED'}
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        n = context.scene.VPT_categories.find(context.scene.VPT_catenum)
        target = context.scene.VPT_categories[n]
        target.name = self.name

        return{'FINISHED'}


class VPT_RemoveCategory(bpy.types.Operator):
    '''Remove a category'''
    bl_idname = "vpt.removecat"
    bl_label = "Remove a category"

    def execute(self, context):
        for item in context.scene.VPT_Items:
            if item.category == context.scene.VPT_catenum:
                item.category = 'Default'

        rank = context.scene.VPT_categories.find(context.scene.VPT_catenum)
        context.scene.VPT_categories.remove(rank)
        context.scene.VPT_catenum = 'Default'

        return{'FINISHED'}





# This class has to be exactly named like that to insert an entry in the right click menu
class WM_MT_button_context(Menu):
    bl_label = "Unused"

    def draw(self, context):
        pass


class VPT_OscPick(bpy.types.Operator):
    '''Pick last event OSC address'''
    bl_idname = "vpt.osc_pick"
    bl_label = "VPT OSC event pick address"
    # bl_options = {'UNDO'}

    n: bpy.props.IntProperty()

    def execute(self, context):
        if g_vars.last_osc_addr is not None:
            bpy.context.scene.VPT_Items[self.n].osc_address = g_vars.last_osc_addr

        return {'FINISHED'}


def menu_func(self, context):
    layout = self.layout
    layout.separator()



cls = ( VPT_AddProp,
        VPT_RemoveProp,
        VPT_CopyProp,
        VPT_CreateCategory,
        VPT_CopyCategory,
        VPT_RemoveCategory,
        VPT_RenameCategory,
        VPT_OscPick,
        
        VIEW3D_PT_VPT_OSC_Config,
        #VIEW3D_PT_VPT_Remote_Config,
        
        VIEW3D_PT_VPT_Routes,
        WM_MT_button_context
    )


def register():
    for c in cls:
        register_class(c)
    bpy.types.WM_MT_button_context.append(menu_func)


def unregister():
    bpy.types.WM_MT_button_context.remove(menu_func)  # order was important
    for c in cls:
        unregister_class(c)


if __name__ == "__main__":
    register()

