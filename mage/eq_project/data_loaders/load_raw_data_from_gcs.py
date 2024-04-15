import pyarrow as pa
import pyarrow.parquet as pq
import os
import pandas as pd
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


# Retrieve Google Cloud credentials from key
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/key.json" 

@data_loader
def load_from_google_cloud_storage(*args, **kwargs):
    # GCS bucket details
    bucket_name = 'seismic_data_888'
    table_name = 'raw_usgs_eq_data'
    root_path = f'{bucket_name}/{table_name}'
    gcs = pa.fs.GcsFileSystem()

    def combine_partitioned_data(start_date, end_date, root_path, fs):
        """
        Load and combine partitioned data from GCS bucket.
        """

        dfs = []
        # Iterate over each month within the specified time interval
        current_date = start_date
        while current_date <= end_date:
            # Construct the path for the current month's partition
            year = current_date.year
            month = current_date.month
            partition_path = f"{root_path}/year={year}/month={month}"
            # Try loading the current month's data
            try:
                print(f'Processing batch for year={year}/month={month}')
                arrow_df = pq.ParquetDataset(partition_path, filesystem=fs)
                pandas_df = arrow_df.read_pandas().to_pandas()
                dfs.append(pandas_df)
            except:
                print(f"There is no data for year={year}/month={month}")
            # Move to the next month
            current_date += pd.DateOffset(months=1)

        # Concatenate all dataframes into a single dataframe
        final_df = pd.concat(dfs)

        return final_df


    # Load raw earthquake data from {{ start_date }} to today
    start_date = pd.to_datetime(kwargs['start_date'])
    end_date = pd.to_datetime('today').date()
    print(f"Loading earthquake data from {start_date} to {end_date}")
    df = combine_partitioned_data(start_date, end_date, root_path, fs=gcs)
    return df


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
    assert len(output.index) >= 10000, 'The data does not have enough records'


@test
def test_columns(output, *args) -> None:
    expected_columns = {
        'latitude',
        'longitude',
        'depth',
        'mag',
        'mag_type',
        'nst',
        'gap',
        'dmin',
        'rms',
        'net',
        'id',
        'place',
        'type',
        'location_source',
        'mag_source',
        'horizontal_error',
        'depth_error',
        'mag_error',
        'mag_nst',
        'status'
        }
    assert set(expected_columns).issubset(set(output.columns)), 'Unexpected columns'