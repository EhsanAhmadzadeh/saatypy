import pytest
import numpy as np
from saatypy.components.pairwise import PairwiseComparison

@pytest.fixture
def mock_criteria():
    return ["price", "quality", "service"]

@pytest.fixture
def mock_alternatives():
    return ["A", "B", "C"]

@pytest.fixture
def consistent_matrix_3x3():
    return np.array([
        [1.0, 2.0, 4.0],
        [0.5, 1.0, 2.0],
        [0.25, 0.5, 1.0]
    ])

@pytest.fixture
def consistent_priorities_3x3(consistent_matrix_3x3):
    pc = PairwiseComparison(["A", "B", "C"], consistent_matrix_3x3)
    return pc.priorities()
