class Sismografo:
    def sosDeSismografo(self) -> bool:
        print("-> Sismografo: Verificando si es de sismógrafo")
        return True

    def getEstacionSismologica(self):
        print("-> Sismografo: Obteniendo estación sismológica asociada")
        from .estacion_sismologica import EstacionSismologica
        return EstacionSismologica()