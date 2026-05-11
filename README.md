# Notes Automation Framework

## Project Overview

This project is a Hybrid Test Automation Framework developed for the Notes Application using:

* Selenium WebDriver
* Python
* Pytest
* API Testing using Requests
* Page Object Model (POM)
* Docker + Selenium Grid
* Parallel Execution using pytest-xdist
* Jenkins CI/CD Integration
* Allure & HTML Reporting

The framework supports:

* UI Testing
* API Testing
* End-to-End (E2E) Testing
* Parallel Execution
* Remote Selenium Grid Execution
* Retry Mechanism
* Self-Healing Click Logic
* Intelligent Wait Handling

---

# Tech Stack

| Technology           | Purpose               |
| -------------------- | --------------------- |
| Python               | Programming Language  |
| Selenium             | UI Automation         |
| Pytest               | Test Framework        |
| Requests             | API Testing           |
| Docker               | Containerization      |
| Selenium Grid        | Distributed Execution |
| Jenkins              | CI/CD                 |
| Allure               | Reporting             |
| pytest-xdist         | Parallel Execution    |
| pytest-rerunfailures | Auto Retry            |
| webdriver-manager    | Driver Management     |

---

# Framework Structure

```text
notes-automation/
│
├── api/
│   ├── base_api.py
│   ├── auth_api.py
│   └── notes_api.py
│
├── config/
│   ├── config.yaml
│   └── environment.py
│
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   └── notes_page.py
│
├── tests/
│   ├── api/
│   ├── ui/
│   └── e2e/
│
├── utils/
│   ├── logger.py
│   └── helpers.py
│
├── reports/
├── screenshots/
├── allure-results/
├── allure-report/
│
├── conftest.py
├── docker-compose.yml
├── Jenkinsfile
├── pytest.ini
├── requirements.txt
├── README.md
└── .env
```

---

# Features Implemented

## UI Automation

* Login validation
* Invalid login validation
* Logout functionality
* Note creation
* Note editing
* Note deletion
* Form validation

## API Automation

* GET Notes API
* Create Note API
* Update Note API
* Delete Note API
* Unauthorized access validation
* Response validation
* Response time validation

## End-to-End Validation

* UI → API synchronization
* API → UI synchronization
* UI edit reflected in API
* API edit reflected in UI
* UI delete reflected in API
* API delete reflected in UI
* Multiple note synchronization validation

---

# Advanced Framework Features

## Parallel Execution

Implemented using:

```bash
pytest -n 2
```

Parallel execution is implemented using pytest-xdist and supports both local and Selenium Grid execution.
---

## Selenium Grid + Docker

Framework supports remote execution using Dockerized Selenium Grid.

### Start Grid

```bash
docker compose up -d --scale chrome=2
```

### Open Grid Dashboard

```text
http://localhost:4444/ui
```

---

## Intelligent Retry Mechanism

Implemented:

* Retry for stale elements
* Retry for intercepted clicks
* JavaScript fallback click
* Explicit waits

After installing `pytest-rerunfailures`, command-level reruns can be enabled with:

```bash
pytest --reruns 1 --reruns-delay 2
```

---

# Stability & Retry Handling

Framework includes:

* Retry handling for flaky UI interactions
* JavaScript fallback clicks for intercepted elements
* Explicit wait synchronization
* DOM stabilization handling
* Parallel execution stability improvements
---

# Setup Instructions

## 1. Clone Repository

```bash
git clone https://github.com/honey3031/Note--automation.git
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Configuration

Update `.env`

```env
EMAIL=your_email
PASSWORD=your_password
```

---

# Local Execution

## Run All Tests

```bash
pytest -v
```

---

## Run UI Tests

```bash
pytest tests/ui -v
```

---

## Run API Tests

```bash
pytest tests/api -v
```

---

## Run E2E Tests

```bash
pytest tests/e2e -v
```

---

# Parallel Execution

```bash
pytest -n 2 -v
```

---

# Generate HTML Report

```bash
pytest --html=reports/report.html --self-contained-html
```

---

# Generate Allure Report

## Run Tests

```bash
pytest --alluredir=allure-results
```

## Generate Report

```bash
allure serve allure-results
```

---

# Jenkins CI/CD Integration

Implemented Pipeline Stages:

1. Checkout Source Code
2. Start Selenium Grid
3. Install Dependencies
4. Run Parallel Tests
5. Generate Reports
6. Archive Artifacts

---

# Jenkins Pipeline Execution

```bash
Build Now
```

Pipeline includes:

* Parallel execution
* Docker Grid startup
* Allure reporting
* Artifact publishing

---

# Docker Configuration

Framework supports:

* Selenium Hub
* Multiple Chrome Nodes
* Remote WebDriver Execution

---

# Performance Validation

Implemented:

* API response time checks
* UI synchronization validation
* DOM stabilization waits

---

# Reporting

## HTML Report

Generated under:

```text
reports/report.html
```

## Allure Report

Generated under:

```text
allure-report/
```

---

# Capstone Documentation

The Section 1 and advanced-quality deliverables are included under:

```text
docs/manual_test_plan.md
docs/test_scenarios_test_cases_rtm.md
docs/advanced_quality_intelligence.md
```

---

# Total Test Coverage

| Test Type | Count |
| --------- | ----- |
| UI Tests  | 7     |
| API Tests | 8     |
| E2E Tests | 8     |
| Total     | 23    |

---

# Key Achievements

* Hybrid UI + API Automation
* Scalable Hybrid Automation Framework Structure
* Parallel Selenium Execution
* Dockerized Selenium Grid
* Jenkins CI/CD Integration
* Intelligent Retry Framework
* Self-Healing Click Handling
* Advanced Reporting

---

# Author

Honey Talabathula

B.Tech CSE-AIML
QA Automation Framework Project
