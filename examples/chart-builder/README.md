# Chart Builder

An interactive chart builder component for Deephaven tables with support for 29 chart types.

## Screenshot

![Screenshot](screenshot.png)

## Features

- 29 chart types: scatter, line, bar, area, pie, histogram, box, violin, strip, density_heatmap, candlestick, ohlc, treemap, sunburst, icicle, funnel, funnel_area, scatter_3d, line_3d, scatter_polar, line_polar, scatter_ternary, line_ternary, timeline, scatter_geo, line_geo, scatter_map, line_map, density_map
- Choose columns from the table schema
- Multi-level grouping with "Group By"
- Chart-type-specific options with dynamic UI controls
- Live chart preview as options change
- Sample datasets including iris, stocks, tips, gapminder, elections, wind, simple, ohlc_sample, flights, outages

## Usage

```python
exec(open('/data/examples/chart-builder/app.py').read())
```

This creates:

- `chart_builder_demo` - Full chart builder with dataset selector
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

| Category | Types |
| -------- | ----- |
| Basic | scatter, line, bar, area, pie |
| Distribution | histogram, box, violin, strip, density_heatmap |
| Financial | candlestick, ohlc |
| Hierarchical | treemap, sunburst, icicle, funnel, funnel_area |
| 3D/Polar/Ternary | scatter_3d, line_3d, scatter_polar, line_polar, scatter_ternary, line_ternary |
| Map/Geo | scatter_geo, line_geo, scatter_map, line_map, density_map |
| Other | timeline |

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
