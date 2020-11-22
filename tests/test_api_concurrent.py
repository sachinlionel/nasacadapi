import time
from http import HTTPStatus
from multiprocessing import Process

import pytest

from app.client import APIClient


@pytest.mark.smoke
class TestApiConcurrent:

    client = APIClient()

    def concurrent_task(self):
        """
        function for testing concurrent calls
        """
        response = self.client.get()
        assert response.code == HTTPStatus.OK, response.raw_content

    @pytest.mark.parametrize("num_of_concurrency", (5, 10))
    def test_concurrent_call(self, num_of_concurrency):
        """
        test concurrent calls
        """
        process_list = []
        for _ in range(num_of_concurrency):
            p = Process(target=self.concurrent_task)
            # sleep is required in unauthorized testing to avoid 503 tmp error
            time.sleep(0.1)
            process_list.append(p)
            p.start()

        # Exit code zero indicates success for concurrent_task, other wise exit code is non zero
        sum_exitcode = 0
        for p in process_list:
            p.join()
            sum_exitcode += p.exitcode
        assert sum_exitcode == 0, "one or more concurrent task failed"
