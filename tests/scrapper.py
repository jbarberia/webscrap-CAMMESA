import pytest
import os
from scrapper import CAMMESAScraper, SMNScrapper
from datetime import date

from scrapper.meteorological_data import SMNScraper

def test_cammesa_scrapper():
    cammesa_scraper = CAMMESAScraper()
    fecha = date.fromisoformat("2021-12-10")
    assert cammesa_scraper.avalaible_date(fecha)

    cammesa_scraper.download_by_date(fecha)
    cammesa_scraper.shutdown()
    download_folder = os.path.expanduser("~")+"/Downloads/"
    assert "" in download_folder

    os.remove(download_folder + "/")

def test_smn_scrapper():
    smn_scrapper = SMNScraper()
    fecha = date.fromisoformat("2021-05-06")
    smn_scrapper.download_by_date(fecha)
    assert "datohorario20210506.txt" in os.listdir()
