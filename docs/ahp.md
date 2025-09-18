# Analytic Hierarchy Process (AHP)

## Overview

The Analytic Hierarchy Process (AHP), developed by Thomas L. Saaty in the 1970s, is a structured technique for organizing and analyzing complex decisions. This document provides a comprehensive overview of AHP methodology, implementation details, and practical applications.

## Mathematical Foundation

### 1. Hierarchical Structure

AHP decomposes a decision problem into a hierarchy of more easily comprehended sub-problems:
1. Goal (top level)
2. Criteria (and possibly sub-criteria)
3. Alternatives (bottom level)

### 2. Pairwise Comparisons

Comparisons use Saaty's fundamental scale:

| Intensity | Definition | Explanation |
|-----------|------------|-------------|
| 1 | Equal importance | Elements contribute equally |
| 3 | Moderate importance | One element slightly favored |
| 5 | Strong importance | One element strongly favored |
| 7 | Very strong importance | Dominance demonstrated in practice |
| 9 | Extreme importance | Highest possible order of affirmation |
| 2,4,6,8 | Intermediate values | When compromise is needed |

### 3. Priority Calculation

For a comparison matrix A:

1. Normalize each column:
   $a_{ij}^* = \frac{a_{ij}}{\sum_{k=1}^n a_{kj}}$

2. Calculate priority vector:
   $w_i = \frac{1}{n}\sum_{j=1}^n a_{ij}^*$

### 4. Consistency Check

Consistency Ratio (CR) calculation:

1. Calculate Consistency Index (CI):
   $CI = \frac{\lambda_{max} - n}{n - 1}$

2. Calculate CR:
   $CR = \frac{CI}{RI}$

where RI is the Random Index based on matrix size. CR ≤ 0.1 is considered acceptable.

## Implementation Details

### Core Components

1. **Pairwise Comparison Matrix**
   ```python
   class PairwiseComparison:
       def __init__(self, labels: List[str]):
           self.labels = labels
           self.matrix = np.ones((len(labels), len(labels)))
   ```

2. **Priority Calculation**
   ```python
   def calculate_priorities(matrix: np.ndarray) -> np.ndarray:
       normalized = matrix / matrix.sum(axis=0)
       return normalized.mean(axis=1)
   ```

### Model Building

```python
from saatypy.ahp import AHPBuilder

model = (AHPBuilder()
    .criteria(["price", "quality", "service"])
    .alternatives(["A", "B", "C"])
    .build())
```

## Practical Example

### Laptop Selection Case

Consider choosing between three laptops based on performance, price, and battery life.

```python
# Create model
model = (AHPBuilder()
    .criteria(["performance", "price", "battery"])
    .alternatives(["laptop_a", "laptop_b", "laptop_c"])
    .build())

# Set criteria weights
model.set_criteria_weights({
    "performance": 0.5,
    "price": 0.3,
    "battery": 0.2
})

# Set alternative priorities for each criterion
for criterion in ["performance", "price", "battery"]:
    model.set_alt_priorities(criterion, priorities_dict)
```

## Advantages and Limitations

### Advantages
- Structured approach to complex decisions
- Handles both objective and subjective criteria
- Built-in consistency checking
- Hierarchical decomposition of complex problems

### Limitations
- Number of comparisons grows quadratically
- Rank reversal possibility
- Assumes criteria independence

## References

1. Saaty, T.L. (1980). "The Analytic Hierarchy Process." McGraw-Hill, New York.
2. Saaty, T.L. (1990). "How to make a decision: The Analytic Hierarchy Process." European Journal of Operational Research, 48(1), 9-26.
3. Saaty, T.L. (2008). "Decision making with the analytic hierarchy process." International Journal of Services Sciences, 1(1), 83-98.