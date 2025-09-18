# SaatyPy Usage Guide

This guide provides step-by-step instructions for using SaatyPy for AHP and ANP decision modeling.

## Installation
```bash
pip install saatypy
```

## AHP Example
```python
from saatypy.ahp import AHPBuilder

model = (AHPBuilder()
    .add_criteria(["price", "quality", "service"])
    .add_alternatives(["A", "B", "C"])
    .build())

model.set_criteria_weights({"price": 0.5, "quality": 0.3, "service": 0.2})
for crit in ["price", "quality", "service"]:
    model.set_alt_priorities(crit, {
        ("A", "B"): 2.0,
        ("A", "C"): 3.0,
        ("B", "C"): 1.5
    })

priorities, labels = model.alternative_priorities()
print(dict(zip(labels, priorities)))
```

### Hierarchical AHP
```python
model = (AHPBuilder()
    .add_criteria_groups({
        "technical": ["performance", "reliability"],
        "economic": ["price", "maintenance"],
        "user": ["battery", "portability"]
    })
    .add_alternatives(["A", "B", "C"])
    .build())

model.set_group_weights({"technical": 0.5, "economic": 0.3, "user": 0.2})
model.set_subcriteria_weights("technical", {"performance": 0.7, "reliability": 0.3})
# ... set other subcriteria and alternative priorities ...
```

## ANP Example
```python
from saatypy.anp import ANPBuilder
from saatypy.components.pairwise import PairwiseComparison

model = (ANPBuilder()
    .add_cluster("criteria", ["C1", "C2"])
    .add_alternatives(["A", "B"])
    .build())

model.set_cluster_weights({"criteria": 0.6, "Alternatives": 0.4})

block_alt_given_crit = {
    "C1": PairwiseComparison.from_judgments(["A", "B"], {("A", "B"): 4.0}),
    "C2": PairwiseComparison.from_judgments(["A", "B"], {("A", "B"): 3.0/7.0}),
}
model.add_block("Alternatives", "criteria", block_alt_given_crit)
model.add_block_uniform("criteria", "criteria")

priorities, labels = model.alternative_priorities()
print(dict(zip(labels, priorities)))
```

### Custom Limiters
```python
from saatypy.components.math.limiters import DampedPowerLimiter
model.limiter = DampedPowerLimiter(damping=0.1)
```

## Error Handling
SaatyPy provides detailed error messages for invalid inputs, missing weights, and matrix inconsistencies.
```python
from saatypy.ahp import AHPBuilder
from saatypy.components.errors import NormalizationError

model = AHPBuilder().add_criteria(["A", "B"]).add_alternatives(["X", "Y"]).build()
try:
    model.set_criteria_weights({"invalid": 1.0})
except NormalizationError as e:
    print("Error:", e)
```

## Reporting
Extract results directly from your model:
```python
report = model.to_report_data()
print(report["criteria_weights"])
print(report["global_priorities"])
print(report["ranking_str"])
```

## Saving Reports
You can save a formatted report for any model using the `ReportManager`:

```python
from saatypy.reporting.report import ReportManager, PlainRenderer

manager = ReportManager()  # Markdown by default
report_path = manager.save(model)  # model can be AHPModel or ANPModel
print(f"Report saved to: {report_path}")

# Save as plain text
manager = ReportManager(renderer=PlainRenderer())
report_path = manager.save(model, path="my_report.txt")
```

- By default, reports are saved in Markdown format to the `reports/` directory.
- You can specify a custom path, file name, or renderer.
- The filename will include a timestamp unless you set `add_timestamp=False`.

## Extending SaatyPy
- Add new adapters for custom reporting
- Use math utilities for normalization and consistency checks
- Integrate with other Python data science tools

## API Highlights
- `AHPBuilder`, `ANPBuilder`: Model construction
- `PairwiseComparison`: Matrix creation and consistency
- `normalize_vector_nonneg`, `normalize_columns_inplace`: Math utilities
- `generate_ahp_report`, `generate_anp_report`: Reporting

## More Information
- [AHP Guide](ahp.md)
- [ANP Guide](anp.md)
- [API Reference](../src/saatypy)
