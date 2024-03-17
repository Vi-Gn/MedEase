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


from tkinter.ttk import Frame as TFrame
from tkinter.ttk import Notebook as TNotebook

from CLog import CLog
from ConfigJSON import Config



class FrameTab(TFrame):
  def __init__(self, mainFrame, width, colIndex: int, border=1, relief: str = 'groove', *args, **vargs) -> None:
    super().__init__(master=mainFrame, border=border, relief=relief, *args, **vargs)
    self.app = mainFrame.app
    self.grid_columnconfigure(index=0, weight=1)
    self.grid_columnconfigure(index=1, weight=0)
    self.grid_rowconfigure(index=0, weight=1)
    self.grid_rowconfigure(index=1, weight=0)
    self.notebook = TNotebook(self, width=width)
    self.notebook.grid(row=0, column=0, sticky="nsew")
    self.__Grid(colIndex)
    self.openPaths: list[str] = []
    
  def destroy(self):
    Config.SetOpenedPathsConfig(self.openPaths)
    Config.SaveConfig()
    super().destroy()

  def __del__(self):
    CLog.Info(f"FrameTab : has been destroyed from memory")
        
  
  def __Grid(self, colIndex: int):
    self.grid(row=0, column=colIndex, sticky="nsew", padx=5, pady=5)
    
    