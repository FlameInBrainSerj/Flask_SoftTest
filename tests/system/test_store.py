import json

from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                resp = client.post("/store/test")

                self.assertEqual(resp.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name("test"))
                self.assertDictEqual({"name": "test", "items": []},
                                     json.loads(resp.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/test")
                resp = client.post("/store/test")

                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual({'message': "A store with name '{}' already exists.".format("test")},
                                     json.loads(resp.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/test")
                resp = client.delete("/store/test")

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'Store deleted'},
                                     json.loads(resp.data))
                self.assertIsNone(StoreModel.find_by_name("test"))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get("/store/test")

                self.assertEqual(resp.status_code, 404)
                self.assertDictEqual({'message': 'Store not found'},
                                     json.loads(resp.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/test")
                client.post("/item/test_item",
                            data=json.dumps({"price": 19.99, "store_id": 1}),
                            headers={"Content-Type": "application/json"})

                resp = client.get("/store/test")
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({"name": "test",
                                      "items":
                                          [
                                              {
                                                  "name": "test_item",
                                                  "price": 19.99
                                              }
                                          ]
                                      },
                                     json.loads(resp.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/test")

                resp = client.get('/stores')

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({"stores": [{"name": "test", "items": []}]}, json.loads(resp.data))

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/test")
                client.post("/item/test_item",
                            data=json.dumps({"price": 19.99, "store_id": 1}),
                            headers={"Content-Type": "application/json"})

                resp = client.get('/stores')

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({"stores":
                                          [
                                              {
                                                  "name": "test",
                                                  "items":
                                                      [
                                                          {"name": "test_item",
                                                           "price": 19.99
                                                           }
                                                      ]
                                              }
                                          ]},
                                     json.loads(resp.data))
