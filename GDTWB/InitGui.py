class GDTWB (Workbench): 
   MenuText = 'GDTWB'

   def Initialize(self):
       import geometry
       commandslist = ['geometry']
       self.appendToolbar(self.__class__.MenuText, commandslist)

   def Activated(self):
       "This function is executed when the workbench is activated"
       import eventMonitor
       self.monitor = eventMonitor.EventMonitor()
       return

   def Deactivated(self):
       "This function is executed when the workbench is deactivated"
       return

   def ContextMenu(self, recipient):
       "This is executed whenever the user right-clicks on screen"
       # "recipient" will be either "view" or "tree"
       self.appendContextMenu(self.__class__.MenuText, self.list) # add commands to the context menu

Gui.addWorkbench(GDTWB()) 

