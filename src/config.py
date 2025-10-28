"""
Configuration file for CBAM Analysis
Contains all constants, file paths, column definitions, and analysis parameters.
"""

from pathlib import Path
from typing import Dict, List

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "datasets"
RESULTS_DIR = PROJECT_ROOT / "results"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

# Dataset filenames
DATASETS = {
    "cbam_exports": "CBAM Exports 2019.csv",
    "gdp": "GDP East Asia - Pacific 2019.csv",
    "total_exports": "Total Exports 2019.csv",
    "carbon_intensity": "Carbon Intensity.csv",
    "spi": "Statistical Performance Indicator.csv",
    "patents": "Total patent applications.csv",
    "population": "Population 2019.csv",
    "trade_elasticity": "Trade elasticities.csv",
}

# Columns to remove from UN Comtrade datasets
COMTRADE_COLUMNS_TO_REMOVE = [
    'PartnerISO', 'CmdCode', 'TypeCode', 'FreqCode', 'RefPeriodId', 
    'RefYear', 'RefMonth', 'Period', 'ReporterCode', 'ReporterDesc', 
    'FlowCode', 'FlowDesc', 'PartnerCode', 'PartnerDesc', 'Partner2Code',
    'Partner2ISO', 'Partner2Desc', 'ClassificationCode',
    'ClassificationSearchCode', 'IsOriginalClassification',
    'CmdDesc', 'AggrLevel', 'IsLeaf', 'CustomsCode', 'CustomsDesc',
    'MosCode', 'MotCode', 'MotDesc', 'QtyUnitCode', 'QtyUnitAbbr', 'Qty',
    'IsQtyEstimated', 'AltQtyUnitCode', 'AltQtyUnitAbbr', 'AtlQty',
    'IsAltQtyEstimated', 'NetWgt', 'IsNetWgtEstimated', 'GrossWgt',
    'IsGrossWgtEstimated', 'Cifvalue', 'Fobvalue',
    'LegacyEstimationFlag', 'IsReported', 'IsAggregate', 'Unnamed: 47'
]

# Column rename mappings
COLUMN_RENAMES = {
    "carbon_intensity": {
        'Carbon Intensity [gCO2e]': 'Carbon_Intensity'
    },
    "spi": {
        '2019 [YR2019]': 'SPI_Score'
    },
    "patents": {
        'Office (Code)': 'Country Code',
        'Office': 'Country Name'
    },
    "population": {
        '2019 [YR2019]': 'Population_2019'
    },
    "trade_elasticity": {
        'TE': 'Trade_Elast'
    }
}

# Normalized column names for analysis
ANALYSIS_COLUMNS = [
    'Carbon_Intensity',
    'PctExpCBAM',
    'ExpCBAMperGDP',
    'SPI_Score',
    'PatPerCap',
    'Trade_Elast'
]

# Weight scenarios for sensitivity analysis
WEIGHT_SCENARIOS: Dict[str, Dict[str, float]] = {
    "baseline": {
        "ExpCBAMperGDP": 0.30,
        "PctExpCBAM": 0.14,
        "Trade_Elast": 0.14,
        "Carbon_Intensity": 0.14,
        "SPI_Score_Compl": 0.14,
        "PatPerCap_Compl": 0.14
    },
    "equal_weights": {
        "ExpCBAMperGDP": 0.166,
        "PctExpCBAM": 0.166,
        "Trade_Elast": 0.166,
        "Carbon_Intensity": 0.166,
        "SPI_Score_Compl": 0.166,
        "PatPerCap_Compl": 0.166
    },
    "export_focused": {
        "PctExpCBAM": 0.30,
        "ExpCBAMperGDP": 0.14,
        "Trade_Elast": 0.14,
        "Carbon_Intensity": 0.14,
        "SPI_Score_Compl": 0.14,
        "PatPerCap_Compl": 0.14
    },
    "no_innovation": {
        "ExpCBAMperGDP": 0.30,
        "PctExpCBAM": 0.175,
        "Trade_Elast": 0.175,
        "Carbon_Intensity": 0.175,
        "SPI_Score_Compl": 0.175
    },
    "no_trade_stat": {
        "ExpCBAMperGDP": 0.30,
        "PctExpCBAM": 0.23,
        "Carbon_Intensity": 0.23,
        "PatPerCap_Compl": 0.23
    },
    "no_trade_innovation": {
        "ExpCBAMperGDP": 0.30,
        "PctExpCBAM": 0.23,
        "Carbon_Intensity": 0.23,
        "SPI_Score_Compl": 0.23
    }
}

# Visualization settings
PLOT_STYLE = {
    "figure_size": (10, 6),
    "dpi": 100,
    "font_size": 10,
    "label_rotation": 45,
    "color_palette": "Set2"
}

# Data conversion factors
CONVERSION_FACTORS = {
    "to_millions": 1e6,
    "to_hundred_thousands": 1e5
}

# Patent data year range
PATENT_YEARS = list(range(1995, 2020))
