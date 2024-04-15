import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


# Retrieve Google Cloud credentials from key
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/key.json" 

@data_exporter
def export_data(data, *args, **kwargs):
    # GCS bucket details
    bucket_name = 'seismic_data_888'
    table_name = 'raw_usgs_eq_data'
    root_path = f'{bucket_name}/{table_name}'

    # Create new 'year' and 'month' columns from the 'time' column for partitioning
    data['year'] = data['time'].dt.year
    data['month'] = data['time'].dt.month

    table = pa.Table.from_pandas(data)
    gcs = pa.fs.GcsFileSystem()

    # Export data as parquet files
    pq.write_to_dataset(
        table,
        root_path=root_path,
        filesystem=gcs,
        partition_cols=['year', 'month'],
        existing_data_behavior='delete_matching'
    )
