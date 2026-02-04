from create_folder.classes_create import add_data_classes
from app.utils.json_loader import load_json

if __name__ == "__main__":
    data = load_json()
    add_data_classes(data)
    print("Database populated with weekly schedules.")
