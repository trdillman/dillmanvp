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
USE_MINI_JPG = False

bl_info = {
    "name": "Virtual Production Tools",
    "author": "Tyler Dillman and Raptor",
    "version": (0, 28),
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

## defaults to near 30fps ##
#STREAM_MODE = 'webp'  ## note: there is a bug in firefox 'load' not getting called at right time
STREAM_MODE = 'jpg'
USE_BGL = True
CAP_RATE = 0.016
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

OSTYPE = platform.system()
CONVERT_EXE = 'convert'  ## Linux
TMP_PNG = '/tmp/stream.png'
TMP_JPG = '/tmp/stream.jpg'
TMP_JPG_WRITE = '/tmp/__stream__.jpg'
TMP_MINI_JPG = '/tmp/stream.min.jpg'
TMP_WEBP = '/tmp/stream.webp'
if OSTYPE=='Windows':
    CONVERT_EXE = os.path.join(directory, 'convert.exe')
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

if '--offscreen' in sys.argv:
    ##OffScreen = gpu.types.GPUOffScreen(CAP_WIDTH, CAP_HEIGHT)   ## this sounds like a bad idea, see comments above by Mr.Epic and reg.cs
    USE_OFFSCREEN = True
    USE_BGL = False
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
else:
    raise RuntimeError("OLD STYLE IS DEPRECATED")


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
            //console.log('A ready');
            //if (!B.hidden) {
            //    B.hidden=true; 
            //    B.src = "/stream.%s?" + Math.random();
            //}
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
            //console.log('B ready');
            //if (!A.hidden) {
            //    A.hidden=true; 
            //    A.src = "/stream.%s?" + Math.random();
            //}
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
        img.src = "/stream.%s?" + Math.random() +'|'+ MX+','+MY+','+MZ+',' + RA+','+RB+','+RG;
    }
}
function start() {
    var div = document.getElementById("STREAM");
    div.appendChild( A );
    div.appendChild( B );
    setInterval(loop, %s);

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
</html>''' % (STREAM_MODE, STREAM_MODE, STREAM_MODE, JS_RATE)

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
            if USE_MINI_JPG and os.path.isfile(TMP_MINI_JPG):
                data = open(TMP_MINI_JPG, 'rb').read()
                if len(data):
                    os.unlink(TMP_MINI_JPG)
                else:
                    data = b''
            elif USE_OFFSCREEN:
                if os.path.isfile(TMP_JPG):
                    data = open(TMP_JPG, 'rb').read()
                    os.unlink(TMP_JPG)
                    PREV_FRAME_DATA = data
                else:
                    data = PREV_FRAME_DATA

            #if data is None:
            #    if PREV_FRAME_DATA:
            #        data = PREV_FRAME_DATA
            #    else:
            #        data = open(TMP_JPG, 'rb').read()
            #else:
            #    PREV_FRAME_DATA = data
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
    bl_label = "dillmanvp main"
    bl_options = {'REGISTER'}

    def modal(self, context, event):
        global COMMANDS
        #print(event.type)
        if event.type == "TIMER":
            if USE_OFFSCREEN:
                #view_matrix = context.scene.camera.matrix_world.inverted()
                #projection_matrix = context.scene.camera.calc_matrix_camera(context.evaluated_depsgraph_get(), x=CAP_WIDTH, y=CAP_HEIGHT)
                #OffScreen.draw_view3d(
                #    scene,
                #    context.view_layer,
                #    context.space_data,
                #    context.region,
                #    view_matrix,
                #    projection_matrix)
                #bgl.glDisable(bgl.GL_DEPTH_TEST)
                #draw_texture_2d(offscreen.color_texture, (0, 0), dWIDTH, dHEIGHT)
                #bgl.glReadPixels(0, 0, CAP_WIDTH, CAP_HEIGHT, bgl.GL_RGBA, bgl.GL_FLOAT, buffer)
                if not os.path.isfile(TMP_JPG):

                    ## this is very fast, but how to set the camera view?
                    bpy.ops.render.opengl(animation=False, render_keyed_only=False, sequencer=False, write_still=True, view_context=False)

                    ## this is an atomic rename on Linux
                    #os.system('mv -v %s %s' %(TMP_JPG_WRITE, TMP_JPG) )
                    ## is os.rename atomic on Windows?
                    #https://bugs.python.org/issue8828
                    os.rename(TMP_JPG_WRITE, TMP_JPG)

            elif USE_BGL:
                if bpy.context.active_object and bpy.context.active_object.type=='GPENCIL':
                    return {'PASS_THROUGH'}
                #print('saving /tmp/stream.jpg')
                #bgl.glReadBuffer(bgl.GL_BACK)
                #bgl.glReadPixels(0, 0, 320, 240, bgl.GL_RGBA, bgl.GL_UNSIGNED_BYTE, buffer)
                bgl.glReadPixels(CAP_FUDGE_X, CAP_FUDGE_Y, CAP_WIDTH, CAP_HEIGHT, bgl.GL_RGBA, bgl.GL_FLOAT, buffer)
                ## hopefully foreach_set runs at the C-level
                buffer_image.pixels.foreach_set(buffer)
                buffer_image.save()
                if STREAM_MODE=='webp' and not os.path.isfile(TMP_WEBP):
                    subprocess.Popen([CONVERT_EXE, '-strip', '-interlace', 'Plane', '-gaussian-blur', '0.05', '-quality', '80%', TMP_JPG, TMP_WEBP])
                if USE_MINI_JPG and not os.path.isfile(TMP_MINI_JPG):
                    subprocess.Popen([
                        CONVERT_EXE, '-strip', '-interlace', 'Plane', 
                        #'-gaussian-blur', '0.05', 
                        '-quality', '90%', 
                        TMP_JPG, TMP_MINI_JPG
                    ])
            else:
                #print('saving /tmp/stream.png')
                bpy.ops.screen.screenshot(
                    filepath="/tmp/stream.png", 
                    hide_props_region=True, check_existing=False, 
                    show_multiview=False, use_multiview=False,
                    display_type='DEFAULT', 
                    full=True  ## note if this is set to False it breaks
                )
                print('saving /tmp/stream.jpg')
                ## note convert.exe on Windows will not work with unix style paths
                subprocess.check_call([CONVERT_EXE, '-strip', '-interlace', 'Plane', '-gaussian-blur', '0.05', '-quality', '80%', TMP_PNG, TMP_JPG])

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

            COMMANDS = []

            if DEVCAM is not None:
                assert len(DEVCAM)==6
                mx,my,mz, ra,rb,rg = DEVCAM
                cam = bpy.data.objects['Camera']
                cam.location.x += mx * 0.1
                cam.location.z += my * 0.1

        return {'PASS_THROUGH'}  ## will not supress event bubbles

    def invoke(self, context, event):
        global _mainloop_timer
        if _mainloop_timer is None:
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


def register():
    print('register dillmanvp tools...')
    if not os.path.isdir('/tmp'):
        try:
            os.mkdir('/tmp')
        except:
            print('ERROR: failed to create /tmp folder')
            sys.exit(1)

    bpy.utils.register_class(MainLoop)
    if '--https' in sys.argv:
        run_https()
    else:
        run_http()
    data.register()
    vp.register()
    ui.register()
    osc.register()
    #blemote.register()
    bpy.ops.dillmanvp.main()


def unregister():
    osc.unregister()
    vp.unregister()
    ui.unregister()
    data.unregister()
    #blemote.unregister()




if __name__ == "__main__" or '--testing' in sys.argv:
    register()
