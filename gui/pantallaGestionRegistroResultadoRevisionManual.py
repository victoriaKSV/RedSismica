# gui/pantallaGestionRegistroResultadoRevisionManual.py

import tkinter as tk
from tkinter import ttk, messagebox
from gestor.gestorRegistroResultadoRevisionManual import GestorRegistroResultadoRevisionManual

class PantallaGestionRegistroResultadoRevisionManual(tk.Frame):
    """
    CORRECCIÓN: Implementación fiel al diagrama de secuencia y anotaciones del PDF.
    SEGÚN ANOTACIONES: "Apenas se runea el main, que muestre el MENU PRINCIPAL directamente, 
    le quitaría la ventana de bienvenida y el botón de aceptar"
    """
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Sistema de Red Sísmica")
        self.master.geometry("900x700")
        self.pack(fill="both", expand=True)

        self.gestor = GestorRegistroResultadoRevisionManual(self)
        self.sismo_seleccionado_id = None

        # Crear las tres vistas principales
        self.vista_menu = tk.Frame(self)
        self.vista_lista = tk.Frame(self)
        self.vista_detalle = tk.Frame(self)

        for frame in (self.vista_menu, self.vista_lista, self.vista_detalle):
            frame.grid(row=0, column=0, sticky='nsew')
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._crear_widgets_menu()
        self._crear_widgets_lista()
        self._crear_widgets_detalle()

        # SEGÚN DIAGRAMA: :PantallaGestionRegistroResultadoRevisionManual → :PantallaGestionRegistroResultadoRevisionManual (self): habilitarVentana()
        self.habilitarVentana()

    def _mostrar_vista(self, vista_a_mostrar):
        """Cambia entre las diferentes vistas de la aplicación"""
        if vista_a_mostrar == 'menu':
            self.master.title("Menú Principal")
            self.vista_menu.tkraise()
        elif vista_a_mostrar == 'lista':
            self.master.title("Selección de Evento Sísmico")
            self.vista_lista.tkraise()
        elif vista_a_mostrar == 'detalle':
            self.master.title(f"Revisión del Evento: {self.sismo_seleccionado_id}")
            self.vista_detalle.tkraise()

    def _crear_widgets_menu(self):
        """
        CORRECCIÓN: Menú principal según anotaciones del PDF
        "Se selecciona el botón registrar resultado de revisión manual
        Y ahí recien se habilita la ventana de selección de evento sismico"
        """
        label = ttk.Label(self.vista_menu, text="Menú Principal", font=("Helvetica", 16, "bold"))
        label.pack(pady=20)
        
        btn_registrar = ttk.Button(
            self.vista_menu, 
            text="Registrar Resultado de Revisión Manual", 
            command=self.seleccionarOpcionRegistrarResultadoDeRevisionManual
        )
        btn_registrar.pack(pady=10, padx=50, ipady=10, fill="x")

    def _crear_widgets_lista(self):
        """Vista de lista de eventos sísmicos pendientes de revisión"""
        frame_lista = ttk.LabelFrame(self.vista_lista, text="Sismos No Revisados")
        frame_lista.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.tree_sismos = ttk.Treeview(
            frame_lista, 
            columns=("ID", "Fecha", "Magnitud", "Estado"), 
            show="headings"
        )
        self.tree_sismos.heading("ID", text="ID")
        self.tree_sismos.heading("Fecha", text="Fecha/Hora")
        self.tree_sismos.heading("Magnitud", text="Magnitud")
        self.tree_sismos.heading("Estado", text="Estado Actual")
        self.tree_sismos.pack(pady=5, padx=5, fill="both", expand=True)
        self.tree_sismos.bind("<<TreeviewSelect>>", self.on_sismo_select)
        
        frame_botones = ttk.Frame(self.vista_lista)
        frame_botones.pack(pady=10, padx=10, fill="x")
        
        self.btn_seleccionar = ttk.Button(
            frame_botones, 
            text="Seleccionar Sismo", 
            state="disabled", 
            command=self.tomarSeleccionEventoSismico
        )
        self.btn_seleccionar.pack(side="right", padx=5)
        
        btn_volver = ttk.Button(
            frame_botones, 
            text="Volver al Menú", 
            command=lambda: self._mostrar_vista('menu')
        )
        btn_volver.pack(side="left", padx=5)

    def _crear_widgets_detalle(self):
        """Vista de detalle con información completa del evento y opciones de acción"""
        frame_detalles = ttk.LabelFrame(self.vista_detalle, text="Detalles del Evento y Acciones")
        frame_detalles.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.lbl_detalles = ttk.Label(
            frame_detalles, 
            text="", 
            font=("Helvetica", 10), 
            justify=tk.LEFT, 
            anchor="nw"
        )
        self.lbl_detalles.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.frame_acciones = ttk.LabelFrame(self.vista_detalle, text="Tomar una Acción")
        self.frame_acciones.pack(pady=10, padx=10, fill="x")
        
        self.btn_confirmar = ttk.Button(
            self.frame_acciones, 
            text="Confirmar Evento",
            command=self.tomarSeleccionConfirmacion
        )
        self.btn_confirmar.pack(side="right", padx=5, pady=5)
        
        self.btn_rechazar = ttk.Button(
            self.frame_acciones, 
            text="Rechazar Evento", 
            command=self.tomarSeleccionRechazo
        )
        self.btn_rechazar.pack(side="right", padx=5, pady=5)
        
        self.btn_derivar = ttk.Button(
            self.frame_acciones, 
            text="Solicitar Revisión a Experto",
            command=self.tomarSeleccionDerivacion
        )
        self.btn_derivar.pack(side="right", padx=5, pady=5)
        
        btn_volver = ttk.Button(
            self.vista_detalle, 
            text="Volver a la Lista", 
            command=lambda: self._mostrar_vista('lista')
        )
        btn_volver.pack(pady=10)

    def habilitarVentana(self):
        """
        SEGÚN DIAGRAMA: :PantallaGestionRegistroResultadoRevisionManual → :PantallaGestionRegistroResultadoRevisionManual (self): habilitarVentana()
        SEGÚN ANOTACIONES PDF: "que muestre el MENU PRINCIPAL directamente"
        """
        print("** PANTALLA: habilitarVentana() **")
        self._mostrar_vista('menu')

    def seleccionarOpcionRegistrarResultadoDeRevisionManual(self):
        """
        SEGÚN DIAGRAMA: :AnalistaEnSismos → :PantallaGestionRegistroResultadoRevisionManual: seleccionarOpciónRegistrarResultadoDeRevisiónManual()
        LUEGO: :PantallaGestionRegistroResultadoRevisionManual → :GestorRegistroResultradoRevisionManual: buscarSismosAutoDetectradosYPendienteDeRevision()
        """
        print("** PANTALLA: seleccionarOpcionRegistrarResultadoDeRevisionManual() **")
        print("** PANTALLA: Analista seleccionó 'Registrar Resultado de Revisión Manual' **")
        
        # SEGÚN DIAGRAMA: llamar al gestor para buscar sismos
        self.gestor.buscarSismosAutoDetectadosYPendienteDeRevision()

    def mostrarEventosSismicosEncontradosOrdenados(self, lista_sismos):
        """
        SEGÚN DIAGRAMA: GestorRegistroResultadoRevisionManual → :PantallaGestionRegistroResultadoRevisionManual: mostrarEventosSismicosEncontradosOrdenados()
        """
        print("** PANTALLA: mostrarEventosSismicosEncontradosOrdenados() **")
        print("** PANTALLA: El Gestor me ordenó mostrar los sismos encontrados **")
        
        self.btn_seleccionar.config(state="disabled")
        
        # Limpiar la tabla
        for i in self.tree_sismos.get_children(): 
            self.tree_sismos.delete(i)
        
        # Cargar los sismos encontrados
        for sismo in lista_sismos:
            self.tree_sismos.insert(
                "", 
                "end", 
                values=(
                    sismo.id_sismo, 
                    sismo.fechaHoraOcurrencia.strftime("%Y-%m-%d %H:%M"), 
                    sismo.valorMagnitud, 
                    sismo.estadoActual.actual.nombre
                )
            )
        
        self._mostrar_vista('lista')

    def solicitarSeleccionEventoSismico(self):
        """
        SEGÚN DIAGRAMA: GestorRegistroResultadoRevisionManual → :PantallaGestionRegistroResultadoRevisionManual: solicitarSeleccionEventoSismico()
        """
        print("** PANTALLA: solicitarSeleccionEventoSismico() **")
        print("** PANTALLA: El Gestor me ordenó solicitar una selección **")
        
        messagebox.showinfo(
            "Siguiente Paso", 
            "Se encontraron sismos. Por favor, seleccione uno y presione 'Seleccionar Sismo'."
        )
        
    def on_sismo_select(self, event):
        """Maneja la selección de un sismo en la tabla"""
        selected_item = self.tree_sismos.selection()
        if selected_item:
            self.sismo_seleccionado_id = self.tree_sismos.item(selected_item)['values'][0]
            self.btn_seleccionar.config(state="normal")

    def tomarSeleccionEventoSismico(self):
        """
        SEGÚN DIAGRAMA: :AnalistaEnSismos → :PantallaGestionRegistroResultadoRevisionManual: tomarSeleccionEventoSismico()
        LUEGO: :PantallaGestionRegistroResultadoRevisionManual: → GestorRegistroResultradoRevisionManual: tomarSeleccionEventoSismico()
        """
        if self.sismo_seleccionado_id:
            print(f"** PANTALLA: tomarSeleccionEventoSismico({self.sismo_seleccionado_id}) **")
            print(f"** PANTALLA: Enviando selección de sismo {self.sismo_seleccionado_id} al gestor **")
            
            # SEGÚN DIAGRAMA: enviar selección al gestor
            self.gestor.tomarSeleccionEventoSismico(self.sismo_seleccionado_id)

    def mostrarDatosEventoSismicoSeleccionado(self, sismo):
        """
        SEGÚN DIAGRAMA: GestorRegistroResultadoRevisionManual → :PantallaGestionRegistroResultadoRevisionManual: mostrarDatosEventoSismicoSeleccionado()
        """
        print(f"** PANTALLA: mostrarDatosEventoSismicoSeleccionado({sismo.id_sismo}) **")
        
        sismo_info = sismo.getDatosEventoSismico()
        texto = (
            f"ID: {sismo_info['ID']}\n"
            f"Fecha/Hora: {sismo_info['Fecha/Hora'].strftime('%Y-%m-%d %H:%M')}\n"
            f"Magnitud: {sismo_info['Magnitud']}\n"
            f"Estado Actual: {sismo.estadoActual.actual.nombre}\n\n"
            f"--- Coordenadas ---\n"
            f"Latitud Epicentro: {sismo_info['LatitudEpicentro']}\n"
            f"Longitud Epicentro: {sismo_info['LongitudEpicentro']}\n"
            f"Latitud Hipocentro: {sismo_info['LatitudHipocentro']}\n"
            f"Longitud Hipocentro: {sismo_info['LongitudHipocentro']}\n\n"
            f"--- Detalles Adicionales ---\n"
            f"Alcance: {sismo.getAlcance()}\n"
            f"Clasificación: {sismo.getClasificacion()}\n"
            f"Origen: {sismo.getOrigen()}\n"
        )
        
        self.lbl_detalles.config(text=texto)
        self._mostrar_vista('detalle')

    def habilitarOpcionVisualizacionMapaConEstacionesSismologicasInvolucradas(self):
        """
        SEGÚN DIAGRAMA: GestorRegistroResultradoRevisionManual → :PantallaGestionRegistroResultradoRevisionManual: habilitarOpcionVisualizacionMapaConEstacionesSismologicasInvolucradas()
        """
        print("** PANTALLA: habilitarOpcionVisualizacionMapaConEstacionesSismologicasInvolucradas() **")
        
        # Continuar con el flujo según el diagrama
        self.tomarSeleccionDeNoVisualizacionMapa()

    def tomarSeleccionDeNoVisualizacionMapa(self):
        """
        SEGÚN DIAGRAMA: :AnalistaEnSismos → :PantallaGestionRegistroResultradoRevisionManual: tomarSeleccionDeNoVisualizacionMapa()
        """
        print("** PANTALLA: tomarSeleccionDeNoVisualizacionMapa() **")
        
        if not messagebox.askyesno("Visualizar Mapa", "¿Desea visualizar en mapa el evento?"):
            print("** PANTALLA: Usuario seleccionó NO visualizar el mapa **")
            self.consultarModificacionDatos()
        else:
            print("** PANTALLA: Usuario desea ver el mapa (funcionalidad no implementada) **")
            self.consultarModificacionDatos()

    def consultarModificacionDatos(self):
        """
        SEGÚN DIAGRAMA: GestorRegistroResultadoRevisionManual → :PantallaGestionRegistroResultradoRevisionManual: consultarModificacionDatos()
        """
        print("** PANTALLA: consultarModificacionDatos() **")
        
        if not messagebox.askyesno("Modificar Datos", "¿Desea modificar los datos del evento sísmico?"):
            print("** PANTALLA: Usuario seleccionó NO modificar datos **")
            self.tomarSeleccionDeNoModificacion()
        else:
            print("** PANTALLA: Usuario desea modificar datos (funcionalidad no implementada) **")
            self.tomarSeleccionDeNoModificacion()

    def tomarSeleccionDeNoModificacion(self):
        """
        SEGÚN DIAGRAMA: :AnalistaEnSismos → :PantallaGestionRegistroResultradoRevisionManual: tomarSeleccionDeNoModificacion()
        """
        print("** PANTALLA: tomarSeleccionDeNoModificacion() **")
        
        # Continuar con la solicitud de confirmación según el diagrama
        self.gestor.solicitarConfirmacionDeRevision()

    def solicitarConfirmarRechazarRevisarEvento(self):
        """
        SEGÚN DIAGRAMA: GestorRegistroResultradoRevisionManual → :PantallaGestionRegistroResultradoRevisionManual: solicitarConfirmarRechazarRevisarEvento()
        """
        print("** PANTALLA: solicitarConfirmarRechazarRevisarEvento() **")
        print("** PANTALLA: El Gestor me ordenó habilitar las opciones finales **")
        
        # Asegurar que el frame de acciones esté visible
        self.frame_acciones.pack_forget()
        self.frame_acciones.pack(pady=10, padx=10, fill="x")
        
        messagebox.showinfo("Acción Requerida", "Por favor, seleccione una acción final para el evento.")
        
    def tomarSeleccionConfirmacion(self):
        """
        SEGÚN DIAGRAMA: :AnalistaEnSismos → :PantallaGestionRegistroResultradoRevisionManual: tomarSeleccionConfirmacion()
        (Aunque en el diagrama no aparece explícitamente, es parte del flujo lógico)
        """
        if messagebox.askyesno("Confirmar Evento", "¿Está seguro de que desea CONFIRMAR este evento como sismo válido?"):
            print("** PANTALLA: tomarSeleccionConfirmacion() **")
            print("** PANTALLA: Usuario confirmó el evento **")
            self.gestor.tomarSeleccionConfirmacion()

    def tomarSeleccionRechazo(self):
        """
        SEGÚN DIAGRAMA: :AnalistaEnSismos → :PantallaGestionRegistroResultradoRevisionManual: tomarSeleccionRechazo()
        LUEGO: :PantallaGestionRegistroResultradoRevisionManual: → GestorRegistroResultradoRevisionManual: tomarSeleccionRechazo()
        """
        if messagebox.askyesno("Confirmar Rechazo", "¿Está seguro de que desea RECHAZAR la revisión?"):
            print("** PANTALLA: tomarSeleccionRechazo() **")
            print("** PANTALLA: Usuario confirmó el rechazo **")
            
            # SEGÚN DIAGRAMA: enviar la selección de rechazo al gestor
            self.gestor.tomarSeleccionRechazo()

    def tomarSeleccionDerivacion(self):
        """Procesa la derivación del evento a un experto."""
        if messagebox.askyesno("Derivar a Experto", "¿Está seguro de que desea derivar este evento a un experto?"):
            print("** PANTALLA: tomarSeleccionDerivacion() **")
            print("** PANTALLA: Usuario confirmó la derivación **")
            self.gestor.tomarSeleccionDerivacion()

    def finCU(self):
        """
        CORRECCIÓN: Finaliza el caso de uso según el diagrama
        Resetea la selección y recarga la lista de eventos.
        """
        print("** PANTALLA: finCU() **")
        print("** PANTALLA: Finalizando caso de uso **")
        
        # Resetear la selección
        self.sismo_seleccionado_id = None
        
        messagebox.showinfo(
            "Proceso Finalizado", 
            "El evento ha sido procesado. Volviendo a la lista de sismos."
        )
        
        # Recargar la lista de sismos para reflejar los cambios
        self.gestor.buscarSismosAutoDetectadosYPendienteDeRevision()