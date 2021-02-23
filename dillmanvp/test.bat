@ECHO OFF

rem "C:\Program Files\Blender Foundation\Blender 2.90\blender.exe" iphonex.blend  --python-expr "import os,sys; sys.argv.extend(['--testing', '--offscreen']); sys.path.append('C:/'); import dillmanvp"

"C:\Program Files\Blender Foundation\Blender 2.91\blender.exe" iphonex.blend  --python-expr "import os,sys; sys.argv.extend(['--testing', '--offscreen']); sys.path.append('C:/'); import dillmanvp"

PAUSE
