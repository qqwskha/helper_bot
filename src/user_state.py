# src/user_state.py
class UserState:
    def __init__(self):
        self.discipline = None
        self.practical_type = None
        self.variant = None
        self.message_id = None
        self.state = None  # Новое поле для хранения состояния

    def is_complete(self):
        return all([self.discipline, self.practical_type, self.variant])

    def reset(self):
        self.discipline = None
        self.practical_type = None
        self.variant = None
        self.message_id = None
        self.state = None
