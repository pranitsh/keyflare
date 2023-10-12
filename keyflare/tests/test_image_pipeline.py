# pylint: disable=redefined-outer-name
"""
Tests the image pipeline, the old and the new version, for improvements.
"""
import os
import numpy as np
import pytest
from PIL import Image
from ..image_pipeline import ImagePipeline


@pytest.fixture
def test_image():
    """
    Fixture that loads a test image from a file for consistent testing.

    Returns:
        np.ndarray: The test image as a NumPy array.
    """
    test_image_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "images",
        "tests.jpg",
    )
    return np.array(Image.open(test_image_path))


@pytest.mark.benchmark(min_rounds=10)
def test_image_pipeline(test_image, benchmark):
    """
    Benchmark test for improved ImagePipeline's run method.
    - It measures the time take to process the image and extract coordinates of clickable locations.

    Assertions:
        - Ensures that coordinate_data is a list.
        - Ensures that coordinate_data contains data.
        - Ensures that each item in coordinate_data is a pair of (key, coordinates).
    """
    y = ImagePipeline()
    y.x.image = lambda: test_image
    benchmark(y.run)
    coordinate_data = y.coordinate_data
    assert isinstance(coordinate_data, list)
    assert len(coordinate_data) > 0
    assert len(coordinate_data[0]) == 2


@pytest.mark.benchmark(min_rounds=10)
def test_old_image_pipeline(test_image, benchmark):
    """
    Benchmark test for my older ImagePipeline process that used tesseract.

    Assertions:
        - Ensures that coordinate_data is a dict. I previously used a dicts
        - Ensures that coordinate_data contains at least one coordinate.
        - Ensures that each item in coordinate_data is a pair of (key, coordinates).
    """
    y = ImagePipeline()
    y.x.image = lambda: test_image
    benchmark(y.old_run)
    coordinate_data = y.coordinate_data
    assert isinstance(coordinate_data, dict), "I used a dictionary in my old process"
    assert len(coordinate_data) > 0, "More than 1 item is necessary"
    assert len(coordinate_data["aa"]) == 2, "Each item does not have two items"
