# Chart Builder Component

## Goal

Build a `@ui.component` that takes a Deephaven table as input and provides a UI for users to interactively configure and build charts using `deephaven.plot.express` (dx). The component should dynamically show/hide options based on the selected chart type.

## Features

- Select chart type from a dropdown
- Dynamically display options relevant to the selected chart type
- Column selectors populated from the input table's schema
- Live preview of the chart as options are changed
- Testable `make_chart` function that takes a configuration dict and returns a chart

## Chart Types (Full List)

### Basic Plots

1. **scatter** - Scatter plot (x, y, optional: by, size, symbol, color)
2. **line** - Line plot (x, y, optional: by, markers, line_shape)
3. **bar** - Bar chart (x, y, optional: by, orientation)
4. **area** - Area chart (x, y, optional: by)
5. **pie** - Pie chart (names, values)

### 1D Distribution Plots

6. **histogram** - Histogram (x or y, optional: by, nbins)
7. **box** - Box plot (x, y, optional: by)
8. **violin** - Violin plot (x, y, optional: by)
9. **strip** - Strip plot (x, y, optional: by)

### 2D Distribution Plots

10. **density_heatmap** - Density heatmap (x, y)

### Financial Plots

11. **candlestick** - Candlestick (x, open, high, low, close)
12. **ohlc** - OHLC chart (x, open, high, low, close)

### Hierarchical Plots

13. **treemap** - Treemap (names, values, parents)
14. **sunburst** - Sunburst (names, values, parents)
15. **funnel** - Funnel (x, y)
16. **funnel_area** - Funnel area (names, values)
17. **icicle** - Icicle (names, values, parents)

### 3D/Polar/Ternary Plots

18. **scatter_3d** - 3D scatter (x, y, z)
19. **line_3d** - 3D line (x, y, z)
20. **scatter_polar** - Polar scatter (r, theta)
21. **line_polar** - Polar line (r, theta)
22. **scatter_ternary** - Ternary scatter (a, b, c)
23. **line_ternary** - Ternary line (a, b, c)

### Map/Geo Plots

24. **scatter_geo** - Geographic scatter on world map (lat, lon, optional: locations, color, size, symbol)
25. **line_geo** - Geographic lines on world map (lat, lon, optional: locations, color, width)
26. **scatter_map** - Scatter on tile-based map (lat, lon, optional: color, size, symbol)
27. **line_map** - Lines on tile-based map (lat, lon, optional: color, width)
28. **density_map** - Density heatmap on tile-based map (lat, lon, optional: z, radius)

### Other

29. **timeline** - Timeline/Gantt (x_start, x_end, y)

## Implementation Phases

### Phase 1: Core Infrastructure (scatter, line)

- Create `make_chart` function with typed config dataclass/TypedDict
- Implement scatter and line chart support
- Create basic `chart_builder` component with chart type selection
- Dynamic column pickers for x, y
- Unit tests for `make_chart`
- E2E tests for scatter and line

### Phase 2: Basic Plots (bar, area, pie)

- Add bar, area, pie chart types
- Handle orientation options for bar
- Handle names/values pattern for pie

### Phase 3: Distribution Plots (histogram, box, violin, strip, density_heatmap)

- Add 1D distribution plots
- Add density_heatmap
- Handle histogram-specific options (nbins)

### Phase 4: Financial Plots (candlestick, ohlc)

- Add OHLC-style plots
- Handle open/high/low/close column requirements

### Phase 5: Hierarchical Plots (treemap, sunburst, funnel, funnel_area, icicle)

- Add hierarchical plot types
- Handle names/values/parents pattern

### Phase 6: 3D/Polar/Ternary (scatter_3d, line_3d, scatter_polar, line_polar, scatter_ternary, line_ternary, timeline)

- Add remaining plot types
- Handle coordinate system-specific parameters

### Phase 7: Map/Geo Plots (scatter_geo, line_geo, scatter_map, line_map, density_map)

- Add geographic/map plot types
- **scatter_geo**: World map scatter plot using lat/lon or location codes
  - Required: `lat` + `lon` OR `locations` (country codes, state codes, etc.)
  - Optional: `locationmode` ("ISO-3", "USA-states", "country names"), `color`, `size`, `symbol`, `text`
- **line_geo**: World map line plot for flight paths, routes, etc.
  - Required: `lat`, `lon`
  - Optional: `color`, `width`, `symbol`
- **scatter_map**: Tile-based map scatter (OpenStreetMap-style)
  - Required: `lat`, `lon`
  - Optional: `color`, `size`, `symbol`, `text`, `zoom`, `center`
- **line_map**: Tile-based map lines for routes/paths
  - Required: `lat`, `lon`
  - Optional: `color`, `width`, `line_dash`
- **density_map**: Tile-based density/heat map
  - Required: `lat`, `lon`
  - Optional: `z` (intensity), `radius`, `zoom`, `center`

#### New Sample Datasets

- **flights**: Flight tracking data with `Lat`, `Lon`, `FlightId`, `Origin`, `Destination`, `Speed`
  - Use with `scatter_map` or `line_map` for flight paths
  - Default center: `{"lat": 50, "lon": -100}` (North America)
- **outages**: Power outage data with `Lat`, `Lon`, `Severity`
  - Use with `scatter_map` or `density_map` for outage visualization
  - Default center: `{"lat": 44.97, "lon": -93.17}` (Minneapolis area)

#### ChartConfig Additions

```python
# Map/Geo chart options
lat: NotRequired[str]          # Latitude column
lon: NotRequired[str]          # Longitude column
locations: NotRequired[str]    # Location codes column (for scatter_geo)
locationmode: NotRequired[Literal["ISO-3", "USA-states", "country names"]]
radius: NotRequired[int]       # Density map radius
zoom: NotRequired[int]         # Map zoom level (for tile-based maps)
center: NotRequired[dict]      # Map center {"lat": float, "lon": float}
```

#### UI Controls for Map Charts

- Lat/Lon column pickers (required for all map types)
- Location column picker + locationmode dropdown (scatter_geo only)
- Size, color, symbol pickers (scatter types)
- Width picker (line types)
- Radius slider (density_map)
- Zoom level control (tile-based maps)
- Optional center lat/lon inputs

### Phase 8: Code Generation

Display a copyable Python code block below the chart that shows the exact code needed to recreate the current chart configuration.

#### Features

- Generate `deephaven.plot.express` code based on current selections
- Display code in a `ui.markdown` component with syntax highlighting
- Include a copy button for easy copying to clipboard
- Update in real-time as user changes options
- Handle all chart types and their specific options

#### Implementation Details

1. **Code Generation Function**

   - Create `_generate_chart_code(config: ChartConfig, dataset_name: str) -> str`
   - Build the appropriate `dx.<chart_type>()` call with all set parameters
   - Include dataset loading code (e.g., `table = dx.data.iris()`)
   - Format code nicely with proper indentation for readability
   - Omit parameters that are empty/default values

2. **UI Component**

   - Add a section below the chart for generated code
   - Use `ui.markdown` with fenced code block for syntax highlighting
   - Add a "Copy" action button using `ui.action_button`
   - Consider making the section collapsible to save space

3. **Code Format Example**

   ```python
   from deephaven.plot import express as dx

   # Load dataset
   table = dx.data.iris()

   # Create chart
   chart = dx.scatter(
       table,
       x="SepalLength",
       y="SepalWidth",
       color="Species",
       title="Iris Scatter Plot",
   )
   ```

4. **Edge Cases to Handle**
   - Custom datasets (ohlc_sample, hierarchy_sample, etc.) need their creation code or a comment placeholder
   - List values (like `by` with multiple columns) need proper formatting
   - Map center dict needs proper formatting `{"lat": 44.97, "lon": -93.17}`
   - Show code even when configuration is incomplete (helps user understand what's needed)

### Phase 9: Advanced Parameters - Scatter/Line Charts

Expose ALL available parameters for scatter and line chart types with commonly-used options in the main UI and advanced/obscure options in a collapsible "Advanced" section.

#### Goals

- Provide complete control over every parameter supported by `dx.scatter()` and `dx.line()`
- Maintain a clean UI by hiding advanced options in a collapsible section
- Serve as a template for adding advanced parameters to other chart types in future phases

#### Scatter Chart Parameters (dx.scatter)

**Currently Implemented (Basic)**:

- `x`, `y` - Axis columns
- `by` - Grouping column
- `size` - Size column
- `symbol` - Symbol column
- `color` - Color column
- `title` - Chart title
- `opacity` - Marker opacity
- `log_x`, `log_y` - Log scale axes

**New Basic Parameters**:

- `text` - Text labels column
- `hover_name` - Hover tooltip name column

**New Advanced Parameters** (in collapsible section):

- Error bars:
  - `error_x` - X error bar column
  - `error_x_minus` - X error bar minus column
  - `error_y` - Y error bar column
  - `error_y_minus` - Y error bar minus column
- Design mappings:
  - `color_discrete_sequence` - Custom color palette
  - `color_discrete_map` - Map specific values to colors
  - `symbol_sequence` - Custom symbol sequence
  - `symbol_map` - Map specific values to symbols
  - `size_sequence` - Custom size sequence
  - `size_map` - Map specific values to sizes
- Continuous color options:
  - `color_continuous_scale` - Color scale for continuous color
  - `range_color` - Fixed color range [min, max]
  - `color_continuous_midpoint` - Midpoint for diverging scales
- Axis configuration:
  - `xaxis_sequence` - Assign series to multiple x axes
  - `yaxis_sequence` - Assign series to multiple y axes
  - `range_x` - Fixed x-axis range
  - `range_y` - Fixed y-axis range
  - `xaxis_titles` - X axis titles
  - `yaxis_titles` - Y axis titles
- Marginal plots:
  - `marginal_x` - Marginal plot type for x axis (histogram, box, violin, rug)
  - `marginal_y` - Marginal plot type for y axis
- Labels:
  - `labels` - Dict to rename columns in legends/tooltips
- Rendering:
  - `template` - Plotly template name
  - `render_mode` - "webgl" or "svg"
  - `calendar` - Business calendar for time axes

#### Line Chart Parameters (dx.line)

**Currently Implemented (Basic)**:

- `x`, `y` - Axis columns
- `by` - Grouping column
- `markers` - Show markers on line
- `line_shape` - Line interpolation shape
- `title` - Chart title
- `log_x`, `log_y` - Log scale axes

**New Basic Parameters**:

- `size` - Line marker size column
- `line_dash` - Line dash pattern column
- `width` - Line width column
- `color` - Line color column
- `symbol` - Marker symbol column
- `text` - Text labels column
- `hover_name` - Hover tooltip name column

**New Advanced Parameters** (in collapsible section):

- Error bars:
  - `error_x` - X error bar column
  - `error_x_minus` - X error bar minus column
  - `error_y` - Y error bar column
  - `error_y_minus` - Y error bar minus column
- Design mappings:
  - `color_discrete_sequence` - Custom color palette
  - `color_discrete_map` - Map specific values to colors
  - `line_dash_sequence` - Custom dash pattern sequence
  - `line_dash_map` - Map specific values to dash patterns
  - `symbol_sequence` - Custom symbol sequence
  - `symbol_map` - Map specific values to symbols
  - `size_sequence` - Custom size sequence
  - `size_map` - Map specific values to sizes
  - `width_sequence` - Custom width sequence
  - `width_map` - Map specific values to widths
- Axis configuration:
  - `xaxis_sequence` - Assign series to multiple x axes
  - `yaxis_sequence` - Assign series to multiple y axes
  - `range_x` - Fixed x-axis range
  - `range_y` - Fixed y-axis range
  - `xaxis_titles` - X axis titles
  - `yaxis_titles` - Y axis titles
- Labels:
  - `labels` - Dict to rename columns in legends/tooltips
- Rendering:
  - `template` - Plotly template name
  - `render_mode` - "webgl" or "svg"
  - `calendar` - Business calendar for time axes

#### ChartConfig Additions

```python
class ChartConfig(TypedDict):
    # ... existing fields ...

    # Text and hover
    text: NotRequired[str]
    hover_name: NotRequired[str]

    # Error bars
    error_x: NotRequired[str]
    error_x_minus: NotRequired[str]
    error_y: NotRequired[str]
    error_y_minus: NotRequired[str]

    # Design mappings (string-based for simplicity)
    color_discrete_sequence: NotRequired[list[str]]
    symbol_sequence: NotRequired[list[str]]
    size_sequence: NotRequired[list[int]]
    line_dash_sequence: NotRequired[list[str]]  # line only
    width_sequence: NotRequired[list[int]]  # line only

    # Continuous color
    color_continuous_scale: NotRequired[list[str]]
    range_color: NotRequired[list[float]]
    color_continuous_midpoint: NotRequired[float]

    # Axis ranges
    range_x: NotRequired[list[int | float]]
    range_y: NotRequired[list[int | float]]
    xaxis_titles: NotRequired[list[str] | str]
    yaxis_titles: NotRequired[list[str] | str]

    # Marginal plots (scatter only)
    marginal_x: NotRequired[Literal["histogram", "box", "violin", "rug"]]
    marginal_y: NotRequired[Literal["histogram", "box", "violin", "rug"]]

    # Line-specific
    line_dash: NotRequired[str]  # column name
    width: NotRequired[str]  # column name

    # Labels dict (for renaming in tooltips/legends)
    labels: NotRequired[dict[str, str]]

    # Rendering
    template: NotRequired[str]
    render_mode: NotRequired[Literal["webgl", "svg"]]
```

#### UI Design

The UI will be organized into sections:

```
┌─────────────────────────────────────────────────────────────┐
│  [Dataset ▼]  [Chart Type: Scatter ▼]                       │
├─────────────────────────────────────────────────────────────┤
│  Data Mapping                                                │
│  [X Column ▼]  [Y Column ▼]  [Group By ▼]                   │
├─────────────────────────────────────────────────────────────┤
│  Appearance                                                  │
│  [Size ▼]  [Symbol ▼]  [Color ▼]  [Text ▼]                 │
│  [Opacity: ____]  [Hover Name ▼]                            │
├─────────────────────────────────────────────────────────────┤
│  ▶ Advanced Options (click to expand)                       │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Error Bars                                             │  │
│  │ [Error X ▼] [Error X- ▼] [Error Y ▼] [Error Y- ▼]    │  │
│  │                                                        │  │
│  │ Axis Configuration                                     │  │
│  │ [Log X ☐] [Log Y ☐]                                   │  │
│  │ Range X: [min] to [max]                               │  │
│  │ Range Y: [min] to [max]                               │  │
│  │ X Axis Title: [____]  Y Axis Title: [____]            │  │
│  │                                                        │  │
│  │ Marginal Plots                                         │  │
│  │ [Marginal X ▼]  [Marginal Y ▼]                        │  │
│  │                                                        │  │
│  │ Rendering                                              │  │
│  │ [Render Mode ▼]  [Template ▼]                         │  │
│  └───────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                    [CHART VISUALIZATION]                     │
├─────────────────────────────────────────────────────────────┤
│  📋 Generated Code                              [Copy]       │
└─────────────────────────────────────────────────────────────┘
```

#### Implementation Steps

1. **Update ChartConfig** - Add all new fields to the TypedDict
2. **Update make_chart** - Pass all new parameters to dx.scatter/dx.line
3. **Update generate_chart_code** - Include new parameters in generated code
4. **Create Advanced Section UI** - Build collapsible panel with grouped options
5. **Add State Variables** - Add useState for each new parameter
6. **Wire Up Controls** - Connect UI controls to state and config
7. **Unit Tests** - Test make_chart with advanced parameters
8. **Update README** - Document new advanced options

#### Completed Phases

- **Phase 10**: ✅ Advanced Parameters - Bar/Area/Pie Charts (barmode, hole, text_auto, opacity, error bars, log axes, templates)
- **Phase 11**: ✅ Advanced Parameters - Distribution Charts (histogram, box, violin, strip)
  - Histogram: histfunc, histnorm, barnorm, barmode, cumulative, nbins
  - Box: boxmode, points, notched
  - Violin: violinmode, points, box (inner box)
  - Strip: stripmode
  - All: log_x, log_y, template
- **Phase 12**: ✅ Advanced Parameters - Financial Charts (candlestick, ohlc)

  - increasing_color_sequence: Custom color for up candles/bars (with color picker UI)
  - decreasing_color_sequence: Custom color for down candles/bars (with color picker UI)
  - Note: xaxis_titles/yaxis_titles are NOT supported due to a bug in dx.candlestick/dx.ohlc

- **Phase 13**: ✅ Advanced Parameters - Hierarchical Charts (treemap, sunburst, icicle, funnel, funnel_area)
  - **treemap/sunburst/icicle** (shared params):
    - `color`: Color column for categorical or continuous coloring
    - `branchvalues`: "total" (value includes descendants) or "remainder" (value is remainder after subtracting children)
    - `maxdepth`: Maximum number of visible hierarchy levels (-1 for all)
    - `template`: Plotly template
  - **funnel**:
    - `color`: Color column
    - `text`: Text labels column
    - `orientation`: "v" (vertical) or "h" (horizontal)
    - `template`: Plotly template
  - **funnel_area**:
    - `color`: Color column
    - `template`: Plotly template
  - Note: opacity, log_x, log_y omitted (less commonly used)

#### Future Phases (Planned)

- **Phase 14**: Advanced Parameters - 3D/Polar/Ternary Charts
- **Phase 15**: Advanced Parameters - Map/Geo Charts

#### UI Layout Update

```
┌─────────────────────────────────────────────────────────────┐
│  [Dataset ▼]  [Chart Type ▼]  [X Column ▼]  [Y Column ▼]    │
│  ... other options ...                                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│                    [CHART VISUALIZATION]                     │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  📋 Generated Code                              [Copy]       │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ from deephaven.plot import express as dx                ││
│  │                                                         ││
│  │ table = dx.data.iris()                                  ││
│  │ chart = dx.scatter(table, x="SepalLength", ...)         ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## Configuration Data Structure

```python
from typing import TypedDict, Literal, NotRequired

class ChartConfig(TypedDict):
    """Configuration for chart creation."""
    chart_type: Literal[
        "scatter", "line", "bar", "area", "pie",
        "histogram", "box", "violin", "strip", "density_heatmap",
        "candlestick", "ohlc",
        "treemap", "sunburst", "funnel", "funnel_area", "icicle",
        "scatter_3d", "line_3d", "scatter_polar", "line_polar",
        "scatter_ternary", "line_ternary", "timeline",
        "scatter_geo", "line_geo", "scatter_map", "line_map", "density_map"
    ]

    # Common options
    x: NotRequired[str]
    y: NotRequired[str]
    by: NotRequired[str]
    title: NotRequired[str]

    # Scatter/Line specific
    size: NotRequired[str]
    symbol: NotRequired[str]
    color: NotRequired[str]

    # Line specific
    markers: NotRequired[bool]
    line_shape: NotRequired[Literal["linear", "spline", "vhv", "hvh", "vh", "hv"]]

    # Bar specific
    orientation: NotRequired[Literal["v", "h"]]

    # Pie specific
    names: NotRequired[str]
    values: NotRequired[str]

    # Histogram specific
    nbins: NotRequired[int]

    # OHLC/Candlestick specific
    open: NotRequired[str]
    high: NotRequired[str]
    low: NotRequired[str]
    close: NotRequired[str]

    # Hierarchical specific
    parents: NotRequired[str]

    # 3D specific
    z: NotRequired[str]

    # Polar specific
    r: NotRequired[str]
    theta: NotRequired[str]

    # Ternary specific
    a: NotRequired[str]
    b: NotRequired[str]
    c: NotRequired[str]

    # Timeline specific
    x_start: NotRequired[str]
    x_end: NotRequired[str]

    # Map/Geo specific
    lat: NotRequired[str]
    lon: NotRequired[str]
    locations: NotRequired[str]
    locationmode: NotRequired[Literal["ISO-3", "USA-states", "country names"]]
    radius: NotRequired[int]
    zoom: NotRequired[int]
    # Note: center would be dict but omitted for simplicity

    # Common styling
    log_x: NotRequired[bool]
    log_y: NotRequired[bool]
    opacity: NotRequired[float]
```

## UI Layout

```
┌─────────────────────────────────────────────────────────────┐
│ Chart Builder                                               │
├─────────────────────────────────────────────────────────────┤
│ Chart Type: [Scatter ▼]                                     │
├─────────────────────────────────────────────────────────────┤
│ Data Mapping                                                │
│ ┌─────────────────┐  ┌─────────────────┐                   │
│ │ X Column:       │  │ Y Column:       │                   │
│ │ [column1 ▼]     │  │ [column2 ▼]     │                   │
│ └─────────────────┘  └─────────────────┘                   │
├─────────────────────────────────────────────────────────────┤
│ Grouping (optional)                                         │
│ ┌─────────────────┐                                        │
│ │ Group By:       │                                        │
│ │ [None ▼]        │                                        │
│ └─────────────────┘                                        │
├─────────────────────────────────────────────────────────────┤
│ Appearance (optional)                                       │
│ ┌─────────────────┐  ┌─────────────────┐                   │
│ │ Size Column:    │  │ Symbol Column:  │                   │
│ │ [None ▼]        │  │ [None ▼]        │                   │
│ └─────────────────┘  └─────────────────┘                   │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Title: [________________]                               │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                      [CHART PREVIEW]                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## File Structure

```
examples/chart-builder/
├── PLAN.md           # This file
├── README.md         # Usage documentation
├── __init__.py       # Package init
├── app.py            # Main component demo
├── chart_builder.py  # The chart_builder component
├── make_chart.py     # The make_chart function (testable)
├── chart_config.py   # ChartConfig type definitions
├── unit/
│   ├── test_make_chart.py    # Unit tests for make_chart
│   └── test_chart_config.py  # Unit tests for config validation
└── e2e/
    └── test_e2e.py           # E2E tests for UI
```

## Dependencies

- deephaven-core
- deephaven-server
- deephaven-plugin-ui
- deephaven-plugin-plotly-express

## Key Implementation Details

### `make_chart` Function

```python
import deephaven.plot.express as dx
from deephaven.table import Table

def make_chart(table: Table, config: ChartConfig) -> DeephavenFigure:
    """Create a chart from the given table and configuration.

    Args:
        table: The source data table
        config: Chart configuration options

    Returns:
        A DeephavenFigure containing the chart

    Raises:
        ValueError: If required options are missing for the chart type
    """
    chart_type = config["chart_type"]

    # Route to appropriate chart function
    if chart_type == "scatter":
        return _make_scatter(table, config)
    elif chart_type == "line":
        return _make_line(table, config)
    # ... etc
```

### Dynamic UI Options

The component will use conditional rendering to show/hide options based on chart type:

```python
@ui.component
def chart_builder(table: Table) -> ui.Element:
    chart_type, set_chart_type = ui.use_state("scatter")
    x_col, set_x_col = ui.use_state(None)
    y_col, set_y_col = ui.use_state(None)
    # ... more state

    columns = get_column_names(table)

    # Build config from state
    config = build_config(chart_type, x_col, y_col, ...)

    # Create chart
    chart = make_chart(table, config) if config_is_valid(config) else None

    return ui.flex(
        ui.picker(label="Chart Type", ...),
        # Conditionally render x/y pickers for most chart types
        ui.picker(label="X Column", ...) if needs_x(chart_type) else None,
        ui.picker(label="Y Column", ...) if needs_y(chart_type) else None,
        # Scatter-specific options
        ui.picker(label="Size", ...) if chart_type == "scatter" else None,
        # Line-specific options
        ui.checkbox(label="Markers", ...) if chart_type == "line" else None,
        # Chart preview
        chart,
        direction="column",
    )
```

## Testing Strategy

### Unit Tests (`test_make_chart.py`)

Test the `make_chart` function in isolation:

- Test each chart type with minimal required options
- Test each chart type with all options
- Test error handling for missing required options
- Test error handling for invalid option combinations

### E2E Tests (`test_e2e.py`)

Test the UI component:

- Test chart type selection changes visible options
- Test column picker population from table schema
- Test chart renders with valid configuration
- Test each chart type produces expected output

## Notes

- Start with scatter and line to validate the architecture
- Use `ui.picker` for column selection with items from table schema
- The chart preview should update reactively as options change
- Consider debouncing chart updates for performance
- Error states should be clearly communicated to the user
