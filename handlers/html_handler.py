import logging
import mimetypes
import pathlib
import urllib.parse
import html
from datetime import datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from handlers.data_handler import DataHandler
from handlers.template_handler import TemplateHandler

DATA_FILE = "storage/data.json"


class HttpHandler(BaseHTTPRequestHandler):
    """HTTP-обробник запитів"""

    BASE_PATH = pathlib.Path(".")
    DATA_HANDLER = DataHandler(DATA_FILE)

    def do_GET(self):
        """Обробка GET-запитів"""
        pr_url = urllib.parse.urlparse(self.path)
        path = pr_url.path

        if path == "/":
            self.send_html_file("index.html")
        elif path == "/message":
            self.send_html_file("message.html")
        elif path == "/read":
            self.send_template("read.html")
        else:
            file_path = self.BASE_PATH / path.lstrip("/")
            if file_path.exists():
                self.send_static(file_path)
            else:
                self.send_html_file("error.html", status=HTTPStatus.NOT_FOUND)

    def do_POST(self):
        """Обробка форми та збереження даних у JSON"""
        content_length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(content_length)
        data_str = urllib.parse.unquote_plus(data.decode())
        data_dict = {
            key: html.escape(value)
            for key, value in (el.split("=") for el in data_str.split("&"))
        }
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        self.DATA_HANDLER.save_data({timestamp: data_dict})
        logging.info(f"Saved message: {data_dict}")
        self.send_response(HTTPStatus.FOUND)
        self.send_header("Location", "/read")
        self.end_headers()

    def send_template(self, template_filename, status=HTTPStatus.OK):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        data = self.DATA_HANDLER.load_data()
        template = TemplateHandler(template_filename)
        rendered = template.render(data=data)
        self.wfile.write(rendered)

    def send_html_file(self, filename, status=HTTPStatus.OK):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        try:
            with open(filename, "rb") as file:
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_response(HTTPStatus.NOT_FOUND)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def send_static(self, path):
        self.send_response(HTTPStatus.OK)
        mime_type, _ = mimetypes.guess_type(str(path))
        self.send_header("Content-type", mime_type or "application/octet-stream")
        self.end_headers()
        with open(path, "rb") as file:
            self.wfile.write(file.read())
