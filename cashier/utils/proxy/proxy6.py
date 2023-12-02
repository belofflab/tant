import requests

class Proxy6(object):
    def __init__(self, api_key: str) -> None:
        self.apI_url = f"https://proxy6.net/api/{api_key}"
        self.session = requests.Session()

    def _send_request(
        self,
        method: str,
        url: str,
        headers: dict = {},
        params: dict = {},
        json: dict = {},
    ) -> requests.Response:
        return self.session.request(
            method=method,
            url=self.apI_url + url,
            headers=headers,
            params=params,
            json=json,
        )

    def getproxy(self, state: str = "all"):
        return self._send_request(
            "GET",
            "/getproxy",
            params={
                "state": state,
            },
        )
    
if __name__ == "__main__":
    proxy6 = Proxy6()
    print(proxy6.getproxy().json())
