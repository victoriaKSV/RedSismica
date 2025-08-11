class SerieTemporal:
    def __init__(self):
        self.muestras = []

    def agregar_muestra(self, muestra):
        self.muestras.append(muestra)

    def getDatos(self):
        """Obtener datos de la serie temporal"""
        print("-> SerieTemporal: getDatos()")
        return {
            "cantidad_muestras": len(self.muestras),
            "muestras": self.muestras
        }