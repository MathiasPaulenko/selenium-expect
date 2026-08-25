"""Integration test fixtures — real Chrome headless + local HTML page."""

from __future__ import annotations

import threading
from pathlib import Path
from typing import Any

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import selenium_expect._config as cfg_module
from selenium_expect._config import ExpectConfig

# --- HTML test page ---

TEST_PAGE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Test Page</title>
    <style>
        .hidden { display: none; }
        .invisible { visibility: hidden; }
        #main { color: rgb(255, 0, 0); display: block; }
        #box { width: 100px; height: 50px; position: absolute; left: 10px; top: 20px; }
    </style>
</head>
<body>
    <h1 id="title">Hello World</h1>
    <div id="main" class="container active" role="main" aria-label="Main content">
        <p>Some text content</p>
    </div>
    <div id="hidden-div" class="hidden">Hidden text</div>
    <div id="invisible-div" class="invisible">Invisible text</div>
    <div id="box"
        style="width:100px;height:50px;position:absolute;left:10px;top:20px;">Box</div>

    <!-- Buttons -->
    <button id="btn-enabled" type="button">Click Me</button>
    <button id="btn-disabled" type="button" disabled>Disabled Button</button>
    <input type="checkbox" id="checkbox-checked" checked>
    <input type="checkbox" id="checkbox-unchecked">
    <input type="text" id="text-input" value="test value">
    <input type="text" id="empty-input" value="">

    <!-- Select single -->
    <select id="select-single">
        <option value="apple">Apple</option>
        <option value="banana" selected>Banana</option>
        <option value="cherry">Cherry</option>
    </select>

    <!-- Select multiple -->
    <select id="select-multiple" multiple>
        <option value="red">Red</option>
        <option value="green" selected>Green</option>
        <option value="blue" selected>Blue</option>
        <option value="yellow">Yellow</option>
    </select>

    <!-- List of items -->
    <ul id="item-list">
        <li class="item">Item 1</li>
        <li class="item">Item 2</li>
        <li class="item">Item 3</li>
    </ul>

    <!-- Shadow DOM -->
    <div id="shadow-host"></div>

    <!-- Iframe -->
    <iframe id="test-iframe"
        srcdoc="<html><body><p id='iframe-text'>Iframe content</p></body></html>"></iframe>

    <!-- Buttons for alert testing -->
    <button id="alert-btn" onclick="window.alert('Test Alert')">Trigger Alert</button>
    <button id="confirm-btn" onclick="window.confirm('Test Confirm')">Trigger Confirm</button>

    <script>
        // Set up shadow DOM
        var host = document.getElementById('shadow-host');
        var shadow = host.attachShadow({mode: 'open'});
        shadow.innerHTML = '<p id="shadow-text">Shadow content</p>'
            + '<button id="shadow-btn">Shadow Button</button>';

        // Set up localStorage and sessionStorage
        localStorage.setItem('test-key', 'test-value');
        localStorage.setItem('other-key', 'other-value');
        sessionStorage.setItem('session-key', 'session-value');
    </script>
</body>
</html>"""


@pytest.fixture()
def driver() -> Any:
    """Chrome headless WebDriver for integration tests."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,720")

    try:
        drv = webdriver.Chrome(options=options)
    except Exception:
        try:
            drv = webdriver.Chrome(service=Service(), options=options)
        except Exception:
            pytest.skip("Chrome WebDriver not available")

    drv.implicitly_wait(0)
    yield drv
    # Quit in a daemon thread to avoid hanging on teardown
    quit_thread = threading.Thread(target=lambda: drv.quit(), daemon=True)
    quit_thread.start()
    quit_thread.join(timeout=5)


@pytest.fixture()
def test_page(driver: Any) -> Any:
    """Load the local test HTML page and return the driver."""
    html_path = Path(__file__).parent / "test_page.html"
    html_path.write_text(TEST_PAGE_HTML, encoding="utf-8")
    driver.get(f"file:///{html_path.as_posix()}")
    yield driver


@pytest.fixture(autouse=True)
def _reset_config() -> None:
    """Reset global config between tests."""
    original = cfg_module._global_config
    cfg_module._global_config = ExpectConfig()
    yield
    cfg_module._global_config = original


@pytest.fixture(autouse=True)
def _reset_soft_collector() -> None:
    """Reset soft assertion collector between tests."""
    from selenium_expect._soft import SoftAssertionCollector

    SoftAssertionCollector.reset()
    yield
    SoftAssertionCollector.reset()
