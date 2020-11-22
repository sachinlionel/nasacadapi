# SBDB Close-Approach Data API

<br>This API provides access to current close-approach data for all asteroids and comets in JPL’s SBDB (Small-Body DataBase). 
Using this API one can inspect near body objects on given time frame and other query params.
API default response provides near body objects for next 60 days with reference to Earth which are within 0.05 au.
<br>
<br>Refer https://ssd-api.jpl.nasa.gov/doc/cad.html for a detailed documentation. 
<br>
## This project is for practicing the API testing in python/pytest.
<br>**Base URL:** https://ssd-api.jpl.nasa.gov/cad.api
<br>**Implementation ref:**
- `app/client.py` is a python client for base url. (Considered as application under test)
- Acceptance Criteria: 
    - Default response should contain close approach bodies with reference to earth which are within 0.05 au.
    - Default response should contain only 60 days results.
    - API query filter parameters should effective.
    - API sorting should be effective.
    - API query filter parameters and sorting should be effective together.
- Tests are defined under `tests` folder, implements **functional testing**.
- Following are the tests at high level:
    - Test default response behaviour
    - Test filters (positive & negative)
    - Test sorting (positive & negative)
    - Test concurrent calls
    - Test complex filters :: TODO
    - Test complex filters with sorting :: TODO


## Directory Structure

```
├── Dockerfile # Builds docker Image for containerizing test app
├── app # Application under test
│   └── client.py # Python client of API
├── docker-compose.yml # Compose config for running containerized test app
├── readme.md # Test app Info & Instruction 
├── requirements.txt # Python libs required for test app
├── run_tests.py # Tests executable
├── tests # Tests folder
│   ├── pytest.ini # Pytest config file
│   ├── test_api_concurrent.py
│   ├── test_api_default_params.py
│   ├── test_api_filters.py
│   └── test_api_sorting.py
└── utils # Test utils folder
    └── data_utils.py
```

## Tests executable
```
usage: run_tests.py [-h] [--smoke-test] [--keywords KEYWORDS] [--pdb PDB]

optional arguments:
  -h, --help           show this help message and exit
  --smoke-test         Run Smoke Tests
  --keywords KEYWORDS  run tests with keyword
  --pdb PDB            enable pdb on first failure
```
- Junit test report will be available in execution path as `test.xml` after test execution
- Code coverage can be reviewed by opening `htmlcov/index.html` in browser. 
- Ignore the coverage percent for now, as the application under test is not actual application. 

## How to execute
1. Containerized execution, requires docker & docker-compose.
    - `docker-compose up` Builds docker image, executes tests inside container.
    - `docker-compose down` To remove container.
2. Non containerized execution, requires python3 & a python virtualenv.
    - `source <virtualenv>/bin/activate` Activates virtual environment.
    - `pip install -r requirements.txt` Install python libraries.
    -  `python run_tests.py` Execute tests.

## Console Report
```
Running tests with following arguments ['test', '-vs', '--junitxml=test.xml', '--cov=./app', '--cov-report=html', '-k test', 'test']
============================= test session starts ==============================
platform darwin -- Python 3.8.1, pytest-6.1.0, py-1.9.0, pluggy-0.13.1 -- /Users/sachin/dev/unifi_virtenv3/bin/python
cachedir: .pytest_cache
rootdir: /Users/sachin/dev/next/dir/test, configfile: pytest.ini
plugins: celery-4.4.0, instafail-0.4.1.post0, cov-2.10.1
collecting ... collected 77 items

test/test_api_concurrent.py::TestApiConcurrent::test_concurrent_call[5] PASSED
test/test_api_concurrent.py::TestApiConcurrent::test_concurrent_call[10] PASSED
test/test_api_default_params.py::TestApiDefaultParams::test_response_code PASSED
test/test_api_default_params.py::TestApiDefaultParams::test_response_structure PASSED
test/test_api_default_params.py::TestApiDefaultParams::test_response_has_results PASSED
test/test_api_default_params.py::TestApiDefaultParams::test_response_results_are_within_60days PASSED
test/test_api_default_params.py::TestApiDefaultParams::test_response_results_are_within_0_05au PASSED
test/test_api_default_params.py::TestApiDefaultParams::test_response_default_sorting PASSED
test/test_api_filters.py::TestApiFilters::test_date_time_filter_cases[filter_key = date-min, filter_value = 2000-01-01, Expected results: cd values ge 2000-01-01] PASSED
test/test_api_filters.py::TestApiFilters::test_date_time_filter_cases[filter_key = date-max, filter_value = 2100-01-01, Expected results: cd values le 2100-01-01] PASSED
test/test_api_filters.py::TestApiFilters::test_numeric_filter_cases[filter_key = dist-min, filter_value = 0.04, Expected results: dist values ge 0.04] PASSED
test/test_api_filters.py::TestApiFilters::test_numeric_filter_cases[filter_key = dist-max, filter_value = 0.03, Expected results: dist values le 0.03] PASSED
test/test_api_filters.py::TestApiFilters::test_numeric_filter_cases[filter_key = dist-min, filter_value = 10LD, Expected results: dist values ge 10LD] PASSED
test/test_api_filters.py::TestApiFilters::test_numeric_filter_cases[filter_key = dist-max, filter_value = 7LD, Expected results: dist values le 7LD] PASSED
test/test_api_filters.py::TestApiFilters::test_numeric_filter_cases[filter_key = h-min, filter_value = 10, Expected results: h values ge 10] PASSED
test/test_api_filters.py::TestApiFilters::test_numeric_filter_cases[filter_key = h-max, filter_value = 20, Expected results: h values le 20] PASSED
test/test_api_filters.py::TestApiFilters::test_numeric_filter_cases[filter_key = h-min, filter_value = 9.56, Expected results: h values ge 9.56] PASSED
test/test_api_filters.py::TestApiFilters::test_numeric_filter_cases[filter_key = h-max, filter_value = 20.05, Expected results: h values le 20.05] PASSED
test/test_api_filters.py::TestApiFilters::test_numeric_filter_cases[filter_key = v-inf-min, filter_value = 7.01, Expected results: v_inf values ge 7.01] PASSED
test/test_api_filters.py::TestApiFilters::test_numeric_filter_cases[filter_key = v-inf-max, filter_value = 15, Expected results: v_inf values le 15] PASSED
test/test_api_filters.py::TestApiFilters::test_numeric_filter_cases[filter_key = v-rel-min, filter_value = 5.01, Expected results: v_inf values ge 5.01] PASSED
test/test_api_filters.py::TestApiFilters::test_numeric_filter_cases[filter_key = v-rel-max, filter_value = 11.9, Expected results: v_inf values le 11.9] PASSED
test/test_api_filters.py::TestApiFilters::test_orbit_class_filter_cases[SDBDOrbitClass.IEO] PASSED
test/test_api_filters.py::TestApiFilters::test_orbit_class_filter_cases[SDBDOrbitClass.ATE] PASSED
test/test_api_filters.py::TestApiFilters::test_orbit_class_filter_cases[SDBDOrbitClass.APO] PASSED
test/test_api_filters.py::TestApiFilters::test_orbit_class_filter_cases[SDBDOrbitClass.AMO] PASSED
test/test_api_filters.py::TestApiFilters::test_orbit_class_filter_cases[SDBDOrbitClass.MCA] XFAIL
test/test_api_filters.py::TestApiFilters::test_orbit_class_filter_cases[SDBDOrbitClass.IMB] XFAIL
test/test_api_filters.py::TestApiFilters::test_orbit_class_filter_cases[SDBDOrbitClass.MBA] XFAIL
test/test_api_filters.py::TestApiFilters::test_orbit_class_filter_cases[SDBDOrbitClass.OMB] XFAIL
test/test_api_filters.py::TestApiFilters::test_orbit_class_filter_cases[SDBDOrbitClass.TJN] XFAIL
test/test_api_filters.py::TestApiFilters::test_orbit_class_filter_cases[SDBDOrbitClass.CEN] XFAIL
test/test_api_filters.py::TestApiFilters::test_orbit_class_filter_cases[SDBDOrbitClass.TNO] XFAIL
test/test_api_filters.py::TestApiFilters::test_orbit_class_filter_cases[SDBDOrbitClass.PAA] XFAIL
test/test_api_filters.py::TestApiFilters::test_orbit_class_filter_cases[SDBDOrbitClass.HYA] XFAIL
test/test_api_filters.py::TestApiFilters::test_orbit_class_filter_cases[SDBDOrbitClass.HYP] XFAIL
test/test_api_filters.py::TestApiFilters::test_orbit_class_filter_cases[SDBDOrbitClass.PAR] XFAIL
test/test_api_filters.py::TestApiFilters::test_orbit_class_filter_cases[SDBDOrbitClass.COM] XFAIL
test/test_api_filters.py::TestApiFilters::test_orbit_class_filter_cases[SDBDOrbitClass.JFC] PASSED
test/test_api_filters.py::TestApiFilters::test_orbit_class_filter_cases[SDBDOrbitClass.HTC] XFAIL
test/test_api_filters.py::TestApiFilters::test_orbit_class_filter_cases[SDBDOrbitClass.ETc] XFAIL
test/test_api_filters.py::TestApiFilters::test_orbit_class_filter_cases[SDBDOrbitClass.CTc] XFAIL
test/test_api_filters.py::TestApiFilters::test_orbit_class_filter_cases[SDBDOrbitClass.JFc] PASSED
test/test_api_filters.py::TestApiFilters::test_body_filter_cases[CloseApproachBodies.Mars] PASSED
test/test_api_filters.py::TestApiFilters::test_body_filter_cases[CloseApproachBodies.Moon] PASSED
test/test_api_filters.py::TestApiFilters::test_body_filter_cases[CloseApproachBodies.ALL] PASSED
test/test_api_filters.py::TestApiFilters::test_bad_request_filter[filter_key = date-min, filter_value = 2000-JAN-01, Expected response code: 400] PASSED
test/test_api_filters.py::TestApiFilters::test_bad_request_filter[filter_key = date-max, filter_value = 2000-March-01, Expected response code: 400] PASSED
test/test_api_filters.py::TestApiFilters::test_bad_request_filter[filter_key = dist-min, filter_value = 5KAU, Expected response code: 400] PASSED
test/test_api_filters.py::TestApiFilters::test_bad_request_filter[filter_key = dist-max, filter_value = -10LD, Expected response code: 400] PASSED
test/test_api_filters.py::TestApiFilters::test_bad_request_filter[filter_key = h-min, filter_value = 4g, Expected response code: 400] PASSED
test/test_api_filters.py::TestApiFilters::test_bad_request_filter[filter_key = h-max, filter_value = -70, Expected response code: 400] PASSED
test/test_api_filters.py::TestApiFilters::test_bad_request_filter[filter_key = v-inf-min, filter_value = --, Expected response code: 400] PASSED
test/test_api_filters.py::TestApiFilters::test_bad_request_filter[filter_key = v-inf-min, filter_value = -0.99, Expected response code: 400] PASSED
test/test_api_filters.py::TestApiFilters::test_bad_request_filter[filter_key = v-rel-min, filter_value = -900, Expected response code: 400] PASSED
test/test_api_filters.py::TestApiFilters::test_bad_request_filter[filter_key = v-rel-min, filter_value = ten, Expected response code: 400] PASSED
test/test_api_filters.py::TestApiFilters::test_bad_request_filter[filter_key = des, filter_value = humanoid, Expected response code: 400] PASSED
test/test_api_filters.py::TestApiFilters::test_bad_request_filter[filter_key = body, filter_value = 433 Eros, Expected response code: 400] PASSED
test/test_api_filters.py::TestApiFilters::test_bad_request_filter[filter_key = limit, filter_value = -15, Expected response code: 400] PASSED
test/test_api_filters.py::TestApiFilters::test_bad_request_filter[filter_key = limit, filter_value = -0.1, Expected response code: 400] PASSED
test/test_api_filters.py::TestApiFilters::test_query_param_fullname PASSED
test/test_api_filters.py::TestApiFilters::test_query_param_body PASSED
test/test_api_filters.py::TestApiFilters::test_query_param_limit PASSED
test/test_api_sorting.py::TestApiSorting::test_sorting[dist] PASSED
test/test_api_sorting.py::TestApiSorting::test_sorting[-dist] PASSED
test/test_api_sorting.py::TestApiSorting::test_sorting[date] PASSED
test/test_api_sorting.py::TestApiSorting::test_sorting[-date] PASSED
test/test_api_sorting.py::TestApiSorting::test_sorting[dist-min] PASSED
test/test_api_sorting.py::TestApiSorting::test_sorting[-dist-min] PASSED
test/test_api_sorting.py::TestApiSorting::test_sorting[v-inf] PASSED
test/test_api_sorting.py::TestApiSorting::test_sorting[-v-inf] PASSED
test/test_api_sorting.py::TestApiSorting::test_sorting[h] PASSED
test/test_api_sorting.py::TestApiSorting::test_sorting[-h] PASSED
test/test_api_sorting.py::TestApiSorting::test_invalid_sorting[dist-max] PASSED
test/test_api_sorting.py::TestApiSorting::test_invalid_sorting[body] PASSED
test/test_api_sorting.py::TestApiSorting::test_invalid_sorting[-body] PASSED
test/test_api_sorting.py::TestApiSorting::test_invalid_sorting[-fullname] PASSED

---------- generated xml file: /Users/sachin/dev/next/dir/test.xml -----------

---------- coverage: platform darwin, python 3.8.1-final-0 -----------

Coverage HTML written to dir htmlcov

================== 62 passed, 15 xfailed in 202.51s (0:03:22) ==================`

Process finished with exit code 0`
```

