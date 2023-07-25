import requests
import base64

def get_accounts_list():
    WHM_API_URL = "https://br43-cp.valueserver.com.br:2087/json-api/listaccts"
    WHM_USERNAME = "cont9448"
    WHM_PASSWORD = "(o1DS72j!nV0Tv"

    # Prepare the authentication header
    auth_str = f"{WHM_USERNAME}:{WHM_PASSWORD}"
    auth_bytes = auth_str.encode("utf-8")
    auth_header = {
        "Authorization": "Basic " + base64.b64encode(auth_bytes).decode("utf-8")
    }

    try:
        response = requests.get(WHM_API_URL, headers=auth_header)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error during the request:", e)
        return None
    except ValueError as e:
        print("Error decoding JSON response:", e)
        return None

def list_suspended_emails(accounts_list):
    suspended_emails = []
    normal_emails = []
    for account in accounts_list["acct"]:
        email = account["email"]
        suspend_reason = account["suspendreason"]
        if suspend_reason == "Overdue on Payment":
            suspended_emails.append(email)
        else:
            normal_emails.append(email)
    return suspended_emails, normal_emails

def api():
    accounts_list = get_accounts_list()
    if accounts_list and "acct" in accounts_list:
        suspended_emails = list_suspended_emails(accounts_list)
        print("Suspended Emails:")
        print(suspended_emails)
    else:
        print("Unable to retrieve account data.")
