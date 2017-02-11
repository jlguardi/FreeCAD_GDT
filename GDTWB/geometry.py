import FreeCADGui, FreeCAD, Part
from FreeCAD import Vector

def makeArrow(p1, p2, projection_plane=Vector(0,0,1), arrow_length=1, arrow_width=1):
    l = Part.Line(p1, p2)
    direction = p1.sub(p2).normalize()
   
    ortho = direction.cross(projection_plane)
    if ortho.Length < 0.05:
        ortho = direction.cross(Vector(1,0,0))
    ortho = ortho.normalize()

    direction = direction.multiply(arrow_length)
    ortho = ortho.multiply(arrow_width)
    arrow_p1 = p2.add(direction).add(ortho)
    arrow_p2 = p2.add(direction).sub(ortho)
    arrow1 = Part.Line(p2, arrow_p1)
    arrow2 = Part.Line(p2, arrow_p2)

    arrow_p1 = p1.sub(direction).add(ortho)
    arrow_p2 = p1.sub(direction).sub(ortho)
    arrow3 = Part.Line(p1, arrow_p1)
    arrow4 = Part.Line(p1, arrow_p2)
    return Part.Shape([l, arrow1, arrow2, arrow3, arrow4])

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
        #FreeCAD.Console.PrintMessage('Executed\n')
        faces = fp.link.Shape.Faces
        if fp.faceId > len(faces):
            fp.faceId = 0
        end_point = faces[fp.faceId].CenterOfMass
        fp.Shape = makeArrow(fp.p1, end_point)

    def onBeforeChange(self, fp, prop):
        if prop == 'link':
            self.oldName = fp.link.Name 
        #FreeCAD.Console.PrintMessage("** on Before Changed" + fp.Name + ":" + prop + "\n")
        return

    def onChanged(self, fp, prop):
        '''Do something when a property has changed'''
        #FreeCAD.Console.PrintMessage("** on Changed " + fp.Name + " : " + prop + "\n")
        if prop == 'link':
            if not fp.link:
                #FreeCAD.Console.PrintMessage("Link removed\n")
                return
            #FreeCAD.Console.PrintMessage("Change the link " + fp.link.Name + '\n')
            self.execute(fp)
            FreeCAD.activeDocument().recompute()
            FreeCADGui.getWorkbench("GDTWB").monitor.remap(self.oldName, fp.link.Name, fp.Name)
        return

    @staticmethod
    def New():
        doc = FreeCAD.activeDocument()
        if doc == None:
                doc = FreeCAD.newDocument()
        a=doc.addObject("Part::FeaturePython","Line")
        Geometric(a)
        a.ViewObject.Proxy=0
        doc.recompute()
        FreeCADGui.getWorkbench("GDTWB").monitor.append(a.link.Name, a.Name, FreeCAD.ActiveDocument.removeObject, a.Name)
        return a

class Geometry:
  "this class will create a line after the user clicked 2 points on the screen"
  def IsActive(self):
    return True

  def Activated(self):
    Geometric.New()

  def GetResources(self): 
    return {'Pixmap' : 'icons/geometry_icon.png', 'MenuText': 'Geometry', 'ToolTip': 'Creates a geometry annotation from face center'} 

FreeCADGui.addCommand('geometry', Geometry())

