# main.py

import tkinter as tk
from gui.pantallaGestionRegistroResultadoRevisionManual import PantallaGestionRegistroResultadoRevisionManual
if __name__ == "__main__":
    root = tk.Tk()
    app = PantallaGestionRegistroResultadoRevisionManual(master=root)
    app.mainloop()