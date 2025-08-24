# modelos/evento_sismico.py

from datetime import datetime
from .cambio_estado import CambioEstado
from .estado import Estado
from .alcance_sismo import AlcanceSismo
from .clasificacion_sismo import ClasificacionSismo
from .origen_de_generacion import OrigenDeGeneracion
from .serie_temporal import SerieTemporal
from .muestra_sismica import MuestraSismica
from .detalle_muestra_sismica import DetalleMuestraSismica

class EventoSismico:
    """
    NOTA IMPORTANTE (de tarjeta amarilla):
    ======================================
    El EventoSismico maneja los cambios de estado mediante:
    - Un estado actual (CambioEstado)
    - Un historial completo de estados
    - Cada cambio registra fecha/hora de inicio y fin
    - Los estados válidos son: Auto-Detectado, Pendiente de Revisión,
      Bloqueado en Revisión, Confirmado, Rechazado
    """
    
    def __init__(self, id_sismo: str, fecha: datetime, magnitud: float, estado_inicial: str = "Auto-Detectado", series_data=None):
        self.id_sismo = id_sismo
        self.fechaHoraOcurrencia = fecha
        self.valorMagnitud = magnitud
        self.estadoActual = CambioEstado(Estado(estado_inicial))
        self.historial_estados = [self.estadoActual]
        self.alcance = None
        self.clasificacion = None
        self.origen = None
        
        # Cargar la estructura de series temporales
        self.series_temporales = self._cargar_series(series_data)
        
        print(f"-> Creada instancia de EventoSismico ID: {self.id_sismo} en estado '{estado_inicial}'")

    def _cargar_series(self, series_data):
        """Carga las series temporales desde los datos proporcionados"""
        lista_series = []
        if series_data:
            for serie_d in series_data:
                serie_obj = SerieTemporal()
                for muestra_d in serie_d.get('muestras', []):
                    muestra_obj = MuestraSismica(datetime.fromisoformat(muestra_d['fecha_hora_muestra']))
                    for detalle_d in muestra_d.get('detalles', []):
                        detalle_obj = DetalleMuestraSismica(detalle_d['tipo_dato'], detalle_d['valor'])
                        muestra_obj.agregar_detalle(detalle_obj)
                    serie_obj.agregar_muestra(muestra_obj)
                lista_series.append(serie_obj)
        return lista_series

    # === MÉTODOS DE ESTADO SEGÚN EL DIAGRAMA ===
    
    def estaEnEstadoAutoDetectado(self) -> bool:
        """
        CORRECCIÓN: Verifica si el evento está en estado Auto-Detectado.
        SEGÚN EL DIAGRAMA: EventoSismico → :CambioEstado: *esEstadoActual() (iterando estados del evento)
        LUEGO: :EventoSismico → estadoActual:CambioEstado: esAutoDetectado()
        """
        print(f"-> EventoSismico {self.id_sismo}: estaEnEstadoAutoDetectado()")
        
        # CORRECCIÓN: Según las anotaciones del PDF, primero verificar si esEstadoActual()
        # Iterando estados del evento para encontrar el estado actual
        for cambio_estado in self.historial_estados:
            if cambio_estado.esEstadoActual():  # Chequeo si fechaHoraFin está en None
                resultado = cambio_estado.esAutoDetectado()
                print(f"-> EventoSismico {self.id_sismo}: estaEnEstadoAutoDetectado() = {resultado}")
                return resultado
        
        return False

    def estaEnEstadoPendienteDeRevision(self) -> bool:
        """
        CORRECCIÓN: Verifica si el evento está en estado Pendiente de Revisión.
        SEGÚN EL DIAGRAMA: EventoSismico → estadoActual:CambioEstado: esPendienteDeRevision()
        LUEGO: estadoActual:CambioEstado → estadoActual:CambioEstado: esDelAmbito()
        """
        print(f"-> EventoSismico {self.id_sismo}: estaEnEstadoPendienteDeRevision()")
        
        # CORRECCIÓN: Verificar primero si es el estado actual vigente
        if self.estadoActual.esEstadoActual():
            resultado = self.estadoActual.esPendienteDeRevision()
            print(f"-> EventoSismico {self.id_sismo}: estaEnEstadoPendienteDeRevision() = {resultado}")
            return resultado
        
        return False

    def sosBloqueadoEnRevision(self) -> bool:
        """Verifica si el evento está bloqueado en revisión"""
        resultado = self.estadoActual.actual.nombre == "Bloqueado en Revisión"
        print(f"-> EventoSismico {self.id_sismo}: sosBloqueadoEnRevision() = {resultado}")
        return resultado

    # === MÉTODOS DE CAMBIO DE ESTADO ===
    
    def cambiarEstadoEventoSismico(self, nuevo_estado_nombre: str):
        """
        Cambiar el estado del evento sísmico según el diagrama.
        NOTA: Este es el método principal para cambios de estado.
        1. Finaliza el estado actual (setFechaHoraFin)
        2. Crea nuevo cambio de estado
        3. Actualiza estado actual y agrega al historial
        """
        print(f"-> EventoSismico {self.id_sismo}: Cambiando estado a '{nuevo_estado_nombre}'")
        
        # Finalizar el estado actual
        if self.estadoActual: 
            self.estadoActual.setFechHoraFin()
        
        # Crear nuevo cambio de estado
        nuevo_cambio_estado = self.crearCambioEstado(nuevo_estado_nombre)
        
        # Actualizar estado actual y agregar al historial
        self.estadoActual = nuevo_cambio_estado
        self.historial_estados.append(self.estadoActual)

    def crearCambioEstado(self, nombre_estado: str):
        """
        Crear nuevo cambio de estado según el diagrama.
        Utiliza el método de clase de CambioEstado.
        """
        print(f"-> EventoSismico {self.id_sismo}: crearCambioEstado('{nombre_estado}')")
        
        nuevo_estado = Estado(nombre_estado)
        return CambioEstado.crearCambioEstado(nuevo_estado)

    def cambiarEstadoEventoSismicoABloqueadoEnRevision(self):
        """
        SEGÚN EL DIAGRAMA: seleccionado:EventoSismico: → estadoActual:CambioEstado: setFechHoraFin()
        LUEGO: seleccionado:EventoSismico → seleccionado:EventoSismico: crearCambioEstado()
        FINALMENTE: seleccionado:EventoSismico → BloqueadoEnRevision:CambioEstado : new()
        """
        print(f"-> EventoSismico {self.id_sismo}: cambiarEstadoEventoSismicoABloqueadoEnRevision()")
        self.cambiarEstadoEventoSismico("Bloqueado en Revisión")

    def cambiarEventoSismicoSeleccionadoARechazado(self):
        """
        CORRECCIÓN: Método específico para rechazo según el diagrama
        """
        print(f"-> EventoSismico {self.id_sismo}: cambiarEventoSismicoSeleccionadoARechazado()")
        self.cambiarEstadoEventoSismico("Rechazado")

    def cambiarEventoSismicoARechazado(self):
        """
        Cambia el estado del evento a Rechazado.
        Marca el evento como falso positivo.
        """
        self.cambiarEstadoEventoSismico("Rechazado")
    
    def cambiarEventoSismicoAConfirmado(self):
        """
        Cambia el estado del evento a Confirmado.
        Valida el evento como sismo real.
        """
        self.cambiarEstadoEventoSismico("Confirmado")

    # === MÉTODOS GETTER SEGÚN EL DIAGRAMA ===
    
    def getDatosEventoSismico(self) -> dict:
        """
        SEGÚN EL DIAGRAMA: :EventoSismico: → :EventoSismico:
        getFechaHoraOcurrencia(), getLatitudEpicentro(), getLongitudEpicentro(),
        getLatitudHipocentro(), getLongitudHipocentro(), getValorMagnitud()
        """
        print(f"-> EventoSismico {self.id_sismo}: getDatosEventoSismico()")
        
        fecha_hora = self.getFechaHoraOcurrencia()
        latitud_epicentro = self.getLatitudEpicentro()
        longitud_epicentro = self.getLongitudEpicentro()
        latitud_hipocentro = self.getLatitudHipocentro()
        longitud_hipocentro = self.getLongitudHipocentro()
        magnitud = self.getValorMagnitud()
        
        return {
            "ID": self.id_sismo, 
            "Fecha/Hora": fecha_hora, 
            "Magnitud": magnitud,
            "LatitudEpicentro": latitud_epicentro,
            "LongitudEpicentro": longitud_epicentro,
            "LatitudHipocentro": latitud_hipocentro,
            "LongitudHipocentro": longitud_hipocentro
        }

    def getLatitudHipocentro(self) -> float:
        """Obtener latitud del hipocentro (punto de origen bajo tierra)"""
        print(f"-> EventoSismico {self.id_sismo}: getLatitudHipocentro()")
        return -31.4301  # Coordenadas de ejemplo (más profundo que epicentro)

    def getLongitudHipocentro(self) -> float:
        """Obtener longitud del hipocentro (punto de origen bajo tierra)"""
        print(f"-> EventoSismico {self.id_sismo}: getLongitudHipocentro()")
        return -64.1988  # Coordenadas de ejemplo (más profundo que epicentro)

    def getFechaHoraOcurrencia(self) -> datetime:
        """Obtener fecha y hora de ocurrencia del evento"""
        print(f"-> EventoSismico {self.id_sismo}: getFechaHoraOcurrencia()")
        return self.fechaHoraOcurrencia

    def getValorMagnitud(self) -> float:
        """Obtener valor de magnitud del evento"""
        print(f"-> EventoSismico {self.id_sismo}: getValorMagnitud() = {self.valorMagnitud}")
        return self.valorMagnitud

    def getLatitudEpicentro(self) -> float:
        """Obtener latitud del epicentro (punto en superficie)"""
        print(f"-> EventoSismico {self.id_sismo}: getLatitudEpicentro()")
        return -31.4201  # Coordenadas de ejemplo (Córdoba, Argentina)

    def getLongitudEpicentro(self) -> float:
        """Obtener longitud del epicentro (punto en superficie)"""
        print(f"-> EventoSismico {self.id_sismo}: getLongitudEpicentro()")
        return -64.1888  # Coordenadas de ejemplo (Córdoba, Argentina)

    # === MÉTODOS DE DATOS SÍSMICOS ===
    
    def getDatosSismicosRegistradosParaEventoSismicoSeleccionado(self):
        """
        SEGÚN EL DIAGRAMA:
        seleccionado:EventoSismico: → :AlcanceSismo: getDatosAlcance()
        seleccionado:EventoSismico → :ClasificacionSismo: getDatosClasificacion()
        seleccionado:EventoSismico → :OrigenDeGeneracion: getDatosOrigen()
        """
        print(f"-> EventoSismico {self.id_sismo}: getDatosSismicosRegistradosParaEventoSismicoSeleccionado()")
        
        # Obtener datos de alcance
        alcance_obj = AlcanceSismo()
        self.alcance = alcance_obj.getDatosAlcance()
        
        # Obtener datos de clasificación  
        clasificacion_obj = ClasificacionSismo()
        self.clasificacion = clasificacion_obj.getDatosClasificacion()
        
        # Obtener datos de origen
        origen_obj = OrigenDeGeneracion()
        self.origen = origen_obj.getDatosOrigen()
        
        return self

    def getAlcance(self):
        """Obtener alcance del sismo (Local, Regional, Nacional, etc.)"""
        print(f"-> EventoSismico {self.id_sismo}: getAlcance() = {self.alcance}")
        return self.alcance

    def getClasificacion(self):
        """Obtener clasificación del sismo (Leve, Moderado, Fuerte, etc.)"""
        print(f"-> EventoSismico {self.id_sismo}: getClasificacion() = {self.clasificacion}")
        return self.clasificacion

    def getOrigen(self):
        """Obtener origen del sismo (Tectónico, Volcánico, etc.)"""
        print(f"-> EventoSismico {self.id_sismo}: getOrigen() = {self.origen}")
        return self.origen

    # === MÉTODOS DE VALIDACIÓN ===
    
    def validarDatosSismo(self):
        """
        SEGÚN EL DIAGRAMA:
        seleccionado:EventoSismico: →seleccionado:EventoSismico: getAlcance()
        seleccionado:EventoSismico: →seleccionado:EventoSismico: getMagnitud()
        seleccionado:EventoSismico: →seleccionado:EventoSismico: getOrigen()
        """
        print(f"-> EventoSismico {self.id_sismo}: validarDatosSismo()")
        
        # Obtener y validar alcance
        alcance = self.getAlcance()
        
        # Obtener y validar magnitud
        magnitud = self.getMagnitud()
        
        # Obtener y validar origen
        origen = self.getOrigen()
        
        # Aquí se podrían agregar validaciones específicas
        return True

    def getMagnitud(self) -> float:
        """Obtener magnitud del evento (alias de getValorMagnitud)"""
        print(f"-> EventoSismico {self.id_sismo}: getMagnitud()")
        return self.getValorMagnitud()

    def esDeEstacionSismologica(self) -> bool:
        """
        SEGÚN EL DIAGRAMA:
        seleccionado:EventoSismico → seleccionado:EventoSismico: esDeEstacionSismologica()
        seleccionado:EventoSismico → :Sismografo: *sosDeSismografo()
        """
        print(f"-> EventoSismico {self.id_sismo}: esDeEstacionSismologica()")
        # En un sistema real, verificaría si hay estaciones asociadas
        return True

    def getValoresAlcanzadosPorCadaInstanteDeTiempo(self):
        """
        SEGÚN EL DIAGRAMA:
        seleccionado:EventoSismico → seleccionado:EventoSismico: getValoresAlcanzadosPorCadaInstanteDeTiempo()
        """
        print(f"-> EventoSismico {self.id_sismo}: getValoresAlcanzadosPorCadaInstanteDeTiempo()")
        # Lógica para procesar valores por instante de tiempo
        return True