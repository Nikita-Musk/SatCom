from app.schemas.link_budget import LinkBudgetRequest 
from app.services.link_budget_service import calculate_link_budget 

def run_verification():
    # 1. Ваш JSON для проверки
    input_data = {
        "transmit_side": {
            "tx_power_w": 10.0,
            "tx_losses_db": 1.5,
            "antenna_diameter_m": 1.2,
            "antenna_efficiency": 0.65
        },
        "receive_side": {
            "antenna_diameter_m": 1.8,
            "antenna_efficiency": 0.65,
            "noise_figure_db": 1.2,
            "line_loss_db": 0.5,
            "antenna_noise_temp_k": 35.0
        },
        "propagation": {
            "ground_station": {
                "latitude_deg": 55.75,
                "longitude_deg": 37.62,
                "altitude_m": 200.0
            },
            "satellite_position": {
                "longitude_deg": 51.5,
                "altitude_km": 35786.0
            },
            "availability_pct": 99.9,
            "climate_zone": "K"
        },
        "link_params": {
            "frequency_ghz": 12.0,
            "bandwidth_hz": 36000000,
            "modulation": "QPSK",
            "fec_rate": "3/4",
            "roll_off_factor": 0.20,
            "implementation_margin_db": 1.0
        }
    }

    print("--- ЗАПУСК ПРОВЕРКИ БЮДЖЕТА ЛИНИИ ---")
    
    try:
        # 2. Валидация через Pydantic (создаем объект запроса)
        request_obj = LinkBudgetRequest(**input_data)
        
        # 3. Вызов вашей математической функции
        response = calculate_link_budget(request_obj)
        
        # 4. Красивый вывод результатов
        print("\n[ГЕОМЕТРИЯ]")
        print(f"Угол места:  {response.geometry.elevation_deg}°")
        print(f"Дистанция:   {response.geometry.slant_range_km} км")

        print("\n[ПЕРЕДАТЧИК]")
        print(f"EIRP:        {response.transmit.eirp_dbw} dBW")

        print("\n[ПОТЕРИ В ПУТИ]")
        print(f"FSPL (Свободное пространство): {response.path.fspl_db} dB")
        print(f"Атмосфера:   {response.path.atmospheric_loss_db} dB")
        print(f"Дождь:       {response.path.rain_loss_db} dB")
        print(f"ИТОГО потери:{response.path.total_path_loss_db} dB")

        print("\n[ПРИЕМНИК]")
        print(f"G/T:         {response.receive.g_over_t_db_k} dB/K")
        print(f"Шум системы: {response.receive.system_noise_temp_k} K")

        print("\n[ИТОГОВАЯ ПРОИЗВОДИТЕЛЬНОСТЬ]")
        print(f"C/N:         {response.performance.cn_db} dB")
        print(f"Eb/N0:       {response.performance.eb_n0_db} dB")
        print(f"Запас (Margin): {response.performance.link_margin_db} dB")
        
        if response.performance.is_viable:
            print("\n✅ СВЯЗЬ ВОЗМОЖНА")
        else:
            print("\n❌ СВЯЗЬ НЕВОЗМОЖНА (отрицательный запас)")

    except Exception as e:
        print(f"\nОшибка при выполнении теста: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_verification()