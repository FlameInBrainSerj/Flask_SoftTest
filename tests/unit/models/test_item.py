from tests.unit.unit_base_test import UnitBaseTest

from models.item import ItemModel


class ItemTest(UnitBaseTest):   # to avoid extra importing of unused classes
    def test_create_item(self):
        item = ItemModel("test", 19.99, 1)

        self.assertEqual(item.name,
                         "test",
                         "The name of the item after creation does not equal the constructor argument.")
        self.assertEqual(item.price,
                         19.99,
                         "The name of the item after creation does not equal the constructor argument.")
        self.assertEqual(item.store_id, 1)
        self.assertIsNone(item.store)

    def test_json(self):
        item = ItemModel("test", 19.99, 1)
        expected = {
            "name": 'test',
            "price": 19.99
        }

        self.assertDictEqual(item.json(),
                             expected,
                             f"The JSON export of the item is incorrect. Received {item.json()}, expected {expected}")