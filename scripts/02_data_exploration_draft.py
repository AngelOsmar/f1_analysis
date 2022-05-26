# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import numpy as np

# %%
races = pd.read_csv("master_df.csv")
# %%
races.info()
races.head()
# %%
races.columns
races.info()
# %%
# Drop `Unnamed: 0` column
races.drop("Unnamed: 0", axis="columns", inplace=True)

# Use regex to change name columns to common convention
for name in races.columns:
    snake_name = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
    races.rename(columns={name: snake_name}, inplace=True)

races.columns
# %%
# Make a table with the name of each unique constructor and the years in which they have raced, plot and identify the longest amount of time with the same constructors recent constructors.
# parse date as time series object
races["date"] = pd.to_datetime(races["date"], format="%d/%m/%y")
# %%

# fig, ax = plt.subplots(figsize=(12,6))

plot_data = pd.DataFrame(
    {"years": races.date.dt.year, "constructor": races.constructor_ref}
)
