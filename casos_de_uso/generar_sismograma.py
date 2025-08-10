# casos_de_uso/generar_sismograma.py

import matplotlib.pyplot as plt
import numpy as np

class SismogramaGenerator:
    """
    Componente que encapsula la lógica del Caso de Uso N°18: Generar Sismograma.
    """
    @staticmethod
    def generar_y_mostrar(sismo):
        if not sismo.series_temporales or not sismo.series_temporales[0].muestras:
            print("ADVERTENCIA: No se encontraron datos de series temporales para graficar.")
            return

        # Extraer los datos de la estructura de objetos
        tiempos_dt = [muestra.fecha_hora_muestra for muestra in sismo.series_temporales[0].muestras]
        amplitudes = []
        
        # Buscamos el detalle específico de 'velocidad_onda'
        for muestra in sismo.series_temporales[0].muestras:
            valor_velocidad = 0 # Valor por defecto si no se encuentra
            for detalle in muestra.detalles:
                if detalle.tipo_dato == "velocidad_onda":
                    valor_velocidad = detalle.valor
                    break
            amplitudes.append(valor_velocidad)

        # Convertimos las fechas a segundos desde el inicio para el eje X
        inicio = tiempos_dt[0]
        tiempos_segundos = [(t - inicio).total_seconds() for t in tiempos_dt]

        plt.figure(figsize=(10, 4))
        plt.plot(tiempos_segundos, amplitudes, color='royalblue')

        titulo = f"Sismograma - Evento: {sismo.id_sismo}\nMagnitud: {sismo.getValorMagnitud()} Richter"
        plt.title(titulo)
        plt.xlabel("Tiempo (segundos desde el inicio de la muestra)")
        plt.ylabel("Amplitud (velocidad de onda)")
        plt.grid(True)
        plt.tight_layout()
        plt.show(block=False)