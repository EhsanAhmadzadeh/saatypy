class ModelError(Exception):
    """Base error for decision models."""

class StructureError(ModelError):
    """Invalid model structure (missing blocks, zero columns, etc.)."""

class NormalizationError(ModelError):
    """Raised when labeled normalization of vectors/matrices fails."""

class DuplicatedCluster(ModelError):
    """Raised when trying to add a cluster with a duplicate name."""
    
class UnknownLabel(ModelError):
    """Raised when referencing a label that isn't registered."""

class ConsistencyError(ModelError):
    """Raised when a matrix is internally inconsistent (e.g., mismatched reciprocals)."""

class InvalidSaatyScaleError(ModelError):
    """Raised when an input value is not on the Saaty 1–9 scale (or its reciprocal)."""
