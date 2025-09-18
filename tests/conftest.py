"""Shared test fixtures and configuration."""
import pytest
import numpy as np

@pytest.fixture
def mock_criteria():
    """Common criteria names for testing."""
    return ["price", "quality", "service"]

@pytest.fixture
def mock_alternatives():
    """Common alternative names for testing."""
    return ["A", "B", "C"]

@pytest.fixture
def consistent_matrix_3x3():
    """A perfectly consistent 3x3 comparison matrix."""
    return np.array([
        [1.0, 2.0, 4.0],
        [0.5, 1.0, 2.0],
        [0.25, 0.5, 1.0]
    ])

@pytest.fixture
def consistent_priorities_3x3():
    """Expected priorities for the consistent_matrix_3x3."""
    return np.array([0.571428571, 0.285714286, 0.142857143])