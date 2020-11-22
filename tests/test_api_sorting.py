from collections import namedtuple
from http import HTTPStatus

import pandas as pd
import pytest

from app.client import APIClient
from utils.data_utils import get_df

# Sorting test case blueprint
# column: sorting resultant column
# key: soring key
# reverse: takes boolean, true for descending and false for ascending
sorting_test_case = namedtuple('sorting_test_case',
                               'column '
                               'key '
                               'reverse ')

# Sorting test case blueprint for invalid cases
# key: soring key
# expected_response_code: expected api response code
invalid_sorting_test_case = namedtuple('invalid_sorting_test_case',
                                       'key '
                                       'expected_response_code ')

# Sorting test cases
sorting_test_cases = [
    sorting_test_case('dist', 'dist', False),
    sorting_test_case('dist', '-dist', True),
    sorting_test_case('cd', 'date', False),
    sorting_test_case('cd', '-date', True),
    sorting_test_case('dist_min', 'dist-min', False),
    sorting_test_case('dist_min', '-dist-min', True),
    sorting_test_case('v_inf', 'v-inf', False),
    sorting_test_case('v_inf', '-v-inf', True),
    sorting_test_case('h', 'h', False),
    sorting_test_case('h', '-h', True),
    # TODO:: Implement object filter
    # sorting_test_case('des', 'object', False),
    # sorting_test_case('des', '-object', True),
]

# Invalid sorting test cases
invalid_sorting_test_cases = [
    invalid_sorting_test_case('dist-max', HTTPStatus.BAD_REQUEST),
    invalid_sorting_test_case('body', HTTPStatus.BAD_REQUEST),
    invalid_sorting_test_case('-body', HTTPStatus.BAD_REQUEST),
    invalid_sorting_test_case('-fullname', HTTPStatus.BAD_REQUEST),
]


# Test Ids
def sorting_test_case_id(test_case):
    """Test names for sorting_test_cases & invalid_sorting_test_cases"""
    return f"{test_case.key}"


# Test class
class TestApiSorting:
    test_client = APIClient()

    def __get_response_df(self, params):
        """
        Get dataframe of response if API response in HTTPStatus.OK (200)
        :param params: api query params as dict
        :return: pandas DF
        """
        res = self.test_client.get(params=params)
        if res.code == HTTPStatus.OK:
            fields = res.get_fields()
            data = res.get_data()
            df = get_df(data, columns=fields)
            return df

    @pytest.mark.parametrize('test_case', sorting_test_cases, ids=sorting_test_case_id)
    def test_sorting(self, test_case):
        """
        test sorting
        """
        res_df = self.__get_response_df(params={'sort': test_case.key, 'limit': 5})
        # response for api
        actual_sorted = res_df[test_case.column].to_list()
        # convert time into Timestamp datatype in case of `cd` column
        if test_case.column == 'cd':
            actual_sorted = list(filter(None, pd.to_datetime(actual_sorted)))
        else:
            actual_sorted = list(filter(None, actual_sorted))
        # assert api response is sorted,
        # sorted builtin check whether the list is sorted or not
        # sorted builtin takes reverse boolean arg, true for descending and false for ascending
        assert actual_sorted == sorted(actual_sorted, reverse=test_case.reverse), "Not sorted as expected"

    @pytest.mark.parametrize('test_case', invalid_sorting_test_cases, ids=sorting_test_case_id)
    def test_invalid_sorting(self, test_case):
        """
         test sorting with invalid sorting keys
        """
        params = {'sort': test_case.key}
        res = self.test_client.get(params=params)
        assert res.code == test_case.expected_response_code, "HTTP status is not as expected"
