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




import sqlite3

"""
# data = sqlite3.connect('MedStocks.db')
# table = 'stocks'
# create_table = \""" CREATE TABLE IF NOT EXISTS projects (
  
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         name text NOT NULL,
#                         begin_date text,
#                         end_date text
                        
#                     ); \"""
                                    
# data.execute(f"create table {table} (id INTEGER PRIMARY KEY AUTOINCREMENT,\
#                                     name VARCHAR(25),\
#                                     price FLOAT,\
#                                     quantity INT\
#                                     )\
#                                     ")

# data.execute(f"INSERT INTO  {table}(name, price, quantity)\
#               VALUES ( 'hmd', 0.0, 99999)"
#             )
#
# data.commit()
#
# cursor = data.execute( f"SELECT * FROM {table}")
# print(cursor.fetchall())
"""


def warn(*kwarg):
  print(kwarg)


class RDB():
    def __init__(self, databaseName: str = 'MedStocks.db') -> None:
      self.databaseName = databaseName
      self.database = sqlite3.connect(databaseName)
      self.cursor = self.database.cursor()
      self.table = 'stocks'

    def __del__(self):
      print(f"{self.databaseName} has been destroyed from memory")
    
    def createTable(self, table: str = 'stocks') -> None:
      self.table = table
      try:
          self.cursor.execute(f""" CREATE TABLE IF NOT EXISTS {table} (

                              ref INTEGER PRIMARY KEY AUTOINCREMENT,
                              label VARCHAR(50) NOT NULL,
                              description VARCHAR(50),
                              quantity INT,
                              price FLOAT

                  ); """)

      except Exception as e:
          print('wdwd',e)

    def save(self):
      print(f"DB : {self.databaseName} has been saved successfully")
      self.database.commit()


    def insert(self, label: str, description: str, quantity: int, price: float):
        self.execLines("INSERT INTO stocks(label, description, quantity, price)",
                              f"VALUES ( '{label}', '{description}', {quantity}, {price})")
        

    def execLinesFetched(self, *lines):
        """fetch all from exec without altering current cursor value"""
        cmd = ''
        for line in lines:
            cmd += ' ' + line
        self.cursor.execute(cmd)
        return self.cursor.fetchall()

    def execLines(self, *lines):
        cmd = ''
        for line in lines:
            cmd += ' ' + line
        self.cursor.execute(cmd)

    def execListFetched(self, arr: list[str]):
        """fetch all from exec without altering current cursor value"""
        cmd = ' '.join(arr)
        self.cursor.execute(cmd)
        return self.cursor.fetchall()

    def execList(self, arr: list[str]):
        cmd = ' '.join(arr)
        self.cursor.execute(cmd)

    def fetchAll(self):
        return self.cursor.fetchall()

    def fetchOne(self):
        return self.cursor.fetchone()

    def getColumnNames(self):
        temp = self.execLinesFetched( f'SELECT name FROM PRAGMA_TABLE_INFO("{self.table}");')
        
        self.colnames = []
        for elem in temp:
            self.colnames.append(elem[0])
        return self.colnames

    def getData(self, cols: str = '*'):
        self.cursor.execute(f'SELECT {cols} FROM {self.table}')
        return self.cursor.fetchall()

    def getDataSortedBy(self, cols: str = '*', colTextToSort: str = 'ref', orderSort:bool = True):
        '''orderSort: [True -> ASC, False -> DESC]'''
        order = 'ASC' if orderSort else 'DESC'
        
        self.cursor.execute(f'SELECT {cols} FROM {self.table} ORDER BY {colTextToSort} {order}')
        return self.cursor.fetchall()

    def getRef(self, ref: int, cols: str = '*'):
        if not(self.existsRef(ref)):
            print(f"{ref =} doesn't exist")
            return
        self.cursor.execute(f'SELECT {cols} FROM {self.table} WHERE ref={ref}')
        return self.cursor.fetchone()

    def getLabel(self, label: str, cols: str = '*'):
        if not(self.existsLabel(label)):
            print(f"{label =} doesn't exist")
            return
        self.cursor.execute(f'SELECT {cols} FROM {self.table} WHERE label="{label}"')
        return self.cursor.fetchone()

    def getLabelContain(self, label: str, cols: str = '*'):
        if not(self.existsLabelContain(label)):
            print(f"{label =} doesn't exist")
            return
        self.cursor.execute(f"SELECT {cols} FROM {self.table} WHERE label like'%{label}%'")
        return self.cursor.fetchall()

    def getColContain(self, content: str, colName: str, cols: str = '*'):
        self.cursor.execute(f"SELECT {cols} FROM {self.table} WHERE {colName} like'%{content}%'")
        return self.cursor.fetchall()

    def modifyAllByRef(self, ref: int, label: str, description: str, quantity: int, price: float):
        if not(self.existsRef(ref)):
            print(f"{ref =} doesn't exist")
            return
        update = f''' UPDATE {self.table}
                      SET label = "{label}" ,
                          description = "{description}" ,
                          quantity = {quantity} ,
                          price = {price}
                      WHERE ref = {ref};
        '''
        self.cursor.execute(update)
        

    def modifyColByRef(self, ref: int, col:str, content):
        if not(self.existsRef(ref)):
            print(f"{ref =} doesn't exist")
            return
        print(col)
        if col.lower() == "label":
          if self.existsLabel(content):
            print(f"Label = {content} already exists")
            return -1
        update = f''' UPDATE {self.table}
                   SET {col} = "{content}" 
                   WHERE ref = {ref};
        '''
        self.cursor.execute(update)
        

    def modifyColByLabel(self, label: str, col, content):
        if not(self.existsLabel(label)):
            print(f"{label =} doesn't exist")
            return
        print(f"label cond : {label}, col name : {col}, its content : {content}")
        update = f''' UPDATE {self.table}
                   SET {col} = "{content}" 
                   WHERE label = "{label}";
        '''
        self.cursor.execute(update)
        

    def modifyAllByLabel(self, oldLabel: str, label: str, description: str, quantity: int, price: float):
        if not(self.existsLabel(oldLabel)):
            print(f"{label =} doesn't exist")
            return
        update = f''' UPDATE {self.table}
                   SET label = "{label}" ,
                       description = "{description}" ,
                       quantity = {quantity} ,
                       price = {price}
                   WHERE label = '{oldLabel}';
        '''
        self.cursor.execute(update)
        

    

    def removeAll(self):
        self.cursor.execute(f"DELETE FROM {self.table};")
        
        
    def removeByRef(self, ref: int):
        if not(self.existsRef(ref)):
            print(f"{ref =} doesn't exist")
            return
        self.cursor.execute(f"DELETE FROM {self.table} WHERE ref = {ref};")
        
        
    def removeByLabel(self, label: str):
        if not(self.existsLabel(label)):
            print(f"{label =} doesn't exist")
            return
        self.cursor.execute(f"DELETE FROM {self.table} WHERE label = '{label}';")
        

    def checkForQuantityByRef(self, ref: int, quantity: int):
        if not(self.existsRef(ref)):
            print(f"{ref =} doesn't exist")
            return
        return (self.getRef(ref, 'quantity')[0] >= quantity)

    def checkForQuantityByLabel(self, label: str, quantity: int):
        if not(self.existsLabel(label)):
            print(f"{label =} doesn't exist")
            return False
        return (self.getLabel(label, 'quantity')[0] >= quantity)

    def consumeByRef(self, ref: int, quantity: int):
        if not(self.existsRef(ref)):
            print(f"{ref =} doesn't exist")
            return
        hasQuantity = self.checkForQuantityByRef(ref, quantity)
        if hasQuantity == False:
            print("We Don't have this much quantity")
            return
        update = f''' UPDATE {self.table}
                           SET quantity = quantity - {quantity}
                           WHERE ref = {ref};
                '''
        self.cursor.execute(update)
        
        
    def consumeByLabel(self, label: str, quantity: int):
        if not(self.existsLabel(label)):
            print(f"{label =} doesn't exist")
            return
        hasQuantity = self.checkForQuantityByLabel(label, quantity)
        if hasQuantity == False:
            print("We Don't have this much quantity")
            return
        update = f''' UPDATE {self.table}
                                   SET quantity = quantity - {quantity}
                                   WHERE label = "{label};
                        '''
        self.cursor.execute(update)
        

    def addQuantityByRef(self, ref: int, quantity: int):
        if not(self.existsRef(ref)):
            print(f"{ref =} doesn't exist")
            return
        update = f''' UPDATE {self.table}
                           SET quantity = quantity + {quantity}
                           WHERE ref = {ref};
                '''
        self.cursor.execute(update)
        
        
    def addQuantityByLabel(self, label: str, quantity: int):
        if not(self.existsLabel(label)):
            print(f"{label =} doesn't exist")
            return
        update = f''' UPDATE {self.table}
                                   SET quantity = quantity + {quantity}
                                   WHERE label = "{label}";
                        '''
        self.cursor.execute(update)
        

    def printData(self, cols: str = '*'):
        for item in self.getData(cols):
            print(item)

    def existsRef(self, ref: int):
        self.cursor.execute(f"SELECT COUNT(*) FROM {self.table} WHERE ref={ref}")
        return self.cursor.fetchone()[0] > 0

    def existsLabel(self, label: str):
        self.cursor.execute(f"SELECT COUNT(*) FROM {self.table} WHERE label='{label}'")
        return self.cursor.fetchone()[0] > 0

    def existsLabelContain(self, label: str):
        self.cursor.execute(f"SELECT COUNT(*) FROM {self.table} WHERE label like'%{label}%'")
        return self.cursor.fetchone()[0] > 0

class DataShower:
  msgshow: str = '''
          1 - Full
          2 - label
          3 - description
          4 - quantity
          5 - price
          0 - back
  '''
  
  @staticmethod
  def showMenu():
    print('''show''')
    menu = int(input(DataShower.msgshow))
    match (menu):
      case (1):
        DataShower.showAll()
      case (2):
        DataShower.showlabelle()
      case (3):
        DataShower.showDescription()
      case (4):
        DataShower.showQuantity()
      case (5):
        DataShower.showPrice()
      case (0):
        return
        

  @staticmethod
  def showAll(ldata):
    if ldata == None:
      raise Exception('data invalid')
    data = ldata
    print('''all''')
    for item in data.getData('*'):
          print(item)
      

  @staticmethod
  def showlabelle(ldata):
    if ldata == None:
      raise Exception('data invalid')
    data = ldata
    print('''label''')
    for item in data.getData('label'):
          print(item)

  @staticmethod
  def showDescription(ldata):
    print('''description''')
    if ldata == None:
      raise Exception('data invalid')
    data = ldata
    for item in data.getData('description'):
          print(item)
      

  @staticmethod
  def showQuantity(ldata):
    print('''quantity''')
    if ldata == None:
      raise Exception('data invalid')
    data = ldata
    for item in data.getData('quantity'):
      print(item)

  @staticmethod
  def showPrice(ldata):
    print('''price''')
    if ldata == None:
      raise Exception('data invalid')
    data = ldata
    for item in data.getData('price'):
      print(item)
      
class DataAdder:
  msgaddstock: str = '''
        1 - ref
        2 - label
        0 - back
  '''
  @staticmethod
  def addMenu(ldata = None, label: str = '', description: str = '', quantity: int = 0, price: float = 0.0, action: str=''):
    """@action => p = add price; q = modify price; qp = both"""
    
    print('''add''')
    if label == '':
      label = input('Enter label')
    if ldata == None:
      raise Exception('data invalid')
    data = ldata
    if data.existsLabel(label):
      if ( action == ''):
        action = input(f'label {label} already exists if you want to add a quantity enter q; if want to change price enter p; if both enter qp')

      match (action):
        case ('q'):
          if(quantity == 0):
            quantity = int(input('Enter quantity to add'))
          data.addQuantityByLabel(label, quantity)
          print(f'the item with name : {label} got an addition in quantity by {quantity}')
          return
        case ('p'):
          if(price == 0.0):
            price = float(input('Important! Erase old Price; Enter the new price'))
          data.modifyColByLabel(label, 'price', price)
          print(f'the item\'s new price = {price}')
          return
        case ('qp'):
          if(quantity == 0):
            quantity = int(input('Enter quantity to add'))
          if(price == 0.0):
            price = float(input('Important! Erase old Price; Enter the new price'))
          data.addQuantityByLabel(label, quantity)
          print(f'the item with name : {label} got an addition in quantity by {quantity}')
          data.modifyColByLabel(label, 'price', price)
          print(f'the item\'s new price = {price}')
          return
        case _:
          raise Exception('action should not be different than p, q, qp')
      

    if description == '':
      description = input('Enter description')
    if quantity == 0:
      quantity = int(input('Enter quantity'))
    if price == 0.0:
      price = float(input('Enter price'))
    
      
    data.insert(label, description, quantity, price)
    
    
    
  @staticmethod
  def addMenuUICheck(ldata = None, label: str = ''):
    """ @function shall return => p = add price; q = modify price; qp = both """
    print('''add''')
    if ldata == None:
      raise Exception('data invalid')
    data = ldata
    if data.existsLabel(label):
      return False
    return True
      
      
  @staticmethod
  def addMenuUI(ldata = None, label: str = '', description: str = '', quantity: int = 0, price: float = 0.0, action = ''):
    """ @function shall return => p = add price; q = modify price; qp = both """
    print('''add''')
    if ldata == None:
      raise Exception('data invalid')
    data = ldata
    if data.existsLabel(label):
      if action=='':
        raise Exception('maaan coome on')
     
      match (action):
        case ('q'):
          if(quantity == 0):
            raise Exception("quantity to add shall not be 0")
          data.addQuantityByLabel(label, quantity)
          print(f'the item with name : {label} got an addition in quantity by {quantity}')
          return
        case ('p'):
          if(price == 0.0):
            raise Exception("price shall not be 0")
          data.modifyColByLabel(label, 'price', price)
          print(f'the item\'s new price = {price}')
          return
        case ('qp'):
          if(quantity == 0):
            raise Exception("quantity to add shall not be 0")
          if(price == 0.0):
            raise Exception("price shall not be 0")
          data.addQuantityByLabel(label, quantity)
          print(f'the item with name : {label} got an addition in quantity by {quantity}')
          data.modifyColByLabel(label, 'price', price)
          print(f'the item\'s new price = {price}')
          return
        case _:
          raise Exception('action should not be different than p, q, qp')
      
    data.insert(label, description, quantity, price)



  @staticmethod
  def expandQuantityMenu(ldata):
    '''add quantity'''
    print('''add quantity''')
    if ldata == None:
      raise Exception('data invalid')
    data = ldata
    menu = int(input(DataAdder.msgaddstock))
    match (menu):
      case (1):
        print('''ref''')
        ref = int(input("enter the ref id to add item's quantity"))
        data.existsRef(ref)

        quantity = int(input("enter the quantity to add"))
        data.addQuantityByRef(ref, quantity)
      case (2):
        print('''label''')
        label = input("Enter the label to add item's quantity")
        data.existsLabel(label)

        quantity = int(input("enter the quantity to add"))
        data.addQuantityByLabel(label, quantity)
      case (0):
        return
    
class DataModder:
  msgmodify: str = '''
        1 - byRef
        2 - byLabel
        3 - label(exp)
        4 - description(exp)
        5 - quantity(exp)
        6 - price(exp)
        0 - back
  '''
  msgmodifyBy: str = '''
            1 - byRef
            2 - byLabel
            0 - back
  '''
  @staticmethod
  def modifyMenu(ldata):
    print('''modify''')
    if ldata == None:
      raise Exception('data invalid')
    data = ldata
    menu = int(input(DataModder.msgmodify))
    match (menu):
        case (1):
            print('''modByRef''')
            ref = int(input('enter ref med to modify'))
            if data.existsRef(ref):
              label = input('Enter label')
              description = input('Enter description')
              quantity = int(input('Enter quantity'))
              price = float(input('Enter price'))
              data.modifyAllByRef(ref, label, description, quantity, price)
            else:
              print(f'ref : {ref} is not found!')
              
        case (2):
            print('''modByLabel''')
            oldLabel = input('enter label med to modify')
            print(f"waaa3ibadllah {oldLabel}")
            if data.existsLabel(oldLabel):
              label = input('Enter new label')
              description = input('Enter description')
              quantity = int(input('Enter quantity'))
              price = float(input('Enter price'))
              data.modifyAllByLabel(oldLabel, label, description, quantity, price)
            else:
              print(f'label : {oldLabel} is not found!')
            
        case (3):
            print('''modLabel (experimental)''')
            temp = DataModder.msgmodify.split('\n')[3]
            menu = int(input(temp + DataModder.msgmodifyBy))
            match (menu):
              case (1):
                print('''modLabelByRef''')
                ref = int(input('enter ref med to modify'))
                if data.existsRef(ref):
                  label = input('Enter new label')
                  data.modifyColByRef(ref, 'label', label)
                else:
                  print(f'ref : {ref} is not found!')
                  
              case (2):
                print('''modLabelByLabel''')
                oldLabel = input('Enter label')
                if data.existsLabel(oldLabel):
                  label = input('Enter new label')
                  data.modifyColByLabel(oldLabel, 'label', label)
                else:
                  print(f'label : {oldLabel} is not found!')
              case (0):
                return
                  
        case (4):
            print('''modDescription (experimental)''')
            temp = DataModder.msgmodify.split('\n')[4]
            menu = int(input(temp + DataModder.msgmodifyBy))
            match (menu):
              case (1):
                print('''modDescriptionByRef''')
                ref = int(input('enter ref med to modify'))
                if data.existsRef(ref):
                  Description = input('Enter new Description')
                  data.modifyColByRef(ref, 'Description', Description)
                else:
                  print(f'ref : {ref} is not found!')
                  
              case (2):
                print('''modDescriptionByLabel''')
                oldLabel = input('Enter label')
                if data.existsLabel(oldLabel):
                  Description = input('Enter new Description')
                  data.modifyColByLabel(oldLabel, 'Description', Description)
                else:
                  print(f'label : {oldLabel} is not found!')  
              case (0):
                return
                  
        case (5):
            print('''modquantity (experimental)''')
            temp = DataModder.msgmodify.split('\n')[5]
            menu = int(input(temp + DataModder.msgmodifyBy))
            match (menu):
              case (1):
                print('''modquantityByRef''')
                ref = int(input('enter ref med to modify'))
                if data.existsRef(ref):
                  quantity = input('Enter new quantity')
                  data.modifyColByRef(ref, 'quantity', quantity)
                else:
                  print(f'ref : {ref} is not found!')
                  
              case (2):
                print('''modquantityByLabel''')
                oldLabel = input('Enter label')
                if data.existsLabel(oldLabel):
                  quantity = input('Enter new quantity')
                  data.modifyColByLabel(oldLabel, 'quantity', quantity)
                else:
                  print(f'label : {oldLabel} is not found!')
              case (0):
                return
        case (6):
            print('''modprice (experimental)''')
            temp = DataModder.msgmodify.split('\n')[6]
            menu = int(input(temp + DataModder.msgmodifyBy))
            match (menu):
              case (1):
                print('''modpriceByRef''')
                ref = int(input('enter ref med to modify'))
                if data.existsRef(ref):
                  price = input('Enter new price')
                  data.modifyColByRef(ref, 'price', price)
                else:
                  print(f'ref : {ref} is not found!')
                  
              case (2):
                print('''modpriceByLabel''')
                oldLabel = input('Enter label')
                if data.existsLabel(oldLabel):
                  price = input('Enter new price')
                  data.modifyColByLabel(oldLabel, 'price', price)
                else:
                  print(f'label : {oldLabel} is not found!')
              case (0):
                return
          
          
        case (0):
          return
        
class DataFinder:
  msgsearch: str = '''
        1 - ref
        2 - label
        3 - label(contain)
        0 - back
  '''
  @staticmethod
  def searchMenu(ldata):
    print('''search''')
    if ldata == None:
      raise Exception('data invalid')
    data = ldata
    menu = int(input(DataFinder.msgsearch))
    match (menu):
        case (1):
            print('''ref''')
            ref = int(input('enter the ref id to search and show item'))
            print(data.getRef(ref))
        case (2):
            print('''label''')
            label = input('Enter the label to search and show item')
            print(data.getLabel(label))
        case (3):
            print('''label(contain)''')
            label = input('Enter the label or sublabelle to search and show item')
            print(data.getLabelContain(label))
        case (0):
          return

class DataRemover:
  msgremove: str = '''
        1 - all
        2 - ref
        3 - label
        0 - back
  '''
  msgconsume: str = '''
        1 - ref
        2 - label
        0 - back
  '''
  @staticmethod
  def removeMenu(ldata):
    print('''remove''')
    if ldata == None:
      raise Exception('data invalid')
    data = ldata
    menu = int(input(DataRemover.msgremove))
    match (menu):
      case (1):
        print('''all''')
        data.removeAll()
      case (2):
        print('''ref''')
        ref = int(input('enter the ref id to remove item'))
        data.removeByRef(ref)
      case (3):
        print('''label''')
        label = input('Enter the label to remove item')
        data.removeByLabel(label)
      case (0):
        return
      
  @staticmethod
  def consumeQuantityMenu(ldata):
    print('''consume quantity''')
    if ldata == None:
      raise Exception('data invalid')
    data = ldata
    menu = int(input(DataRemover.msgconsume))
    match (menu):
      case (1):
        print('''ref''')
        ref = int(input('enter the ref id to consume item'))
        if data.existsRef(ref):
          quantity = int(input('enter the quantity to consume'))
          data.consumeByRef(ref, quantity)
        else:
          print(f'ref : {ref} is not found!')

      case (2):
        print('''label''')
        label = input('Enter the label to consume item')
        if data.existsLabel(label):
          quantity = int(input('enter the quantity to consume'))
          data.consumeByLabel(label, quantity)
        else:
          print(f'label : {label} is not found!')
      case (0):
        return
        


