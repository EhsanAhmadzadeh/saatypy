# Analytic Network Process (ANP)

## Overview

The Analytic Network Process (ANP), developed by Thomas L. Saaty, extends the Analytic Hierarchy Process (AHP) by handling dependencies and feedback between elements. This document provides a comprehensive guide to ANP methodology, implementation, and applications.

## Mathematical Foundation

### 1. Network Structure

Unlike AHP's hierarchical structure, ANP organizes elements into clusters with various types of dependencies:
- Inner dependencies (within clusters)
- Outer dependencies (between clusters)
- Feedback loops

### 2. Supermatrix Formation

The supermatrix W represents all network relationships:

$$W = \begin{bmatrix} 
W_{11} & W_{12} & \cdots & W_{1n} \\
W_{21} & W_{22} & \cdots & W_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
W_{n1} & W_{n2} & \cdots & W_{nn}
\end{bmatrix}$$

Where $W_{ij}$ represents the influence of cluster i on cluster j.

### 3. Supermatrix Transformation

1. **Unweighted Supermatrix**: Contains local priority vectors
2. **Weighted Supermatrix**: Multiply by cluster weights
3. **Limit Supermatrix**: Raise to powers until convergence
   $\lim_{k \to \infty} W^k$

## Implementation Details

### Core Components

1. **Cluster Definition**
   ```python
   class ANPCluster:
       def __init__(self, name: str, nodes: List[str]):
           self.name = name
           self.nodes = nodes
   ```

2. **Supermatrix Construction**
   ```python
   def build_supermatrix(clusters: List[ANPCluster],
                        dependencies: Dict) -> np.ndarray:
       size = sum(len(c.nodes) for c in clusters)
       matrix = np.zeros((size, size))
       # Fill matrix based on dependencies
       return matrix
   ```

### Model Building

```python
from saatypy.anp import ANPBuilder

model = (ANPBuilder()
    .add_cluster("criteria", ["c1", "c2", "c3"])
    .add_cluster("alternatives", ["a1", "a2"])
    .build())
```

## Example: Market Share Analysis

Consider analyzing market share with interdependent factors:

```python
# Define clusters
model = (ANPBuilder()
    .add_cluster("market_factors", ["price", "quality", "advertising"])
    .add_cluster("competitors", ["comp_a", "comp_b"])
    .build())

# Set inner dependencies
model.set_inner_dependencies("market_factors", "price",
    {"quality": 0.7, "advertising": 0.3})

# Set outer dependencies
model.set_outer_dependencies("competitors", "price",
    {"comp_a": 0.6, "comp_b": 0.4})
```

## Advanced Topics

### 1. Control Hierarchies

ANP can incorporate control hierarchies for:
- Benefits
- Opportunities
- Costs
- Risks

### 2. BOCR Analysis

Benefits, Opportunities, Costs, and Risks (BOCR) provide a comprehensive decision framework:

1. Structure separate networks for each BOCR component
2. Synthesize results using strategic criteria
3. Calculate overall priorities

### 3. Dynamic Analysis

ANP can handle time-dependent decisions through:
- Dynamic judgments
- Time-based supermatrices
- Evolutionary network structures

## Advantages and Limitations

### Advantages
- Captures complex interactions
- More realistic modeling
- Handles feedback relationships
- Suitable for market dynamics

### Limitations
- Complex data collection
- More difficult to explain
- Requires more judgments than AHP
- Computational complexity

## Best Practices

1. **Network Design**
   - Keep clusters manageable
   - Clearly define relationships
   - Document dependencies

2. **Judgment Collection**
   - Use expert panels
   - Maintain consistency
   - Document assumptions

3. **Analysis**
   - Verify convergence
   - Conduct sensitivity analysis
   - Validate results

## References

1. Saaty, T.L. (1996). "Decision Making with Dependence and Feedback: The Analytic Network Process." RWS Publications, Pittsburgh.

2. Saaty, T.L. (2001). "Decision Making with the Analytic Network Process (ANP) and Its 'Super-Decisions' Software." ISAHP 2001 Proceedings, Bern, Switzerland.

3. Saaty, T.L., & Vargas, L.G. (2013). "Decision Making with the Analytic Network Process: Economic, Political, Social and Technological Applications with Benefits, Opportunities, Costs and Risks." Springer.

4. Saaty, T.L. (2004). "Fundamentals of the Analytic Network Process — Multiple Networks with Benefits, Costs, Opportunities and Risks." Journal of Systems Science and Systems Engineering, 13(3), 348-379.