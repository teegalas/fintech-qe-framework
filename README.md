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
