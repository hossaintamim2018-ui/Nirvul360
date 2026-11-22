# Nirvul360 — Developer Handover Specification & Architecture Guide

## 1. Overview & Vision
**Nirvul360** is an automated, double-entry accounting and operating platform purpose-built for Bangladeshi e-commerce and f-commerce merchants. It unifies order management, multi-channel inventory, point-of-sale (POS), courier COD reconciliation, operational expenses, WhatsApp bot automation, and real-time financial reporting (P&L, Balance Sheet, Cash Flow).

---

## 2. Monorepo Layout
The repository follows a clean, production-grade monorepo layout:

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml               # Automated CI pipeline (lint, test, build)
├── backend/
│   ├── app/                     # FastAPI application
│   │   ├── api/                 # REST API routers (orders, products, pos, etc.)
│   │   ├── core/                # Config, database connections, security
│   │   ├── models/              # Pydantic schemas and database models
│   │   └── services/            # Accounting engine, inventory, settlements
│   ├── scripts/                 # One-off scripts (backfills, data migrations)
│   ├── tests/                   # 28+ comprehensive test suites
│   ├── Dockerfile               # Backend container definition
│   ├── pyproject.toml           # Python package & tool configs (pytest, ruff)
│   ├── requirements.txt         # Pinned Python dependencies
│   ├── run_backend.py           # Backend dev entrypoint
│   └── seed.py                  # Database seeder
├── frontend/
│   ├── src/
│   │   ├── app/                 # Next.js 15 App Router pages
│   │   ├── components/          # Reusable UI views and modular tabs
│   │   └── lib/                 # Frontend helpers, types, API clients
│   ├── tests/                   # Frontend smoke & component tests
│   ├── Dockerfile               # Multi-stage production container
│   ├── next.config.ts           # Next.js config with backend proxy rewrite
│   └── package.json             # Frontend package & dependencies
├── supabase/
│   ├── migrations/              # Versioned SQL migrations
│   │   ├── 20261101000000_initial_schema.sql
│   │   └── 20261122000000_add_product_image_url.sql
│   ├── schema.sql               # Base canonical database schema
│   └── seed.sql                 # Reference demo data
├── docs/                        # Architecture, test guides, handover docs
│   ├── developer-handover.md    # This document
│   ├── developer-handover.pdf   # Original handover reference
│   ├── TEST_INFRA.md            # Test infrastructure and mock strategies
│   ├── TEST_READY.md            # Test readiness checklist
│   └── WHATSAPP_INTEGRATION_GUIDE.md
├── docker-compose.yml           # Local multi-service orchestration
├── vercel.json                  # Frontend cloud deployment routing
├── package.json                 # Monorepo root workspace orchestrator
├── .env.example                 # Environment template (NO secrets)
├── .gitignore                   # Ignored directories, envs, build artifacts
├── .dockerignore                # Docker ignore rules
├── LICENSE                      # Project license
├── SECURITY.md                  # Security and vulnerability reporting
├── CONTRIBUTING.md              # Contribution standards and branch conventions
└── README.md                    # Top-level quickstart & documentation
```

---

## 3. Core Accounting Engine Principles (Non-Negotiable)

1. **Strict Double-Entry Balanced Journals**:
   - Every financial transaction must generate equal debit and credit journal entries (`SUM(debit) == SUM(credit)`).
   - Any unbalanced transaction is rejected at the engine level with an exception.

2. **Immutable Historical Records**:
   - Never overwrite or mutate historical purchase costs (`unit_cost`) or landed unit costs upon subsequent stock additions.
   - Adjustments must be posted as offsetting journal entries, never by mutating past records.

3. **Multi-Tenant Isolation**:
   - All database tables enforce `tenant_id` separation.
   - In PostgreSQL / Supabase, Row-Level Security (RLS) policies enforce that requests only access their active tenant.

4. **Accrual-to-Cash Courier Settlements**:
   - When an order is delivered via Courier (Pathao, Steadfast, RedX), revenue is accrued against **Courier Clearing (Asset)**.
   - When courier settlement deposits cash into the merchant's bank/MFS account (bKash, Nagad), the clearing account is credited and bank is debited, explicitly recognizing courier delivery charges and COD percentage fees.

---

## 4. Key Endpoints & Services

- **POS System (`/api/v1/pos`)**:
  - `GET /api/v1/pos/products`: Lists active products with available inventory, retail prices, and `image_url`.
  - `POST /api/v1/pos/checkout`: Generates sale, creates customer ledger entry, posts inventory movement, and records cash/card receipt.

- **Integrations & Scraping (`/api/v1/integrations`)**:
  - `POST /api/v1/integrations/pull-inventory`: Pulls products and images from external web shops (WooCommerce, Shopify, custom websites) using OpenGraph and JSON-LD schema parsing.

- **Courier Settlements (`/api/v1/settlements`)**:
  - `POST /api/v1/settlements/reconcile`: Upload courier statements (Excel/CSV), auto-matches tracking codes, calculates disputed/unsettled amounts.

- **WhatsApp Assistant (`/api/v1/whatsapp`)**:
  - Webhook listener accepting inbound text/audio expense notes in Bengali, English, or Banglish, parsed via regex and OpenAI LLM fallback.

---

## 5. Development & Testing Commands

### Backend
```bash
# Run backend development server
python backend/run_backend.py

# Run all pytest suites
pytest backend/tests/ -v

# Run lint checks
ruff check backend/
```

### Frontend
```bash
# From monorepo root:
npm run dev:frontend
npm run build:frontend
npm test

# Directly inside frontend/:
cd frontend
npm run dev
npm run build
npm test
```

### Docker
```bash
# Start backend and frontend containers
docker compose up --build
```
