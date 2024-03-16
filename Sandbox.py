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
# from Application import Interactions





def main():
  app: Application = Application()
  app.framedTableFile.table.bind('<Double-1>', Interactions.OpenFramedTable)
  
  app.frameTabData.notebook.bind("<Button-2>", Interactions.close_tab)


  # //todo this should be called after double clicking a db from file table
  framedTableData = FramedTable(frameTab=Application.Get().frameTabData, tabname='Demo')
  framedTableData.InitTableData(relpath='databases\\DemoData.db')
  app.mainloop()









if __name__ == '__main__':
  main()
