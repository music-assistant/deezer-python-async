from __future__ import annotations

from typing import Generator, Generic, TypeVar
from urllib.parse import parse_qs, urlparse

import deezer

ResourceType = TypeVar("ResourceType")
REPR_OUTPUT_SIZE = 5


class PaginatedList(Generic[ResourceType]):
    """Abstract paginated response from the API and make them more Pythonic."""

    # Lifted and adapted from PyGithub:
    # https://github.com/PyGithub/PyGithub/blob/master/github/PaginatedList.py

    def __init__(
        self,
        client: deezer.Client,
        base_path: str,
        parent: deezer.Resource | None = None,
        **params,
    ):
        self.__elements: list[ResourceType] = []
        self.__client = client
        self.__base_path = base_path
        self.__base_params = params
        self.__next_path: str | None = base_path
        self.__next_params = params
        self.__parent = parent
        self.__iter = iter(self)
        self._fetched = False
        self.total = False

    def __iter__(self) -> Generator[ResourceType, None, None]:
        yield from self.__elements

    def __next__(self) -> ResourceType:
        return next(self.__iter)

    def __len__(self) -> int:
        return self.total

    def _could_grow(self) -> bool:
        return self.__next_path is not None

    async def _grow(self) -> list[ResourceType]:
        new_elements = await self._fetch_next_page()
        self.__elements.extend(new_elements)
        return new_elements

    async def _fetch_next_page(self) -> list[ResourceType]:
        assert self.__next_path is not None  # nosec B101
        response_payload = await self.__client.request(
            "GET",
            self.__next_path,
            parent=self.__parent,
            paginate_list=True,
            **self.__next_params,
        )
        self.__next_path = None
        self.total = response_payload.get("total")
        next_url = response_payload.get("next", None)
        if next_url:
            url_bits = urlparse(next_url)
            self.__next_path = url_bits.path.lstrip("/")
            self.__next_params = parse_qs(url_bits.query)
        return response_payload["data"]

    async def _fetch_to_index(self, index: int):
        while len(self.__elements) <= index and self._could_grow():
            await self._grow()

    async def fetch(self) -> PaginatedList:
        """Function to fetch the thing"""
        if self.total is None:
            params = self.__base_params.copy()
            params["limit"] = 1
            response_payload = await self.__client.request(
                "GET",
                self.__base_path,
                parent=self.__parent,
                paginate_list=True,
                **params,
            )
            self.total = response_payload["total"]
        while self._could_grow():
            await self._grow()
        self._fetched = True
        return self
