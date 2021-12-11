import pandas as pd
import os
from os import listdir
from datetime import datetime

def read_files(cammesa_folder: str, smn_folder: str) -> pd.DataFrame:
    df_cammesa = parse_cammesa(cammesa_folder)
    pass
    # df_smn = parse_smn(smn_folder)

def is_file_in_path(folder:str):
    return lambda file: os.path.isfile(path(folder, file))

def path(folder:str, file:str) -> str:
    path = "{}/{}".format(folder, file)
    return path

def parse_cammesa(folder: str) -> pd.DataFrame:
    # Read all the file data
    is_file = is_file_in_path(folder)
    files = filter(is_file, listdir(folder))
    # Store all the CSV data
    data = []
    for file in filter(lambda x: x.endswith(".csv"), files):
        data.append(pd.read_csv(path(folder, file), sep=";", decimal=","))
    # Concat the data
    df = pd.concat(data, ignore_index=True)
    # Sort by date
    df.Momento = pd.to_datetime(df.Momento)
    df.sort_values("Momento")
    return df

def parse_smn(folder: str) -> pd.DataFrame:
    # Read all the file data
    is_file = is_file_in_path(folder)
    files = filter(is_file, listdir(folder))
    # Store all the TXT data
    data = []
    colspecs = [(0, 8), (8, 14), (14, 20), (20, 26), (26,33), (33, 39), (39, 47), (47, 103)]
    for file in filter(lambda x: x.endswith(".txt"), files):
        data.append(pd.read_fwf(path(folder, file), skiprows=[1], colspecs=colspecs))
    df = pd.concat(data, ignore_index=True)
    # Remove bad data (Nan)
    df = df.dropna()
    # Generate date (Momento) and sort it
    to_str = lambda x: str(int(x))
    df["Momento"] = df["HORA"].apply(to_str) + "-" + df["FECHA"].apply(to_str)
    df["Momento"] = df["Momento"].apply(lambda x: datetime.strptime(x, "%H-%d%m%Y"))
    # drop unuseful columns
    df.drop(["FECHA", "HORA"], axis=1)

    return df