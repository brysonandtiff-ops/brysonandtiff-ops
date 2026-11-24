# brysonandtiff-ops — Completion Plan & Build Laws

This repository follows the S.I.R.E. canonical eight-step build laws:

**FIND → PLAN → BUILD → TEST → SHOW → HARDEN → PROVE → FINISH**

Canonical reference (external):  
[SIRE-CANONICAL_STEP_BUILDING_LAWS.md](https://github.com/brysonandtiff-ops/SIRE/blob/main/docs/engineering-laws/SIRE-CANONICAL_STEP_BUILDING_LAWS.md)

Read this file in **FIND** before mutating.

---

## Product (plain language)

**brysonandtiff-ops** is a **thin organisation meta repository**: a public index of Bryson’s software, systems, and game-development work. It is **not** an application codebase. Product work belongs in the linked product repos (Vishvakarma.OS, PerthSaver, iCrystal.OS, PRISMAFLOW, Aetheria, Midnight, S.I.R.E., and others).

---

## Completion north star

1. `README.md` stays an accurate, current index of public work — no stale “selected” links that misrepresent status.
2. No parallel app trees or product source land here by accident.
3. Engineering-approach wording stays evidence-honest (historical build ≠ current proof).
4. Cross-links to product repos remain the path for real build/test/release work.
5. Never invent **GREEN** for products from this meta repo alone.

---

## The eight steps (every change)

| Step | Name | What you do here |
| :---: | :--- | :--- |
| **1** | **FIND** | Exact HEAD SHA; confirm this is meta-only; check README link accuracy |
| **2** | **PLAN** | Docs/index edits only unless owner explicitly expands scope |
| **3** | **BUILD** | Feature branch; touch README/docs — do not invent an app tree |
| **4** | **TEST** | Link/path sanity; no product test suite exists here |
| **5** | **SHOW** | N/A for pure index text unless a published profile page is in scope |
| **6** | **HARDEN** | No secrets; no copied product credentials |
| **7** | **PROVE** | LAW-101 disclosure for substantial index changes |
| **8** | **FINISH** | Commit/push on feature branch; PASS / FAIL / BLOCKED / NOT RUN |

Merge of meta edits still follows owner preference; **product** merge/release remains phone-gated in each product repo.

---

## Ordered next steps

1. Keep the selected-public-work list aligned with real GitHub repos and honest one-line descriptions.
2. Point agents and humans to product repos for implementation — do not grow this into a monorepo.
3. When a product’s public status changes (name, URL, retirement), update the index in the same mission.
4. Leave completion plans and evidence inside each product’s own `docs/SIRE_COMPLETION_AND_BUILD_LAWS.md`.
5. Owner phone path for any org-level publication that claims product readiness.

---

## Honest blockers

- **Thin org meta only:** there is no app to “complete” here. Treating this repo as a product build target is a process error.
- **No substitute for product gates:** verifying Vishvakarma, PerthSaver, Midnight, etc. must happen in those repositories with their own tests and evidence.
- **Index drift:** an outdated README can imply a product state that the product repo no longer claims — fix the index or the product docs, do not invent GREEN in either.

---

## Software-building AI autonomy

Authorised cloud agents may run **24/7** on feature branches for **docs/index** maintenance through FIND→FINISH.

- Do not use this repo’s autonomy loop to ship product code.
- Product merge/release stays **phone-gated** in the owning product repository.
- Never invent **GREEN**. `UNKNOWN` = fail-closed.

---

## Fleet status — 2026-11-24 (Wave B)

Canonical control-plane record (S.I.R.E. repo):  
`docs/SYSTEM_UPGRADES_WAVE_B_2026-11-24.md` · `docs/ECOSYSTEM_COMPLETION_WAVE_2026-11-24.md` · `docs/FLEET_STATUS_WAVE_B_2026-11-24.md`

**Phone-merged this wave (exact main SHAs):**
- SIRE Wave B `123c7aa9` (PR #844) — doctor honesty, local verify allowlist, Connections Git Stop, UI soft-lie cleanup
- Aethelgard orphan XP boot fix `ce21b08` (PR #151)
- Fossil.Os autocert `push: main` `fd04200` (PR #98)
- The-Wrong-Refl3ction autocert + unreal `push: main` `c534f91` (PR #35)
- OCEANIS read-only blockout integrity on every main push `cb433cb` (PR #10)

**Still HOLD / NOT_VERIFIED (fleet-wide):**
- LAW-105 fresh screenshots and full-clip videos on exact HEAD
- Horizon game-engine release (no engine source in SIRE)
- KRAIT verified trained model / live inference
- True 24×7 Auto (cloud doctor READY + phone-gated install)
- ChatGPT MCP gateway deploy + OAuth secrets
- Mission dispatch execution (local verify allowlist ≠ mission POST)

**This repo — status note:**
- Org meta / index only. Keep fleet pointers accurate; no parallel app trees. Wave B phone merges recorded in SIRE fleet status doc.

