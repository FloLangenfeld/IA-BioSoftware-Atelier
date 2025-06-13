"""Unit tests for the burger-making system."""

# Assuming burger.py is in src/ directory
import sys
from datetime import datetime
from unittest.mock import Mock, patch

import pytest

sys.path.append("src")
import burger


class TestGetOrderTimestamp:
    """Tests for get_order_timestamp function."""

    def test_returns_string(self):
        """Test that function returns a string."""
        result = burger.get_order_timestamp()
        assert isinstance(result, str)

    def test_returns_iso_format(self):
        """Test that timestamp is in ISO format."""
        result = burger.get_order_timestamp()
        # Should be parseable as datetime
        parsed = datetime.fromisoformat(result)
        assert isinstance(parsed, datetime)

    @patch("burger.datetime")
    def test_uses_current_datetime(self, mock_datetime):
        """Test that function uses current datetime."""
        mock_now = Mock()
        mock_now.isoformat.return_value = "2024-01-01T12:00:00"
        mock_datetime.now.return_value = mock_now

        result = burger.get_order_timestamp()

        mock_datetime.now.assert_called_once()
        mock_now.isoformat.assert_called_once()
        assert result == "2024-01-01T12:00:00"


class TestGetBun:
    """Tests for get_bun function."""

    @patch("builtins.input", return_value="sesame")
    def test_returns_user_input(self, mock_input):
        """Test that function returns user input."""
        result = burger.get_bun()
        assert result == "sesame"
        mock_input.assert_called_once_with("What kind of bun would you like? ")

    @patch("builtins.input", return_value="  whole wheat  ")
    def test_strips_whitespace(self, mock_input):
        """Test that function strips whitespace from input."""
        result = burger.get_bun()
        assert result == "whole wheat"

    @patch("builtins.input", return_value="")
    @patch("burger.logger")
    def test_empty_input_returns_default(self, mock_logger, mock_input):
        """Test that empty input returns default value."""
        result = burger.get_bun()
        assert result == "sesame"
        mock_logger.warning.assert_called_once()


class TestGetBunV2:
    """Tests for get_bun_v2 function."""

    @patch("burger.get_bun", return_value="brioche")
    def test_calls_get_bun(self, mock_get_bun):
        """Test that function calls get_bun."""
        result = burger.get_bun_v2()
        assert result == "brioche"
        mock_get_bun.assert_called_once()


class TestCalculateBurgerPrice:
    """Tests for calculate_burger_price function."""

    def test_valid_ingredients(self):
        """Test price calculation with valid ingredients."""
        ingredients = ["bun", "beef", "cheese"]
        result = burger.calculate_burger_price(ingredients)

        # Expected: (2.0 + 5.0 + 1.0) * 1.1 * 1.1 = 9.68
        expected = 8.0 * (1.1 ** 2)
        assert abs(result - expected) < 0.01

    def test_empty_ingredients_raises_error(self):
        """Test that empty ingredients list raises ValueError."""
        with pytest.raises(ValueError, match="Ingredients list cannot be empty"):
            burger.calculate_burger_price([])

    def test_none_ingredients_raises_error(self):
        """Test that None ingredients raises ValueError."""
        with pytest.raises(ValueError, match="Ingredients list cannot be empty"):
            burger.calculate_burger_price(None)

    def test_unknown_ingredients(self):
        """Test handling of unknown ingredients."""
        ingredients = ["bun", "unknown_ingredient", "cheese"]
        result = burger.calculate_burger_price(ingredients)

        # Should only count bun (2.0) and cheese (1.0)
        expected = 3.0 * (1.1 ** 2)
        assert abs(result - expected) < 0.01

    def test_case_insensitive_ingredients(self):
        """Test that ingredient matching is case insensitive."""
        ingredients = ["BUN", "BEEF", "CHEESE"]
        result = burger.calculate_burger_price(ingredients)

        expected = 8.0 * (1.1 ** 2)
        assert abs(result - expected) < 0.01

    def test_original_list_not_modified(self):
        """Test that original ingredients list is not modified."""
        ingredients = ["bun", "beef", "cheese"]
        original = ingredients.copy()

        burger.calculate_burger_price(ingredients)

        assert ingredients == original

    @patch("burger.logger")
    def test_invalid_ingredient_format_logs_warning(self, mock_logger):
        """Test logging when ingredient format is invalid."""
        ingredients = ["bun", None, 123, "cheese"]
        burger.calculate_burger_price(ingredients)

        # Should log warnings for None and 123
        assert mock_logger.warning.call_count >= 1


class TestGetMeat:
    """Tests for get_meat function."""

    @patch("builtins.input", return_value="chicken")
    def test_valid_meat_type(self, mock_input):
        """Test with valid meat type."""
        result = burger.get_meat()
        assert result == "chicken"

    @patch("builtins.input", return_value="BEEF")
    def test_case_normalization(self, mock_input):
        """Test that valid meat types are normalized to lowercase."""
        result = burger.get_meat()
        assert result == "beef"

    @patch("builtins.input", return_value="wagyu")
    @patch("burger.logger")
    def test_unknown_meat_type(self, mock_logger, mock_input):
        """Test handling of unknown meat types."""
        result = burger.get_meat()
        assert result == "wagyu"
        mock_logger.info.assert_called_once()

    @patch("builtins.input", return_value="")
    @patch("burger.logger")
    def test_empty_meat_returns_default(self, mock_logger, mock_input):
        """Test that empty input returns default meat."""
        result = burger.get_meat()
        assert result == "beef"
        mock_logger.warning.assert_called_once()

    @patch("builtins.input", return_value="  turkey  ")
    def test_strips_whitespace(self, mock_input):
        """Test that whitespace is stripped."""
        result = burger.get_meat()
        assert result == "turkey"


class TestGetSauce:
    """Tests for get_sauce function."""

    def test_returns_expected_sauce(self):
        """Test that function returns expected sauce combination."""
        result = burger.get_sauce()
        assert result == "ketchup and mustard"

    def test_returns_string(self):
        """Test that function returns a string."""
        result = burger.get_sauce()
        assert isinstance(result, str)


class TestGetCheese:
    """Tests for get_cheese function."""

    @patch("builtins.input", return_value="cheddar")
    def test_returns_user_input(self, mock_input):
        """Test that function returns user input."""
        result = burger.get_cheese()
        assert result == "cheddar"

    @patch("builtins.input", return_value="")
    @patch("burger.logger")
    def test_empty_input_returns_default(self, mock_logger, mock_input):
        """Test that empty input returns default cheese."""
        result = burger.get_cheese()
        assert result == "cheddar"
        mock_logger.warning.assert_called_once()

    @patch("builtins.input", return_value="  swiss  ")
    def test_strips_whitespace(self, mock_input):
        """Test that whitespace is stripped."""
        result = burger.get_cheese()
        assert result == "swiss"


class TestAssembleBurger:
    """Tests for assemble_burger function."""

    def setup_method(self):
        """Reset global state before each test."""
        burger.BURGER_COUNT = 0
        burger.last_burger = None

    @patch("burger.get_bun", return_value="sesame")
    @patch("burger.get_meat", return_value="beef")
    @patch("burger.get_sauce", return_value="ketchup and mustard")
    @patch("burger.get_cheese", return_value="cheddar")
    @patch("burger.calculate_burger_price", return_value=10.50)
    def test_successful_assembly(self, mock_price, mock_cheese, mock_sauce, mock_meat, mock_bun):
        """Test successful burger assembly."""
        result = burger.assemble_burger()

        expected = "sesame bun + beef + ketchup and mustard + cheddar cheese"
        assert result == expected
        assert burger.BURGER_COUNT == 1
        assert burger.last_burger == expected

    @patch("burger.get_bun", side_effect=Exception("Input error"))
    @patch("burger.logger")
    def test_assembly_failure(self, mock_logger, mock_bun):
        """Test handling of assembly failure."""
        result = burger.assemble_burger()

        assert result is None
        mock_logger.error.assert_called_once()

    @patch("burger.get_bun", return_value="whole wheat")
    @patch("burger.get_meat", return_value="chicken")
    @patch("burger.get_sauce", return_value="mayo")
    @patch("burger.get_cheese", return_value="swiss")
    @patch("burger.calculate_burger_price", return_value=12.75)
    def test_burger_count_increments(self, mock_price, mock_cheese, mock_sauce, mock_meat, mock_bun):
        """Test that burger count increments properly."""
        burger.assemble_burger()
        burger.assemble_burger()

        assert burger.BURGER_COUNT == 2


class TestSaveBurger:
    """Tests for save_burger function."""

    def test_empty_burger_returns_false(self):
        """Test that empty burger description returns False."""
        result = burger.save_burger("")
        assert result is False

    def test_none_burger_returns_false(self):
        """Test that None burger description returns False."""
        result = burger.save_burger(None)
        assert result is False

    @patch("burger.tempfile.mkdtemp")
    @patch("burger.Path")
    @patch("burger.logger")
    def test_successful_save(self, mock_logger, mock_path, mock_mkdtemp):
        """Test successful burger save."""
        # Setup mocks
        mock_temp_dir = "/tmp/burger_test"
        mock_mkdtemp.return_value = mock_temp_dir

        mock_path_instance = Mock()
        mock_burger_file = Mock()
        mock_count_file = Mock()

        mock_path.return_value = mock_path_instance
        mock_path_instance.__truediv__ = Mock(side_effect=[mock_burger_file, mock_count_file])

        # Test
        result = burger.save_burger("test burger")

        # Assertions
        assert result is True
        mock_burger_file.write_text.assert_called_once_with("test burger", encoding="utf-8")
        mock_count_file.write_text.assert_called_once()
        mock_logger.info.assert_called_once()

    @patch("burger.tempfile.mkdtemp", side_effect=OSError("Permission denied"))
    @patch("burger.logger")
    def test_save_failure(self, mock_logger, mock_mkdtemp):
        """Test handling of save failure."""
        result = burger.save_burger("test burger")

        assert result is False
        mock_logger.error.assert_called_once()


class TestMain:
    """Tests for main function."""

    def setup_method(self):
        """Reset global state before each test."""
        burger.BURGER_COUNT = 0
        burger.last_burger = None

    @patch("burger.assemble_burger", return_value="test burger")
    @patch("burger.save_burger", return_value=True)
    @patch("burger.logger")
    def test_successful_execution(self, mock_logger, mock_save, mock_assemble):
        """Test successful main execution."""
        burger.main()

        mock_assemble.assert_called_once()
        mock_save.assert_called_once_with("test burger")
        mock_logger.info.assert_called()

    @patch("burger.assemble_burger", return_value=None)
    @patch("burger.logger")
    def test_assembly_failure(self, mock_logger, mock_assemble):
        """Test handling when burger assembly fails."""
        burger.main()

        mock_assemble.assert_called_once()
        mock_logger.error.assert_called()

    @patch("burger.assemble_burger", return_value="test burger")
    @patch("burger.save_burger", return_value=False)
    @patch("burger.logger")
    def test_save_failure(self, mock_logger, mock_save, mock_assemble):
        """Test handling when burger save fails."""
        burger.main()

        mock_logger.error.assert_called()

    @patch("burger.assemble_burger", side_effect=KeyboardInterrupt())
    @patch("burger.logger")
    def test_keyboard_interrupt(self, mock_logger, mock_assemble):
        """Test handling of keyboard interrupt."""
        burger.main()

        mock_logger.info.assert_called_with("Burger creation cancelled by user")

    @patch("burger.assemble_burger", side_effect=Exception("Unexpected error"))
    @patch("burger.logger")
    def test_unexpected_error_raises(self, mock_logger, mock_assemble):
        """Test that unexpected errors are re-raised."""
        with pytest.raises(Exception, match="Unexpected error"):
            burger.main()

        mock_logger.error.assert_called()
