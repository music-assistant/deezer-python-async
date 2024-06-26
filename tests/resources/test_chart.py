from __future__ import annotations

import pytest

import deezer

pytestmark = pytest.mark.vcr


class TestChart:
    @pytest.fixture()
    async def chart(self, client):
        return await client.get_chart(0)

    async def test_get_tracks(self, chart):
        tracks = await chart.get_tracks()
        assert isinstance(tracks, deezer.PaginatedList)
        track = tracks[0]
        assert isinstance(track, deezer.Track)
        assert repr(track) == "<Track: LA FAMA>"
        assert len(tracks) == 10

    async def test_get_artists(self, chart):
        artists = await chart.get_artists()
        assert isinstance(artists, deezer.PaginatedList)
        artist = artists[0]
        assert isinstance(artist, deezer.Artist)
        assert repr(artist) == "<Artist: Jul>"
        assert len(artists) == 10

    async def test_get_albums(self, chart):
        albums = await chart.get_albums()
        assert isinstance(albums, deezer.PaginatedList)
        album = albums[0]
        assert isinstance(album, deezer.Album)
        assert repr(album) == "<Album: Multitude>"
        assert len(albums) == 10

    async def test_get_playlists(self, chart):
        playlists = await chart.get_playlists()
        assert isinstance(playlists, deezer.PaginatedList)
        playlist = playlists[0]
        assert isinstance(playlist, deezer.Playlist)
        assert repr(playlist) == "<Playlist: Les titres du moment>"
        assert len(playlists) == 10

    async def test_get_podcasts(self, chart):
        podcasts = await chart.get_podcasts()
        assert isinstance(podcasts, deezer.PaginatedList)
        podcast = podcasts[0]
        assert isinstance(podcast, deezer.Podcast)
        assert repr(podcast) == "<Podcast: Les Grosses Têtes>"
        assert len(podcasts) == 10
