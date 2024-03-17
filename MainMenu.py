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


from CLog import CLog
from Enums import EThemeState


from tkinter import Menu as TMenu
from FileManager import TFileManager


# from Application import *

class MainMenu(TMenu):
  def __init__(self, appRoot, *args, **vargs) -> None:
    super().__init__(master=appRoot, *args, **vargs)
    self.app = appRoot
    # //todo fill it one table is loaded
    self.FramedTableFile = None
    ## test start --------------------------------------------------------------------- 
    self.file_menu = TMenu(self, tearoff=0)
    self.file_menu.add_command(label="Open Directory", command= lambda : self.app.framedTableFile.OpenDirectoryFileTable())
    self.file_menu.add_command(label="New Database", command= lambda : self.app.framedTableFile.CreateNewFile())
    self.file_menu.add_command(label="Save Database", command= lambda : self.app.framedTableData.SaveFile())
    self.file_menu.add_command(label="Reload Database", command= lambda : self.app.framedTableData.LoadDataTable())
    self.file_menu.add_command(label="Reload Directory", command= lambda : self.app.framedTableFile.ReLoadDirectoryTable())
    self.file_menu.add_separator()
    self.file_menu.add_command(label="Exit", command=self.app.Quit)
    self.add_cascade(label="File", menu=self.file_menu)

    self.edit_menu = TMenu(self, tearoff=0)
    self.edit_menu.add_command(label="Add Item", command = lambda : self.app.framedTableData.AddItem())
    self.edit_menu.add_command(label="Remove Item", command = lambda : self.app.framedTableData.RemoveSelectedItems())
    self.edit_menu.add_command(label="Modify Item (Ref) Custom", command = lambda : self.app.framedTableData.ModifyChoose())
    self.edit_menu.add_command(label="Modify Item (Ref)", command = lambda : self.app.framedTableData.ModifyItemByRef())
    self.edit_menu.add_command(label="Modify Item (Label)", command = lambda : self.app.framedTableData.ModifyItemByLabel())
    self.edit_menu.add_command(label="Search Items", command = lambda : self.app.framedTableData.SearchByLabel())
    self.add_cascade(label="Edit", menu=self.edit_menu)

    self.view_menu = TMenu(self, tearoff=0)
    self.view_menu.add_command(label="Toggle FullScreen", command= lambda : self.app.ToggleFullScreen())
    self.view_menu.add_separator()
    self.view_menu.add_command(label="Default Theme", command= lambda : self.app.SetTheme(EThemeState.DEFAULT))
    self.view_menu.add_command(label="Forest Light Theme", command= lambda :  self.app.SetTheme(EThemeState.FORESTLIGHT))
    self.view_menu.add_command(label="Forest Dark Theme", command= lambda :  self.app.SetTheme(EThemeState.FORESTDARK))
    self.view_menu.add_command(label="Azure Light Theme", command= lambda :  self.app.SetTheme(EThemeState.AZURELIGHT))
    self.view_menu.add_command(label="Azure Dark Theme", command= lambda :  self.app.SetTheme(EThemeState.AZUREDARK))
    self.view_menu.add_command(label="Alt Theme", command= lambda :  self.app.SetTheme(EThemeState.ALT))
    self.view_menu.add_command(label="Clam Theme", command= lambda :  self.app.SetTheme(EThemeState.CLAM))
    self.view_menu.add_command(label="Vista Theme", command= lambda :  self.app.SetTheme(EThemeState.VISTA))
    self.view_menu.add_command(label="XP Native Theme", command= lambda :  self.app.SetTheme(EThemeState.XPNATIVE))
    self.view_menu.add_command(label="Win Native Theme", command= lambda :  self.app.SetTheme(EThemeState.WINNATIVE))
    self.view_menu.add_command(label="Classic Theme", command= lambda :  self.app.SetTheme(EThemeState.CLASSIC))
    self.add_cascade(label="View", menu=self.view_menu)

    self.help_menu = TMenu(self, tearoff=0)
    self.help_menu.add_command(label="Documentation", command= lambda : self.app.OpenDocumentation())
    self.add_cascade(label="Help", menu=self.help_menu)

    appRoot.config(menu=self)
    appRoot.CenterWindow()
    ## test ends  ---------------------------------------------------------------------
    

  def __del__(self):
    CLog.Info(f"MainMenu : has been destroyed from memory")