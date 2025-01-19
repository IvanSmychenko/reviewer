from delivery_project.delivery.delivery_cost import calculate_delivery_cost, WORKLOAD_OPTIONS

if __name__ == "__main__":
    try:
        # Ввод данных
        distance = float(input("Введите расстояние до пункта назначения (км): "))
        size_input = input("Введите размер груза ('маленький' или 'большой'): ").strip().lower()
        fragile_input = input("Хрупкий груз? Введите 'Да' или 'Нет': ").strip().lower()
        workload_input = input("Введите загруженность службы доставки ('очень высокая', 'высокая', 'повышенная', 'нормальная'): ").strip().lower()

        # Расчет стоимости
        cost = calculate_delivery_cost(distance, size_input, fragile_input, workload_input)
        print(f"Стоимость доставки: {cost} руб.")

    except Exception as e:
        print(f"Ошибка: {e}")
