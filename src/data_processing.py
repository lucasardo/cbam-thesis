"""
Data processing module for CBAM Analysis
Handles cleaning, transformation, merging, and feature engineering.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from typing import List, Optional, Dict
import logging

from .config import (
    COMTRADE_COLUMNS_TO_REMOVE,
    COLUMN_RENAMES,
    CONVERSION_FACTORS,
    PATENT_YEARS,
    ANALYSIS_COLUMNS
)

logger = logging.getLogger(__name__)


class DataProcessor:
    """Class for processing and transforming CBAM analysis data."""
    
    def __init__(self):
        """Initialize DataProcessor."""
        self.scaler = MinMaxScaler()
    
    def clean_comtrade_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean UN Comtrade datasets by removing unnecessary columns.
        
        Args:
            df: Raw Comtrade DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        # Remove columns that exist in the dataframe
        cols_to_drop = [col for col in COMTRADE_COLUMNS_TO_REMOVE if col in df.columns]
        df_clean = df.drop(columns=cols_to_drop)
        
        logger.info(f"Cleaned Comtrade data: {len(df.columns)} -> {len(df_clean.columns)} columns")
        return df_clean
    
    def convert_to_millions(self, df: pd.DataFrame, 
                           column: str, 
                           new_column: Optional[str] = None,
                           drop_original: bool = True) -> pd.DataFrame:
        """
        Convert a column to millions.
        
        Args:
            df: Input DataFrame
            column: Column to convert
            new_column: Name for new column (defaults to column + " (millions)")
            drop_original: Whether to drop the original column
            
        Returns:
            DataFrame with converted column
        """
        if new_column is None:
            new_column = f"{column} (millions)"
        
        df = df.copy()
        df[new_column] = df[column] / CONVERSION_FACTORS["to_millions"]
        
        if drop_original:
            df = df.drop(columns=[column])
        
        return df
    
    def prepare_cbam_exports(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare CBAM exports dataset.
        
        Args:
            df: Raw CBAM exports data
            
        Returns:
            Processed DataFrame
        """
        df = self.clean_comtrade_data(df)
        df = self.convert_to_millions(df, 'PrimaryValue', 'CBAM Value (millions)')
        df = df.sort_values(by='CBAM Value (millions)', ascending=False)
        
        logger.info("CBAM exports data prepared")
        return df
    
    def prepare_total_exports(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare total exports dataset.
        
        Args:
            df: Raw total exports data
            
        Returns:
            Processed DataFrame
        """
        df = self.clean_comtrade_data(df)
        df = self.convert_to_millions(df, 'PrimaryValue', 'Total Export Value (millions)')
        
        logger.info("Total exports data prepared")
        return df
    
    def prepare_carbon_intensity(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare carbon intensity dataset.
        
        Args:
            df: Raw carbon intensity data
            
        Returns:
            Processed DataFrame
        """
        df = df.copy()
        df = df.rename(columns=COLUMN_RENAMES["carbon_intensity"])
        df = df.sort_values(by='Carbon_Intensity', ascending=False)
        
        logger.info("Carbon intensity data prepared")
        return df
    
    def prepare_spi(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare Statistical Performance Indicator dataset.
        
        Args:
            df: Raw SPI data
            
        Returns:
            Processed DataFrame
        """
        df = df.copy()
        df = df.drop(columns=['Country Name', 'Series Name', 'Series Code'], errors='ignore')
        df = df.rename(columns=COLUMN_RENAMES["spi"])
        df = df.sort_values(by='SPI_Score', ascending=False)
        
        logger.info("SPI data prepared")
        return df
    
    def prepare_patents(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare patent applications dataset.
        
        Args:
            df: Raw patent data
            
        Returns:
            Processed DataFrame with total patents 1995-2019
        """
        df = df.copy()
        
        # Sum yearly patent values
        year_columns = [str(year) for year in PATENT_YEARS]
        existing_years = [col for col in year_columns if col in df.columns]
        
        df['TotalPat_2019'] = df[existing_years].sum(axis=1)
        
        # Clean up columns
        df = df.drop(columns=existing_years + ['Origin', 'Type'], errors='ignore')
        df = df.rename(columns=COLUMN_RENAMES["patents"])
        
        logger.info("Patent data prepared")
        return df
    
    def prepare_population(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare population dataset.
        
        Args:
            df: Raw population data
            
        Returns:
            Processed DataFrame
        """
        df = df.copy()
        df = df.drop(columns=['Series Name', 'Series Code', 'Country Name'], errors='ignore')
        df = df.rename(columns=COLUMN_RENAMES["population"])
        df['Population (Hundreds of Thousands)'] = df['Population_2019'] / CONVERSION_FACTORS["to_hundred_thousands"]
        df = df.drop(columns=['Population_2019'])
        
        logger.info("Population data prepared")
        return df
    
    def prepare_trade_elasticity(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare trade elasticity dataset.
        
        Args:
            df: Raw trade elasticity data
            
        Returns:
            Processed DataFrame
        """
        df = df.copy()
        df = df.rename(columns=COLUMN_RENAMES["trade_elasticity"])
        df = df.sort_values(by='Trade_Elast', ascending=False)
        
        logger.info("Trade elasticity data prepared")
        return df
    
    def merge_cbam_gdp(self, cbam_df: pd.DataFrame, gdp_df: pd.DataFrame) -> pd.DataFrame:
        """
        Merge CBAM exports with GDP data and calculate exposure ratio.
        
        Args:
            cbam_df: CBAM exports DataFrame
            gdp_df: GDP DataFrame
            
        Returns:
            Merged DataFrame with ExpCBAMperGDP
        """
        merged = pd.merge(
            cbam_df, gdp_df,
            left_on='ReporterISO',
            right_on='Country Code',
            how='left'
        )
        merged = merged.drop(columns=['Country', 'Country Code'], errors='ignore')
        merged['ExpCBAMperGDP'] = merged['CBAM Value (millions)'] / merged['2019 GDP (Millions)']
        merged = merged.sort_values(by='ExpCBAMperGDP', ascending=False)
        
        logger.info("CBAM and GDP data merged")
        return merged
    
    def merge_cbam_total_exports(self, total_exp_df: pd.DataFrame, 
                                  cbam_df: pd.DataFrame) -> pd.DataFrame:
        """
        Merge total exports with CBAM exports and calculate percentage.
        
        Args:
            total_exp_df: Total exports DataFrame
            cbam_df: CBAM exports DataFrame
            
        Returns:
            Merged DataFrame with PctExpCBAM
        """
        merged = pd.merge(
            total_exp_df, cbam_df,
            on='ReporterISO',
            how='left'
        )
        merged['PctExpCBAM'] = merged['CBAM Value (millions)'] / merged['Total Export Value (millions)']
        merged = merged.sort_values(by='PctExpCBAM', ascending=False)
        
        logger.info("Total exports and CBAM data merged")
        return merged
    
    def merge_patents_population(self, patents_df: pd.DataFrame, 
                                  pop_df: pd.DataFrame) -> pd.DataFrame:
        """
        Merge patents with population and calculate per capita metric.
        
        Args:
            patents_df: Patents DataFrame
            pop_df: Population DataFrame
            
        Returns:
            Merged DataFrame with PatPerCap
        """
        merged = pd.merge(
            patents_df, pop_df,
            on='Country Code',
            how='left'
        )
        merged = merged.drop(columns=['Country Name'], errors='ignore')
        merged['PatPerCap'] = merged['TotalPat_2019'] / merged['Population (Hundreds of Thousands)']
        merged = merged.drop(columns=['TotalPat_2019', 'Population (Hundreds of Thousands)'])
        merged = merged.sort_values(by='PatPerCap', ascending=False)
        
        logger.info("Patents and population data merged")
        return merged
    
    def normalize_columns(self, df: pd.DataFrame, 
                         columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Normalize specified columns to [0, 1] range using MinMaxScaler.
        
        Args:
            df: Input DataFrame
            columns: List of columns to normalize (defaults to ANALYSIS_COLUMNS)
            
        Returns:
            DataFrame with normalized columns
        """
        if columns is None:
            columns = ANALYSIS_COLUMNS
        
        df = df.copy()
        existing_columns = [col for col in columns if col in df.columns]
        
        if existing_columns:
            df[existing_columns] = self.scaler.fit_transform(df[existing_columns])
            logger.info(f"Normalized {len(existing_columns)} columns")
        
        return df
    
    def create_complementary_scores(self, df: pd.DataFrame,
                                    columns: List[str]) -> pd.DataFrame:
        """
        Create complementary scores (1 - x) for columns where lower is worse.
        
        Args:
            df: Input DataFrame
            columns: List of columns to complement
            
        Returns:
            DataFrame with complementary columns added
        """
        df = df.copy()
        
        for col in columns:
            if col in df.columns:
                compl_col = f"{col}_Compl"
                df[compl_col] = 1 - df[col]
                logger.info(f"Created complementary column: {compl_col}")
        
        return df
    
    def build_comprehensive_dataset(self, datasets: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Build comprehensive dataset by merging all data sources.
        
        Args:
            datasets: Dictionary of processed DataFrames
            
        Returns:
            Comprehensive merged DataFrame
        """
        logger.info("Building comprehensive dataset...")
        
        # Merge CBAM and GDP
        cbam_gdp = self.merge_cbam_gdp(
            datasets['cbam_exports'],
            datasets['gdp']
        )
        
        # Merge total exports and CBAM
        cbam_total = self.merge_cbam_total_exports(
            datasets['total_exports'],
            datasets['cbam_exports']
        )
        
        # Merge the two export datasets
        two_dim = pd.merge(
            cbam_total, cbam_gdp,
            on='ReporterISO',
            how='left'
        )
        two_dim = two_dim.drop(columns=[
            'Total Export Value (millions)',
            'CBAM Value (millions)_x',
            '2019 GDP (Millions)',
            'CBAM Value (millions)_y'
        ], errors='ignore')
        
        # Add carbon intensity
        three_dim = pd.merge(
            datasets['carbon_intensity'], two_dim,
            left_on='Country Code',
            right_on='ReporterISO',
            how='left'
        )
        three_dim = three_dim.drop(columns=['ReporterISO'], errors='ignore')
        
        # Add SPI
        four_dim = pd.merge(
            three_dim, datasets['spi'],
            on='Country Code',
            how='left'
        )
        
        # Add patents
        patents_pop = self.merge_patents_population(
            datasets['patents'],
            datasets['population']
        )
        five_dim = pd.merge(
            four_dim, patents_pop,
            on='Country Code',
            how='left'
        )
        
        # Add trade elasticity
        six_dim = pd.merge(
            five_dim, datasets['trade_elasticity'],
            on='Country Code',
            how='left'
        )
        
        logger.info(f"Comprehensive dataset built: {six_dim.shape}")
        return six_dim
