import os
import json
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from pandas import DataFrame

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


# Retrieve Google Cloud credentials from key
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/key.json" 
with open(os.environ['GOOGLE_APPLICATION_CREDENTIALS'], 'r') as fp:
    credentials = json.load(fp)

@data_exporter
def export_data_to_big_query(df: DataFrame, **kwargs) -> None:  
    # BigQuery details
    project_id = credentials['project_id']
    table_id = f'{project_id}.eq.mart_eq'
    config_path = os.path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    # Export data to BigQuery
    BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).export(
        df,
        table_id,
        if_exists='replace', 
    )
