from __future__ import annotations

import pytest

import deezer

pytestmark = pytest.mark.vcr


class TestArtist:
    @pytest.fixture()
    async def daft_punk(self, client):
        return await client.get_artist(27)

    async def test_attributes(self, daft_punk):
        assert hasattr(daft_punk, "name")
        assert isinstance(daft_punk, deezer.Artist)
        assert repr(daft_punk) == "<Artist: Daft Punk>"

    async def test_get_albums(self, daft_punk):
        albums = await daft_punk.get_albums()
        assert isinstance(albums, deezer.PaginatedList)
        album = albums[0]
        assert isinstance(album, deezer.Album)
        assert repr(album) == "<Album: Homework (25th Anniversary Edition)>"
        assert len(albums) == 36

    async def test_get_top(self, daft_punk):
        tracks = await daft_punk.get_top()
        assert isinstance(tracks, deezer.PaginatedList)
        track = tracks[0]
        assert isinstance(track, deezer.Track)
        assert (
            repr(track)
            == "<Track: Get Lucky (Radio Edit - feat. Pharrell Williams and Nile Rodgers)>"
        )
        assert len(tracks) == 100

    async def test_get_radio(self, daft_punk):
        tracks = await daft_punk.get_radio()
        assert isinstance(tracks, list)
        assert len(tracks) == 25
        track = tracks[0]
        assert isinstance(track, deezer.Track)
        assert repr(track) == "<Track: One More Time>"

    async def test_get_related(self, daft_punk):
        related_artists = await daft_punk.get_related()
        assert isinstance(related_artists, deezer.PaginatedList)
        related_artist = related_artists[0]
        assert isinstance(related_artist, deezer.Artist)
        assert repr(related_artist) == "<Artist: Julian Casablancas>"
        assert len(related_artists) == 20

    async def test_get_playlists(self, daft_punk):
        playlists = await daft_punk.get_playlists()
        assert isinstance(playlists, deezer.PaginatedList)
        playlist = playlists[0]
        assert isinstance(playlist, deezer.Playlist)
        assert repr(playlist) == "<Playlist: Fitness Motivation Hits 2023>"
        assert len(playlists) == 100
