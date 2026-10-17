# AI Governance — UX replica (demo version)

Clickable replica of the **AI Governance** mode of AppMod.AI, rebuilt to match the product demo recording (Appmod.AI theme).
Text and numbers are copied verbatim from the demo frames; layout is matched side-by-side against them.

**Live:** https://andy07-debug.github.io/ai-governance-clone/

## Screens
| Screen | What's in it |
|---|---|
| `#dashboard` | Global dashboard: Security, FinOps, System Health, Change Management panels with trend charts, breaking news, key metrics, live alerts, recent activity, section cards |
| `#llm-studio` | LLM Studio Analytics: cost trend (LLM / Infra / Total), KPI tiles, Top assistants / users / agents tabs, All Records; drill-down drawers for assistant **ggcllmprgenie** and user **aadhithya.sendhilmanian** |
| `#firewall` | Firewall Overview: security trend, KPI cards, real-time event stream with inline alert detail and Cognitive Decisioning AI |
| `#policies` / `#policies-change-logs` | Smart AI Prompt Policies deck, Create New Governance Policy modal, change-log audit table |
| `#budget-setup` | My Usage, Platform Usage, Setup Budget tabs |

Deep-link any screen with its hash; open an overlay too with `#screen+overlay`, e.g. `#llm-studio+llm-assistant-ggcllmprgenie`.
Sections of the demo not yet rebuilt (Live Events, Traffic Analysis, IP Whitelisting, System Health, global Change Logs, RBAC) are linked but inert.

## How it's built
| Path | What |
|---|---|
| `clone/` | Built site (`index.html` + `assets/`) |
| `v2/screens/`, `v2/overlays/` | Hand-built screen and drawer/modal fragments (Tailwind classes) |
| `v2/build_v2.py` | Builds `clone/`: real captured AppMod shell (re-themed) + screens + Tailwind CSS |
| `v2/router.js` | Navigation, overlays, tabs, toggles, Chart.js charts (`data-go`, `data-open`, `data-tab`, `data-chart` …) |
| `v2/BUILDING.md` | Conventions for adding screens |
| `v2/tools/shot.py` | Render a screen at the demo's 1512×863 @2x and compare with a demo frame |
| `v2/tools/test_v2.py` | Clicks every wired control on every screen |
| `demo/sections/`, `demo/transcript.txt` | Per-section demo frame index + narration transcript |
| `capture/`, `build.py` | Original live-app DOM captures (source of the shell) and the v1 build pipeline |

Rebuild: `cd v2 && npm install && cd .. && python3 v2/build_v2.py`. Test: `python3 v2/tools/test_v2.py`.
