class TipoDeDato:
    def __init__(self, nombre_tipo):
        self.nombre_tipo = nombre_tipo

    def esVelocidadDeOnda(self) -> bool:
        """Verificar si es Velocidad de Onda"""
        resultado = self.nombre_tipo == "velocidad_onda"
        print(f"-> TipoDeDato: esVelocidadDeOnda() = {resultado}")
        return resultado

    def esFrecuenciaDeOnda(self) -> bool:
        """Verificar si es Frecuencia de Onda"""
        resultado = self.nombre_tipo == "frecuencia_onda"
        print(f"-> TipoDeDato: esFrecuenciaDeOnda() = {resultado}")
        return resultado

    def esLongitud(self) -> bool:
        """Verificar si es Longitud"""
        resultado = self.nombre_tipo == "longitud_onda"
        print(f"-> TipoDeDato: esLongitud() = {resultado}")
        return resultado

    def getDenominacion(self) -> str:
        """Obtener denominación del tipo de dato"""
        denominaciones = {
            "velocidad_onda": "Velocidad",
            "frecuencia_onda": "Frecuencia", 
            "longitud_onda": "Longitud"
        }
        denominacion = denominaciones.get(self.nombre_tipo, "Desconocido")
        print(f"-> TipoDeDato: getDenominacion() = {denominacion}")
        return denominacion