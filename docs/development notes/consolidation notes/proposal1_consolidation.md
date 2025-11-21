# Tech Stack Consolidation Proposal
## Database & Service Architecture

---

## Architecture Overview: 37 Tools → 6 Consolidated Services

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    TIER 1: SAME STACK - EASY MERGE                          │
│                         (HIGHEST ROI - 23 Projects)                         │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  GROUP A: Python + FastAPI + PostgreSQL (8 Projects)                       │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │              jane-platform (Modular Monolith)                         │  │
│  │  ┌────────────────────────────────────────────────────────────────┐  │  │
│  │  │  API Gateway Layer (FastAPI Router)                            │  │  │
│  │  │  Routes: /api/v1/{domain}/*                                    │  │  │
│  │  └────────────────┬───────────────────────────────────────────────┘  │  │
│  │                   │                                                   │  │
│  │       ┌───────────┼───────────┬───────────┬───────────┬─────────┐   │  │
│  │       │           │           │           │           │         │   │  │
│  │       ▼           ▼           ▼           ▼           ▼         ▼   │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ...  │  │
│  │  │Dispatch │ │HexStrike│ │ Mealie  │ │   MTG   │ │ Nemesis │      │  │
│  │  │ Module  │ │ Module  │ │ Module  │ │ Module  │ │ Module  │      │  │
│  │  │(FastAPI)│ │(FastAPI)│ │(FastAPI)│ │(FastAPI)│ │(FastAPI)│      │  │
│  │  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘      │  │
│  │       │           │           │           │           │            │  │
│  │       │  No Direct DB Access - Uses Dapr State Store API          │  │
│  │       │           │           │           │           │            │  │
│  │       ▼           ▼           ▼           ▼           ▼            │  │
│  │  ┌──────────────────────────────────────────────────────────────┐  │  │
│  │  │              Dapr Sidecar (localhost:3500)                   │  │  │
│  │  │  ┌────────────┐  ┌────────────┐  ┌────────────┐             │  │  │
│  │  │  │ State API  │  │ Pub/Sub    │  │  Secrets   │             │  │  │
│  │  │  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘             │  │  │
│  │  └────────┼───────────────┼───────────────┼────────────────────┘  │  │
│  │           │               │               │                        │  │
│  └───────────┼───────────────┼───────────────┼────────────────────────┘  │
│              │               │               │                            │
│              ▼               ▼               ▼                            │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Dapr State Store Components (per module)                       │    │
│  │  ┌───────────────────────────────────────────────────────────┐  │    │
│  │  │  dispatch-state:                                           │  │    │
│  │  │    type: state.postgresql                                  │  │    │
│  │  │    metadata:                                               │  │    │
│  │  │      - connectionString: ...&search_path=dispatch          │  │    │
│  │  │      - tableName: dapr_state_dispatch                      │  │    │
│  │  │                                                             │  │    │
│  │  │  hexstrike-state:                                          │  │    │
│  │  │    type: state.postgresql                                  │  │    │
│  │  │    metadata:                                               │  │    │
│  │  │      - connectionString: ...&search_path=hexstrike         │  │    │
│  │  │      - tableName: dapr_state_hexstrike                     │  │    │
│  │  │                                                             │  │    │
│  │  │  [mealie-state, mtg-state, nemesis-state, jane-state...]  │  │    │
│  │  └───────────────────────────────────────────────────────────┘  │    │
│  └─────────────────────────┬───────────────────────────────────────┘    │
│                            │                                             │
│                            ▼                                             │
│              ┌─────────────────────────────┐                            │
│              │  PostgreSQL Instance #1     │                            │
│              │  ┌───────────────────────┐  │                            │
│              │  │ Schema: dispatch      │  │  ◄── Enforced by Dapr     │
│              │  │ Schema: hexstrike     │  │      component config     │
│              │  │ Schema: mealie        │  │      (search_path)        │
│              │  │ Schema: mtg_toolkit   │  │                            │
│              │  │ Schema: nemesis       │  │  ◄── Each module can ONLY │
│              │  │ Schema: jane          │  │      access its own schema│
│              │  └───────────────────────┘  │                            │
│              └─────────────────────────────┘                            │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  GROUP B: Python + Django + PostgreSQL (3 Projects)                        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │              jane-django-platform (Modular Monolith)                  │  │
│  │  ┌────────────────────────────────────────────────────────────────┐  │  │
│  │  │  Django Project Root                                           │  │  │
│  │  │  URLs: /admin, /api/{app}/*                                    │  │  │
│  │  └────────────────┬───────────────────────────────────────────────┘  │  │
│  │                   │                                                   │  │
│  │       ┌───────────┼───────────┬───────────────────┐                  │  │
│  │       │           │           │                   │                  │  │
│  │       ▼           ▼           ▼                   ▼                  │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐                             │  │
│  │  │Commander │ │Ghostwrite│ │ Nemesis  │                             │  │
│  │  │Spellbook │ │   App    │ │Django App│                             │  │
│  │  │Django App│ │(DRF API) │ │          │                             │  │
│  │  └────┬─────┘ └────┬─────┘ └────┬─────┘                             │  │
│  │       │            │            │                                    │  │
│  │       │  Django ORM with DATABASE_ROUTERS (schema isolation)        │  │
│  │       │            │            │                                    │  │
│  │       ▼            ▼            ▼                                    │  │
│  │  ┌──────────────────────────────────────────────────────────────┐  │  │
│  │  │         Database Router (settings.py)                        │  │  │
│  │  │  class SchemaRouter:                                         │  │  │
│  │  │    def db_for_read(model, **hints):                          │  │  │
│  │  │      if model._meta.app_label == 'spellbook':                │  │  │
│  │  │        return 'spellbook'  # Uses spellbook schema           │  │  │
│  │  │      elif model._meta.app_label == 'ghostwriter':            │  │  │
│  │  │        return 'ghostwriter' # Uses ghostwriter schema        │  │  │
│  │  │                                                               │  │  │
│  │  │  DATABASES = {                                                │  │  │
│  │  │    'spellbook': {'OPTIONS': {'options': '-c search_path=...}}│  │  │
│  │  │    'ghostwriter': {'OPTIONS': {'options': '-c search_path=..│  │  │
│  │  │  }                                                            │  │  │
│  │  └───────────────────────┬──────────────────────────────────────┘  │  │
│  │                          │                                          │  │
│  └──────────────────────────┼──────────────────────────────────────────┘  │
│                             │                                             │
│                             ▼                                             │
│               ┌─────────────────────────────┐                            │
│               │  PostgreSQL Instance #1     │                            │
│               │  ┌───────────────────────┐  │                            │
│               │  │ Schema: cmd_spellbook │  │  ◄── Django ORM enforces   │
│               │  │ Schema: ghostwriter   │  │      bounded contexts via  │
│               │  │ Schema: nemesis_dj    │  │      DATABASE_ROUTERS      │
│               │  └───────────────────────┘  │                            │
│               └─────────────────────────────┘                            │
│                                                                           │
│  Note: Django apps use native ORM with schema routing instead of Dapr   │
│        (Django's ORM already provides bounded context enforcement)       │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  GROUP C: TypeScript + React + Node.js (21+ Frontend Applications)        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                    jane-ui-platform (Next.js 15.5.2)                 │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌──────────┐   │  │
│  │  │   Actual    │  │  HexStrike  │  │  Inspector  │  │   MTG    │   │  │
│  │  │   Budget    │  │     UI      │  │     UI      │  │ Toolkit  │   │  │
│  │  │  (React)    │  │  (React)    │  │  (React)    │  │  (React) │   │  │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └────┬─────┘   │  │
│  │         │                │                │               │          │  │
│  │         │     ┌──────────┴────────┐       │               │          │  │
│  │         │     │   Nemesis UI      │       │               │          │  │
│  │         │     │    (React)        │       │               │          │  │
│  │         │     └──────────┬────────┘       │               │          │  │
│  │         └────────────────┴────────────────┴───────────────┘          │  │
│  │                              │                                        │  │
│  │  FRONTEND UI CONSOLIDATION (21+ Applications):                       │  │
│  │  ┌──────────────────────────────────────────────────────────────┐  │  │
│  │  │ Security Domain (7):  Nemesis, CyberChef, Dispatch, KasmVNC,  │  │  │
│  │  │                      Ghostwriter, MISP, Maltrail              │  │  │
│  │  │ Productivity Domain (6): Actual, n8n, Mealie, Inspector,       │  │  │
│  │  │                         OneX, Dashboard                        │  │  │
│  │  │ AI Domain (4):       Goose, Docs, Firecrawl, Monitoring       │  │  │
│  │  │ TCG Domain (2):      Commander Spellbook, Client Library       │  │  │
│  │  └──────────────────────────────────────────────────────────────┘  │  │
│  │                              │                                        │  │
│  │                    Unified Component Library                          │  │
│  │   libs/ui: Domain-specific components, Auth, Theme, Navigation       │  │
│  └──────────────────────────────┬─────────────────────────────────────┘  │
│                                  │                                        │
│                                  ▼                                        │
│              ┌───────────────────────────────────────┐                   │
│              │  Backend APIs (from Groups A & B)     │                   │
│              │  - jane-platform-api (FastAPI)        │                   │
│              │  - jane-django-platform (Django)      │                   │
│              └───────────────────────────────────────┘                   │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  GROUP D: Python MCP Servers (5 Projects)                                  │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                      jane-mcp-gateway                                 │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────┐ │  │
│  │  │  Chroma  │  │FileScope │  │ Malware  │  │VirusTotal│  │  n8n  │ │  │
│  │  │   MCP    │  │   MCP    │  │Bazaar MCP│  │   MCP    │  │  MCP  │ │  │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └───┬───┘ │  │
│  │       │             │             │             │             │      │  │
│  │       └─────────────┴─────────────┴─────────────┴─────────────┘      │  │
│  │                              │                                        │  │
│  │              Shared MCP Protocol Implementation                       │  │
│  │              Common Auth, Logging, Metrics                            │  │
│  └──────────────────────────────┬─────────────────────────────────────┘  │
│                                  │                                        │
│                                  ▼                                        │
│                    ┌─────────────────────────────┐                       │
│                    │   MCP Client Applications   │                       │
│                    │   (Goose, Claude, etc.)     │                       │
│                    └─────────────────────────────┘                       │
└────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                    TIER 2: SIMILAR STACK - UPGRADE PATH                     │
│                         (GOOD ROI - 6 Projects)                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  GROUP E: Flask → FastAPI Migration (6 Projects)                           │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  ┌────────────┐      Migrate      ┌─────────────────────────────┐   │  │
│  │  │MTG Cmd Map │  ───────────────►  │                             │   │  │
│  │  │  (Flask)   │                    │   Join GROUP A:             │   │  │
│  │  └────────────┘                    │   jane-platform-api         │   │  │
│  │  ┌────────────┐      Migrate      │   (FastAPI consolidated)    │   │  │
│  │  │  Maltrail  │  ───────────────►  │                             │   │  │
│  │  │  (Custom)  │                    │   +6 more FastAPI services  │   │  │
│  │  └────────────┘                    └─────────────────────────────┘   │  │
│  │  ┌────────────┐                                                       │  │
│  │  │ Forensic   │                                                       │  │
│  │  │    Kit     │                                                       │  │
│  │  └────────────┘                                                       │  │
│  │       +3 more Flask projects                                          │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  Result: 8 FastAPI projects → 14 FastAPI projects in GROUP A                │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  GROUP F: SQLite → PostgreSQL Upgrades (6 Projects)                        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  ┌─────────────┐    Upgrade    ┌──────────────────────────────┐     │  │
│  │  │Brute Ratel  │ ────────────► │  PostgreSQL Instance #1      │     │  │
│  │  │  (SQLite)   │               │  + Schema: brute_ratel       │     │  │
│  │  └─────────────┘               └──────────────────────────────┘     │  │
│  │  ┌─────────────┐    Upgrade                                          │  │
│  │  │  KasmVNC    │ ────────────► │  + Schema: kasmvnc           │     │  │
│  │  │  (SQLite)   │               │  + Schema: maltrail          │     │  │
│  │  └─────────────┘               │  + Schema: forensic_kit      │     │  │
│  │  ┌─────────────┐    Upgrade    │  + Schema: n8n (prod)        │     │  │
│  │  │  Maltrail   │ ────────────► │                              │     │  │
│  │  │  (SQLite)   │               └──────────────────────────────┘     │  │
│  │  └─────────────┘                                                     │  │
│  │       +3 more SQLite projects                                        │  │
│  │                                                                       │  │
│  │  ┌─────────────┐    KEEP LOCAL (Offline Required)                   │  │
│  │  │Actual Budget│ ───────────── Local SQLite Files                   │  │
│  │  │   Goose     │               (User preference + AI offline mode)  │  │
│  │  └─────────────┘                                                     │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  Result: 8 SQLite → 6 migrated to PostgreSQL, 2 kept local                  │
└────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                  TIER 3: STRATEGIC - STANDARDIZE INFRASTRUCTURE             │
│                         (MODERATE ROI - 5 Projects)                         │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  GROUP G: Node.js + Express Standardization (5 Projects)                   │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  Keep as Microservices, Standardize Infrastructure:                  │  │
│  │                                                                       │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │  │
│  │  │  Firecrawl   │  │  Inspector   │  │     n8n      │              │  │
│  │  │  (Express)   │  │  (Express)   │  │  (Express)   │              │  │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │  │
│  │         │                 │                 │                        │  │
│  │         └─────────────────┴─────────────────┘                        │  │
│  │                          │                                           │  │
│  │            Shared: Base Docker Image (node:20-alpine)                │  │
│  │                    Common Middleware (auth, logging)                 │  │
│  │                    Unified TypeScript Config                         │  │
│  │                    Shared API Gateway (Kong)                         │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  Result: Standardized infrastructure, NOT merged (different concerns)       │
└────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                  TIER 4: SPECIALIZED - KEEP SEPARATE                        │
│                         (Outliers - 8 Projects)                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  Performance-Critical (Compiled Languages)                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   YARA-X     │  │    Goose     │  │   KasmVNC    │  │ Meterpreter  │  │
│  │   (Rust)     │  │   (Rust)     │  │    (C/C++)   │  │   (C/C++)    │  │
│  │Pattern Match │  │  AI Agent    │  │ VNC Server   │  │  Payload     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  │
│  Reason: Max performance, low-level control, small footprint               │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  System-Level Tools (Bash/Shell)                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                    │
│  │  BlackArch   │  │   LScript    │  │     OneX     │                    │
│  │    (Bash)    │  │    (Bash)    │  │    (Bash)    │                    │
│  │ OS Distribution│ │Kali Automation│ │Security Kit  │                    │
│  └──────────────┘  └──────────────┘  └──────────────┘                    │
│  Reason: Standalone by design, system-level integration                    │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  Specialized Platforms (Unique Ecosystems)                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │     HELK     │  │SecurityOnion │  │     Kong     │  │     MISP     │  │
│  │(Elastic Stack│  │ (Multi-tool) │  │ (Lua/Nginx)  │  │  (PHP/Cake)  │  │
│  │     SIEM)    │  │    Suite     │  │ API Gateway  │  │ Threat Intel │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  │
│  Reason: Mature platforms, specialized infrastructure, own ecosystems      │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  Client-Side Only (No Backend)                                             │
│  ┌──────────────┐  ┌──────────────┐                                       │
│  │  CyberChef   │  │  IT-Tools    │                                       │
│  │ (Vanilla JS) │  │  (Vue.js)    │                                       │
│  │Browser-based │  │Browser Utils │                                       │
│  └──────────────┘  └──────────────┘                                       │
│  Reason: Pure client-side, no server consolidation possible                │
└────────────────────────────────────────────────────────────────────────────┘

```

---

## Shared Infrastructure Layer

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CONSOLIDATED DATABASES                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  Instance 1: PostgreSQL (Consolidated)                                     │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  18 Schemas Total:                                                    │  │
│  │                                                                       │  │
│  │  FastAPI Group (6):                                                  │  │
│  │    ├─ dispatch         (incident management)                         │  │
│  │    ├─ hexstrike        (security analysis)                           │  │
│  │    ├─ mealie           (recipe management)                           │  │
│  │    ├─ mtg_toolkit      (card analysis)                               │  │
│  │    ├─ nemesis          (post-exploitation)                           │  │
│  │    └─ jane             (orchestration)                               │  │
│  │                                                                       │  │
│  │  Django Group (3):                                                   │  │
│  │    ├─ commander_spellbook  (MTG combos)                              │  │
│  │    ├─ ghostwriter      (pentest reports)                             │  │
│  │    └─ nemesis_django   (Django components)                           │  │
│  │                                                                       │  │
│  │  TypeScript Group (2):                                               │  │
│  │    ├─ firecrawl        (web scraping)                                │  │
│  │    └─ n8n              (workflow automation)                         │  │
│  │                                                                       │  │
│  │  SQLite Upgrades (6):                                                │  │
│  │    ├─ brute_ratel      (C2 framework)                                │  │
│  │    ├─ kasmvnc          (remote desktop)                              │  │
│  │    ├─ maltrail         (traffic detection)                           │  │
│  │    ├─ forensic_kit     (code analysis)                               │  │
│  │    ├─ n8n_production   (n8n prod mode)                               │  │
│  │    └─ [reserved]                                                     │  │
│  │                                                                       │  │
│  │  Existing PostgreSQL Users (3):                                      │  │
│  │    ├─ meterpreter      (session data)                                │  │
│  │    ├─ kong             (API gateway config)                          │  │
│  │    └─ actual           (can optionally use PostgreSQL)               │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  Connection Pooling: PgBouncer (300 max connections)                        │
│  Backup Strategy: pg_dump daily + WAL archiving                             │
│  High Availability: PostgreSQL replication (optional)                       │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  Instance 2: Redis (Consolidated)                                          │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  16 Logical Databases (Redis DB 0-15):                               │  │
│  │                                                                       │  │
│  │  DB 0:  Dispatch cache              (incident data)                  │  │
│  │  DB 1:  HexStrike cache             (analysis results)               │  │
│  │  DB 2:  Mealie cache                (recipe data)                    │  │
│  │  DB 3:  Nemesis job queues          (RabbitMQ alternative)           │  │
│  │  DB 4:  Ghostwriter sessions        (Django sessions)                │  │
│  │  DB 5:  HELK temp data              (log processing)                 │  │
│  │  DB 6:  Firecrawl queues            (BullMQ jobs)                    │  │
│  │  DB 7:  MISP sessions               (PHP sessions)                   │  │
│  │  DB 8:  SecurityOnion cache         (temp processing)                │  │
│  │  DB 9:  n8n cache                   (workflow state)                 │  │
│  │  DB 10: [Reserved for future use]                                    │  │
│  │  DB 11: [Reserved for future use]                                    │  │
│  │  DB 12: [Reserved for future use]                                    │  │
│  │  DB 13: [Reserved for future use]                                    │  │
│  │  DB 14: [Reserved for future use]                                    │  │
│  │  DB 15: [Reserved for future use]                                    │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  Max Memory: 8GB (configurable)                                             │
│  Eviction Policy: allkeys-lru (Least Recently Used)                         │
│  Persistence: AOF (Append-Only File) enabled                                │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  Instance 3: Elasticsearch (Consolidated)                                  │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  Indices (with lifecycle policies):                                  │  │
│  │                                                                       │  │
│  │  dispatch-*          (incident search, 90-day retention)             │  │
│  │  nemesis-*           (file analysis, 180-day retention)              │  │
│  │  helk-*              (security logs, 30-day retention)               │  │
│  │  securityonion-*     (security events, 30-day retention)             │  │
│  │  misp-*              (threat intel, 365-day retention)               │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  Cluster: Single-node (dev), 3-node (prod)                                  │
│  Heap Size: 4GB (50% of available RAM)                                      │
│  Index Shards: 1 primary + 1 replica (configurable)                         │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  Instance 4: SQLite (Keep Local)                                           │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  Offline/Local-First Tools Only:                                     │  │
│  │                                                                       │  │
│  │  ├─ Actual Budget    (~/Documents/actual-budget.db)                  │  │
│  │  │   Reason: User preference for portable local files                │  │
│  │  │   Sync: Optional cloud sync (user-controlled)                     │  │
│  │  │                                                                    │  │
│  │  └─ Goose            (~/.config/goose/sessions.db)                   │  │
│  │      Reason: AI agent requires offline mode                          │  │
│  │      Sync: Not applicable (local context only)                       │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  Instance 5: Specialized Databases                                         │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  MongoDB (1 instance):                                                │  │
│  │    └─ RITA only           (network traffic analysis)                 │  │
│  │       Reason: Unique document structure for network analysis         │  │
│  │                                                                       │  │
│  │  MySQL/MariaDB (1 instance):                                         │  │
│  │    └─ MISP only           (threat intelligence platform)             │  │
│  │       Reason: PHP/CakePHP ecosystem, mature platform                 │  │
│  │                                                                       │  │
│  │  Chroma (Vector DB):                                                 │  │
│  │    ├─ HexStrike          (security analysis embeddings)              │  │
│  │    └─ MTG Toolkit        (card similarity embeddings)                │  │
│  │       Reason: AI/ML vector operations, semantic search               │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow: Cross-Group Communication

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DAPR SERVICE MESH + STATE MANAGEMENT                     │
│              (Enforcing DDD Bounded Contexts + Data Abstraction)            │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  CROSS-MODULE COMMUNICATION (Pub/Sub)                                       │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────────┐
                              │   Dapr Pub/Sub   │
                              │   (RabbitMQ)     │
                              └────────┬─────────┘
                                       │
       ┌───────────────────────────────┼───────────────────────────────┐
       │                               │                               │
       ▼                               ▼                               ▼
┌──────────────┐              ┌──────────────┐              ┌──────────────┐
│ GROUP A      │              │ GROUP B      │              │ GROUP C      │
│ FastAPI      │              │ Django       │              │ React/Next   │
│ Modules      │              │ Apps         │              │ Frontends    │
│              │              │              │              │              │
│ ┌──────────┐ │              │ ┌──────────┐ │              │ ┌──────────┐ │
│ │  Dapr    │ │              │ │  Dapr    │ │              │ │  Dapr    │ │
│ │ Sidecar  │ │              │ │ Sidecar  │ │              │ │  Client  │ │
│ └────┬─────┘ │              │ └────┬─────┘ │              │ └────┬─────┘ │
└──────┼───────┘              └──────┼───────┘              └──────┼───────┘
       │                             │                             │
       │         ┌───────────────────┴──────────┐                  │
       │         │                              │                  │
       ▼         ▼                              ▼                  ▼
┌──────────────────┐                    ┌──────────────────────────────┐
│ GROUP D          │                    │ Shared Infrastructure         │
│ MCP Gateway      │                    │ - PostgreSQL (18 schemas)    │
│ (Python MCP)     │                    │ - Redis (16 databases)       │
│ ┌──────────┐     │                    │ - Elasticsearch (5 indices)  │
│ │  Dapr    │     │                    └──────────────────────────────┘
│ │ Sidecar  │     │
│ └──────────┘     │
└──────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  PER-MODULE STATE MANAGEMENT (Dapr State Store)                             │
└─────────────────────────────────────────────────────────────────────────────┘

  Dispatch Module                     Dapr State API              PostgreSQL
  ┌─────────────┐                    ┌──────────────┐           ┌────────────┐
  │ incident =  │                    │ Dapr Sidecar │           │ dispatch   │
  │  Incident() │ ──save_state()──►  │              │ ─────────►│  schema    │
  │             │                    │ Component:   │           │            │
  │             │ ◄─get_state()────  │ dispatch-    │ ◄─────────│ Only this  │
  │             │                    │   state      │           │ schema     │
  └─────────────┘                    └──────────────┘           └────────────┘
                                           │
                                           │ Enforces boundary:
                                           │ - connectionString with search_path
                                           │ - Cannot access other schemas
                                           ▼
  Mealie Module                      Dapr State API              PostgreSQL
  ┌─────────────┐                    ┌──────────────┐           ┌────────────┐
  │ recipe =    │                    │ Dapr Sidecar │           │  mealie    │
  │  Recipe()   │ ──save_state()──►  │              │ ─────────►│  schema    │
  │             │                    │ Component:   │           │            │
  │             │ ◄─get_state()────  │ mealie-      │ ◄─────────│ Only this  │
  │             │                    │   state      │           │ schema     │
  └─────────────┘                    └──────────────┘           └────────────┘

       Event Flow Example (DDD-Compliant):
       1. Security Alert detected (Nemesis module - GROUP A)
          ├─ Nemesis saves alert via Dapr state API (nemesis schema only)
          └─ Publishes "security.alert.created" event to Dapr Pub/Sub
       
       2. Dispatch module (GROUP A) subscribes to "security.alert.created"
          ├─ Receives event via Dapr Pub/Sub
          ├─ Creates incident via Dapr state API (dispatch schema only)
          └─ Publishes "incident.created" event
       
       3. Ghostwriter app (GROUP B) subscribes to "incident.created"
          ├─ Receives event via Dapr Pub/Sub
          ├─ Creates report via Django ORM (ghostwriter schema only)
          └─ Publishes "report.created" event
       
       4. Jane UI (GROUP C) subscribes to "incident.created"
          └─ Updates dashboard via WebSocket
       
       5. n8n MCP (GROUP D) subscribes to "security.alert.created"
          └─ Triggers automation workflow

       Key DDD Principles Enforced:
       ✅ Bounded Contexts: Each module owns its data (via schema isolation)
       ✅ No Direct DB Access: Modules use Dapr State API (abstraction layer)
       ✅ Event-Driven: Modules communicate via Pub/Sub (loose coupling)
       ✅ Database Agnostic: Can swap PostgreSQL → CosmosDB without code changes
       ✅ Schema Boundaries: Dapr components enforce search_path restrictions
```

---

## Frontend UI Migration Strategy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    COMPREHENSIVE FRONTEND CONSOLIDATION                     │
│                         (21+ Applications → 1 Unified UI)                   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  1. AUTHENTICATION & AUTHORIZATION CONSOLIDATION                            │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  Single Sign-On (SSO) Strategy:                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  Current State: 21+ Different Auth Systems                           │  │
│  │  ├─ n8n: Built-in user management + JWT                               │  │
│  │  ├─ Actual Budget: Local authentication                               │  │
│  │  ├─ Nemesis: Session-based auth                                      │  │
│  │  ├─ MISP: PHP session management                                      │  │
│  │  ├─ Ghostwriter: Django authentication                               │  │
│  │  └─ 16+ other individual auth systems                                │  │
│  │                                                                       │  │
│  │  Unified Solution:                                                    │  │
│  │  ┌─────────────────────────────────────────────────────────────┐   │  │
│  │  │  Jane UI Authentication Layer                                │   │  │
│  │  │  • Next.js middleware for route protection                  │   │  │
│  │  │  • JWT token management (NextAuth.js)                      │   │  │
│  │  │  • Role-Based Access Control (RBAC):                       │   │  │
│  │  │    - Security Admin: Full security domain access            │   │  │
│  │  │    - Analyst: Read-only security tools                     │   │  │
│  │  │    - Developer: AI domain + productivity tools             │   │  │
│  │  │    - User: Limited productivity access                     │   │  │
│  │  │  • Session synchronization across domains                  │   │  │
│  │  └─────────────────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  2. DATA MIGRATION & STATE SYNCHRONIZATION                                  │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  User Preferences Migration:                                                 │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  Source Systems:                                                      │  │
│  │  ├─ n8n: User settings (workflows, credentials)                        │  │
│  │  ├─ Actual: Budget preferences, categories                           │  │
│  │  ├─ Nemesis: Analysis preferences, filters                           │  │
│  │  ├─ CyberChef: Recipe bookmarks, favorites                           │  │
│  │  └─ 17+ other preference systems                                     │  │
│  │                                                                       │  │
│  │  Unified Preferences Store:                                          │  │
│  │  ┌─────────────────────────────────────────────────────────────┐   │  │
│  │  │  PostgreSQL Schema: user_preferences                        │   │  │
│  │  │  ┌─────────────────────────────────────────────────────┐   │   │  │
│  │  │  │ user_id | domain    | component | key     | value   │   │   │  │
│  │  │  │ 123     | security  | nemesis   | theme   | dark    │   │   │  │
│  │  │  │ 123     | ai        | goose     | model   | gpt-4   │   │   │  │
│  │  │  │ 123     | prod.     | actual    | currency| USD     │   │   │  │
│  │  │  └─────────────────────────────────────────────────────────┘   │   │  │
│  │  │  • Real-time sync via WebSockets                          │   │  │
│  │  │  • Local storage fallback for offline mode                │   │  │
│  │  │  • Migration tools for existing preferences               │   │  │
│  │  └─────────────────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  3. TESTING STRATEGY AT SCALE                                               │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  Multi-Application Testing Framework:                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  Cross-Domain Integration Tests:                                      │  │
│  │  ├─ Security → Productivity: Incident creation → n8n workflow        │  │
│  │  ├─ AI → Security: Goose analysis → Nemesis threat detection          │  │
│  │  └─ TCG → Productivity: Card analysis → Budget tracking               │  │
│  │                                                                       │  │
│  │  Visual Regression Testing:                                           │  │
│  │  ├─ Playwright screenshots for all 21+ application UIs                │  │
│  │  ├─ Percy.io integration for visual diff detection                    │  │
│  │  └─ Mobile responsive testing across domains                          │  │
│  │                                                                       │  │
│  │  Performance Testing:                                                 │  │
│  │  ├─ <75ms UI response time validation (ADHD accommodation)           │  │
│  │  ├─ Lighthouse CI for Core Web Vitals                                │  │
│  │  ├─ Load testing: 100+ concurrent users across domains               │  │
│  │  └─ Memory leak detection for long-running sessions                  │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  4. SEARCH & NAVIGATION UNIFICATION                                         │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  Global Search Implementation:                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  Unified Search Index (Elasticsearch):                               │  │
│  │  ┌─────────────────────────────────────────────────────────────┐   │  │
│  │  │  jane-search-*                                              │   │  │
│  │  │  ├─ security-incidents  (Dispatch, Nemesis data)           │   │  │
│  │  │  ├─ productivity-items  (n8n workflows, Actual transactions)│   │  │
│  │  │  ├─ ai-conversations   (Goose chat history)                │   │  │
│  │  │  ├─ tcg-cards         (MTG card database)                  │   │  │
│  │  │  └─ documentation     (All tool docs, help content)        │   │  │
│  │  └─────────────────────────────────────────────────────────────┘   │  │
│  │                                                                       │  │
│  │  Command Palette (Cmd/Ctrl+K):                                       │  │
│  │  ├─ "Create incident" → /security/dispatch/incidents/new             │  │
│  │  ├─ "Run n8n workflow" → /productivity/n8n/workflows                 │  │
│  │  ├─ "Analyze with Goose" → /ai/goose/analyze                         │  │
│  │  └─ "MTG card lookup" → /tcg/commander-spellbook/search              │  │
│  │                                                                       │  │
│  │  Breadcrumb Navigation:                                               │  │
│  │  Jane UI → Security → Nemesis → File Analysis → Report #1234        │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  5. ASSET & RESOURCE MANAGEMENT                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  Asset Consolidation Strategy:                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  Font Standardization:                                                │  │
│  │  ├─ Primary: Inter (system UI, readability for ADHD)                 │  │
│  │  ├─ Code: JetBrains Mono (CyberChef, code analysis)                  │  │
│  │  ├─ Data: Roboto Mono (tables, numbers in Actual)                    │  │
│  │  └─ Fallback: System fonts (performance, offline)                    │  │
│  │                                                                       │  │
│  │  Icon Library Unification:                                           │  │
│  │  ├─ Heroicons: Primary UI icons (consistent with Tailwind)           │  │
│  │  ├─ Lucide React: Secondary icons (lightweight)                      │  │
│  │  ├─ Custom SVGs: Tool-specific icons (security, MTG symbols)         │  │
│  │  └─ Domain-specific: Preserved for specialized tools                 │  │
│  │                                                                       │  │
│  │  Large File Handling:                                                │  │
│  │  ├─ CyberChef operations: Client-side processing (Web Workers)       │  │
│  │  ├─ Security logs: Streaming via WebSockets                          │  │
│  │  ├─ File uploads: Chunked upload with progress indicators             │  │
│  │  └─ CDN integration: Static assets served from edge                  │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  6. REAL-TIME FEATURES CONSOLIDATION                                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  WebSocket Management:                                                       │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  Unified WebSocket Gateway (Socket.io):                              │  │
│  │  ┌─────────────────────────────────────────────────────────────┐   │  │
│  │  │  Connection Namespaces:                                      │   │  │
│  │  │  ├─ /security   - Real-time threat alerts, incident updates │   │  │
│  │  │  ├─ /ai         - Goose conversation streams, model status  │   │  │
│  │  │  ├─ /productivity - n8n workflow execution, Actual syncing  │   │  │
│  │  │  └─ /notifications - System-wide alerts, user messages      │   │  │
│  │  └─────────────────────────────────────────────────────────────┘   │  │
│  │                                                                       │  │
│  │  Notification System:                                                 │  │
│  │  ├─ Toast notifications: Non-intrusive, auto-dismiss                 │  │
│  │  ├─ Desktop notifications: Critical security alerts                  │  │
│  │  ├─ In-app badges: Unread counts per domain                          │  │
│  │  └─ Email fallback: For offline users                                │  │
│  │                                                                       │  │
│  │  Background Task Management:                                          │  │
│  │  ├─ Service Workers: Offline capability, background sync             │  │
│  │  ├─ Web Workers: Heavy computations (CyberChef operations)           │  │
│  │  └─ Task queues: Long-running operations with progress tracking      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  7. ACCESSIBILITY & INTERNATIONALIZATION                                    │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  WCAG 2.1 AA Compliance:                                                    │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  Executive Function Accommodations (ADHD-friendly):                  │  │
│  │  ├─ Enhanced focus indicators (3px outline, high contrast)            │  │
│  │  ├─ Reduced motion options (prefers-reduced-motion)                  │  │
│  │  ├─ Clear visual hierarchy (consistent heading levels)               │  │
│  │  ├─ Timeout extensions (auto-save, session warnings)                 │  │
│  │  └─ Customizable UI density (compact/comfortable/spacious)           │  │
│  │                                                                       │  │
│  │  Keyboard Navigation:                                                 │  │
│  │  ├─ Tab order optimization across all 21+ applications               │  │
│  │  ├─ Skip links for complex interfaces (security dashboards)          │  │
│  │  ├─ Hotkey consistency (Cmd+K search, Esc close modals)              │  │
│  │  └─ Focus management in single-page app navigation                   │  │
│  │                                                                       │  │
│  │  Screen Reader Support:                                               │  │
│  │  ├─ Semantic HTML structure across all domains                       │  │
│  │  ├─ ARIA labels for complex widgets (charts, graphs)                │  │
│  │  ├─ Live regions for dynamic content updates                         │  │
│  │  └─ Alternative text for security diagrams, MTG card images         │  │
│  │                                                                       │  │
│  │  Multi-language Support:                                             │  │
│  │  ├─ i18next integration with namespace per domain                    │  │
│  │  ├─ RTL language support (Arabic, Hebrew)                           │  │
│  │  ├─ Number/date localization (currency in Actual Budget)            │  │
│  │  └─ Dynamic language switching without page reload                   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  8. SECURITY CONSIDERATIONS                                                  │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  Content Security Policy (CSP):                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  Domain-Specific CSP Rules:                                           │  │
│  │  ├─ Security tools: Strict CSP, no inline scripts                     │  │
│  │  ├─ AI domain: Allow LLM API calls, WebSocket connections            │  │
│  │  ├─ Productivity: n8n iframe embedding with sandbox                  │  │
│  │  └─ TCG domain: Allow external card image CDNs                       │  │
│  │                                                                       │  │
│  │  Cross-Origin Resource Sharing (CORS):                               │  │
│  │  ├─ API Gateway: Centralized CORS configuration                      │  │
│  │  ├─ Development: Permissive for localhost                            │  │
│  │  ├─ Production: Strict origin validation                             │  │
│  │  └─ Embedded tools: PostMessage API for secure communication        │  │
│  │                                                                       │  │
│  │  Secure Iframe Embedding:                                            │  │
│  │  ├─ CyberChef: Sandboxed iframe with restricted permissions          │  │
│  │  ├─ n8n workflows: iframe with postMessage communication             │  │
│  │  ├─ Security tools: Read-only embedded dashboards                    │  │
│  │  └─ File viewers: Secure preview with download restrictions          │  │
│  │                                                                       │  │
│  │  Vulnerability Management:                                            │  │
│  │  ├─ Automated dependency scanning (Snyk, GitHub Security)            │  │
│  │  ├─ Regular security audits for consolidated codebase                │  │
│  │  ├─ Input sanitization across all 21+ application interfaces        │  │
│  │  └─ Rate limiting per user, per domain, per API endpoint             │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  9. MONITORING & OBSERVABILITY                                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  Frontend Performance Monitoring:                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  Real User Monitoring (RUM):                                          │  │
│  │  ├─ Core Web Vitals tracking per domain                               │  │
│  │  ├─ User interaction metrics (click-to-response times)                │  │
│  │  ├─ Error boundary reporting with domain context                      │  │
│  │  └─ Performance budget alerts (<75ms target)                          │  │
│  │                                                                       │  │
│  │  User Analytics:                                                      │  │
│  │  ├─ Domain usage patterns (most/least used tools)                    │  │
│  │  ├─ Cross-domain workflow analysis                                    │  │
│  │  ├─ Feature adoption tracking                                         │  │
│  │  └─ User journey mapping across 37 consolidated tools                │  │
│  │                                                                       │  │
│  │  Resource Utilization:                                                │  │
│  │  ├─ Memory usage monitoring (prevent leaks in long sessions)         │  │
│  │  ├─ Bundle size tracking per domain                                   │  │
│  │  ├─ Asset loading performance                                         │  │
│  │  └─ WebSocket connection health monitoring                            │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  10. DEPLOYMENT & ROLLBACK STRATEGY                                         │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  Feature Flagging System:                                                   │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  Gradual Domain Rollout:                                              │  │
│  │  ├─ Phase 1: TCG domain (lowest risk, 2 applications)                │  │
│  │  ├─ Phase 2: AI domain (4 applications, controlled user base)         │  │
│  │  ├─ Phase 3: Productivity domain (6 applications, power users)        │  │
│  │  └─ Phase 4: Security domain (7 applications, critical workflows)    │  │
│  │                                                                       │  │
│  │  Per-User Feature Flags:                                              │  │
│  │  ├─ Beta users: Access to consolidated UI early                      │  │
│  │  ├─ Domain experts: Gradual migration with feedback                   │  │
│  │  ├─ Production users: Stable consolidated experience                  │  │
│  │  └─ Emergency fallback: Revert to individual applications            │  │
│  │                                                                       │  │
│  │  Blue-Green Deployment:                                               │  │
│  │  ├─ Blue environment: Current individual applications                 │  │
│  │  ├─ Green environment: Consolidated jane-ui-platform                 │  │
│  │  ├─ Traffic routing: Gradual shift via load balancer                 │  │
│  │  └─ Instant rollback: DNS switch back to blue environment            │  │
│  │                                                                       │  │
│  │  Critical Application Rollback:                                       │  │
│  │  ├─ Security tools: <30 second rollback SLA                          │  │
│  │  ├─ Productivity tools: <5 minute rollback SLA                       │  │
│  │  ├─ AI tools: <10 minute rollback SLA                                │  │
│  │  └─ Automated health checks trigger emergency rollback               │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## Summary: Consolidation Metrics

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          BEFORE CONSOLIDATION                               │
├─────────────────────────────────────────────────────────────────────────────┤
│  37 Separate Services                                                       │
│  30 Database Instances                                                      │
│  37 Docker Containers                                                       │
│  37 CI/CD Pipelines                                                         │
│  37 Monitoring Setups                                                       │
│  37 Backup Strategies                                                       │
└─────────────────────────────────────────────────────────────────────────────┘

                                    │
                                    │ CONSOLIDATION
                                    ▼

┌─────────────────────────────────────────────────────────────────────────────┐
│                          AFTER CONSOLIDATION                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  DEPLOYMENT ARCHITECTURE:                                                   │
│  ├─ 6 Modular Monoliths (internal module boundaries)                        │
│  │   ├─ jane-platform (8 FastAPI modules with Dapr sidecars)                │
│  │   ├─ jane-django-platform (3 Django apps with schema routing)            │
│  │   ├─ jane-ui-platform (5 React apps with shared components)              │
│  │   ├─ jane-mcp-gateway (5 MCP servers)                                    │
│  │   └─ 2 additional consolidated platforms                                 │
│  └─ 9 Specialized Services (performance/ecosystem requirements)             │
│                                                                              │
│  INFRASTRUCTURE:                                                             │
│   5 Database Instances (83% reduction)                                      │
│  15 Docker Containers (59% reduction)                                       │
│   8 CI/CD Pipelines (78% reduction - shared across domains)                │
│   1 Unified Monitoring Stack (97% reduction)                                │
│   1 Backup Strategy (97% reduction)                                         │
│                                                                              │
│  DDD COMPLIANCE:                                                             │
│  ✅ Bounded Contexts: Enforced via Dapr state components + schema isolation │
│  ✅ Data Ownership: Each module exclusively owns its schema                 │
│  ✅ Loose Coupling: Inter-module communication via Dapr Pub/Sub only        │
│  ✅ Database Abstraction: Dapr State API (swappable backends)               │
│  ✅ Technology Agnostic: Same patterns work across Python/Django/Node.js    │
│                                                                              │
│  OPERATIONAL BENEFITS:                                                      │
│  ✅ Infrastructure: 60-70% reduction                                        │
│  ✅ Maintenance Overhead: 75% reduction                                     │
│  ✅ Cognitive Load: 60% reduction (fewer deployment units)                  │
│  ✅ Development Velocity: 2-3x faster (shared libraries + patterns)         │
│  ✅ Data Consistency: Guaranteed by DDD boundaries + Dapr transactions      │
│  ✅ Cloud Portability: Dapr enables multi-cloud without code changes        │
│                                                                              │
│  FRONTEND-SPECIFIC BENEFITS:                                                │
│  ✅ User Experience: Single interface for all 37 tools (<75ms response)     │
│  ✅ Authentication: Unified SSO eliminates 21+ separate login systems       │
│  ✅ Navigation: Global search + command palette across all domains          │
│  ✅ Accessibility: WCAG 2.1 AA + executive function accommodations          │
│  ✅ Real-time Features: Consolidated WebSocket management + notifications    │
│  ✅ Asset Optimization: 80% reduction in duplicate fonts, icons, styles     │
│  ✅ Testing Efficiency: Single test suite vs. 21+ individual test setups    │
│  ✅ Security Posture: Unified CSP, CORS, and vulnerability management       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Physical Deployment: 2-Server Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     NETWORK TOPOLOGY (Home Lab)                             │
└─────────────────────────────────────────────────────────────────────────────┘

                         ┌─────────────────────┐
                         │   Home Network      │
                         │   (10.0.0.0/24)     │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
       ┌────────────────────────┐      ┌────────────────────────┐
       │    NUC (Frontend)      │      │  AMD Server (Backend)  │
       │    10.0.0.10           │◄────►│  10.0.0.20             │
       │    Intel NUC           │      │  AMD Ryzen/Threadripper│
       └────────────────────────┘      └────────────────────────┘
              │                                   │
              │ User Access                       │ Heavy Compute
              ▼                                   ▼
       Browser (localhost)              LLM Inference + DB


┌─────────────────────────────────────────────────────────────────────────────┐
│                    SERVER 1: NUC (Frontend/Edge Server)                     │
│                    IP: 10.0.0.10  |  Role: User-Facing Services             │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  Docker Containers (6 total)                                                │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  [1] jane-ui-platform (Next.js 15.5.2 - Consolidated)   PORT: 3000        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  • ALL 21+ UI applications consolidated into App Router domains       │  │
│  │  • /security/* - Nemesis, CyberChef, Dispatch, etc. (7 apps)         │  │
│  │  • /productivity/* - Actual, n8n, Mealie, Inspector, etc. (6 apps)   │  │
│  │  • /ai/* - Goose, Docs, Firecrawl, Monitoring (4 apps)              │  │
│  │  • /tcg/* - Commander Spellbook, Client tools (2 apps)               │  │
│  │  • Unified auth, navigation, search, real-time features              │  │
│  │  • <75ms response times with executive function accommodations        │  │
│  │  • Resource: 3GB RAM, 3 CPU cores (increased for consolidated load)  │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  [2] Kong API Gateway                                    PORT: 8080        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  • Reverse proxy for all services                                    │  │
│  │  • Rate limiting, auth, SSL termination                              │  │
│  │  • Routes:                                                            │  │
│  │    /api/v1/*      → 10.0.0.20:8000 (jane-platform)                   │  │
│  │    /api/django/*  → 10.0.0.20:8001 (jane-django-platform)            │  │
│  │    /mcp/*         → 10.0.0.20:8002 (jane-mcp-gateway)                │  │
│  │  • Resource: 1GB RAM, 1 CPU core                                     │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  [3] CyberChef (Static Site)                             PORT: 3001        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  • Pure client-side JavaScript                                       │  │
│  │  • No backend dependencies                                           │  │
│  │  • Nginx serving static files                                        │  │
│  │  • Resource: 256MB RAM, 0.5 CPU cores                                │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  [4] IT-Tools (Static Site)                              PORT: 3002        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  • Vue.js browser-based utilities                                    │  │
│  │  • No backend dependencies                                           │  │
│  │  • Resource: 256MB RAM, 0.5 CPU cores                                │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  [5] Actual Budget (Local SQLite)                        PORT: 5006        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  • Local-first financial app                                         │  │
│  │  • SQLite: ~/actual-data/budget.db                                   │  │
│  │  • Optional sync to AMD server                                       │  │
│  │  • Resource: 512MB RAM, 1 CPU core                                   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  [6] Goose (AI Agent - Local SQLite)                     PORT: 3003        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  • Rust-based AI agent                                               │  │
│  │  • SQLite: ~/.config/goose/sessions.db                               │  │
│  │  • LLM calls → 10.0.0.20:8003 (vLLM server on AMD)                   │  │
│  │  • Resource: 1GB RAM, 2 CPU cores                                    │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
├────────────────────────────────────────────────────────────────────────────┤
│  Total Resources: 5GB RAM, 7 CPU cores                                     │
│  Recommended Hardware: Intel NUC 11/12/13 with 16GB RAM, 4-core CPU        │
└────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                 SERVER 2: AMD (Backend/LLM/Database Server)                 │
│                 IP: 10.0.0.20  |  Role: Heavy Compute + Data               │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  Docker Containers (9 total)                                                │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  [1] jane-platform (FastAPI Modular Monolith)            PORT: 8000        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  • 8 Internal Modules: Dispatch, HexStrike, Mealie, MTG, Nemesis...  │  │
│  │  • Dapr Sidecar (localhost:3500)                                     │  │
│  │  • PostgreSQL connection via Dapr State API                          │  │
│  │  • Resource: 4GB RAM, 4 CPU cores                                    │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  [2] jane-django-platform (Django Modular Monolith)      PORT: 8001        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  • 3 Django Apps: Commander Spellbook, Ghostwriter, Nemesis          │  │
│  │  • DATABASE_ROUTERS for schema isolation                             │  │
│  │  • PostgreSQL connection via Django ORM                              │  │
│  │  • Resource: 3GB RAM, 3 CPU cores                                    │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  [3] jane-mcp-gateway (Python MCP Servers)               PORT: 8002        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  • 5 MCP Servers: Chroma, FileScope, MalwareBazaar, VirusTotal, n8n │  │
│  │  • Shared MCP protocol implementation                                │  │
│  │  • Resource: 2GB RAM, 2 CPU cores                                    │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  [4] vLLM Server (LLM Inference)                         PORT: 8003        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  • Multiple models loaded:                                           │  │
│  │    - cyber-llm (security domain)                                     │  │
│  │    - mtg-llm (Magic: The Gathering domain)                           │  │
│  │    - code-llm (development tools)                                    │  │
│  │  • GPU acceleration (NVIDIA/AMD ROCm)                                │  │
│  │  • Resource: 24GB VRAM, 8GB RAM, 8 CPU cores                         │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  [5] PostgreSQL (Consolidated Database)                  PORT: 5432        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  • 18 schemas (dispatch, hexstrike, mealie, etc.)                    │  │
│  │  • PgBouncer connection pooling                                      │  │
│  │  • Daily backups + WAL archiving                                     │  │
│  │  • Resource: 8GB RAM, 4 CPU cores                                    │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  [6] Redis (Consolidated Cache)                          PORT: 6379        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  • 16 logical databases (DB 0-15)                                    │  │
│  │  • AOF persistence enabled                                           │  │
│  │  • Resource: 8GB RAM, 2 CPU cores                                    │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  [7] Elasticsearch (Search + Analytics)                  PORT: 9200        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  • Indices: dispatch-*, nemesis-*, helk-*, securityonion-*, misp-*   │  │
│  │  • Single-node cluster (dev) or 3-node (prod)                        │  │
│  │  • Resource: 8GB RAM (4GB heap), 4 CPU cores                         │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  [8] RabbitMQ (Dapr Pub/Sub Backend)                     PORT: 5672        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  • Message broker for Dapr pub/sub                                   │  │
│  │  • Event-driven communication between modules                        │  │
│  │  • Management UI: http://10.0.0.20:15672                             │  │
│  │  • Resource: 2GB RAM, 2 CPU cores                                    │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  [9] Chroma DB (Vector Database)                         PORT: 8004        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  • Vector embeddings for HexStrike + MTG Toolkit                     │  │
│  │  • Semantic search capabilities                                      │  │
│  │  • Resource: 4GB RAM, 2 CPU cores                                    │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
├────────────────────────────────────────────────────────────────────────────┤
│  Total Resources: 63GB RAM, 31 CPU cores, 24GB VRAM (GPU)                  │
│  Recommended Hardware: AMD Ryzen 9/Threadripper, 64GB+ RAM, RTX 4090/A6000│
└────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                         NETWORK TRAFFIC FLOW                                │
└─────────────────────────────────────────────────────────────────────────────┘

  User Browser                 NUC (10.0.0.10)              AMD Server (10.0.0.20)
  ─────────────                ───────────────              ───────────────────────
       │
       │ http://nuc.local:3000
       ▼
  ┌─────────────┐
  │  jane-ui    │
  │ (Next.js)   │
  └──────┬──────┘
         │
         │ GET /api/v1/incidents
         ▼
  ┌─────────────┐              ┌─────────────────────┐
  │    Kong     │──────────────►│  jane-platform      │
  │  Gateway    │ Proxy to     │  (FastAPI)          │
  └─────────────┘ 10.0.0.20:8000│  PORT: 8000         │
                                 └──────┬──────────────┘
                                        │ Dapr State API
                                        ▼
                                 ┌─────────────────────┐
                                 │  PostgreSQL         │
                                 │  (dispatch schema)  │
                                 └─────────────────────┘

  ─────────────────────────────────────────────────────────────────────────────

  Goose (NUC)                                   vLLM Server (AMD)
  ───────────                                   ─────────────────
       │
       │ POST /v1/completions
       │ {"prompt": "Analyze this code..."}
       ▼
  ┌─────────────┐              ┌─────────────────────┐
  │ Goose Agent │──────────────►│  vLLM Server        │
  │ (Rust)      │ 10.0.0.20:8003│  PORT: 8003         │
  └─────────────┘               │  Model: code-llm    │
                                └──────┬──────────────┘
                                       │ GPU Inference
                                       ▼
                                ┌─────────────────────┐
                                │ NVIDIA RTX 3090     │
                                │ 24GB VRAM           │
                                └─────────────────────┘

  ─────────────────────────────────────────────────────────────────────────────

  Event-Driven Flow (Cross-Module)
  ─────────────────────────────────
       Nemesis Module                          Dispatch Module
       ──────────────                          ───────────────
            │
            │ Publish "security.alert.created"
            ▼
       ┌─────────────┐
       │  RabbitMQ   │
       │  (AMD)      │
       └──────┬──────┘
              │ Subscribe "security.alert.created"
              ▼
       ┌─────────────┐
       │  Dispatch   │
       │  Module     │
       └─────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                       DEPLOYMENT CONFIGURATION                              │
└─────────────────────────────────────────────────────────────────────────────┘

docker-compose.nuc.yml (Frontend Server)
─────────────────────────────────────────
services:
  jane-ui:
    image: jane-ui-platform:latest
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://10.0.0.20:8080
      - NEXT_PUBLIC_WS_URL=ws://10.0.0.20:8080

  kong:
    image: kong:latest
    ports:
      - "8080:8000"
    environment:
      - KONG_DATABASE=off
      - KONG_DECLARATIVE_CONFIG=/usr/local/kong/kong.yml
      - KONG_PROXY_ACCESS_LOG=/dev/stdout
      - KONG_ADMIN_ACCESS_LOG=/dev/stdout
    volumes:
      - ./kong.yml:/usr/local/kong/kong.yml

  cyberchef:
    image: mpepping/cyberchef:latest
    ports:
      - "3001:8080"

  it-tools:
    image: corentinth/it-tools:latest
    ports:
      - "3002:80"

  actual-budget:
    image: actualbudget/actual-server:latest
    ports:
      - "5006:5006"
    volumes:
      - ./actual-data:/data

  goose:
    image: block/goose:latest
    ports:
      - "3003:3003"
    environment:
      - GOOSE_LLM_URL=http://10.0.0.20:8003
    volumes:
      - ./goose-data:/root/.config/goose

docker-compose.amd.yml (Backend/LLM Server)
───────────────────────────────────────────
services:
  jane-platform:
    image: jane-platform:latest
    ports:
      - "8000:8000"
    environment:
      - DAPR_HTTP_PORT=3500
      - DATABASE_URL=postgresql://user:pass@postgres:5432/jane
    depends_on:
      - postgres
      - redis
      - rabbitmq

  jane-django:
    image: jane-django-platform:latest
    ports:
      - "8001:8001"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/jane
    depends_on:
      - postgres

  jane-mcp:
    image: jane-mcp-gateway:latest
    ports:
      - "8002:8002"

  vllm:
    image: vllm/vllm-openai:latest
    ports:
      - "8003:8000"
    environment:
      - VLLM_MODEL=codellama/CodeLlama-34b-Instruct-hf
    runtime: nvidia
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  postgres:
    image: postgres:15
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_PASSWORD=securepass
    volumes:
      - postgres-data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data

  elasticsearch:
    image: elasticsearch:8.11.0
    ports:
      - "9200:9200"
    environment:
      - discovery.type=single-node
      - ES_JAVA_OPTS=-Xms4g -Xmx4g
    volumes:
      - elastic-data:/usr/share/elasticsearch/data

  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"

  chroma:
    image: chromadb/chroma:latest
    ports:
      - "8004:8000"
    volumes:
      - chroma-data:/chroma/chroma

volumes:
  postgres-data:
  redis-data:
  elastic-data:
  chroma-data:


┌─────────────────────────────────────────────────────────────────────────────┐
│                         FAILOVER & SCALING NOTES                            │
└─────────────────────────────────────────────────────────────────────────────┘

Failover Strategy:
  • If AMD server down → NUC shows cached data + offline mode
  • If NUC down → Access AMD server directly via http://10.0.0.20:8000
  • Database backups on both servers (rsync every 4 hours)

Horizontal Scaling (Future):
  • Add second AMD server for LLM load balancing (10.0.0.21)
  • PostgreSQL read replicas for high-traffic domains
  • Redis Sentinel for HA caching

Monitoring:
  • Prometheus on AMD server collecting metrics from both servers
  • Grafana dashboards accessible via http://10.0.0.20:3000
  • Alerting via ntfy.sh for critical failures
```

