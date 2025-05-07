"""
Various fixtures for pytest that help automate and generate report(s).
"""

# https://pytest-with-eric.com/hooks/pytest-hooks/#Example-pytest-sessionstart-and-pytest-sessionfinish-Hooks

import pytest
import logging

logger = logging.getLogger(__name__)

def pytest_configure(config: pytest.Config):
    config.addinivalue_line(
        "markers", "description: Adds a description to the test."
    )

@pytest.hookimpl()
def pytest_sessionstart(session: pytest.Session):
    logger.debug("Starting Testing Session: %s", session.name)

@pytest.hookimpl()
def pytest_sessionfinish(session: pytest.Session, exitstatus: int):
    logger.debug("Completed Testing Session: %s - %d", session.name, exitstatus)

