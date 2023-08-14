from __future__ import annotations

import pytest

import deezer
from deezer.exceptions import DeezerErrorResponse, DeezerUnknownResource

pytestmark = pytest.mark.vcr


class TestClient:
    # async def test_access_token_set(self, client, mocker):
    #     """Test that access token is set when making the request."""
    #     session_get = mocker.patch.object(aiohttp.ClientSession, "request")
    #     client.access_token = "token"
    #     assert client.access_token, "token"
    #     await client.request("GET", "user/me")
    #     session_get.assert_called_with(
    #         "GET",
    #         "https://api.deezer.com/user/me",
    #         params={"access_token": "token"},
    #     ) TODO  TypeError: object MagicMock can't be used in 'await' expression

    # async def test_request_404(self, client):
    #     with pytest.raises(DeezerErrorResponse):
    #         await client.request("GET", "does-not-exists") TODO
    # Im getting AttributeError: module 'aiohttp' has no attribute 'web'  ????? makes no sense

    async def test_request_unknown_resource(self, client):
        with pytest.raises(DeezerUnknownResource):
            await client.request("GET", "chart")

    async def test_get_album(self, client):
        """Test method to retrieve an album"""
        album = await client.get_album(302127)
        assert isinstance(album, deezer.Album)

    async def test_no_album_raise(self, client):
        """Test method get_album for invalid value"""
        with pytest.raises(DeezerErrorResponse):
            await client.get_album(-1)

    async def test_get_artist(self, client):
        """Test methods to get an artist"""
        artist = await client.get_artist(27)
        assert isinstance(artist, deezer.Artist)

    async def test_get_overall_chart(self, client):
        result = await client.get_chart()
        assert isinstance(result, deezer.Chart)
        assert result.id == 0

        assert isinstance(result.tracks[0], deezer.Track)
        assert isinstance(result.albums[0], deezer.Album)
        assert isinstance(result.artists[0], deezer.Artist)
        assert isinstance(result.playlists[0], deezer.Playlist)

    async def test_get_chart(self, client):
        result = await client.get_chart(106)
        assert isinstance(result, deezer.Chart)
        assert result.id == 106

        assert isinstance(result.tracks[0], deezer.Track)
        assert isinstance(result.albums[0], deezer.Album)
        assert isinstance(result.artists[0], deezer.Artist)
        assert isinstance(result.playlists[0], deezer.Playlist)

    async def test_get_overall_tracks_chart(self, client):
        result = await client.get_tracks_chart()
        assert isinstance(result, list)
        assert len(result) == 10
        assert result[0].title == "Khapta"
        assert isinstance(result[0], deezer.Track)

    async def test_get_tracks_chart(self, client):
        result = await client.get_tracks_chart(106)
        assert isinstance(result, list)
        assert len(result) == 10
        assert result[0].title == "Where Are You Now"
        assert isinstance(result[0], deezer.Track)

    async def test_get_overall_albums_chart(self, client):
        result = await client.get_albums_chart()
        assert isinstance(result, list)
        assert len(result) == 10
        assert result[0].title == "Lacrim"
        assert isinstance(result[0], deezer.Album)

    async def test_get_albums_chart(self, client):
        result = await client.get_albums_chart(106)
        assert isinstance(result, list)
        assert len(result) == 10
        assert result[0].title == "Dissidænce Episode 2"
        assert isinstance(result[0], deezer.Album)

    async def test_get_overall_artists_chart(self, client):
        result = await client.get_artists_chart()
        assert isinstance(result, list)
        assert len(result) == 10
        assert result[0].name == "Lacrim"
        assert isinstance(result[0], deezer.Artist)

    async def test_get_artists_chart(self, client):
        result = await client.get_artists_chart(106)
        assert isinstance(result, list)
        assert len(result) == 10
        assert result[0].name == "Polo & Pan"
        assert isinstance(result[0], deezer.Artist)

    async def test_get_overall_playlists_chart(self, client):
        result = await client.get_playlists_chart()
        assert isinstance(result, list)
        assert len(result) == 10
        assert result[0].title == "Les titres du moment"
        assert isinstance(result[0], deezer.Playlist)

    async def test_get_playlists_chart(self, client):
        result = await client.get_playlists_chart(106)
        assert isinstance(result, list)
        assert len(result) == 10
        assert result[0].title == "Chill tranquille"
        assert isinstance(result[0], deezer.Playlist)

    async def test_get_overall_podcasts_chart(self, client):
        result = await client.get_podcasts_chart()
        assert isinstance(result, list)
        assert len(result) == 10
        assert result[0].title == "Rob Beckett and Josh Widdicombe's Parenting Hell"
        assert isinstance(result[0], deezer.Podcast)

    async def test_get_podcasts_chart(self, client):
        result = await client.get_podcasts_chart(210)
        assert isinstance(result, list)
        assert len(result) == 10
        assert result[0].title == "Les Grosses Têtes"
        assert isinstance(result[0], deezer.Podcast)

    async def test_get_editorial(self, client):
        """Test methods to get an editorial"""
        editorial = await client.get_editorial(0)
        assert isinstance(editorial, deezer.Editorial)

    async def test_no_editorial_raise(self, client):
        """Test method get_editorial for invalid value"""
        with pytest.raises(DeezerErrorResponse):
            await client.get_editorial(-1)

    async def test_list_editorials(self, client):
        """Test methods to list editorials"""
        editorials = await client.list_editorials()
        assert isinstance(editorials, deezer.PaginatedList)
        assert isinstance(editorials[0], deezer.Editorial)
        assert len(editorials) == 22

    async def test_get_episode(self, client):
        """Test methods to get an episode"""
        episode = await client.get_episode(238455362)
        assert isinstance(episode, deezer.Episode)

    async def test_no_episode_raise(self, client):
        """Test method get_episode for invalid value"""
        with pytest.raises(DeezerErrorResponse):
            await client.get_episode(-1)

    async def test_get_genre(self, client):
        """Test methods to get a genre"""
        genre = await client.get_genre(106)
        assert isinstance(genre, deezer.Genre)

    async def test_no_genre_raise(self, client):
        """Test method get_genre for invalid value"""
        with pytest.raises(DeezerErrorResponse):
            await client.get_genre(-1)

    async def test_list_genres(self, client):
        """Test methods to list several genres"""
        genres = await client.list_genres()
        assert isinstance(genres, list)
        assert len(genres) == 23
        assert isinstance(genres[0], deezer.Genre)

    async def test_get_playlist(self, client):
        """Test methods to get a playlist"""
        playlist = await client.get_playlist(908622995)
        assert isinstance(playlist, deezer.Playlist)

    async def test_no_playlist_raise(self, client):
        """Test method get_playlist for invalid value"""
        with pytest.raises(DeezerErrorResponse):
            await client.get_playlist(-1)

    async def test_get_podcast(self, client):
        """Test methods to get a podcast"""
        podcast = await client.get_podcast(699612)
        assert isinstance(podcast, deezer.Podcast)

    async def test_no_podcast_raise(self, client):
        """Test method get_podcast for invalid value"""
        with pytest.raises(DeezerErrorResponse):
            await client.get_podcast(-1)

    async def test_get_radio(self, client):
        """Test methods to get a radio"""
        radio = await client.get_radio(23261)
        assert isinstance(radio, deezer.Radio)

    async def test_no_radio_raise(self, client):
        """Test method get_radio for invalid value"""
        with pytest.raises(DeezerErrorResponse):
            await client.get_radio(-1)

    async def test_list_radios(self, client):
        """Test methods to list radios"""
        radios = await client.list_radios()
        assert isinstance(radios, list)
        assert len(radios) == 115
        assert isinstance(radios[0], deezer.Radio)

    async def test_get_radios_top(self, client):
        radios = await client.get_radios_top()
        assert isinstance(radios, deezer.PaginatedList)
        assert isinstance(radios[0], deezer.Radio)
        assert len(radios) == 20

    async def test_get_track(self, client):
        """Test methods to get a track"""
        track = await client.get_track(3135556)
        assert isinstance(track, deezer.Track)

    async def test_no_track_raise(self, client):
        """Test method get_track for invalid value"""
        with pytest.raises(DeezerErrorResponse):
            await client.get_track(-1)

    async def test_get_user(self, client):
        """Test methods to get a user"""
        user = await client.get_user(359622)
        assert isinstance(user, deezer.User)

    async def test_get_current_user(self, client_token):
        """Test methods to get the current user"""
        user = await client_token.get_user()
        assert isinstance(user, deezer.User)

    async def test_no_user_raise(self, client):
        """Test method get_user for invalid value"""
        with pytest.raises(DeezerErrorResponse):
            await client.get_user(-1)

    async def test_get_user_recommended_tracks(self, client_token):
        tracks = await client_token.get_user_recommended_tracks()
        assert isinstance(tracks, deezer.PaginatedList)
        track = tracks[0]
        assert isinstance(track, deezer.Track)

    async def test_get_user_recommended_albums(self, client_token):
        albums = await client_token.get_user_recommended_albums()
        assert isinstance(albums, deezer.PaginatedList)
        album = albums[0]
        assert isinstance(album, deezer.Album)

    async def test_get_user_recommended_artists(self, client_token):
        artists = await client_token.get_user_recommended_artists()
        assert isinstance(artists, deezer.PaginatedList)
        artist = artists[0]
        assert isinstance(artist, deezer.Artist)

    async def test_get_user_recommended_playlists(self, client_token):
        playlists = await client_token.get_user_recommended_playlists()
        assert isinstance(playlists, deezer.PaginatedList)
        playlist = playlists[0]
        assert isinstance(playlist, deezer.Playlist)

    # async def test_get_user_flow(self, client_token):
    #     flow = await client_token.get_user_flow()
    #     assert isinstance(flow, deezer.PaginatedList)
    #     track = flow[0]
    #     assert isinstance(track, deezer.Track) TODO
    # UnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte

    @pytest.mark.parametrize(
        "args",
        [
            (),
            (359622,),
        ],
    )
    async def test_get_user_albums(self, client_token, args):
        user_albums = await client_token.get_user_albums(*args)
        assert isinstance(user_albums, deezer.PaginatedList)
        assert all(isinstance(a, deezer.Album) for a in user_albums)
        assert len(user_albums) == 2
        assert user_albums[0].title == "OK Cowboy"
        assert user_albums[1].title == "Tank (Remastered)"

    async def test_add_user_album(self, client_token):
        result = await client_token.add_user_album(302127)
        assert result is True

    async def test_remove_user_album(self, client_token):
        result = await client_token.remove_user_album(302127)
        assert result is True

    @pytest.mark.parametrize(
        "args",
        [
            (),
            (359622,),
        ],
    )
    async def test_get_user_artists(self, client_token, args):
        user_artists = await client_token.get_user_artists(*args)
        assert isinstance(user_artists, deezer.PaginatedList)
        assert all(isinstance(a, deezer.Artist) for a in user_artists)
        assert len(user_artists) == 4
        assert [a.name for a in user_artists] == [
            "Wax Tailor",
            "Vitalic",
            "Morcheeba",
            "Tribute Stars",
        ]

    async def test_add_user_artist(self, client_token):
        result = await client_token.add_user_artist(243)
        assert result is True

    async def test_remove_user_artist(self, client_token):
        result = await client_token.remove_user_artist(243)
        assert result is True

    @pytest.mark.parametrize(
        "args",
        [
            (),
            (359622,),
        ],
    )
    async def test_get_user_followers(self, client_token, args):
        user_followers = await client_token.get_user_followers(*args)
        assert isinstance(user_followers, deezer.PaginatedList)
        assert all(isinstance(a, deezer.User) for a in user_followers)
        assert len(user_followers) == 2
        assert [u.name for u in user_followers] == [
            "John Doe",
            "Jane Doe",
        ]

    @pytest.mark.parametrize(
        "args",
        [
            (),
            (359622,),
        ],
    )
    async def test_get_user_followings(self, client_token, args):
        user_followings = await client_token.get_user_followings(*args)
        assert isinstance(user_followings, deezer.PaginatedList)
        assert all(isinstance(a, deezer.User) for a in user_followings)
        assert len(user_followings) == 2
        assert [u.name for u in user_followings] == [
            "John Doe",
            "Jane Doe",
        ]

    async def test_add_user_following(self, client_token):
        result = await client_token.add_user_following(2640689)
        assert result is True

    async def test_remove_user_following(self, client_token):
        result = await client_token.remove_user_following(2640689)
        assert result is True

    async def test_get_user_history(self, client_token):
        user_history = await client_token.get_user_history()
        assert isinstance(user_history, deezer.PaginatedList)
        assert all(isinstance(t, deezer.Track) for t in user_history)
        assert len(user_history) == 3
        assert [t.title for t in user_history] == [
            "Loverini",
            "Superchérie",
            "Run Away",
        ]

    @pytest.mark.parametrize(
        "args",
        [
            (),
            (359622,),
        ],
    )
    async def test_get_user_tracks(self, client_token, args):
        user_tracks = await client_token.get_user_tracks(*args)
        assert isinstance(user_tracks, deezer.PaginatedList)
        assert all(isinstance(a, deezer.Track) for a in user_tracks)
        assert len(user_tracks) == 3
        assert [t.title for t in user_tracks] == [
            "Flyover",
            "Poney Pt. I",
            "Young Blood",
        ]

    async def test_add_user_track(self, client_token):
        result = await client_token.add_user_track(1374789602)
        assert result is True

    async def test_remove_user_track(self, client_token):
        result = await client_token.remove_user_track(1374789602)
        assert result is True

    async def test_add_user_playlist(self, client_token):
        result = await client_token.add_user_playlist(8749345882)
        assert result is True

    async def test_remove_user_playlist(self, client_token):
        result = await client_token.remove_user_playlist(8749345882)
        assert result is True

    async def test_create_playlist(self, client_token):
        result = await client_token.create_playlist("CoolPlaylist")
        print(result)
        assert result == 11336219744

    async def test_delete_playlist(self, client_token):
        result = await client_token.delete_playlist(11336219744)
        assert result is True

    async def test_search_simple(self, client):
        """Test search method"""
        result = await client.search("Soliloquy")
        assert isinstance(result, deezer.PaginatedList)
        first = result[0]
        assert isinstance(first, deezer.Track)
        assert first.title == "Soliloquy (Wouldn't Feel Alone)"
        assert len(result) == 307

    async def test_search_strict(self, client):
        result = await client.search("Soliloquy", strict=True)
        assert isinstance(result, deezer.PaginatedList)
        first = result[0]
        assert isinstance(first, deezer.Track)
        assert first.title == "Soliloquy (Wouldn't Feel Alone)"
        assert len(result) == 307

    @pytest.mark.parametrize(
        "ordering",
        [
            "RANKING",
            "TRACK_ASC",
            "TRACK_DESC",
            "ARTIST_ASC",
            "ARTIST_DESC",
            "ALBUM_ASC",
            "ALBUM_DESC",
            "RATING_ASC",
            "RATING_DESC",
            "DURATION_ASC",
            "DURATION_DESC",
        ],
    )
    async def test_search_results_ordering(self, client, ordering):
        result = await client.search("Soliloquy", ordering=ordering)
        assert isinstance(result, deezer.PaginatedList)
        first = result[0]
        assert isinstance(first, deezer.Track)
        assert first.title == "Soliloquy (Wouldn't Feel Alone)"
        assert len(result) == 307

    async def test_search_advanced_simple(self, client):
        """Test advanced search with one term"""
        result = await client.search(artist="Lou Doillon")
        assert isinstance(result, deezer.PaginatedList)
        assert result[0].title == "Left Behind"
        assert len(result) == 114

    async def test_search_advanced_multiple(self, client):
        """Test advanced search with two term"""
        result = await client.search(artist="Lou Doillon", album="Lay Low")
        assert isinstance(result, deezer.PaginatedList)
        assert result[0].title == "Where To Start"
        assert len(result) == 22

    async def test_search_albums(self, client):
        """Test search for albums"""
        result = await client.search_albums("Daft Punk")
        assert isinstance(result, deezer.PaginatedList)
        first = result[0]
        assert isinstance(first, deezer.Album)
        assert first.title == "Discovery"
        assert len(result) == 294

    async def test_search_artists(self, client):
        """Test search for artists"""
        result = await client.search_artists("Daft Punk")
        assert isinstance(result, deezer.PaginatedList)
        first = result[0]
        assert isinstance(first, deezer.Artist)
        assert first.name == "Daft Punk"
        assert len(result) == 5

    async def test_search_playlists(self, client):
        """Test search for playlists"""
        result = await client.search_playlists("Daft Punk")
        assert isinstance(result, deezer.PaginatedList)
        first = result[0]
        assert isinstance(first, deezer.Playlist)
        assert first.title == "100% Daft Punk"

    # @pytest.mark.parametrize(
    #     ("header_value", "expected_name"),
    #     [
    #         ("fr", "Chanson fran\u00e7aise"),
    #         ("ja", "\u30d5\u30ec\u30f3\u30c1\u30fb\u30b7\u30e3\u30f3\u30bd\u30f3"),
    #     ],
    #     ids=["fr", "ja"],
    # )
    # async def test_with_language_header(self, header_value, expected_name):
    #     """Get localised content with Accept-Language header."""
    #     client_fr = deezer.Client(headers={"Accept-Language": header_value})
    #     genre = await client_fr.get_genre(52)
    #     assert isinstance(genre, deezer.Genre)
    #     assert genre.name == expected_name TODO

    @pytest.mark.parametrize(
        ("json", "expected_type"),
        [
            ({"name": "Unknown", "type": "unknown-type"}, deezer.Resource),
            ({"title": "Album", "type": "album"}, deezer.Album),
            ({"name": "Artist", "type": "artist"}, deezer.Artist),
            ({"name": "Editorial", "type": "editorial"}, deezer.Editorial),
            ({"title": "Episode", "type": "episode"}, deezer.Episode),
            ({"name": "Genre", "type": "genre"}, deezer.Genre),
            ({"title": "Playlist", "type": "playlist"}, deezer.Playlist),
            ({"title": "Podcast", "type": "podcast"}, deezer.Podcast),
            ({"title": "Radio", "type": "radio"}, deezer.Radio),
            ({"title": "Track", "type": "track"}, deezer.Track),
            ({"name": "User", "type": "user"}, deezer.User),
        ],
        ids=[
            "unknown",
            "album",
            "artist",
            # chart not tested here as isn't returned with "type":"chart"
            "editorial",
            "episode",
            "genre",
            "playlist",
            "podcast",
            "radio",
            "track",
            "user",
        ],
    )
    def test_process_json_types(self, client, json, expected_type):
        result = client._process_json(json)
        assert type(result) is expected_type
