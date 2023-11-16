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
    print("found master modified today")


"""
    based on the user settings of base
    symbol nifty or banknifty get the ltp
    find ATM
"""


def atm_strike() -> int:
    return 15600


def ce_pe_symbols(atm_strike) -> list:
    """
    you can adapt any data structure
    you want. i am not restricting you
    here
    """
    lst = [{15600: {"CE": 0, "PE": 0}}, {15650: {"CE": 0, "PE": 0}}]
    return lst


def get_nse_history(lst_ce_pe) -> None:
    """
    i have attached a sample program
    that downloads data from any NSE endpoint.
    you just suit it your need.
    refer bhavcopy.py in this repo for the target url
    we need 10 days of ohlc. also move this function
    outside this file, so we dont have to deal with nse
    code here.
    """
    return None


def generate_signals(lst_ce_pe) -> None:
    """
    this is buy only strategy so all
    our entries are buy. a new buy can come anytime
    on any symbol we are scanning. check rules.
    """

    def read_dumped_csv(dct):
        pass

    for dct in lst_ce_pe:
        history = read_dumped_csv(dct)

    # from the history read the array starting from the oldest
    # and extropolate to the current day.


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
