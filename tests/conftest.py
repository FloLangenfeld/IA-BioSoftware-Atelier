"""Pytest configuration and fixtures for burger tests."""

import pytest

import burger


@pytest.fixture(autouse=True)
def reset_global_state():
    """Reset global state before each test."""
    original_count = burger.BURGER_COUNT
    original_last = burger.last_burger

    # Reset for test
    burger.BURGER_COUNT = 0
    burger.last_burger = None

    yield

    # Restore original state
    burger.BURGER_COUNT = original_count
    burger.last_burger = original_last


@pytest.fixture
def sample_ingredients():
    """Provide sample ingredients for testing."""
    return ["bun", "beef", "cheese"]


@pytest.fixture
def mock_burger_components():
    """Provide mock burger components."""
    return {
        "bun": "sesame",
        "meat": "beef",
        "sauce": "ketchup and mustard",
        "cheese": "cheddar",
    }


@pytest.fixture
def expected_price():
    """Calculate expected price for standard burger."""
    # (bun: 2.0 + beef: 5.0 + cheese: 1.0) * 1.1 * 1.1
    return 8.0 * (1.1**2)
