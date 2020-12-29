from fbtftp.base_handler import BaseHandler
from fbtftp.base_handler import ResponseData
from fbtftp.base_server import BaseServer

import os

class FileResponseData(ResponseData):
    def __init__(self, path):
        self._size = os.stat(path).st_size
        self._reader = open(path, 'rb')

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

class RequestHandler(BaseHandler):
    def __init__(self, server_addr, peer, path, options, root, stats_callback):
        self._root = root
        super().__init__(server_addr, peer, path, options, stats_callback)

    def get_response_data(self):
        # return FileResponseData(os.path.join(self._root, self._path))
        
        request = handle_request(self._root, self._path)
        if request is None:
            raise FileNotFoundError(f"File not found: {self._root}/{self._path}")

        return request


class TFTPServer(BaseServer):
    def __init__(self, address, port, retries, timeout, root,
                 handler_stats_callback, server_stats_callback=None):
        self._root = root
        self._handler_stats_callback = handler_stats_callback
        super().__init__(address, port, retries, timeout, server_stats_callback)

    def get_handler(self, server_addr, peer, path, options):
        return RequestHandler(
            server_addr, peer, path, options, self._root,
            self._handler_stats_callback
        )

def main():
    server = TFTPServer(
        address='10.0.0.1', port=6969, retries=5, timeout=5,
        root='../tftproot', 
        handler_stats_callback=handle_session
    )
    try:
        server.run()
    except KeyboardInterrupt:
        server.close()

if __name__ == '__main__':
    main()