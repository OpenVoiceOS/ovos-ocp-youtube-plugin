import sys
import unittest
from unittest.mock import MagicMock

# Mock the heavy / network deps before importing the plugin so the test is
# deterministic and never touches the network, youtube, yt-dlp or pytube.
sys.modules.setdefault("requests", MagicMock())
sys.modules.setdefault("yt_dlp", MagicMock())

_tutubo = MagicMock()
sys.modules.setdefault("tutubo", _tutubo)
sys.modules.setdefault("tutubo.models", MagicMock())
sys.modules.setdefault("tutubo.pytube", MagicMock())

from ovos_plugin_manager.templates.ocp import OCPStreamExtractor

from ovos_ocp_youtube_plugin import (
    OCPYoutubeExtractor,
    OCPYDLExtractor,
    OCPInvidiousExtractor,
    OCPPytubeExtractor,
    OCPYoutubeChannelLiveExtractor,
)


class TestOCPYoutubeExtractor(unittest.TestCase):

    def setUp(self):
        self.extractor = OCPYoutubeExtractor()

    def test_is_stream_extractor_subclass(self):
        self.assertTrue(issubclass(OCPYoutubeExtractor, OCPStreamExtractor))
        self.assertIsInstance(self.extractor, OCPStreamExtractor)
        # the sub-extractors are also OCPStreamExtractor subclasses
        for clazz in (OCPYDLExtractor, OCPInvidiousExtractor,
                      OCPPytubeExtractor, OCPYoutubeChannelLiveExtractor):
            self.assertTrue(issubclass(clazz, OCPStreamExtractor))

    def test_declares_base_methods(self):
        self.assertTrue(hasattr(OCPYoutubeExtractor, "supported_seis"))
        self.assertTrue(callable(getattr(self.extractor, "extract_stream")))
        self.assertTrue(callable(getattr(self.extractor, "validate_uri")))

    def test_supported_seis(self):
        self.assertEqual(
            OCPYoutubeExtractor.supported_seis,
            ["youtube", "ydl", "youtube.channel.live", "pytube", "invidious"],
        )

    def test_is_youtube(self):
        self.assertTrue(OCPYoutubeExtractor.is_youtube("https://youtube.com/watch?v=x"))
        self.assertTrue(OCPYoutubeExtractor.is_youtube("https://youtu.be/x"))
        self.assertFalse(OCPYoutubeExtractor.is_youtube("https://example.com/x"))
        self.assertFalse(OCPYoutubeExtractor.is_youtube(""))
        self.assertFalse(OCPYoutubeExtractor.is_youtube(None))

    def test_validate_uri(self):
        # matches via sei prefix
        self.assertTrue(self.extractor.validate_uri("youtube//abc"))
        self.assertTrue(self.extractor.validate_uri("invidious//abc"))
        # matches via is_youtube host check
        self.assertTrue(self.extractor.validate_uri("https://youtube.com/watch?v=x"))
        # unrelated uri
        self.assertFalse(self.extractor.validate_uri("bandcamp//abc"))

    def test_parse_title(self):
        title, artist = OCPYoutubeExtractor.parse_title("Artist - Song (Official Video)")
        self.assertEqual(artist, "Artist")
        self.assertEqual(title, "Song")

    def test_settings_from_ocp(self):
        ext = OCPYoutubeExtractor({"youtube": {"invidious_host": "http://h"}})
        self.assertEqual(ext.settings.get("invidious_host"), "http://h")


class TestEntryPointGroup(unittest.TestCase):

    def test_canonical_entrypoint_group(self):
        import os
        import re

        here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(here, "pyproject.toml")) as f:
            pyproject_src = f.read()
        # the canonical stream-extractor group read by ovos-plugin-manager
        self.assertIn('[project.entry-points."opm.ocp.extractor"]', pyproject_src)
        # the deprecated form must be gone
        self.assertIsNone(re.search(r'"ovos\.ocp\.extractor"', pyproject_src))


if __name__ == "__main__":
    unittest.main()
