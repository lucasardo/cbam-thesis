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

## 📁 Output Files

Results are saved to the `results/` directory:

- `cbam_risk_analysis_results.xlsx`: Main risk index rankings
- `sensitivity_analysis_results.xlsx`: Results for all weight scenarios
- `cbam_risk_index.png`: Bar chart of risk rankings
- `sensitivity_analysis.png`: Multi-panel sensitivity comparison

## 🛠️ Development

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