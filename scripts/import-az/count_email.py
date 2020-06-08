import json
from pathlib import Path

cache_path = Path("/app/data/cache")

multi_record_count = 0
record_count = 0
contact_count = 0
email_count = 0
license_ids = []
license_active_count = 0
license_inactive_count = {}
noresults_count = 0
email_domains = {}
email_list = []
contact_list = []
gov_id_count = 0
phone_count = 0
birthday_count = 0
contact_email_count = 0

account_ids = []
account_province = {}

for file_path in cache_path.glob("*.json"):
    with open(file_path, "r") as in_file:
        data = json.load(in_file)
    
    if len(data) != 1:
        # file_path.unlink()
        multi_record_count += 1
        continue

    if "noresults" in data[0]:
        noresults_count += 1
        continue
    
    record_count += 1
    
    # we should only have 1 record
    data = data[0]

    # update our counts per state
    if "ROC_State_Province__c" in data:
        if data["Id"] not in account_ids:
            account_ids.append(data["Id"])

            state_prov = data["ROC_State_Province__c"]
            if state_prov not in account_province:
                account_province[state_prov] = 0
            
            # increase the count
            account_province[state_prov] += 1

    if "Licenses__r" in data:
        for lic in data["Licenses__r"]["records"]:
            # skip if we've already processed this license
            if lic["Id"] in license_ids:
                continue

            # add to the list
            license_ids.append(lic["Id"])

            if lic["Status__c"] == "Active":
                license_active_count += 1
            else:
                if lic["Status__c"] not in license_inactive_count:
                    license_inactive_count[lic["Status__c"]] = 0
                license_inactive_count[lic["Status__c"]] += 1

    # bump our email count
    if "Email__c" in data:
        email_count += 1

        # how about the domain?
        email = data["Email__c"]

        if email not in email_list:
            email_list.append(email)
        
    if "Account_Contacts__r" in data:
        for acct in data["Account_Contacts__r"]["records"]:
            contact_count += 1

            if "Contact__r" in acct:
                contact = acct["Contact__r"]

                if contact["Id"] not in contact_list:
                    contact_list.append(contact["Id"])

                    if "Email" in contact:
                        contact_email_count += 1
                        email = contact["Email"]
                        if email not in email_list:
                            email_list.append(email)
                    if "drivers_License_or_government_id_no__c" in contact:
                        gov_id_count += 1
                    if "Phone" in contact:
                        phone_count += 1
                    if "Birthdate" in contact:
                        birthday_count += 1

    # for email in email_list:
    #     domain = email[email.index("@")+1:]

    #     if domain not in email_domains:
    #         email_domains[domain] = 0
        
    #     email_domains[domain] += 1
    
    # break

print("-" * 50)
email_percent = email_count / record_count
print(
    "Success: {} emails (total: {} ({:.1f}%) - unique: {} ({:.1f}%) - multi: {} - noresults: {})".format(
        email_count,
        record_count,
        email_percent * 100,
        len(email_list),
        (len(email_list) / email_count) * 100,
        multi_record_count,
        noresults_count,
    )
)
print("License: Active: {} - Other: {}".format(
    license_active_count,
    sorted(
        license_inactive_count.items(),
        key=lambda x: x[0]
    ),
))
print("Contacts: Total: {} - Gov Id: {} - Email: {} - Phone number: {} - Birthday: {}".format(
    len(contact_list),
    gov_id_count,
    contact_email_count,
    phone_count,
    birthday_count,
))
print("Accounts by state: {}".format(
    sorted(
        account_province.items(),
        key=lambda x: x[0]
    ),
))

# sorted_email_domains = sorted(
#     email_domains.items(),
#     key=lambda x: x[1],
#     reverse=True,
# )

# with open("/app/data/email_domains.json", "w") as out_file:
#     json.dump(sorted_email_domains, out_file, indent=4)

