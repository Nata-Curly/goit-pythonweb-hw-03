import logging
from http.server import HTTPServer
from handlers.html_handler import HttpHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app.log",
    filemode="a",
)


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ("", 3000)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting server on port 3000")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        logging.info("Stopping server")


if __name__ == "__main__":
    run()
