import pytest
import numpy as np
from numpy.testing import assert_array_almost_equal
from saatypy.components.errors import (
    InvalidSaatyScaleError,
    ConsistencyError,
    StructureError,
    NormalizationError,
    UnknownLabel
)
from saatypy.components.pairwise import PairwiseComparison


def test_pairwise_matrix_validation():
    labels = ["A", "B"]

    with pytest.raises(NormalizationError, match="All comparison values must be positive"):
        M = np.array([[1.0, -2.0], [-0.5, 1.0]])
        PairwiseComparison(labels, M)

    with pytest.raises(StructureError, match="All diagonal values must be 1.0"):
        M = np.array([[2.0, 2.0], [0.5, 1.0]])
        PairwiseComparison(labels, M)

    with pytest.raises(ConsistencyError, match="Matrix is not reciprocal"):
        M = np.array([[1.0, 2.0], [0.6, 1.0]])  # 0.6 ≠ 1/2
        PairwiseComparison(labels, M)

    with pytest.raises(StructureError, match="Matrix shape"):
        M = np.array([
            [1.0, 2.0, 3.0],
            [0.5, 1.0, 2.0],
            [0.33, 0.5, 1.0]
        ])
        PairwiseComparison(["A", "B"], M)


def test_pairwise_from_invalid_judgments():
    labels = ["price", "quality", "design"]

    with pytest.raises(UnknownLabel, match="Unknown"):
        PairwiseComparison.from_judgments(
            labels,
            {("price", "unknown"): 2.0}
        )

    with pytest.raises(InvalidSaatyScaleError, match="Invalid Saaty"):
        PairwiseComparison.from_judgments(
            labels,
            {("price", "quality"): -1.0}
        )

    with pytest.raises(ConsistencyError, match="Inconsistent judgments"):
        PairwiseComparison.from_judgments(
            labels,
            {
                ("price", "quality"): 3,
                ("quality", "price"): 3  # should be 1/3 to be consistent
            }
        )


def test_pairwise_principal_eigen():
    matrix = np.array([
        [1.0, 2.0, 4.0],
        [0.5, 1.0, 2.0],
        [0.25, 0.5, 1.0]
    ])
    priorities = np.array([0.5714, 0.2857, 0.1429])
    pc = PairwiseComparison(["A", "B", "C"], matrix)

    lam, evec = pc.principal_eigen()
    assert lam == pytest.approx(3.0, abs=1e-2)
    assert_array_almost_equal(evec, priorities, decimal=2)

    assert_array_almost_equal(pc.priorities(), priorities, decimal=2)

    lam2, evec2 = pc.principal_eigen()
    assert_array_almost_equal(evec2, evec, decimal=6)


def test_pairwise_comparisons_normalized():
    labels = ["A", "B", "C"]
    pc = PairwiseComparison.from_judgments(
        labels,
        {
            ("A", "B"): 2.0,
            ("A", "C"): 4.0,
            ("B", "C"): 2.0
        }
    )
    priorities = pc.priorities()
    assert np.sum(priorities) == pytest.approx(1.0, abs=1e-6)
    assert np.all(priorities > 0)


def test_pairwise_comparison_string_repr():
    labels = ["A", "B"]
    M = np.array([[1.0, 2.0], [0.5, 1.0]])
    pc = PairwiseComparison(labels, M)
    assert str(pc).startswith("PairwiseComparison")
