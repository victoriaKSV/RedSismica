import json
from datetime import datetime
from modelos.evento_sismico import EventoSismico
from modelos.sesion import Sesion
from casos_de_uso.generar_sismograma import SismogramaGenerator

class GestorRegistroResultadoRevisionManual:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.eventos_sismicos_en_memoria = []
        self.seleccionado = None
        self._cargar_datos_desde_json()
        print("-> Creada instancia del Gestor con referencia a la Pantalla.")

    def _cargar_datos_desde_json(self):
        try:
            with open("sismos.json", "r", encoding="utf-8") as f: 
                data = json.load(f)
            for sismo_data in data:
                self.eventos_sismicos_en_memoria.append(EventoSismico(
                    id_sismo=sismo_data["id_sismo"],
                    fecha=datetime.fromisoformat(sismo_data["fecha_hora_ocurrencia"]),
                    magnitud=sismo_data["valor_magnitud"],
                    estado_inicial=sismo_data["estado_inicial"],
                    series_data=sismo_data.get("series_temporales", [])
                ))
        except FileNotFoundError: 
            print(">> GESTOR: ADVERTENCIA - No se encontró 'sismos.json'.")
        except Exception as e: 
            print(f">> GESTOR: ERROR al cargar 'sismos.json': {e}")

    def buscarSismosAutoDetectadosYPendienteDeRevision(self):
        print("\n>> GESTOR: Buscando sismos auto-detectados y pendientes de revisión...")
        
        # Loop Para Todos Los Eventos Sísmicos (mientras haya eventos sísmicos)
        sismos_filtrados = []
        
        for evento_sismico in self.eventos_sismicos_en_memoria:
            print(f">> GESTOR: Procesando evento {evento_sismico.id_sismo}")
            print(f"   -> Estado actual: {evento_sismico.estadoActual.actual.nombre}")
            
            # Solo procesar sismos que NO estén rechazados, bloqueados o confirmados
            estado_actual = evento_sismico.estadoActual.actual.nombre
            if estado_actual in ["Rechazado", "Confirmado", "Bloqueado en Revisión"]:
                print(f"   -> Evento {evento_sismico.id_sismo} excluido por estar en estado '{estado_actual}'")
                continue
            
            # 1. Chequeo "AutoDetectado"
            if evento_sismico.estaEnEstadoAutoDetectado():
                print(f"   -> Evento {evento_sismico.id_sismo} está en estado Auto-Detectado")
                # 3. Datos del evento
                datos_evento = evento_sismico.getDatosEventoSismico()
                sismos_filtrados.append(evento_sismico)
            
            # 2. Chequeo "PendienteDeRevision"
            elif evento_sismico.estaEnEstadoPendienteDeRevisión():
                print(f"   -> Evento {evento_sismico.id_sismo} está en estado Pendiente de Revisión")
                # 3. Datos del evento
                datos_evento = evento_sismico.getDatosEventoSismico()
                sismos_filtrados.append(evento_sismico)
                
            else:
                print(f"   -> Evento {evento_sismico.id_sismo} no cumple criterios de filtrado")
        
        # FUERA DEL LOOP
        print(f">> GESTOR: Se encontraron {len(sismos_filtrados)} eventos que cumplen los criterios")
        
        # Ordenar los eventos encontrados
        eventos_ordenados = self.ordenarEventosSismicosPorFechaYHora(sismos_filtrados)
        
        # Mostrar los eventos en la pantalla
        self.pantalla.mostrarEventosSismicosEncontradosOrdenados(eventos_ordenados)
        
        # Solicitar selección
        self.pantalla.solicitarSeleccionEventoSismico()

    def ordenarEventosSismicosPorFechaYHora(self, eventos):
        eventos.sort(key=lambda x: x.getFechaHoraOcurrencia(), reverse=True)
        return eventos

    def tomarSeleccionEventoSismico(self, id_sismo: str):
        print(f"\n>> GESTOR: La pantalla informó la selección del sismo ID: {id_sismo}")
        
        # Buscar el sismo seleccionado
        for sismo in self.eventos_sismicos_en_memoria:
            if sismo.id_sismo == id_sismo:
                self.seleccionado = sismo
                break
        
        if not self.seleccionado:
            print(f">> GESTOR: ERROR - No se encontró el sismo {id_sismo}")
            return
            
        # Según el diagrama: cambiarEventoSismicoSeleccionadoABloqueadoEnRevision()
        self.cambiarEventoSismicoSeleccionadoABloqueadoEnRevision()
        
        # Según el diagrama: buscarDatosSismicosRegistradosParaElEventoSísmicoSeleccionado()
        self.buscarDatosSismicosRegistradosParaElEventoSismicoSeleccionado()
        
        # Según el diagrama: mostrarDatosEventoSismicoSeleccionado()
        self.pantalla.mostrarDatosEventoSismicoSeleccionado(self.seleccionado)
        
        # Según el diagrama: obtenerValoresAlcanzadosDeSeriesTemporales()
        self.obtenerValoresAlcanzadosDeSeriesTemporales()

    def cambiarEventoSismicoSeleccionadoABloqueadoEnRevision(self):
        print(">> GESTOR: Cambiando evento seleccionado a 'Bloqueado en Revisión'")
        
        if not self.seleccionado:
            return
            
        # Según el diagrama: GestorRegistroResultadoRevisionManual → :Estado: *sosBloqueadoEnRevision() (loop)
        # Verificar primero si ya está bloqueado
        for estado in self.seleccionado.historial_estados:
            if estado.actual.nombre == "Bloqueado en Revisión" and estado.esEstadoActual():
                print(">> GESTOR: El evento ya está bloqueado en revisión")
                return
        
        # Cambiar estado del evento seleccionado
        self.seleccionado.cambiarEstadoEventoSismicoABloqueadoEnRevision()

    def buscarDatosSismicosRegistradosParaElEventoSismicoSeleccionado(self):
        print(">> GESTOR: Buscando datos sísmicos registrados para el evento seleccionado")
        
        if not self.seleccionado:
            return
            
        # Según el diagrama: GestorRegistroResultadoRevisionManual → seleccionado:EventoSismico: getDatosSismicosRegistradosParaEventoSísmicoSeleccionado()
        self.seleccionado.getDatosSismicosRegistradosParaEventoSismicoSeleccionado()

    def obtenerValoresAlcanzadosDeSeriesTemporales(self):
        print(">> GESTOR: Obteniendo valores de series temporales...")
        
        if not self.seleccionado or not self.seleccionado.series_temporales:
            print(">> GESTOR: No hay series temporales para procesar")
            return
            
        # Según el diagrama: GestorRegistroResultadoRevisionManual → seleccionado:EventoSismico: getDatosSismicosRegistradosParaEventoSísmicoSeleccionado()
        self.seleccionado.getDatosSismicosRegistradosParaEventoSismicoSeleccionado()
        
        # Loop (para todas las series temporales)
        for serie_temporal in self.seleccionado.series_temporales:
            print(f">> GESTOR: Procesando serie temporal")
            
            # seleccionado:EventoSismico → seleccionado:EventoSismico: getValoresAlcanzadosPorCadaInstanteDeTiempo()
            self.seleccionado.getValoresAlcanzadosPorCadaInstanteDeTiempo()
            
            # seleccionado:EventoSismico → :SerieTemporal: *getDatos()
            datos_serie = serie_temporal.getDatos()
            
            # Loop (para todas las muestras sísmicas)
            for muestra_sismica in serie_temporal.muestras:
                print(f">> GESTOR: Procesando muestra sísmica")
                
                # :SerieTemporal → :MuestraSismica: *getDatos()
                datos_muestra = muestra_sismica.getDatos()
                
                # Loop (para todos los detalles de la muestra sísmica)
                for detalle_muestra in muestra_sismica.detalles:
                    print(f">> GESTOR: Procesando detalle de muestra")
                    
                    # :MuestraSismica → :DetalleMuestraSismica: *getDatos()
                    datos_detalle = detalle_muestra.getDatos()
                    
                    # :DetalleMuestraSismica → :TipoDeDatos: esVelocidadDeOnda(), esFrecuenciaDeOnda(), esLongitud()
                    tipo_dato = detalle_muestra.getTipoDeDato()
                    es_velocidad = tipo_dato.esVelocidadDeOnda()
                    es_frecuencia = tipo_dato.esFrecuenciaDeOnda()
                    es_longitud = tipo_dato.esLongitud()
                    
                    # :TipoDeDatos: → :TipoDeDatos: getDenominacion()
                    denominacion = tipo_dato.getDenominacion()
                    
            # seleccionado:EventoSismico → seleccionado:EventoSismico: esDeEstacionSismologica()
            es_de_estacion = self.seleccionado.esDeEstacionSismologica()
            
            # seleccionado:EventoSismico → :Sismografo: *sosDeSismografo()
            # :Sismografo → :Sismografo: getEstacionSismologica()
            # :Sismografo → :EstacionSismologica: getCodigoEstacion()
            # (Estos se implementarían si hay sismógrafos asociados)
        
        # FUERA DEL LOOP DE LAS SERIES TEMPORALES
        print(">> GESTOR: Finalizando procesamiento de series temporales")
        
        # GestorRegistroResultadoRevisionManual → GestorRegistroResultadoRevisionManual: clasificarMuestrasPorEstacionSismologica()
        self.clasificarMuestrasPorEstacionSismologica()
        
        # GestorRegistroResultadoRevisionManual → GestorRegistroResultadoRevisionManual: llamarAlCasoDeUsoGenerarSismograma()
        self.llamarAlCasoDeUsoGenerarSismograma()
        
        # GestorRegistroResultadoRevisionManual → :PantallaGestionRegistroResultadoRevisionManual: habilitarOpcionVisualizacionMapaConEstacionesSismologicasInvolucradas()
        self.pantalla.habilitarOpcionVisualizacionMapaConEstacionesSismologicasInvolucradas()

    def clasificarMuestrasPorEstacionSismologica(self):
        """Clasificar muestras por estación sismológica"""
        print(">> GESTOR: Clasificando muestras por estación sismológica")
        # Implementación específica según necesidades del sistema
        
    def solicitarConfirmacionDeRevision(self):
        """
        NUEVO MÉTODO: El gestor le pide a la pantalla que solicite las acciones finales.
        Esto se llama después de que el usuario responde a los carteles de mapa y modificación.
        """
        print(">> GESTOR: Solicitando a la pantalla que muestre las opciones finales de revisión.")
        self.pantalla.solicitarConfirmarRechazarRevisarEvento()

    def tomarSeleccionRechazo(self):
        print("\n>> GESTOR: Se ha tomado la selección de RECHAZAR.")
        if self.validarDatosEvento():
            self.cambiarEventoSismicoARechazado()
            self.finCU()
            
    def llamarAlCasoDeUsoGenerarSismograma(self):
        print(">> GESTOR: Llamando al CU 'Generar Sismograma'...")
        if self.seleccionado:
            SismogramaGenerator.generar_y_mostrar(self.seleccionado)
        
    def validarDatosEvento(self) -> bool:
        if not self.seleccionado: 
            return False
        print(">> GESTOR: Validando datos del evento.")
        self.seleccionado.validarDatosSismo()
        self.validarSeleccionConfirmacion()
        return True

    def validarSeleccionConfirmacion(self):
        print(">> GESTOR: Validando selección y registrando auditoría.")
        self.obtenerFechaHoraActual()
        self.obtenerEmpleadoSesion()

    def obtenerFechaHoraActual(self):
        print(f">> GESTOR: Obteniendo fecha y hora actual: {datetime.now()}")
        return datetime.now()

    def obtenerEmpleadoSesion(self):
        empleado = Sesion().getEmpleado()
        print(f">> GESTOR: Empleado en sesión: {empleado}")
        return empleado

    def cambiarEventoSismicoARechazado(self):
        if self.seleccionado:
            self.seleccionado.cambiarEventoSismicoARechazado()

    def finCU(self):
        print("\n>> GESTOR: Fin del Caso de Uso para este evento.")
        self.pantalla.finCU()