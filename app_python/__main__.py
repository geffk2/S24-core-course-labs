"""HTTP server that returns current MSK time."""
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from prometheus_client import Counter, generate_latest
import pytz

c = Counter("n_requests", "number of time requests processed since latest restart")


def get_time():
    """Returns current MSK time."""
    timezone = pytz.timezone("Europe/Moscow")
    return datetime.now(timezone)


class HTTPTimeHandler(BaseHTTPRequestHandler):
    """Handles GET requests."""

    def do_GET(self):  # pylint: disable=C0103
        """Returns current time in the 'Europe/Moscow'
        timezone with 'text/plain' content type."""
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        if self.path == "/metrics":
            self.wfile.write(str(generate_latest()).encode())
        else:
            c.inc()
            self.wfile.write(str(get_time()).encode())


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    """Starts HTTP server listening on all interfaces on port 8080."""
    server_address = ("", 8080)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    run(handler_class=HTTPTimeHandler)
