# fintech-qe-framework

Fintech Test Automation Framework (Python)

This is a modern and easy-to-use API + UI automation framework built using Python.
It’s designed to feel clean, readable, and scalable — something you can hand over to any team and they can understand it right away.

The goal of this framework is to show how a real-world automation setup should look:
fast API tests, reliable UI tests, clean architecture, and minimal duplication by applying DRY (Don’t Repeat Yourself) principles everywhere.

🌟 What This Framework Does

This framework tests a simple fintech-style system with two core areas:

1. API Testing

It validates:

Creating users

Fetching users

Creating transactions

Listing transactions for a user

Error handling (invalid data, missing fields, etc.)

It uses:

httpx (async) for fast network calls

pydantic models so responses are strongly typed

pytest-asyncio so tests run efficiently and clearly

2. UI Testing

It provides reusable flows for:

Registering a user via the UI

Creating a transaction via the UI

UI tests run on:

Playwright, the most modern browser automation tool

Automatic screenshots when a test fails

Allure-friendly output

Everything is built to be simple, clean, and maintainable.

🧱 Why This Framework Is “Modern”

Here’s what makes the stack up-to-date:

httpx.AsyncClient → better than requests, supports async

pydantic v2 → typed models, automatic validation

pydantic-settings → strong environment configuration

Playwright → stable UI automation with built-in retries

pytest-playwright → no extra boilerplate needed

Allure reports → nice HTML reports with screenshots

Fully DRY architecture → no copy/paste code, all reusable

📂 Project Structure (Simple Overview)
fintech-qe-framework/
├── config/            # All environment settings
├── src/
│   ├── api/           # API routes, client, and reusable services
│   ├── ui/            # UI flows (reusable Playwright steps)
│   └── utils/         # Models, data factories, logger
├── tests/
│   ├── api/           # API test suite
│   └── ui/            # UI test suite
├── reports/           # Allure results (auto-created)
├── logs/              # Test execution logs
├── pyproject.toml     # Dependencies and project metadata
└── README.md          # This file


Everything is placed exactly where you’d expect it.
No surprises. No messy folders.

🧪 Core Concepts (In Plain English)
✔ Centralized API Routes

You never hardcode API paths like /api/users inside tests.
Instead, they live in:

src/api/routes.py


If the backend changes a route tomorrow, you update it once.

✔ Service Layer (Clean Testing Style)

Services wrap real API calls like this:

user = await users_service.create_user(payload)
transactions = await transactions_service.list_for_user(user.id)


Your tests remain readable and focused on behavior, not plumbing.

✔ Test Data Factories

Every test uses clean factory methods:

make_user()
make_transaction(user_id)


This keeps data generation consistent and avoids duplication.

✔ Typed Models (Automatic Schema Validation)

Responses are validated using pydantic:

User.model_validate(resp.json())


If the backend returns wrong fields → test fails immediately.

✔ Playwright UI Flows

Reusable UI steps for:

register_user(page, "John", "john@example.com", "premium")
create_transaction_ui(page, user_id="123", amount=200, ...)


All UI interactions are stored in one place so tests stay tiny and clean.

✔ Screenshots on Failure (Allure Friendly)

If a UI test fails, we capture a screenshot automatically and attach it to reports.

🧰 Prerequisites

Make sure you have:

Python 3.11+

pip up to date

Playwright browsers installed

To install Playwright browsers:

playwright install

⚙️ Setup Instructions

Install all Python dependencies:

pip install -e .


(Optional) Create a .env file:

BASE_URL=http://localhost:8080
UI_URL=http://localhost:3000
AUTH_TOKEN=


This allows you to switch between environments easily.

▶️ Running Tests
Run everything
pytest

Run only API tests
pytest tests/api

Run only UI tests
pytest -m ui

Run with Allure reporting
pytest --alluredir=reports/allure-results
allure serve reports/allure-results


This opens a beautiful dashboard with:

Test run summary

Step-by-step logs

Screenshots

Errors & stack traces

🧠 How DRY Is Applied

The framework avoids duplication by using:

✔ One place for all routes
✔ One reusable API client
✔ One service layer for each feature
✔ One set of data factories
✔ One set of UI flows
✔ Reusable fixtures for user + transaction setup
✔ Parameterized tests instead of multiple test copies

This makes the framework easy to extend, easy to understand, and cheap to maintain.

📈 Extending the Framework

Want to add a new API like /api/loans?

Just:

Add a route → routes.py

Add a model → models.py

Add a service method → services.py

Write clean tests → tests/api/

No boilerplate. No repeated code.

Same for UI — just add new flows and tests.

✔ Final Thoughts

This framework is built to feel:

Realistic

Modern

Clean

Easy to onboard new engineers

Strong enough for enterprise use

flowchart TD

    %% ===============================
    %% SECTION: CONFIG & SETTINGS
    %% ===============================
    A[config/settings.py<br>Environment Config<br>BASE_URL, UI_URL, Tokens]

    %% ===============================
    %% SECTION: TEST RUNNER
    %% ===============================
    Z[pytest<br>pytest-asyncio<br>pytest-playwright]

    %% ===============================
    %% SECTION: API LAYER
    %% ===============================
    subgraph API Layer
        B1[routes.py<br>Central API Paths]
        B2[client.py<br>httpx.AsyncClient<br>Logging + Headers]
        B3[services.py<br>UsersService<br>TransactionsService]
    end

    %% ===============================
    %% SECTION: UTILS
    %% ===============================
    subgraph Utilities
        C1[models.py<br>pydantic Models<br>(User, Transaction)]
        C2[data_factory.py<br>make_user(), make_transaction()]
        C3[logger.py<br>Central Test Logger]
    end

    %% ===============================
    %% SECTION: UI LAYER
    %% ===============================
    subgraph UI Layer
        D1[flows.py<br>Reusable Playwright Flows]
    end

    %% ===============================
    %% SECTION: FIXTURES
    %% ===============================
    subgraph Fixtures (conftest.py)
        E1[event_loop]
        E2[api_client]
        E3[users_service / tx_service]
        E4[user fixture]
        E5[transaction fixture]
        E6[Playwright<br>page/browser]
    end

    %% ===============================
    %% SECTION: TEST SUITES
    %% ===============================
    subgraph Test Suites
        F1[API Tests<br>test_users_api.py<br>test_transactions_api.py]
        F2[Validation Tests<br>parametrized]
        F3[UI Tests<br>test_flows_ui.py]
    end

    %% ===============================
    %% SECTION: REPORTING
    %% ===============================
    G[Reports<br>Allure + Screenshots<br>logs/tests.log]

    %% FLOW CONNECTIONS
    Z --> A
    Z --> B1
    Z --> B2
    Z --> B3
    Z --> D1
    Z --> E1
    Z --> F1
    Z --> F2
    Z --> F3

    A --> B2
    A --> D1

    B1 --> B2
    B2 --> B3
    B3 --> F1
    B3 --> F2

    C1 --> B3
    C2 --> F1
    C2 --> F2
    C2 --> E4

    D1 --> F3

    E2 --> B3
    E4 --> F1
    E5 --> F2
    E6 --> F3

    F1 --> G
    F2 --> G
    F3 --> G
