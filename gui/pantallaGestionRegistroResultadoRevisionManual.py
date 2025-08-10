# gui/pantallaGestionRegistroResultadoRevisionManual.py

import tkinter as tk
from tkinter import ttk, messagebox
from gestor.gestorRegistroResultadoRevisionManual import GestorRegistroResultadoRevisionManual

class PantallaGestionRegistroResultadoRevisionManual(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Registrar Resultado de Revisión Manual (CU-23)")
        self.master.geometry("900x700")
        self.pack(fill="both", expand=True)
        self.gestor = GestorRegistroResultadoRevisionManual(self)
        self.crear_widgets()
        self.habilitarVentana()

    def crear_widgets(self):
        frame_lista = tk.LabelFrame(self, text="Paso 1: Seleccionar Opción y Evento a Revisar")
        frame_lista.pack(pady=10, padx=10, fill="x")
        
        self.btn_buscar = tk.Button(frame_lista, text="Registrar Resultado de Revisión Manual", command=self.opcion_registrar_resultado)
        self.btn_buscar.pack(pady=5)
        
        self.tree_sismos = ttk.Treeview(frame_lista, columns=("ID", "Fecha", "Magnitud", "Estado"), show="headings")
        self.tree_sismos.heading("ID", text="ID"); self.tree_sismos.heading("Fecha", text="Fecha/Hora"); self.tree_sismos.heading("Magnitud", text="Magnitud"); self.tree_sismos.heading("Estado", text="Estado Actual")
        self.tree_sismos.pack(pady=5, padx=5, fill="x")
        self.tree_sismos.bind("<<TreeviewSelect>>", self.on_sismo_select)

        frame_detalles = tk.LabelFrame(self, text="Paso 2: Visualizar Datos del Evento Seleccionado")
        frame_detalles.pack(pady=10, padx=10, fill="both", expand=True)
        self.lbl_detalles = tk.Label(frame_detalles, text="Seleccione un sismo de la lista para comenzar.", justify=tk.LEFT, anchor="nw")
        self.lbl_detalles.pack(pady=5, padx=5, fill="both", expand=True)
        
        frame_acciones = tk.LabelFrame(self, text="Paso 3: Tomar una Acción")
        frame_acciones.pack(pady=10, padx=10, fill="x")

        self.btn_ver_mapa = tk.Button(frame_acciones, text="Visualizar Mapa", state="disabled")
        self.btn_ver_mapa.pack(side="left", padx=5, pady=5)
        self.btn_modificar = tk.Button(frame_acciones, text="Modificar Datos", state="disabled")
        self.btn_modificar.pack(side="left", padx=5, pady=5)

        self.btn_confirmar = tk.Button(frame_acciones, text="Confirmar Evento", state="disabled")
        self.btn_confirmar.pack(side="right", padx=5, pady=5)
        self.btn_rechazar = tk.Button(frame_acciones, text="Rechazar Evento", state="disabled", command=self.tomarSeleccionRechazo)
        self.btn_rechazar.pack(side="right", padx=5, pady=5)
        self.btn_derivar = tk.Button(frame_acciones, text="Solicitar Revisión a Experto", state="disabled")
        self.btn_derivar.pack(side="right", padx=5, pady=5)


    def habilitarVentana(self):
        print("\n** PANTALLA: Ventana habilitada. **")
        messagebox.showinfo("Inicio", "Bienvenido. Por favor, seleccione la opción para registrar un resultado.")

    def opcion_registrar_resultado(self):
        print("\n** PANTALLA: (CU-23 P.5) Actor seleccionó la opción. Buscando sismos... **")
        self.solicitarSeleccionEventoSismico()
        self.btn_buscar.config(state="disabled")

    def solicitarSeleccionEventoSismico(self):
        self.gestor.buscarSismosAutoDetectadosYPendienteDeRevision()

    def mostrarEventosSismicosEncontradosOrdenados(self, lista_sismos):
        print("** PANTALLA: (CU-23 P.6) Mostrando sismos no revisados. Por favor, seleccione uno. **")
        for i in self.tree_sismos.get_children(): self.tree_sismos.delete(i)
        for sismo in lista_sismos:
            estado_nombre = sismo.estadoActual.actual.nombre
            self.tree_sismos.insert("", "end", values=(sismo.id_sismo, sismo.fechaHoraOcurrencia.strftime("%Y-%m-%d %H:%M"), sismo.valorMagnitud, estado_nombre))

    def on_sismo_select(self, event):
        selected_item = self.tree_sismos.selection()
        if selected_item:
            sismo_id = self.tree_sismos.item(selected_item)['values'][0]
            self.tomarSeleccionEventoSismico(sismo_id)

    def tomarSeleccionEventoSismico(self, sismo_id):
        print(f"\n** PANTALLA: (CU-23 P.7) Se tomó la selección del sismo ID: {sismo_id} **")
        self.tree_sismos.config(selectmode="none")
        self.gestor.tomarSeleccionEventoSismico(sismo_id)

    def mostrarDatosEventoSismicoSeleccionado(self, sismo):
        print(f"** PANTALLA: (CU-23 P.9) Mostrando datos del sismo {sismo.id_sismo} **")
        sismo_info = sismo.getDatosEventoSismico()
        texto = (
            f"ID: {sismo_info['ID']}\n"
            f"Fecha/Hora: {sismo_info['Fecha/Hora'].strftime('%Y-%m-%d %H:%M')}\n"
            f"Magnitud: {sismo_info['Magnitud']}\n"
            f"Estado Actual: {sismo.estadoActual.actual.nombre}\n\n"
            f"--- Detalles Adicionales ---\n"
            f"Alcance: {sismo.getAlcance()}\n"
            f"Clasificación: {sismo.getClasificacion()}\n"
            f"Origen: {sismo.getOrigen()}\n\n"
            f"Sismograma generado. (CU-23 P.9.3)"
        )
        self.lbl_detalles.config(text=texto)

    def habilitarOpcionesDeRevision(self):
        print("** PANTALLA: (CU-23 P.10, 12, 14) Habilitando opciones de revisión. **")
        self.btn_ver_mapa.config(state="normal")
        self.btn_modificar.config(state="normal")
        self.btn_confirmar.config(state="normal")
        self.btn_rechazar.config(state="normal")
        self.btn_derivar.config(state="normal")
        messagebox.showinfo("Siguiente Paso", "Se han cargado los datos del sismo. Por favor, seleccione una acción a realizar.")

    def tomarSeleccionRechazo(self):
        print("** PANTALLA: (CU-23 P.15) Usuario seleccionó RECHAZAR. **")
        if messagebox.askyesno("Confirmar Rechazo", "¿Está seguro de que desea RECHAZAR la revisión de este evento sísmico?"):
            self.gestor.tomarSeleccionRechazo()
        else:
            print("** PANTALLA: El usuario canceló el rechazo. **")

    def finCU(self):
        messagebox.showinfo("Proceso Finalizado", "El evento ha sido marcado como 'Rechazado'. La interfaz se reiniciará.")
        self.lbl_detalles.config(text="Seleccione un sismo de la lista para comenzar.")
        for btn in [self.btn_ver_mapa, self.btn_modificar, self.btn_confirmar, self.btn_rechazar, self.btn_derivar, self.btn_buscar]:
            btn.config(state="disabled")
        self.tree_sismos.config(selectmode="browse")
        self.btn_buscar.config(state="normal")
        self.gestor.buscarSismosAutoDetectadosYPendienteDeRevision()