import hashlib
import json
import logging
import os
import requests
from requests_toolbelt.utils import dump
from connectors.core.connector import get_logger, ConnectorError

TOKEN_FILE_TPL = "/tmp/fs_session_{}.json"

logger = get_logger('Fabric Studio')
logger.setLevel(logging.DEBUG)

class FSClient:
    def __init__(self, config):
        # Fallback to environment variable or placeholder if not provided
        self.username = config.get("username")
        self.password = config.get("password")
        self.server_url = config.get("server_url").strip('/')
        if self.server_url.startswith("http://"):
            self.server_url = self.server_url.replace("http://", "https://", 1)
        elif not self.server_url.startswith("https://"):
            self.server_url = f"https://{self.server_url}"

        self.verify_ssl = config.get('verify_ssl')
        if not self.verify_ssl:
            requests.packages.urllib3.disable_warnings(
                requests.packages.urllib3.exceptions.InsecureRequestWarning
            )
        
    
        self._token_path = TOKEN_FILE_TPL.format(
            hashlib.md5(self.server_url.encode()).hexdigest()
        )

        # Initialize a session to automatically handle cookies/CSRF
        self.session = requests.Session()
        # Equivalent to the -k (insecure) flag in curl
        self.session.verify = self.verify_ssl
        self.session.hooks["response"].append(self._log_http)
        self._load_token()
        
    def _log_http(self, response, *args, **kwargs):
        """Log full HTTP request/response details when DEBUG logging is active."""
        if logger.isEnabledFor(logging.DEBUG):
            data = dump.dump_all(response)
            logger.debug(data.decode("utf-8", errors="replace"))

    def _load_token(self):
        """Restore session cookies from /tmp if a saved token exists."""
        if os.path.exists(self._token_path):
            try:
                with open(self._token_path) as f:
                    cookies = json.load(f)
                self.session.cookies.update(cookies)
            except (OSError, ValueError):
                pass

    def _save_token(self):
        """Persist current session cookies to /tmp."""
        try:
            with open(self._token_path, "w") as f:
                json.dump(dict(self.session.cookies), f)
        except OSError as e:
            logger.warning(f"Could not save session token: {e}")

    def login(self):
        """Authenticate against the API and persist the session token."""
        try:
            response = self.session.request(
                "POST",
                f"{self.server_url}/api/v1/session/open",
                json={"username": self.username, "password": self.password},
            )
            response.raise_for_status()
            self._save_token()
            return response
        except Exception as err:
            logger.error("{0}".format(str(err)))
            raise ConnectorError("{0}".format(str(err)))

    def _get_csrf_token(self):
        """Extracts the CSRF token from the session cookies."""
        return self.session.cookies.get("fortipoc-csrftoken", "")

    def request(self, method, endpoint, **kwargs):
        """
        Generic wrapper for API calls that manages headers and tokens.
        Automatically logs in if no session token is present.
        """
        if not self._get_csrf_token():
            self.login()

        url = f"{self.server_url}{endpoint}"
        
        # Set up default headers
        headers = kwargs.get("headers", {})
        headers["Referer"] = f"{self.server_url}/"
        
        # Add CSRF token if it exists in the cookie jar
        csrf_token = self._get_csrf_token()
        if csrf_token:
            headers["X-FortiPoC-CSRFToken"] = csrf_token
        
        kwargs["headers"] = headers

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except Exception as err:
            logger.error("{0}".format(str(err)))
            raise ConnectorError("{0}".format(str(err)))

def _check_health(config):
    try:
        client = FSClient(config)

    except:
        logger.exception('Error occured')
        raise ConnectorError('Error occured')


def run_api_call(config, params):
    pass

operations = {
    'power-on': run_api_call
}