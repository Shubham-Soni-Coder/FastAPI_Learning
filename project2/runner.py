from create_folder.classes_create import check_for_upcoming_classes
from datetime import datetime, time


if __name__ == "__main__":
    todey_day = 1
    current_time = time(8, 0, 0)

    result = check_for_upcoming_classes(todey_day, current_time)

    if len(result) > 0:
        for data in result:
            print(data.name)

    else:
        print("No upcoming classes found")
