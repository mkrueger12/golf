import os

import pandas as pd
import requests
from draft_kings import Sport, Client
from io import StringIO


def get_field(league, n):
    ''' Get the field based on the DraftKings fields. '''

    # urls
    API_BASE_URL = 'https://api.draftkings.com'
    DRAFTGROUPS_PATH = '/draftgroups/v1/'

    # get contests

    contest = Client().contests(sport=Sport.GOLF)

    contest = contest['contests']
    contest = pd.DataFrame.from_dict(contest)
    df = contest.sort_values(by=['name'])

    dgid = df[df['name'].str.contains('PGA')]
    print(dgid.iloc[n, 8], dgid.iloc[n, 2])
    dgid = dgid.iloc[n, 2]


    # get draft table
    url = f"{API_BASE_URL}{DRAFTGROUPS_PATH}draftgroups/{dgid}/draftables"

    df = requests.get(url).json()
    df = pd.Series(df)
    df = df['draftables']
    df = pd.DataFrame(df)
    df = df.iloc[:, [0, 3, 4, 5, 6, 7, 8, 9, 10, 25]]
    df = df[df['status'] != 'O']
    df = df.drop_duplicates()
    df.rename(columns={'displayName': 'name'}, inplace=True)

    return df


def sg_data(date):

    """ Collects latest strokes gained data from db """

    # get data
    os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'

    # download data
    sql = ('SELECT * FROM "golf-processed"."adjusted_sg_table_processed_all"')

    data = wr.athena.read_sql_query(sql, database="golf-processed")

    # data after 2017
    data = data[data['start_date'] > date]
    data.sort_values(by=['start_date', 'trnyearid', 'full', 'round'], ascending=True, inplace=True)

    return data



