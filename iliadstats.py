import requests
import logging
import json
import time  # Import time for refresh functionality
from lxml import html  # Import lxml for XPath support

# Configure logging
logger = logging.getLogger(__name__)

LOGIN_URL='https://www.iliad.it/account/'
DASHBOARD_URL='https://www.iliad.it/account/'

USED_TRAFFIC_XPATH= "//*[@id=\"container\"]/div/div/div[2]/div[2]/div/div/div[1]/div[3]/div[2]/div[1]/div/div[1]/span[1]/text()"
TRAFFIC_ENDOWMENT_XPATH = "//div[contains(@class, 'conso__text')]/text()[contains(., '/') and (contains(., 'GB') or contains(., 'MB'))]"
RENEWAL_DATE_XPATH = RENEWAL = "//*[@id=\"container\"]/div/div/div[2]/div[2]/div/div/div[1]/div[2]/span/text()"

class IliadStats:

    def __init__(self, secrets_file_path, refresh_interval=120):
        """
        Initialize the module.

        :param secrets_file_path: Path to the secrets file.
        :param login_url: URL for login.
        :param scrape_url: URL for scraping.
        :param refresh_interval: Time in seconds to wait before refreshing the webpage (default: 60 seconds).
        """
        # Initialize internal variables
        self.login_url = LOGIN_URL
        self.dashboard_url = DASHBOARD_URL
        self.username = ""
        self.password = ""
        self.token = ""
        self.secrets_file_path = secrets_file_path
        self.refresh_interval = refresh_interval  # New parameter
        self.dashboard_response = None  # Store the dashboard response
        self.last_fetch_time = 0  # Timestamp of the last dashboard fetch

        # Initialize session
        self.session = requests.session()

        # Load secrets and check if token exists. If not, log in to obtain a new token.
        self._load_secrets(self.secrets_file_path)
        if self.token == "":
            logger.warning("Token is empty. Logging in to obtain a new token...")
            self.login()

        logger.info("IliadStats initialized with login_url: %s, dashboard_url: %s, and refresh_interval: %d seconds",
                    self.login_url, self.dashboard_url, refresh_interval)

    def _load_secrets(self, secrets_file):
        """Load secrets from a JSON file."""
        try:
            with open(secrets_file, 'r') as file:
                secrets = json.load(file)
                self.username = secrets.get('username', '')
                self.password = secrets.get('password', '')
                self.token = secrets.get('token', '')
                logger.debug("Secrets loaded successfully from %s", secrets_file)
        except FileNotFoundError:
            logger.error("Secrets file not found: %s", secrets_file)
            raise
        except json.JSONDecodeError:
            logger.error("Failed to parse secrets file: %s", secrets_file)
            raise

    def _save_token(self):
        """Save the token to the secrets file."""
        try:
            with open(self.secrets_file_path, 'w') as file:
                secrets = {'username': self.username, 'password': self.password, 'token': self.token}
                json.dump(secrets, file)
                logger.debug("Token saved successfully to %s", 'secrets.json')
        except IOError as e:
            logger.error("Failed to save token: %s", e)
            raise
    
    def _check_authentication(self, response_text: str) -> bool:
        """Check if the authentication was successful."""
        invalid_login_element = "ID utente o password non corretto."
        invalid_token_element = "Accedi alla tua area personale iliad per gestire la tua offerta"
        if invalid_login_element in response_text:
            logger.debug("Invalid login credentials.")
            return False
        elif invalid_token_element in response_text:
            logger.debug("Invalid token.")
            return False
        else:
            return True

    def login(self):
        logger.info("Attempting to log in...")
        try:
            LOGIN_INFO = {'login-ident': self.username, 'login-pwd': self.password}
            response = self.session.post(self.login_url, data=LOGIN_INFO)
            response.raise_for_status()  # Raise an error for bad responses
        except requests.exceptions.RequestException as e:
            logger.error("Login failed: %s", e)
            raise

        # Check if the login was successful
        if not self._check_authentication(response.text):
            logger.error("Login failed: Invalid credentials or token.")
            raise Exception("Login failed: Invalid credentials or token.")
        else:
            logger.info("Login successful.")
            logger.debug("Login tokens: %s", self.session.cookies.get_dict())
            self.token = self.session.cookies.get_dict().get('ACCOUNT_SESSID', '')
            # Save the token to the secrets file
            self._save_token()
            logger.info("Token updated in secrets file.")

    def _fetch_dashboard(self):
        """Fetch the dashboard using a POST request with the token in the header."""
        logger.debug("Fetching dashboard webpage from %s using POST with token...", self.dashboard_url)
        try:
            headers = self.__get_header_info()
            response = self.session.post(self.dashboard_url, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses
            logger.debug("Webpage fetched successfully, checking for authentication...")
        except requests.exceptions.RequestException as e:
            logger.error("Failed to fetch webpage: %s", e)
            raise

        if not self._check_authentication(response.text):
            logger.warning("Authentication failed while fetching the dashboard.")
            # Attempt to log in again
            logger.warning("Re-attempting login...")
            self.login()
            # Fetch the dashboard again after re-login
            self._fetch_dashboard()
        else:
            logger.debug("Authentication successful while fetching the dashboard.")
            self.dashboard_response = response
            self.last_fetch_time = time.time()  # Save the current time as the last fetch time
            logger.debug("Dashboard fetch time updated to: %s", self.last_fetch_time)

    def __get_header_info(self) -> dict:
        """
        Returns the header for the request with the token.

        RETURN:
            The header for the request with the token.
        """
        HEADER_COOKIE = "ACCOUNT_SESSID="
        HEADER_INFO = {'cookie': ""}

        if self.token:
            HEADER_INFO['cookie'] = HEADER_COOKIE + self.token
            logger.debug("Header created with token: %s", self.token)
        else:
            logger.warning("Token is empty. Logging in to obtain a new token...")
            self.login()
            HEADER_INFO['cookie'] = HEADER_COOKIE + self.token
            logger.debug("Header created with new token: %s", self.token)
        return HEADER_INFO

    def _match_xpath(self, xpath: str) -> str:
        """
        Extract a string from the dashboard response using an XPath.

        :param xpath: The XPath to apply to the dashboard response.
        :return: The extracted string.
        """
        # Check if the response is older than the refresh interval
        current_time = time.time()
        if not self.dashboard_response or (current_time - self.last_fetch_time > self.refresh_interval):
            logger.info("Dashboard response is outdated or missing. Fetching a new one...")
            self._fetch_dashboard()

        try:
            # Parse the dashboard response content
            tree = html.fromstring(self.dashboard_response.content)
            result = tree.xpath(xpath)

            if result:
                logger.debug("XPath result: %s", result[0])
                return result[0]  # Return the first match
            else:
                logger.warning("No result found for the given XPath: %s", xpath)
                return ""
        except Exception as e:
            logger.error("Failed to extract string using XPath: %s", e)
            raise
    
    def get_traffic_consumption(self):
        """
        Get the used traffic from the dashboard using XPath.
        """
        logger.debug("Getting used traffic...")
        match = self._match_xpath(USED_TRAFFIC_XPATH).strip()
        # Last 2 characters are the unit of measure (GB or MB), we use them to convert the value
        unit = match[-2:]
        value = match[:-2].replace(",", ".")
        if unit == "GB":
            value = float(value)
        elif unit == "MB":
            value = float(value) / 1024  # Convert MB to GB
        else:
            logger.error("Unknown unit of measure: %s", unit)
            raise ValueError("Unknown unit of measure.")
        return value
    
    def get_traffic_endowment(self):
        """
        Get the traffic endowment from the dashboard using XPath.
        """
        logger.debug("Getting traffic endowment...")
        match = self._match_xpath(TRAFFIC_ENDOWMENT_XPATH).strip()
        match = match[2:]
        # Last 2 characters are the unit of measure (GB or MB), we use them to convert the value
        unit = match[-2:]
        value = match[:-2].replace(",", ".")
        if unit == "GB":
            value = float(value)
        elif unit == "MB":
            value = float(value) / 1024
        else:
            logger.error("Unknown unit of measure: %s", unit)
            raise ValueError("Unknown unit of measure.")
        return value
    
    def get_renewal_date(self):
        """
        Get the renewal date from the dashboard using XPath.
        """
        logger.debug("Getting renewal date...")
        match = self._match_xpath(RENEWAL_DATE_XPATH).strip()
        # parse the date string to a datetime object
        try:
            renewal_date = time.strptime(match, "%d/%m/%Y")
            logger.debug("Renewal date parsed successfully: %s", renewal_date)
            return renewal_date
        except ValueError as e:
            logger.error("Failed to parse renewal date: %s", e)
            raise