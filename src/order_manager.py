# src/order_manager.py
class OrderManager:
    def __init__(self, payment_token):
        self.payment_token = payment_token

    def create_invoice(self, user_id, order_details, price):
        return {
            "chat_id": user_id,
            "title": "Практическая работа",
            "description": order_details,
            "payload": "custom_payload",  # Уникальный идентификатор заказа
            "provider_token": self.payment_token,
            "currency": "RUB",  # Валюта (рубли)
            "prices": [{"label": "Практическая работа", "amount": price * 100}],  # Цена в копейках
            "start_parameter": "payment",  # Параметр для начала платежа
        }