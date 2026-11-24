# AGENTS.md

## Cursor Cloud specific instructions

This repository is a profile README. It has no install step and no server.

The shared Cloud Agent environment checks the studio out under `/agent/repos/<name>`. Godot 4.7.2 stable is on `PATH` as `godot`. Node is v22. On boot, four dev servers start:

| App | URL |
| --- | --- |
| Aethelgard | http://127.0.0.1:5173 |
| bad-take-final-cut web (Midnight Madhouse) | http://127.0.0.1:5174 |
| DentalStudio.OS | http://127.0.0.1:8080 |
| Vishvakarma.OS | http://127.0.0.1:5175 |

Vishvakarma's gitignored `.env.local` sets `VITE_ALLOW_LOCAL_DEMO=true` so `/editor` opens without Google sign-in. Other web apps are installed when they have a lockfile and are left stopped so they do not take port 5173.
