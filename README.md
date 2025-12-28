# ⚡ Berlin Charging Hub

A professional, test-driven geographic dashboard for exploring and managing charging station infrastructure in Berlin. This project demonstrates high-level software engineering principles, including **Clean Architecture**, **Test-Driven Development (TDD)**, and **Cloud Deployment**.

## 🌐 Live Application
**View the live app here:** [https://berlinchargingstation.streamlit.app/](https://berlinchargingstation.streamlit.app/)

---

## 🏗️ Architecture: 3-Layer Pattern
This project follows the **Clean Architecture** (Onion Architecture) pattern to ensure a strict separation of concerns, making the system highly maintainable and scalable.

1.  **Domain Layer**: Contains the "Source of Truth" (Entities and Value Objects). It has no dependencies on other layers.
2.  **Application Layer**: Contains services that orchestrate the business logic (e.g., searching for stations or handling reports).
3.  **Infrastructure Layer**: Handles data persistence (CSV Repositories) and external frameworks.
4.  **Presentation Layer**: Built with Streamlit and PyDeck for interactive user experience.



---

## 🧪 Quality Assurance: TDD Process
The backend of this system was developed using **Test-Driven Development**. 
- **Validation**: Strict ZIP code validation ensuring only 5-digit German codes are processed.
- **Unit Testing**: 8+ automated tests cover station discovery, error handling, and reporting logic.
- **Independence**: The logic is tested entirely separate from the UI, ensuring reliability.

**To run the automated tests locally:**
```bash
python3 -m pytest tests/