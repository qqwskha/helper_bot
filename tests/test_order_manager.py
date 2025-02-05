import unittest

from src.order_manager import OrderManager


class TestOrderManager(unittest.TestCase):
    def setUp(self):
        self.manager = OrderManager("test_token")

    def test_create_invoice(self):
        invoice = self.manager.create_invoice(12345, "Test order details")
        self.assertEqual(invoice["chat_id"], 12345)
        self.assertEqual(invoice["title"], "Практическая работа")
        self.assertEqual(invoice["description"], "Test order details")
        self.assertEqual(invoice["provider_token"], "test_token")
        self.assertEqual(invoice["currency"], "RUB")
        self.assertEqual(invoice["prices"][0]["amount"], 500 * 100)


if __name__ == '__main__':
    unittest.main()
