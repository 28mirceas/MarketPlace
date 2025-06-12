from databasemanager import DatabaseManager

class BaseEntity:
    def __init__(self):
        self.db_manager = DatabaseManager("baza12.db")
