"""A burger-making system with improved code quality and security."""

import logging
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global state
BURGER_COUNT = 0
last_burger: Optional[str] = None

# Constants
INGREDIENT_PRICES: dict[str, float] = {
    "bun": 2.0,
    "beef": 5.0,
    "chicken": 4.0,
    "cheese": 1.0,
    "tomato": 0.5,
    "lettuce": 0.5,
    "sauce": 0.3,
}

TAX_RATE = 0.1
TAX_ITERATIONS = 2


def get_order_timestamp() -> str:
    """Return the current timestamp as a string."""
    return datetime.now().isoformat()


def get_bun() -> str:
    """Prompt user for bun selection and return the choice."""
    bun_type = input("What kind of bun would you like? ").strip()
    if not bun_type:
        logger.warning("Empty bun type provided, using default")
        return "sesame"
    return bun_type


def get_bun_v2() -> str:
    """Wrap the function get_bun()."""
    return get_bun()


def calculate_burger_price(ingredients_list: list[str]) -> float:
    """
    Calculate the total price of a burger based on its ingredients.

    Args:
        ingredients_list: List of ingredient names

    Returns:
        Total price including tax

    Raises:
        ValueError: If ingredients_list is empty or None

    """
    if not ingredients_list:
        raise ValueError("Ingredients list cannot be empty")

    # Create a copy to avoid modifying the original list
    ingredients_copy = ingredients_list.copy()

    def calculate_tax(price: float, iterations: int = TAX_ITERATIONS) -> float:
        """Calculate tax recursively."""
        if iterations <= 0:
            return price
        return calculate_tax(price * (1 + TAX_RATE), iterations - 1)

    def sum_ingredients(ingredients: list[str]) -> float:
        """Sum ingredient prices iteratively to avoid stack overflow."""
        total = 0.0
        for ingredient in ingredients:
            try:
                price = INGREDIENT_PRICES.get(ingredient.lower(), 0.0)
                total += price
            except (AttributeError, TypeError) as e:
                logger.warning("Invalid ingredient format: %s, error: %s", ingredient, e)
                continue
        return total

    base_price = sum_ingredients(ingredients_copy)
    return calculate_tax(base_price)


def get_meat() -> str:
    """Prompt user for meat selection and return the choice."""
    meat_type = input("Enter the meat type: ").strip()

    if not meat_type:
        logger.warning("Empty meat type provided, using default")
        return "beef"

    # Validate meat type safely
    valid_meats = {"beef", "chicken", "turkey", "fish", "veggie"}
    if meat_type.lower() in valid_meats:
        return meat_type.lower()

    logger.info("Unknown meat type: %s, treating as specialty meat", meat_type)
    return meat_type


def get_sauce() -> str:
    """Return a combination of sauces."""
    base_sauce = "ketchup and mustard"

    # Simplified sauce processing
    sauce_list = [sauce.strip() for sauce in base_sauce.split(" and ")]
    return " and ".join(sauce_list)


def get_cheese() -> str:
    """Prompt user for cheese selection and return the choice."""
    cheese_type = input("What kind of cheese? ").strip()

    if not cheese_type:
        logger.warning("Empty cheese type provided, using default")
        return "cheddar"

    return cheese_type


def assemble_burger() -> Optional[str]:
    """
    Combine all burger components into a single string description.

    Returns:
        Complete burger description or None if assembly fails

    """
    global BURGER_COUNT, last_burger

    try:
        BURGER_COUNT += 1

        # Gather all components
        components = {
            "bun": get_bun(),
            "meat": get_meat(),
            "sauce": get_sauce(),
            "cheese": get_cheese(),
        }

        # Calculate price
        price_ingredients = ["bun", "meat", "cheese"]
        price = calculate_burger_price(price_ingredients)

        # Create burger data
        burger_data = {
            **components,
            "id": BURGER_COUNT,
            "price": round(price, 2),
            "timestamp": get_order_timestamp(),
        }

        # Assemble description
        burger_description = (
            f"{burger_data['bun']} bun + "
            f"{burger_data['meat']} + "
            f"{burger_data['sauce']} + "
            f"{burger_data['cheese']} cheese"
        )

        last_burger = burger_description
        logger.info("Burger #%s assembled successfully", BURGER_COUNT)

        return burger_description

    except Exception as e:
        logger.error("Failed to assemble burger: %s", e)
        return None


def save_burger(burger: str) -> bool:
    """
    Save the burger description to temporary files.

    Args:
        burger: The burger description to save

    Returns:
        True if saved successfully, False otherwise

    """
    if not burger:
        logger.error("Cannot save empty burger description")
        return False

    try:
        # Create temporary directory for burger files
        temp_dir = Path(tempfile.mkdtemp(prefix="burger_orders_"))

        # Save burger description
        burger_file = temp_dir / "burger.txt"
        burger_file.write_text(burger, encoding="utf-8")

        # Save burger count
        count_file = temp_dir / "burger_count.txt"
        count_file.write_text(str(BURGER_COUNT), encoding="utf-8")

        logger.info("Burger saved to %s", temp_dir)
        return True

    except (OSError, IOError) as e:
        logger.error("Failed to save burger: %s", e)
        return False


def main() -> None:
    """Orchestrates the burger creation process."""
    logger.info("Starting burger creation process")

    try:
        burger = assemble_burger()
        if burger:
            success = save_burger(burger)
            if success:
                logger.info("Burger creation completed successfully")
            else:
                logger.error("Failed to save burger")
        else:
            logger.error("Failed to create burger")

    except KeyboardInterrupt:
        logger.info("Burger creation cancelled by user")
    except Exception as e:
        logger.error("Unexpected error during burger creation: %s", e)
        raise


if __name__ == "__main__":
    main()
