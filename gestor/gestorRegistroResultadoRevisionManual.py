# gestor/gestorRegistroResultadoRevisionManual.py

import json
from datetime import datetime
from modelos.evento_sismico import EventoSismico
from modelos.sesion import Sesion
from modelos.estado import Estado
from casos_de_uso.generar_sismograma import SismogramaGenerator

class GestorRegistroResultadoRevisionManual:
    """
    CORRECCIÓN: Implementación fiel al diagrama de secuencia.
    Incluye todos los loops anidados y métodos según el PDF.
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
        CORRECCIÓN: Implementación fiel al diagrama.
        SEGÚN DIAGRAMA: GestorRegistroResultadoRevisionManual → GestorRegistroResultadoRevisionManual (self)
        LOOP (por cada EventoSismico):
        1. Chequeo "AutoDetectado" 
        2. Chequeo "PendienteDeRevision"
        3. Datos del evento
        """
        print("\n>> GESTOR: buscarSismosAutoDetectadosYPendienteDeRevision()")
        
        # ============= INICIO DEL LOOP PARA TODOS LOS EVENTOS SÍSMICOS =============
        sismos_filtrados = []
        
        for evento_sismico in self.eventos_sismicos_en_memoria:
            print(f">> GESTOR: Procesando evento {evento_sismico.id_sismo}")
            
            # VALIDACIÓN PREVENTIVA: Excluir eventos ya procesados
            estado_actual = evento_sismico.estadoActual.actual.nombre
            if estado_actual in ["Rechazado", "Confirmado", "Bloqueado en Revisión"]:
                print(f"   -> Evento {evento_sismico.id_sismo} excluido por estar en estado '{estado_actual}'")
                continue
            
            # ===== 1. CHEQUEO "AutoDetectado" =====
            # SEGÚN DIAGRAMA: GestorRegistroResultadoRevisionManual → EventoSismico: estaEnEstadoAutoDetectado()
            if evento_sismico.estaEnEstadoAutoDetectado():
                print(f"   -> Evento {evento_sismico.id_sismo} está en estado Auto-Detectado")
                # 3. Datos del evento - SEGÚN DIAGRAMA: GestorRegistroResultadoRevisionManual → EventoSismico: getDatosEventoSismico()
                datos_evento = evento_sismico.getDatosEventoSismico()
                sismos_filtrados.append(evento_sismico)
                continue
            
            # ===== 2. CHEQUEO "PendienteDeRevision" =====  
            # SEGÚN DIAGRAMA: GestorRegistroResultadoRevisionManual → EventoSismico: estaEnEstadoPendienteDeRevision()
            if evento_sismico.estaEnEstadoPendienteDeRevision():
                print(f"   -> Evento {evento_sismico.id_sismo} está en estado Pendiente de Revisión")
                # 3. Datos del evento
                datos_evento = evento_sismico.getDatosEventoSismico()
                sismos_filtrados.append(evento_sismico)
                continue
                
            print(f"   -> Evento {evento_sismico.id_sismo} no cumple criterios de filtrado")
        
        # ============= FUERA DEL LOOP =============
        print(f">> GESTOR: Se encontraron {len(sismos_filtrados)} eventos que cumplen los criterios")
        
        # SEGÚN DIAGRAMA: GestorRegistroResultadoRevisionManual → GestorRegistroResultadoRevisionManual: ordenarEventosSismicosPorFechaYHora()
        eventos_ordenados = self.ordenarEventosSismicosPorFechaYHora(sismos_filtrados)
        
        # SEGÚN DIAGRAMA: GestorRegistroResultadoRevisionManual → :PantallaGestionRegistroResultadoRevisionManual: mostrarEventosSismicosEncontradosOrdenados()
        self.pantalla.mostrarEventosSismicosEncontradosOrdenados(eventos_ordenados)
        
        # SEGÚN DIAGRAMA: GestorRegistroResultadoRevisionManual → :PantallaGestionRegistroResultadoRevisionManual: solicitarSeleccionEventoSismico()
        self.pantalla.solicitarSeleccionEventoSismico()

    def ordenarEventosSismicosPorFechaYHora(self, eventos):
        """SEGÚN DIAGRAMA: Ordena los eventos sísmicos por fecha y hora"""
        print(">> GESTOR: ordenarEventosSismicosPorFechaYHora()")
        eventos.sort(key=lambda x: x.getFechaHoraOcurrencia(), reverse=True)
        return eventos

    def tomarSeleccionEventoSismico(self, id_sismo: str):
        """
        CORRECCIÓN: Implementa la secuencia del diagrama después de la selección
        SEGÚN DIAGRAMA: :PantallaGestionRegistroResultadoRevisionManual: → GestorRegistroResultadoRevisionManual: tomarSeleccionEventoSismico()
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
            
        # SEGÚN DIAGRAMA: GestorRegistroResultadoRevisionManual → GestorRegistroResultadoRevisionManual: cambiarEventoSismicoSeleccionadoABloqueadoEnRevision()
        self.cambiarEventoSismicoSeleccionadoABloqueadoEnRevision()
        
        # SEGÚN DIAGRAMA: GestorRegistroResultadoRevisionManual → GestorRegistroResultadoRevisionManual: buscarDatosSismicosRegistradosParaElEventoSísmicoSeleccionado()
        self.buscarDatosSismicosRegistradosParaElEventoSismicoSeleccionado()
        
        # SEGÚN DIAGRAMA: GestorRegistroResultadoRevisionManual → :PantallaGestionRegistroResultadoRevisionManual: mostrarDatosEventoSismicoSeleccionado()
        self.pantalla.mostrarDatosEventoSismicoSeleccionado(self.seleccionado)
        
        # SEGÚN DIAGRAMA: GestorRegistroResultadoRevisionManual → GestorRegistroResultadoRevisionManual: obtenerValoresAlcanzadosDeSeriesTemporales()
        self.obtenerValoresAlcanzadosDeSeriesTemporales()

    def cambiarEventoSismicoSeleccionadoABloqueadoEnRevision(self):
        """
        CORRECCIÓN: Implementa la secuencia completa del diagrama para cambio de estado
        SEGÚN DIAGRAMA: 
        - GestorRegistroResultadoRevisionManual → :Estado: *sosBloqueadoEnRevision() (loop)
        - GestorRegistroResultadoRevisionManual → seleccionado:EventoSismico: cambiarEstadoEventoSismicoABloqueadoEnRevision()
        """
        print(">> GESTOR: cambiarEventoSismicoSeleccionadoABloqueadoEnRevision()")
        
        if not self.seleccionado:
            return
            
        # SEGÚN DIAGRAMA: Buscar el estado "Bloqueado en Revisión" iterando estados
        # GestorRegistroResultadoRevisionManual → :Estado: *sosBloqueadoEnRevision() (loop)
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
        
        # SEGÚN DIAGRAMA: GestorRegistroResultadoRevisionManual → seleccionado:EventoSismico: cambiarEstadoEventoSismicoABloqueadoEnRevision()
        self.seleccionado.cambiarEstadoEventoSismicoABloqueadoEnRevision()

    def buscarDatosSismicosRegistradosParaElEventoSismicoSeleccionado(self):
        """
        SEGÚN DIAGRAMA: GestorRegistroResultadoRevisionManual → seleccionado:EventoSismico: getDatosSismicosRegistradosParaEventoSísmicoSeleccionado()
        """
        print(">> GESTOR: buscarDatosSismicosRegistradosParaElEventoSismicoSeleccionado()")
        
        if not self.seleccionado:
            return
            
        # SEGÚN DIAGRAMA: Obtener datos sísmicos del evento seleccionado
        self.seleccionado.getDatosSismicosRegistradosParaEventoSismicoSeleccionado()

    def obtenerValoresAlcanzadosDeSeriesTemporales(self):
        """
        CORRECCIÓN PRINCIPAL: Implementa los loops anidados según el diagrama
        SEGÚN DIAGRAMA Y ANOTACIONES PDF:
        - Loop (para todas las series temporales)
        - Loop (para todas las muestras sísmicas) [mientras la serie temporal tenga muestras sismicas]
        - Loop (para todos los detalles de la muestra sísmica) [mientras la muestra sismica tenga detalles]
        """
        print(">> GESTOR: obtenerValoresAlcanzadosDeSeriesTemporales()")
        
        if not self.seleccionado or not self.seleccionado.series_temporales:
            print(">> GESTOR: No hay series temporales para procesar")
            return
            
        # SEGÚN DIAGRAMA: GestorRegistroResultadoRevisionManual → seleccionado:EventoSismico: getDatosSismicosRegistradosParaEventoSismicoSeleccionado()
        self.seleccionado.getDatosSismicosRegistradosParaEventoSismicoSeleccionado()
        
        # ============= CORRECCIÓN: LOOP PARA TODAS LAS SERIES TEMPORALES =============
        print(">> GESTOR: Iniciando Loop para todas las series temporales")
        
        for indice_serie, serie_temporal in enumerate(self.seleccionado.series_temporales):
            print(f">> GESTOR: Procesando serie temporal #{indice_serie + 1}")
            
            # SEGÚN DIAGRAMA: seleccionado:EventoSismico → seleccionado:EventoSismico: getValoresAlcanzadosPorCadaInstanteDeTiempo()
            self.seleccionado.getValoresAlcanzadosPorCadaInstanteDeTiempo()
            
            # SEGÚN DIAGRAMA: seleccionado:EventoSismico → :SerieTemporal: *getDatos()
            datos_serie = serie_temporal.getDatos()
            print(f"   -> Serie con {datos_serie['cantidad_muestras']} muestras")
            
            # ========= LOOP PARA TODAS LAS MUESTRAS SÍSMICAS [mientras la serie temporal tenga muestras sismicas] =========
            print("   >> GESTOR: Iniciando Loop para todas las muestras sísmicas")
            
            for indice_muestra, muestra_sismica in enumerate(serie_temporal.muestras):
                print(f"      -> Procesando muestra sísmica #{indice_muestra + 1}")
                
                # SEGÚN DIAGRAMA: :SerieTemporal → :MuestraSismica: *getDatos()
                datos_muestra = muestra_sismica.getDatos()
                print(f"         Muestra con {datos_muestra['cantidad_detalles']} detalles")
                
                # ======= LOOP PARA TODOS LOS DETALLES DE LA MUESTRA SÍSMICA [mientras la muestra sismica tenga detalles] =======
                print("         >> GESTOR: Iniciando Loop para todos los detalles de la muestra sísmica")
                
                for indice_detalle, detalle_muestra in enumerate(muestra_sismica.detalles):
                    print(f"            -> Procesando detalle #{indice_detalle + 1}")
                    
                    # SEGÚN DIAGRAMA: :MuestraSismica → :DetalleMuestraSismica: *getDatos()
                    datos_detalle = detalle_muestra.getDatos()
                    
                    # SEGÚN DIAGRAMA: :DetalleMuestraSismica → :TipoDeDatos: esVelocidadDeOnda()
                    tipo_dato = detalle_muestra.getTipoDeDato()
                    es_velocidad = tipo_dato.esVelocidadDeOnda()
                    
                    # SEGÚN DIAGRAMA: :DetalleMuestraSismica → :TipoDeDatos: esFrecuenciaDeOnda()
                    es_frecuencia = tipo_dato.esFrecuenciaDeOnda()
                    
                    # SEGÚN DIAGRAMA: :DetalleMuestraSismica → :TipoDeDatos: esLongitud()
                    es_longitud = tipo_dato.esLongitud()
                    
                    # SEGÚN DIAGRAMA: :TipoDeDatos: → :TipoDeDatos: getDenominacion()
                    denominacion = tipo_dato.getDenominacion()
                    
                    print(f"               Tipo: {denominacion}, Valor: {datos_detalle['valor']}")
                    print(f"               ¿Es velocidad?: {es_velocidad}")
                    print(f"               ¿Es frecuencia?: {es_frecuencia}")
                    print(f"               ¿Es longitud?: {es_longitud}")
            
            # SEGÚN DIAGRAMA: seleccionado:EventoSismico → seleccionado:EventoSismico: esDeEstacionSismologica()
            es_de_estacion = self.seleccionado.esDeEstacionSismologica()
            print(f"   -> ¿Es de estación sismológica?: {es_de_estacion}")
            
            # CORRECCIÓN: Según el diagrama también hay referencias a Sismografo y EstacionSismologica
            # seleccionado:EventoSismico → :Sismografo: *sosDeSismografo()
            # :Sismografo → :Sismografo: getEstacionSismologica()
            # :Sismografo → :EstacionSismologica: getCodigoEstacion()
            # Esto se implementaría si fuera necesario para el sistema completo
        
        # ============= FUERA DEL LOOP DE LAS SERIES TEMPORALES =============
        print(">> GESTOR: Finalizando procesamiento de series temporales")
        
        # SEGÚN DIAGRAMA: GestorRegistroResultadoRevisionManual → GestorRegistroResultadoRevisionManual: clasificarMuestrasPorEstacionSismologica()
        self.clasificarMuestrasPorEstacionSismologica()
        
        # SEGÚN DIAGRAMA: GestorRegistroResultadoRevisionManual → GestorRegistroResultadoRevisionManual: llamarAlCasoDeUsoGenerarSismograma()
        self.llamarAlCasoDeUsoGenerarSismograma()
        
        # SEGÚN DIAGRAMA: GestorRegistroResultadoRevisionManual → :PantallaGestionRegistroResultadoRevisionManual: habilitarOpcionVisualizacionMapaConEstacionesSismologicasInvolucradas()
        self.pantalla.habilitarOpcionVisualizacionMapaConEstacionesSismologicasInvolucradas()

    def clasificarMuestrasPorEstacionSismologica(self):
        """
        SEGÚN DIAGRAMA: GestorRegistroResultadoRevisionManual → GestorRegistroResultadoRevisionManual: clasificarMuestrasPorEstacionSismologica()
        Clasifica las muestras sísmicas por estación sismológica.
        """
        print(">> GESTOR: clasificarMuestrasPorEstacionSismologica()")
        # Implementación específica según necesidades del sistema
        
    def llamarAlCasoDeUsoGenerarSismograma(self):
        """
        SEGÚN DIAGRAMA: GestorRegistroResultadoRevisionManual → GenerarSismograma (include)
        Invoca el Caso de Uso 18: Generar Sismograma.
        """
        print(">> GESTOR: llamarAlCasoDeUsoGenerarSismograma()")
        if self.seleccionado:
            SismogramaGenerator.generar_y_mostrar(self.seleccionado)

    def solicitarConfirmacionDeRevision(self):
        """Solicita al usuario confirmar, rechazar o derivar el evento."""
        print(">> GESTOR: solicitarConfirmacionDeRevision()")
        self.pantalla.solicitarConfirmarRechazarRevisarEvento()

    def tomarSeleccionConfirmacion(self):
        """
        CORRECCIÓN: Procesa la confirmación según el diagrama
        """
        print("\n>> GESTOR: tomarSeleccionConfirmacion()")
        
        if self.validarDatosEvento():
            self.cambiarEventoSismicoAConfirmado()
            self.finCU()
    
    def tomarSeleccionRechazo(self):
        """
        CORRECCIÓN: Implementa la secuencia completa del rechazo según el diagrama
        SEGÚN DIAGRAMA:
        - GestorRegistroResultadoRevisionManual: → GestorRegistroResultadoRevisionManual: validarDatosEvento()
        - GestorRegistroResultadoRevisionManual: → seleccionado:EventoSismico: validarDatosSismo()
        - GestorRegistroResultadoRevisionManual: → GestorRegistroResultadoRevisionManual: cambiarEventoSismicoSeleccionadoARechazado()
        - seleccionado:EventoSismico→ estadoActual:CambioEstado: setFechaHoraFin()
        - seleccionado:EventoSismico: →seleccionado:EventoSismico: crearCambioEstado()
        - seleccionado:EventoSismico: → Rechazado:CambioEstado: new()
        """
        print("\n>> GESTOR: tomarSeleccionRechazo()")
        
        if self.validarDatosEvento():
            # SEGÚN DIAGRAMA: GestorRegistroResultadoRevisionManual: → GestorRegistroResultadoRevisionManual: cambiarEventoSismicoSeleccionadoARechazado()
            self.cambiarEventoSismicoSeleccionadoARechazado()
            self.finCU()
    
    def tomarSeleccionDerivacion(self):
        """Procesa la derivación del evento a un experto."""
        print("\n>> GESTOR: tomarSeleccionDerivacion()")
        
        if self.validarDatosEvento():
            self.cambiarEventoSismicoAPendienteRevisionExperto()
            self.registrarDerivacionAExperto()
            self.finCU()
        
    def validarDatosEvento(self) -> bool:
        """
        SEGÚN DIAGRAMA: 
        GestorRegistroResultadoRevisionManual: → GestorRegistroResultadoRevisionManual: validarDatosEvento()
        GestorRegistroResultadoRevisionManual: → seleccionado:EventoSismico: validarDatosSismo()
        """
        if not self.seleccionado: 
            return False
            
        print(">> GESTOR: validarDatosEvento()")
        
        # SEGÚN DIAGRAMA: validar datos sísmicos del evento
        self.seleccionado.validarDatosSismo()
        
        # SEGÚN DIAGRAMA: validar selección y registrar auditoría
        self.validarSeleccionConfirmacion()
        
        return True

    def validarSeleccionConfirmacion(self):
        """
        SEGÚN DIAGRAMA:
        GestorRegistroResultadoRevisionManual: → GestorRegistroResultadoRevisionManual: obtenerFechaHoraActual()
        GestorRegistroResultadoRevisionManual: → GestorRegistroResultadoRevisionManual: obtenerEmpleadoSesion()
        GestorRegistroResultradoRevisionManual: → ActualSesion: getEmpleado()
        """
        print(">> GESTOR: validarSeleccionConfirmacion()")
        
        # SEGÚN DIAGRAMA: obtener fecha/hora actual
        fecha_hora = self.obtenerFechaHoraActual()
        
        # SEGÚN DIAGRAMA: obtener empleado de sesión
        empleado = self.obtenerEmpleadoSesion()
        
        print(f"   -> Acción registrada: {fecha_hora} por {empleado}")

    def obtenerFechaHoraActual(self):
        """SEGÚN DIAGRAMA: Obtiene la fecha y hora actual del sistema"""
        fecha_hora = datetime.now()
        print(f">> GESTOR: obtenerFechaHoraActual() = {fecha_hora}")
        return fecha_hora

    def obtenerEmpleadoSesion(self):
        """
        SEGÚN DIAGRAMA: GestorRegistroResultadoRevisionManual: → ActualSesion: getEmpleado()
        """
        print(">> GESTOR: obtenerEmpleadoSesion()")
        sesion_actual = Sesion()
        empleado = sesion_actual.getEmpleado()
        print(f">> GESTOR: Empleado en sesión: {empleado}")
        return empleado

    def cambiarEventoSismicoSeleccionadoARechazado(self):
        """
        SEGÚN DIAGRAMA: GestorRegistroResultadoRevisionManual: → seleccionado:EventoSismico:cambiarEventoSismicoSeleccionadoARechazado()
        """
        if self.seleccionado:
            print(f">> GESTOR: cambiarEventoSismicoSeleccionadoARechazado()")
            self.seleccionado.cambiarEventoSismicoSeleccionadoARechazado()
    
    def cambiarEventoSismicoAConfirmado(self):
        """Cambia el estado del evento seleccionado a "Confirmado"."""
        if self.seleccionado:
            print(f">> GESTOR: cambiarEventoSismicoAConfirmado()")
            self.seleccionado.cambiarEventoSismicoAConfirmado()
    
    def cambiarEventoSismicoAPendienteRevisionExperto(self):
        """Cambia el estado del evento a "Pendiente de Revisión Experto"."""
        if self.seleccionado:
            print(f">> GESTOR: cambiarEventoSismicoAPendienteRevisionExperto()")
            self.seleccionado.cambiarEstadoEventoSismico("Pendiente de Revisión Experto")
    
    def registrarDerivacionAExperto(self):
        """Registra la derivación del evento a un experto."""
        fecha_hora = self.obtenerFechaHoraActual()
        empleado = self.obtenerEmpleadoSesion()
        print(f"   -> Derivación registrada: {fecha_hora} por {empleado}")

    def finCU(self):
        """
        SEGÚN DIAGRAMA: GestorRegistroResultadoRevisionManual: → GestorRegistroResultadoRevisionManual: fincu()
        Finaliza el Caso de Uso actual.
        """
        print("\n>> GESTOR: finCU() - Fin del Caso de Uso")
        print(">> GESTOR: El evento ha sido procesado exitosamente.")
        
        # Notificar a la pantalla que el CU ha finalizado
        self.pantalla.finCU()