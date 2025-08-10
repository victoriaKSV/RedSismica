# modelos/evento_sismico.py

from datetime import datetime
from .cambio_estado import CambioEstado
from .estado import Estado
from .alcance_sismo import AlcanceSismo
from .clasificacion_sismo import ClasificacionSismo
from .origen_de_generacion import OrigenDeGeneracion

class EventoSismico:
    def __init__(self, id_sismo: str, fecha: datetime, magnitud: float, estado_inicial: str = "Auto-Detectado"):
        self.id_sismo = id_sismo
        self.fechaHoraOcurrencia = fecha
        self.valorMagnitud = magnitud
        self.estadoActual = CambioEstado(Estado(estado_inicial))
        self.historial_estados = [self.estadoActual]
        self.alcance = None
        self.clasificacion = None
        self.origen = None
        self.series_temporales = []
        print(f"-> Creada instancia de EventoSismico ID: {self.id_sismo} en estado '{estado_inicial}'")

    def cambiarEstadoEventoSismico(self, nuevo_estado_nombre: str):
        if self.estadoActual:
            self.estadoActual.setFechHoraFin()
        nuevo_estado = Estado(nuevo_estado_nombre)
        self.estadoActual = CambioEstado.crearCambioEstado(nuevo_estado)
        self.historial_estados.append(self.estadoActual)
        print(f"-> EventoSismico {self.id_sismo}: Atributo 'estadoActual' actualizado a '{nuevo_estado_nombre}'")

    def cambiarEstadoEventoSismicoABloqueadoEnRevision(self):
        self.cambiarEstadoEventoSismico("Bloqueado en Revisión")

    def cambiarEventoSismicoARechazado(self):
        self.cambiarEstadoEventoSismico("Rechazado")

    def estaEnEstadoAutoDetectado(self) -> bool:
        return self.estadoActual.esAutoDetectado()

    def estaEnEstadoPendienteDeRevisión(self) -> bool:
        return self.estadoActual.esPendienteDeRevision()

    def sosBloqueadoEnRevisión(self) -> bool:
        return self.estadoActual.actual.nombre == "Bloqueado en Revisión"
    
    def getDatosEventoSismico(self) -> dict:
        return {
            "ID": self.id_sismo, "Fecha/Hora": self.getFechaHoraOcurrencia(),
            "Magnitud": self.getValorMagnitud(), "Latitud Epicentro": self.getLatitudEpicentro(),
            "Longitud Epicentro": self.getLongitudEpicentro(),
        }

    def getDatosSismicosRegistradosParaEventoSismicoSeleccionado(self):
        self.alcance = AlcanceSismo().getDatosAlcance()
        self.clasificacion = ClasificacionSismo().getDatosClasificacion()
        self.origen = OrigenDeGeneracion().getDatosOrigen()
        return self

    def getFechaHoraOcurrencia(self) -> datetime: return self.fechaHoraOcurrencia
    def getLatitudEpicentro(self) -> str: return "-31.4135"
    def getLongitudEpicentro(self) -> str: return "-64.1811"
    def getLatitudHipocentro(self) -> str: return "-31.4140"
    def getLongitudHipocentro(self) -> str: return "-64.1820"
    def getValorMagnitud(self) -> float: return self.valorMagnitud
    def getAlcance(self): return self.alcance
    def getClasificacion(self): return self.clasificacion
    def getOrigen(self): return self.origen

    def validarDatosSismo(self):
        print(f"-> EventoSismico {self.id_sismo}: Validando sus propios datos...")
        self.getAlcance()
        self.getMagnitud()
        self.getOrigen()
        print(f"-> EventoSismico {self.id_sismo}: Datos validados.")

    def esDeEstacionSismologica(self) -> bool:
        return True