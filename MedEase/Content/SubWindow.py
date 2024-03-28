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




from tkinter import Toplevel as TTopLevel

from CLog import CLog




class SubWindow(TTopLevel):
  def __init__(self, master, title, icon: str='Icon/meds.ico', state: str ='normal', *args, **vargs) -> None:
    '''state: [normal, icon, iconic (see wm_iconwindow), withdrawn, or zoomed (Windows only)]'''
    super().__init__(master, *args, **vargs)
    self.title(title)
    self.iconbitmap(icon)
    self.state(state)
    self.CenterWindow()
    self.Title = title
    CLog.Trace(f"SubWindow : {self.wm_title()} has been created")
    
  def __del__(self):
    CLog.Info(f"SubWindow : {self.Title} has been destroyed from memory")
        
  def destroy(self):
    self.Title = self.wm_title()
    super().destroy()
        
    
  def CenterWindow(self):
    self.update_idletasks()
    width = self.winfo_width()
    height = self.winfo_height()
    x_offset = (self.winfo_screenwidth() - width) // 2
    y_offset = (self.winfo_screenheight() - height) // 2
    self.geometry(f"{width}x{height}+{x_offset}+{y_offset}")
  