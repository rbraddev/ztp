from fbtftp.base_handler import BaseHandler
from fbtftp.base_server import BaseServer

from session_handler import handle_request, handle_session


class RequestHandler(BaseHandler):
    def __init__(self, server_addr, peer, path, options, root, stats_callback):
        self._root = root
        super().__init__(server_addr, peer, path, options, stats_callback)

    def get_response_data(self):
        request = handle_request(self._root, self._path, self._peer)
        if request is None:
            raise FileNotFoundError(f"File not found: {self._root}/{self._path}")

        return request


class TFTPServer(BaseServer):
    def __init__(
        self,
        address,
        port,
        retries,
        timeout,
        root,
        handler_stats_callback,
        server_stats_callback=None,
    ):
        self._root = root
        self._handler_stats_callback = handler_stats_callback
        super().__init__(address, port, retries, timeout, server_stats_callback)

    def get_handler(self, server_addr, peer, path, options):
        return RequestHandler(server_addr, peer, path, options, self._root, self._handler_stats_callback)


def main():
    server = TFTPServer(
        address="0.0.0.0",
        port=69,
        retries=5,
        timeout=5,
        root="../tftproot",
        handler_stats_callback=handle_session,
    )
    try:
        server.run()
    except KeyboardInterrupt:
        server.close()


if __name__ == "__main__":
    main()
