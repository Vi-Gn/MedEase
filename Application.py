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
from Enums import ETHEMESTATE
import os
from tkinter import Tk as TTk, messagebox, ttk
from typing import Self

from CLog import *

from FrameTab import FrameTab
from FramedTable import FramedTable
from MainFrame import MainFrame
from MainMenu import MainMenu

from ConfigJSON import Config, EWINSTATE

    
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
    tempState = Config.GetWinStateConfig().value
    if tempState != '':
      self.state(tempState)
    else:
      self.state(state)
    size = Config.GetSizeXYConfig()
    if size != (-1, -1):
      self.geometry(f"{size[0]}x{size[1]}")
    else:
      self.geometry(f"{width}x{height}")
    self.minsize(width=width, height=height)
    self.CenterWindow()
    self.mainmenu = MainMenu(self)
    self.mainframe = MainFrame(appRoot=self, labelText='App')
    self.frameTabFile = FrameTab(mainFrame=self.mainframe, colIndex=0, width=250)
    self.framedTableFile: FramedTable = FramedTable(frameTab=self.frameTabFile, tabname='taby', FileOrData=True)
    relPath = Config.GetRelDirectoryConfig()
    self.framedTableFile.InitTableFile(relpath=relPath,show='tree headings')
    self.frameTabData = FrameTab(mainFrame=self.mainframe, colIndex=1, width=100)
    self.framedTableData: FramedTable
    self.Theme: ETHEMESTATE = Config.GetThemeConfig()
    self.style = ttk.Style()
    self.InitThemes()
    self.SetTheme(self.Theme)
    self.bind("<F11>", self.ToggleFullScreen)
    self.bind("<F7>", self.PreviousTheme)
    self.bind("<F8>", self.NextTheme)
    self.protocol("WM_DELETE_WINDOW", self.onClose)
    self.INTERACTION = Interactions()

  def destroy(self):    
    Config.SetThemeConfig(self.Theme)
    Config.SetWinStateConfig(EWINSTATE(self.wm_state()))
    width: int = self.winfo_width()
    height: int = self.winfo_height()
    Config.SetSizeXYConfig(sizeXY=(width, height))
    Config.SaveConfig()
    CLog.Trace('Main Application Destroyed')
    del self.mainmenu
    del self.mainframe
    del self.framedTableData
    del self.framedTableFile
    del self.frameTabFile
    del self.frameTabData
    super().destroy()
    
    
  def InitThemes(self):
    self.style.tk.call("source", "Themes\\ForestTheme\\forest-dark.tcl")
    self.style.tk.call("source", "Themes\\ForestTheme\\forest-light.tcl")
    self.style.tk.call("source", "Themes/AzureTheme/azure.tcl")
    
  def SetTheme(self, eThemeState: ETHEMESTATE):
    """ themeName: [EThemeState.DEFAULT,  EThemeState.LIGHT,  EThemeState.DARK] """
    self.Theme = eThemeState
    match (eThemeState):
      
      case (ETHEMESTATE.DEFAULT):
        self.style.theme_use( f"default")
        
      case (ETHEMESTATE.FORESTLIGHT):
        # Source : https://github.com/rdbende/Forest-ttk-theme
        self.style.theme_use( f"forest-light")
        
      case (ETHEMESTATE.FORESTDARK):
        # Source : https://github.com/rdbende/Forest-ttk-theme
        self.style.theme_use( f"forest-dark")
      
      case (ETHEMESTATE.AZURELIGHT):
        # Source : https://github.com/rdbende/Azure-ttk-theme
        self.style.theme_use("azure-light")
        
      case (ETHEMESTATE.AZUREDARK):
        # Source : https://github.com/rdbende/Azure-ttk-theme
        self.style.theme_use("azure-dark")
      
      case (ETHEMESTATE.ALT):
        self.style.theme_use( f"alt")
        
      case (ETHEMESTATE.CLAM):
        self.style.theme_use( f"clam")
        
      case (ETHEMESTATE.VISTA):
        self.style.theme_use( f"vista")
        
      case (ETHEMESTATE.XPNATIVE):
        self.style.theme_use( f"xpnative")
        
      case (ETHEMESTATE.WINNATIVE):
        self.style.theme_use( f"winnative")
        
      case (ETHEMESTATE.CLASSIC):
        self.style.theme_use( f"classic")
        
      case _:
        raise Exception(f"There is no theme called {eThemeState}")
      
    
    

  def NextTheme(self, *args):    
    self.Theme = ETHEMESTATE.next(self.Theme)
    self.SetTheme(self.Theme)
      

  def PreviousTheme(self, *args):    
    self.Theme = ETHEMESTATE.prev(self.Theme)
    self.SetTheme(self.Theme)
      
      
    
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
      CLog.Error(f"File '{filePath}' not found.")
    except OSError as e:
      CLog.Error(f"{e}")

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
        if answer == None:
          CLog.Info(f"Close Event Canceled")    
          return
        if answer:
          tabs = self.frameTabData.notebook.tabs()
          for tab in tabs:
            framedTableTemp: FramedTable = self.frameTabData.notebook.nametowidget(tab) 
            
            if framedTableTemp.database.database.total_changes > 0:
                CLog.Warn("There are pending changes that need to be saved (committed).")
                framedTableTemp.SaveFile()
            else:
                CLog.Info("No pending changes to be saved.")
            framedTableTemp.destroy()
            
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
          framedtableData = FramedTable(frameTab=Application.Get().frameTabData, tabname=itemName.split('.')[0], FileOrData=False)
          framedtableData.InitTableData(relpath=path)
        
        # //todo continue
        #####################

  @staticmethod
  def CheckIsTabOpen(tabPath: str) -> bool:
    app = Application.Get()
    CLog.Trace(f"Tab To Check For Is Open Is : {tabPath}, \n\t\t\t\t From {app.frameTabData.openPaths} Tabs")
    if tabPath in app.frameTabData.openPaths:
      return True
    else:
      return False
    

  
  @staticmethod
  def close_tab(event):
    tab_id = event.widget.identify(event.x, event.y)
    if tab_id and "label" in tab_id:
      indexTab = event.widget.index(f"@{event.x},{event.y}")
      
      selected_tab = event.widget.tab(indexTab, 'text')
      
      
      framedTableTemp = event.widget.nametowidget(event.widget.tabs()[indexTab]) 
      pathToClose = framedTableTemp.fileManager.GetAbsolutePath()
      Application.Get().frameTabData.openPaths.remove(pathToClose)
      event.widget.forget(f"@{event.x},{event.y}")
      framedTableTemp.destroy()
      del framedTableTemp.database
      CLog.Info(f"CloseTab's name : {selected_tab}")
      CLog.Info(f"CloseTab's path : {pathToClose}")



  