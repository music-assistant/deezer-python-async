from __future__ import annotations

import pytest

import deezer

pytestmark = pytest.mark.vcr


class TestPodcast:
    async def test_get_episodes(self, client):
        podcast = await client.get_podcast(699612)

        episodes = await podcast.get_episodes()
        assert isinstance(episodes, deezer.PaginatedList)
        episode = episodes[0]
        assert isinstance(episode, deezer.Episode)
        assert episode.title == "Episode 9: Follow the money"
        assert len(episodes) == 12
