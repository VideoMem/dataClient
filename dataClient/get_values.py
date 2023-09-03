from modules.GraphiteReader import GraphiteReader
from datetime import datetime
from os import path
from modules.FSUtils import delete_older_files

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
    return f"""
Fecha: {now.strftime('%d/%m/%Y')}.
Hora: {now.strftime('%H:%M')}.

Los parámetros interiores de los invernaderos son:

Temperatura {round(reader.temperature, 1)} grados, humedad {round(reader.humidity)}%.
Iluminación {round(reader.light)} lux.
{"Es de noche." if not reader.is_day else "Es de día."}
Concentración de dióxido de carbono en el aire {int(reader.co2)} ppm.

Parámetros exteriores:
Temperatura {round(reader.external_temperature, 1)} grados.
Humedad {round(reader.external_humidity)}%.
La velocidad del viento es de {round(reader.wind_speed_kmh)} km/h con dirección {angulo_a_punto_cardinal(reader.wind_angle_deg)}.

Ventanas {'abiertas' if reader.blinds else 'cerradas'}.
Extractores {'encendidos' if reader.fans else 'apagados' }.

{"El sistema de alimentación eléctrico funciona con normalidad" if reader.power_ok else "Hay corte de energía."}
"""


if __name__ == '__main__':
    delete_older_files(path.join(path.dirname(path.abspath(__file__)), 'logs'), max_days=8)
    print(main())
