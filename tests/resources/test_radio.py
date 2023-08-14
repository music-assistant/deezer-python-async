from __future__ import annotations

import pytest

import deezer

pytestmark = pytest.mark.vcr


class TestRadio:
    @pytest.fixture
    async def radio(self, client):
        return await client.get_radio(23261)

    def test_attributes(self, radio):
        assert hasattr(radio, "title")
        assert isinstance(radio, deezer.Radio)
        assert repr(radio) == "<Radio: Telegraph Classical>"

    async def test_get_tracks(self, radio):
        tracks = await radio.get_tracks()
        assert isinstance(tracks, list)
        assert len(tracks) == 25
        track = tracks[0]
        assert isinstance(track, deezer.Track)
        assert (
            repr(track)
            == '<Track: Mozart: Piano Concerto No. 9 in E-Flat Major, K. 271 "Jeunehomme": I. Allegro>'
        )
