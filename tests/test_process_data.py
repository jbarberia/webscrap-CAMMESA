from numpy import fromstring
import pytest
from webscrap_cammesa import read_files
from webscrap_cammesa.data_processing.process_data import parse_cammesa, parse_smn
from datetime import datetime

def _extract_day(x: str):
    return datetime.strptime(x, "%d-%m-%y %H:%M").day

def test_parse_cammesa() -> None:
    df = parse_cammesa("./tests/data")
    assert df.iloc[286].Eólico == 983.82 
    assert _extract_day(df.iloc[287].id) - _extract_day(df.iloc[286].id) == 1

def test_parse_smn() -> None:
    df = parse_smn("./tests/data")
    assert _extract_day(df.iloc[24].id) - _extract_day(df.iloc[23].id) == 1

def test_read_files() -> None:
    df = read_files("./tests/data", "./tests/data")
    for col in ["Eólico", "Fotovoltaico", "Bioenergías", "Hidráulico"]:
        assert col in df.columns
    assert df.shape[0] == 577