import bz2
import os
from pathlib import Path
import math

import requests
from tqdm.auto import tqdm


def check_if_file_exist_make_dir(filename: str) -> (Path, bool):
    """
    Function performs the following checks:
       if file directory does not exist, directory is created.

    :param filename: name of a new file.
    :return: Path object for a new filename, boolean sign if file is already existed.
    """
    file_path = Path(filename)

    dir = str(file_path.parent.absolute())
    if not os.path.exists(dir):
        os.mkdir(dir)

    if file_path.is_file():
        return file_path, True

    return file_path, False


def unpack_bz2(a_name: str, unpacked_name: str):
    a_file_path, packed_already_existed = check_if_file_exist_make_dir(a_name)
    u_file_path, unpacked_already_existed = check_if_file_exist_make_dir(unpacked_name)
    if unpacked_already_existed:
        print(f"Unpacked file '{a_file_path.absolute()}' is already existed, unpacking was skipped.")
        return

    print(f"Start to unpack archive '{a_name}'")
    chunk_size: int = 16 * 1024
    with open(unpacked_name, 'wb') as new_file, bz2.BZ2File(a_name, 'rb') as file:
        for data in tqdm(iter(lambda: file.read(chunk_size), b'')):
            new_file.write(data)
    print(f"Archive was unpacked to file '{unpacked_name}'.")


def download_with_progress(link: str, filename: str):
    file_path = Path(filename)

    dir = str(file_path.parent.absolute())
    if not os.path.exists(dir):
        os.mkdir(dir)

    if file_path.is_file():
        print(f"File '{file_path.absolute()}' is already existed, downloading was skipped.")
        return

    with open(filename, "wb") as f:
        print("Downloading '%s'" % filename)
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:  # no content length header
            print(f"Length of the downloaded file is unknown, start downloading")
            f.write(response.content)
        else:
            wrote = 0
            total_size: int = int(total_length)
            chunk_size = 1024 * 8
            with tqdm(total=total_size, unit="B") as p_bar:
                for data in response.iter_content(chunk_size=chunk_size):
                    bl_size = f.write(data)
                    wrote += bl_size
                    p_bar.update(bl_size)

    print(f"File downloaded, length = {file_path.stat().st_size} b")
