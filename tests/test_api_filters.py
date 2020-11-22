import datetime
import operator
from collections import namedtuple
from http import HTTPStatus

import pandas as pd
import pytest

from app.client import APIClient, SDBDOrbitClass, CloseApproachBodies
from utils.data_utils import get_df, get_des_class_name

# Filter test case blueprint
# filter_key: key name for filter
# filter_value: value for filter
# impact_column: column which will expected to have filters applied
# impact_column_focus_value_by: pick column value by math operator for easy assertion of filter function
# compare_operator: math operator for comparing filter value with column values
# compare_with: is always filter_value or transformed filter_value for easy assertion
filter_test_case = namedtuple('filter_test_case',
                              'filter_key '
                              'filter_value '
                              'impact_column '
                              'impact_column_focus_value_by '
                              'compare_operator '
                              'compare_with')

# Datetime filter test cases
datetime_filter_test_cases = [
    filter_test_case('date-min',
                     '2000-01-01',
                     'cd',
                     min,
                     operator.ge,
                     datetime.datetime.strptime('2000-01-01', "%Y-%m-%d")),
    filter_test_case('date-max',
                     '2100-01-01',
                     'cd',
                     max,
                     operator.le,
                     datetime.datetime.strptime('2100-01-01', "%Y-%m-%d")),
]

# Numeric filter test cases
numeric_filter_test_cases = [
    filter_test_case('dist-min',
                     '0.04',
                     'dist',
                     min,
                     operator.ge,
                     0.04),
    filter_test_case('dist-max',
                     '0.03',
                     'dist',
                     max,
                     operator.le,
                     0.03),
    filter_test_case('dist-min',
                     '10LD',
                     'dist',
                     min,
                     operator.ge,
                     10 * 0.002569),
    filter_test_case('dist-max',
                     '7LD',
                     'dist',
                     max,
                     operator.le,
                     7 * 0.002569),
    filter_test_case('h-min',
                     10,
                     'h',
                     min,
                     operator.ge,
                     10),
    filter_test_case('h-max',
                     20,
                     'h',
                     max,
                     operator.le,
                     20),
    filter_test_case('h-min',
                     9.56,
                     'h',
                     min,
                     operator.ge,
                     9.56),
    filter_test_case('h-max',
                     20.05,
                     'h',
                     max,
                     operator.le,
                     20.05),
    filter_test_case('v-inf-min',
                     7.01,
                     'v_inf',
                     min,
                     operator.ge,
                     7.01),
    filter_test_case('v-inf-max',
                     15,
                     'v_inf',
                     max,
                     operator.le,
                     15.7),
    filter_test_case('v-rel-min',
                     5.01,
                     'v_inf',
                     min,
                     operator.ge,
                     5.01),
    filter_test_case('v-rel-max',
                     11.9,
                     'v_inf',
                     max,
                     operator.le,
                     11.9),

]

# Filter test case blueprint for invalid cases
# filter_key: key name for filter
# filter_value: value for filter
# expected_response_code: expected api response code
invalid_filter_test_case = namedtuple('invalid_filter_test_case',
                                      'filter_key '
                                      'filter_value '
                                      'expected_response_code')

# Invalid filter test cases
invalid_filter_test_cases = [
    invalid_filter_test_case('date-min', '2000-JAN-01', HTTPStatus.BAD_REQUEST),
    invalid_filter_test_case('date-max', '2000-March-01', HTTPStatus.BAD_REQUEST),
    invalid_filter_test_case('dist-min', '5KAU', HTTPStatus.BAD_REQUEST),
    invalid_filter_test_case('dist-max', '-10LD', HTTPStatus.BAD_REQUEST),
    invalid_filter_test_case('h-min', '4g', HTTPStatus.BAD_REQUEST),
    invalid_filter_test_case('h-max', '-70', HTTPStatus.BAD_REQUEST),
    invalid_filter_test_case('v-inf-min', '--', HTTPStatus.BAD_REQUEST),
    invalid_filter_test_case('v-inf-min', '-0.99', HTTPStatus.BAD_REQUEST),
    invalid_filter_test_case('v-rel-min', '-900', HTTPStatus.BAD_REQUEST),
    invalid_filter_test_case('v-rel-min', 'ten', HTTPStatus.BAD_REQUEST),
    invalid_filter_test_case('des', 'humanoid', HTTPStatus.BAD_REQUEST),
    invalid_filter_test_case('body', '433 Eros', HTTPStatus.BAD_REQUEST),
    invalid_filter_test_case('limit', '-15', HTTPStatus.BAD_REQUEST),
    invalid_filter_test_case('limit', '-0.1', HTTPStatus.BAD_REQUEST),
]


# Test Ids
def filter_test_case_id(test_case):
    """
    test name for datetime_filter_test_cases & numeric_filter_test_cases
    """
    return f"filter_key = {test_case.filter_key}, filter_value = {test_case.filter_value}, " \
           f"Expected results: {test_case.impact_column} values {test_case.compare_operator.__name__} " \
           f"{test_case.filter_value}"


def invalid_filter_test_case_id(test_case):
    """
    test name for invalid_filter_test_cases
    """
    return f"filter_key = {test_case.filter_key}, filter_value = {test_case.filter_value}, " \
           f"Expected response code: {test_case.expected_response_code}"


# Test Class
class TestApiFilters:
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

    @pytest.mark.parametrize('test_case', datetime_filter_test_cases, ids=filter_test_case_id)
    def test_date_time_filter_cases(self, test_case):
        """
        test filter of date time datatype
        """
        res_df = self.__get_response_df(params={test_case.filter_key: test_case.filter_value})
        # actual_value is column value used for asserting filter functionality
        actual_value = test_case.impact_column_focus_value_by(pd.to_datetime(res_df[test_case.impact_column]))
        assert test_case.compare_operator(actual_value, test_case.compare_with)

    @pytest.mark.parametrize('test_case', numeric_filter_test_cases, ids=filter_test_case_id)
    def test_numeric_filter_cases(self, test_case):
        """
        test filter of numeric datatype
        """
        res_df = self.__get_response_df(params={test_case.filter_key: test_case.filter_value})
        # actual_value is column value used for asserting filter functionality
        actual_value = test_case.impact_column_focus_value_by(pd.to_numeric(res_df[test_case.impact_column]))
        assert test_case.compare_operator(actual_value, test_case.compare_with)

    @pytest.mark.parametrize('test_case', SDBDOrbitClass)
    def test_orbit_class_filter_cases(self, test_case):
        """
        test filter by orbit classes
        """
        res_df = self.__get_response_df(params={'class': test_case.name, 'limit': 5, 'date-min': '1900-01-01'})
        if not res_df.empty:
            des_class_list = res_df['des'].apply(get_des_class_name).to_list()
            assert set(des_class_list) == {test_case.name}
        else:
            pytest.xfail(f"{test_case.name} des are not seen in mentioned timeframe")

    @pytest.mark.parametrize('test_case', [CloseApproachBodies.Mars, CloseApproachBodies.Moon, CloseApproachBodies.ALL])
    def test_body_filter_cases(self, test_case):
        """
        test filter by reference body
        """
        res_df = self.__get_response_df(params={'body': test_case.name, 'limit': 5, 'date-min': '1900-01-01'})
        if test_case.name not in ['ALL', '*']:
            assert 'body' not in res_df.columns
        else:
            assert 'body' in res_df.columns

    @pytest.mark.parametrize('test_case', invalid_filter_test_cases, ids=invalid_filter_test_case_id)
    def test_bad_request_filter(self, test_case):
        """
        test filter of invalid cases
        """
        params = {test_case.filter_key: test_case.filter_value}
        res = self.test_client.get(params=params)
        assert res.code == test_case.expected_response_code

    def test_query_param_fullname(self):
        """
        test query param fullname
        """
        res_df = self.__get_response_df(params={'fullname': True})
        assert 'fullname' in res_df.columns
        assert not res_df['fullname'].empty

    def test_query_param_body(self):
        """
        test query param body
        """
        res_df = self.__get_response_df(params={'body': 'ALL'})
        assert 'body' in res_df.columns
        assert not res_df['body'].empty

    def test_query_param_limit(self):
        """
        test query param limit
        """
        res = self.test_client.get(params={'limit': 15})
        assert res.get_count() == 15

    # TODO:: Implement seperate test class for test_query_param** tests
    # TODO:: Implement tests for following filters
    # pha, nea, comet, nea-comet, neo, kind, spk
