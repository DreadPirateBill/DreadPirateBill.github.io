# Site content review — October 2026

**Status: APPLIED 2026-10-01**, with one amendment: intro detection now runs on every source type (SMB, NFS and the media servers, on a local link), so §2.4's scoping was dropped and the copy says "from a share or a media server". Written 2026-10-01 against Sprocket `master` (343 commits past `release`).
Layout, colours and artwork stay exactly as they are. Everything below is copy, ordering within existing sections, and
which screenshot goes in which existing slot.

Sources checked: `CLAUDE.md`, `docs/media-server-sources.md`, `docs/media-server-transcoding-and-remote.md`,
`docs/mpv-engine-facts.md`, `docs/mpv-hdr-player-plan.md`, `docs/options-reorganization.md`, `docs/infuse-comparison.md`,
`Source/Enums/SupportedFileTypes.swift`, `Source/Services/MediaServers/*`, `Source/Services/Network/SetupForm*`,
`Source/Services/Mpv/*`, `Source/Services/SubtitleSidecars.swift`, and the English strings in `Localizable.xcstrings`.

---

## 1. What changed in the app, and whether it matters to the pitch

| Change | Verified state | Marketing weight |
|---|---|---|
| Plex, Jellyfin, Emby as sources (`MediaServerProvider`) | Landed 2026-09-27. Jellyfin and Plex verified on hardware. Emby built against its API, playback not exercised. | **Headline.** Changes the whole "companion" story and removes the biggest objection (your library must be Kodi-shaped on disk). |
| Sign in with a code + QR on tvOS (Plex PIN link, Jellyfin Quick Connect) | Hardware-verified 2026-09-21. Emby has no code flow; it uses the hosted form below. | **Strong.** Concrete, demoable, solves a pain every Apple TV user recognises. |
| Setup from your phone (TV serves the Add/Edit form over the LAN, QR to open it, fields encrypted in-page) | Built 2026-09-22, offered on every Add and Edit form on tvOS. Doc notes "NOT yet tried with a phone" as of that date. | **Strong,** same reason. Applies to SMB and NFS too, not only servers. Confirm it has since been tried on a phone before we publish the claim. |
| MPV as a second video engine with HDR output on Apple TV, libplacebo picture pipeline | Phases 0–4 hardware-verified. HDR is On/Off, shown only for HDR sources. Tuning: upscaling, debanding, tone mapping, interpolation, frame-rate matching. | **Strong.** HDR was the one hole against Infuse. |
| Direct play by default, server transcode only when the original cannot succeed (hardware, bandwidth, remote), with a visible reason | Jellyfin and Plex transcode decisions run live. Runtime step-down verified on Apple TV HD. | **Important for honesty.** The "no transcoding" section cannot stay as written. |
| Per-file picture overrides, slimmed Picture page, Advanced Options column | Landed 2026-09-30 | Supports the engine story; one bullet. |
| External subtitle sidecars (SRT, ASS, SSA, VTT) found beside the video, auto-enabled | Landed 2026-09-16 | One chip in Formats. |
| ISO removed from the video list | Landed | Remove the ISO chip. |
| HTML viewer removed on tvOS | Landed 2026-09-27 | No site impact (we never listed HTML). |
| Options reorganised into tabs; "Beta Features" gone, MPV first-class | Landed 2026-09-30 | No site impact. |
| Sort direction, Director in context menu | Landed | No site impact. |
| Remote Plex servers listed from plex.tv, relay badge, locality-based transcode | Built; plex.tv resources listing has "only met a fixture". | **Do not claim yet.** See §5. |
| Intro detection | Now on every provider (SMB, NFS, media servers) on a local link; a remote server is skipped. | Copy says "from a share or a media server". |
| Platforms and floors | Still Apple TV (tvOS 18.6) and iPad (iPadOS 17.6). The `1,2` device family in the project is on test targets only. | Unchanged. |

---

## 2. Section-by-section recommendations

Section names are the ids in `templates/pages/index.html`. Strings are keys in `i18n/en.json`.

### 2.1 Hero

**Keep** "Your media. Your way." It is stronger now, not weaker: the app genuinely plays from more places.

**Change the lede.** Current: "…straight from the shares on your home network. No server to install. No account to
create. Nothing leaves your house."

Two of those four claims are now wrong for a server user. They *have* a server, and Plex sign-in goes through plex.tv.
Proposed:

> Sprocket Player plays the movies, shows, photos and documents you already own, from your Plex, Jellyfin or Emby
> server or straight from the shares on your home network. No subscription. No cloud library. Your media stays yours.

"No subscription" is a true, pointed contrast with Infuse Pro. "No cloud library" is the honest version of "nothing
leaves your house" (nothing of yours is uploaded or scraped to a third party; the only outbound traffic is a sign-in
handshake you initiate and crash reporting you can switch off).

**Hero screenshot slot (`hero-library.png`).** Unchanged brief, but with servers in the picture the easiest route to a
poster-rich library is now a Jellyfin or Plex library view. That also side-steps the Kodi-NFO prep work.

### 2.2 Formats (`#formats`)

Mostly stands. Specific edits:

- Lede currently says "built on the VLC engine". Change to "built on the VLC and MPV engines" or "ships two engines".
- Video card: drop the **ISO** chip (removed from `SupportedFileTypes.video`). Add a short line: "External subtitles
  found automatically", with chips **SRT ASS SSA VTT**.
- Sources caption: "Sources: SMB and NFS network shares, Plex, Jellyfin and Emby servers, plus the on-device Photos
  library. Shares and servers are discovered automatically." (Bonjour is no longer the whole story; servers are found
  by a port probe.)

### 2.3 Companion section (`#companion`) — the biggest rewrite

Current framing is "we read the same folders those servers use", with Plex and Jellyfin cards that are honestly a
little thin ("Point at the library share and go"). That framing was a workaround for not having server support. Now
the section should say what it does.

**Eyebrow:** "Your library, wherever it lives"
**Title:** "Plays nicely with **Plex, Jellyfin and Emby.**" (Kodi moves to a bullet; it is a sidecar format on disk,
not a server you connect to. `docs/media-server-sources.md` §2: "Kodi is not offered — it serves nothing".)

**Lede, proposed:**

> Already running a media server? Sign in and your libraries, posters, episode titles and summaries are there,
> served by the catalogue you already built. Prefer plain file shares? Sprocket reads Kodi-style metadata and artwork
> straight from the folder, so a Radarr, Sonarr or tinyMediaManager library looks right without a server at all.

**Bullets, proposed order:**

1. Plex, Jellyfin and Emby libraries appear as sources, with the server's own artwork and metadata.
2. SMB and NFS shares work with no server: Kodi-style NFO files and artwork are read in place.
3. Direct play by default. The server only converts when the original truly can't play, and tells you why.
4. Watched state and resume points live on your device. Hide what you've seen with one toggle.
5. Optional Collections group a franchise into one folder. (Shares only today; servers bypass the grouping pipeline.
   Either phrase as "on file shares" or drop the bullet.)

**Server cards.** Keep the three-card row but change the fourth implied member: Plex, Jellyfin, Emby. Sub-lines:

- Plex: "Sign in with a code at plex.tv/link."
- Jellyfin: "Quick Connect, no password typed."
- Emby: "Set up from your phone." (Emby has no code flow, which is fine; the phone form covers it.)

If you want Kodi to remain visible as a logo, a fourth card "Kodi libraries: NFO files and artwork, read from the share"
is accurate. I'd keep it to three and put Kodi in bullet 2 so the row reads "servers".

**Trademark line in the footer:** add Emby.

**Screenshot slot (`library-show.png`).** Brief unchanged. A Jellyfin or Plex show page would illustrate the new
story best.

### 2.4 Intro detection (`#intro`)

Still accurate, but the first bullet ("Works on your own files, with no online database and no server plugin") now
needs a scope. Intro detection runs on SMB sources only. Proposed:

- Bullet 1: "Works on your own files on an SMB share, with no online database and no server plugin."
- Add nothing about servers. Jellyfin's Intro Skipper and Plex markers are a known future item
  (`media-server-sources.md` §3); do not pre-announce.

Everything else in the section stands.

### 2.5 Direct play section (`#direct`) — must change

Current title: "The file you have is the file you watch." Current eyebrow: "On device. No transcoding." Both are now
only true for shares, and the body argues *against* transcoding servers in a way that reads oddly next to a section
that just said we support them.

The idea is still right. Reframe it as **direct play first**:

**Eyebrow:** "Direct play first"
**Title:** "The file you have is **the file you watch.**" (keep)
**Lede, proposed:**

> Sprocket decodes on the Apple TV or iPad itself, so what you see is the original bitstream at full quality. On a
> file share that is the only way it works. On a media server it is the default, and a conversion is asked for only
> when the original genuinely can't play: a codec this device can't decode, a link too slow to carry it, or a server
> outside your network. When that happens, a short notice tells you which, and the original comes back when it can.

**Bullets, proposed:**

1. Two engines on board: VLC as the standard, MPV as the alternative with HDR output on Apple TV. Pick per app or
   per file.
2. Switch audio tracks and subtitles instantly, with no re-encode.
3. Thumbnails are generated by the device and cached, encrypted, for next time.
4. A plain share only has to serve files. A basic NAS, a PC, a Raspberry Pi all do.

**Flow diagram.** Keep the three boxes. Change the struck-through text from "transcoding server" to "cloud relay"
or simply remove the strike line, since a transcoding server is now a supported path. My preference: keep the bar
labelled "Direct play" and strike nothing. It stays visually identical minus one small line.

**Screenshot slot (`player-tracks.png`).** Brief unchanged.

### 2.6 Privacy (`#privacy`) — adjust two claims

The architecture claims still hold (no backend, no account with us, Keychain, PIN encryption, auto-disconnect). Two
sentences need care:

- Lede: "It talks to your shares and nothing else." Change to: "It talks to your shares and your own servers, and
  nothing else."
- Note under the pillars: "The only outbound connection is anonymous crash reporting" is no longer strictly true; a
  Plex code sign-in talks to plex.tv (once, to get the token), and a remote Plex server would be reached over the
  internet. Proposed: "Beyond your own shares and servers, the only connections Sprocket makes are a one-time Plex
  sign-in handshake with plex.tv when you choose it, and anonymous crash reporting you can turn off in Options."

Add one pillar-sized fact if it fits the four-up grid without a fifth card: media-server tokens are held in the
Keychain like share passwords, and the hosted phone form encrypts the fields in the page so plain Wi-Fi carries
nothing readable. Suggest folding it into the "Keychain credentials" pillar body:

> Share passwords and server tokens live in the device Keychain. Set up from your phone and the form is encrypted
> end to end, even over plain Wi-Fi.

**The privacy policy page needs a real revision**, separately from marketing. `PRIVACY.md` in the app repo is
unchanged since June and currently says the app "does not connect to any servers on the public internet other than
Sentry". That is now false for Plex sign-in. The policy should name: media-server connections the user configures,
the plex.tv PIN exchange, the token stored in the Keychain, the LAN-only setup form, and that the server's watched
state is neither read nor written. I'd treat this as a blocker for the next App Store submission rather than a
website nicety, and update both the app's `privacy.html` and `i18n/en.json` `policy.*` strings together.

### 2.7 "And the rest of the living room" (`#more`)

Six cards. Two should change:

- Replace **Localised** (least interesting of the six) with **Set up from your phone**: "Scan the QR code on your
  Apple TV and fill in the address, name and PIN on your phone's keyboard. Sign in to Plex or Jellyfin with a short
  code, never a password on the remote." This is the second-best new feature and currently has no home. Localised
  can move to the footer or the download section as a one-liner.
- Replace **Slideshows** with **Picture controls**: "Aspect, deinterlace, speed, brightness and colour, plus
  upscaling, debanding and tone mapping on the MPV engine. Adjust live while the picture plays, per file if you like."
  Slideshows can fold into the Photos card in Formats ("Slideshows with a timer" is already there).

Keep Apple TV and iPad, Wallpapers, Sort your way, Collections (with the "on file shares" scope, or leave unscoped
since it is a sidebar card).

### 2.8 Gallery and download

Gallery captions unchanged. One of the two Apple TV slots (`photos-gallery.png` or `documents-comic.png`) could
become the **code sign-in screen** (code + QR, "Waiting for approval…"). It is the most distinctive screenshot the
app can produce right now and it photographs well. If you'd rather keep photos and comics, the sign-in shot can be a
fifth gallery item; the grid is two-up and wraps.

Download section copy: "Free of servers, accounts and transcoders." Change to: "No subscription. No account with us.
Your media, on your terms." Or reuse the hero lede's last line.

### 2.9 Support page FAQ

Two answers are now wrong and one is worth adding:

- Q2 "Does Sprocket Player need Plex, Jellyfin or Kodi installed?" Answer should become: no, it isn't required; shares
  work on their own; but if you run Plex, Jellyfin or Emby you can sign in and use the server's library directly.
- Add: "How do I sign in to Plex or Jellyfin on Apple TV?" Short answer describing the code flow, that Quick Connect
  can be switched off by a Jellyfin admin (then use a password), and that Emby uses the phone form.
- Add: "Why did a video play as a converted stream?" Pointing at the three reasons and the per-source Streaming
  Quality setting (Automatic, Original Only, caps).

---

## 3. Wording to avoid

- **"Dolby Vision."** The libplacebo pipeline can reshape DV, but the mark is licensed. Say "HDR10 and HLG"
  (`mpv-engine-facts.md` §2). The app's strings contain no Dolby mention; the site should match.
- **"No transcoding"** as an absolute. Use "direct play first" / "never converts unless it has to".
- **"Nothing leaves your house"** as an absolute. Use "no cloud library" / "nothing of yours is uploaded".
- **"Universal"** or "plays everything". The Formats section lists what it plays; that is more credible.
- **Remote access / watch away from home.** Built but not verified end to end (§5). Leave it out until it is.
- **Emby parity.** Emby is "built but unexercised". Listing it is fine; a hero claim about Emby is not. Keep Emby in
  the trio but let Plex and Jellyfin carry the examples (code sign-in).

---

## 4. Screenshot list, revised

Same nine filenames. Three briefs change:

| File | New brief |
|---|---|
| `hero-library.png` | Poster-rich library. A Jellyfin or Plex movie library is the easiest way to get there. |
| `library-show.png` | A show page from a server source, or a Kodi-scraped one; either illustrates the section. |
| `sources-setup.png` | **Prefer the code sign-in screen** (code, QR, "Waiting for approval…") or the Add form with its QR and "Or scan to fill this in on your phone". Either is a stronger privacy/setup shot than the plain form. |

If a tenth image is wanted: `player-picture.png`, the Advanced Options column open beside a playing video, for the
Picture controls card.

---

## 5. Things to confirm before publishing the new copy

1. **Phone form tried on a real phone?** The doc's last note (2026-09-22) says not yet. The claim "set up from your
   phone" needs one successful run on hardware.
2. **HDR output seen on an Apple TV 4K with an HDR TV?** The plan says Phases 0–4 hardware-verified. One sentence
   from you confirming "HDR10 lit up the TV's HDR mode" is all the site needs.
3. **Emby playback.** Fine to list; just don't screenshot it until a file has played.
4. **What ships next.** `release` is 343 commits behind `master`. If the next App Store build is the one that carries
   servers, MPV and QR setup, the site should go live with the new copy at the same time, not before. Until then the
   current site describes the shipping app accurately.

---

## 6. What does not change

Layout, section order, device frames, colours, hero plate, typography, nav, language structure, the build system.
Every edit above is a string in `i18n/en.json` or a small structural change inside an existing section (one chip
removed, one chip row added, one card swapped for another of the same shape, one strike line removed from the flow
diagram). Nothing new is introduced visually.
