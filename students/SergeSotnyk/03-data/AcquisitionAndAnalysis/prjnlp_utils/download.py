import os
from pathlib import Path

import requests
from tqdm.auto import tqdm


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
                    p_bar.update(wrote)

    print(f"File downloaded, length = {file_path.stat().st_size} b")
