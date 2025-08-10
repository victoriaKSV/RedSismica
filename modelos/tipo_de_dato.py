class TipoDeDato:
    def esVelocidadDeOnda(self) -> bool:
        print("-> TipoDeDato: Verificando si es Velocidad de Onda")
        return True

    def esFrecuenciaDeOnda(self) -> bool:
        print("-> TipoDeDato: Verificando si es Frecuencia de Onda")
        return False

    def esLongitud(self) -> bool:
        print("-> TipoDeDato: Verificando si es Longitud")
        return False

    def getDenominacion(self) -> str:
        print("-> TipoDeDato: Obteniendo denominación")
        return "Velocidad"