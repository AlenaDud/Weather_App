from pyowm import OWM
from pyowm.utils.config import get_default_config
from pyowm.commons import exceptions
from datetime import datetime, timedelta
from config import OPENWEATHER_API_KEY

config_dict = get_default_config()
config_dict["language"] = "ru"
owm = OWM(OPENWEATHER_API_KEY)

mgr = owm.weather_manager()
mgr_uv = owm.uvindex_manager()


def data_weather(place: str) -> dict:
    try:
        country_and_place = f"{place}, RU"
        observation = mgr.weather_at_place(country_and_place)
        uf = mgr_uv.uvindex_around_coords(lat=observation.location.lat, lon=observation.location.lon)
        weath = observation.weather
        delta = timedelta(hours=3, minutes=0)
        forecast = {
            "uv": uf.value,
            "status": weath.detailed_status,
            "temp": weath.temperature("celsius")["temp"],
            "wind": weath.wind()["speed"],
            "sunrise": datetime.fromisoformat(weath.sunrise_time(timeformat='iso')) + delta,
            "sunset": datetime.fromisoformat(weath.sunset_time(timeformat='iso')) + delta}

        return forecast
    except exceptions.NotFoundError:
        raise FileNotFoundError
    except exceptions.InvalidSSLCertificateError:
        raise ConnectionError
    except exceptions.UnauthorizedError:
        raise ImportError
