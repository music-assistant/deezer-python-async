from __future__ import annotations

import pytest

import deezer

pytestmark = pytest.mark.vcr


class TestEpisode:
    async def test_get_episode(self, client):
        episode = await client.get_episode(343457312)
        assert isinstance(episode, deezer.Episode)
        assert episode.title == "Stuart Hogg and the GOAT"

    async def test_as_dict(self, client):
        """Test resource conversion to dict."""
        episode = await client.get_episode(343457312)
        episode_dict = episode.as_dict()
        assert episode_dict["id"] == 343457312
        assert episode_dict["release_date"] == "2021-11-22 23:42:00"

    async def test_access_inferable_fields(self, client):
        """Accessing a missing inferable field doesn't do any API calls."""
        track = await deezer.Track(
            client,
            json={
                "id": 3135556,
                "type": "track",
            },
        ).get()
        assert track.link == "https://www.deezer.com/track/3135556"
        assert track.share == (
            "https://www.deezer.com/track/3135556?utm_source=deezer"
            "&utm_content=track-3135556&utm_term=0_1692022470&utm_medium=web"
        )

    async def test_access_non_inferable_field(self, client):
        episode = await deezer.Episode(
            client,
            json={
                "id": 343457312,
                "type": "episode",
            },
        ).get()
        assert episode.duration == 3254

    # async def test_add_bookmark(self, client_token):
    #     episode = await client_token.get_episode(343457312)
    #     result = await episode.add_bookmark(55)
    #     assert result is True

    # async def test_remove_bookmark(self, client_token):
    #     episode = await client_token.get_episode(343457312)
    #     result = await episode.remove_bookmark()
    #     assert result is True TODO Deezer api broken...
