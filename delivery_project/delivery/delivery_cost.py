WORKLOAD_COEFFICIENTS = {
    'very_high': 1.6,
    'high': 1.4,
    'increased': 1.2,
    'normal': 1.0
}

WORKLOAD_OPTIONS = {
    'очень высокая': 'very_high',
    'высокая': 'high',
    'повышенная': 'increased',
    'нормальная': 'normal'
}

MINIMUM_COST = 400

def validate_fragile_cargo(distance, fragile):
    if fragile and distance > 30:
        raise ValueError("Хрупкие грузы нельзя доставлять на расстояние более 30 км.")

def preprocess_inputs(size_input, fragile_input, workload_input):
    """
    Преобразует пользовательский ввод в формат, понятный алгоритму.
    """
    # Обработка размера
    size_mapping = {'маленький': 'small', 'большой': 'large'}
    size = size_mapping.get(size_input)
    if size is None:
        raise ValueError("Некорректный размер груза. Используйте 'маленький' или 'большой'.")

    # Обработка хрупкости
    fragile_mapping = {'да': True, 'нет': False}
    fragile = fragile_mapping.get(fragile_input)
    if fragile is None:
        raise ValueError("Некорректное значение для хрупкости. Используйте 'Да' или 'Нет'.")

    # Обработка загруженности
    workload = WORKLOAD_OPTIONS.get(workload_input)
    if workload is None:
        raise ValueError("Некорректное значение загруженности. Используйте: 'очень высокая', 'высокая', 'повышенная', 'нормальная'.")

    return size, fragile, workload

def calculate_delivery_cost(distance, size_input, fragile_input, workload_input):
    """
    Рассчитывает стоимость доставки с учетом обработки пользовательского ввода.
    """
    # Обработка пользовательских данных
    size, fragile, workload = preprocess_inputs(size_input, fragile_input, workload_input)

    # Проверка ограничения для хрупкого груза
    validate_fragile_cargo(distance, fragile)

    # Базовая стоимость доставки в зависимости от расстояния
    if distance > 30:
        base_cost = 300
    elif distance > 10:
        base_cost = 200
    elif distance > 2:
        base_cost = 100
    else:
        base_cost = 50

    # Добавление стоимости в зависимости от габаритов груза
    if size == 'large':
        base_cost += 200
    elif size == 'small':
        base_cost += 100

    if fragile:
        base_cost += 300

    # Определение коэффициента загруженности
    coefficient = WORKLOAD_COEFFICIENTS[workload]
    total_cost = base_cost * coefficient

    # Применение минимальной стоимости доставки
    return max(total_cost, MINIMUM_COST)