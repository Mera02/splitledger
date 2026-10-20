# SplitLedger

SplitLedger is a full-stack expense-sharing application for creating groups, recording shared expenses, calculating member balances, and generating deterministic settlement suggestions.

The project was designed with a strong focus on financial correctness, testability, and separation of concerns.

It exposes the same underlying business logic through:

- a React web interface
- a FastAPI REST API
- a Typer command-line interface

An independent QA automation repository tests SplitLedger externally through the API, CLI, and browser UI.

**QA repository:**  
https://github.com/Mera02/splitledger-qa

---

## Features

SplitLedger currently supports:

- creating expense groups
- adding members to groups
- recording shared expenses
- selecting the payer
- equal expense splitting
- deterministic remainder handling
- viewing expense history
- calculating member balances
- generating suggested settlements
- persistent SQLite storage
- REST API access
- command-line access
- machine-readable CLI JSON output

---

## Technology Stack

### Backend

- Python 3.11
- FastAPI
- SQLite
- Typer
- pytest

### Frontend

- React
- TypeScript
- Vite
- CSS

### Quality and Tooling

- pytest
- FastAPI TestClient
- Git
- GitHub Actions

Independent external QA automation is maintained in the separate `splitledger-qa` repository using:

- httpx
- subprocess
- Playwright
- pytest

---

## Architecture

SplitLedger uses one shared business and service layer rather than duplicating financial logic between interfaces.

```text
React UI
   |
   | HTTP / JSON
   v
FastAPI
   |
   v
Services
   |
   v
Domain Logic
   |
   v
Repositories
   |
   v
SQLite


Typer CLI
   |
   v
Services
   |
   v
Domain Logic
   |
   v
Repositories
   |
   v
SQLite
```

The React application communicates with FastAPI over HTTP.

The CLI uses the same Python services and domain logic directly.

This keeps financial behavior consistent across application interfaces.

---

## Project Structure

```text
splitledger/
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── backend/
│   ├── app/
│   │   ├── db/
│   │   │   ├── connection.py
│   │   │   ├── repositories.py
│   │   │   └── schema.py
│   │   │
│   │   ├── domain/
│   │   │   ├── balances.py
│   │   │   ├── money.py
│   │   │   ├── settlements.py
│   │   │   └── splitting.py
│   │   │
│   │   ├── services/
│   │   │   ├── balances.py
│   │   │   ├── expenses.py
│   │   │   ├── groups.py
│   │   │   └── settlements.py
│   │   │
│   │   ├── cli.py
│   │   └── main.py
│   │
│   ├── tests/
│   │   ├── api/
│   │   ├── cli/
│   │   ├── integration/
│   │   └── unit/
│   │
│   └── requirements.txt
│
├── docs/
│   └── business-rules.md
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
│
├── .gitignore
└── README.md
```

---

## Financial Model

SplitLedger stores monetary values as integer cents instead of floating-point numbers.

For example:

```text
100.00 BAM
=
10000 cents
```

This avoids common floating-point precision problems when working with money.

### Equal Split Example

For an expense of:

```text
100.00 BAM
```

shared between three members:

```text
10000 / 3
```

produces:

```text
Member 1: 3334 cents
Member 2: 3333 cents
Member 3: 3333 cents
```

The remainder is assigned deterministically according to ascending member ID.

No cents are created or lost.

---

## Balances

A member balance is calculated as:

```text
balance = total paid - total owed
```

Example:

Faris pays `100.00 BAM` for three members.

Expected balances:

```text
Faris   +66.66 BAM
Ada     -33.33 BAM
Amar    -33.33 BAM
```

A positive balance means the member should receive money.

A negative balance means the member owes money.

An important invariant is:

```text
sum of all balances = 0
```

---

## Settlements

SplitLedger converts balances into deterministic settlement suggestions.

For the previous example:

```text
Ada  -> Faris   33.33 BAM
Amar -> Faris   33.33 BAM
```

Settlement amounts are always positive.

The settlement algorithm processes debtors and creditors deterministically by member ID.

---

## Business Rules

Important rules include:

- currency is BAM
- amounts must be greater than zero
- amounts may contain at most two decimal places
- monetary values are stored as integer cents
- equal splitting is deterministic
- payer must belong to the group
- duplicate member names within the same group are rejected
- expense shares must sum to the original expense
- member balances must sum to zero
- settlements must not create or destroy money

More details are available in:

```text
docs/business-rules.md
```

---

# Running SplitLedger

## 1. Clone the Repository

```bash
git clone https://github.com/Mera02/splitledger.git
cd splitledger
```

---

## 2. Backend Setup

Create a Python virtual environment:

```bash
python -m venv .venv
```

### Windows

```cmd
.venv\Scripts\activate.bat
```

Install backend dependencies:

```cmd
cd backend
python -m pip install -r requirements.txt
```

Start FastAPI:

```cmd
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 3. Frontend Setup

Open another terminal:

```cmd
cd frontend
npm install
npm run dev
```

The React application will be available at:

```text
http://localhost:5173
```

The backend and frontend should run at the same time.

---

# REST API

Examples of available endpoints include:

```text
GET  /api/health

GET  /api/groups
POST /api/groups

GET  /api/groups/{group_id}/members
POST /api/groups/{group_id}/members

GET  /api/groups/{group_id}/expenses
POST /api/groups/{group_id}/expenses

GET  /api/groups/{group_id}/balances
GET  /api/groups/{group_id}/settlements
```

Example expense request:

```json
{
  "payer_member_id": 1,
  "description": "Apartment",
  "amount": "100.00"
}
```

---

# Command-Line Interface

The CLI uses the same service and financial logic as the web application.

Run commands from the `backend` directory.

## List Groups

```cmd
python -m app.cli group-list
```

## Create Group

```cmd
python -m app.cli group-create "Weekend Trip"
```

## Add Member

```cmd
python -m app.cli member-add 1 Faris
```

## List Members

```cmd
python -m app.cli member-list 1
```

## Add Expense

```cmd
python -m app.cli expense-add 1 1 "Apartment" 100.00
```

## List Expenses

```cmd
python -m app.cli expense-list 1
```

## View Balances

```cmd
python -m app.cli balances 1
```

Example:

```text
Faris: +66.66 KM
Ada: -33.33 KM
Amar: -33.33 KM
```

## View Settlements

```cmd
python -m app.cli settlements 1
```

Example:

```text
Ada -> Faris: 33.33 KM
Amar -> Faris: 33.33 KM
```

---

## JSON CLI Output

CLI commands support machine-readable JSON output.

Example:

```cmd
python -m app.cli balances 1 --json
```

Example response:

```json
[
  {
    "member_id": 1,
    "member_name": "Faris",
    "balance_cents": 6666
  },
  {
    "member_id": 2,
    "member_name": "Ada",
    "balance_cents": -3333
  },
  {
    "member_id": 3,
    "member_name": "Amar",
    "balance_cents": -3333
  }
]
```

This output is also useful for independent automated QA testing.

---

# Automated Tests

The application repository contains automated tests covering:

- financial domain logic
- amount validation
- equal splitting
- remainder handling
- balances
- settlements
- repositories
- services
- API workflows
- CLI workflows
- regression scenarios

Run all backend tests:

```cmd
cd backend
python -m pytest
```

Current application test suite:

```text
44 tests passing
```

---

# Independent QA Automation

SplitLedger also has a dedicated independent QA repository:

https://github.com/Mera02/splitledger-qa

The QA project tests SplitLedger externally rather than importing its internal financial implementation.

It currently includes:

- black-box REST API tests using `httpx`
- CLI tests using `subprocess`
- UI end-to-end tests using Playwright
- boundary and negative testing
- business-rule validation
- cross-layer consistency testing
- independent financial test oracles
- exploratory testing documentation
- requirements traceability
- documented test cases

Current independent QA suite:

```text
15 tests passing
```

---

## Cross-Layer Testing

One of the key QA scenarios verifies the same financial state through:

```text
API
CLI
UI
```

Each interface is compared against an independently defined expected result.

For example:

```text
Expense: 100.00 BAM
Members: Faris, Ada, Amar
Payer: Faris
```

Independent expected result:

```text
Faris   +6666 cents
Ada     -3333 cents
Amar    -3333 cents
```

The API, CLI, and UI must each represent that state correctly.

Agreement between interfaces alone is not treated as proof of correctness because different interfaces may depend on the same underlying implementation.

---

# Continuous Integration

GitHub Actions automatically runs on pushes and pull requests to `main`.

The CI workflow verifies:

```text
Backend
✓ install Python dependencies
✓ run automated backend tests

Frontend
✓ install Node dependencies
✓ create production build
```

A failing test or frontend build causes the workflow to fail.

---

# Design Decisions

## Integer Cents

Money is represented with integer cents rather than floating-point values to avoid monetary precision issues.

## Shared Business Logic

The API and CLI use the same service and domain layers.

This avoids duplicating important financial rules.

## Deterministic Behavior

Equal-split remainder handling and settlement ordering are deterministic, making results reproducible and testable.

## SQLite

SQLite keeps the MVP lightweight while still providing real persistent relational storage and transaction support.

## Separate QA Repository

The external QA automation lives in a separate repository so that tests can exercise SplitLedger through its public interfaces without depending on its internal implementation.

---

# Current MVP Scope

Included:

- groups
- members
- shared expenses
- equal splitting
- balances
- settlements
- React UI
- REST API
- CLI
- SQLite persistence
- automated testing
- continuous integration

Not currently included:

- authentication
- multiple currencies
- percentage-based splits
- custom unequal splits
- payment processing
- production deployment

The project intentionally prioritizes correctness, clear architecture, and testability over feature quantity.

---

# Related Repository

Independent QA automation:

**SplitLedger QA**  
https://github.com/Mera02/splitledger-qa