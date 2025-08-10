# gestor/GestorRegistroResultadoRevisionManual.py

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
            with open("sismos.json", "r", encoding="utf-8") as f: data = json.load(f)
            for sismo_data in data:
                self.eventos_sismicos_en_memoria.append(EventoSismico(
                    id_sismo=sismo_data["id_sismo"],
                    fecha=datetime.fromisoformat(sismo_data["fecha_hora_ocurrencia"]),
                    magnitud=sismo_data["valor_magnitud"],
                    estado_inicial=sismo_data["estado_inicial"],
                    series_data=sismo_data.get("series_temporales", [])
                ))
        except FileNotFoundError: print(">> GESTOR: ADVERTENCIA - No se encontró 'sismos.json'.")
        except Exception as e: print(f">> GESTOR: ERROR al cargar 'sismos.json': {e}")
            
    def buscarSismosAutoDetectadosYPendienteDeRevision(self):
        print("\n>> GESTOR: Buscando sismos no revisados...")
        sismos_filtrados = [s for s in self.eventos_sismicos_en_memoria if not s.sosBloqueadoEnRevisión() and (s.estaEnEstadoAutoDetectado() or s.estaEnEstadoPendienteDeRevisión())]
        eventos_ordenados = self.ordenarEventosSismicosPorFechaYHora(sismos_filtrados)
        self.pantalla.mostrarEventosSismicosEncontradosOrdenados(eventos_ordenados)
        self.pantalla.solicitarSeleccionEventoSismico()

    def ordenarEventosSismicosPorFechaYHora(self, eventos):
        eventos.sort(key=lambda x: x.getFechaHoraOcurrencia(), reverse=True)
        return eventos

    def tomarSeleccionEventoSismico(self, id_sismo: str):
        print(f"\n>> GESTOR: La pantalla informó la selección del sismo ID: {id_sismo}")
        for sismo in self.eventos_sismicos_en_memoria:
            if sismo.id_sismo == id_sismo:
                self.seleccionado = sismo
                self.cambiarEventoSismicoSeleccionadoABloqueadoEnRevision()
                self.buscarDatosSismicosRegistradosParaElEventoSismicoSeleccionado()
                self.obtenerValoresAlcanzadosDeSeriesTemporales()
                # Ahora el gestor le devuelve el control a la pantalla para que continúe el flujo interactivo
                self.pantalla.mostrarDatosYContinuarFlujo(self.seleccionado)
                break

    def cambiarEventoSismicoSeleccionadoABloqueadoEnRevision(self):
        if self.seleccionado and not self.seleccionado.sosBloqueadoEnRevisión():
            self.seleccionado.cambiarEstadoEventoSismicoABloqueadoEnRevision()

    def buscarDatosSismicosRegistradosParaElEventoSismicoSeleccionado(self):
        if not self.seleccionado: return
        print("\n>> GESTOR: Buscando datos registrados para el evento 'seleccionado'.")
        self.seleccionado.getDatosSismicosRegistradosParaEventoSismicoSeleccionado()

    def obtenerValoresAlcanzadosDeSeriesTemporales(self):
        print(">> GESTOR: Obteniendo valores de series temporales...")
        if self.seleccionado and self.seleccionado.series_temporales:
            print(f"Se encontraron {len(self.seleccionado.series_temporales[0].muestras)} muestras para procesar.")
        self.llamarAlCasoDeUsoGenerarSismograma()
        
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
        if not self.seleccionado: return False
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