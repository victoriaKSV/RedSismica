class MuestraSismica:
    def __init__(self, fecha_hora):
        self.fecha_hora_muestra = fecha_hora
        self.detalles = []

    def agregar_detalle(self, detalle):
        self.detalles.append(detalle)

    def getDatos(self):
        """Obtener datos de la muestra sísmica"""
        print("-> MuestraSismica: getDatos()")
        return {
            "fecha_hora": self.fecha_hora_muestra,
            "cantidad_detalles": len(self.detalles),
            "detalles": self.detalles
        }