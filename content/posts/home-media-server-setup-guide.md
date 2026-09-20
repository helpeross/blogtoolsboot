---
title: "How to Set Up a Home Media Server: Plex and Jellyfin Without the Pain"
description: "A step-by-step tutorial for turning a NAS (or any always-on PC) into a media server with Plex or Jellyfin — folder structure, permissions, hardware transcoding and safe remote access."
date: 2026-09-18
draft: false
categories: ["Storage", "Software"]
tags: ["media server", "Plex", "Jellyfin", "NAS", "streaming", "self-hosting"]
summary: "Everything a media server setup actually involves: choosing Plex or Jellyfin, preparing your library, fixing permissions, and enabling remote access safely."
---

# How to Set Up a Home Media Server: Plex and Jellyfin Without the Pain

A home media server is just an always-on computer that stores your movies, shows, music and photos, and streams them to every screen in the house — and outside it, if you want. This guide walks through the whole setup the way it works in practice, not the way the marketing pages make it sound.

## First: what you're actually building

| Component | What it does | Where it runs |
|---|---|---|
| **Storage** | Holds the media files | NAS, external drive, PC |
| **Media server app** | Scans the library, serves the apps | Plex or Jellyfin on the same box |
| **Clients** | Play the content | TV, phone, tablet, browser, game console |

The server app is the only new software. Everything else is probably already in your house.

## Plex vs. Jellyfin: the honest difference

| | Plex | Jellyfin |
|---|---|---|
| Price | Free tier, paid features (hardware transcoding, downloads) | Completely free, open source |
| Ease of setup | Slightly easier, polished apps | Very good, slightly more DIY |
| Account needed | Yes (Plex account for login) | No — your server, your login |
| Phone app playback | Free tier has limits | Free, unlimited |
| Who it's for | People who want it to "just work" | People who like controlling everything |

**Rule of thumb:** if you want the least friction and don't mind a free account, pick **Plex**. If you want zero accounts, zero subscriptions and full control, pick **Jellyfin**. Both handle the same libraries; switching later is possible but annoying, so decide once.

## The setup, step by step

### Step 1 — Create a clean folder structure

Media servers are dumb in one specific way: they match file names to library entries. Messy folders mean missing art, wrong titles and "unmatched" entries. Use this layout:

```
media/
├── Movies/
│   └── Interstellar (2014)/
│       └── Interstellar (2014).mkv
├── TV Shows/
│   └── The Expanse/
│       └── Season 1/
│           └── The Expanse - S01E01.mkv
├── Music/
└── Photos/
```

One movie per folder (for extras like subtitles), and shows in `Season N` subfolders. Naming matters more than any setting in the app.

### Step 2 — Install and point the server at the library

On Synology/QNAP this is a one-click package; on Debian/Ubuntu it's a few commands. Then in the web UI:

1. Add a **library** of the type you want (Movies, Shows, Music, Photos).
2. Point it at the folder you created in Step 1.
3. Set the language and let it scan. The first scan of a large library can take a while — that's normal.

### Step 3 — Fix permissions *before* you wonder why nothing plays

The #1 beginner failure: the media server runs as its own user, can't read your files, and shows empty libraries or "unavailable." On Linux:

```bash
# Give the media server user read access to the whole library
sudo chown -R plex:plex /srv/media   # or: jellyfin:jellyfin
sudo chmod -R 750 /srv/media
```

If the app runs in Docker, the volume mount itself is usually the culprit — mount the media path read-only if you want to be extra safe:

```yaml
volumes:
  - /srv/media:/media:ro
```

### Step 4 — Understand transcoding (the thing everyone over-worries about)

Transcoding converts a file into a format the client can play. It only happens when the source file and the client don't match (e.g. streaming 4K HDR to a phone).

- **Direct Play** — file plays as-is, no CPU load. This is what happens most of the time on a decent TV or app.
- **Transcoding** — CPU-heavy for 4K; hardware transcoding (GPU) makes it nearly free.

**What to do:** don't buy hardware for transcoding. Buy storage, run everything, and check your dashboard after a week. Most households transcode rarely. If you *do* transcode a lot, that's when you look at a device with Quick Sync or a newer NAS.

### Step 5 — Remote access, the safe way

The tempting approach is forwarding port 32400 (Plex) or 8096 (Jellyfin) on your router. Don't — you're exposing your whole server to the internet, and home routers get scanned constantly.

Better options, in order of preference:

1. **Tailscale** (free for personal use) — a private VPN mesh. Install it on the server and your phone/laptop; you get a stable address that works anywhere. No open ports.
2. **A reverse proxy with HTTPS** — works, but you must keep it updated and use authentication. More moving parts than most people need.

For 95% of home users, Tailscale is the answer: 10 minutes, zero open ports, and it also happens to solve remote access to everything else on your network.

## The mistakes we see most

1. **Bad naming** — spend 10 minutes on file names, save yourself hours of "unmatched" fixing.
2. **Skipping permission checks** — libraries that show up empty are almost always permissions.
3. **Transcoding panic** — most 1080p/4K playback on modern devices is direct play. Don't buy hardware to solve a problem you don't have yet.
4. **Port forwarding from day one** — use a VPN mesh instead.
5. **One copy only** — a media library is still data. If it's irreplaceable (home videos, photos), it belongs in a backup strategy, not just on the server. See our [3-2-1 backup guide](/posts/321-backup-strategy-guide/) if you haven't set one up.

### Hardware we'd start from

A 2-bay NAS is the classic media server foundation — quiet, low power, and room to grow:

{{< amazon asin="B0XXXXXXXX" name="2-Bay NAS (Beginner-Friendly Brand)" note="Replace with your own Amazon Associates ASIN and tag." >}}

## The bottom line

Set up the folder structure first, install Plex or Jellyfin, fix permissions, and access everything remotely through a private VPN. That's the whole system — most of the "media server" complexity you read about online only appears if you skip one of those four steps.

*Stuck on a specific step? Tell us where on the [Contact page](/contact/) and we'll help you work it out.*
