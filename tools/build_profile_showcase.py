#!/usr/bin/env python3
"""Build a curated git-profile showcase of verified UI photos/videos across repos.

Honest audit rules:
- Only copy existing committed evidence / screenshots / release proof.
- Record exact source path, source SHA, file SHA-256, and proof class.
- Projects with no UI media are listed as NO_VISUAL_PROOF (not invented).
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPOS_ROOT = Path("/agent/repos")
OUT_ROOT = Path(__file__).resolve().parents[1] / "showcase"
MAX_BYTES = 12 * 1024 * 1024  # skip huge single files
MAX_PER_PROJECT = 10
MAX_VIDEOS = 6

# Curated picks: (repo_dirname, display_name, category, relative paths)
CURATED: dict[str, dict] = {
    "vishvakarma-os": {
        "name": "Vishvakarma.OS",
        "category": "software",
        "summary": "Browser-native architectural planning and 3D review workstation.",
        "photos": [
            "docs/release/evidence/screenshots/01-landing-hero.png",
            "docs/release/evidence/screenshots/03-editor-2d-sample.png",
            "docs/release/evidence/screenshots/04-editor-3d-premium.png",
            "docs/release/evidence/screenshots/02-auth-email-link.png",
            "docs/release/evidence/screenshots/09-pricing-tiers.png",
            "docs/release/evidence/screenshots/11-releases.png",
            "docs/release/evidence/screenshots/12-world-records.png",
            "docs/release/evidence/screenshots/13-audit.png",
        ],
        "videos": [],
    },
    "dentalstudio-os": {
        "name": "DentalStudio.OS",
        "category": "software",
        "summary": "Clinical-grade browser dental planning OS with demo corridor and evidence packs.",
        "photos": [
            "release-evidence/dentist-pilot-final-20260814/browser-proof/screenshots/landing.png",
            "release-evidence/dentist-pilot-final-20260814/browser-proof/screenshots/pricing.png",
            "docs/release/proof-pack/screenshots/cold-open-critical-routes/reports.png",
            "e2e-results/phiro-corridor/Implant-Planning.png",
            "e2e-results/phiro-corridor/Presentation-Mode.png",
            "e2e-results/phiro-corridor/Report.png",
            "e2e-results/phiro-corridor/Cases.png",
        ],
        "videos": [
            "release-evidence/dentist-pilot-final-20260814/videos/video-1-dentist-core-workflow.mp4",
            "release-evidence/dentist-pilot-final-20260814/videos/video-2-ipad-workflow.mp4",
            "release-evidence/dentist-pilot-final-20260814/videos/video-3-imaging-workflow.mp4",
            "release-evidence/dentist-pilot-final-20260814/videos/video-5-pilot-overview.mp4",
        ],
    },
    "aiprofex-os": {
        "name": "AIProfex.OS",
        "category": "software",
        "summary": "Education / operations OS with dashboard, scheduling, and admin surfaces.",
        "photos": [
            "docs/screenshots/dashboard-overview.png",
            "docs/screenshots/projects.png",
            "docs/screenshots/scheduling.png",
            "docs/screenshots/guardians.png",
            "docs/screenshots/admin-users.png",
            "docs/screenshots/settings-appearance.png",
            "evidence/auth-production-proof/01-register-page.png",
        ],
        "videos": [],
    },
    "Midnight-": {
        "name": "Midnight (Velvet Haven / Veilmorph)",
        "category": "software",
        "summary": "Phone-first creative apps: Velvet Haven couture + Veilmorph studio.",
        "photos": [
            "docs/screenshots/01-today-phone-390x844.png",
            "docs/screenshots/02-planner-fold-344x882-large.png",
            "docs/screenshots/03-veilmorph-studio-390x844.png",
            "docs/screenshots/04-velvet-couture-390x844.png",
            "apps/velvet-haven/docs/screenshots/new-ui-20261114/01-codex-hub_390x844.png",
            "apps/velvet-haven/docs/screenshots/new-ui-20261114/02-ideas-discover_390x844.png",
            "apps/velvet-haven/docs/screenshots/new-ui-20261114/03-workshop-monster_390x844.png",
            "apps/veilmorph-studio/evidence/live-release/access-desktop-1280x720.png",
        ],
        "videos": [],
    },
    "PERTHSAVER": {
        "name": "PerthSaver",
        "category": "software",
        "summary": "Perth savings / deals platform (limited committed UI proof in-repo).",
        "photos": [
            "client/public/opengraph.jpg",
        ],
        "videos": [],
    },
    "OmniWord": {
        "name": "OmniWord",
        "category": "software",
        "summary": "Writing / cryptex web app (no committed UI screenshots found).",
        "photos": [],
        "videos": [],
    },
    "animesteam-os": {
        "name": "AnimeSteam.OS",
        "category": "software",
        "summary": "Anime-focused OS web app (icons only; no UI screenshots found).",
        "photos": [],
        "videos": [],
    },
    "Moonwake": {
        "name": "Moonwake",
        "category": "software",
        "summary": "S.I.R.E.-governed project (no committed UI screenshots found).",
        "photos": [],
        "videos": [],
    },
    "SIRE": {
        "name": "S.I.R.E.",
        "category": "tooling",
        "summary": "Sovereign engineering laws, control surfaces, and certification tooling.",
        "photos": [
            "evidence/sire-horizon-certification/01_SPLASH.png",
            "evidence/sire-horizon-certification/02_MAIN_1920x1080.png",
            "evidence/sire-horizon-certification/08_FLEET.png",
            "evidence/sire-horizon-certification/09_PRESERVATION.png",
            "evidence/sire-horizon-certification/10_RECOVERY.png",
            "evidence/fleet-command-v1/fleet-command-proof-annotated.png",
            "sire-web/src/assets/hero.png",
        ],
        "videos": [],
    },
    "Aethelgard": {
        "name": "Aethelgard",
        "category": "game",
        "summary": "Browser Three.js world / Wildborn baseline (known boot hang on current main).",
        "photos": [
            "docs/release/wildborn-baseline/amber-fox-select.png",
            "docs/release/wildborn-baseline/moon-lynx-select.png",
            "docs/release/wildborn-baseline/spirit-wyrmling-select.png",
            "docs/release/wildborn-baseline/amber-fox-hud.png",
            "docs/release/wildborn-baseline/moon-lynx-hud.png",
            "docs/release/wildborn-baseline/spirit-wyrmling-hud.png",
            "public/screenshot-wide.png",
        ],
        "videos": [],
        "notes": "AGENTS.md notes orphaned top-level ReferenceError blocks in-world boot.",
    },
    "aethelgard-unity": {
        "name": "Aethelgard Unity",
        "category": "game",
        "summary": "Unity port stub / companion (no visual proof found).",
        "photos": [],
        "videos": [],
    },
    "-Aetheria-Hyperstrike-Web": {
        "name": "Aetheria: Hyperstrike (Web)",
        "category": "game",
        "summary": "Browser game prototype with main-menu and combat proof shots.",
        "photos": [
            "artifacts/hyperstrike-proof/main_menu_super_art.jpg",
            "artifacts/hyperstrike-proof/combat_boss_encounter.jpg",
        ],
        "videos": [],
    },
    "Aetheria-Hyperstrike-Godot": {
        "name": "Aetheria: Hyperstrike (Godot)",
        "category": "game",
        "summary": "Godot campaign preview art.",
        "photos": [
            "artifacts/campaign_preview.png",
        ],
        "videos": [],
    },
    "bad-take-final-cut": {
        "name": "Mimic Mayhem / Bad Take",
        "category": "game",
        "summary": "Prop-hunt prototype (Godot screenshots + Three.js web build).",
        "photos": [
            "godot/screenshots/01-coop-hide-phase-start.png",
            "godot/screenshots/02-coop-both-morphed.png",
            "godot/screenshots/03-coop-hunt-phase.png",
            "godot/screenshots/04-coop-props-win.png",
        ],
        "videos": [],
    },
    "ASHEN-SUN": {
        "name": "ASHEN SUN",
        "category": "game",
        "summary": "Godot desert-temple exploration with software-render and Forward+ proof packs.",
        "photos": [
            "proof/game_capture_software/screens/01_spawn_landing_plaza.png",
            "proof/game_capture_software/screens/02_overview_temple_route.png",
            "proof/game_capture_software/screens/03_fork_nekhet_ward.png",
            "proof/game_capture_software/screens/04_guardian_courtyard.png",
            "evidence/software-render/capture_overview.png",
            "proof/native_forward_plus_visual_v3/screens/overview.png",
        ],
        "videos": [],
    },
    "Fossil.Os": {
        "name": "Fossil.OS",
        "category": "game",
        "summary": "Godot 4.7 fossil expedition loop with visual evidence packs.",
        "photos": [
            "evidence/visual/20260914T112235Z_63ccffb7a874/screens/02_strata_junction.png",
            "evidence/visual/20260914T112235Z_63ccffb7a874/screens/03_bone_canyon.png",
            "evidence/visual/20260914T112235Z_63ccffb7a874/screens/05_digging_reveal.png",
            "Docs/visual_references/bone_canyon_aaa_visual_target.png",
        ],
        "videos": [],
    },
    "Revamed-Mansion": {
        "name": "Revamed Mansion",
        "category": "game",
        "summary": "Family co-op mansion game with SHA-bound desktop/phone evidence.",
        "photos": [
            "docs/evidence/f2b95cbdc8d0c037c449c1b7527eb2654b07a63e/desktop-1920x1080/00-title-screen.png",
            "docs/evidence/f2b95cbdc8d0c037c449c1b7527eb2654b07a63e/desktop-1920x1080/19-act2-continuation-unlocked.png",
            "docs/sire-layout-sweep-20261011/desktop.png",
            "docs/sire-layout-sweep-20261011/phone-portrait.png",
            "docs/sire-layout-sweep-20261011/tablet-landscape.png",
            "docs/family-coop-demo-20261011.png",
        ],
        "videos": [],
    },
    "The-Wrong-Refl3ction": {
        "name": "The Wrong Reflection",
        "category": "game",
        "summary": "Horror mirror/co-op game with visual_proof screenshot set.",
        "photos": [
            "reports/visual_proof/01_Title_Screen.png",
            "reports/visual_proof/07_Darkroom.png",
            "reports/visual_proof/08_Isolation_Corridor.png",
            "reports/visual_proof/15_Mirror_Court.png",
            "reports/visual_proof/19_Pause_Settings.png",
            "reports/visual_proof/20_Split_Screen_CoOp.png",
            "reports/game_screenshots_and_proof/evidence_01_entry_cinematic.png",
            "reports/game_screenshots_and_proof/evidence_02_story_event.png",
        ],
        "videos": [],
    },
    "gloam-and-gear-heart-of-the-last-flame": {
        "name": "Gloam & Gear",
        "category": "game",
        "summary": "Godot 3D vertical slice with beta runtime proof screenshots.",
        "photos": [
            "KICKSTART_BUILD/GODOT_3D_POLISHED_VERTICAL_SLICE/BUILD_EVIDENCE/2026-11-18_beta_slice_runtime_proof/after_01_title.png",
            "KICKSTART_BUILD/GODOT_3D_POLISHED_VERTICAL_SLICE/BUILD_EVIDENCE/2026-11-18_beta_slice_runtime_proof/after_02_hub_start.png",
            "KICKSTART_BUILD/GODOT_3D_POLISHED_VERTICAL_SLICE/BUILD_EVIDENCE/2026-11-18_beta_slice_runtime_proof/after_03_mox_scan_pip.png",
            "KICKSTART_BUILD/GODOT_3D_POLISHED_VERTICAL_SLICE/BUILD_EVIDENCE/2026-11-18_beta_slice_runtime_proof/after_04_brambleboot.png",
            "KICKSTART_BUILD/GODOT_3D_POLISHED_VERTICAL_SLICE/BUILD_EVIDENCE/2026-11-18_beta_slice_runtime_proof/after_05_bloom_gate_puffdrake.png",
            "KICKSTART_BUILD/GODOT_3D_POLISHED_VERTICAL_SLICE/BUILD_EVIDENCE/2026-11-18_beta_slice_runtime_proof/after_06_restored_complete.png",
        ],
        "videos": [],
    },
    "hushkin-rumor-bloom": {
        "name": "Hushkin: Rumor Bloom",
        "category": "game",
        "summary": "Storybook / companion game with art-lock and gameplay contact sheets.",
        "photos": [
            "artifacts/lanternlight_village_v6_final.png",
            "artifacts/gameplay_contact_sheet_debug.png",
            "artifacts/art_lock_character_face_v1.png",
            "artifacts/gameplay_test_06_arena_shift.png",
            "assets/original/brand/moonring_stadium_key_art.png",
        ],
        "videos": [],
    },
    "the_great_green_valley": {
        "name": "The Great Green Valley",
        "category": "game",
        "summary": "Environment / character visual evidence pack.",
        "photos": [
            "docs/evidence/environment/ingame_meadow.png",
            "docs/evidence/environment/ingame_canyon.png",
            "docs/evidence/environment/ingame_trees.png",
            "docs/evidence/environment/canyon_three_quarter.png",
            "docs/evidence/characters/cinder_jaw_three_quarter.png",
            "art/great_green_valley_moodboard.png",
        ],
        "videos": [],
    },
    "OCEANIS": {
        "name": "OCEANIS",
        "category": "game",
        "summary": "KRAIT Godot ocean game (no committed UI screenshots in this checkout).",
        "photos": [],
        "videos": [],
    },
    "venomward": {
        "name": "VENOMWARD",
        "category": "game",
        "summary": "KRAIT Godot game on sire/build-venomward (no committed UI screenshots).",
        "photos": [],
        "videos": [],
    },
    "DOOMBOAT-LAST-RIGHTS": {
        "name": "DOOMBOAT: Last Rights",
        "category": "game",
        "summary": "KRAIT Godot game (no committed UI screenshots in this checkout).",
        "photos": [],
        "videos": [],
    },
}


def git_meta(repo: Path) -> dict:
    def run(*args: str) -> str:
        return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()

    return {
        "branch": run("rev-parse", "--abbrev-ref", "HEAD"),
        "sha": run("rev-parse", "HEAD"),
        "sha_short": run("rev-parse", "--short", "HEAD"),
        "commit_date": run("log", "-1", "--format=%cI"),
        "subject": run("log", "-1", "--format=%s"),
        "remote": run("config", "--get", "remote.origin.url"),
    }


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_name(rel: str) -> str:
    return rel.replace("/", "__").replace(" ", "_")


def copy_media(repo: Path, rel: str, dest_dir: Path, kind: str) -> dict | None:
    src = repo / rel
    if not src.is_file():
        return {
            "status": "MISSING",
            "source_rel": rel,
            "kind": kind,
        }
    size = src.stat().st_size
    if size > MAX_BYTES:
        return {
            "status": "SKIPPED_TOO_LARGE",
            "source_rel": rel,
            "kind": kind,
            "bytes": size,
        }
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_name = safe_name(rel)
    dest = dest_dir / dest_name
    shutil.copy2(src, dest)
    digest = sha256_file(dest)
    return {
        "status": "COPIED",
        "kind": kind,
        "source_rel": rel,
        "showcase_rel": str(dest.relative_to(OUT_ROOT)).replace("\\", "/"),
        "bytes": size,
        "sha256": digest,
        "ext": src.suffix.lower(),
    }


def proof_status(photos: list, videos: list) -> str:
    ok_photos = [p for p in photos if p and p.get("status") == "COPIED"]
    ok_videos = [v for v in videos if v and v.get("status") == "COPIED"]
    if ok_photos and ok_videos:
        return "HAS_PHOTOS_AND_VIDEOS"
    if ok_photos:
        return "HAS_PHOTOS_ONLY"
    if ok_videos:
        return "HAS_VIDEOS_ONLY"
    return "NO_VISUAL_PROOF"


def build() -> dict:
    if OUT_ROOT.exists():
        shutil.rmtree(OUT_ROOT)
    projects_dir = OUT_ROOT / "projects"
    projects_dir.mkdir(parents=True)

    built_at = datetime.now(timezone.utc).isoformat()
    projects = []

    for repo_name, cfg in CURATED.items():
        repo = REPOS_ROOT / repo_name
        if not (repo / ".git").exists():
            projects.append(
                {
                    "repo": repo_name,
                    "name": cfg["name"],
                    "status": "REPO_MISSING",
                    "category": cfg["category"],
                }
            )
            continue

        meta = git_meta(repo)
        slug = cfg["name"].lower().replace(" ", "-").replace(".", "").replace(":", "").replace("/", "-")
        slug = "".join(c for c in slug if c.isalnum() or c in "-_")
        dest = projects_dir / slug
        photo_dir = dest / "photos"
        video_dir = dest / "videos"

        photos = []
        for rel in cfg.get("photos", [])[:MAX_PER_PROJECT]:
            photos.append(copy_media(repo, rel, photo_dir, "photo"))

        videos = []
        for rel in cfg.get("videos", [])[:MAX_VIDEOS]:
            videos.append(copy_media(repo, rel, video_dir, "video"))

        status = proof_status(photos, videos)
        entry = {
            "repo": repo_name,
            "name": cfg["name"],
            "slug": slug,
            "category": cfg["category"],
            "summary": cfg["summary"],
            "notes": cfg.get("notes"),
            "github": meta["remote"].replace("git@", "https://").replace("github.com:", "github.com/").removesuffix(".git")
            if meta["remote"].endswith(".git") or "github" in meta["remote"]
            else meta["remote"],
            "branch": meta["branch"],
            "sha": meta["sha"],
            "sha_short": meta["sha_short"],
            "commit_date": meta["commit_date"],
            "commit_subject": meta["subject"],
            "proof_status": status,
            "photo_count": sum(1 for p in photos if p and p.get("status") == "COPIED"),
            "video_count": sum(1 for v in videos if v and v.get("status") == "COPIED"),
            "photos": photos,
            "videos": videos,
            "folder": f"projects/{slug}",
        }
        # fix photo markdown links properly
        photo_md = []
        for p in photos:
            if p and p.get("status") == "COPIED":
                fname = Path(p["showcase_rel"]).name
                photo_md.append(
                    f"### `{p['source_rel']}`\n\n"
                    f"![UI](photos/{fname})\n\n"
                    f"- sha256: `{p['sha256']}`\n"
                    f"- source HEAD: `{meta['sha_short']}`\n"
                )
        video_md = []
        for v in videos:
            if v and v.get("status") == "COPIED":
                fname = Path(v["showcase_rel"]).name
                video_md.append(
                    f"- [`{v['source_rel']}`](videos/{fname}) — sha256 `{v['sha256']}`"
                )
        body = [
            f"# {cfg['name']}",
            "",
            f"- **Repo:** `{repo_name}`",
            f"- **Branch:** `{meta['branch']}`",
            f"- **Exact HEAD:** `{meta['sha']}`",
            f"- **Commit date:** {meta['commit_date']}",
            f"- **Proof status:** `{status}`",
            f"- **Photos:** {entry['photo_count']}",
            f"- **Videos:** {entry['video_count']}",
            "",
            cfg["summary"],
            "",
        ]
        if cfg.get("notes"):
            body += [f"> Note: {cfg['notes']}", ""]
        if photo_md:
            body += ["## Photos", "", *photo_md]
        if video_md:
            body += ["## Videos", "", *video_md, ""]
        if status == "NO_VISUAL_PROOF":
            body += [
                "## Gap",
                "",
                "No committed UI screenshot or video was found for this checkout.",
                "Do not treat this project as visually audited until fresh proof is captured on the exact HEAD above.",
                "",
            ]
        (dest / "README.md").write_text("\n".join(body), encoding="utf-8")
        projects.append(entry)

    manifest = {
        "title": "Bryson — Git Profile Software Showcase & Visual Audit",
        "built_at_utc": built_at,
        "rules": [
            "Media is copied from existing repo evidence only — nothing invented.",
            "Each file records source path, source HEAD SHA, and content SHA-256.",
            "NO_VISUAL_PROOF means audit gap, not a pass.",
            "Committed historical proof is not automatic certification of current live deploy.",
        ],
        "counts": {
            "projects": len(projects),
            "with_photos": sum(1 for p in projects if p.get("photo_count", 0) > 0),
            "with_videos": sum(1 for p in projects if p.get("video_count", 0) > 0),
            "no_visual_proof": sum(1 for p in projects if p.get("proof_status") == "NO_VISUAL_PROOF"),
            "total_photos": sum(p.get("photo_count", 0) for p in projects),
            "total_videos": sum(p.get("video_count", 0) for p in projects),
        },
        "projects": projects,
    }

    (OUT_ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    write_audit_md(manifest)
    write_gallery_html(manifest)
    write_root_readme(manifest)
    return manifest


def write_root_readme(manifest: dict) -> None:
    c = manifest["counts"]
    lines = [
        "# Software Profile Showcase — Visual Audit Pack",
        "",
        "Curated folder of **latest-checkout UI photos and verified videos** across Bryson's public software and game repos, for audit and portfolio review.",
        "",
        f"- Built (UTC): `{manifest['built_at_utc']}`",
        f"- Projects indexed: **{c['projects']}**",
        f"- With photos: **{c['with_photos']}**",
        f"- With videos: **{c['with_videos']}**",
        f"- No visual proof yet: **{c['no_visual_proof']}**",
        f"- Total photos copied: **{c['total_photos']}**",
        f"- Total videos copied: **{c['total_videos']}**",
        "",
        "## How to use",
        "",
        "1. Open [`AUDIT.md`](AUDIT.md) for the status board.",
        "2. Open [`gallery.html`](gallery.html) for a local photo/video browser.",
        "3. Open each `projects/<slug>/` folder for per-project media + SHA.",
        "4. Machine-readable index: [`manifest.json`](manifest.json).",
        "",
        "## Proof honesty",
        "",
    ]
    for r in manifest["rules"]:
        lines.append(f"- {r}")
    lines += ["", "## Projects", ""]
    for p in manifest["projects"]:
        if p.get("status") == "REPO_MISSING":
            lines.append(f"- **{p['name']}** — REPO_MISSING")
            continue
        lines.append(
            f"- **[{p['name']}]({p['folder']}/)** — `{p['proof_status']}` — "
            f"`{p['sha_short']}` on `{p['branch']}` — "
            f"{p['photo_count']} photos / {p['video_count']} videos"
        )
    lines.append("")
    (OUT_ROOT / "README.md").write_text("\n".join(lines), encoding="utf-8")


def write_audit_md(manifest: dict) -> None:
    rows = [
        "# Visual Audit Board",
        "",
        f"Generated: `{manifest['built_at_utc']}`",
        "",
        "| Project | Category | Branch | HEAD | Commit date | Proof | Photos | Videos | Folder |",
        "|---|---|---|---|---|---|---:|---:|---|",
    ]
    for p in manifest["projects"]:
        if p.get("status") == "REPO_MISSING":
            rows.append(f"| {p['name']} | {p.get('category','')} | — | — | — | REPO_MISSING | 0 | 0 | — |")
            continue
        rows.append(
            f"| [{p['name']}]({p['folder']}/) | {p['category']} | `{p['branch']}` | "
            f"`{p['sha_short']}` | {p['commit_date'][:10]} | `{p['proof_status']}` | "
            f"{p['photo_count']} | {p['video_count']} | [{p['folder']}]({p['folder']}/) |"
        )
    rows += [
        "",
        "## Priority gaps (no visual proof on this checkout)",
        "",
    ]
    gaps = [p for p in manifest["projects"] if p.get("proof_status") == "NO_VISUAL_PROOF"]
    if not gaps:
        rows.append("None.")
    else:
        for p in gaps:
            rows.append(f"- **{p['name']}** (`{p['repo']}` @ `{p.get('sha_short','?')}`) — {p.get('summary','')}")
    rows += [
        "",
        "## Video coverage note",
        "",
        "Only DentalStudio.OS currently contributes committed workflow videos into this pack. "
        "Other projects have photo evidence only unless fresh recordings are added.",
        "",
    ]
    (OUT_ROOT / "AUDIT.md").write_text("\n".join(rows), encoding="utf-8")


def write_gallery_html(manifest: dict) -> None:
    cards = []
    for p in manifest["projects"]:
        if p.get("status") == "REPO_MISSING":
            continue
        media = []
        for ph in p.get("photos") or []:
            if ph and ph.get("status") == "COPIED":
                media.append(
                    f'<figure><img src="{ph["showcase_rel"]}" alt="{p["name"]}" loading="lazy"/>'
                    f'<figcaption>{ph["source_rel"]}</figcaption></figure>'
                )
        for v in p.get("videos") or []:
            if v and v.get("status") == "COPIED":
                media.append(
                    f'<figure><video controls preload="metadata" src="{v["showcase_rel"]}"></video>'
                    f'<figcaption>{v["source_rel"]}</figcaption></figure>'
                )
        if not media:
            media.append('<p class="gap">NO_VISUAL_PROOF — capture required on listed HEAD.</p>')
        cards.append(
            f'<section class="project" data-status="{p["proof_status"]}" data-cat="{p["category"]}">'
            f'<header><h2>{p["name"]}</h2>'
            f'<p class="meta"><code>{p["sha_short"]}</code> · <code>{p["branch"]}</code> · '
            f'<span class="badge">{p["proof_status"]}</span></p>'
            f'<p>{p["summary"]}</p></header>'
            f'<div class="grid">{"".join(media)}</div></section>'
        )
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Profile Showcase — Visual Audit Gallery</title>
<style>
:root {{
  --bg: #0f1412;
  --panel: #18211c;
  --ink: #e8f0ea;
  --muted: #9bb0a2;
  --accent: #c4a35a;
  --gap: #c45c4a;
  --ok: #6fbf8a;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0; font-family: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
  background:
    radial-gradient(1200px 600px at 10% -10%, #24352c 0%, transparent 60%),
    radial-gradient(900px 500px at 100% 0%, #2a2418 0%, transparent 50%),
    var(--bg);
  color: var(--ink);
}}
header.hero {{
  padding: 2.5rem 1.5rem 1rem; max-width: 1200px; margin: 0 auto;
}}
header.hero h1 {{
  font-size: clamp(2rem, 4vw, 3rem); margin: 0 0 .4rem; letter-spacing: .02em;
}}
header.hero p {{ color: var(--muted); max-width: 60ch; }}
.stats {{ display: flex; flex-wrap: wrap; gap: .75rem; margin: 1rem 0 0; }}
.stats span {{
  background: var(--panel); border: 1px solid #2d3c34; padding: .45rem .75rem; border-radius: 4px;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: .85rem;
}}
nav.filters {{
  position: sticky; top: 0; z-index: 5; backdrop-filter: blur(8px);
  background: rgba(15,20,18,.85); border-bottom: 1px solid #2d3c34;
  padding: .75rem 1.5rem; display: flex; flex-wrap: wrap; gap: .5rem;
}}
nav.filters button {{
  background: transparent; color: var(--ink); border: 1px solid #3a4b42;
  padding: .35rem .7rem; border-radius: 999px; cursor: pointer;
}}
nav.filters button.active {{ background: var(--accent); color: #1a1408; border-color: var(--accent); }}
main {{ max-width: 1200px; margin: 0 auto; padding: 1rem 1.5rem 4rem; }}
.project {{
  margin: 1.5rem 0 2.5rem; padding: 1.25rem; background: rgba(24,33,28,.7);
  border: 1px solid #2d3c34; border-radius: 8px;
}}
.project h2 {{ margin: 0 0 .35rem; font-size: 1.45rem; }}
.meta {{ color: var(--muted); font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: .85rem; }}
.badge {{ color: var(--ok); }}
.project[data-status="NO_VISUAL_PROOF"] .badge {{ color: var(--gap); }}
.grid {{
  display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: .85rem; margin-top: 1rem;
}}
figure {{ margin: 0; background: #0b100e; border: 1px solid #24302a; border-radius: 6px; overflow: hidden; }}
img, video {{ display: block; width: 100%; height: 180px; object-fit: cover; background: #000; }}
figcaption {{
  padding: .45rem .55rem; font-size: .72rem; color: var(--muted);
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  word-break: break-all;
}}
.gap {{ color: var(--gap); font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
</style>
</head>
<body>
<header class="hero">
  <h1>Git Profile Showcase</h1>
  <p>Verified UI photos and videos copied from repo evidence for audit. Historical screenshots are not automatic live-deploy certification.</p>
  <div class="stats">
    <span>projects {manifest['counts']['projects']}</span>
    <span>photos {manifest['counts']['total_photos']}</span>
    <span>videos {manifest['counts']['total_videos']}</span>
    <span>gaps {manifest['counts']['no_visual_proof']}</span>
    <span>{manifest['built_at_utc']}</span>
  </div>
</header>
<nav class="filters">
  <button class="active" data-filter="all">All</button>
  <button data-filter="software">Software</button>
  <button data-filter="game">Games</button>
  <button data-filter="tooling">Tooling</button>
  <button data-filter="NO_VISUAL_PROOF">Gaps only</button>
</nav>
<main>
{''.join(cards)}
</main>
<script>
const buttons = document.querySelectorAll('nav.filters button');
const sections = document.querySelectorAll('.project');
buttons.forEach(btn => btn.addEventListener('click', () => {{
  buttons.forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  const f = btn.dataset.filter;
  sections.forEach(s => {{
    const show = f === 'all'
      || s.dataset.cat === f
      || s.dataset.status === f;
    s.style.display = show ? '' : 'none';
  }});
}}));
</script>
</body>
</html>
"""
    (OUT_ROOT / "gallery.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    m = build()
    print(json.dumps(m["counts"], indent=2))
    print("Wrote", OUT_ROOT)
