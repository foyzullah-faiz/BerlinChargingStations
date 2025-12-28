# ⚡ Berlin Charging Hub

An advanced software system for discovering, filtering, and managing EV charging stations in Berlin. Built with a **3-Layer Clean Architecture**, this project ensures high maintainability, testability, and scalability.

**Live App:** [https://berlinchargingstation.streamlit.app/](https://berlinchargingstation.streamlit.app/)

---

## 🏛️ Architectural Overview

This project follows **Domain-Driven Design (DDD)** and **Separation of Concerns (SoC)**. By isolating business logic from infrastructure, the system remains "pluggable" and robust.



### The 3-Layer Structure:
1.  **Domain Layer (`src/*/domain`)**: The "Heart" of the app. Contains Entities and Value Objects (e.g., `PostalCode` validation). It has zero dependencies on external libraries.
2.  **Application Layer (`src/*/application`)**: The "Brain." Orchestrates the flow of data between the UI and the Domain models.
3.  **Infrastructure Layer (`src/*/infrastructure`)**: The "Tools." Handles data persistence (CSV reading/writing) and external datasets.

---

## 📂 Project Structure

```text
BerlinChargingStations/
├── src/
│   ├── charging/           # Charging Station Discovery Domain
│   │   ├── application/    # Filtering and Search Services
│   │   ├── domain/         # Station Entities
│   │   └── infrastructure/ # CSV Repositories
│   ├── maintenance/        # Malfunction Reporting Domain
│   │   ├── application/    # Reporting Services
│   │   ├── domain/         # Malfunction Entities
│   │   └── infrastructure/ # Persistence for Reports
│   ├── shared/             # Cross-cutting concerns
│   │   ├── domain/         # Shared Value Objects (PostalCode)
│   │   └── infrastructure/ # Centralized CSV Datasets
│   └── presentation/       # Streamlit UI Layer (app.py)
├── tests/                  # TDD Suite (Pytest)
├── requirements.txt        # Dependency Management
└── README.md               # Project Documentation