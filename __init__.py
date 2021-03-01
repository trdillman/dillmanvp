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
#  Copyright (C) 2020 Tyler Dillman

# Code inspired and used from Jpef 2019
# ##### END GPL LICENSE BLOCK #####


bl_info = {
    "name": "Virtual Production Tools",
    "author": "Tyler Dillman and Raptor",
    "version": (0, 29),
    "blender": (2, 91, 2),
    "location": "",
    "description": "Realtime Virtual Production Tools",
    "wiki_url": "http://www.tylerdillman.info",
    "tracker_url": "",
    "category": "System"}



import sys
import os
script_file = os.path.realpath(__file__)
directory = os.path.dirname(script_file)
if directory not in sys.path:
   sys.path.append(directory)
 

if "bpy" in locals():
    import importlib
    importlib.reload(vp)
    importlib.reload(ui)
    importlib.reload(osc)
    importlib.reload(data)
    importlib.reload(remote)
else:
    from . import vp
    from . import ui
    from . import osc
    from . import data
    from . import remote

def register():
    print('register dillmanvp tools...')
    if not os.path.isdir('/tmp'):
        try:
            os.mkdir('/tmp')
        except:
            print('ERROR: failed to create /tmp folder')
            sys.exit(1)

    data.register()
    vp.register()
    ui.register()
    osc.register()
    #blemote.register()


def unregister():
    osc.unregister()
    vp.unregister()
    ui.unregister()
    data.unregister()
    #blemote.unregister()




if __name__ == "__main__" or '--testing' in sys.argv:
    register()
