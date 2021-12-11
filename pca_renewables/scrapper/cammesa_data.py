from time import sleep
from msedge.selenium_tools import Edge
from selenium.webdriver.common.keys import Keys
from datetime import date

class CAMMESAScraper():
    WEBDRIVER_PATH = "C:/Users/Barberia Juan Luis/Desktop/Programas/msedgedriver.exe"
    URL_DASHBOARD = "https://cdsrenovables.cammesa.com/renovableschart/#/totalesLineAndPie"

    def __init__(self, download_folder:str=""):
        self.driver = Edge(self.WEBDRIVER_PATH)
        self.driver.get(self.URL_DASHBOARD)
        self._load_web_page_elements()

    def _load_web_page_elements(self):
        self.csv_button = self.driver.find_element_by_id("btnCsv")
        self.date = self.driver.find_element_by_id("dxFecha")
        self.date_selector = self.driver.find_element_by_xpath("//*[@id=\"dxFecha\"]/div[1]/div/input")

    def _cammesa_format_date(self, date:date) -> str:
        return date.strftime("%d/%m/%y")

    def download_by_date(self, date:date):
        if self.avalaible_date(date):
            ValueError("Fecha no disponible")
        self.write_date(date)
        sleep(3)
        self.csv_button.click()
        sleep(10)

    def erase_date(self):
            self.date_selector.click()
            self.date_selector.send_keys(Keys.CONTROL + "a")
            self.date_selector.send_keys(Keys.DELETE)

    def write_date(self, date:date):
            str_date = self._cammesa_format_date(date)
            self.erase_date()
            self.date_selector.click()
            self.date_selector.send_keys(str_date)
            self.date_selector.send_keys(Keys.RETURN)

    def avalaible_date(self, date:date) -> bool:
        self.write_date(date)
        unavalaible = "dx-invalid"
        classes = self.date.get_attribute("class").split(" ")
        return not (unavalaible in classes)

    def shutdown(self) -> None:
        self.driver.quit()
