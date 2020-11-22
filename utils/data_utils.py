import json
from http import HTTPStatus

import pandas as pd
from requests import get


def get_df(data, columns):
    """
    Get pandas dataframe out of data & column
    :param data: is row data. data on API response
    :param columns: is column names. fields on API response
    :return: pandas dataframe
    """
    return pd.DataFrame(data=data, columns=columns)


def get_des_class_name(des_name):
    """
    Utility function to get ORBIT class name from external sbdb.api
    :param des_name: asteroid or comet name
    :return: ORBIT class name
    """
    url = 'https://ssd-api.jpl.nasa.gov/sbdb.api'
    params = {'des': des_name}
    res = get(url, params=params)
    code = res.status_code
    raw_content = res.content.decode()
    content_decoded = '{}' if raw_content == '' else raw_content
    json_content = json.loads(content_decoded)
    if code == HTTPStatus.OK:
        return json_content['object']['orbit_class']['code']
