# gui/pantallaGestionRegistroResultadoRevisionManual.py

import tkinter as tk
from tkinter import ttk, messagebox
from gestor.gestorRegistroResultadoRevisionManual import GestorRegistroResultadoRevisionManual

class PantallaGestionRegistroResultadoRevisionManual(tk.Frame):
    """
    NOTA DE TARJETA AZUL - Interfaz Principal:
    ==========================================
    Esta pantalla maneja tres vistas principales:
    1. MENÚ PRINCIPAL: Muestra las opciones disponibles
    2. LISTA DE EVENTOS: Muestra eventos filtrados para revisión
    3. DETALLE DEL EVENTO: Muestra información completa y opciones de acción
    
    El analista sigue este flujo:
    - Selecciona opción del menú
    - Ve lista de eventos pendientes
    - Selecciona un evento
    - Revisa detalles y toma acción
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

        # Llamar a habilitarVentana() según el diagrama
        self.habilitarVentana()

    def _mostrar_vista(self, vista_a_mostrar):
        """
        NOTA: Cambia entre las diferentes vistas de la aplicación
        """
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
        NOTA DE TARJETA AZUL: 
        El analista selecciona "REGISTRAR RESULTADO DE REVISION MANUAL"
        Esta es la opción principal del caso de uso
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
        """
        NOTA DE TARJETA VIOLETA:
        Muestra la lista de eventos sísmicos pendientes de revisión
        con ID, Fecha/Hora, Magnitud y Estado Actual
        """
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
        """
        Vista de detalle con información completa del evento y opciones de acción
        """
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
        Método que habilita la ventana según el diagrama de secuencia
        Muestra el menú principal al inicio
        """
        print("** PANTALLA: Habilitando ventana principal **")
        self._mostrar_vista('menu')

    def seleccionarOpcionRegistrarResultadoDeRevisionManual(self):
        """
        NOTA DE TARJETA AZUL:
        El analista selecciona la opción "Registrar Resultado de Revisión Manual"
        desde el menú principal. Esto inicia el caso de uso.
        """
        print("** PANTALLA: Analista seleccionó 'Registrar Resultado de Revisión Manual' **")
        self.gestor.buscarSismosAutoDetectadosYPendienteDeRevision()

    def mostrarEventosSismicosEncontradosOrdenados(self, lista_sismos):
        """
        NOTA DE TARJETA VIOLETA:
        Los eventos se muestran ordenados por fecha/hora.
        Se incluye ID, Fecha/Hora, Magnitud y Estado Actual.
        """
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
        NOTA DE TARJETA AZUL:
        Solicita al analista que seleccione un evento de la lista.
        """
        print("** PANTALLA: El Gestor me ordenó solicitar una selección **")
        messagebox.showinfo(
            "Siguiente Paso", 
            "Se encontraron sismos. Por favor, seleccione uno y presione 'Seleccionar Sismo'."
        )
        
    def on_sismo_select(self, event):
        """
        Maneja la selección de un sismo en la tabla
        """
        selected_item = self.tree_sismos.selection()
        if selected_item:
            self.sismo_seleccionado_id = self.tree_sismos.item(selected_item)['values'][0]
            self.btn_seleccionar.config(state="normal")

    def tomarSeleccionEventoSismico(self):
        """
        NOTA DE TARJETA AZUL:
        Envía la selección del evento al gestor.
        El evento seleccionado será bloqueado para revisión.
        """
        if self.sismo_seleccionado_id:
            print(f"** PANTALLA: Enviando selección de sismo {self.sismo_seleccionado_id} al gestor **")
            self.gestor.tomarSeleccionEventoSismico(self.sismo_seleccionado_id)

    def mostrarDatosEventoSismicoSeleccionado(self, sismo):
        """
        NOTA DE TARJETA VIOLETA:
        Muestra todos los datos del evento sísmico seleccionado:
        - Información básica (ID, Fecha/Hora, Magnitud)
        - Coordenadas del epicentro e hipocentro
        - Alcance, Clasificación y Origen
        - Estado actual
        """
        print(f"** PANTALLA: Mostrando datos del evento sísmico seleccionado {sismo.id_sismo} **")
        
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
        NOTA DE TARJETA VIOLETA:
        Habilita la opción de visualizar el evento en un mapa
        con las estaciones sismológicas involucradas.
        """
        print("** PANTALLA: Habilitando opción de visualización de mapa con estaciones sismológicas **")
        
        # Continuar con el flujo interactivo después del procesamiento
        self.tomarSeleccionDeNoVisualizacionMapa()

    def tomarSeleccionDeNoVisualizacionMapa(self):
        """
        NOTA DE TARJETA VIOLETA:
        Gestiona la decisión del usuario sobre visualizar el mapa.
        Si no desea ver el mapa, continúa con la consulta de modificación.
        """
        print("** PANTALLA: tomarSeleccionDeNoVisualizacionMapa() **")
        if not messagebox.askyesno("Visualizar Mapa", "¿Desea visualizar en mapa el evento?"):
            print("** PANTALLA: Usuario seleccionó NO visualizar el mapa **")
            self.consultarModificacionDatos()
        else:
            # NOTA: Aquí iría la lógica para mostrar el mapa
            print("** PANTALLA: Usuario desea ver el mapa (funcionalidad no implementada) **")
            self.consultarModificacionDatos()

    def consultarModificacionDatos(self):
        """
        NOTA DE TARJETA VIOLETA:
        Consulta si el usuario desea modificar los datos del evento.
        """
        print("** PANTALLA: consultarModificacionDatos() **")
        if not messagebox.askyesno("Modificar Datos", "¿Desea modificar los datos del evento sísmico?"):
            print("** PANTALLA: Usuario seleccionó NO modificar datos **")
            self.tomarSeleccionDeNoModificacion()
        else:
            # NOTA: Aquí iría la lógica para la modificación
            print("** PANTALLA: Usuario desea modificar datos (funcionalidad no implementada) **")
            self.tomarSeleccionDeNoModificacion()

    def tomarSeleccionDeNoModificacion(self):
        """
        Procesar selección de no modificación según el diagrama
        """
        print("** PANTALLA: tomarSeleccionDeNoModificacion() **")
        self.gestor.solicitarConfirmacionDeRevision()

    def solicitarConfirmarRechazarRevisarEvento(self):
        """
        NOTA DE TARJETA VIOLETA:
        Muestra las opciones finales para el evento:
        - Confirmar: Valida el evento como sismo real
        - Rechazar: Marca como falso positivo
        - Derivar: Solicita revisión de experto
        """
        print("** PANTALLA: El Gestor me ordenó habilitar las opciones finales **")
        
        # Asegurar que el frame de acciones esté visible
        self.frame_acciones.pack_forget()
        self.frame_acciones.pack(pady=10, padx=10, fill="x")
        
        messagebox.showinfo("Acción Requerida", "Por favor, seleccione una acción final para el evento.")
        
    def tomarSeleccionConfirmacion(self):
        """
        NOTA DE TARJETA VIOLETA:
        Procesa la confirmación del evento como sismo válido.
        """
        if messagebox.askyesno("Confirmar Evento", "¿Está seguro de que desea CONFIRMAR este evento como sismo válido?"):
            print("** PANTALLA: Usuario confirmó el evento **")
            self.gestor.tomarSeleccionConfirmacion()

    def tomarSeleccionRechazo(self):
        """
        NOTA DE TARJETA VIOLETA:
        Procesa el rechazo del evento (falso positivo).
        Solicita confirmación antes de proceder.
        """
        if messagebox.askyesno("Confirmar Rechazo", "¿Está seguro de que desea RECHAZAR la revisión?"):
            print("** PANTALLA: Usuario confirmó el rechazo **")
            self.gestor.tomarSeleccionRechazo()

    def tomarSeleccionDerivacion(self):
        """
        NOTA DE TARJETA VIOLETA:
        Procesa la derivación del evento a un experto.
        """
        if messagebox.askyesno("Derivar a Experto", "¿Está seguro de que desea derivar este evento a un experto?"):
            print("** PANTALLA: Usuario confirmó la derivación **")
            self.gestor.tomarSeleccionDerivacion()

    def finCU(self):
        """
        NOTA DE TARJETA AZUL:
        Finaliza el caso de uso actual.
        Resetea la selección y recarga la lista de eventos.
        """
        print("** PANTALLA: Finalizando caso de uso **")
        
        # Resetear la selección
        self.sismo_seleccionado_id = None
        
        messagebox.showinfo(
            "Proceso Finalizado", 
            "El evento ha sido procesado. Volviendo a la lista de sismos."
        )
        
        # Recargar la lista de sismos para reflejar los cambios
        self.gestor.buscarSismosAutoDetectadosYPendienteDeRevision()