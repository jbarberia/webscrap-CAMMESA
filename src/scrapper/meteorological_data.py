from urllib.request import urlretrieve
from datetime import date

class SMNScraper():
    URL_HEADER = "https://ssl.smn.gob.ar/dpd/descarga_opendata.php?file=observaciones/"
   
    def __init__(self, download_folder:str = "") -> None:
        self._set_download_folder(download_folder)

    def _set_download_folder(self, folder: str) -> None:
        self.download_folder = folder + "/"

    def download_by_date(self, date: date) -> None:
        filename = "datohorario{}.txt".format(date.isoformat().replace("-", ""))
        url_string = self.URL_HEADER + filename
        print(url_string)
        urlretrieve(url_string, self.download_folder + filename)



d = date.fromisoformat("2021-05-06")
d.strftime("%d/%m/%y")
