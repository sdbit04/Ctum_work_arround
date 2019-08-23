import os
import re
import shutil
import argparse
Base_directory = r"D:\D_drive_BACKUP\MENTOR\BATELCO\CTUM_Collection_workarround\Test"


class ArrangeLogsEtc(object):

    def __init__(self, logs_etc_path):
        self.logs_etc_dir = logs_etc_path

    def get_dates_dir(self):
        abs_date_dirs = []
        for _dir in os.listdir(self.logs_etc_dir):
            abs_dir = os.path.join(self.logs_etc_dir, _dir)
            # print(abs_dir)
            abs_date_dirs.append(abs_dir)
        return abs_date_dirs

    @staticmethod
    def get_good_dir_delete_bad(abs_date_direcotry):
        """This will return list of good hours-directory for each date
        Here good hours-directory means, directory for only one hour of duration.
        """
        hour_dirs = os.listdir(abs_date_direcotry)
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
                    abs_hour_dir = os.path.abspath(os.path.join(abs_date_direcotry, hour_dir))
                    print("Delete hour_directory : {}".format(abs_hour_dir))
                    try:
                        # os.remove(os.path.abspath(abs_hour_dir))
                        shutil.rmtree(os.path.abspath(abs_hour_dir))
                    except PermissionError:
                        print("Unable to delete the directory {}".format(os.path.abspath(abs_hour_dir)))
                        continue
            else:
                print("Error: Incorrect folder name")
                continue
        return list_of_good_hours

    def get_days_and_good_hours(self, abs_date_dirs: list):
        """This will return a dict key=date, value=[list of good hour-directories]
        """
        days_and_good_hours = {}
        for date_dir in abs_date_dirs:
            # print(date_dir)
            list_of_good_hours = ArrangeLogsEtc.get_good_dir_delete_bad(date_dir)
            date_dir = os.path.basename(date_dir)
            days_and_good_hours[date_dir] = list_of_good_hours
        # print(days_and_good_hours)
        return days_and_good_hours

    #{'20180808': ['10-11', '8-9'], '20180809': ['10-11', '8-9'], '20180810': ['10-11', '8-9']}

    def delete_incorrect_files(self, days_and_good_hours: dict):
        for day, good_hours in days_and_good_hours.items():
            base_date_dir = os.path.join(self.logs_etc_dir, day)
            print(base_date_dir)
            for hour in good_hours:
                search_directory = os.path.join(base_date_dir, hour)
                print(search_directory)
                # print(hour)
                pattern_suffics = "{0:02d}".format(int(hour.split("-")[0]))
                # print(pattern_suffics)
                pattern = "{0}.{1}".format(day, pattern_suffics)
                print("Search pattern is {}".format(pattern))
                for file in os.listdir(search_directory):
                    file_name = str(file)
                    print(file_name, end=":")
                    if re.search(pattern, file_name):
                        print("Good File")
                    else:
                        print("Bad file ")
                        try:
                            os.remove(os.path.join(search_directory, file))
                        except:
                            print("Unable to delete {}".format(os.path.join(search_directory, file)))
                            continue


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("logs_etc_directory")
    args = parser.parse_args()
    print(args.logs_etc_directory)
    A = ArrangeLogsEtc(args.logs_etc_directory)
    # A = ArrangeLogsEtc(Base_directory)
    date_dirs1 = A.get_dates_dir()
    days_and_hour = A.get_days_and_good_hours(date_dirs1)
    A.delete_incorrect_files(days_and_hour)

