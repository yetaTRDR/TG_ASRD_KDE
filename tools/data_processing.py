import pandas as pd
import numpy as np
from pathlib import Path

# Ruta de la carpeta donde está este archivo
BASE_DIR = Path(__file__).resolve().parent.parent  # sube dos niveles: tools -> proyecto
DATA_DIR = BASE_DIR / "data"

def dataprep(path):
    df = pd.read_csv(path)
    df.columns = ["date", "time", "open", "high", "low", "close", "volume"]
    df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"])
    df = df[["datetime", "open", "high", "low", "close", "volume"]]
    df.set_index("datetime", inplace=True)
    return df

def dataprep2(symbol: str, tf: str):
    file_path = DATA_DIR / symbol / f"{symbol}-{tf}.csv"
    df = pd.read_csv(file_path)
    df.columns = ["date", "time", "open", "high", "low", "close", "volume"]
    df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"])
    df = df[["datetime", "open", "high", "low", "close", "volume"]]
    df.set_index("datetime", inplace=True)
    return df

def standardize(X):
    mu = X.mean(axis=0)
    std = X.std(axis=0)
    std = np.where(std == 0, 1, std)
    return (X - mu) / std
