"""Test suite for core components of SaatyPy."""
import pytest
import numpy as np
from numpy.testing import assert_array_almost_equal

from saatypy.components.scale import SaatyScale
from saatypy.components.pairwise import PairwiseComparison
from saatypy.components.modeling import Node, Cluster
from saatypy.components.errors import (
    ModelError,
    NormalizationError,
    StructureError,
    ConsistencyError,
    InvalidSaatyScaleError
)


def test_saaty_scale_validation_and_reciprocal():
    """Test Saaty scale validation and reciprocal calculation."""
    assert SaatyScale.is_valid(1.0)
    assert SaatyScale.is_valid(9.0)
    assert SaatyScale.is_valid(1/9)
    assert not SaatyScale.is_valid(0.0)
    assert not SaatyScale.is_valid(-1.0)
    assert not SaatyScale.is_valid(1.3)

    assert SaatyScale.reciprocal(2.0) == 0.5
    assert SaatyScale.reciprocal(1.0) == 1.0

    with pytest.raises(InvalidSaatyScaleError):
        SaatyScale.reciprocal(0.0)
    with pytest.raises(InvalidSaatyScaleError):
        SaatyScale.reciprocal(-1.0)
    with pytest.raises(InvalidSaatyScaleError):
        SaatyScale.reciprocal(1.3)


def test_saaty_scale_all_values():
    """Test SaatyScale.all_valid_values returns full correct list."""
    values = SaatyScale.ALLOWED_VALUES
    assert 1 in values
    assert 2 in values
    assert 1/3 in values
    assert 1/9 in values
    assert 9 in values
    assert 1.3 not in values


def test_pairwise_comparison_from_judgments(mock_criteria):
    """Test PairwiseComparison creation from sparse judgments."""
    judgments = {
        ("price", "quality"): 2,
        ("price", "service"): 4,
        ("quality", "service"): 2
    }
    pc = PairwiseComparison.from_judgments(mock_criteria, judgments)

    assert pc.matrix.shape == (3, 3)
    assert np.all(pc.matrix > 0)
    assert np.allclose(np.diag(pc.matrix), 1.0)
    assert np.allclose(pc.matrix * pc.matrix.T, 1.0)

    assert pc.matrix[0, 1] == 2.0
    assert pc.matrix[0, 2] == 4.0
    assert pc.matrix[1, 2] == 2.0
    assert pc.matrix[1, 0] == 0.5


def test_pairwise_from_judgments_invalid(mock_criteria):
    """Test PairwiseComparison.from_judgments with invalid values."""
    with pytest.raises(InvalidSaatyScaleError):
        PairwiseComparison.from_judgments(
            mock_criteria,
            {("price", "quality"): 1.3}
        )

    with pytest.raises(ConsistencyError):
        PairwiseComparison.from_judgments(
            mock_criteria,
            {
                ("price", "quality"): 2,
                ("quality", "price"): 4  # Should be 0.5 to be consistent
            }
        )


def test_pairwise_comparison_consistency(consistent_matrix_3x3, consistent_priorities_3x3):
    """Test consistency calculations in PairwiseComparison."""
    pc = PairwiseComparison(["A", "B", "C"], consistent_matrix_3x3)
    cr, ci, lambda_max = pc.consistency_ratio()

    assert cr == pytest.approx(0.0, abs=1e-6)
    assert ci == pytest.approx(0.0, abs=1e-6)
    assert lambda_max == pytest.approx(3.0, abs=1e-6)

    assert_array_almost_equal(pc.priorities(), consistent_priorities_3x3, decimal=6)


def test_node_and_cluster():
    """Test Node and Cluster creation and validation."""
    node = Node("price", description="Cost in USD")
    assert node.name == "price"
    assert node.description == "Cost in USD"

    cluster = Cluster("criteria", [
        Node("price"),
        Node("quality"),
        Node("service")
    ])
    assert cluster.name == "criteria"
    assert cluster.size == 3
    assert [n.name for n in cluster.nodes] == ["price", "quality", "service"]

    assert "price" in str(cluster)

    with pytest.raises(ValueError):
        Cluster("test", [Node("price"), Node("price")])


def test_error_class_hierarchy():
    """Test that custom error classes inherit properly."""
    assert issubclass(ModelError, Exception)
    assert issubclass(NormalizationError, ModelError)
    assert issubclass(StructureError, ModelError)
    assert issubclass(ConsistencyError, ModelError)
    assert issubclass(InvalidSaatyScaleError, ModelError)
