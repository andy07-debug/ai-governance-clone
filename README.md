# AI Governance Mode — UX replica

Static, clickable replica of the **AI Governance** mode of AppMod.AI, built from live DOM snapshots of the logged-in app (captured 2026-10-15).

## View it
Live: https://andy07-debug.github.io/ai-governance-clone/ — or open `clone/index.html` locally in Chrome (works offline). Deep-link to any screen with a hash, e.g. `clone/index.html#05d-traffic-statistics`.

23 screens: landing grid, LLM Studio Analytics, Firewall Overview, Live Events, Policies (deck / change logs / New Policy), Smart LLM Load Balancer (projects, usage, model config, statistics, applications, error logs), RBAC (access management, user groups, modules, permissions, roles, mapping), and the shell overlays (mode dropdown, conversation drawer, projects).

Working interactions: navigation and breadcrumbs, fullscreen mode, mode dropdown + search, drawer, segmented pills, collapsible sections, accordion, log "more", checkbox, typing in chat/forms, browser Back/Forward. Charts are live Chart.js 4.5.1 canvases with the app's own configs. Data is frozen at capture time; nothing submits or saves.

## Layout
| Path | What |
|---|---|
| `clone/` | The built replica (`index.html` + `assets/`) |
| `capture/` | Raw DOM + CSSOM snapshots per screen (source for the build) |
| `build.py` | Builds `clone/` from `capture/` (CSS merge, font localisation, overlay stripping, templates) |
| `router.js` | Click/hash router inlined into the build |
| `charts.js` | Chart configs + recovered data |
| `qa/` | Playwright test suites (`test_router.py`, `test_findings.py`), render/diff and chart-fitting scripts, QA artefacts |

Rebuild: `python3 build.py`. Tests: `python3 qa/test_router.py && python3 qa/test_findings.py`.

> Contains data captured from the live app (names, emails, usage and cost figures).
