import os
from datetime import datetime
from functools import reduce
from os import listdir

import pandas as pd
from pandas.core.algorithms import unique


def read_files(cammesa_folder: str, smn_folder: str) -> pd.DataFrame:
    df_cammesa = parse_cammesa(cammesa_folder)
    df_smn = parse_smn(smn_folder)
    df = pd.merge(df_cammesa, df_smn, on="id", how="inner")
    return df


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
    df["Momento"] = pd.to_datetime(df["Momento"])
    df.sort_values("Momento")
    df["id"] = (df["Momento"].apply(lambda x: x.strftime("%d-%m-%y %H:%M")))
    df = df.drop("Momento", axis=1)
    return df


def parse_smn(folder: str) -> pd.DataFrame:
    # Read all the file data
    is_file = is_file_in_path(folder)
    files = filter(is_file, listdir(folder))
    # Store all the TXT data
    data = []
    colspecs = [(0, 8), (8, 14), (14, 20), (20, 26), (26,33), (33, 39), (39, 47), (47, 103)]
    for file in filter(lambda x: x.endswith(".txt"), files):
        data.append(pd.read_fwf(path(folder, file), encoding="iso-8859-1", skiprows=[1], colspecs=colspecs))
    df = pd.concat(data, ignore_index=True)
    # Remove bad data (Nan)
    df = df.dropna()
    # Generate date (Momento) and sort it
    to_str = lambda x: str(int(x))
    to_str_check_day = lambda x: "0" + to_str(x) if len(to_str(x)) == 7 else to_str(x) # Start with zeros in days
    df["Momento"] = df["HORA"].apply(to_str) + "-" + df["FECHA"].apply(to_str_check_day)
    df["Momento"] = df["Momento"].apply(lambda x: datetime.strptime(x, "%H-%d%m%Y"))
    df["id"] = (df["Momento"].apply(lambda x: x.strftime("%d-%m-%y %H:%M")))
    # drop unuseful columns
    df = df.drop(["FECHA", "HORA", "Momento"], axis=1)
    # Transpose data, make columns per station
    stations = unique(df["NOMBRE"])
    dfs_for_stations = []
    for station in stations:
        # Sub-df per station
        station_df = df[df["NOMBRE"] == station]
        station_df = station_df.drop("NOMBRE", axis=1)
        # Generate new columns
        cols = {f"{col}" : f"{col}-{station}" for col in station_df.columns if col not in ["id"]}
        station_df = station_df.rename(columns = cols)
        # Append to list to join
        dfs_for_stations.append(station_df)
    # Join dfs
    fun = lambda acc, el: pd.merge(acc, el, on="id", how="outer")
    dfs = reduce(fun, dfs_for_stations)
    dfs = dfs.dropna(axis=1) # Remove empty columns
    return dfs
