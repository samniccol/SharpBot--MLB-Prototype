from mlb_injuryscraper_selenium_assist import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# ✅ SET THIS TO WHERE YOU EXTRACTED msedgedriver.exe
EDGEDRIVER_PATH = r"C:\Users\reile\Downloads\edgedriver_win64\msedgedriver.exe"

# ✅ Set up Edge options
edge_options = EdgeOptions()
# edge_options.add_argument("--headless")  # Disable headless for now
 # Comment this out if you want to see the browser open
edge_options.add_argument("--window-size=1920,1080")

# ✅ Launch Edge browser
driver = webdriver.Edge(service=EdgeService(EDGEDRIVER_PATH), options=edge_options)

# ✅ Go to the injury report page
driver.get("https://www.rotowire.com/baseball/injury-report.php")

WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CLASS_NAME, "webix_ss_center_scroll"))
)
driver.save_screenshot("debug_view.png")

