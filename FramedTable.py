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
from tkinter import filedialog, messagebox
from tkinter import ttk
import tkinter
from tkinter.ttk import Frame as TFrame
from tkinter.ttk import Notebook as TNotebook
from tkinter.ttk import Treeview as TTreeview
from tkinter.ttk import Scrollbar as TScrollbar
from typing import Literal


from FileManager import TFileManager
from SubWindow import SubWindow
from RDB import *
from CLog import *


class FramedTable(TFrame):
  '''with scroll'''
  def __init__(self, frameTab, FileOrData:bool, tabname:str = 'Tab', border=1, relief='groove', *args, **vargs) -> None:
    self.app = frameTab.app
    self.notebook: TNotebook = frameTab.notebook
    
    super().__init__(master=self.notebook, border=border, relief=relief, *args, **vargs)
    self.fileManager: TFileManager = None
    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(1, weight=0)
    self.grid_rowconfigure(0, weight=1)
    self.grid_rowconfigure(1, weight=0)
    self.notebook.add(child=self, text=tabname, sticky="nsew")
    self.notebook.bind("<<NotebookTabChanged>>", self.onTabChanged)
    self.columns = ''
    self.frameTab = frameTab
    self.IsActive: bool = True
    self.database: RDB
    self.FileOrData: bool = FileOrData
   
  def destroy(self):
    super().destroy()
    
    
  def __del__(self):
    CLog.Info(f"FramedTable : has been destroyed from memory")
        
  
  def onTabChanged(self, e):
    FramedTableDataTemp = e.widget.nametowidget(e.widget.select()) 
    self.app.framedTableData = FramedTableDataTemp
    self.IsActive = FramedTableDataTemp == self
    
  def HeadingTableClick(self, nameCol):
    self.LoadDataTableSortedBy(nameCol)
    
  
  def InitTableData(self, relpath: str = '', show = 'headings', selectmode = "extended"):
    self.DataSortOrder: list[str | bool] = ['ref', True]
    self.fileManager = TFileManager(relpath)
    path = self.fileManager.GetAbsolutePath()
    
    self.frameTab.openPaths.append(path)
    self.database = RDB(path)
    self.database.createTable()
    
    if relpath == '':
      raise Exception("this is not a valid database")
    
    self.columns = self.database.getColumnNames()
      
    if len(self.columns) >= 1:      
      self.table = TTreeview(master=self, columns=self.columns, selectmode=selectmode, show=show)
      self.table.bind("<Delete>", self.RemoveSelectedItems)
      self.table.bind("<Double-1>", self.__DataTableSelect)
      self.table.bind("<Button-1>", self.__ClearSelection)
      self.table['columns'] = self.columns
      for column in self.columns:
        currentColumn = column.lower()
        currentColumnText = currentColumn.capitalize()
        anchor: Literal['center', 'w'] = 'center' 
        minwidth=80
        stretch=False
        
        if currentColumn in ('ref', 'id', 'reference', 'references'):
          ...
                      
        elif currentColumn in ('name', 'nom', 'prenom', 'label', 'libelle', 'labelle', 'label', 'lastname', 'firstname'):
          anchor = 'w' 
          minwidth=150
          stretch=True
    
        elif currentColumn in ('desc', 'description', 'info'):
          anchor = 'w' 
          minwidth=250
          stretch=True
    
        elif currentColumn in ('price', 'quantity', 'quantite', 'prix'):
          minwidth=100

        else:
            raise Exception('lookout for unhandled column')
          
        self.table.heading(column=column, text=currentColumnText, anchor=anchor, command=lambda colText= column : self.HeadingTableClick(colText))
        self.table.column(column=column, anchor=anchor, minwidth=minwidth, width=minwidth, stretch=stretch)
        # self.table.tag_bind(column, "<Button-1>", self.HeadingTableClick)
          
    else:
      raise Exception('how is that?!!!')

    self.LoadDataTable()

    self.table.grid(row=0, column=0, sticky='nsew')
    self.InitScrollbars()
    
    return self.table  
    
  def LoadDataTableSortedBy(self, colText):
    if self.DataSortOrder[0] == colText:
      self.DataSortOrder[1] = not self.DataSortOrder[1]
    else:
      self.DataSortOrder = [colText, True]
    for item in self.table.get_children():
      self.table.delete(item)
    for row in self.database.getDataSortedBy(colTextToSort=self.DataSortOrder[0], orderSort=self.DataSortOrder[1]):
      self.Insert(values=row)
    
  def __ClearSelection(self, e):
    widget = e.widget
    widget.selection_remove(widget.selection())

  def ModifyQuantity(self):
    ...
    
  def __DataTableSelect(self, e): 
    item = e.widget.identify_row(e.y)  # Get the item (row) at the y-coordinate of the event
    column = e.widget.identify_column(e.x)  # Get the column at the x-coordinate of the event
    column = int(column[1:]) - 1
    
    selectedItems = e.widget.selection()
    if selectedItems:
      itemDataValues = e.widget.item(selectedItems[-1], 'values')
      ref = itemDataValues[0]
      selectedValue =  itemDataValues[column]
      colName = e.widget.heading(column)["text"]
      
      
      top = SubWindow(self.app, title=f'Modify {colName}', width=500, height=200)
      UpperFrame = TFrame(top)
      UpperFrame.pack(fill='both', expand=1, anchor='center')
      for i in range(3):
        UpperFrame.grid_columnconfigure(i, weight=1, minsize=20)
      
      UpperFrame.grid_rowconfigure(0, minsize=20)
      lbl1 = ttk.Label(UpperFrame, text=f"Enter {colName}")
      lbl1.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
      # lbl1.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
      Label = ttk.Entry(UpperFrame, width=35)
      Label.grid(row=2, column=1, sticky='nsew', padx=5, pady=5)
      
      
      LowerFrame = TFrame(top)
      for i in range(4):
        LowerFrame.grid_columnconfigure(i, weight=1, minsize=20)
      LowerFrame.pack(fill='both', expand=1, anchor='center')
      btnSet = ttk.Button(LowerFrame,text='Set', command=lambda ref=ref, col=colName, ltop=top, lLabel=Label: self.__ModifyColByRefLoadAndDestroy(ref=ref, col=col, content=lLabel.get(),topL=ltop))
      btnSet.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
      btnCancel = ttk.Button(LowerFrame,text='Cancel', command=lambda: top.destroy())
      btnCancel.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)
      
      
  def __ModifyColByRefLoadAndDestroy(self, ref, col, content, topL):
    if self.database.modifyColByRef(ref=ref, col=col, content=content) == -1:
      messagebox.showwarning(title='Label exists already', message='Re-Enter a non indentical label')
      topL.focus()
    else:
      self.LoadDataTable()
      topL.destroy()
    
  ########################################################################################
  
  def LoadDataTable(self):
    for item in self.table.get_children():
      self.table.delete(item)
    for row in self.database.getData():
      self.Insert(values=row)
      
      

  def InitTableFile(self, relpath: str = '-1', show = 'headings', title: str = "File", selectmode = "browse") -> TTreeview:
    ''' selectmode: ['extended', "browse", 'none']
        show: ["tree", "headings", "tree headings", ""]
        '''
    self.FileSortOrder: bool = True
    if relpath == '-1':
      self.fileManager = TFileManager('..\\databases')
      relpath = filedialog.askdirectory(initialdir=self.fileManager.GetAbsolutePath())
      
      
    self.fileManager = TFileManager(relpath)
      
    self.columns = "#0"
    self.table = TTreeview(master=self, selectmode=selectmode, show=show)
    self.table.bind("<Delete>", self.RemoveSelectedItems)
    
    
    self.table.heading(column='#0', text=title, anchor="center", command=lambda : self.ToggleSortFile())
    self.table.column(column='#0', anchor="w")

    ################################################
    # //todo this 
    self.LoadDirectoryTable(relpath)
    ################################################
    
    self.table.grid(row=0, column=0, sticky='nsew')
    self.InitScrollbars()
    
    return self.table
  
    

  def LoadDirectoryTable(self, rel_directory, sortMode:bool = True):
    self.fileManager.SetPathWorkdir(rel_directory)
    tempTitle: str = self.app.Title
    self.app.title( tempTitle + '          ' +  self.fileManager.GetAbsolutePath())
    
    absoluteDirectory = self.fileManager.GetAbsolutePath()
    baseName = self.fileManager.GetFileName()
    self.insertFiles(absoluteDirectory, baseName, sortMode)
    
  def ToggleSortFile(self):
    self.FileSortOrder = not self.FileSortOrder
    self.ReLoadDirectoryTable(sortMode=self.FileSortOrder)
    
  def ReLoadDirectoryTable(self, sortMode:bool = True):
    '''sortMode: [True -> Sort ascending, False -> descending order]'''
    for item in self.table.get_children():
      self.table.delete(item)
    absoluteDirectory = self.fileManager.GetAbsolutePath()
    baseName = self.fileManager.GetFileName()
    self.insertFiles(absoluteDirectory, baseName, sortMode)

  def insertFiles(self, directory, baseName, sortMode:bool):
    '''sortMode: [True -> Sort ascending, False -> descending order]'''
    rootNode = self.table.insert("", "end", text=baseName, open=True)
    self.insertTree(rootNode, directory, sortMode)

  def insertTree(self, parent_node, directory, sortMode:bool):
    '''sortMode: [True -> Sort ascending, False -> descending order]'''
    if os.path.isdir(directory):
      for item in sorted(os.listdir(directory), reverse=sortMode):
        itemPath = os.path.join(directory, item)
        
        itemName = os.path.basename(itemPath)
        if os.path.isdir(itemPath):
          node = self.table.insert(parent_node, "end", text=itemName, open=True)
          self.insertTree(node, itemPath, sortMode)  # Recursively insert subdirectories
        else:
          temp = itemPath.replace('\\', '/')
          self.table.insert(parent_node, "end", text=itemName, values=temp)



########################################################################################
  
    
  def SaveFile(self):
    self.database.save()

    
    
  def __addItemAction(self, Label, Description, Quantity, Price):
    
    lbl = Label.get().capitalize()
    Label.delete(0,'end')
    
    dsc: str = Description.get().capitalize()
    Description.delete(0,'end')
    
    qtt = Quantity.get()
    Quantity.delete(0,'end')
    
    prc = Price.get()
    Price.delete(0,'end')
    labelNoFound = not self.database.existsLabel(lbl)
    CLog.Trace(f"{labelNoFound = }")
    if labelNoFound == True:
        DataAdder().addMenuUI(self.database ,lbl, dsc, qtt, prc, '')
        # //todo 
        # self.database.save() 
        self.LoadDataTable()
    else:
        self.checkWhatToChange(lbl, dsc, qtt, prc, '')
    
      
  def checkWhatToChange(self , lbl, dsc, qtt, prc, answer:str =''):
    '''asks if should change attributes'''
    if answer=='':
      top = SubWindow(self.app, title='Choose what to change', width=700, height=200)
      UpperFrame = TFrame(top)
      UpperFrame.pack(fill='both', expand=1, anchor='center')
      for i in range(6):
        UpperFrame.grid_columnconfigure(i, weight=1, minsize=20)
      for i in range(3):
        UpperFrame.grid_rowconfigure(i, minsize=50)
    
      
      btnQ = ttk.Button(UpperFrame,text='Add Quantity', command=lambda : [self.checkWhatToChange(lbl, dsc, qtt, prc,'q'), top.destroy()])
      btnQ.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
      btnP = ttk.Button(UpperFrame,text='Override Price', command=lambda: [self.checkWhatToChange(lbl, dsc, qtt, prc,'p'), top.destroy()])
      btnP.grid(row=1, column=2, sticky='nsew', padx=5, pady=5)
      btnQP = ttk.Button(UpperFrame,text='Add Quatity & Override Price', command=lambda: [self.checkWhatToChange(lbl, dsc, qtt, prc,'qp'), top.destroy()])
      btnQP.grid(row=1, column=3, sticky='nsew', padx=5, pady=5)
      
      btnCancel = ttk.Button(UpperFrame,text='Cancel', command=lambda: top.destroy())
      btnCancel.grid(row=1, column=4, sticky='nsew', padx=5, pady=5)
    else:
      DataAdder().addMenuUI(self.database ,lbl, dsc, qtt, prc, answer)
        # //todo 
        # self.database.save() 
      self.LoadDataTable()
        
  def AddItem(self):
      top = SubWindow(self.app, title='Add Item', width=750, height=200)
      UpperFrame = TFrame(top)
      UpperFrame.pack(fill='both', expand=1, anchor='center')
      for i in range(6):
        UpperFrame.grid_columnconfigure(i, weight=1, minsize=20)
      
      UpperFrame.grid_rowconfigure(0, minsize=20)
      lbl1 = ttk.Label(UpperFrame, text="Enter Label")
      lbl1.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
      # lbl1.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
      Label = ttk.Entry(UpperFrame)
      Label.grid(row=2, column=1, sticky='nsew', padx=5, pady=5)
      # Label.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
      lbl2 = ttk.Label(UpperFrame, text="Enter Description")
      lbl2.grid(row=1, column=2, sticky='nsew', padx=5, pady=5)
      # lbl2.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
      Description = ttk.Entry(UpperFrame)
      Description.grid(row=2, column=2, sticky='nsew', padx=5, pady=5)
      # Description.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
      lbl3 = ttk.Label(UpperFrame, text="Enter Quantity")
      lbl3.grid(row=1, column=3, sticky='nsew', padx=5, pady=5)
      # lbl3.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)
      Quantity = ttk.Entry(UpperFrame)
      Quantity.grid(row=2, column=3, sticky='nsew', padx=5, pady=5)
      # Quantity.grid(row=1, column=2, sticky='nsew', padx=5, pady=5)
      lbl4 = ttk.Label(UpperFrame, text="Enter Price")
      lbl4.grid(row=1, column=4, sticky='nsew', padx=5, pady=5)
      # lbl4.grid(row=0, column=3, sticky='nsew', padx=5, pady=5)
      Price = ttk.Entry(UpperFrame)
      Price.grid(row=2, column=4, sticky='nsew', padx=5, pady=5)
      # Price.grid(row=1, column=3, sticky='nsew', padx=5, pady=5)
      
      LowerFrame = TFrame(top)
      for i in range(4):
        LowerFrame.grid_columnconfigure(i, weight=1, minsize=20)
      LowerFrame.pack(fill='both', expand=1, anchor='center')
      btnAdd = ttk.Button(LowerFrame,text='Add', command=lambda: self.__addItemAction(Label, Description, Quantity, Price))
      btnAdd.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
      btnCancel = ttk.Button(LowerFrame,text='Cancel', command=lambda: top.destroy())
      btnCancel.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)
  
         
  def RemoveSelectedItems(self, *args):
    if self.FileOrData:
      CLog.Warn(f"This is an experimental function should not be used in production | File : {__file__}, Function : {self.RemoveSelectedItems.__name__}")
      confirm = messagebox.askyesno(title='Danger', message='Are You Sure You Want To Delete File?')
      selectedItems =  self.table.item(self.table.selection())
      path = selectedItems["values"][0]
      path = os.path.abspath(path)
      tabname = os.path.basename(path) 
      if confirm:
        if self.app.INTERACTION.CheckIsTabOpen(path):
          messagebox.showerror(title="Database already opened!", message=f"Please close {tabname}'s tab first!")
          CLog.Error(f"Database already opened! | Please close {tabname}'s tab first!")          
          return
        if path != '':
          try:
            os.remove(path)
          except PermissionError:
            messagebox.showerror(title="Can't Remove Database", message="Please close it first!")
            CLog.Error(f"Can't Remove Database | {selectedItems['values'][0]}")
          else:
            CLog.Info(f"Database's Remove Success | {selectedItems['values'][0]}")
          self.ReLoadDirectoryTable()
        elif path == '':
          CLog.Warn(f"Can't Remove Main Directory!")
        return
      return
    
    if self.IsActive:
      selectedItems = self.table.selection()  # Get the IDs of selected items
      if selectedItems:
        confirm = messagebox.askyesno(title='Delete Selected Items', message='Are You Sure?')
        if confirm:
          for item in selectedItems:
            id: int = self.table.item(item, "value")[0]  # Get the value of each selected item
            self.database.removeByRef(id) 
          self.LoadDataTable()
    else:
      CLog.Error('Trying to erase items from unactive tab ')
  
  def CreateNewFile(self):
    # top = tk.Toplevel(self.app)
    top = SubWindow(master=self.app, title='Create Database Window')
    UpperFrame = TFrame(top)
    UpperFrame.pack(fill='both', expand=1, anchor='center')
    for i in range(3):
      UpperFrame.grid_columnconfigure(i, weight=1, minsize=20)
    for i in range(6):
      UpperFrame.grid_rowconfigure(i, minsize=20)
    
    ttk.Label(UpperFrame, text='Enter the file name').grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
    
    name = ttk.Entry(UpperFrame)
    name.grid(row=2, column=1, sticky='nsew', padx=5, pady=5)
    # inp = name.
    
    btn = ttk.Button(UpperFrame,text='reload', command=lambda: [ self.fileManager.CreateFile(name.get()), self.ReLoadDirectoryTable(), top.destroy()], padding=5)
    btn.grid(row=4, column=1, sticky='nsew', padx=5, pady=5)
    
    
  def ModifyChoose(self):
    top = SubWindow(self.app, title='Modify Items by Label', width=540, height=217)
    top.minsize(width=536, height=210)
    UpperFrame = TFrame(top)
    UpperFrame.pack(fill='both', expand=1, anchor='center')
    for i in range(3):
      UpperFrame.grid_columnconfigure(i, weight=1, minsize=20)
    for i in range(3):
      UpperFrame.grid_rowconfigure(i, minsize=30)
    
  #################################################
    selectedValueRadio = tkinter.StringVar()  
    LabelText = tkinter.StringVar() 
    
    
    
    MiddleFrame = TFrame(top)
    MiddleFrame.pack(fill='both', expand=1, anchor='center')
    for i in range(3):
      MiddleFrame.grid_columnconfigure(i, weight=0, minsize=0)
      
    MiddleFrame.grid_columnconfigure(0, weight=1, minsize=10)
    # MiddleFrame.grid_columnconfigure(1, weight=0, minsize=100)
    # MiddleFrame.grid_columnconfigure(2, weight=0, minsize=100)
    MiddleFrame.grid_columnconfigure(3, weight=1, minsize=10)
    
    
    
    radioRef = ttk.Radiobutton(MiddleFrame, text="ByRef", value="ref", variable=selectedValueRadio, command=lambda : [ LabelText.set('Choose item By Ref') , selectedValueRadio.set("ref"), top.title(f'Modify Items by {selectedValueRadio.get().capitalize()}') ] ) 
    radioRef.grid(row=0, column=1, sticky='nsew', padx=12, pady=5)
    
    radioLabel = ttk.Radiobutton(MiddleFrame, text="ByLabel", value="label", variable=selectedValueRadio, command=lambda : [ LabelText.set('Choose item By Label') , selectedValueRadio.set("label"), top.title(f'Modify Items by {selectedValueRadio.get().capitalize()}') ] ) 
    radioLabel.grid(row=0, column=2, sticky='nsew', padx=12, pady=5)
    
    
    selectedValueRadio.set("label")
  #################################################
      
      
    lbl1 = ttk.Label(UpperFrame, textvariable=LabelText)
    lbl1.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
    Label = ttk.Entry(UpperFrame, width=120)
    Label.grid(row=2, column=1, sticky='nsew', padx=5, ipady=5)
    # Label.bind("<KeyRelease>", lambda e : self.__SearchColumnCommand(content=e.widget.get(), colName=selectedValueRadio.get()))
    
    
    
    LabelText.set('Choose item By Label')
    LowerFrame = TFrame(top)
    LowerFrame.pack(fill='both', expand=1, anchor='center')
    for i in range(4):
      LowerFrame.grid_columnconfigure(i, weight=1, minsize=20)
    for i in range(2):
      LowerFrame.grid_rowconfigure(i, minsize=30)
    btnSet = ttk.Button(LowerFrame,text='Set', command=lambda:  self.__OpenModifyMenu(value=Label.get(), colName=selectedValueRadio.get() ,topL=top) )
    btnSet.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
    btnCancel = ttk.Button(LowerFrame,text='Cancel', command=lambda: top.destroy())
    btnCancel.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)
    
      
      
  def __OpenModifyMenu(self, value, colName: str, topL: SubWindow): 
    title = ''
    match (colName):
      case ('ref'):
        if not self.database.existsRef(value):
          CLog.Error(f'Ref : {value} is not available')
          messagebox.showwarning(title="Can't Modify !", message=f"Ref : {value} is not available")
          topL.focus()
          
          return
        title = f'Modify for Ref : {value}'
        
      case ('label'):
        if not self.database.existsLabel(value):
          CLog.Error(f'Label : {value} is not available')
          messagebox.showwarning(title="Can't Modify !", message=f"Label : {value} is not available")
          topL.focus()
          return
        title = f'Modify for Label : {value}'
      case _:
        raise Exception('__OpenModifyMenu() only supports Ref and Label as colName')
      
    if topL:
      topL.destroy()
      
    top = SubWindow(self.app, title=title, width=540, height=217)
    top.minsize(width=536, height=255)
    UpperFrame = TFrame(top)
    UpperFrame.pack(fill='both', expand=1, anchor='center')
    for i in range(3):
      UpperFrame.grid_columnconfigure(i, weight=1, minsize=20)
    for i in range(3):
      UpperFrame.grid_rowconfigure(i, minsize=30)
    
  #################################################
  
    selectedValueRadio = tkinter.StringVar(self.app)  
    LabelText = tkinter.StringVar() 
    
    MiddleFrame = TFrame(top)
    MiddleFrame.pack(fill='both', expand=1, anchor='center')
    for i in range(4):
      MiddleFrame.grid_columnconfigure(i, weight=0, minsize=0)
      
    MiddleFrame.grid_columnconfigure(0, weight=1, minsize=10)
    # MiddleFrame.grid_columnconfigure(1, weight=0, minsize=100)
    # MiddleFrame.grid_columnconfigure(2, weight=0, minsize=100)
    MiddleFrame.grid_columnconfigure(4, weight=1, minsize=10)
    
    
    radioLabelDesc = ttk.Radiobutton(MiddleFrame, text="Description", value="description", variable=selectedValueRadio, command=lambda : [ LabelText.set('Enter The New Description') , selectedValueRadio.set("description") ] )
    radioLabelDesc.grid(row=0, column=1, sticky='nsew', padx=2,)
    
    radioLabelQty = ttk.Radiobutton(MiddleFrame, text="Quantity", value="quantity", variable=selectedValueRadio, command=lambda : [ LabelText.set('Enter The New Quantity') , selectedValueRadio.set("quantity") ] )
    radioLabelQty.grid(row=0, column=2, sticky='nsew', padx=2,)
    
    radioLabelPrice = ttk.Radiobutton(MiddleFrame, text="Price", value="price", variable=selectedValueRadio, command=lambda : [ LabelText.set('Enter The New Price') , selectedValueRadio.set("price") ] )
    radioLabelPrice.grid(row=0, column=3, sticky='nsew', padx=2,)
    
    selectedValueRadio.set("description")
    
  #################################################
      
    # done it here instead of above cuz we need that LabelText Variable to be Initialized First
    lbl1 = ttk.Label(UpperFrame, textvariable=LabelText)
    lbl1.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
    Label = ttk.Entry(UpperFrame, width=120)
    Label.grid(row=2, column=1, sticky='nsew', padx=5, ipady=5)
    
  #################################################
  
    LabelText.set('Enter The New Description')
    LowerFrame = TFrame(top)
    LowerFrame.pack(fill='both', expand=1, anchor='center')
    for i in range(4):
      LowerFrame.grid_columnconfigure(i, weight=1, minsize=20)
    for i in range(2):
      LowerFrame.grid_rowconfigure(i, minsize=30)
    btnSet = ttk.Button(LowerFrame,text='Set', command=lambda:  self.__ModifyColAutomaticallyLoadAndDestroy(labelOrRef=value, colName=colName, col=selectedValueRadio.get(), content=Label.get(), topL=top))
    btnSet.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
    btnCancel = ttk.Button(LowerFrame,text='Cancel', command=lambda: top.destroy())
    btnCancel.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)
    
  def __ModifyColAutomaticallyLoadAndDestroy(self, labelOrRef, colName, col, content, topL):
    match (colName):
      case ('ref'):
        self.__ModifyColByRefLoadAndDestroy(ref=labelOrRef, col=col, content=content, topL=topL)
        
      case ('label'):
        self.__ModifyColByLabelLoadAndDestroy(label=labelOrRef, col=col, content=content, topL=topL)
        
      case _:
        raise Exception('__OpenModifyMenu() only supports Ref and Label as colName')
      
      
      
  def __ModifyColByLabelLoadAndDestroy(self, label, col, content, topL):
    if self.database.modifyColByLabel(label=label, col=col, content=content) == -1:
      messagebox.showwarning(title='Label exists already', message='Re-Enter a non indentical label')
      topL.focus()
    else:
      self.LoadDataTable()
      topL.destroy()
      
      
      
  def SearchByLabel(self):
    top = SubWindow(self.app, title='Search Items by Label', width=700, height=255)
    top.minsize(width=536, height=255)
    UpperFrame = TFrame(top)
    UpperFrame.pack(fill='both', expand=1, anchor='center')
    for i in range(3):
      UpperFrame.grid_columnconfigure(i, weight=1, minsize=20)
    for i in range(3):
      UpperFrame.grid_rowconfigure(i, minsize=30)
    
  #################################################
  
    selectedValueRadio = tkinter.StringVar()  
    LabelText = tkinter.StringVar() 
    
    MiddleFrame = TFrame(top)
    MiddleFrame.pack(fill='both', expand=1, anchor='center')
    for i in range(7):
      MiddleFrame.grid_columnconfigure(i, weight=0, minsize=0)
      
    MiddleFrame.grid_columnconfigure(0, weight=1, minsize=10)
    # MiddleFrame.grid_columnconfigure(1, weight=0, minsize=100)
    # MiddleFrame.grid_columnconfigure(2, weight=0, minsize=100)
    MiddleFrame.grid_columnconfigure(6, weight=1, minsize=10)
    
    radioRef = ttk.Radiobutton(MiddleFrame, text="ByRef", value="ref", variable=selectedValueRadio, command=lambda : [ LabelText.set('Search By Ref') , selectedValueRadio.set("ref") ] )
    radioRef.grid(row=0, column=1, sticky='nsew', padx=2,)
    
    radioLabel = ttk.Radiobutton(MiddleFrame, text="ByLabel", value="label", variable=selectedValueRadio, command=lambda : [ LabelText.set('Search By Label') , selectedValueRadio.set("label") ] )
    radioLabel.grid(row=0, column=2, sticky='nsew', padx=2,)
    
    radioLabelDesc = ttk.Radiobutton(MiddleFrame, text="ByDescription", value="description", variable=selectedValueRadio, command=lambda : [ LabelText.set('Search By Description') , selectedValueRadio.set("description") ] )
    radioLabelDesc.grid(row=0, column=3, sticky='nsew', padx=2,)
    
    radioLabelQty = ttk.Radiobutton(MiddleFrame, text="ByQuantity", value="quantity", variable=selectedValueRadio, command=lambda : [ LabelText.set('Search By Quantity') , selectedValueRadio.set("quantity") ] )
    radioLabelQty.grid(row=0, column=4, sticky='nsew', padx=2,)
    
    radioLabelPrice = ttk.Radiobutton(MiddleFrame, text="ByPrice", value="price", variable=selectedValueRadio, command=lambda : [ LabelText.set('Search By Price') , selectedValueRadio.set("price") ] )
    radioLabelPrice.grid(row=0, column=5, sticky='nsew', padx=2,)
    
    selectedValueRadio.set("label")
    
  #################################################
      
    # done it here instead of above cuz we need that LabelText Variable to be Initialized First
    lbl1 = ttk.Label(UpperFrame, textvariable=LabelText)
    lbl1.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
    Label = ttk.Entry(UpperFrame, width=120)
    Label.grid(row=2, column=1, sticky='nsew', padx=5, ipady=5)
    Label.bind("<KeyRelease>", lambda e : self.__SearchColumnCommand(content=e.widget.get(), colName=selectedValueRadio.get()))
    
  #################################################
  
    LabelText.set('Search By Label')
    LowerFrame = TFrame(top)
    LowerFrame.pack(fill='both', expand=1, anchor='center')
    for i in range(4):
      LowerFrame.grid_columnconfigure(i, weight=1, minsize=20)
    for i in range(2):
      LowerFrame.grid_rowconfigure(i, minsize=30)
    btnSet = ttk.Button(LowerFrame,text='Set', command=lambda: [ self.__SearchColumnCommand(content=Label.get(), colName=selectedValueRadio.get()), top.destroy() ] )
    btnSet.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
    btnCancel = ttk.Button(LowerFrame,text='Cancel', command=lambda: top.destroy())
    btnCancel.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)
      
      
  def __SearchColumnCommand(self, content: str, colName: str):    
    for item in self.table.get_children():
      self.table.delete(item)
    tempData = self.database.getColContain(content=content, colName=colName)
    if tempData:
      for row in tempData:
        self.Insert(values=row)
    
    
  def __ModifyRefCommand(self, ref ,label, description, quantity, price):
    self.database.modifyAllByRef( ref=ref ,label=label.get(), description=description.get(), quantity=quantity.get(), price=price.get()) 
    self.LoadDataTable()
    
    
  def ModifyByRefAction(self, ref, topLevel):
    if not self.database.existsRef(ref):
      CLog.Error(f'Ref : {ref} is not available')
      messagebox.showwarning(title="Can't Modify !", message=f"Ref : {ref} is not available")
      topLevel.focus()
      return
    
    if topLevel:
      topLevel.destroy()
    top = SubWindow(self.app, title='Modify Item', width=700, height=200)
    UpperFrame = TFrame(top)
    UpperFrame.pack(fill='both', expand=1, anchor='center')
    for i in range(6):
      UpperFrame.grid_columnconfigure(i, weight=1, minsize=20)
    for i in range(3):
      UpperFrame.grid_rowconfigure(i, minsize=30)
    
      
    lbl1 = ttk.Label(UpperFrame, text="Enter Label")
    lbl1.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
    
    Label = ttk.Entry(UpperFrame)
    Label.grid(row=2, column=1, sticky='nsew', padx=5, pady=5)
    
    lbl2 = ttk.Label(UpperFrame, text="Enter Description")
    lbl2.grid(row=1, column=2, sticky='nsew', padx=5, pady=5)
    
    Description = ttk.Entry(UpperFrame)
    Description.grid(row=2, column=2, sticky='nsew', padx=5, pady=5)
    
    lbl3 = ttk.Label(UpperFrame, text="Enter Quantity")
    lbl3.grid(row=1, column=3, sticky='nsew', padx=5, pady=5)
    
    Quantity = ttk.Entry(UpperFrame)
    Quantity.grid(row=2, column=3, sticky='nsew', padx=5, pady=5)
    
    lbl4 = ttk.Label(UpperFrame, text="Enter Price")
    lbl4.grid(row=1, column=4, sticky='nsew', padx=5, pady=5)
    
    Price = ttk.Entry(UpperFrame)
    Price.grid(row=2, column=4, sticky='nsew', padx=5, pady=5)
    
    LowerFrame = TFrame(top)
    LowerFrame.pack(fill='both', expand=1, anchor='center')
    for i in range(4):
      LowerFrame.grid_columnconfigure(i, weight=1, minsize=20)
    for i in range(2):
      LowerFrame.grid_rowconfigure(i, minsize=30)
    btnSet = ttk.Button(LowerFrame,text='Set', 
              command=lambda: [ self.__ModifyRefCommand(ref=ref, label=Label, description=Description, quantity=Quantity, price=Price), top.destroy() ] )
    btnSet.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
    btnCancel = ttk.Button(LowerFrame,text='Cancel', command=lambda: top.destroy())
    btnCancel.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)
      
    
    
  def __ModifyLabelCommand(self, oldLabel ,label, description, quantity, price):
    self.database.modifyAllByLabel( oldLabel=oldLabel ,label=label, description=description, quantity=quantity, price=price) 
    self.LoadDataTable()
    CLog.Trace(f'Label : {oldLabel} is modified successfully by {label =}, {description =}, {quantity =}, {price =}')
    
  def ModifyByLabelAction(self, oldLabel, topLevel):
    if not self.database.existsLabel(oldLabel):
      CLog.Error(f'Label : {oldLabel} is not available')
      messagebox.showwarning(title="Can't Modify !", message=f"Label : {oldLabel} is not available")
      topLevel.focus()
      return
    
    CLog.Trace(f'Label : {oldLabel} is being modified')
    
    if topLevel:
      topLevel.destroy()
    top = SubWindow(self.app, title='Modify Item', width=700, height=200)
    UpperFrame = TFrame(top)
    UpperFrame.pack(fill='both', expand=1, anchor='center')
    for i in range(6):
      UpperFrame.grid_columnconfigure(i, weight=1, minsize=20)
    for i in range(3):
      UpperFrame.grid_rowconfigure(i, minsize=30)
    
      
    lbl1 = ttk.Label(UpperFrame, text="Enter Label")
    lbl1.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
    
    Label = ttk.Entry(UpperFrame)
    Label.grid(row=2, column=1, sticky='nsew', padx=5, pady=5)
    
    lbl2 = ttk.Label(UpperFrame, text="Enter Description")
    lbl2.grid(row=1, column=2, sticky='nsew', padx=5, pady=5)
    
    Description = ttk.Entry(UpperFrame)
    Description.grid(row=2, column=2, sticky='nsew', padx=5, pady=5)
    
    lbl3 = ttk.Label(UpperFrame, text="Enter Quantity")
    lbl3.grid(row=1, column=3, sticky='nsew', padx=5, pady=5)
    
    Quantity = ttk.Entry(UpperFrame)
    Quantity.grid(row=2, column=3, sticky='nsew', padx=5, pady=5)
    
    lbl4 = ttk.Label(UpperFrame, text="Enter Price")
    lbl4.grid(row=1, column=4, sticky='nsew', padx=5, pady=5)
    
    Price = ttk.Entry(UpperFrame)
    Price.grid(row=2, column=4, sticky='nsew', padx=5, pady=5)
    
    LowerFrame = TFrame(top)
    LowerFrame.pack(fill='both', expand=1, anchor='center')
    for i in range(4):
      LowerFrame.grid_columnconfigure(i, weight=1, minsize=20)
    for i in range(2):
      LowerFrame.grid_rowconfigure(i, minsize=30)
    btnSet = ttk.Button(LowerFrame,text='Set', 
              command=lambda: [ self.__ModifyLabelCommand(oldLabel=oldLabel, label=Label.get(), description=Description.get(), quantity=Quantity.get(), price=Price.get()), top.destroy() ] )
    btnSet.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
    btnCancel = ttk.Button(LowerFrame,text='Cancel', command=lambda: top.destroy())
    btnCancel.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)
      
    
    
  def ModifyItemByLabel(self):
    top = SubWindow(self.app, title='Modify Item By Label', width=300, height=200)
    UpperFrame = TFrame(top)
    UpperFrame.pack(fill='both', expand=1, anchor='center')
    for i in range(3):
      UpperFrame.grid_columnconfigure(i, weight=1, minsize=20)
    for i in range(3):
      UpperFrame.grid_rowconfigure(i, minsize=30)
    
      
    lbl1 = ttk.Label(UpperFrame, text="Enter Label")
    lbl1.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
    Label = ttk.Entry(UpperFrame, width=35)
    Label.grid(row=2, column=1, sticky='nsew', padx=5, pady=5)
    
    
    
    LowerFrame = TFrame(top)
    LowerFrame.pack(fill='both', expand=1, anchor='center')
    for i in range(4):
      LowerFrame.grid_columnconfigure(i, weight=1, minsize=20)
    for i in range(3):
      LowerFrame.grid_rowconfigure(i, minsize=30)
    btnGet = ttk.Button(LowerFrame,text='Get', command=lambda: [self.ModifyByLabelAction(oldLabel=Label.get(), topLevel=top)])
    btnGet.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
    
    btnCancel = ttk.Button(LowerFrame,text='Cancel', command=lambda: top.destroy())
    btnCancel.grid(row=1, column=2, sticky='nsew', padx=5, pady=5)
    
  def ModifyItemByRef(self):
    top = SubWindow(self.app, title='Modify Item By Ref', width=300, height=200)
    UpperFrame = TFrame(top)
    UpperFrame.pack(fill='both', expand=1, anchor='center')
    for i in range(3):
      UpperFrame.grid_columnconfigure(i, weight=1, minsize=20)
    for i in range(4):
      UpperFrame.grid_rowconfigure(i, minsize=30)
    
      
    lbl1 = ttk.Label(UpperFrame, text="Enter Ref")
    lbl1.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
    Ref = ttk.Entry(UpperFrame, width=35)
    Ref.grid(row=2, column=1, sticky='nsew', padx=5, pady=5)
    
    
    
    LowerFrame = TFrame(top)
    LowerFrame.pack(fill='both', expand=1, anchor='center')
    for i in range(4):
      LowerFrame.grid_columnconfigure(i, weight=1, minsize=20)
    for i in range(3):
      LowerFrame.grid_rowconfigure(i, minsize=40)
    btnGet = ttk.Button(LowerFrame,text='Get', command=lambda: [self.ModifyByRefAction(ref=Ref.get(), topLevel=top)])
    btnGet.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
    
    btnCancel = ttk.Button(LowerFrame,text='Cancel', command=lambda: top.destroy())
    btnCancel.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)
    
  def OpenDirectoryFileTable(self, relpath: str = '-1'):
   
    if relpath == '-1':
      self.fileManager = TFileManager('..\\databases')
      relpath = filedialog.askdirectory(initialdir=self.fileManager.GetAbsolutePath())
      
      
    self.fileManager = TFileManager(relpath)
      
    for item in self.table.get_children():
      self.table.delete(item)
    
    
    self.table 
    

    ################################################
    # //todo this 
    self.LoadDirectoryTable(relpath)
    ################################################
    
    
    
  def InitScrollbars(self):
    self.scrollbarVertical = TScrollbar(master=self, orient='vertical', command=self.table.yview)
    self.table.configure(yscroll = self.scrollbarVertical.set)
    self.scrollbarVertical.grid(row=0, column=1, sticky='ns')

    self.scrollbarHorizontal = TScrollbar(master=self, orient='horizontal', command=self.table.xview)
    self.table.configure(xscroll=self.scrollbarHorizontal.set)
    self.scrollbarHorizontal.grid(row=1, column=0, sticky='ew')
      
  def Insert(self, parentiid = '', text: str = '', values = [], index='end'):
    self.table.insert(parentiid, index=index, values=values, text=text)