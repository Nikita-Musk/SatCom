import math

def calculate_fspl(
        frequency_hz: float,
        distanse_m: float
) -> float:
    """
    Расчёт затухания в свободном пространстве (Free Space Path Loss).
    
    Аргументы:
        frequency_hz: Частота в герцах (Гц).
        distance_m: Дистанция в метрах (м).
    
    Возвращает:
        Затухание в децибелах (дБ).
    """
    
    if distanse_m <= 0 or frequency_hz <= 0:
        raise ValueError("Дистанция и частота должны быть положительными")

    return (
        20 * math.log10(frequency_hz) + 20 * math.log10(distanse_m) - 147.55
    )