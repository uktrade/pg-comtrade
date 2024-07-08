import sqlalchemy
from pg_comtrade import sync, query
import pandas as pd
import pytest
import requests_mock
    
@pytest.fixture
def schema():
    return '_team_firebreak_pg'
    
@pytest.fixture
def table():
    return 'example'

def comtrade_json():
    df = pd.read_csv('./data/comtrade_example.txt', delimiter='\t')
    return df.to_dict(orient='records')


def test_sync(schema, table):
    # sql_engine = sqlalchemy.create_engine("postgresql://postgres:postgres@127.0.0.1:5432/")
    sql_engine = sqlalchemy.create_engine("postgresql://")
    
    # This is setting up the "fake" API
    with requests_mock.Mocker() as m:
        url = 'https://comtradeapi.un.org/public/v1/getComtradeReleases'
        m.get(url, json = comtrade_json())
        with sql_engine.connect() as connection:
            try:
                sync(connection=connection, schema=schema,
                    table=table,
                    if_exists='replace')
            except Exception as e:
                pytest.fail(f"Something is wrong with error: {repr(e)}")

            df = query(connection, sql=f"SELECT * FROM {schema}.{table}")
    assert  df.equals(pd.read_csv('./data/comtrade_example.txt', delimiter='\t'))
