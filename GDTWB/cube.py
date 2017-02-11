import FreeCADGui, FreeCAD, Part
from FreeCAD import Vector

class Cube:
    def __init__(self, obj):
        self.Shape = Part.makeBox(10, 10, 10)
        obj.Proxy = self

    def execute(self, fp):
        '''"Print a short message when doing a recomputation, this method is mandatory" '''
        pass

    @staticmethod
    def New():
        doc = FreeCAD.activeDocument()
        if doc == None:
                doc = FreeCAD.newDocument()
        a=doc.addObject("Part::FeaturePython","Cube")
        Cube(a)
        a.ViewObject.Proxy=0
        doc.recompute()
        return a

class CubeV:
  "this class will create a line after the user clicked 2 points on the screen"
  def IsActive(self):
    return True

  def Activated(self):
    Cube.New()

  def GetResources(self): 
    return {'Pixmap' : 'icons/cube_icon.png', 'MenuText': 'Cube', 'ToolTip': 'Creates a cube'} 

FreeCADGui.addCommand('cube', CubeV())

