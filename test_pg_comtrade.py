from pg_comtrade import sync, query
import pandas as pd
import pytest

@pytest.fixture
def example_data():
    return pd.DataFrame({'col1':['test1'], 'col2':['test2']})
    
@pytest.fixture
def schema():
    return '_team_opss_ds'
    
@pytest.fixture
def table():
    return 'example'


def test_sync(example_data, schema, table):
    try:
        sync(schema=schema,
            table=table,
            df=example_data,
            if_exists='replace')
    except Exception as e:
        pytest.fail(f"Something is wrong with error: {repr(e)}")

    df = query(sql=f"SELECT * FROM {schema}.{table}")
    assert  df.equals(example_data)