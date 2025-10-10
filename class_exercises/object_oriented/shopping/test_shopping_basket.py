import pytest
from class_exercises.object_oriented.shopping.shopping_basket import Item, ShoppingBasket


@pytest.fixture
def setup_items_and_basket():
    # Create items
    tomatoSoup = Item("Tomato Soup", "200mL can", 0.70, 20)
    spaghetti = Item("Spaghetti", "500g pack", 1.10, 20)
    blackOlives = Item("Black Olives Jar", "200g Jar", 2.10, 20)
    mozarella = Item("Mozarella", "100g", 1.50, 20)
    gratedCheese = Item("Grated Cheese", "100g", 2.20, 29)

    # Create basket and add items
    basket = ShoppingBasket()
    basket.addItem(tomatoSoup, 4)
    basket.addItem(blackOlives, 1)
    basket.addItem(mozarella, 2)
    basket.addItem(tomatoSoup, 6)

    return basket, tomatoSoup, spaghetti, blackOlives, mozarella, gratedCheese


def test_shopping_basket_setup(setup_items_and_basket):
    """ Test basket has been set up correctly """
    basket, tomatoSoup, *other = setup_items_and_basket
    assert basket.items[tomatoSoup] == 10
    assert tomatoSoup.stock == 10


def test_add_more_than_stock(setup_items_and_basket):
    """ Test adding more items than exist in stock"""
    basket, tomatoSoup, *other = setup_items_and_basket
    # Raise an error if you try to add more items than exist in stock.
    # TODO - maybe this should be to add only what exists in stock
    with pytest.raises(ValueError):
        basket.addItem(tomatoSoup, 20)


def test_add_item():
    assert False


def test_remove_item():
    assert False


def test_update_item():
    assert False


def test_reset():
    assert False
