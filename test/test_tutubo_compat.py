"""
Regression test for https://github.com/OpenVoiceOS/ovos-ocp-youtube-plugin/issues/3

tutubo>=3.0.0 (see renovate PR #23, bumping to tutubo v4) removed the
`tutubo.pytube` module entirely (it was rewritten around a new innertube-based
API). ovos_ocp_youtube_plugin imported `from tutubo.pytube import YouTube` at
*module level*, so simply having a newer tutubo installed made the whole
plugin fail to import - breaking every extractor (ydl, pytube, invidious,
live-channel), not just the pytube-specific one.

This test simulates "tutubo.pytube is unavailable" (as it is with tutubo v4)
by removing it from sys.modules, and asserts the plugin still imports.
"""
import builtins
import sys


def _reload_plugin():
    for mod in list(sys.modules):
        if mod == "ovos_ocp_youtube_plugin" or mod.startswith("ovos_ocp_youtube_plugin."):
            del sys.modules[mod]
    import ovos_ocp_youtube_plugin
    return ovos_ocp_youtube_plugin


def _block_tutubo_pytube(monkeypatch):
    """simulate tutubo>=3 where the `tutubo.pytube` submodule no longer
    exists, WITHOUT breaking tutubo's own (unrelated) internal imports."""
    real_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "tutubo.pytube" and (fromlist is None or "YouTube" in (fromlist or ())):
            raise ModuleNotFoundError("No module named 'tutubo.pytube'")
        return real_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)


def test_import_survives_missing_tutubo_pytube(monkeypatch):
    _block_tutubo_pytube(monkeypatch)
    mod = _reload_plugin()
    assert mod.OCPYoutubeExtractor is not None


def test_ydl_extractor_still_usable_without_pytube(monkeypatch):
    # the default (ydl) backend must not depend on tutubo.pytube being importable
    _block_tutubo_pytube(monkeypatch)
    mod = _reload_plugin()
    ex = mod.OCPYoutubeExtractor()
    assert ex.ydl is not None
