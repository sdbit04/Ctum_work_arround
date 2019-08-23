import os
Base_directory = r"D:\D_drive_BACKUP\MENTOR\BATELCO\CTUM_Collection_workarround\Test"


def get_dates_dir(etc_dir):
    date_dirs = []
    for dir in os.listdir(etc_dir):
        abs_dir = os.path.join(etc_dir, dir)
        # print(abs_dir)
        date_dirs.append(abs_dir)
    return date_dirs


def get_good_dir_delete_bad(date_direcotry):
    hour_dirs = os.listdir(date_direcotry)
    list_of_good_hours = []
    for hour_dir in hour_dirs:
        dir_parts = hour_dir.split(sep="-", maxsplit=2)
        # print(dir, end=":")
        # print(dir_parts)
        if len(dir_parts) == 2:
            if int(dir_parts[1]) - int(dir_parts[0]) == 1:
                print("{} is a good hour direcotry".format(hour_dir))
                list_of_good_hours.append(hour_dir)
            else:
                abs_hour_dir = os.path.abspath(os.path.join(date_direcotry, hour_dir))
                print("Delete hour_directory : {}".format(abs_hour_dir))
                # os.remove(abs_hour_dir)
        else:
            print("Error: Incorrect folder name")
            continue
    return list_of_good_hours


def get_days_and_good_hours(date_dirs: list):
    days_and_good_hours = {}
    for date_dir in date_dirs:
        # print(date_dir)
        list_of_good_h = get_good_dir_delete_bad(date_dir)
        date_dir = os.path.basename(date_dir)
        days_and_good_hours[date_dir] = list_of_good_h
    # print(days_and_good_hours)
    return days_and_good_hours

#{'20180808': ['10-11', '8-9'], '20180809': ['10-11', '8-9'], '20180810': ['10-11', '8-9']}


def delete_incorrect_files(days_and_good_hours: dict):
    for day, hours in days_and_good_hours.items():
        for hour in hours:
            # print(hour)
            pattern_suffics_a = hour.split("-")[0]
            pattern_suffics =  "{0:02d}".format(int(pattern_suffics_a))
            # print(pattern_suffics)
            pattern = "{0}.{1}".format(day, pattern_suffics)
            print(pattern)


date_dirs1 = get_dates_dir(Base_directory)
days_and_hour = get_days_and_good_hours(date_dirs1)
delete_incorrect_files(days_and_hour)

