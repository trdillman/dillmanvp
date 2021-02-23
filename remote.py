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

from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient
import time

import g_vars
from data import upd_settings_sub

rem_server = None
bl_ok = False
g_vars.remote_midi_fb = []
g_vars.remote_osc_fb = []
g_vars.remote_fb = []


def actua_bl():
    for i in range(100):
        if len(g_vars.remote_fb) > 0:
            msg = g_vars.remote_fb.pop(0)
            route = int(msg[0])
            item = msg[1]
            val = float(msg[2])
       
            func = item['func']
            post_func = item['post_func']

            # scene can change in the meanwhile
            try:
                bl_item = bpy.context.scene.VPT_Items[route]
                result = func(bl_item, item, val)

                if bl_item.is_array:
                    current = getattr(item['ref'], item['prop'])[bl_item.array]
                    getattr(item['ref'], item['prop'])[bl_item.array] = post_func(current, result, bl_item)
                else:
                    current = getattr(item['ref'], item['prop'])
                    result2 = post_func(current, result, bl_item)
                    setattr(item['ref'], item['prop'], result2)

                # insert keyframe
                if bl_item.record and bpy.data.screens[0].is_animation_playing:
                    if bl_item.is_array:
                        index = bl_item.array
                        item['ref'].keyframe_insert(data_path=item['prop'], index=index, **item['ks_params'])
                    else:
                        item['ref'].keyframe_insert(data_path=item['prop'], **item['ks_params'])


            except:
                pass

    return 0.001


def Remote_callback(*args):
    bcw = bpy.context.window_manager
    fail = True
    #bcw.vpt_osc_lastaddr = args[0]
    content = ""
    args = list(args)

    # still needed to decode the address
    addr = args[0].decode('UTF-8')

     #for i in args[1:]:
    #    content += str(i) + " "
    #bpy.context.window_manager.addosc_lastpayload = content
    #print(content)
    route = args[1]
    if addr == '/blender':
        dico = g_vars.vpt_remote.get(route)
        if dico['engine'] == 'MIDI':
            chan = dico['trigger']['channel']
            cont_type = dico['trigger']['cont_type']
            controller = dico['trigger']['controller']
            g_vars.remote_midi_fb.append([chan, cont_type, controller, args[2]])

        elif dico['engine'] == 'OSC':
            g_vars.remote_osc_fb.append([dico['trigger'], args[2]])
            #print(dico['trigger'], args[1])

        elif dico['engine'] == 'Remote':
            g_vars.remote_fb.append([route, dico['trigger'], args[2]])

    #g_vars.append(args)
    # if args[0] == '/GET_ROUTES':
    #     print("GET ROUTES")
    #     for item in bpy.context.scene.VPT_Items:
    #         print(repr(item))


def save_remote_addr_in(self, context):
    upd_settings_sub(20)
    #bpy.ops.vpt.refresh_remote()


def save_remote_port_in(self, context):
    upd_settings_sub(21)
    #bpy.ops.vpt.refresh_remote()


def save_remote_addr_out(self, context):
    upd_settings_sub(22)


def save_remote_port_out(self, context):
    upd_settings_sub(23)


rem_server = OSCThreadServer(encoding='utf8', default_handler=Remote_callback)


def redraw_hack():
    # trick to update the GUI
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()


def retry_server():
    global rem_server, bl_ok
    pref = bpy.context.preferences.addons['VPT'].preferences
    bcw = bpy.context.window_manager
    ip = pref.remote_udp_in
    port = pref.remote_port_in

    # open connection
    if pref.remote_enable is True and bl_ok is False:
        # try closing a previous instance
        try:
            sock = rem_server.listen(address=ip, port=port, default=False)
            bcw.vpt_remote_alert = False
            bl_ok = True
            redraw_hack()

        except:
            if bcw.vpt_remote_alert is not True:
                bcw.vpt_remote_alert = True
                redraw_hack()

    # close connection
    if pref.remote_enable is False and bl_ok is True:
        # try closing a previous instance
        rem_server.stop_all()
        bl_ok = False

    return 1


bpy.types.WindowManager.vpt_remote_udp_in = bpy.props.StringProperty(
    default="0.0.0.0",
    update=save_remote_addr_in,
    description='The IP of the interface of your Blender machine to listen on, set to 0.0.0.0 for all of them')

bpy.types.WindowManager.vpt_remote_udp_out = bpy.props.StringProperty(
    default="127.0.0.1",
    update=save_remote_addr_out,
    description='The IP of Remote to send messages to')

bpy.types.WindowManager.vpt_remote_port_in = bpy.props.IntProperty(
    default=9003,
    min=0,
    max=65535,
    update=save_remote_port_in,
    description='The input network port (0-65535)')

bpy.types.WindowManager.vpt_remote_port_out = bpy.props.IntProperty(
    default=9004,
    min=0,
    max=65535,
    update=save_remote_port_out,
    description='The output network port (0-65535)')
bpy.types.WindowManager.vpt_remote_alert = bpy.props.BoolProperty()


cls = (#VPT_Refresh_Remote,
       )


def remote_poll():
    pref = bpy.context.preferences.addons['VPT'].preferences
    osc = OSCClient(pref.remote_udp_out, pref.remote_port_out, encoding='utf8')

    '''
    for item in g_vars.vpt['remote']:
        addr = str.encode(item['address'])
        osc.send_message(addr, [val2])
    '''
    addr = str.encode('/BLEMOTE_ROUTES')
    osc.send_message(addr, [str.encode('START')])
    if g_vars.vpt_remote:
        for item in g_vars.vpt_remote.items():
            route = item[0]
            dico = item[1]
            to_send = [route, dico['min'], dico['max']]
            osc.send_message(addr, to_send)
    osc.send_message(addr, ['STOP'])
    return 3


def register():
    bpy.app.timers.register(actua_bl, persistent=True)
    #bpy.app.timers.register(retry_server, persistent=True)
    #bpy.app.timers.register(remote_poll, persistent=True)
    for c in cls:
        register_class(c)


def unregister():
    bpy.app.timers.unregister(actua_bl)
    #bpy.app.timers.unregister(retry_server)
    #bpy.app.timers.unregister(remote_poll)
    for c in cls:
        unregister_class(c)


if __name__ == "__main__":
    register()