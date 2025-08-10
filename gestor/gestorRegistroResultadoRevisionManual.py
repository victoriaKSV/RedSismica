# gestor/GestorRegistroResultadoRevisionManual.py

import json
from datetime import datetime
from modelos.evento_sismico import EventoSismico
from modelos.sesion import Sesion

class GestorRegistroResultadoRevisionManual:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.eventos_sismicos_en_memoria = []
        self.seleccionado = None
        self._cargar_datos_desde_json()
        print("-> Creada instancia del Gestor.")

    def _cargar_datos_desde_json(self):
        try:
            with open("sismos.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            
            for sismo_data in data:
                sismo = EventoSismico(
                    id_sismo=sismo_data["id_sismo"],
                    fecha=datetime.fromisoformat(sismo_data["fecha_hora_ocurrencia"]),
                    magnitud=sismo_data["valor_magnitud"],
                    estado_inicial=sismo_data["estado_inicial"]
                )
                self.eventos_sismicos_en_memoria.append(sismo)
            print(f">> GESTOR: Se cargaron {len(self.eventos_sismicos_en_memoria)} sismos desde 'sismos.json'.")
        except FileNotFoundError:
            print(">> GESTOR: ADVERTENCIA - No se encontró 'sismos.json'. Ejecuta 'generar_datos.py' primero.")
        except Exception as e:
            print(f">> GESTOR: ERROR - Ocurrió un problema al cargar 'sismos.json': {e}")
            
    def buscarSismosAutoDetectadosYPendienteDeRevision(self):
        print("\n>> GESTOR: (CU-23 P.6) Buscando sismos no revisados...")
        sismos_filtrados = [s for s in self.eventos_sismicos_en_memoria if not s.sosBloqueadoEnRevisión() and (s.estaEnEstadoAutoDetectado() or s.estaEnEstadoPendienteDeRevisión())]
        eventos_ordenados = self.ordenarEventosSismicosPorFechaYHora(sismos_filtrados)
        self.pantalla.mostrarEventosSismicosEncontradosOrdenados(eventos_ordenados)

    def ordenarEventosSismicosPorFechaYHora(self, eventos):
        eventos.sort(key=lambda x: x.getFechaHoraOcurrencia(), reverse=True)
        return eventos

    def tomarSeleccionEventoSismico(self, id_sismo: str):
        print(f"\n>> GESTOR: (CU-23 P.7) Tomando selección del evento ID: {id_sismo}")
        for sismo in self.eventos_sismicos_en_memoria:
            if sismo.id_sismo == id_sismo:
                self.seleccionado = sismo
                self.cambiarEventoSismicoSeleccionadoABloqueadoEnRevision()
                self.buscarDatosSismicosRegistradosParaElEventoSismicoSeleccionado()
                break

    def cambiarEventoSismicoSeleccionadoABloqueadoEnRevision(self):
        if self.seleccionado and not self.seleccionado.sosBloqueadoEnRevisión():
            print(">> GESTOR: (CU-23 P.8) Bloqueando evento seleccionado...")
            self.seleccionado.cambiarEstadoEventoSismicoABloqueadoEnRevision()

    def buscarDatosSismicosRegistradosParaElEventoSismicoSeleccionado(self):
        if not self.seleccionado: return
        print("\n>> GESTOR: (CU-23 P.9) Buscando datos registrados para el evento 'seleccionado'.")
        datos = self.seleccionado.getDatosSismicosRegistradosParaEventoSismicoSeleccionado()
        print(">> GESTOR: (CU-23 P.9.3) Llamando a generar sismograma...")
        self.pantalla.mostrarDatosEventoSismicoSeleccionado(datos)
        self.obtenerValoresAlcanzadosDeSeriesTemporales()

    def obtenerValoresAlcanzadosDeSeriesTemporales(self):
        print(">> GESTOR: Obteniendo valores de series temporales y clasificando por estación.")
        self.pantalla.habilitarOpcionesDeRevision()

    def tomarSeleccionRechazo(self):
        print("\n>> GESTOR: (CU-23 P.15) Se ha tomado la selección de RECHAZAR.")
        if self.validarDatosEvento():
            self.cambiarEventoSismicoARechazado()
            self.finCU()

    def validarDatosEvento(self) -> bool:
        print(">> GESTOR: (CU-23 P.16) Validando datos del evento 'seleccionado'...")
        if not self.seleccionado: return False
        self.validarSeleccionConfirmacion()
        self.seleccionado.validarDatosSismo()
        return True

    def validarSeleccionConfirmacion(self):
        self.obtenerFechaHoraActual()
        self.obtenerEmpleadoSesion()

    def obtenerFechaHoraActual(self):
        return datetime.now()

    def obtenerEmpleadoSesion(self):
        return Sesion().getEmpleado()

    def cambiarEventoSismicoARechazado(self):
        if self.seleccionado:
            print(">> GESTOR: (CU-23 P.17) Invocando cambio de estado a 'Rechazado' en el 'seleccionado'")
            self.seleccionado.cambiarEventoSismicoARechazado()

    def finCU(self):
        print("\n>> GESTOR: Fin del Caso de Uso.")
        self.pantalla.finCU()