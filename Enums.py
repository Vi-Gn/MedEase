from enum import Enum



class ETHEMESTATE(Enum):
  DEFAULT = 0
  FORESTLIGHT = 1
  FORESTDARK = 2
  AZURELIGHT = 3
  AZUREDARK = 4
  ALT = 5
  CLAM = 6
  VISTA = 7
  XPNATIVE = 8
  WINNATIVE = 9
  CLASSIC = 10
  
  def next(self):
    index = self.value + 1
    index %= len(ETHEMESTATE)
    return ETHEMESTATE(index)
    
  def prev(self):
    index = self.value - 1
    index %= len(ETHEMESTATE)
    return ETHEMESTATE(index)
    
  