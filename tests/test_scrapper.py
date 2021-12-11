import pytest
import os
from pca_renewables import CAMMESAScraper, SMNScraper
from datetime import date

def test_cammesa_scrapper():
    cammesa_scraper = CAMMESAScraper()
    fecha = date.fromisoformat("2021-12-10")
    assert cammesa_scraper.avalaible_date(fecha)

    cammesa_scraper.download_by_date(fecha)
    cammesa_scraper.shutdown()
    download_folder = os.path.expanduser("~")+"\\Downloads\\"
    assert "EvoluciónTemporal_10122021.csv" in os.listdir(download_folder)

    os.remove(download_folder + "EvoluciónTemporal_10122021.csv")

def test_smn_scrapper():
    smn_scrapper = SMNScraper()
    fecha = date.fromisoformat("2021-05-06")
    smn_scrapper.download_by_date(fecha)
    assert "datohorario20210506.txt" in os.listdir()

    os.remove("datohorario20210506.txt")
