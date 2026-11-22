# Nirvul360 — Accounting Engine & POS for Bangladeshi E-Commerce

Automated double-entry accounting and operating platform purpose-built for Bangladeshi e-commerce and f-commerce merchants (FastAPI + Next.js 15 + Supabase PostgreSQL).

---

## Project Structure

```text
.
├── .github/workflows/ci.yml     # Automated CI (lint, tests, build)
├── backend/                     # FastAPI backend
│   ├── app/                     # App routers, domain rules, DB services
│   ├── scripts/                 # Migration & backfill scripts
│   ├── tests/                   # 28+ test suites
│   ├── Dockerfile               # Backend container definition
│   ├── pyproject.toml           # Python tool configurations
│   ├── requirements.txt         # Pinned Python dependencies
│   └── run_backend.py           # Backend server runner
├── frontend/                    # Next.js 15 App Router frontend
│   ├── src/                     # React components, POS views, and routes
│   ├── tests/                   # Smoke tests
│   ├── Dockerfile               # Multi-stage production container
│   ├── next.config.ts           # Next.js config with backend API rewrite
│   └── package.json             # Frontend dependencies
├── supabase/                    # Supabase database config
│   ├── migrations/              # Versioned SQL migrations
│   ├── schema.sql               # Base canonical schema
│   └── seed.sql                 # Seed database records
├── docs/                        # Architecture, test, and handover guides
│   ├── developer-handover.md    # System specification
│   ├── developer-handover.pdf   # Reference PDF
│   ├── TEST_INFRA.md            # Test infrastructure details
│   └── WHATSAPP_INTEGRATION_GUIDE.md
├── docker-compose.yml           # Multi-service local orchestrator
├── vercel.json                  # Frontend cloud deployment routing
├── package.json                 # Monorepo root workspace orchestrator
├── .env.example                 # Environment configuration template
├── LICENSE                      # License details
├── SECURITY.md                  # Security vulnerability reporting
└── CONTRIBUTING.md              # Contribution and PR guidelines
```

---

## Quickstart (Local Development)

### 1. Prerequisites
- Python 3.11+
- Node.js 20+
- npm or pnpm

### 2. Environment Setup
Copy the sample environment file and configure variables:
```bash
cp .env.example .env
```

### 3. Running Services

From the root directory:
```bash
# Start backend server (port 8000)
npm run dev:backend

# Start frontend application (port 3000)
npm run dev:frontend
```

Alternatively, run via Docker Compose:
```bash
docker compose up --build
```

---

## Testing & Quality Assurance

Run backend and frontend suites:
```bash
# Run all tests
npm test

# Run backend pytest suite directly
pytest backend/tests/ -v

# Run frontend smoke verification
npm run test:frontend

# Build frontend for production
npm run build:frontend
```

---

## Core Domain Rules

1. **Strict Double-Entry**: Every transaction balances `debit == credit`.
2. **Immutable Price History**: Historical purchase costs are never overwritten.
3. **Multi-Tenant Isolation**: RLS and explicit tenant boundaries across all tables.
4. **Poisha Precision**: Currency values stored as integers (poisha) to avoid floating-point drift.
5. **Accrual-to-Cash Courier Settlements**: Complete reconciliation of COD remittances and courier deduction fees.
