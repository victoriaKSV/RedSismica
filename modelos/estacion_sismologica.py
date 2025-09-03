# CORRECCIÓN 6: modelos/estacion_sismologica.py
# Agregar más estaciones sismológicas

class EstacionSismologica:
    # Diccionario de estaciones disponibles
    ESTACIONES = {
        "CBA-01": {"nombre": "Córdoba Central", "lat": -31.4201, "lon": -64.1888},
        "CBA-02": {"nombre": "Córdoba Norte", "lat": -31.3501, "lon": -64.1788},
        "CBA-03": {"nombre": "Córdoba Sur", "lat": -31.4901, "lon": -64.1988},
        "MDZ-01": {"nombre": "Mendoza Central", "lat": -32.8908, "lon": -68.8272},
        "SJN-01": {"nombre": "San Juan Central", "lat": -31.5351, "lon": -68.5364},
    }
    
    def __init__(self, codigo="CBA-01"):
        self.codigo = codigo
        self.info = self.ESTACIONES.get(codigo, self.ESTACIONES["CBA-01"])
    
    def getCodigoEstacion(self) -> str:
        print(f"-> EstacionSismologica: Obteniendo código de estación: {self.codigo}")
        return self.codigo
    
    def getNombreEstacion(self) -> str:
        return self.info["nombre"]
    
    def getCoordenadas(self) -> tuple:
        return (self.info["lat"], self.info["lon"])