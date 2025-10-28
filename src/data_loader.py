"""
Data loading module for CBAM Analysis
Handles reading and initial validation of all datasets.
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Union
import logging

from .config import DATA_DIR, DATASETS

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class DataLoader:
    """Class for loading and validating CBAM analysis datasets."""
    
    def __init__(self, data_dir: Union[str, Path] = DATA_DIR):
        """
        Initialize DataLoader.
        
        Args:
            data_dir: Path to the directory containing datasets
        """
        self.data_dir = Path(data_dir)
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {self.data_dir}")
    
    def load_dataset(self, dataset_key: str, **kwargs) -> pd.DataFrame:
        """
        Load a dataset by its key.
        
        Args:
            dataset_key: Key from DATASETS configuration
            **kwargs: Additional arguments passed to pd.read_csv
            
        Returns:
            Loaded DataFrame
            
        Raises:
            KeyError: If dataset_key is not found
            FileNotFoundError: If file doesn't exist
        """
        if dataset_key not in DATASETS:
            raise KeyError(f"Unknown dataset key: {dataset_key}. "
                         f"Available keys: {list(DATASETS.keys())}")
        
        filename = DATASETS[dataset_key]
        filepath = self.data_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Dataset file not found: {filepath}")
        
        logger.info(f"Loading {dataset_key} from {filepath}")
        df = pd.read_csv(filepath, **kwargs)
        logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
        
        return df
    
    def load_cbam_exports(self) -> pd.DataFrame:
        """Load CBAM exports dataset."""
        return self.load_dataset("cbam_exports")
    
    def load_gdp(self) -> pd.DataFrame:
        """Load GDP dataset."""
        return self.load_dataset("gdp")
    
    def load_total_exports(self) -> pd.DataFrame:
        """Load total exports dataset."""
        return self.load_dataset("total_exports")
    
    def load_carbon_intensity(self) -> pd.DataFrame:
        """Load carbon intensity dataset."""
        return self.load_dataset("carbon_intensity")
    
    def load_spi(self) -> pd.DataFrame:
        """Load Statistical Performance Indicator dataset."""
        return self.load_dataset("spi")
    
    def load_patents(self) -> pd.DataFrame:
        """Load patent applications dataset."""
        return self.load_dataset("patents")
    
    def load_population(self) -> pd.DataFrame:
        """Load population dataset."""
        return self.load_dataset("population")
    
    def load_trade_elasticity(self) -> pd.DataFrame:
        """Load trade elasticity dataset."""
        return self.load_dataset("trade_elasticity")
    
    def load_all(self) -> dict[str, pd.DataFrame]:
        """
        Load all datasets at once.
        
        Returns:
            Dictionary mapping dataset keys to DataFrames
        """
        logger.info("Loading all datasets...")
        datasets = {}
        
        for key in DATASETS.keys():
            try:
                datasets[key] = self.load_dataset(key)
            except Exception as e:
                logger.error(f"Failed to load {key}: {e}")
                raise
        
        logger.info(f"Successfully loaded {len(datasets)} datasets")
        return datasets


def validate_dataset(df: pd.DataFrame, 
                     required_columns: Optional[list[str]] = None,
                     name: str = "Dataset") -> bool:
    """
    Validate a dataset for common issues.
    
    Args:
        df: DataFrame to validate
        required_columns: List of columns that must be present
        name: Name of dataset for logging
        
    Returns:
        True if validation passes
        
    Raises:
        ValueError: If validation fails
    """
    if df is None or df.empty:
        raise ValueError(f"{name} is empty or None")
    
    if required_columns:
        missing = set(required_columns) - set(df.columns)
        if missing:
            raise ValueError(f"{name} missing required columns: {missing}")
    
    # Check for suspicious patterns
    null_pct = df.isnull().sum().sum() / (len(df) * len(df.columns))
    if null_pct > 0.5:
        logger.warning(f"{name} has {null_pct:.1%} null values")
    
    logger.info(f"{name} validation passed: {df.shape}")
    return True
