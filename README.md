# OCP YouTube Plugin

This plugin lets OVOS Common Play (OCP) play YouTube URLs. It extracts a
playable stream from a YouTube link, channel, or live broadcast, so OCP can
hand it to an audio or video player.

## Install

```bash
pip install ovos-ocp-youtube-plugin
```

The plugin registers itself as an OCP stream extractor through the
`opm.ocp.extractor` entry point. OCP loads it automatically once it is
installed. No extra setup is needed.

## Usage

OCP calls this plugin when it meets a URI that starts with one of these
prefixes:

- `youtube`: a YouTube video or playlist URL
- `ydl`: any URL that yt-dlp can resolve
- `youtube.channel.live`: a channel's current live stream
- `pytube`: force the pytube backend
- `invidious`: force an Invidious instance

Configure the extractor under the `OCP` section of `mycroft.conf`:

```json
{
  "OCP": {
    "youtube": {
      "youtube_backend": "youtube-dl",
      "youtube_live_backend": "redirect",
      "ydl_backend": "yt-dlp"
    }
  }
}
```

- `youtube_backend` selects the extraction method: `youtube-dl`, `pytube`,
  `invidious`, or `webview`.
- `youtube_live_backend` selects how a channel live stream resolves:
  `redirect`, `youtube-dl`, or `pytube`.
- `ydl_backend` selects the youtube-dl fork used: `youtube-dl`,
  `youtube-dlc`, `yt-dlp`, or `auto`.

## Related projects

- [OpenVoiceOS/ovos-plugin-manager](https://github.com/OpenVoiceOS/ovos-plugin-manager): loads and manages OCP stream extractor plugins.
- [OpenVoiceOS/ovos-ocp-audio-plugin](https://github.com/OpenVoiceOS/ovos-ocp-audio-plugin): a sibling OCP stream extractor plugin.
- [OpenVoiceOS/ovos-media](https://github.com/OpenVoiceOS/ovos-media): the media service that plays streams resolved by OCP extractors.

## License

Apache-2.0
