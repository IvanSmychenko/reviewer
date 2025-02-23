import pytest
from delivery_project.delivery.delivery_cost import (
    calculate_delivery_cost,
    validate_fragile_cargo,
    WORKLOAD_COEFFICIENTS,
    MINIMUM_COST
)

# Определяем возможные параметры из кода
WORKLOAD_LABELS = {v: k for k, v in WORKLOAD_COEFFICIENTS.items()}  # Инверсия словаря коэффициентов

# --- Validation Tests ---
@pytest.mark.parametrize(
    "distance, fragile",
    [
        (30, True),  # Допустимое расстояние для хрупкого груза
        (15, True),  # Допустимое расстояние для хрупкого груза
        (30, False),  # Не хрупкий груз
    ]
)
def test_validate_fragile_cargo_positive(distance, fragile):
    assert validate_fragile_cargo(distance, fragile) is None

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
    "distance, size, fragile, workload_label",
    [
        (0, 'маленький', 'нет', 'нормальная'),
        (2, 'большой', 'нет', 'повышенная'),
        (15, 'маленький', 'нет', 'высокая'),
        (15, 'большой', 'да', 'высокая'),
        (35, 'большой', 'нет', 'очень высокая')
    ]
)
def test_calculate_delivery_cost_positive(distance, size, fragile, workload_label):
    expected_cost = calculate_delivery_cost(distance, size, fragile, workload_label)  # Динамический расчет

    assert pytest.approx(
        calculate_delivery_cost(distance, size, fragile, workload_label), rel=1e-2
    ) == expected_cost

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
    "distance, size, fragile, workload_label",
    [
        (2, 'маленький', 'нет', 'нормальная'),
        (10, 'маленький', 'нет', 'нормальная'),
        (30, 'большой', 'нет', 'нормальная'),
        (30, 'маленький', 'да', 'повышенная')
    ]
)
def test_calculate_delivery_cost_boundaries(distance, size, fragile, workload_label):
    expected_cost = calculate_delivery_cost(distance, size, fragile, workload_label)  # Динамический расчет

    assert pytest.approx(
        calculate_delivery_cost(distance, size, fragile, workload_label), rel=1e-2
    ) == expected_cost
