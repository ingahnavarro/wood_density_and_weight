import pytest
from wood_density import WoodProperties, ElementProperties, WeightCalculator


@pytest.fixture
def example_material():
    """
    Creates a sample WoodProperties object for testing.
    """
    return WoodProperties(specific_gravity=0.7, fibre_saturation_point=25.0)


@pytest.fixture
def example_element():
    """
    Creates a sample ElementProperties object for testing.
    """
    return ElementProperties(width=0.2, depth=0.05, length=2.5)


def test_weight_calculator_valid_input(example_material, example_element):
    """
    Test the weight calculation with valid inputs.
    """
    calculator = WeightCalculator(example_material, example_element)
    weight = calculator.calculate_weight_at_moisture_content(12.0)
    assert isinstance(weight, float)
    assert weight > 0


def test_weight_calculator_invalid_moisture_content_type(example_material, example_element):
    """
    Test the weight calculation with invalid moisture content type.
    """
    calculator = WeightCalculator(example_material, example_element)
    with pytest.raises(TypeError):
        calculator.calculate_weight_at_moisture_content("invalid")


def test_weight_calculator_invalid_moisture_content_value(example_material, example_element):
    """
    Test the weight calculation with invalid moisture content value.
    """
    calculator = WeightCalculator(example_material, example_element)
    with pytest.raises(ValueError):
        calculator.calculate_weight_at_moisture_content(-5)


@pytest.mark.parametrize(
    "invalid_width, invalid_depth, invalid_length",
    [
        (-0.05, 0.15, 2.0),
        (0.05, -0.15, 2.0),
        (0.05, 0.15, -2.0),
    ],
)
def test_weight_calculator_invalid_element_dimensions( #Claridad: Added descriptive name
    example_material, invalid_width, invalid_depth, invalid_length
):
    """
    Test the weight calculation with invalid element dimensions.
    """
    element = ElementProperties(
        width=invalid_width, depth=invalid_depth, length=invalid_length
    )
    calculator = WeightCalculator(example_material, element)
    with pytest.raises(ValueError):
        calculator.calculate_weight_at_moisture_content(10)


def test_weight_calculator_density_at_moisture_content_valid(example_material, example_element):
    """
    Test the density calculation with valid inputs.
    """
    calculator = WeightCalculator(example_material, example_element)
    density = calculator.calculate_density_at_moisture_content(12.0)
    assert isinstance(density, float)
    assert density > 0


def test_weight_calculator_density_at_moisture_content_invalid_type(example_material, example_element):
    """
    Test the density calculation with invalid moisture content type.
    """
    calculator = WeightCalculator(example_material, example_element)
    with pytest.raises(TypeError):
        calculator.calculate_density_at_moisture_content("invalid")


def test_weight_calculator_density_at_moisture_content_invalid_value(example_material, example_element):
    """
    Test the density calculation with invalid moisture content value.
    """
    calculator = WeightCalculator(example_material, example_element)
    with pytest.raises(ValueError):
        calculator.calculate_density_at_moisture_content(-5)


def test_weight_calculator_density_at_moisture_content_invalid_saturation_point(example_element): #Mejora: Changed name to example for clarity
    """
    Test the density calculation with invalid fibre saturation point.
    """
    material = WoodProperties(
         specific_gravity=0.7, fibre_saturation_point=-25.0
    )
    calculator = WeightCalculator(material, example_element)
    with pytest.raises(ValueError):
        calculator.calculate_density_at_moisture_content(10)