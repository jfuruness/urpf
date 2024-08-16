from bs4 import BeautifulSoup


class SpoofedASNCollector:

    URL = 'https://spoofer.caida.org/as_stats.php'

    def __init__(
        self,
        requests_cache_db_path: Optional[Path] = None,
    ) -> None:

        # By default keep requests cached for a single day
        if requests_cache_db_path is None:
            requests_cache_db_path = Path("/tmp/") / f"{date.today()}.db"
        self.requests_cache_db_path: Path = requests_cache_db_path
        self.session = requests_cache.CachedSession(str(self.requests_cache_db_path))

    def __del__(self):
        self.session.close()

    def run(self) -> tuple[int]:
        """Gets spoofed ASNs from CAIDA"""

        resp = self.session.get(self.URL)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all rows in the table - adjust the selector as needed
        rows = soup.select('table tr')

        # Extract AS numbers
        return tuple([int(x.find_all('td')[0].text.strip().split()[0]) for x in rows])
