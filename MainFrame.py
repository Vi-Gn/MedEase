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



from tkinter.ttk import LabelFrame as TLabelFrame

from CLog import CLog

class MainFrame(TLabelFrame):
  def __init__(self, appRoot, labelText, border=2, relief: str = 'solid', *args, **vargs) -> None:
    super().__init__(master=appRoot, text=labelText, border=border, relief=relief, *args, **vargs)
    self.app = appRoot
    self.grid_columnconfigure(0, weight=0, minsize=100)
    self.grid_columnconfigure(1, minsize=700, weight=1)
    self.rowconfigure(0, weight=1)
    self.rowconfigure(1, weight=0)
    self.pack(fill="both", padx=0, pady=0, expand=1)
    
  
  def __del__(self):
    CLog.Info(f"MainFrame : has been destroyed from memory")
        