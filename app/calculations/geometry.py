import math
from app.validation.validators import validate_finite, validate_range
from app.calculations.constants import BELINTERSAT_LON_DEG, GEO_ALTITUDE_KM, EARTH_RADIUS_KM
from typing import NamedTuple
from app.calculations.constants import LIGHT_SPEED

class SatelliteGeometry(NamedTuple):
    slant_range_km: float
    elevation_deg: float
    propagation_delay_ms: float 

def calculate_link_geometry(
    station_lat_deg: float,
    station_lon_deg: float,
    satellite_lon_deg: float = BELINTERSAT_LON_DEG,
    satellite_alt_km: float = GEO_ALTITUDE_KM,
    earth_radius_km: float = EARTH_RADIUS_KM
) -> SatelliteGeometry:
    """
    Рассчитывает геометрические параметры связи между наземной станцией и спутником.
    
    Возвращает расстояние в км и угол возвышения в градусах.
    """
    validate_range(station_lat_deg, -90.0, 90.0, "station_lat_deg")
    validate_range(station_lon_deg, -180.0, 180.0, "station_lon_deg")
    validate_range(satellite_lon_deg, -180.0, 180.0, "satellite_lon_deg")
    validate_finite(satellite_alt_km=satellite_alt_km, earth_radius_km=earth_radius_km)

    satellite_radius_km = earth_radius_km + satellite_alt_km

    # Перевод в радианы
    lat_rad = math.radians(station_lat_deg)
    lon_diff_rad = math.radians(satellite_lon_deg - station_lon_deg)

    # Центральный угол между станцией и подспутниковой точкой (на экваторе)
    cos_gamma = math.cos(lat_rad) * math.cos(lon_diff_rad)

    # Теорема косинусов для треугольника: Центр Земли - Станция - Спутник
    slant_range_km = math.sqrt(
        earth_radius_km**2
        + satellite_radius_km**2
        - 2 * earth_radius_km * satellite_radius_km * cos_gamma
    )
    
    # Угол возвышения (elevation angle)
    elevation_rad = math.asin((satellite_radius_km * cos_gamma - earth_radius_km) / slant_range_km)
    elevation_deg = math.degrees(elevation_rad)

    # Рассчитаем задержку сигнала (скорость света ~299792 км/с)
    propagation_delay_ms = (slant_range_km / LIGHT_SPEED) * 1000
    
    return SatelliteGeometry(
        slant_range_km=round(slant_range_km, 3),
        elevation_deg=round(elevation_deg, 2),
        propagation_delay_ms=round(propagation_delay_ms, 2)
    )


if __name__ == "__main__":
    # Тестовые данные
    # Минск: 53.9° N, 27.5° E
    minsk_lat = 53.9
    minsk_lon = 27.5
    
    try:
        print("--- Проверка расчета геометрии ---")
        
        # 1. Тест для Минска
        geo_minsk = calculate_link_geometry(minsk_lat, minsk_lon)
        print(f"Станция Минск (Lat: {minsk_lat}, Lon: {minsk_lon}):")
        print(f"  - Дистанция:    {geo_minsk.slant_range_km} км")
        print(f"  - Угол места:   {geo_minsk.elevation_deg}°")
        print(f"  - Задержка:     {geo_minsk.propagation_delay_ms} мс")
        
        # 2. Тест "Под спутником" (Экватор, та же долгота)
        # Дистанция должна быть равна высоте орбиты, угол места ~90°
        geo_ideal = calculate_link_geometry(0.0, BELINTERSAT_LON_DEG)
        print(f"\nСтанция прямо под спутником (Экватор, Lon: {BELINTERSAT_LON_DEG}):")
        print(f"  - Дистанция:    {geo_ideal.slant_range_km} км (Ожидалось ~{GEO_ALTITUDE_KM})")
        print(f"  - Угол места:   {geo_ideal.elevation_deg}° (Ожидалось 90.0)")
        print(f"  - Задержка:     {geo_ideal.propagation_delay_ms} мс")

    except Exception as e:
        print(f"Ошибка при расчете: {e}")