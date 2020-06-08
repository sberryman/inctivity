import json
from pathlib import Path

cache_path = Path("/app/data/cache")

record_count = 0
id_count = 0
birthday_count = 0

used_ids = []

for file_path in cache_path.glob("*.json"):
    with open(file_path, "r") as in_file:
        data = json.load(in_file)
    
    if len(data) != 1:
        continue
    
    record_count += 1
    
    # we should only have 1 record
    data = data[0]

    # bump our email count
    if "Account_Contacts__r" not in data:
        continue

    for contact in data["Account_Contacts__r"]["records"]:
        if "Contact__r" not in contact:
            continue
        
        record = contact["Contact__r"]

        if record["Id"] in used_ids:
            continue

        # we don't want duplicate contacts
        used_ids.append(record["Id"])

        if "drivers_License_or_government_id_no__c" in record:
            id_count += 1
        if "Birthdate" in record:
            birthday_count += 1

        
    
    # break

print("-" * 50)
print("Success: {} ids and {} birthdays (total: {})".format(id_count, birthday_count, record_count))
