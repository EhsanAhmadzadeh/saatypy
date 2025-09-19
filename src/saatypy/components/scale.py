from __future__ import annotations
from typing import Final, Dict
import numpy as np
from saatypy.components.errors import ConsistencyError, InvalidSaatyScaleError


class SaatyScale:
    ALLOWED_VALUES: Final[list[float]] = [
        1 / 9,
        1 / 8,
        1 / 7,
        1 / 6,
        1 / 5,
        1 / 4,
        1 / 3,
        1 / 2,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
    ]

    @staticmethod
    def is_valid(x: float) -> bool:
        if x <= 0:
            return False
        for v in SaatyScale.ALLOWED_VALUES:
            if np.isclose(x, v, atol=1e-6):
                return True
        return False

    @staticmethod
    def pretty_scale() -> list[str]:
        return [
            "1/9",
            "1/8",
            "1/7",
            "1/6",
            "1/5",
            "1/4",
            "1/3",
            "1/2",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
        ]

    @staticmethod
    def reciprocal(x: float) -> float:
        if not SaatyScale.is_valid(x):
            raise InvalidSaatyScaleError(
                f"Invalid Saaty scale value: {x}. Allowed values are: {SaatyScale.pretty_scale()}"
            )
        return 1.0 / x

    @staticmethod
    def apply_judgment(
        matrix: np.ndarray,
        i: int,
        j: int,
        value: float,
        label_i: str,
        label_j: str,
    ) -> None:
        if not SaatyScale.is_valid(value):
            raise InvalidSaatyScaleError(
                f"Invalid Saaty judgment value ({label_i} vs {label_j}): {value}. "
                f"Must be in Saaty's scale: {SaatyScale.pretty_scale()}."
            )

        reciprocal = SaatyScale.reciprocal(value)
        existing = matrix[i, j]
        existing_rec = matrix[j, i]

        is_unset = np.isclose(existing, 1.0) and np.isclose(existing_rec, 1.0)

        if not is_unset:
            if not (
                np.isclose(existing, value, atol=1e-6)
                and np.isclose(existing_rec, reciprocal, atol=1e-6)
            ):
                raise ConsistencyError(
                    f"Inconsistent judgments for ({label_i}, {label_j}): "
                    f"existing=({existing}, {existing_rec}), new=({value}, {reciprocal})"
                )

        matrix[i, j] = value
        matrix[j, i] = reciprocal


# Random Index (RI) values for CR computation (Saaty, n=1..15). We cap at 15.
_RI: Final[Dict[int, float]] = {
    1: 0.00,
    2: 0.00,
    3: 0.58,
    4: 0.90,
    5: 1.12,
    6: 1.24,
    7: 1.32,
    8: 1.41,
    9: 1.45,
    10: 1.49,
    11: 1.51,
    12: 1.48,
    13: 1.56,
    14: 1.57,
    15: 1.59,
}
RI_TABLE: Final[Dict[int, float]] = _RI
