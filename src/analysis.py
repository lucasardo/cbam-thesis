"""
Analysis module for CBAM Risk Assessment
Handles risk index calculation, sensitivity analysis, and summary statistics.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
import logging

from .config import WEIGHT_SCENARIOS

logger = logging.getLogger(__name__)


class RiskAnalyzer:
    """Class for calculating and analyzing CBAM risk indices."""
    
    def __init__(self):
        """Initialize RiskAnalyzer."""
        pass
    
    def calculate_weighted_index(self,
                                 df: pd.DataFrame,
                                 weights: Dict[str, float],
                                 index_name: str = "WeightedSum") -> pd.DataFrame:
        """
        Calculate weighted risk index.
        
        Args:
            df: Input DataFrame with normalized columns
            weights: Dictionary mapping column names to weights
            index_name: Name for the resulting index column
            
        Returns:
            DataFrame with new weighted index column
        """
        df = df.copy()
        
        # Validate weights
        missing_cols = set(weights.keys()) - set(df.columns)
        if missing_cols:
            logger.warning(f"Columns not found in DataFrame: {missing_cols}")
        
        # Calculate weighted sum
        df[index_name] = 0
        for col, weight in weights.items():
            if col in df.columns:
                df[index_name] += df[col] * weight
        
        logger.info(f"Calculated {index_name} using {len(weights)} components")
        return df
    
    def run_sensitivity_analysis(self,
                                 df: pd.DataFrame,
                                 scenarios: Optional[Dict[str, Dict[str, float]]] = None) -> pd.DataFrame:
        """
        Run sensitivity analysis with multiple weight scenarios.
        
        Args:
            df: Input DataFrame with normalized columns
            scenarios: Dictionary of scenario names to weight dictionaries
                      (defaults to WEIGHT_SCENARIOS from config)
            
        Returns:
            DataFrame with multiple risk index columns
        """
        if scenarios is None:
            scenarios = WEIGHT_SCENARIOS
        
        df_result = df.copy()
        
        for scenario_name, weights in scenarios.items():
            index_name = f"Index_{scenario_name}"
            df_result = self.calculate_weighted_index(
                df_result, weights, index_name
            )
        
        logger.info(f"Completed sensitivity analysis with {len(scenarios)} scenarios")
        return df_result
    
    def rank_countries(self,
                      df: pd.DataFrame,
                      index_col: str,
                      country_col: str = "Country Name",
                      ascending: bool = False) -> pd.DataFrame:
        """
        Rank countries by risk index and add rank column.
        
        Args:
            df: Input DataFrame
            index_col: Column containing the risk index
            country_col: Column containing country names
            ascending: Sort order (False = highest risk first)
            
        Returns:
            Sorted DataFrame with Rank column
        """
        df_ranked = df.copy()
        df_ranked = df_ranked.sort_values(by=index_col, ascending=ascending)
        df_ranked['Rank'] = range(1, len(df_ranked) + 1)
        
        logger.info(f"Ranked countries by {index_col}")
        return df_ranked
    
    def categorize_risk(self,
                       df: pd.DataFrame,
                       index_col: str,
                       thresholds: Optional[Dict[str, float]] = None) -> pd.DataFrame:
        """
        Categorize countries into risk levels.
        
        Args:
            df: Input DataFrame
            index_col: Column containing the risk index
            thresholds: Dictionary of category names to threshold values
                       (e.g., {'Low': 0.33, 'Medium': 0.66, 'High': 1.0})
            
        Returns:
            DataFrame with RiskCategory column
        """
        if thresholds is None:
            # Default to quartile-based categorization
            thresholds = {
                'Low': df[index_col].quantile(0.33),
                'Medium': df[index_col].quantile(0.66),
                'High': df[index_col].max()
            }
        
        df_cat = df.copy()
        
        def categorize(value):
            if pd.isna(value):
                return 'Unknown'
            for category, threshold in sorted(thresholds.items(), 
                                            key=lambda x: x[1]):
                if value <= threshold:
                    return category
            return list(thresholds.keys())[-1]
        
        df_cat['RiskCategory'] = df_cat[index_col].apply(categorize)
        
        logger.info(f"Categorized countries into risk levels")
        return df_cat
    
    def get_summary_statistics(self,
                              df: pd.DataFrame,
                              index_col: str) -> pd.Series:
        """
        Get summary statistics for a risk index.
        
        Args:
            df: Input DataFrame
            index_col: Column containing the risk index
            
        Returns:
            Series with summary statistics
        """
        stats = df[index_col].describe()
        logger.info(f"Summary statistics for {index_col}:\n{stats}")
        return stats
    
    def compare_scenarios(self,
                         df: pd.DataFrame,
                         scenario_cols: List[str],
                         country_col: str = "Country Name",
                         top_n: int = 10) -> pd.DataFrame:
        """
        Compare rankings across different scenarios.
        
        Args:
            df: DataFrame with multiple scenario columns
            scenario_cols: List of scenario column names
            country_col: Column with country names
            top_n: Number of top countries to include
            
        Returns:
            DataFrame with country rankings for each scenario
        """
        comparison = pd.DataFrame()
        comparison[country_col] = df[country_col]
        
        for col in scenario_cols:
            if col in df.columns:
                # Calculate rank for this scenario
                ranks = df[col].rank(ascending=False, method='min')
                comparison[f"{col}_Rank"] = ranks
        
        # Filter to top N countries (lowest average rank)
        rank_cols = [c for c in comparison.columns if c.endswith('_Rank')]
        comparison['AvgRank'] = comparison[rank_cols].mean(axis=1)
        comparison = comparison.sort_values('AvgRank').head(top_n)
        
        logger.info(f"Compared {len(scenario_cols)} scenarios for top {top_n} countries")
        return comparison
    
    def identify_risk_drivers(self,
                             df: pd.DataFrame,
                             country: str,
                             component_cols: List[str],
                             country_col: str = "Country Name") -> pd.Series:
        """
        Identify the main risk drivers for a specific country.
        
        Args:
            df: Input DataFrame
            country: Country name to analyze
            component_cols: List of component columns (normalized metrics)
            country_col: Column containing country names
            
        Returns:
            Series with component values for the country
        """
        country_data = df[df[country_col] == country]
        
        if country_data.empty:
            logger.warning(f"Country not found: {country}")
            return pd.Series()
        
        existing_cols = [col for col in component_cols if col in df.columns]
        drivers = country_data[existing_cols].iloc[0].sort_values(ascending=False)
        
        logger.info(f"Risk drivers for {country}:\n{drivers}")
        return drivers
    
    def calculate_correlation_matrix(self,
                                    df: pd.DataFrame,
                                    columns: List[str]) -> pd.DataFrame:
        """
        Calculate correlation matrix for risk components.
        
        Args:
            df: Input DataFrame
            columns: List of columns to include
            
        Returns:
            Correlation matrix
        """
        existing_cols = [col for col in columns if col in df.columns]
        corr_matrix = df[existing_cols].corr()
        
        logger.info("Calculated correlation matrix")
        return corr_matrix
    
    def generate_risk_report(self,
                            df: pd.DataFrame,
                            index_col: str,
                            country_col: str = "Country Name",
                            top_n: int = 5,
                            bottom_n: int = 5) -> Dict[str, Any]:
        """
        Generate a comprehensive risk report.
        
        Args:
            df: Input DataFrame with risk index
            index_col: Column containing the risk index
            country_col: Column with country names
            top_n: Number of highest risk countries to include
            bottom_n: Number of lowest risk countries to include
            
        Returns:
            Dictionary containing report components
        """
        df_sorted = df.sort_values(by=index_col, ascending=False)
        
        report = {
            'summary_stats': self.get_summary_statistics(df, index_col),
            'highest_risk': df_sorted[[country_col, index_col]].head(top_n),
            'lowest_risk': df_sorted[[country_col, index_col]].tail(bottom_n),
            'mean_risk': df[index_col].mean(),
            'median_risk': df[index_col].median(),
            'total_countries': len(df)
        }
        
        logger.info("Generated comprehensive risk report")
        return report
    
    def export_results(self,
                      df: pd.DataFrame,
                      output_path: str,
                      sheet_name: str = "Risk Analysis") -> None:
        """
        Export analysis results to Excel file.
        
        Args:
            df: DataFrame to export
            output_path: Path to output file
            sheet_name: Name of Excel sheet
        """
        df.to_excel(output_path, sheet_name=sheet_name, index=False)
        logger.info(f"Exported results to {output_path}")
