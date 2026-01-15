# Chart Builder

An interactive chart builder component for Deephaven tables.

## Screenshot

![Screenshot](screenshot.png)

## Features

- Select chart type (scatter, line)
- Choose X and Y columns from the table
- Optional grouping by a column
- Chart-type-specific options:
  - **Scatter**: Size, Symbol, Color columns
  - **Line**: Show markers, Line shape
- Live chart preview as options change

## Usage

```python
exec(open('/data/examples/chart-builder/app.py').read())
```

This creates two chart builders:

- `iris_chart_builder` - For the Iris flower dataset
- `stocks_chart_builder` - For the stocks dataset

## How It Works

The chart builder consists of three main parts:

### 1. `ChartConfig` (chart_config.py)

A TypedDict that defines all possible chart configuration options:

```python
config: ChartConfig = {
    "chart_type": "scatter",
    "x": "SepalWidth",
    "y": "SepalLength",
    "by": "Species",
    "title": "Iris Scatter Plot",
}
```

### 2. `make_chart` (make_chart.py)

A pure function that takes a table and config, returning a chart:

```python
from examples.chart_builder import make_chart

chart = make_chart(my_table, {
    "chart_type": "line",
    "x": "Timestamp",
    "y": "Price",
    "by": "Sym",
    "markers": True,
})
```

### 3. `chart_builder` (chart_builder.py)

The `@ui.component` that provides the interactive UI:

```python
from examples.chart_builder import chart_builder

my_chart_builder = chart_builder(my_table)
```

## Supported Chart Types

| Type    | Required | Optional                       |
| ------- | -------- | ------------------------------ |
| scatter | x, y     | by, size, symbol, color, title |
| line    | x, y     | by, markers, line_shape, title |

## Testing

### Unit Tests

```bash
pytest examples/chart-builder/unit/ -v
```

### E2E Tests

```bash
# Start the server
python scripts/run_example.py chart-builder

# In another terminal, run the tests
DH_PSK=<psk> pytest examples/chart-builder/e2e/ -v
```
