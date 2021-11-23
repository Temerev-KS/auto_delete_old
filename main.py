import arrow
import os
from pathlib import Path
from datetime import datetime


FILES_PATH: Path = Path("//192.168.0.98/ftp")
CRITICAL_TIME = arrow.now().shift(days=-31)  # returns time in format 2021-10-20T16:59:27.833144+03:00
FOLDER_LIST = []


def delete_files(path, c_time):
    global FOLDER_LIST
    for item in path.glob('*'):
        # check and continue only if item is folder
        if not item.is_file():
            # get item time eg 2021-11-22T16:59:27.834147+03:00
            item_time = arrow.get(item.stat().st_mtime)
            if item_time < c_time:
                # log it
                FOLDER_LIST.append(item.resolve().__str__())
                # remove it
                os.remove(item.resolve())


def write_folder_list():
    current_time_string = datetime.now().strftime('%m-%d-%Y_%H-%M-%S')
    log_path: Path = Path(f'log/folder_list_{current_time_string}.txt')
    with open(log_path, 'w') as file:
        for i in FOLDER_LIST:
            file.write(f'{i}\n')


if __name__ == '__main__':
    delete_files(FILES_PATH, CRITICAL_TIME)
    write_folder_list()

