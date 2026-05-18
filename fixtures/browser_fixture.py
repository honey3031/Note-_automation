from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.chrome.options import (
    Options
)

from webdriver_manager.chrome import (
    ChromeDriverManager
)

from config.environment import config

from utils.logger import get_logger


logger = get_logger()


def get_driver():

    chrome_options = Options()

    # browser window
    chrome_options.add_argument(
        "--start-window-maximized"
    )

    chrome_options.add_argument(
        "--window-size=1920,1080"
    )

    # stability
    chrome_options.add_argument(
        "--disable-notifications"
    )

    chrome_options.add_argument(
        "--disable-popup-blocking"
    )

    chrome_options.add_argument(
        "--disable-dev-shm-usage"
    )

    chrome_options.add_argument(
        "--no-sandbox"
    )

    chrome_options.add_argument(
        "--disable-gpu"
    )

    chrome_options.add_argument(
        "--disable-extensions"
    )
    chrome_options.add_argument(
        "--disable-logging"
    )

    chrome_options.add_argument(
        "--log-level=3"
    )

    chrome_options.add_experimental_option(
        "excludeSwitches",
        ["enable-logging"]
    )

    chrome_options.add_argument(
        "--disable-infobars"
    )

    chrome_options.add_argument(
        "--disable-blink-features=AutomationControlled"
    )

    # reduce automation flakiness
    chrome_options.page_load_strategy = "eager"

    # headless support
    if config.headless:

        chrome_options.add_argument(
            "--headless=new"
        )

        logger.info(
            "Running in headless mode"
        )

    # remote/grid execution
    if config.execution == "remote":

        driver = webdriver.Remote(
            command_executor=config.grid_url,
            options=chrome_options
        )

        logger.info(
            "Remote Chrome browser launched "
            "using Selenium Grid"
        )

    else:

        driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager().install()
            ),
            options=chrome_options
        )

        logger.info(
            "Local Chrome browser launched"
        )

    # stabilize browser
    driver.implicitly_wait(2)

    # block common ad overlays
    try:

        driver.execute_script("""
            const style = document.createElement('style');

            style.innerHTML = `
                iframe,
                .adsbygoogle,
                [id*='google_ads'],
                [class*='ads'],
                [src*='doubleclick']
                {
                    display: none !important;
                    visibility: hidden !important;
                }
            `;

            document.head.appendChild(style);
        """)

    except Exception:

        logger.warning(
            "Could not inject ad-block style"
        )

    return driver