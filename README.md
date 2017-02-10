# FreeCAD GDT plugin

By now:

Example workbench with just a command (geometry) which creates a line from origin (0,0,0) to the middle of the selected face.

If no selection while creation: Exception!!

Main properties: created line links object. It means:
  - line is deleted if you delete the object
  - line is updated if you edit object

Howto install:
 - just copy the GDTWB dir to /usr/lib/freecad/Mod/
 - restart FreeCAD!
