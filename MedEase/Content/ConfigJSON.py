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
  
              'themeName': ETHEMESTATE.VISTA.name,
              'winSizeX': -1,
              'winSizeY': -1,
              'winState': EWINSTATE.NONE.name,
              'openedAbsPaths' :  [
                    
              ],
              'absDirectory' : ""
  }

  
  @staticmethod
  def SaveConfig():
    CLog.Info("Config | Saved")
    cfg = open('config.JSON', 'w', newline='\n')
    JSON.dump(Config.configDict, cfg, indent=4)
    cfg.close()
    
  @staticmethod
  def LoadConfig():
    try:
      cfg = open('config.JSON', 'r')
    except Exception as e:
      CLog.Error("Can't find config file | Will revert back to default")
      Config.SaveConfig()
    else:  
      try:
        Config.configDict = JSON.load(cfg)
        arrOpenPaths = []
        for path in Config.GetOpenedAbsPathsConfig():
          if(os.path.isfile(path)):
            arrOpenPaths.append(path)
        Config.configDict['openedAbsPaths'] = arrOpenPaths
        CLog.Info("Valid opened paths were : arrOpenPaths")
            
      except Exception as e:
        CLog.Error("Can't load config file | Will revert back to default")
        Config.SaveConfig()


  @staticmethod
  def GetAbsDirectoryConfig():
    
    absDirectory = Config.configDict['absDirectory']      
    CLog.Info(f"Working Directory : {absDirectory} | Loaded Successfully")
    
    return str(absDirectory)
    
    
  @staticmethod
  def SetAbsDirectoryConfig(absDirectory: str):
    Config.configDict['absDirectory'] = absDirectory
    CLog.Info(f"Working Directory : {absDirectory} | Saved Successfully")
    
  
  @staticmethod
  def GetOpenedAbsPathsConfig():
    openedAbsPaths: list[str] = Config.configDict['openedAbsPaths']
    if len(openedAbsPaths):
      CLog.Info(f"Opened Paths : ")
      for openedAbsPath in openedAbsPaths:
        CLog.Info(f"             : {openedAbsPath} | Loaded Successfully")
    else:
      CLog.Warn(f"Can't load Recent Opened Paths : not found! | Path to DemoData.db choosed instead")
    return openedAbsPaths
    
    
  @staticmethod
  def SetOpenedAbsPathsConfig(openedAbsPaths: list[str]):
    Config.configDict['openedAbsPaths'] = openedAbsPaths
    CLog.Trace(f"Opened Paths | Saved | Success")
    
  
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
  


if __name__ == '__main__':
  # theme = EThemeState.FORESTDARK
  # Config.SetThemeConfig(theme)

  # conf = Config.SaveConfig()

  
  Config.LoadConfig()

  print(Config.GetThemeConfig())