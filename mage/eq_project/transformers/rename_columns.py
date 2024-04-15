from re import sub

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    def snake_case(s):
        """
        Convert string to snake case
        """
        return '_'.join(
            sub('([A-Z][a-z]+)', r' \1',
            sub('([A-Z]+)', r' \1',
            s.replace('-', ' '))).split()).lower()


    # Convert column names to snake case
    new_columns = []
    for column in data.columns:
        new_column = snake_case(column)
        new_columns.append(new_column)

    print("Number of columns changed to snake case: ")
    print(len(data.columns) - sum(data.columns == new_columns))
    
    data.columns = new_columns

    return data


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
