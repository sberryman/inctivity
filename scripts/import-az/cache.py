import json
import random
import requests
import time
import pandas as pd
import numpy as np
from tqdm import tqdm
from pathlib import Path
import sys

# where are we saving files?
output_path = Path("/app/data/cache")

# parse our csv
df = pd.read_csv(
    "/app/data/ROC_Posting-List_2020-06-08.csv",
    skiprows=1,
    dtype={
        "License No": str
    }
)

# load our license numbers
print("Loading license numbers...")
license_numbers = [row["License No"] for _, row in df.iterrows()]

# just fill the gaps!
# license_numbers = np.arange(
#     300000,
#     np.amax(
#         np.array(license_numbers)
#     )
# )

print("Checking existing cache...")
new_license_numbers = []
for license_number in license_numbers:
    # build the output path for this license
    license_path = output_path.joinpath(
        "{}.json".format(license_number)
    )

    # skip if we already have it cached!
    if license_path.exists():
        continue

    new_license_numbers.append(license_number)

# shuffle the numbers
random.shuffle(new_license_numbers)

# and away they go!
for license_number in tqdm(new_license_numbers):
    # build the output path for this license
    license_path = output_path.joinpath(
        "{}.json".format(license_number)
    )
    # print("license_path: {}".format(license_path))

    # build our payload
    payload = {
        "ff": "contractorSearchResults",
        "searchfor": license_number,
        "city": "",
        "persontype": "",
        "ctrtype": "",
        "licensestatus": "",
        "resultstoreturn": "20",
        "classtype": "",
        "clientIP": ".".join(str(random.randint(0, 255)) for _ in range(4)),
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
        "referer": "https://roc.az.gov/contractor-search",
        "accept-language": "en-US,en;q=0.9",
    }

    # make the request!
    r = requests.get(
        "https://roc.az.gov/online-services",
        params=payload,
        headers=headers,
    )

    # save our response!
    with open(license_path, "w") as out_file:
        json.dump(
            r.json(),
            out_file,
            indent=4,
        )

    # take a break
    time.sleep(
        np.random.uniform(
            1.0,
            3.0
        )
    )