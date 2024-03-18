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


 
 

from Application import *

from CLog import *


from ThankApp import *


  
  
  
def main():
  Config.LoadConfig()
  
  bigThanks = ThanksApp()
  bigThanks.Run()
  
  
  # launch the application
  app: Application = Application()
  
  # // this will open the double clicked database from file structure table
  app.framedTableFile.table.bind('<Double-1>', Interactions.OpenFramedTable)
    
  # // todo needs to close only after being saved means not dirty
  # // this will close the tab, clicked with middle mouse  
  app.frameTabData.notebook.bind("<Button-2>", Interactions.close_tab)


  # // Loads Databases from config that has been recently opened
  for path in Config.GetOpenedAbsPathsConfig():
    absPath = os.path.abspath(path)
    fileName = os.path.basename(path)
    framedTableData = FramedTable(frameTab=Application.Get().frameTabData, tabname=fileName, FileOrData=False)
    framedTableData.InitTableData(absPath=absPath)
    
    
  app.Run()
  









if __name__ == '__main__':
  main()
