import FreeCADGui, FreeCAD, Part
from pivy.coin import *

class Geometric:
    def __init__(self, obj):
        '''"App two point properties" '''
        obj.addProperty("App::PropertyVector","p1","Line","Start point")
        #obj.addProperty("App::PropertyVector","p2","Line","End point").p2 = FreeCAD.Vector(1,0,0)
        obj.addProperty("App::PropertyLink","link","Link","Linked object").link = FreeCADGui.Selection.getSelectionEx()[0].Object #.SubObjects[0]
        face_hash = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0].hashCode()
        obj.addProperty("App::PropertyInteger","faceId","Link","Linked element of the object").faceId = [ f.hashCode() for f in obj.link.Shape.Faces].index(face_hash)
        FreeCAD.Console.PrintMessage('Element ' + str(obj.faceId) + '\n')
        obj.Proxy = self

    def execute(self, fp):
        '''"Print a short message when doing a recomputation, this method is mandatory" '''
        FreeCAD.Console.PrintMessage('Executed\n')
        FreeCAD.Console.PrintMessage(str(fp.link.Shape.Faces[fp.faceId].CenterOfMass))
        fp.Shape = Part.makeLine(fp.p1,fp.link.Shape.Faces[fp.faceId].CenterOfMass)

    def onBeforeChange(self,obj,prop):
        #FreeCAD.Console.PrintMessage("** on Before Changed\n")
        return

    def onChanged(self, fp, prop):
        '''Do something when a property has changed'''
        return

    def __del__(self):
        FreeCAD.Console.PrintMessage("** onDelete\n")

    @staticmethod
    def New():
        a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Line")
        Geometric(a)
        a.ViewObject.Proxy=0
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.getWorkbench("GDTWB").monitor.append(a.link.Name, a.Name, FreeCAD.ActiveDocument.removeObject, a.Name)
        return a

class Geometry:
  "this class will create a line after the user clicked 2 points on the screen"
  def IsActive(self):
    return True

  def Activated(self):
    Geometric.New()

  def GetResources(self): 
    return {'Pixmap' : 'path_to_an_icon/xline_icon.png', 'MenuText': 'XLine', 'ToolTip': 'Creates a line to object center'} 

FreeCADGui.addCommand('geometry', Geometry())

