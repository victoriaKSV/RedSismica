# main.py

import tkinter as tk
from gui.pantallaGestionRegistroResultadoRevisionManual import PantallaGestionRegistroResultadoRevisionManual

if __name__ == "__main__":

    print("=== INICIANDO SISTEMA DE RED SÍSMICA ===")
    print("Mostrando MENU PRINCIPAL directamente (sin ventana de bienvenida)")
    
    root = tk.Tk()
    app = PantallaGestionRegistroResultadoRevisionManual(master=root)
    
    # El sistema ya está configurado para mostrar el menú principal directamente
    # gracias al método habilitarVentana() que se llama en el constructor
    
    app.mainloop()