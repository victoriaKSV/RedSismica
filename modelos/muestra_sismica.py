class MuestraSismica:
    def __init__(self, fecha_hora):
        self.fecha_hora_muestra = fecha_hora
        self.detalles = []

    def agregar_detalle(self, detalle):
        self.detalles.append(detalle)