import io
from datetime import datetime
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):  
    def fetch_usgs_earthquake_data(start_date, end_date):
        """
        Load USGS EQ API data for a specific period into a dataframe
        """
        base_url = 'https://earthquake.usgs.gov/fdsnws/event/1/'
        
        # URL for obtaining the data
        query_url = base_url + 'query'
        # URL for counting the number of rows without fetching the data
        count_url = base_url + 'count'
        # Period constraints
        params = {
            "starttime": start_date,
            "endtime": end_date
        }

        # Datatypes for dataframe columns 
        eq_dtypes = {
            'latitude': float,
            'longitude': float,
            'depth': float,
            'mag': float,
            'magType': str,
            'nst': pd.Int64Dtype(),
            'gap': float,
            'dmin': float,
            'rms': float,
            'net': str,
            'id': str,
            'place': str,
            'type': str,
            'locationSource': str,
            'magSource': str,
            'horizontalError': float,
            'depthError': float,
            'magError': float,
            'magNst': pd.Int64Dtype(),
            'status': str
        }
        # Datetime columns
        parse_dates = ['time', 'updated']

        # Get the total number of earthquakes in the specified date range
        count_response = requests.get(count_url, params=params)
        count_response.raise_for_status()
        total_count = int(count_response.text)

        # If the total number of earthquakes is less than or equal to 20000, 
        # fetch all data in one request
        if total_count <= 20000:
            print(f'Processing batch of {total_count} records from {start_date} to {end_date}')
            params["format"] = "csv"
            params["limit"] = total_count
            response = requests.get(query_url, params=params)
            response.raise_for_status()
            df = pd.read_csv(io.StringIO(response.text),
                             sep=',', dtype=eq_dtypes, parse_dates=parse_dates)
        # If the total number of earthquakes exceeds 20000, 
        # divide the time range in half and make recursive calls
        else:
            mid_date = ((end_date - start_date) / 2) + start_date
            df1 = fetch_usgs_earthquake_data(start_date, mid_date)
            df2 = fetch_usgs_earthquake_data(mid_date, end_date)
            df = pd.concat([df1, df2])

        return df

    
    # Obtain raw earthquake data from {{ start_date }} to today
    start_date = pd.to_datetime(kwargs['start_date']).date()
    end_date = pd.to_datetime('today').date()
    print(f"Fetching earthquake data from {start_date} to {end_date}")
    df = fetch_usgs_earthquake_data(start_date, end_date)
    return df


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
    assert len(output.index) >= 10000, 'The data does not have enough records'

@test
def test_columns(output, *args) -> None:
    assert len(output.columns) == 22, 'Unexpected number of columns'
