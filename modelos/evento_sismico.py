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
        Verifica si el evento está en estado Auto-Detectado.
        Según el diagrama: EventoSismico → :CambioEstado: *esEstadoActual() (iterando estados del evento)
        """
        print(f"-> EventoSismico {self.id_sismo}: estaEnEstadoAutoDetectado()")
        
        for cambio_estado in self.historial_estados:
            if cambio_estado.esEstadoActual():
                resultado = cambio_estado.esAutoDetectado()
                print(f"-> EventoSismico {self.id_sismo}: estaEnEstadoAutoDetectado() = {resultado}")
                return resultado
        
        return False

    def estaEnEstadoPendienteDeRevision(self) -> bool:
        """
        Verifica si el evento está en estado Pendiente de Revisión.
        Según el diagrama: EventoSismico → estadoActual:CambioEstado: esPendienteDeRevision()
        """
        print(f"-> EventoSismico {self.id_sismo}: estaEnEstadoPendienteDeRevisiÃ³n()")
        
        resultado = self.estadoActual.esPendienteDeRevision()
        print(f"-> EventoSismico {self.id_sismo}: estaEnEstadoPendienteDeRevisiÃ³n() = {resultado}")
        return resultado

    def sosBloqueadoEnRevision(self) -> bool:
        """Verifica si el evento está bloqueado en revisión"""
        resultado = self.estadoActual.actual.nombre == "Bloqueado en Revisión"
        print(f"-> EventoSismico {self.id_sismo}: sosBloqueadoEnRevisiÃ³n() = {resultado}")
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
        Cambia el estado del evento a Bloqueado en Revisión.
        Esto previene que otros usuarios trabajen con el mismo evento.
        """
        self.cambiarEstadoEventoSismico("Bloqueado en Revisión")

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
        Obtener datos básicos del evento sísmico.
        Según el diagrama, debe llamar a múltiples métodos getter.
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
        # Valor simulado para efectos del diagrama
        return -31.4301  # Coordenadas de ejemplo (más profundo que epicentro)

    def getLongitudHipocentro(self) -> float:
        """Obtener longitud del hipocentro (punto de origen bajo tierra)"""
        print(f"-> EventoSismico {self.id_sismo}: getLongitudHipocentro()")
        # Valor simulado para efectos del diagrama
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
        # Valor simulado para efectos del diagrama
        return -31.4201  # Coordenadas de ejemplo (Córdoba, Argentina)

    def getLongitudEpicentro(self) -> float:
        """Obtener longitud del epicentro (punto en superficie)"""
        print(f"-> EventoSismico {self.id_sismo}: getLongitudEpicentro()")
        # Valor simulado para efectos del diagrama
        return -64.1888  # Coordenadas de ejemplo (Córdoba, Argentina)

    # === MÉTODOS DE DATOS SÍSMICOS ===
    
    def getDatosSismicosRegistradosParaEventoSismicoSeleccionado(self):
        """
        Buscar y cargar datos sísmicos registrados para el evento.
        Carga alcance, clasificación y origen del sismo.
        """
        print(f"-> EventoSismico {self.id_sismo}: getDatosSismicosRegistradosParaEventoSismicoSeleccionado()")
        self.alcance = AlcanceSismo().getDatosAlcance()
        self.clasificacion = ClasificacionSismo().getDatosClasificacion()
        self.origen = OrigenDeGeneracion().getDatosOrigen()
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
        Validar datos del sismo según el diagrama.
        Verifica alcance, magnitud y origen.
        """
        print(f"-> EventoSismico {self.id_sismo}: validarDatosSismo()")
        
        # Obtener y validar alcance
        alcance = self.getAlcance()
        
        # Obtener y validar magnitud
        magnitud = self.getMagnitud()
        
        # Obtener y validar origen
        origen = self.getOrigen()
        
        # Aquí se podrían agregar validaciones específicas
        # Por ejemplo: magnitud > 0, alcance no nulo, etc.
        
        return True

    def getMagnitud(self) -> float:
        """Obtener magnitud del evento (alias de getValorMagnitud)"""
        print(f"-> EventoSismico {self.id_sismo}: getMagnitud()")
        return self.getValorMagnitud()

    def esDeEstacionSismologica(self) -> bool:
        """
        Verificar si el evento fue detectado por una estación sismológica.
        Retorna True si hay datos de estación asociados.
        """
        print(f"-> EventoSismico {self.id_sismo}: esDeEstacionSismologica()")
        # En un sistema real, verificaría si hay estaciones asociadas
        return True

    def getValoresAlcanzadosPorCadaInstanteDeTiempo(self):
        """
        Obtener valores alcanzados por cada instante de tiempo.
        Procesa las series temporales para extraer valores en cada momento.
        """
        print(f"-> EventoSismico {self.id_sismo}: getValoresAlcanzadosPorCadaInstanteDeTiempo()")
        # Lógica para procesar valores por instante de tiempo
        # En un sistema real, esto retornaría un diccionario con timestamp -> valores
        return True