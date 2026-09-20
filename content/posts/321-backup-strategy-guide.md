***

title: "The 3-2-1 Backup Strategy, Actually Implemented"

description: "Stop planning backups and start having them. A practical guide to building the 3-2-1 rule at home: local copy, NAS copy, off-site copy, automation and restore testing."

date: 2026-09-20

draft: false

categories: \["Storage"]

tags: \["backup", "3-2-1", "NAS", "cloud storage", "data safety", "rclone"]

summary: "What the 3-2-1 rule really means and how to implement it with free tools, cheap storage and a restore test you can actually pass."



***

# The 3-2-1 Backup Strategy, Actually Implemented

Everyone knows the rule: **3 copies of your data, on 2 different media types, with 1 copy off-site.** Almost nobody has it. This guide is the implementation — which copies, which tools, which schedules, and how to verify it all works before you need it.

## What the rule actually means



| Number            | Meaning                            | Why                                                                                                                       |
| ----------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **3** copies      | Your working copy + 2 backups      | One copy is not a backup; two means a failure plus a restore gone wrong still leaves you safe                             |
| **2** media types | e.g. external drive + NAS/cloud    | A dead laptop + a dead external drive from the same batch is rare — but a stolen bag takes out *all* local copies at once |
| **1** off-site    | Cloud, or a drive at another house | Fire, theft and flood take out every copy in your home regardless of redundancy                                           |

The off-site copy is the part most people skip, and it's the part that actually protects you.

## The three copies, concretely

### Copy 1 — Your working data (the original)

This is your computer, phone, or the drive you edit photos from. Nothing to set up — but it's *not* a backup. A backup is a separate copy you don't touch every day.

### Copy 2 — Local backup (different media)

The classic implementation is an **external drive**, because it's genuinely a different medium from your internal SSD — and it's cheap:



* **Windows:** File History (built-in) or [Veeam Agent Free](https://www.veeam.com/) for full image backups.

* **macOS:** Time Machine — plug in a drive, it just works.

* **Linux:** `rsync` or [Timeshift](https://github.com/linuxmint/timeshift) for the system, and a simple `rsync` script for data.

A full disk image (Veeam/Time Machine) is the one that saves you when a drive dies mid-project: boot the image, you're back. Don't rely on copying files only.

### Copy 3 — The off-site copy (NAS → cloud, or a drive at work)

Two good implementations, pick based on your data size:

**Option A — Cloud for the important stuff (photos, documents, passwords):**



* [Backblaze B2](https://www.backblaze.com/) or Wasabi, \~\$6/TB/month, billed by usage.

* Use [rclone](https://rclone.org/) to sync a folder nightly. Rclone is one command, free, and runs everywhere:



```
rclone sync /home/you/Photos remote:bucket/Photos --backup-dir remote:archive/Photos/\$(date +%F)
```

The `--backup-dir` line keeps old versions so an accidental delete is never instantly mirrored into the cloud.

**Option B — A second drive off-site:**

If your data is too big for cheap cloud (a 20 TB media library), keep a second external drive at a family member's house or a work drawer, and swap it monthly. It's manual, but a 20 TB cloud bill is its own disaster.

## Automation: the part that makes it survive

Backups that require remembering are backups that stop. Set schedules that run without you:



| What                       | When              | Tool                                     |
| -------------------------- | ----------------- | ---------------------------------------- |
| Phone photos               | Nightly, on Wi-Fi | Google Photos / iCloud / Synology Photos |
| Computer files             | Nightly at 2 AM   | Veeam / Time Machine / rsync             |
| NAS → cloud                | Nightly at 3 AM   | rclone cron job / Synology Hyper Backup  |
| Critical folder, real-time | On change         | Syncthing (self-hosted) or Dropbox       |

And the single most useful setting: **a failure alert.** rclone, Veeam and most NAS apps can email you when a job fails. A backup job that silently failed for three months is exactly how people lose a year of photos.

## The part nobody does: restore tests

A backup that can't be restored isn't a backup — it's hope. Test on a schedule that matters:



* **Monthly:** restore one random file or folder from the local backup and open it.

* **Quarterly:** restore a full system image to a spare machine (or at least boot it in a VM).

* **Yearly:** pull the off-site copy and confirm the cloud bucket isn't empty, encrypted with a lost key, or syncing a corrupt directory.

Rclone makes the cloud check one line:



```
rclone lsl remote:bucket | tail -5   # confirm files are really there
```

Also write down your encryption keys and rclone config location. The #1 cause of "my backups are gone" after ransomware isn't ransomware — it's a lost password or a config file that was never backed up itself.

## What it costs



| Setup                                    | One-time    | Monthly  | Restore time  |
| ---------------------------------------- | ----------- | -------- | ------------- |
| External drive + manual copy             | \~\$60–100  | —        | Minutes–hours |
| External drive + NAS + free cloud tier   | \~\$300–600 | \$0      | Minutes       |
| External drive + NAS + paid cloud (1 TB) | \~\$400–700 | \~\$6–15 | Minutes       |
| Two external drives, swapped monthly     | \~\$150–200 | —        | Hours         |

Start with the cheapest row today — an external drive and a schedule beats a perfect plan that hasn't been started. Then grow into the NAS row when you're ready; our [home NAS guide](/posts/home-nas-guide/) covers choosing one, and the [media server guide](/posts/home-media-server-setup-guide/) shows what else the box can do.

### The starting point we recommend

A 2-bay NAS for your on-site copy, plus cloud for the important folders, is the 3-2-1 sweet spot for most households:

{{< amazon asin="B0XXXXXXXX" name="2-Bay NAS (Beginner-Friendly Brand)" note="Replace with your own Amazon Associates ASIN and tag." >}}

## The bottom line

Three copies, two media types, one off-site — implemented as: external drive tonight, NAS when you're ready, cloud or a family member's drawer for the third copy, nightly automation, and a monthly restore test. A backup you've never restored is a guess. A backup you've restored once is a system you can trust.

*Not sure what needs backing up? Tell us what you store on the&#x20;*[Contact page](/contact/)*&#x20;and we'll suggest a tier that matches.*