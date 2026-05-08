# Advanced Quality Intelligence Notes

## Parallel Execution

The suite supports pytest-xdist:

```bash
pytest -n 2
```

Each pytest worker receives its own WebDriver from `fixtures/browser_fixture.py`, which keeps browser sessions isolated for parallel UI execution.

## CI/CD

`Jenkinsfile` covers checkout, dependency installation, Selenium Grid startup, parallel pytest execution, and report/artifact publishing.

## Agentic Automation Layer

Implemented framework hooks:

- Self-healing click fallback in `pages/base_page.py`.
- Retry handling through `pytest-rerunfailures` and safe element actions.
- Screenshot capture on UI failures in `conftest.py`.
- Allure environment metadata generation in `conftest.py`.
- Performance trend logging in `utils/performance_logger.py`.

## MCP / Locator Intelligence Layer

`utils/locator_intelligence.py` provides a small MCP-friendly utility surface for locator analysis:

- Generate stable selector candidates from `data-testid`.
- Check which locator candidate is currently available in the DOM.
- Return locator improvement suggestions that can be consumed by an LLM or MCP workflow.

The intent is to keep the test runtime deterministic while still providing structured data that an assistant can use for failure analysis and locator improvement.

## Performance Engineering

Implemented checks:

- API response-time threshold for GET /notes in `tests/api/test_notes_api.py`.
- UI DOM readiness threshold in `tests/e2e/test_ui_api_sync.py`.
- Trend output written to `reports/performance_trends.csv`.
