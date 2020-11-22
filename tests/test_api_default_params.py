import datetime
import pytest
from http import HTTPStatus

import pandas as pd

from app.client import APIClient
from utils.data_utils import get_df


@pytest.mark.smoke
class TestApiDefaultParams:
    """
    Test default API response
    """
    test_client = APIClient()
    res = test_client.get()
    res_count = res.get_count()
    fields = res.get_fields()
    data = res.get_data()
    df = get_df(data, columns=fields)

    def test_response_code(self):
        """
        Test api response code
        """
        assert self.res.code == HTTPStatus.OK

    def test_response_structure(self):
        """
        Test api response structure
        """
        response = self.res.json_content
        assert response['signature']['source'] == 'NASA/JPL SBDB Close Approach Data API'
        assert response['signature']['version'] == '1.1'
        assert int(response['count']) >= 0
        if int(response['count']) > 0:
            assert response['fields']
            assert response['data']

    def test_response_has_results(self):
        """
        Test api response has some results
        """
        assert self.res_count > 0

    def test_response_results_are_within_60days(self):
        """
        Test default api results are within 60 days from today
        Timedelta of 1 day has been used to easily overcome TZ issues
        # TODO: Better solution for TZ issues
        """
        min_date = datetime.datetime.today().date() - datetime.timedelta(days=1)
        max_date = (min_date + datetime.timedelta(days=61))
        # assert latest item in results in within 60 days from today
        latest_date_in_res = pd.to_datetime(self.df['cd']).max()
        assert latest_date_in_res <= max_date
        # assert earliest item in results in not older than today
        earliest_date_in_res = pd.to_datetime(self.df['cd']).min()
        assert earliest_date_in_res >= min_date

    def test_response_results_are_within_0_05au(self):
        """
        Test default api results are within 0.05 au distance
        """
        distances_in_res = self.df['dist']
        # assert farthest item in results is less than 0.05 au
        max_distances_in_res = distances_in_res.max()
        assert float(max_distances_in_res) <= 0.05

    def test_response_default_sorting(self):
        """
        Test default api results are sorted based on `cd` ascending
        """
        actual_sorted = self.df['cd'].to_list()
        # convert time into Timestamp datatype in case of `cd` column
        actual_sorted = list(filter(None, pd.to_datetime(actual_sorted)))
        # assert api response is sorted,
        # sorted builtin check whether the list is sorted or not
        # sorted builtin takes reverse boolean arg, true for descending and false for ascending
        assert actual_sorted == sorted(actual_sorted, reverse=False), "Not sorted as expected"
