import sqlalchemy
from pg_comtrade import sync, query
import pandas as pd
import pytest

@pytest.fixture
def example_data():
    return pd.DataFrame({'col1':['test1'], 'col2':['test2']})
    
@pytest.fixture
def schema():
    return 'public'
    
@pytest.fixture
def table():
    return 'example'


def test_sync(example_data, schema, table):
    sql_engine = sqlalchemy.create_engine("postgresql://postgres:postgres@127.0.0.1:5432/")
    with sql_engine.connect() as connection:
        try:
            sync(connection=connection, schema=schema,
                table=table,
                df=example_data,
                if_exists='replace')
        except Exception as e:
            pytest.fail(f"Something is wrong with error: {repr(e)}")

        df = query(connection, sql=f"SELECT * FROM {schema}.{table}")
    assert  df.equals(example_data)