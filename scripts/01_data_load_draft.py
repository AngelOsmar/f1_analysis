# %%
import pandas as pd

# %%
results = pd.read_csv("../data/results.csv")  # set index col as index
# %%
# select columns to use
circuits_cols = list(("circuitRef", "circuitId", "country", "lat"))
status_cols = list(("statusId", "status"))
races_cols = list(("circuitId", "date", "time", "round"))
drivers_cols = list(("driverId", "driverRef", "dob", "nationality"))
# %%
# import helper dataframes
circuits = pd.read_csv("../data/circuits.csv", usecols=circuits_cols)
status = pd.read_csv("../data/status.csv", usecols=status_cols)
races = pd.read_csv("../data/races.csv", usecols=races_cols)
drivers = pd.read_csv("../data/drivers.csv", usecols=drivers_cols)
# constructors = pd.read_csv('../data/constructors.csv', usecols=[
# 'constructorId', 'constructorRef'
# ])
# %%
constructors = pd.read_csv(
    "../data/constructors.csv", usecols=["constructorId", "constructorRef"]
)
# %%
# join data
results_test = results.join(races, how="left", on="raceId", rsuffix="_hour")
# %%
results_test = results_test.join(circuits, how="left", on="circuitId", rsuffix="_right")
# %%
results_test = results_test.join(status, on="statusId", rsuffix="_right")
# %%
results_test = results_test.join(drivers, on="driverId", rsuffix="_right")
# %%
results_test = results_test.join(constructors, on="constructorId", rsuffix="_right")
# %%
ext_bool = results_test.columns.str.contains("_right")
# %%
cols_to_drop = results_test.columns[ext_bool]
# %%
results_test = results_test.drop(cols_to_drop, axis="columns")
# %%
id_cols = results_test.columns[results_test.columns.str.contains("Id")]
id_cols = id_cols.drop(id_cols[0])
# %%
results_test = results_test.drop(id_cols, axis="columns")
# %%
results_test = results_test.drop("positionText", axis="columns")
# %%
# results_test.to_csv('master_table.csv')
