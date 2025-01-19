import pytest
from delivery_project.delivery.delivery_cost import calculate_delivery_cost, validate_fragile_cargo

# --- Validation Tests ---
@pytest.mark.parametrize(
    "distance, fragile, expected",
    [
        (30, True, None),  # Допустимое расстояние для хрупкого груза
        (15, True, None),  # Допустимое расстояние для хрупкого груза
        (30, False, None),  # Не хрупкий груз
    ]
)
def test_validate_fragile_cargo_positive(distance, fragile, expected):
    assert validate_fragile_cargo(distance, fragile) == expected

@pytest.mark.parametrize(
    "distance, fragile",
    [
        (31, True),  # Недопустимое расстояние для хрупкого груза
        (40, True),  # Недопустимое расстояние для хрупкого груза
    ]
)
def test_validate_fragile_cargo_negative(distance, fragile):
    with pytest.raises(ValueError):
        validate_fragile_cargo(distance, fragile)

# --- Positive Tests ---
@pytest.mark.parametrize(
    "distance, size, fragile, workload, expected_cost",
    [
        (0, 'маленький', 'нет', 'нормальная', 400.0),  # Минимальная стоимость
        (2, 'большой', 'нет', 'повышенная', 400.0),    # Минимальная стоимость
        (15, 'маленький', 'нет', 'высокая', 420.0),    # Base: 200 + 100 = 300 * 1.4
        (15, 'большой', 'да', 'высокая', 980.0),       # Base: 200 + 200 + 300 = 700 * 1.4
        (35, 'большой', 'нет', 'очень высокая', 800.0) # Base: 300 + 200 = 500 * 1.6
    ]
)
def test_calculate_delivery_cost_positive(distance, size, fragile, workload, expected_cost):
    assert pytest.approx(calculate_delivery_cost(distance, size, fragile, workload), rel=1e-2) == expected_cost

# --- Negative Tests ---
@pytest.mark.parametrize(
    "distance, size, fragile, workload",
    [
        (10, 'средний', 'нет', 'нормальная'),   # Некорректный размер
        (10, 'маленький', 'нет', 'экстремальная'), # Некорректная загруженность
        (31, 'маленький', 'да', 'нормальная'), # Хрупкий груз на недопустимом расстоянии
    ]
)
def test_calculate_delivery_cost_negative(distance, size, fragile, workload):
    with pytest.raises(ValueError):
        calculate_delivery_cost(distance, size, fragile, workload)

# --- Boundary Tests ---
@pytest.mark.parametrize(
    "distance, size, fragile, workload, expected_cost",
    [
        (2, 'маленький', 'нет', 'нормальная', 400.0),  # Минимальная стоимость
        (10, 'маленький', 'нет', 'нормальная', 400.0),  # Минимальная стоимость
        (30, 'большой', 'нет', 'нормальная', 400.0),    # Минимальная стоимость
        (30, 'маленький', 'да', 'повышенная', 720.0)    # Base: 300 + 100 + 300 = 700 * 1.2
    ]
)
def test_calculate_delivery_cost_boundaries(distance, size, fragile, workload, expected_cost):
    assert calculate_delivery_cost(distance, size, fragile, workload) == expected_cost
