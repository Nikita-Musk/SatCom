BOLTZMANN_DB = -228.6 # дБ(Вт/К/Гц) или дБ(м²·кг·с⁻²·К⁻¹)
LIGHT_SPEED = 299792458 # м/с
ANTENNA_GAIN_CONSTANT = 20.4 # 20*log10(π·10⁹/c) — усиление антенны (f в ГГц)
FSPL_CONSTANT = 92.45
# Таблица требуемых Eb/N0 по DVB-S2 (модуляция → FEC → Eb/N0 дБ)
REQUIRED_EB_N0: dict[tuple[str, str], float] = {
    ("BPSK",   "1/2"): 4.5,
    ("QPSK",   "1/2"): 4.5,
    ("QPSK",   "2/3"): 5.5,
    ("QPSK",   "3/4"): 6.0,
    ("QPSK",   "4/5"): 6.5,
    ("QPSK",   "7/8"): 7.0,
    ("8PSK",   "2/3"): 8.0,
    ("8PSK",   "3/4"): 9.0,
    ("8PSK",   "4/5"): 9.5,
    ("8PSK",   "7/8"): 10.0,
    ("16APSK", "2/3"): 10.0,
    ("16APSK", "3/4"): 11.0,
    ("16APSK", "4/5"): 11.5,
    ("16APSK", "7/8"): 12.0,
    ("32APSK", "3/4"): 13.0,
    ("32APSK", "4/5"): 13.7,
    ("32APSK", "7/8"): 14.5,
}
# Порядок модуляции (бит на символ)
MODULATION_ORDER: dict[str, int] = {
    "BPSK":   1,
    "QPSK":   2,
    "8PSK":   3,
    "16APSK": 4,
    "32APSK": 5,
}

FEC_RATE_VALUE: dict[str, float] = {
    "1/2": 0.5,
    "2/3": 2/3,
    "3/4": 0.75,
    "4/5": 0.8,
    "7/8": 0.875,
}
# Координаты Belintersat-1
BELINTERSAT_LON_DEG = 51.5
GEO_ALTITUDE_KM = 35786.0
EARTH_RADIUS_KM = 6371.0

