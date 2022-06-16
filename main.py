import requests
import os
from sqlalchemy import create_engine, Integer, Column, String, DECIMAL, DateTime
from sqlalchemy.orm import declarative_base, Session

API_BASE_URL = 'https://api.weatherapi.com/v1/'
API_KEY = os.getenv('WEATHER_API_KEY')
CITY = 'Ahwaz'
DB_USERNAME = os.getenv('WEATHER_DB_USERNAME')
DB_PASSWORD = os.getenv('WEATHER_DB_PASSWORD')
DB_HOST = os.getenv('WEATHER_DB_HOST')
DB_NAME = os.getenv('WEATHER_DB_NAME')

engine = create_engine(f'mysql+mysqldb://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')
Base = declarative_base()


class Weather(Base):
    __tablename__ = 'weather_table'

    id = Column(Integer, primary_key=True)
    city_name = Column(String(255), nullable=False)
    temp_c = Column(DECIMAL(precision=5, scale=2))
    local_time = Column(DateTime)
    wind_kph = Column(DECIMAL(precision=5, scale=2))


Base.metadata.create_all(engine)


def get_weather():
    url = API_BASE_URL + 'current.json'
    params = {
        'q': CITY,
        'key': API_KEY,
    }

    return requests.get(
        url,
        params=params,
    ).json()


if __name__ == '__main__':
    weather_json = get_weather()
    with Session(engine) as session:
        weather = Weather(
            city_name=weather_json['location']['name'],
            temp_c=weather_json['current']['temp_c'],
            local_time=weather_json['location']['localtime'],
            wind_kph=weather_json['current']['wind_kph'],
        )
        session.add(weather)
        session.commit()
