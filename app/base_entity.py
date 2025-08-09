from .databasemanager import DatabaseManager

class BaseEntity:
    def __init__(self, db_manager=None):
        if db_manager is None:
            self.db_manager = DatabaseManager("baza12.db")
        else:
            self.db_manager = db_manager
