# modelos/estado.py

class Estado:
    def __init__(self, nombre: str):
        self.nombre = nombre
        print(f"-> Creada instancia de Estado: {self.nombre}")

    def esPendienteDeRevision(self) -> bool:
        """Verifica si el estado es 'Pendiente de Revisión'"""
        resultado = self.nombre == "Pendiente de Revisión"
        print(f"-> Estado '{self.nombre}': esPendienteDeRevision() = {resultado}")
        return resultado

    def esAutoDetectado(self) -> bool:
        """Verifica si el estado es 'Auto-Detectado'"""
        resultado = self.nombre == "Auto-Detectado"
        print(f"-> Estado '{self.nombre}': esAutoDetectado() = {resultado}")
        return resultado

    def esBloqueadoEnRevision(self) -> bool:
        """Verifica si el estado es 'Bloqueado en Revisión'"""
        resultado = self.nombre == "Bloqueado en Revisión"
        print(f"-> Estado '{self.nombre}': esBloqueadoEnRevision() = {resultado}")
        return resultado

    def esRechazado(self) -> bool:
        """Verifica si el estado es 'Rechazado'"""
        resultado = self.nombre == "Rechazado"
        print(f"-> Estado '{self.nombre}': esRechazado() = {resultado}")
        return resultado

    def esConfirmado(self) -> bool:
        """Verifica si el estado es 'Confirmado'"""
        resultado = self.nombre == "Confirmado"
        print(f"-> Estado '{self.nombre}': esConfirmado() = {resultado}")
        return resultado

    def esAmbitoEventoSismico(self) -> bool:
        """Verifica si el estado pertenece al ámbito de evento sísmico"""
        print(f"-> Estado '{self.nombre}': esAmbitoEventoSismico() = True")
        return True

    def __str__(self):
        return self.nombre

    def __repr__(self):
        return f"Estado('{self.nombre}')"