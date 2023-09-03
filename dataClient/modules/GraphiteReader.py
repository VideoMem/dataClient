from time import sleep

import numpy as np
import requests

from modules.Logger import Logger

logger = Logger.__call__().get_logger()


class GraphiteReader:

    def __init__(self, host="http://172.17.0.1:8080"):
        self.host = host

    def get_last(self, metric):
        value = None
        while value is None:
            query = f"{self.host}/render/?" \
                f"target=summarize({metric},'1hour','last')&from=-1h&format=json"
            try:
                r = requests.get(query)
                value = r.json()[0][u'datapoints'][-1][0]
            except (ConnectionError, requests.exceptions.ConnectionError) as e:
                logger.error(e)
                sleep(3)

        return value

    @property
    def temperature(self) -> float:
        return self.get_last("fitoLab.tolhuin.Temperatura")

    @property
    def humidity(self) -> float:
        return self.get_last("fitoLab.tolhuin.Humedad_relativa")

    @property
    def light(self) -> int:
        return self.get_last("fitoLab.tolhuin.Luz")

    @property
    def co2(self) -> int:
        return self.get_last("fitoLab.tolhuin.CO2")

    @property
    def external_temperature(self) -> float:
        return self.get_last("fitoLab.tolhuin.Temperatura_exterior")

    @property
    def external_humidity(self) -> float:
        return self.get_last("fitoLab.tolhuin.Humedad_relativa_exterior")

    @property
    def wind_speed_kmh(self) -> float:
        return self.get_last("fitoLab.tolhuin.Velocidad_del_viento") * 3.6

    @property
    def blinds(self) -> bool:
        return self.get_last("fitoLab.tolhuin.Persianas") == 1

    @property
    def fans(self) -> bool:
        return self.get_last("fitoLab.tolhuin.Extractores") == 1

    @property
    def power_ok(self) -> bool:
        return self.get_last("fitoLab.tolhuin.ups.input_voltage") > 180

    @property
    def wind_angle_deg(self) -> float:
        return 360.0 - self.get_last("fitoLab.tolhuin.Angulo_del_viento")

    @property
    def wind_angle_rad(self) -> float:
        return (self.wind_angle_deg * 2 * np.pi / 360.0) + (np.pi / 2)

    @property
    def is_day(self) -> bool:
        return self.light >= 10.0

