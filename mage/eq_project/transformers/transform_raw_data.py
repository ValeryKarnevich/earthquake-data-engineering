import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data: pd.DataFrame, *args, **kwargs):
    # Filter to earthquake events only
    data = data[data['type'] == 'earthquake']

    # Assign categories based on magnitude
    bins = [-999, 3, 4, 5, 6, 7, 8, 999]
    labels = ['micro', 'minor', 'light', 'moderate', 'strong', 'major', 'great']

    # Create a new column with categories based on numerical_values
    data['category'] = pd.cut(data['mag'], 
        bins=bins, labels=labels, right=False).astype('str')

    # Combine latitude and longitide into a single column
    data["coords"] = data["latitude"].astype(str) + ',' + data["longitude"].astype(str)

    # Drop unnecessary columns, records with null data in main columns, duplicate records
    data = data \
        .drop(columns=['net', 'location_source', 'mag_source', 'type', 'latitude', 'longitude']) \
        .dropna(subset=['time', 'coords', 'depth', 'mag', 'id', 'category']) \
        .drop_duplicates()

    return data


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
