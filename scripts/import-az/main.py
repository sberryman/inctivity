import pandas as pd
import json

# Use 3 decimal places in output display
pd.set_option("display.precision", 3)

# Don't wrap repr(DataFrame) across additional lines
# pd.set_option("display.expand_frame_repr", False)

# Set max rows displayed in output to 25
pd.set_option("display.max_rows", 25)

df = pd.read_csv(
    "/app/data/ROC_Posting-List_2020-06-04.csv",
    skiprows=1,
)

# group based on address
grouped_address = df.groupby([
    "Address",
    "City",
    "State"
])["License No"]

# simple array of arrays for output
output = {}

# loop through and build a json dict which we'll use to pull data
# from roc.az.gov
for address, df_group in grouped_address:
    # print("address: {}".format(address))

    # our license numbers for this group
    license_numbers = sorted(df_group.values.tolist())
    
    # add to our dict
    output[license_numbers[0]] = license_numbers

with open("/app/data/license_group.json", "w") as out_file:
    json.dump(output, out_file, indent=4)