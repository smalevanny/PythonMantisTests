import json
import os.path

import pytest

from fixture.application import Application

fixture = None
target = None

def load_config(file):
    global target
    if target is None:
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_path) as config_file:
            target = json.load(config_file)
    return target

@pytest.fixture
def app(request):
    global fixture
    browser = request.config.getoption("--browser")
    config = load_config(request.config.getoption("--target"))
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=config["web"]["baseURL"])
    fixture.session.ensure_login(username=config["webadmin"]["username"], password=config["webadmin"]["password"])
    return fixture

@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--target", action="store", default="target.json")




