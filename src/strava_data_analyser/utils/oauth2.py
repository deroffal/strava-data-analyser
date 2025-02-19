import _thread
import logging
import random
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from webbrowser import open_new

import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class OAuth2:

    def __init__(self, authorize_url, token_url, client_id, client_secret, response_type='code', scope=None,
                 approval_prompt=None, grant_type=None, redirect_url=None):
        self.authorize_url = authorize_url
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.response_type = response_type
        self.scope = scope
        self.approval_prompt = approval_prompt
        self.grant_type = grant_type

        if redirect_url is None:
            self.scheme = "http"
            self.redirect_host = "localhost"
            self.redirect_port = random.randrange(10000, 65535)
        else:
            parsed = urlparse(redirect_url)
            self.scheme = parsed.scheme
            self.redirect_host = parsed.hostname
            self.redirect_port = parsed.port
        self.redirect_url = f"{self.scheme}://{self.redirect_host}:{self.redirect_port}"

    def authorize(self):
        _authorize_url = f"{self.authorize_url}?client_id={self.client_id}&response_type={self.response_type}&redirect_uri={self.redirect_url}"
        if self.approval_prompt is not None:
            _authorize_url = f"{_authorize_url}&approval_prompt={self.approval_prompt}"
        if self.scope is not None:
            _authorize_url = f"{_authorize_url}&scope={self.scope}"
        return open_new(_authorize_url)

    def token(self, code):
        _token_exchange_url = f"{self.token_url}?client_id={self.client_id}&client_secret={self.client_secret}&code={code}"

        if self.grant_type is not None:
            _token_exchange_url = f"{_token_exchange_url}&grant_type={self.grant_type}"

        response = requests.request("POST", _token_exchange_url)
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            logger.error(f"Error: {response.status_code}")
        return None

    def get_access_token(self):
        server = CallbackServer((self.redirect_host, self.redirect_port), RedirectHandler)
        logger.info("server created.")

        _thread.start_new_thread(server.serve_forever, ())
        logger.info("server started.")

        self.authorize()
        logger.info("browser opened.")

        while not server.code:
            logger.info("waiting...")
            time.sleep(1)

        logger.info("waiting done !")

        server.server_close()
        logger.info(f"code: {server.code}")
        access_token = self.token(server.code)
        logger.info(f"access token : {access_token}")
        return access_token


class RedirectHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        url = urlparse(self.path)
        query = parse_qs(url.query)
        logger.info(f"query : {query}")
        code = query.get("code")
        if code:
            self.server.code = code[0]
            self.wfile.write(b"<html><h1>OK</h1></html>")
        else:
            self.wfile.write(b"<html><h1>Error : code is missing</h1></html>")


class CallbackServer(HTTPServer):
    def __init__(self, *args, **kwargs):
        self.code = None
        super().__init__(*args, **kwargs)
