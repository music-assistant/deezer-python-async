from __future__ import annotations

from typing import AsyncGenerator, Generic, TypeVar, overload
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
        self.__total = None
        self.__iter = iter(self)

    @overload
    async def __getitem__(self, index: int) -> ResourceType:
        ...

    @overload
    async def __getitem__(self, index: slice) -> list[ResourceType]:
        ...

    async def __getitem__(
        self,
        index: int | slice,
    ) -> ResourceType | list[ResourceType]:
        if isinstance(index, int):
            await self._fetch_to_index(index)
            return self.__elements[index]
        if index.stop is not None:
            await self._fetch_to_index(index.stop)
        else:
            while self._could_grow():
                await self._grow()
        return self.__elements[index]

    async def __aiter__(self) -> AsyncGenerator[ResourceType, None]:
        for element in self.__elements:
            yield element
        while self._could_grow():
            for result in await self._grow():
                yield result

    async def __next__(self) -> ResourceType:
        return await next(self.__iter)

    async def __len__(self) -> int:
        return await self.total

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
        self.__total = await response_payload.get("total")
        next_url = await response_payload.get("next", None)
        if next_url:
            url_bits = urlparse(next_url)
            self.__next_path = url_bits.path.lstrip("/")
            self.__next_params = parse_qs(url_bits.query)
        return response_payload["data"]

    async def _fetch_to_index(self, index: int):
        while len(self.__elements) <= index and self._could_grow():
            await self._grow()

    @property
    async def total(self) -> int:
        """The total number of items in the list, mirroring what Deezer returns."""
        if self.__total is None:
            params = self.__base_params.copy()
            params["limit"] = 1
            response_payload = await self.__client.request(
                "GET",
                self.__base_path,
                parent=self.__parent,
                paginate_list=True,
                **params,
            )
            self.__total = response_payload["total"]
        assert self.__total is not None  # nosec B101
        return self.__total
