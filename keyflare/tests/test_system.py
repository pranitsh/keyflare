import os
import pytest
import numpy as np
from ..system import System
import time

test_image_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "images", "test.jpg")

@pytest.fixture(scope="module")
def system_instance():
    """
    Fixture; creates an instance of the System class.

    Returns:
        System: An instance of the System class.
    """
    system = System()
    return system

@pytest.mark.benchmark(min_rounds=10)
def test_capture_screenshot_benchmark(system_instance, benchmark):
    """
    Benchmark test for taking a screenshot and converting it a numpy.ndarray as part of System's image() method.

    Args:
        system_instance (System): An instance of the System class.
        benchmark: The benchmark fixture provided by pytest-benchmark.

    Assertions:
        - Ensures that the captured screenshot is an instance of np.ndarray.
    """
    def capture_screenshot():
        return system_instance.image()

    result = benchmark(capture_screenshot)
    assert isinstance(result, np.ndarray)

if __name__ == "__main__":
    pytest.main([__file__])
