import pytest

import logging

logger = logging.getLogger(__name__)

def pytest_collection_modifyitems(session: pytest.Session, config: pytest.Config, items: list[pytest.Item]):
    for item in items:
        for marker in item.iter_markers(name="description"):
            description = marker.args[0]
            item.user_properties.append(("description", description))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield

    report = outcome.get_result()

    logger.debug("Testing Item Configuration (%s): %s", item.name, vars(item.config))
    logger.debug("Testing Report (%s): %s", item.name, vars(report))

    item.user_properties.append(("identifier", item.nodeid))

    item.user_properties.append(("name", item.name))
    # item.user_properties.append(("description", report.description))



    # function = item.obj
    #
    # docstring = getattr(function, "__doc__")
    # if docstring:
    #     logger.debug("Found Docstring: %s", docstring)
    #     report.nodeid = docstring
