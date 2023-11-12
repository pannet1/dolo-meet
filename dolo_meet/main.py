from omspy.brokers.neo import Neo
from constants import CRED, FUTL, logging, CSVF, SDIR
from urllib.parse import urlsplit
import requests
import pandas as pd


def login_and_get_token():
    try:
        kwargs = {"environment": CRED["environment"]}
        client = Neo(
            # user_id=CRED["user_id"],
            password=CRED["password"],
            mobilenumber=CRED["mobilenumber"],
            consumer_key=CRED["consumer_key"],
            consumer_secret=CRED["consumer_secret"],
            twofa=CRED["twofa"],
            **kwargs,
        )
        client.authenticate()
    except Exception as e:
        logging.error(f"while login {e}")
    finally:
        return client


def _filter_csv():
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(CSVF)
        # Filter rows where the 'OPTSTK' column has the value 'stock'
        df = df[df["pInstType"] == "OPTIDX"]
        # Save the updated DataFrame back to the CSV file
        df.to_csv(CSVF, index=False)
    except Exception as e:
        print(f"unable to filter options {e}")


def download_master():
    try:
        url = client.neo.scrip_master("nse_fo")
        response = requests.get(url)
        if response.status_code == 200:
            # Extract filename from URL or use a default name
            filename = urlsplit(url).path.split("/")[-1] or "downloaded_file.csv"
            with open(SDIR + filename, "wb") as file:
                file.write(response.content)
            print(f"File '{filename}' downloaded successfully.")
            _filter_csv()
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
    except Exception as e:
        print("Exception when calling Scrip Master Api->scrip_master: %s\n" % e)


client = login_and_get_token()
if FUTL.is_file_not_2day(CSVF):
    download_master()
else:
    "found master modified today"


"""
inst_tokens = [
    {"instrument_token": "11536", "exchange_segment": "nse_cm"},
    {"instrument_token": "1594", "exchange_segment": "nse_cm"},
    {"instrument_token": "11915", "exchange_segment": "nse_cm"},
    {"instrument_token": "13245", "exchange_segment": "nse_cm"},
]


try:
    # get LTP and Market Depth Data
    ltp = client.neo.quotes(inst_tokens)
    print(ltp)

except Exception as e:
    print(e)
"""
