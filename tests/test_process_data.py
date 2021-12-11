import pytest
from pca_renewables import read_files
from pca_renewables.data_processing.process_data import parse_cammesa, parse_smn

def test_parse_cammesa() -> None:
    df = parse_cammesa("./tests/data")

    assert df.iloc[286].Eólico == 983.82 
    assert (df.iloc[287].Momento.day - df.iloc[286].Momento.day) == 1

def test_parse_smn() -> None:
    df = parse_smn("./tests/data")
    assert (df.iloc[2086].Momento.day - df.iloc[2085].Momento.day) == 1