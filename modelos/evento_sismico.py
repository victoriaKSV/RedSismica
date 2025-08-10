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

    def cambiarEstadoEventoSismico(self, nuevo_estado_nombre: str):
        if self.estadoActual: self.estadoActual.setFechHoraFin()
        nuevo_estado = Estado(nuevo_estado_nombre)
        self.estadoActual = CambioEstado.crearCambioEstado(nuevo_estado)
        self.historial_estados.append(self.estadoActual)

    def cambiarEstadoEventoSismicoABloqueadoEnRevision(self): self.cambiarEstadoEventoSismico("Bloqueado en Revisión")
    def cambiarEventoSismicoARechazado(self): self.cambiarEstadoEventoSismico("Rechazado")
    def estaEnEstadoAutoDetectado(self) -> bool: return self.estadoActual.esAutoDetectado()
    def estaEnEstadoPendienteDeRevisión(self) -> bool: return self.estadoActual.esPendienteDeRevision()
    def sosBloqueadoEnRevisión(self) -> bool: return self.estadoActual.actual.nombre == "Bloqueado en Revisión"
    def getDatosEventoSismico(self) -> dict: return {"ID": self.id_sismo, "Fecha/Hora": self.getFechaHoraOcurrencia(), "Magnitud": self.getValorMagnitud()}
    def getDatosSismicosRegistradosParaEventoSismicoSeleccionado(self):
        self.alcance = AlcanceSismo().getDatosAlcance()
        self.clasificacion = ClasificacionSismo().getDatosClasificacion()
        self.origen = OrigenDeGeneracion().getDatosOrigen()
        return self
    def getFechaHoraOcurrencia(self) -> datetime: return self.fechaHoraOcurrencia
    def getValorMagnitud(self) -> float: return self.valorMagnitud
    def getAlcance(self): return self.alcance
    def getClasificacion(self): return self.clasificacion
    def getOrigen(self): return self.origen
    def validarDatosSismo(self): self.getAlcance(); self.getMagnitud(); self.getOrigen()
    def esDeEstacionSismologica(self) -> bool: return True