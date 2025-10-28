# CBAM East Asia Pacific Analysis

A comprehensive, modular framework for analyzing the impact of the EU's Carbon Border Adjustment Mechanism (CBAM) on East Asian and Pacific countries.

## 📋 Overview

This project assesses country-level vulnerability to CBAM through a multi-dimensional risk index that combines:

- **Exposure Metrics**: CBAM exports relative to GDP and total exports
- **Vulnerability Indicators**: Carbon intensity of electricity production
- **Adaptive Capacity**: Statistical performance and innovation capability
- **Economic Flexibility**: Trade elasticity measures

## 🗂️ Project Structure

```
cbam-thesis/
├── datasets/               # Raw data files (CSV)
│   ├── CBAM Exports 2019.csv
│   ├── GDP East Asia - Pacific 2019.csv
│   ├── Total Exports 2019.csv
│   ├── Carbon Intensity.csv
│   ├── Statistical Performance Indicator.csv
│   ├── Total patent applications.csv
│   ├── Population 2019.csv
│   └── Trade elasticities.csv
├── src/                    # Source code modules
│   ├── __init__.py
│   ├── config.py          # Configuration and constants
│   ├── data_loader.py     # Data loading functions
│   ├── data_processing.py # Data cleaning and transformation
│   ├── visualization.py   # Plotting functions
│   └── analysis.py        # Risk calculation and analysis
├── notebooks/              # Jupyter notebooks
│   └── CBAM_Analysis_Refactored.ipynb  # Main analysis notebook
├── results/                # Output files (Excel, plots)
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/lucasardo/cbam-thesis.git
   cd cbam-thesis
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify data files**
   Ensure all CSV files are present in the `datasets/` directory.

### Running the Analysis

#### Option 1: Using Jupyter Notebook (Recommended)

```bash
jupyter notebook notebooks/CBAM_Analysis_Refactored.ipynb
```

Run all cells to execute the complete analysis pipeline.

#### Option 2: Using Python Scripts

```python
from src.data_loader import DataLoader
from src.data_processing import DataProcessor
from src.analysis import RiskAnalyzer

# Load data
loader = DataLoader()
raw_data = loader.load_all()

# Process data
processor = DataProcessor()
processed_data = {
    'cbam_exports': processor.prepare_cbam_exports(raw_data['cbam_exports']),
    # ... process other datasets
}

# Build comprehensive dataset
comprehensive_df = processor.build_comprehensive_dataset(processed_data)

# Normalize and analyze
analysis_df = processor.normalize_columns(comprehensive_df)
analyzer = RiskAnalyzer()
results = analyzer.calculate_weighted_index(analysis_df, weights)
```

## 📊 Methodology

### Risk Index Components

The CBAM Comprehensive Risk Index combines six normalized components:

| Component | Weight | Description |
|-----------|--------|-------------|
| ExpCBAMperGDP | 30% | CBAM exports as % of GDP |
| PctExpCBAM | 14% | CBAM exports as % of total exports |
| Carbon_Intensity | 14% | Carbon intensity of electricity (gCO2e/kWh) |
| Trade_Elast | 14% | Trade elasticity measure |
| SPI_Score_Compl | 14% | Statistical Performance Indicator (complemented) |
| PatPerCap_Compl | 14% | Patents per capita (complemented) |

### Data Processing Pipeline

1. **Data Loading**: Raw CSV files loaded with validation
2. **Data Cleaning**: Remove unnecessary columns, handle missing values
3. **Data Transformation**: Calculate derived metrics, normalize units
4. **Data Merging**: Combine datasets on country identifiers
5. **Normalization**: Scale all metrics to [0, 1] range using Min-Max scaling
6. **Index Calculation**: Apply weighted sum to normalized components
7. **Sensitivity Analysis**: Test alternative weighting schemes

## 📈 Key Features

### Modular Architecture
- **Separation of Concerns**: Data loading, processing, visualization, and analysis in separate modules
- **Reusability**: Functions can be imported and used in other projects
- **Maintainability**: Easy to update individual components

### Comprehensive Analysis
- **Exploratory Data Analysis**: Visualizations for each dimension
- **Risk Index Calculation**: Weighted composite index
- **Sensitivity Analysis**: Multiple weighting scenarios
- **Risk Categorization**: Group countries by risk level
- **Driver Analysis**: Identify key risk factors per country

### Professional Visualizations
- Consistent styling across all plots
- Export-ready high-quality figures
- Interactive exploration in notebooks

## 📦 Module Documentation

### `src/config.py`
Configuration constants, file paths, and weight scenarios.

### `src/data_loader.py`
```python
loader = DataLoader()
data = loader.load_cbam_exports()  # Load specific dataset
all_data = loader.load_all()        # Load all datasets
```

### `src/data_processing.py`
```python
processor = DataProcessor()
clean_data = processor.prepare_cbam_exports(raw_data)
merged_data = processor.merge_cbam_gdp(cbam_df, gdp_df)
normalized_data = processor.normalize_columns(df)
```

### `src/visualization.py`
```python
viz = Visualizer()
viz.create_bar_chart(df, x_col='Country', y_col='Value')
viz.create_scatter_plot(df, x_col='X', y_col='Y', label_col='Country')
viz.create_risk_index_chart(df, country_col='Country', index_col='Risk')
```

### `src/analysis.py`
```python
analyzer = RiskAnalyzer()
results = analyzer.calculate_weighted_index(df, weights)
sensitivity = analyzer.run_sensitivity_analysis(df)
report = analyzer.generate_risk_report(df, index_col='Risk')
```

## 🔬 Sensitivity Analysis

The framework includes six pre-configured weighting scenarios:

1. **Baseline**: Export exposure weighted 30%
2. **Equal Weights**: All components weighted equally (16.6% each)
3. **Export Focused**: Trade proportion weighted 30%
4. **No Innovation**: Excludes innovation capacity
5. **No Trade & Stats**: Excludes trade elasticity and statistical capacity
6. **No Trade & Innovation**: Excludes trade elasticity and innovation

Add custom scenarios in `src/config.py`:

```python
WEIGHT_SCENARIOS["custom"] = {
    "ExpCBAMperGDP": 0.25,
    "PctExpCBAM": 0.25,
    # ... other components
}
```

## 📁 Output Files

Results are saved to the `results/` directory:

- `cbam_risk_analysis_results.xlsx`: Main risk index rankings
- `sensitivity_analysis_results.xlsx`: Results for all weight scenarios
- `cbam_risk_index.png`: Bar chart of risk rankings
- `sensitivity_analysis.png`: Multi-panel sensitivity comparison

## 🛠️ Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black src/
flake8 src/
```

### Adding New Datasets

1. Place CSV file in `datasets/`
2. Add entry to `DATASETS` dictionary in `src/config.py`
3. Create loading method in `DataLoader` class
4. Create processing method in `DataProcessor` class

## 📚 Data Sources

- **UN Comtrade**: Trade data (CBAM and total exports)
- **World Bank**: GDP, population, Statistical Performance Indicator
- **IEA/EMBER**: Carbon intensity of electricity
- **WIPO**: Patent applications
- **Academic literature**: Trade elasticity estimates

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Lucas Ardo**
- GitHub: [@lucasardo](https://github.com/lucasardo)

## 📝 Citation

If you use this framework in your research, please cite:

```bibtex
@software{ardo2025cbam,
  author = {Ardo, Lucas},
  title = {CBAM East Asia Pacific Analysis: A Modular Risk Assessment Framework},
  year = {2025},
  url = {https://github.com/lucasardo/cbam-thesis}
}
```

## 🔮 Future Improvements

- [ ] Add automated data updates from APIs
- [ ] Implement machine learning for risk prediction
- [ ] Create interactive dashboard with Plotly/Dash
- [ ] Add time-series analysis for trend detection
- [ ] Expand to other regions beyond East Asia & Pacific
- [ ] Include sector-specific analysis
- [ ] Add Monte Carlo simulation for uncertainty quantification

## 📞 Contact

For questions or feedback, please open an issue on GitHub or contact the author directly.

---

**Last Updated**: October 2025  
**Version**: 2.0.0
