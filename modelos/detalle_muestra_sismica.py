from .tipo_de_dato import TipoDeDato

class DetalleMuestraSismica:
    def __init__(self, tipo_dato, valor):
        self.tipo_dato = tipo_dato
        self.valor = valor
        self._tipo_de_dato_obj = TipoDeDato(tipo_dato)  # Crear instancia del objeto TipoDeDato

    def getDatos(self):
        """Obtener datos del detalle de muestra sísmica"""
        print("-> DetalleMuestraSismica: getDatos()")
        return {
            "tipo_dato": self.tipo_dato,
            "valor": self.valor
        }

    def getTipoDeDato(self):
        """Obtener objeto TipoDeDato asociado"""
        print("-> DetalleMuestraSismica: getTipoDeDato()")
        return self._tipo_de_dato_obj