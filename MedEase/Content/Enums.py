from enum import Enum



class ETHEMESTATE(Enum):
  DEFAULT = 0
  FORESTLIGHT = 1
  FORESTDARK = 2
  AZURELIGHT = 3
  AZUREDARK = 4
  SUNVALLEYLIGHT = 5
  SUNVALLEYDARK = 6
  ALT = 7
  CLAM = 8
  VISTA = 9
  XPNATIVE = 10
  WINNATIVE = 11
  CLASSIC = 12
  
  def next(self):
    index = self.value + 1
    index %= len(ETHEMESTATE)
    return ETHEMESTATE(index)
    
  def prev(self):
    index = self.value - 1
    index %= len(ETHEMESTATE)
    return ETHEMESTATE(index)
    
  