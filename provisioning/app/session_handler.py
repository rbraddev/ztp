import os

from fbtftp.base_handler import ResponseData


class FileResponseData(ResponseData):
    def __init__(self, path):
        self._size = os.stat(path).st_size
        self._reader = open(path, "rb")

    def read(self, n):
        return self._reader.read(n)

    def size(self):
        return self._size

    def close(self):
        self._reader.close()


def handle_request(root, file):
    if file == "testfile1.txt":
        return FileResponseData(os.path.join(root, "testfile2.txt"))

    if os.path.exists(os.path.join(root, file)):
        return FileResponseData(os.path.join(root, file))

    return None


def handle_session(stats):
    if stats.packets_sent > 0:
        print(f"{stats.peer[0]} received {stats.file_path}")