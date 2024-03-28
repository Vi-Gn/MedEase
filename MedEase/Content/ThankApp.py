
from tkinter.ttk import Label as TLabel
from tkinter.ttk import Frame as TFrame
from tkinter.ttk import Style as TStyle
from tkinter import Tk as TTk
from tkinter.font import Font as TFont

from ConfigJSON import *
from Enums import ETHEMESTATE

class ThanksApp(TTk):
    def __init__(self, *args, **vargs) -> None:
        super().__init__(*args, **vargs)
        self.title('Thank You!')
        self.bind('<KeyPress>', lambda e : self.destroy())
        self.bind("<F7>", self.PreviousTheme)
        self.bind("<F8>", self.NextTheme)
        self.width = 880
        self.height = 725
        self.minsize(width=self.width, height=self.height)
        self.maxsize(width=self.width, height=self.height)
        self.CenterWindow()
        self.Theme: ETHEMESTATE = ETHEMESTATE.SUNVALLEYDARK
        self.frame = TFrame(master=self)
        self.frame.pack(fill='both', expand=1)
        self.style = TStyle()
        self.style.tk.call("source", "Themes\\ForestTheme\\forest-dark.tcl")
        self.style.tk.call("source", "Themes\\ForestTheme\\forest-light.tcl")
        self.style.tk.call("source", "Themes/AzureTheme/azure.tcl")
        self.style.tk.call("source", "Themes/SunValley/sv_ttk/sv.tcl")
        self.SetTheme(self.Theme)
                
        custom_font = TFont(family="Helvetica", size=16, weight="bold", slant="italic")
        TLabel(master=self.frame, text='''Dear HALA Nourdine,


      I wanted to express my heartfelt thanks for your 
    exceptional teaching in software engineering and 
    algorithms.
    
      Your passion and expertise have made a significant
    impact on my understanding and confidence in these
    subjects.
    
      Your support and encouragement have created a positive
    learning environment that I truly appreciate.
        
        
      Thank you for your dedication to our education.


Best regards,
EL HARRAK Anouar

                Press Escape to close this window!
                ''', font=custom_font, anchor='center').pack(fill='both', expand=1, padx=80, pady=80)
        
        
    def Run(self):
        self.mainloop()
        
        
    def CenterWindow(self):
        self.update_idletasks()
        x_offset = (self.winfo_screenwidth() - self.width) // 2
        y_offset = (self.winfo_screenheight() - self.height) // 2
        self.geometry(f"{self.width}x{self.height}+{x_offset}+{y_offset}")
        
    def SetTheme(self, eThemeState: ETHEMESTATE):
        """ themeName: [EThemeState.DEFAULT,  EThemeState.LIGHT,  EThemeState.DARK] """
        self.Theme = eThemeState
        match (eThemeState):
        
            case (ETHEMESTATE.DEFAULT):
                self.style.theme_use( f"default")
                
            case (ETHEMESTATE.FORESTLIGHT):
                # Source : https://github.com/rdbende/Forest-ttk-theme
                self.style.theme_use( f"forest-light")
                
            case (ETHEMESTATE.FORESTDARK):
                # Source : https://github.com/rdbende/Forest-ttk-theme
                self.style.theme_use( f"forest-dark")
            
            case (ETHEMESTATE.AZURELIGHT):
                # Source : https://github.com/rdbende/Azure-ttk-theme
                self.style.theme_use("azure-light")
                
            case (ETHEMESTATE.AZUREDARK):
                # Source : https://github.com/rdbende/Azure-ttk-theme
                self.style.theme_use("azure-dark")
            
            
            case (ETHEMESTATE.SUNVALLEYLIGHT):
                # Source : https://github.com/rdbende/Azure-ttk-theme
                self.style.theme_use("sun-valley-light")
                
            case (ETHEMESTATE.SUNVALLEYDARK):
                # Source : https://github.com/rdbende/Azure-ttk-theme
                self.style.theme_use("sun-valley-dark")
            
            case (ETHEMESTATE.ALT):
                self.style.theme_use( f"alt")
                
            case (ETHEMESTATE.CLAM):
                self.style.theme_use( f"clam")
                
            case (ETHEMESTATE.VISTA):
                self.style.theme_use( f"vista")
                
            case (ETHEMESTATE.XPNATIVE):
                self.style.theme_use( f"xpnative")
                
            case (ETHEMESTATE.WINNATIVE):
                self.style.theme_use( f"winnative")
                
            case (ETHEMESTATE.CLASSIC):
                self.style.theme_use( f"classic")
                
            case _:
                raise Exception(f"There is no theme called {eThemeState}")
            
            
        

    def NextTheme(self, *args):    
        self.Theme = ETHEMESTATE.next(self.Theme)
        self.SetTheme(self.Theme)
        print(self.Theme)
    

    def PreviousTheme(self, *args):    
        self.Theme = ETHEMESTATE.prev(self.Theme)
        self.SetTheme(self.Theme)
        print(self.Theme)
    