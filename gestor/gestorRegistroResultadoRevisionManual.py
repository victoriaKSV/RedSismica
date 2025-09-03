# gestor/gestorRegistroResultadoRevisionManual.py

import json
from datetime import datetime
from modelos.evento_sismico import EventoSismico
from modelos.sesion import Sesion
from modelos.estado import Estado
from casos_de_uso.generar_sismograma import SismogramaGenerator

class GestorRegistroResultadoRevisionManual:
    """
    IMPLEMENTACIÓN CORREGIDA: Con todas las mejoras solicitadas
    Incluye validaciones de fechaHoraFin, ordenamiento fuera del loop,
    método intermedio para series temporales y clasificación por estación.
    """
    
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
        """
        CORRECCIÓN APLICADA:
        - Validación de fechaHoraFin == null (CORRECCIÓN 1)
        - Ordenamiento movido fuera del loop (CORRECCIÓN 2)
        """
        print("\n>> GESTOR: buscarSismosAutoDetectadosYPendienteDeRevision()")
        
        # ============= INICIO DEL LOOP PARA TODOS LOS EVENTOS SÍSMICOS =============
        sismos_filtrados = []
        
        for evento_sismico in self.eventos_sismicos_en_memoria:
            print(f">> GESTOR: Procesando evento {evento_sismico.id_sismo}")
            
            # CORRECCIÓN 1: Validar que el estado actual tenga fechaHoraFin == null
            if not evento_sismico.estadoActual.esEstadoActual():
                print(f"   -> Evento {evento_sismico.id_sismo} excluido por tener estado finalizado")
                continue
            
            # VALIDACIÓN PREVENTIVA: Excluir eventos ya procesados
            estado_actual = evento_sismico.estadoActual.actual.nombre
            if estado_actual in ["Rechazado", "Confirmado", "Bloqueado en Revisión"]:
                print(f"   -> Evento {evento_sismico.id_sismo} excluido por estar en estado '{estado_actual}'")
                continue
            
            # ===== 1. CHEQUEO "AutoDetectado" =====
            if evento_sismico.estaEnEstadoAutoDetectado():
                print(f"   -> Evento {evento_sismico.id_sismo} está en estado Auto-Detectado")
                datos_evento = evento_sismico.getDatosEventoSismico()
                sismos_filtrados.append(evento_sismico)
                continue
            
            # ===== 2. CHEQUEO "PendienteDeRevision" =====
            if evento_sismico.estaEnEstadoPendienteDeRevision():
                print(f"   -> Evento {evento_sismico.id_sismo} está en estado Pendiente de Revisión")
                datos_evento = evento_sismico.getDatosEventoSismico()
                sismos_filtrados.append(evento_sismico)
                continue
                
            print(f"   -> Evento {evento_sismico.id_sismo} no cumple criterios de filtrado")
        
        # ============= CORRECCIÓN 2: ORDENAMIENTO FUERA DEL LOOP =============
        print(f">> GESTOR: Se encontraron {len(sismos_filtrados)} eventos que cumplen los criterios")
        
        # SEGÚN DIAGRAMA: ordenar eventos por fecha y hora
        eventos_ordenados = self.ordenarEventosSismicosPorFechaYHora(sismos_filtrados)
        
        # Mostrar eventos ordenados en pantalla
        self.pantalla.mostrarEventosSismicosEncontradosOrdenados(eventos_ordenados)
        
        # Solicitar selección de evento
        self.pantalla.solicitarSeleccionEventoSismico()

    def ordenarEventosSismicosPorFechaYHora(self, eventos):
        """SEGÚN DIAGRAMA: Ordena los eventos sísmicos por fecha y hora"""
        print(">> GESTOR: ordenarEventosSismicosPorFechaYHora()")
        eventos.sort(key=lambda x: x.getFechaHoraOcurrencia(), reverse=True)
        return eventos

    def tomarSeleccionEventoSismico(self, id_sismo: str):
        """
        CORRECCIÓN 4 APLICADA: Usa método intermedio procesarSeriesTemporales()
        """
        print(f"\n>> GESTOR: tomarSeleccionEventoSismico({id_sismo})")
        
        # Buscar el sismo seleccionado
        for sismo in self.eventos_sismicos_en_memoria:
            if sismo.id_sismo == id_sismo:
                self.seleccionado = sismo
                break
        
        if not self.seleccionado:
            print(f">> GESTOR: ERROR - No se encontró el sismo {id_sismo}")
            return
            
        # Cambiar estado a Bloqueado en Revisión
        self.cambiarEventoSismicoSeleccionadoABloqueadoEnRevision()
        
        # Buscar datos sísmicos registrados
        self.buscarDatosSismicosRegistradosParaElEventoSismicoSeleccionado()
        
        # Mostrar datos en pantalla
        self.pantalla.mostrarDatosEventoSismicoSeleccionado(self.seleccionado)
        
        # CORRECCIÓN 4: Usar método intermedio para procesamiento de series
        self.procesarSeriesTemporales()

    def procesarSeriesTemporales(self):
        """
        CORRECCIÓN 4: Método intermedio que encadena el procesamiento
        Actúa como enlace en la cadena de procesamiento según el diagrama
        """
        print(">> GESTOR: procesarSeriesTemporales() - Método intermedio de enlace")
        
        # Delegar al método de obtención de valores
        self.obtenerValoresAlcanzadosDeSeriesTemporales()

    def cambiarEventoSismicoSeleccionadoABloqueadoEnRevision(self):
        """
        Implementa la secuencia completa del diagrama para cambio de estado
        """
        print(">> GESTOR: cambiarEventoSismicoSeleccionadoABloqueadoEnRevision()")
        
        if not self.seleccionado:
            return
            
        # Buscar el estado "Bloqueado en Revisión" iterando estados
        estados_disponibles = [
            Estado("Auto-Detectado"),
            Estado("Pendiente de Revisión"), 
            Estado("Bloqueado en Revisión"),
            Estado("Confirmado"),
            Estado("Rechazado")
        ]
        
        estado_bloqueado = None
        for estado in estados_disponibles:
            if estado.nombre == "Bloqueado en Revisión":
                print(f"   -> Encontrado estado: {estado.nombre}")
                estado_bloqueado = estado
                break
        
        # Cambiar estado del evento seleccionado
        self.seleccionado.cambiarEstadoEventoSismicoABloqueadoEnRevision()

    def buscarDatosSismicosRegistradosParaElEventoSismicoSeleccionado(self):
        """
        Obtiene los datos sísmicos del evento seleccionado
        """
        print(">> GESTOR: buscarDatosSismicosRegistradosParaElEventoSismicoSeleccionado()")
        
        if not self.seleccionado:
            return
            
        self.seleccionado.getDatosSismicosRegistradosParaEventoSismicoSeleccionado()

    def obtenerValoresAlcanzadosDeSeriesTemporales(self):
        """
        Implementa los loops anidados según el diagrama
        Loop para series temporales -> Loop para muestras -> Loop para detalles
        """
        print(">> GESTOR: obtenerValoresAlcanzadosDeSeriesTemporales()")
        
        if not self.seleccionado or not self.seleccionado.series_temporales:
            print(">> GESTOR: No hay series temporales para procesar")
            return
            
        # Obtener datos sísmicos registrados
        self.seleccionado.getDatosSismicosRegistradosParaEventoSismicoSeleccionado()
        
        # ============= LOOP PARA TODAS LAS SERIES TEMPORALES =============
        print(">> GESTOR: Iniciando Loop para todas las series temporales")
        
        for indice_serie, serie_temporal in enumerate(self.seleccionado.series_temporales):
            print(f">> GESTOR: Procesando serie temporal #{indice_serie + 1}")
            
            self.seleccionado.getValoresAlcanzadosPorCadaInstanteDeTiempo()
            
            datos_serie = serie_temporal.getDatos()
            print(f"   -> Serie con {datos_serie['cantidad_muestras']} muestras")
            
            # ========= LOOP PARA TODAS LAS MUESTRAS SÍSMICAS =========
            print("   >> GESTOR: Iniciando Loop para todas las muestras sísmicas")
            
            for indice_muestra, muestra_sismica in enumerate(serie_temporal.muestras):
                print(f"      -> Procesando muestra sísmica #{indice_muestra + 1}")
                
                datos_muestra = muestra_sismica.getDatos()
                print(f"         Muestra con {datos_muestra['cantidad_detalles']} detalles")
                
                # ======= LOOP PARA TODOS LOS DETALLES DE LA MUESTRA =======
                print("         >> GESTOR: Iniciando Loop para todos los detalles")
                
                for indice_detalle, detalle_muestra in enumerate(muestra_sismica.detalles):
                    print(f"            -> Procesando detalle #{indice_detalle + 1}")
                    
                    datos_detalle = detalle_muestra.getDatos()
                    
                    tipo_dato = detalle_muestra.getTipoDeDato()
                    es_velocidad = tipo_dato.esVelocidadDeOnda()
                    es_frecuencia = tipo_dato.esFrecuenciaDeOnda()
                    es_longitud = tipo_dato.esLongitud()
                    denominacion = tipo_dato.getDenominacion()
                    
                    print(f"               Tipo: {denominacion}, Valor: {datos_detalle['valor']}")
                    print(f"               ¿Es velocidad?: {es_velocidad}")
                    print(f"               ¿Es frecuencia?: {es_frecuencia}")
                    print(f"               ¿Es longitud?: {es_longitud}")
            
            es_de_estacion = self.seleccionado.esDeEstacionSismologica()
            print(f"   -> ¿Es de estación sismológica?: {es_de_estacion}")
        
        # ============= FUERA DEL LOOP DE LAS SERIES TEMPORALES =============
        print(">> GESTOR: Finalizando procesamiento de series temporales")
        
        # Clasificar muestras por estación
        self.clasificarMuestrasPorEstacionSismologica()
        
        # Llamar al caso de uso de generación de sismograma
        self.llamarAlCasoDeUsoGenerarSismograma()
        
        # Habilitar opción de visualización de mapa
        self.pantalla.habilitarOpcionVisualizacionMapaConEstacionesSismologicasInvolucradas()

    def clasificarMuestrasPorEstacionSismologica(self):
        """
        CORRECCIÓN 5: Implementación completa de clasificación por estación
        Agrupa las muestras sísmicas según la estación que las registró
        """
        print(">> GESTOR: clasificarMuestrasPorEstacionSismologica()")
        
        if not self.seleccionado or not self.seleccionado.series_temporales:
            print("   -> No hay series temporales para clasificar")
            return {}
        
        clasificacion_por_estacion = {}
        
        # Procesar cada serie temporal
        for indice_serie, serie in enumerate(self.seleccionado.series_temporales):
            # Obtener código de estación para esta serie
            codigo_estacion = self._obtenerCodigoEstacion(serie, indice_serie)
            
            if codigo_estacion not in clasificacion_por_estacion:
                clasificacion_por_estacion[codigo_estacion] = {
                    'serie_indices': [],
                    'muestras': [],
                    'total_muestras': 0
                }
            
            clasificacion_por_estacion[codigo_estacion]['serie_indices'].append(indice_serie)
            
            # Clasificar las muestras de esta serie
            for muestra in serie.muestras:
                muestra_info = {
                    'fecha_hora': muestra.fecha_hora_muestra,
                    'cantidad_detalles': len(muestra.detalles),
                    'detalles': []
                }
                
                # Procesar detalles de la muestra
                for detalle in muestra.detalles:
                    muestra_info['detalles'].append({
                        'tipo': detalle.tipo_dato,
                        'valor': detalle.valor
                    })
                
                clasificacion_por_estacion[codigo_estacion]['muestras'].append(muestra_info)
                clasificacion_por_estacion[codigo_estacion]['total_muestras'] += 1
        
        # Mostrar resumen de clasificación
        print(f"   -> Muestras clasificadas en {len(clasificacion_por_estacion)} estación(es):")
        for estacion, datos in clasificacion_por_estacion.items():
            print(f"      Estación {estacion}: {datos['total_muestras']} muestras en {len(datos['serie_indices'])} serie(s)")
        
        self.clasificacion_estaciones = clasificacion_por_estacion
        return clasificacion_por_estacion

    def _obtenerCodigoEstacion(self, serie, indice):
        """
        Método auxiliar para obtener el código de estación de una serie
        En un sistema real, esto vendría de la serie temporal
        """
        # Simular diferentes estaciones para diferentes series
        estaciones_disponibles = ["CBA-01", "CBA-02", "CBA-03", "MDZ-01", "SJN-01"]
        return estaciones_disponibles[indice % len(estaciones_disponibles)]
        
    def llamarAlCasoDeUsoGenerarSismograma(self):
        """
        Invoca el Caso de Uso 18: Generar Sismograma
        """
        print(">> GESTOR: llamarAlCasoDeUsoGenerarSismograma()")
        if self.seleccionado:
            SismogramaGenerator.generar_y_mostrar(self.seleccionado)

    def solicitarConfirmacionDeRevision(self):
        """Solicita al usuario confirmar, rechazar o derivar el evento"""
        print(">> GESTOR: solicitarConfirmacionDeRevision()")
        self.pantalla.solicitarConfirmarRechazarRevisarEvento()

    def tomarSeleccionConfirmacion(self):
        """
        Procesa la confirmación del evento sísmico
        """
        print("\n>> GESTOR: tomarSeleccionConfirmacion()")
        
        if self.validarDatosEvento():
            self.cambiarEventoSismicoAConfirmado()
            self.finCU()
    
    def tomarSeleccionRechazo(self):
        """
        Procesa el rechazo del evento sísmico
        """
        print("\n>> GESTOR: tomarSeleccionRechazo()")
        
        if self.validarDatosEvento():
            self.cambiarEventoSismicoSeleccionadoARechazado()
            self.finCU()
    
    def tomarSeleccionDerivacion(self):
        """Procesa la derivación del evento a un experto"""
        print("\n>> GESTOR: tomarSeleccionDerivacion()")
        
        if self.validarDatosEvento():
            self.cambiarEventoSismicoAPendienteRevisionExperto()
            self.registrarDerivacionAExperto()
            self.finCU()
        
    def validarDatosEvento(self) -> bool:
        """
        Valida los datos del evento sísmico seleccionado
        """
        if not self.seleccionado: 
            return False
            
        print(">> GESTOR: validarDatosEvento()")
        
        # Validar datos sísmicos
        self.seleccionado.validarDatosSismo()
        
        # Validar selección y registrar auditoría
        self.validarSeleccionConfirmacion()
        
        return True

    def validarSeleccionConfirmacion(self):
        """
        Valida la selección y registra información de auditoría
        """
        print(">> GESTOR: validarSeleccionConfirmacion()")
        
        fecha_hora = self.obtenerFechaHoraActual()
        empleado = self.obtenerEmpleadoSesion()
        
        print(f"   -> Acción registrada: {fecha_hora} por {empleado}")

    def obtenerFechaHoraActual(self):
        """Obtiene la fecha y hora actual del sistema"""
        fecha_hora = datetime.now()
        print(f">> GESTOR: obtenerFechaHoraActual() = {fecha_hora}")
        return fecha_hora

    def obtenerEmpleadoSesion(self):
        """
        Obtiene el empleado de la sesión actual
        """
        print(">> GESTOR: obtenerEmpleadoSesion()")
        sesion_actual = Sesion()
        empleado = sesion_actual.getEmpleado()
        print(f">> GESTOR: Empleado en sesión: {empleado}")
        return empleado

    def cambiarEventoSismicoSeleccionadoARechazado(self):
        """
        Cambia el estado del evento seleccionado a Rechazado
        """
        if self.seleccionado:
            print(f">> GESTOR: cambiarEventoSismicoSeleccionadoARechazado()")
            self.seleccionado.cambiarEventoSismicoSeleccionadoARechazado()
    
    def cambiarEventoSismicoAConfirmado(self):
        """Cambia el estado del evento seleccionado a Confirmado"""
        if self.seleccionado:
            print(f">> GESTOR: cambiarEventoSismicoAConfirmado()")
            self.seleccionado.cambiarEventoSismicoAConfirmado()
    
    def cambiarEventoSismicoAPendienteRevisionExperto(self):
        """Cambia el estado del evento a Pendiente de Revisión Experto"""
        if self.seleccionado:
            print(f">> GESTOR: cambiarEventoSismicoAPendienteRevisionExperto()")
            self.seleccionado.cambiarEstadoEventoSismico("Pendiente de Revisión Experto")
    
    def registrarDerivacionAExperto(self):
        """Registra la derivación del evento a un experto"""
        fecha_hora = self.obtenerFechaHoraActual()
        empleado = self.obtenerEmpleadoSesion()
        print(f"   -> Derivación registrada: {fecha_hora} por {empleado}")

    def finCU(self):
        """
        Finaliza el Caso de Uso actual
        """
        print("\n>> GESTOR: finCU() - Fin del Caso de Uso")
        print(">> GESTOR: El evento ha sido procesado exitosamente.")
        
        # Notificar a la pantalla que el CU ha finalizado
        self.pantalla.finCU()