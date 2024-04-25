import pytest

from benchmark.benchmark_task import BenchmarkTask


@pytest.mark.parametrize('response, expected', [
    ('Sure, here you go!\nhello', 'hello'),
    ('Sure, here you go!\n\nhello', 'hello'),
    ('Sure, here you go!\t\thello', ''),
    ('\nSure, here you go!\nhello', 'hello'),
    ('\n\tSure, here you go!\t\nhello', 'hello')
])
def test_benchmark_task_strip_boilerplate(response, expected):
    assert BenchmarkTask.strip_boilerplate(response) == expected
