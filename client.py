import json
from typing import Optional

from requests import request
from requests.auth import HTTPBasicAuth


class Client:
    def __init__(
        self,
        url: str,
        client_key: str,
        client_secret: str,
        **kwargs,
    ) -> None:
        self.url = url
        self.client_key = client_key
        self.client_secret = client_secret
        self.wp_api = kwargs.get("wp_api", True)
        self.version = kwargs.get("version", "wc/v3")

    def __get_url(self, endpoint):
        url = self.url
        api = "wc-api"

        if url.endswith("/") is False:
            url = f"{url}/"

        if self.wp_api:
            api = "wp-json"

        return f"{url}/{api}/{self.version}/{endpoint}"

    def __request(
        self,
        method: str,
        endpoint: str,
        data: Optional[dict],
        params: Optional[dict] = {},
        **kwargs,
    ):
        headers = {}

        if data is not None:
            data = data
            headers["content-type"] = "application/json;charset=utf-8"

        url = self.__get_url(endpoint)

        auth = HTTPBasicAuth(self.client_key, self.client_secret)

        return request(
            method=method,
            url=url,
            auth=auth,
            params=params,
            data=data,
            headers=headers,
            **kwargs,
        )

    def get(self, endpoint, **kwargs):
        return self.__request("GET", endpoint, None, **kwargs)

    def post(self, endpoint, data, **kwargs):
        return self.__request("POST", endpoint, data, **kwargs)

    def put(self, endpoint, data, **kwargs):
        return self.__request("PUT", endpoint, data, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.__request("DELETE", endpoint, None, **kwargs)
