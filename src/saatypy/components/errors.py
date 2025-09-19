class ModelError(Exception):
    """Base error for decision models."""

class StructureError(ModelError):
    """Invalid model structure (missing blocks, zero columns, etc.)."""

class NormalizationError(ModelError):
    """Raised when labeled normalization of vectors/matrices fails."""

class UnknownLabel(ModelError):
    """Raised when refer the label that isn't registered to the model."""


class ConsistencyError(ModelError):
    """Raised when a matrix is internally inconsistent (e.g., mismatched reciprocals)."""

class InvalidSaatyScaleError(ModelError):
    """Raised when an input value is not on the Saaty 1–9 scale (or its reciprocal)."""
