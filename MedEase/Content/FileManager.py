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
from SubWindow import SubWindow


import os
from tkinter import *
from tkinter import ttk

# def newFileAction(name):
#   fName = name.get()
#   f = open(self.workdir + '/' + fName+'.db','w')
#   f.close()
#   OpenDirLoaded('', False)
        

class TFileManager:
  def __init__(self, relPathWorkdir) -> None:
    self.__workdirAbs = os.path.abspath(relPathWorkdir)


  def SetPathWorkdir(self, absPathWorkdir):
    self.__workdirAbs = os.path.abspath(absPathWorkdir)
    CLog.Trace(f"Setup new path in a file manager {self.__workdirAbs}")

  def GetFileName(self):
    return os.path.basename(self.__workdirAbs)
  
  def GetRelativePath(self):
    return os.path.relpath(self.__workdirAbs)
  
  def GetAbsolutePath(self):
    return os.path.abspath(self.__workdirAbs)
  
  def CreateFile(self, filename):
    fullPath:str = os.path.join(self.GetAbsolutePath(), filename)
    if fullPath.split('.')[-1] != 'db':
      fullPath += '.db'
    f = open(fullPath, 'w')
    f.close()
    CLog.Trace(f"Created a new database in {fullPath}")
    

  # def CreateFileAsk(self, filename):
  #   fullPath = os.path.join(self.GetAbsolutePath(), filename)
  #   f = open(fullPath, 'w')
  #   f.close()
  #   CLog.Trace(f"Created a new database in {fullPath}")
    

    
  # @staticmethod
  # def OpenDirectory(root):
  #   top = SubWindow(master=root, title='Add')
  #   ttk.Label(top, text='Enter the file name').pack(fill="x", expand=True, ipadx=35, padx=15, pady=5)
  #   name = ttk.Entry(top)
  #   name.pack(fill="x", expand=True, ipadx=35, padx=15, pady=5)
  #   btn = ttk.Button(top,text='reload', command=lambda: [ print('---------------------Not Implemented OpenDirectory()---------------'), newFileAction(name), top.destroy()], padding=5)
  #   btn.pack(fill="x", expand=True, ipadx=35, padx=15, pady=5)
    

