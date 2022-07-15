# %%
import re
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
import numpy as np

# %%
# Get year and constructor data
ctr_results = pd.read_csv("../data/constructor_results.csv")
ctr_names = pd.read_csv(
    "../data/constructors.csv", usecols=["constructorId", "constructorRef"]
)
races = pd.read_csv("../data/races.csv", usecols=["raceId", "year", "date"])
# %%
data = ctr_results.merge(ctr_names, how="left", on="constructorId")
# %%
data = data.merge(races, how="left", on="raceId")
# %%
# test join integrity by searching for mercedes
# data = data.loc[
#     data.constructorRef=='mercedes',['constructorRef','year','date']
#     ]

# data.drop_duplicates(subset=['constructorRef','year'],inplace=True)

# data.year.unique()
# %%
data = data[["constructorRef", "year"]].drop_duplicates()
# %%

matrix_data = data.pivot(
    index="year", columns="constructorRef", values="constructorRef"
)
# %%
msno.matrix(matrix_data, labels=True, figsize=(50, 20))

# %%
# change `matrix_data` stored data to contain numbers instead of labels to make calculations easier.

matrix_data[matrix_data.notnull()] = 1

# get teams with longest history in F1

matrix_data.sum().sort_values(ascending=False).head(10)
# %% [markdown]
""" If we take the 2021 season as reference the results are quite surprising. In recent years there has been a fierce competition between Mercedes, Red Bull and Ferrari each championship. Thus, it seems strange that unlike Ferrari, the former two teams have less than 20 years competing as constructors in F1.

We will center our analysis to take into account the period consisting between the earliest year, where all three constructors are present and the latest year of data available
"""
# %%
matrix_data[matrix_data["mercedes"].notnull()]
# %% [markdown]
""" Given the results, we will use the subset of data from the year 2010 up to 2022 of the `results.csv` dataset. We will need to merge other datasets in order to know the year in which each race took place and other data not included in this particular dataset.
"""
# %%
circuits_cols = list(("circuitRef", "circuitId", "country", "lat"))
races_cols = list(("raceId", "year", "name"))
drivers_cols = list(("driverId", "driverRef", "dob", "nationality"))

results = pd.read_csv("../data/results.csv")
races = pd.read_csv("../data/races.csv", usecols=["raceId", "year", "name"])
drivers = pd.read_csv("../data/drivers.csv", usecols=drivers_cols)
status = pd.read_csv("../data/status.csv")
# %%
# merge results and races to know year
f1_info = (
    results.merge(races, how="left", on="raceId")
    .merge(drivers, how="left", on="driverId")
    .merge(status, how="left", on="statusId")
    .merge(ctr_names, how="left", on="constructorId")
)
# get subset from year 2010 up to 2022
f1_subset = f1_info[f1_info["year"] >= 2010].copy()

f1_subset.year.unique()
# %%
# export to excel to explore data interactively

# f1_subset.to_csv('02_f1ExploreData.csv')
# %%
# change column names to snake_case
for name in f1_subset.columns:
    snake_name = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
    f1_subset.rename(columns={name: snake_name}, inplace=True)

f1_subset.columns
# %%
# delete id cols
cols_to_drop = f1_subset.columns[f1_subset.columns.str.contains("_id")]

f1_subset.drop(cols_to_drop, axis="columns", inplace=True)
# %%
f1_subset[["constructor_ref", "driver_ref", "points", "year"]].groupby(
    ["year", "constructor_ref", "driver_ref"]
).sum()
# %%
pivot = f1_subset.pivot_table(
    index=["year", "constructor_ref", "driver_ref"], values=["points"], aggfunc=np.sum
)
# %%
pivot.tail(10)
