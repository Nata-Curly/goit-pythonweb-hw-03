import json
import os


class DataHandler:
    """Класс для завантаження та збереження даних у JSON-файлі"""

    def __init__(self, filepath):
        self.filepath = filepath

    def load_data(self):
        if not os.path.exists(self.filepath) or os.stat(self.filepath).st_size == 0:
            return {}
        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}

    def save_data(self, new_data):
        data = self.load_data()
        data.update(new_data)
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
