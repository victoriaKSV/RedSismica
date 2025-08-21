# gestor/gestorRegistroResultadoRevisionManual.py

import json
from datetime import datetime
from modelos.evento_sismico import EventoSismico
from modelos.sesion import Sesion
from casos_de_uso.generar_sismograma import SismogramaGenerator

class GestorRegistroResultadoRevisionManual:
    """
    NOTA IMPORTANTE (de tarjeta amarilla del diagrama):
    =================================================
    * El GESTOR maneja cambio de estado básicos (Auto-Detectado -> Bloqueado en Revisión)
      y (Estado) hacia un rechazo decidido sobre esta selección en Estados después a asignar "Bloqueado en Revisión"
    
    * Al final de el Gestor es hora el Estado básico (Auto-Detectado) => Estado a asignar 'copia de confirmación' al evento sismologico
      Por alguna razón no estamos humanamente con el objetivo en Python.
    
    * Para Toda crear una nueva instancia de CAMBIODESTADO: Entonces desde el seleccionado:EventoSismico se encarga el
      método (notación propia) ESTADO->estadoNuevoFInalyValidado() por ejemplo de pasar (tarde cambios en SISMOS en Python).
      Este modelo instancia propia Estado a NotificadorFin en fecha y si ResultadoRegistrado con el inicio de otro nuevo comenzado en la GUI Python.
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
        NOTA DE TARJETA ROSADA - Loop Para Todos Los Eventos Sísmicos:
        =============================================================
        El proceso debe evaluar TODOS los eventos sísmicos almacenados:
        
        1. Si el sismo está en REGISTRAR => RESULTADO DE REVISION
           MANUAL
        
        2. Primero verifica si el ESTADO está en "AutoDetectado" o "Pendiente de Revisión"
           - Si está en "AutoDetectado": Se incluye en la lista
           - Si está en "Pendiente de Revisión": También se incluye
           - Otros estados: Se descartan
        
        3. Por cada sismo que cumpla los criterios se obtiene:
           - getDatosEventoSismico() para información básica
           - Se agrega a la lista de sismos filtrados
           
        4. Al finalizar el loop:
           - Se ordenan los eventos por fecha y hora
           - Se muestran en pantalla
           - Se solicita selección al usuario
           
        NOTA DE TARJETA VIOLETA - Mostrando Eventos:
        ============================================
        Los eventos se muestran al ANALISTA con:
        - ID del evento
        - Fecha y hora de ocurrencia
        - Magnitud
        - Estado actual
        La pantalla debe solicitarSeleccionEvento() después
        """
        print("\n>> GESTOR: Buscando sismos auto-detectados y pendientes de revisión...")
        
        # ============= INICIO DEL LOOP PARA TODOS LOS EVENTOS SÍSMICOS =============
        # NOTA: Este loop debe procesar TODOS los eventos sísmicos sin excepción
        sismos_filtrados = []
        
        for evento_sismico in self.eventos_sismicos_en_memoria:
            print(f">> GESTOR: Procesando evento {evento_sismico.id_sismo}")
            print(f"   -> Estado actual: {evento_sismico.estadoActual.actual.nombre}")
            
            # VALIDACIÓN IMPORTANTE: Solo procesar sismos que NO estén rechazados, bloqueados o confirmados
            # Esto evita re-procesar eventos ya gestionados
            estado_actual = evento_sismico.estadoActual.actual.nombre
            if estado_actual in ["Rechazado", "Confirmado", "Bloqueado en Revisión"]:
                print(f"   -> Evento {evento_sismico.id_sismo} excluido por estar en estado '{estado_actual}'")
                continue
            
            # ===== CHEQUEO 1: Verificar si está en estado "Auto-Detectado" =====
            if evento_sismico.estaEnEstadoAutoDetectado():
                print(f"   -> Evento {evento_sismico.id_sismo} está en estado Auto-Detectado")
                # Obtener datos básicos del evento para mostrar en la lista
                datos_evento = evento_sismico.getDatosEventoSismico()
                sismos_filtrados.append(evento_sismico)
            
            # ===== CHEQUEO 2: Verificar si está en estado "Pendiente de Revisión" =====
            elif evento_sismico.estaEnEstadoPendienteDeRevision():
                print(f"   -> Evento {evento_sismico.id_sismo} está en estado Pendiente de Revisión")
                # Obtener datos básicos del evento para mostrar en la lista
                datos_evento = evento_sismico.getDatosEventoSismico()
                sismos_filtrados.append(evento_sismico)
                
            else:
                print(f"   -> Evento {evento_sismico.id_sismo} no cumple criterios de filtrado")
        
        # ============= FIN DEL LOOP - FUERA DEL LOOP =============
        print(f">> GESTOR: Se encontraron {len(sismos_filtrados)} eventos que cumplen los criterios")
        
        # Ordenar los eventos encontrados por fecha y hora (más recientes primero)
        eventos_ordenados = self.ordenarEventosSismicosPorFechaYHora(sismos_filtrados)
        
        # Mostrar los eventos encontrados en la pantalla
        self.pantalla.mostrarEventosSismicosEncontradosOrdenados(eventos_ordenados)
        
        # Solicitar al usuario que seleccione un evento
        self.pantalla.solicitarSeleccionEventoSismico()

    def ordenarEventosSismicosPorFechaYHora(self, eventos):
        """Ordena los eventos sísmicos por fecha y hora de ocurrencia (más recientes primero)"""
        eventos.sort(key=lambda x: x.getFechaHoraOcurrencia(), reverse=True)
        return eventos

    def tomarSeleccionEventoSismico(self, id_sismo: str):
        """
        NOTA IMPORTANTE: Captura una vez ahí que ya el gestor tiene todos los
        EventosSismicos filtrados para gestión de estado.
        """
        print(f"\n>> GESTOR: La pantalla informó la selección del sismo ID: {id_sismo}")
        
        # Buscar el sismo seleccionado en la lista de eventos en memoria
        for sismo in self.eventos_sismicos_en_memoria:
            if sismo.id_sismo == id_sismo:
                self.seleccionado = sismo
                break
        
        if not self.seleccionado:
            print(f">> GESTOR: ERROR - No se encontró el sismo {id_sismo}")
            return
            
        # Cambiar el estado del evento seleccionado a "Bloqueado en Revisión"
        # NOTA: Esto previene que otro usuario pueda seleccionar el mismo evento
        self.cambiarEventoSismicoSeleccionadoABloqueadoEnRevision()
        
        # Buscar y cargar todos los datos sísmicos registrados para el evento
        self.buscarDatosSismicosRegistradosParaElEventoSismicoSeleccionado()
        
        # Mostrar los datos del evento seleccionado en la pantalla
        self.pantalla.mostrarDatosEventoSismicoSeleccionado(self.seleccionado)
        
        # Procesar series temporales y generar visualizaciones
        self.obtenerValoresAlcanzadosDeSeriesTemporales()

    def cambiarEventoSismicoSeleccionadoABloqueadoEnRevision(self):
        """
        Cambia el estado del evento seleccionado a 'Bloqueado en Revisión'.
        Esto asegura que ningún otro analista pueda trabajar con el mismo evento.
        """
        print(">> GESTOR: Cambiando evento seleccionado a 'Bloqueado en Revisión'")
        
        if not self.seleccionado:
            return
            
        # Verificar primero si ya está bloqueado (no debería suceder, pero por seguridad)
        for estado in self.seleccionado.historial_estados:
            if estado.actual.nombre == "Bloqueado en Revisión" and estado.esEstadoActual():
                print(">> GESTOR: El evento ya está bloqueado en revisión")
                return
        
        # Cambiar el estado del evento
        self.seleccionado.cambiarEstadoEventoSismicoABloqueadoEnRevision()

    def buscarDatosSismicosRegistradosParaElEventoSismicoSeleccionado(self):
        """Carga todos los datos sísmicos asociados al evento seleccionado"""
        print(">> GESTOR: Buscando datos sísmicos registrados para el evento seleccionado")
        
        if not self.seleccionado:
            return
            
        # Obtener alcance, clasificación y origen del sismo
        self.seleccionado.getDatosSismicosRegistradosParaEventoSismicoSeleccionado()

    def obtenerValoresAlcanzadosDeSeriesTemporales(self):
        """
        NOTA DE TARJETA VERDE - Loop Para Todas Las Series Temporales:
        =============================================================
        Este proceso itera sobre TODAS las series temporales del evento:
        
        1. Por cada Serie Temporal:
           - Se obtienen todos los datos con getDatos()
           - Se procesan todas las muestras sísmicas
           
        2. Por cada Muestra Sísmica dentro de la serie:
           - Se obtienen los datos de la muestra
           - Se procesan todos los detalles
           
        3. Por cada Detalle de Muestra Sísmica:
           - Se verifica el tipo de dato (velocidad, frecuencia, longitud)
           - Se obtiene la denominación del tipo de dato
           - Se procesa el valor registrado
           
        4. Validaciones adicionales:
           - Verificar si es de estación sismológica
           - Obtener código de estación si aplica
           
        5. Al finalizar todas las series:
           - Clasificar muestras por estación sismológica
           - Generar sismograma
           - Habilitar visualización en mapa
        """
        print(">> GESTOR: Obteniendo valores de series temporales...")
        
        if not self.seleccionado or not self.seleccionado.series_temporales:
            print(">> GESTOR: No hay series temporales para procesar")
            return
            
        # Obtener datos sísmicos registrados
        self.seleccionado.getDatosSismicosRegistradosParaEventoSismicoSeleccionado()
        
        # ============= INICIO LOOP PARA TODAS LAS SERIES TEMPORALES =============
        print(">> GESTOR: Iniciando procesamiento de series temporales...")
        
        for indice_serie, serie_temporal in enumerate(self.seleccionado.series_temporales):
            print(f">> GESTOR: Procesando serie temporal #{indice_serie + 1}")
            
            # Obtener valores alcanzados por cada instante de tiempo
            self.seleccionado.getValoresAlcanzadosPorCadaInstanteDeTiempo()
            
            # Obtener datos de la serie temporal
            datos_serie = serie_temporal.getDatos()
            print(f"   -> Serie con {datos_serie['cantidad_muestras']} muestras")
            
            # ========= LOOP PARA TODAS LAS MUESTRAS SÍSMICAS =========
            for indice_muestra, muestra_sismica in enumerate(serie_temporal.muestras):
                print(f"   -> Procesando muestra sísmica #{indice_muestra + 1}")
                
                # Obtener datos de la muestra
                datos_muestra = muestra_sismica.getDatos()
                
                # ======= LOOP PARA TODOS LOS DETALLES DE LA MUESTRA =======
                for indice_detalle, detalle_muestra in enumerate(muestra_sismica.detalles):
                    print(f"      -> Procesando detalle #{indice_detalle + 1}")
                    
                    # Obtener datos del detalle
                    datos_detalle = detalle_muestra.getDatos()
                    
                    # Obtener y verificar tipo de dato
                    tipo_dato = detalle_muestra.getTipoDeDato()
                    
                    # Verificar tipo específico de dato
                    es_velocidad = tipo_dato.esVelocidadDeOnda()
                    es_frecuencia = tipo_dato.esFrecuenciaDeOnda()
                    es_longitud = tipo_dato.esLongitud()
                    
                    # Obtener denominación del tipo de dato
                    denominacion = tipo_dato.getDenominacion()
                    
                    print(f"         Tipo: {denominacion}, Valor: {datos_detalle['valor']}")
            
            # Verificar si es de estación sismológica
            es_de_estacion = self.seleccionado.esDeEstacionSismologica()
            print(f"   -> ¿Es de estación sismológica?: {es_de_estacion}")
            
            # NOTA: Aquí se podría obtener información del sismógrafo y estación
            # si el sistema lo requiere (según el diagrama)
        
        # ============= FIN DEL LOOP DE SERIES TEMPORALES =============
        print(">> GESTOR: Finalizando procesamiento de series temporales")
        
        # Clasificar las muestras por estación sismológica
        self.clasificarMuestrasPorEstacionSismologica()
        
        # Llamar al caso de uso "Generar Sismograma"
        self.llamarAlCasoDeUsoGenerarSismograma()
        
        # Habilitar opción de visualización en mapa
        self.pantalla.habilitarOpcionVisualizacionMapaConEstacionesSismologicasInvolucradas()

    def clasificarMuestrasPorEstacionSismologica(self):
        """
        Clasifica las muestras sísmicas por estación sismológica.
        Esto permite agrupar los datos según su origen para análisis posteriores.
        """
        print(">> GESTOR: Clasificando muestras por estación sismológica")
        # Implementación específica según necesidades del sistema
        # Por ejemplo, crear un diccionario con estación como clave y muestras como valor
        
    def solicitarConfirmacionDeRevision(self):
        """
        Solicita al usuario confirmar, rechazar o derivar el evento.
        Se llama después de que el usuario responde a las opciones de visualización y modificación.
        """
        print(">> GESTOR: Solicitando a la pantalla que muestre las opciones finales de revisión.")
        self.pantalla.solicitarConfirmarRechazarRevisarEvento()

    def tomarSeleccionConfirmacion(self):
        """
        NOTA DE TARJETA VIOLETA:
        Procesa la confirmación del evento como sismo real.
        Cambia el estado a "Confirmado" y registra la acción.
        """
        print("\n>> GESTOR: Se ha tomado la selección de CONFIRMAR.")
        
        if self.validarDatosEvento():
            # Cambiar el estado del evento a "Confirmado"
            self.cambiarEventoSismicoAConfirmado()
            
            # Finalizar el caso de uso
            self.finCU()
    
    def tomarSeleccionRechazo(self):
        """
        NOTA DE TARJETA ROSADA - Proceso de Rechazo:
        ==========================================
        1. Validar datos del evento antes del rechazo
        2. Cambiar estado a "Rechazado"
        3. Registrar en auditoría con fecha/hora y empleado
        4. Finalizar el caso de uso
        """
        print("\n>> GESTOR: Se ha tomado la selección de RECHAZAR.")
        
        if self.validarDatosEvento():
            # Cambiar el estado del evento a "Rechazado"
            self.cambiarEventoSismicoARechazado()
            
            # Finalizar el caso de uso
            self.finCU()
    
    def tomarSeleccionDerivacion(self):
        """
        NOTA DE TARJETA VIOLETA:
        Procesa la derivación del evento a un experto.
        Cambia el estado a "Pendiente de Revisión" para que
        un experto lo revise posteriormente.
        """
        print("\n>> GESTOR: Se ha tomado la selección de DERIVAR A EXPERTO.")
        
        if self.validarDatosEvento():
            # Cambiar el estado del evento a "Pendiente de Revisión"
            self.cambiarEventoSismicoAPendienteRevisionExperto()
            
            # Registrar la derivación
            print(">> GESTOR: Registrando derivación a experto...")
            self.registrarDerivacionAExperto()
            
            # Finalizar el caso de uso
            self.finCU()
            
    def llamarAlCasoDeUsoGenerarSismograma(self):
        """
        Invoca el Caso de Uso 18: Generar Sismograma.
        Genera una visualización gráfica de los datos sísmicos.
        """
        print(">> GESTOR: Llamando al CU 'Generar Sismograma'...")
        if self.seleccionado:
            SismogramaGenerator.generar_y_mostrar(self.seleccionado)
        
    def validarDatosEvento(self) -> bool:
        """
        Valida los datos del evento antes de confirmar o rechazar.
        Incluye validación de datos sísmicos y registro de auditoría.
        """
        if not self.seleccionado: 
            return False
            
        print(">> GESTOR: Validando datos del evento.")
        
        # Validar datos sísmicos del evento
        self.seleccionado.validarDatosSismo()
        
        # Validar y registrar información de auditoría
        self.validarSeleccionConfirmacion()
        
        return True

    def validarSeleccionConfirmacion(self):
        """
        Registra información de auditoría para la acción tomada.
        Incluye fecha/hora y empleado que realizó la acción.
        """
        print(">> GESTOR: Validando selección y registrando auditoría.")
        
        # Obtener y registrar fecha/hora actual
        fecha_hora = self.obtenerFechaHoraActual()
        
        # Obtener y registrar empleado de la sesión
        empleado = self.obtenerEmpleadoSesion()
        
        print(f"   -> Acción registrada: {fecha_hora} por {empleado}")

    def obtenerFechaHoraActual(self):
        """Obtiene la fecha y hora actual del sistema"""
        fecha_hora = datetime.now()
        print(f">> GESTOR: Obteniendo fecha y hora actual: {fecha_hora}")
        return fecha_hora

    def obtenerEmpleadoSesion(self):
        """Obtiene el empleado actual desde la sesión"""
        empleado = Sesion().getEmpleado()
        print(f">> GESTOR: Empleado en sesión: {empleado}")
        return empleado

    def cambiarEventoSismicoARechazado(self):
        """
        Cambia el estado del evento seleccionado a "Rechazado".
        Esto marca el evento como no válido tras la revisión manual.
        """
        if self.seleccionado:
            print(f">> GESTOR: Cambiando evento {self.seleccionado.id_sismo} a estado 'Rechazado'")
            self.seleccionado.cambiarEventoSismicoARechazado()
    
    def cambiarEventoSismicoAConfirmado(self):
        """
        Cambia el estado del evento seleccionado a "Confirmado".
        Esto valida el evento como sismo real.
        """
        if self.seleccionado:
            print(f">> GESTOR: Cambiando evento {self.seleccionado.id_sismo} a estado 'Confirmado'")
            self.seleccionado.cambiarEventoSismicoAConfirmado()
    
    def cambiarEventoSismicoAPendienteRevisionExperto(self):
        """
        Cambia el estado del evento a "Pendiente de Revisión Experto".
        Esto marca el evento para revisión especializada.
        """
        if self.seleccionado:
            print(f">> GESTOR: Cambiando evento {self.seleccionado.id_sismo} a estado 'Pendiente de Revisión Experto'")
            self.seleccionado.cambiarEstadoEventoSismico("Pendiente de Revisión Experto")
    
    def registrarDerivacionAExperto(self):
        """
        Registra la derivación del evento a un experto.
        Incluye información del analista que derivó y timestamp.
        """
        fecha_hora = self.obtenerFechaHoraActual()
        empleado = self.obtenerEmpleadoSesion()
        print(f"   -> Derivación registrada: {fecha_hora} por {empleado}")
        # Aquí se podría notificar al experto o sistema de expertos

    def finCU(self):
        """
        Finaliza el Caso de Uso actual.
        Notifica a la pantalla y reinicia el proceso para permitir nueva selección.
        """
        print("\n>> GESTOR: Fin del Caso de Uso para este evento.")
        print(">> GESTOR: El evento ha sido procesado exitosamente.")
        
        # Notificar a la pantalla que el CU ha finalizado
        self.pantalla.finCU()
        
        # NOTA: El evento procesado queda en su estado final (Rechazado, Confirmado, etc.)
        # y no aparecerá en futuras búsquedas de eventos pendientes