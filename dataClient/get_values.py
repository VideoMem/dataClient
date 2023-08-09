from modules.GraphiteReader import GraphiteReader
from datetime import datetime


def angulo_a_punto_cardinal(angulo):
    # Asegurarnos de que el ángulo esté entre 0 y 360
    angulo = angulo % 360

    # Definir los puntos cardinales y sus ángulos
    puntos_cardinales = {
        'Norte': (0, 22.5),
        'Noreste': (22.5, 67.5),
        'Este': (67.5, 112.5),
        'Sureste': (112.5, 157.5),
        'Sur': (157.5, 202.5),
        'Suroeste': (202.5, 247.5),
        'Oeste': (247.5, 292.5),
        'Noroeste': (292.5, 337.5),
        'NorteB': (337.5, 360)
    }

    # Buscar el punto cardinal correspondiente al ángulo
    for punto, (inicio, fin) in puntos_cardinales.items():
        if inicio <= angulo < fin:
            return punto.replace('NorteB', 'Norte')

    return 'Norte'  # Si no se encontró coincidencia, asumimos que es el norte (0 o 360 grados)


def main():
    reader = GraphiteReader()
    now = datetime.now()
    return f"""Reporte del clima:
Ubicación: Tolhuin, Tierra del Fuego, Argentina.
Fecha: {now.strftime('%d/%m/%Y')}.
Hora: {now.strftime('%H:%M')}.

Los parámetros interiores son:

Temperatura del invernadero {round(reader.temperature, 1)} grados, humedad {round(reader.humidity)}%.
La iluminación en las bancadas de cultivo es de {round(reader.light)} lux y
la concentración de dióxido de carbono en el aire es de {int(reader.co2)} ppm.
{"Es de noche." if not reader.is_day else "Es de día."}

Parámetros exteriores:
La temperatura exterior de los invernaderos es de {round(reader.external_temperature, 1)} grados,
mientras que la humedad es de {round(reader.external_humidity)}%.
La velocidad del viento es {round(reader.wind_speed_kmh)} km/h con dirección {angulo_a_punto_cardinal(reader.wind_angle_deg)}.
"""


if __name__ == '__main__':
    print(main())
