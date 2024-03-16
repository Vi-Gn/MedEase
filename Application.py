"""
Copyright 2024 Anouar El Harrak

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
from tkinter import Tk as TTk, messagebox, ttk
from typing import Self


from FrameTab import FrameTab
from FramedTable import FramedTable
from MainFrame import MainFrame
from MainMenu import MainMenu
from FileManager import TFileManager

    
class Application(TTk):
  _instance = None
  def __new__(cls, *args, **vargs) -> Self:
    if cls._instance == None:
      cls._instance = super().__new__(cls)
    return cls._instance
  
  @staticmethod
  def Get():
      return Application._instance

  def __init__(self, title: str = 'MedEase', iconRelPath: str = 'Icon/meds.ico', width: int = 1024, height: int = 450, state: str ='normal') -> None:
    '''state: [normal, icon, iconic (see wm_iconwindow), withdrawn, or zoomed (Windows only)]'''
    super().__init__()
    self.Title: str = title
    self.title(title)
    self.iconbitmap(iconRelPath)
    self.state(state)
    self.geometry(f"{width}x{height}")
    self.minsize(width=width, height=height)
    self.CenterWindow()
    self.mainmenu = MainMenu(self)
    self.mainframe = MainFrame(appRoot=self, labelText='App')
    self.frameTabFile = FrameTab(mainFrame=self.mainframe, colIndex=0, width=250)
    self.framedTableFile: FramedTable = FramedTable(frameTab=self.frameTabFile, tabname='taby')
    self.framedTableFile.InitTableFile(relpath='-1',show='tree headings')
    self.frameTabData = FrameTab(mainFrame=self.mainframe, colIndex=1, width=100)
    self.framedTableData: FramedTable
    self.darkTheme: bool = True
    self.style = ttk.Style()
    self.InitThemes()
    self.SetDarkTheme(self.darkTheme)
    self.bind("<F11>", self.ToggleFullScreen)
    self.protocol("WM_DELETE_WINDOW", self.onClose)

  def InitThemes(self):
    self.style.tk.call("source", "ForestTheme\\forest-dark.tcl")
    self.style.tk.call("source", "ForestTheme\\forest-light.tcl")
  def SetDarkTheme(self, cond):
    """ themeName: [dark, light] """
    if cond:
      themeName = 'dark'
    else:
      themeName = 'light'
    filePath = TFileManager(f"ForestTheme\\forest-{themeName}.tcl")
    self.style.theme_use( f"forest-{themeName}")

  def ToggleTheme(self):
    if self.darkTheme:
      self.darkTheme = False
    else:
      self.darkTheme = True 
      
    self.SetDarkTheme(self.darkTheme)
    
  def CenterWindow(self):
    self.update_idletasks()
    width = self.winfo_width()
    height = self.winfo_height()
    x_offset = (self.winfo_screenwidth() - width) // 2
    y_offset = (self.winfo_screenheight() - height) // 2
    self.geometry(f"{width}x{height}+{x_offset}+{y_offset}")

  def Quit(self):
    self.onClose()
  
  def ToggleFullScreen(self, *args):
    if self.attributes('-fullscreen'):
        # If it's fullscreen, disable fullscreen mode
        self.attributes('-fullscreen', False)
    else:
        # If it's not fullscreen, enable fullscreen mode
        self.attributes('-fullscreen', True)

  def OpenDocumentation(self):
    filePath = 'readme.txt'
    try:
      os.startfile(filePath)
    except FileNotFoundError:
      print(f"Error: File '{filePath}' not found.")
    except OSError as e:
      print(f"Error: {e}")

  def NeedsSave(self) -> bool:
    tabs = self.frameTabData.notebook.tabs()
    for i in range(len(tabs)):
      framedTableTemp: FramedTable = self.frameTabData.notebook.nametowidget(self.frameTabData.notebook.tabs()[i]) 
      
      if framedTableTemp.database.database.total_changes > 0:
        return True
      
    return False
  
  def onClose(self):
    if messagebox.askyesno(title='Quit', message='Are You Sure You Want To Quit !'):
      if self.NeedsSave():
        answer = messagebox.askyesnocancel(title='Closing App', message='Do you want to save changes?')
        print(answer)    
        if answer == None:
          return
        if answer:
          tabs = self.frameTabData.notebook.tabs()
          for i in range(len(tabs)):
            framedTableTemp: FramedTable = self.frameTabData.notebook.nametowidget(self.frameTabData.notebook.tabs()[i]) 
            
            if framedTableTemp.database.database.total_changes > 0:
                print("There are pending changes that need to be saved (committed).")
                framedTableTemp.SaveFile()
            else:
                print("No pending changes to be saved.")
          self.destroy()
        else:
          self.destroy()
      else:
        self.destroy()
      
      
class Interactions:
  
  @staticmethod  
  def OpenFramedTable(e):
    item_id = e.widget.identify('item', x=e.x, y=e.y)
    if item_id:
      itemName: str = e.widget.item(item_id, 'text')
      if itemName.endswith('.db'):
        path: str = e.widget.item(item_id, 'values')[0]
        path = os.path.abspath(path)
        
        #######################
          
        
        if not Interactions.CheckIsTabOpen(tabPath=path):
          framedtableData = FramedTable(frameTab=Application.Get().frameTabData, tabname=itemName.split('.')[0])
          framedtableData.InitTableData(relpath=path)
        
        # //todo continue
        #####################

  @staticmethod
  def CheckIsTabOpen(tabPath: str) -> bool:
    app = Application.Get()
    if tabPath in app.frameTabData.openPaths:
      return True
    else:
      return False
    

  
  @staticmethod
  def close_tab(event):
    tab_id = event.widget.identify(event.x, event.y)
    if tab_id and "label" in tab_id:
      indexTab = event.widget.index(f"@{event.x},{event.y}")
      print(indexTab)
      selected_tab = event.widget.tab(indexTab, 'text')
      framedTableTemp = event.widget.nametowidget(event.widget.tabs()[indexTab]) 
      pathToClose = framedTableTemp.fileManager.GetAbsolutePath()
      print(pathToClose)
      Application.Get().frameTabData.openPaths.remove(pathToClose)
      event.widget.forget(f"@{event.x},{event.y}")
      print(f"CloseTab : {selected_tab}------------------")



  