# modelos/estado.py

class Estado:
    def __init__(self, nombre: str):
        self.nombre = nombre
        print(f"-> Creada instancia de Estado: {self.nombre}")

    def esPendienteDeRevision(self) -> bool:
        return self.nombre == "Pendiente de Revisión"

    def esAutoDetectado(self) -> bool:
        return self.nombre == "Auto-Detectado"

    def esAmbitoEventoSismico(self) -> bool:
        return True