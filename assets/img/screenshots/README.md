# Screenshots

Drop PNG files into this folder using the exact names below. The site picks them up
automatically; until a file exists, the page shows a labelled placeholder in its slot.

Apple TV shots: capture from the tvOS simulator or a real Apple TV at 1920×1080 (3840×2160 is fine too).
iPad shots: landscape, any current iPad; the frame on the site is 4:3 so 2732×2048 / 2360×1640 all work.

| File | Where it appears | What to show |
|---|---|---|
| `hero-library.png` | Hero, top of the home page | The library browser with plenty of poster art. This is the money shot. |
| `library-show.png` | "Companion to Plex, Jellyfin and Kodi" | A TV show or season view with fanart, episode thumbnails and plot summaries. |
| `player-skip-intro.png` | "Skip the intro" | Playback mid-title-sequence with the **Skip Intro** button visible. Transport controls hidden if possible. |
| `player-tracks.png` | "No transcoding" | Full-screen video with the audio / subtitle track picker open. A multi-track MKV is ideal. |
| `sources-setup.png` | "Privacy first" | Either the Add Source form showing the PIN field, or Options → Privacy showing the disconnect settings. |
| `ipad-library.png` | Gallery | iPad, landscape, library browser with posters. |
| `ipad-photos.png` | Gallery | iPad, landscape, a photo grid or a comic / PDF open in the reader. |
| `photos-gallery.png` | Gallery | Apple TV, a photo folder or slideshow. |
| `documents-comic.png` | Gallery | Apple TV, a CBZ/CBR or PDF page open full-screen. |

Tips:
- Use content you have the rights to show publicly, or content whose artwork you're comfortable having on the site.
- Keep the same wallpaper across shots so the set feels consistent.
- PNG is preferred for UI. If a file is over ~1.5 MB, a high-quality JPEG with the same base name is fine, but then update the `src` in `index.html` to `.jpg`.
