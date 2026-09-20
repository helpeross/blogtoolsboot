---
title: "Turn a Mini PC into a Low-Power Home Server: A Step-by-Step Build"
description: "Why a mini PC is the best 24/7 home server hardware in 2026, how to pick one, and a complete walkthrough: OS choice, Docker services, power draw and basic security."
date: 2026-09-18
draft: false
categories: ["Computers", "Software"]
tags: ["mini PC", "home server", "Linux", "Docker", "Proxmox", "self-hosting"]
summary: "A complete build guide: choose the right mini PC, install Ubuntu Server or Proxmox, run services in Docker, and keep power and security sane."
---

# Turn a Mini PC into a Low-Power Home Server: A Step-by-Step Build

If you want a machine that runs 24/7 — ad-blocking your whole network, hosting your photos, running a media server or a private Git server — a mini PC is usually the right box. This guide covers why, what to buy, and the exact steps to go from unboxed to serving.

## Why a mini PC and not a NAS, an old laptop, or a tower?

| Option | Power draw | Setup effort | What it's best at |
|---|---|---|---|
| **Mini PC** | 10–25 W idle | Low | The all-rounder: apps, media, VMs, Docker |
| Dedicated NAS | 10–40 W | Low | Central storage first, apps second |
| Old laptop | 5–15 W | Medium | Silent, built-in battery (UPS for free) |
| Old desktop tower | 50–150 W | Medium | Lots of CPU/GPU — but loud and power-hungry |
| Raspberry Pi 5 | 5–10 W | Medium | Tinkering and light services; weak for transcoding |

The mini PC wins because it's cheap, silent, uses little power, and runs full x86 software — which means everything runs on it without ARM compatibility games.

## What to look for when picking one

1. **CPU generation matters more than cores.** An N100 or N150 (12 W TDP) handles Docker, Jellyfin, and a few VMs fine. Go bigger only if you plan to run Windows VMs or heavy transcoding.
2. **16 GB RAM, not 8.** You'll run 10–20 containers before you know it, and RAM is the thing you can't easily upgrade later on many models.
3. **Two NICs or one — check before buying.** One NIC is fine; two gives you room for a future router/firewall project or link aggregation.
4. **Fanless or quiet fan.** For a living-room box, fan noise is the #1 regret. Many N100 boxes are passively cooled.
5. **NVMe + SATA.** One NVMe for the OS and containers, one 2.5" drive (or a DAS) for bulk storage keeps things fast *and* spacious.

## Step 1 — Install the OS (pick one)

| OS | Best for | Trade-off |
|---|---|---|
| **Ubuntu Server** | The default choice | Rolling your own setup, CLI comfort needed |
| **Proxmox VE** | Running VMs and containers | More complexity than most homes need |
| **Debian** | Minimal, rock solid | Less hand-holding than Ubuntu |
| **Windows 11** | People who fear Linux | More overhead, worse for containers |

**Our recommendation:** start with **Ubuntu Server**. Write it to a USB stick with Rufus or balenaEtcher, boot the mini PC from it, and choose "Use an entire disk" during install. Ten minutes later you have a server.

## Step 2 — First login and basics

```bash
# Update everything
sudo apt update && sudo apt upgrade -y

# Install Docker (the standard convenience script)
curl -fsSL https://get.docker.com | sudo sh

# Add your user to the docker group so you don't need sudo
sudo usermod -aG docker $USER
```

Log out and back in, and Docker is ready. Everything from here on is `docker compose`.

## Step 3 — The starter service stack

Create one folder and a `docker-compose.yml`. Here's a sensible first set — every one of these is optional, and this is exactly the kind of list you should trim to what you'll actually use:

| Service | What it does | Image |
|---|---|---|
| **AdGuard Home** | Network-wide ad & tracker blocking | `adguard/adguardhome` |
| **Jellyfin** | Media server (see our [setup guide](/posts/home-media-server-setup-guide/)) | `linuxserver/jellyfin` |
| **Uptime Kuma** | Uptime monitoring with alerts | `louislam/uptime-kuma` |
| **Vaultwarden** | Self-hosted password manager (Bitwarden-compatible) | `vaultwarden/server` |
| **Gitea** | Lightweight private Git server | `gitea/gitea` |

A working compose file looks like this (trim to what you need):

```yaml
services:
  adguard:
    image: adguard/adguardhome
    container_name: adguard
    restart: unless-stopped
    ports:
      - "53:53/tcp"
      - "53:53/udp"
      - "80:80"
    volumes:
      - ./adguard:/opt/adguardhome/work
      - ./adguard/conf:/opt/adguardhome/conf
```

Run `docker compose up -d`, then check `docker compose ps`. Each service gets a short config page — don't be tempted to enable all of them at once; add one, configure it, move on.

## Step 4 — Measure the power draw (before you buy anything else)

A cheap wall-plug power meter tells you the truth about your server. Typical numbers for an N100 mini PC:

- **Idle:** 6–10 W
- **Light load (10 containers):** 10–15 W
- **Peak (transcoding):** 20–30 W

At 10 W average, that's about **88 kWh per year** — roughly $10–15 in electricity depending on your rate. A gaming desktop running the same services would cost 5–10× that. This is the quiet superpower of the whole setup.

## Step 5 — Basic security in 15 minutes

1. **SSH keys, not passwords:** `ssh-keygen` on your laptop, `ssh-copy-id user@server-ip`, then disable password login in `/etc/ssh/sshd_config` (`PasswordAuthentication no`).
2. **Firewall on:** `sudo ufw allow OpenSSH && sudo ufw enable`. Don't open Docker ports to the internet unless you understand what you're exposing.
3. **Remote access:** install **Tailscale** on the server and your devices instead of port forwarding. Same recommendation as our [media server guide](/posts/home-media-server-setup-guide/) — private network, zero open ports.
4. **Backups:** your server will hold things you care about (photos, passwords, notes). Run the 3-2-1 strategy from our [backup guide](/posts/321-backup-strategy-guide/) before you trust it with anything irreplaceable.

## Common beginner traps

- **"More services = better."** No. Every container is a thing to update and a thing that can break. Start with 3, not 12.
- **Buying 8 GB RAM.** It runs out fast with Docker + browsers + VMs.
- **Forgetting `restart: unless-stopped`.** One reboot and half your services never come back.
- **Skipping the firewall because "it's on my home network."** Your router's guest network and IoT devices are on the same network, and they don't care about your plans.

### Hardware we'd start from

An N100-class mini PC with 16 GB RAM is the sweet spot for this exact build:

{{< amazon asin="B0XXXXXXXX" name="N100 Mini PC (16 GB RAM, 512 GB NVMe)" note="Replace with your own Amazon Associates ASIN and tag." >}}

## The bottom line

A mini PC, Ubuntu Server, Docker and three useful services give you a 10-watt home server that runs for years. The whole build is an evening of work, and the payoff — ad-free network, private media, self-hosted passwords — shows up every single day.

*Want a build plan for your exact needs? Tell us your services list on the [Contact page](/contact/) and we'll suggest hardware and setup.*
