import json as JSON
from Enums import *

from CLog import *


class EWINSTATE(Enum):
  '''ZOOMED is (Windows only)'''
  NONE = ''
  NORMAL = 'normal'
  ICON = 'icon'
  ICONIC = 'iconic'
  WITHDRAWN = 'withdrawn'
  ZOOMED = 'zoomed'

class Config:
  
  configDict = {
  
              'themeName': ETHEMESTATE.AZURELIGHT.name,
              'winSizeX': -1,
              'winSizeY': -1,
              'winState': EWINSTATE.NONE.name,
              'openedRelPaths' : ['databases\\DemoData.db'],
              'relDirectory' : 'databases'
  }

  
  @staticmethod
  def GetRelDirectoryConfig():
    
    relDirectory = Config.configDict['relDirectory']      
    CLog.Info(f"Relative Directory : {relDirectory} | Loaded Successfully")
    
    return relDirectory
    
    
  @staticmethod
  def SetRelDirectoryConfig(relDirectory: str):
    Config.configDict['relDirectory'] = relDirectory
    
  
  @staticmethod
  def GetOpenedRelPathsConfig():
    openedRelPaths: list[str] = Config.configDict['openedRelPaths']
    if len(openedRelPaths):
      CLog.Info(f"Opened Paths : ")
      for penedRelPath in openedRelPaths:
        CLog.Info(f"             : {penedRelPath} | Loaded Successfully")
    else:
      CLog.Warn(f"Can't load Recent Opened Paths : not found! | Path to DemoData.db choosed instead")
    return openedRelPaths
    
    
  @staticmethod
  def SetOpenedRefPathsConfig(openedRelPaths: list[str]):
    Config.configDict['openedRelPaths'] = openedRelPaths
    
  
  @staticmethod
  def GetWinStateConfig():
    try:
      stateName = EWINSTATE[Config.configDict["winState"]]
    except Exception as e:
      stateName = EWINSTATE.NORMAL
      CLog.Error(f"Can't load window state : not found! | NORMAL state choosed instead || error msg : {e}")
    else:
      CLog.Info(f"Window State : {stateName.name} | Loaded Successfully")
    return stateName
    
  @staticmethod
  def SetWinStateConfig(eWinState: EWINSTATE):
    Config.configDict['winState'] = eWinState.name
    
    
  
  @staticmethod
  def GetThemeConfig():
    try:
      themeName = ETHEMESTATE[Config.configDict['themeName']]
    except:
      themeName = ETHEMESTATE.VISTA
      CLog.Error("Can't load theme : not found! | VISTA theme choosed instead")
    else:
      CLog.Info(f"Theme : {themeName.name} | Loaded Successfully")
    return themeName
    
  @staticmethod
  def SetThemeConfig(eThemeState: ETHEMESTATE):
    Config.configDict['themeName'] = eThemeState.name
    
    
    
    
  @staticmethod
  def GetSizeXYConfig() -> tuple[int , int]:
    SizeXY: tuple[int , int]
    
    SizeXY = ( int(Config.configDict['winSizeX']) , int(Config.configDict['winSizeY']) )
    
    CLog.Info(f"Size Loaded : X = {SizeXY[0]}, Y = {SizeXY[1]} | Loaded Successfully")
    return SizeXY
  
    
  @staticmethod
  def SetSizeXYConfig(sizeXY: tuple[int, int]):
    Config.configDict['winSizeX'] = sizeXY[0]
    Config.configDict['winSizeY'] = sizeXY[1]
  
  @staticmethod
  def SaveConfig():
    cfg = open('config.JSON', 'w', newline='\n')
    JSON.dump(Config.configDict, cfg, indent=4)
    cfg.close()
    
  @staticmethod
  def LoadConfig():
    cfg = open('config.JSON', 'r')
    try:
      Config.configDict = JSON.load(cfg)
    except Exception as e:
      CLog.Error("Can't load config file | Will revert back to default")
      Config.SaveConfig()

Config.LoadConfig()


if __name__ == '__main__':
  # theme = EThemeState.FORESTDARK
  # Config.SetThemeConfig(theme)

  # conf = Config.SaveConfig()

  

  print(Config.GetThemeConfig())