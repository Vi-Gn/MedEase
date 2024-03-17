import json as JSON
from Enums import *

from CLog import *




class Config:
  
  configDict = {
  
              'themeName': EThemeState.AZURELIGHT.name,
              'winSizeX': 1024,
              'winSizeY': 450,
              'winState': 'normal',

  }

  
  @staticmethod
  def GetThemeConfig():
    try:
      themeName = EThemeState[Config.configDict['themeName']]
    except:
      themeName = EThemeState.VISTA.name
      CLog.Error("Can't load theme : not found! | VISTA theme choosed instead")
    else:
      print(f"Theme : {themeName} | Loaded Successfully")
    return themeName
    
  @staticmethod
  def SetThemeConfig(eThemeState: EThemeState):
    Config.configDict['themeName'] = eThemeState.name
    
  
  @staticmethod
  def SaveConfig():
    cfg = open('config.JSON', 'w', newline='\n')
    JSON.dump(Config.configDict, cfg, indent=4)
    cfg.close()
    
  @staticmethod
  def LoadConfig():
    cfg = open('config.JSON', 'r')
    Config.configDict = JSON.load(cfg)


# theme = EThemeState.FORESTDARK
# Config.SetThemeConfig(theme)

# conf = Config.SaveConfig()

Config.LoadConfig()

print(Config.GetThemeConfig())