from app.utils.json_loader import load_json
from app.utils.seeder import DataBaseCreate

if __name__ == "__main__":
    data = load_json()
    creater = DataBaseCreate(data)
    creater.CreateBatchSubjects()
