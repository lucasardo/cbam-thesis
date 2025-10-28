"""
Visualization module for CBAM Analysis
Provides reusable plotting functions with consistent styling.
"""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
from typing import Optional, Tuple, List
import logging

from .config import PLOT_STYLE

logger = logging.getLogger(__name__)


class Visualizer:
    """Class for creating consistent visualizations."""
    
    def __init__(self, style: Optional[dict] = None):
        """
        Initialize Visualizer.
        
        Args:
            style: Custom style dictionary (defaults to PLOT_STYLE from config)
        """
        self.style = style or PLOT_STYLE
        plt.rcParams['figure.dpi'] = self.style.get('dpi', 100)
        plt.rcParams['font.size'] = self.style.get('font_size', 10)
    
    def create_bar_chart(self,
                        df: pd.DataFrame,
                        x_col: str,
                        y_col: str,
                        title: Optional[str] = None,
                        xlabel: Optional[str] = None,
                        ylabel: Optional[str] = None,
                        figsize: Optional[Tuple[int, int]] = None,
                        rotation: Optional[int] = None,
                        sort_by: Optional[str] = None,
                        ascending: bool = False,
                        save_path: Optional[str] = None) -> Figure:
        """
        Create a bar chart.
        
        Args:
            df: Input DataFrame
            x_col: Column for x-axis
            y_col: Column for y-axis
            title: Chart title
            xlabel: X-axis label
            ylabel: Y-axis label
            figsize: Figure size (width, height)
            rotation: X-axis label rotation
            sort_by: Column to sort by
            ascending: Sort order
            save_path: Path to save figure
            
        Returns:
            matplotlib Figure object
        """
        if figsize is None:
            figsize = self.style['figure_size']
        if rotation is None:
            rotation = self.style['label_rotation']
        
        # Sort if requested
        if sort_by:
            df = df.sort_values(by=sort_by, ascending=ascending)
        
        fig, ax = plt.subplots(figsize=figsize)
        ax.bar(df[x_col], df[y_col])
        
        if title:
            ax.set_title(title)
        ax.set_xlabel(xlabel or x_col)
        ax.set_ylabel(ylabel or y_col)
        ax.tick_params(axis='x', rotation=rotation)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            logger.info(f"Saved chart to {save_path}")
        
        return fig
    
    def create_scatter_plot(self,
                           df: pd.DataFrame,
                           x_col: str,
                           y_col: str,
                           label_col: Optional[str] = None,
                           title: Optional[str] = None,
                           xlabel: Optional[str] = None,
                           ylabel: Optional[str] = None,
                           figsize: Optional[Tuple[int, int]] = None,
                           grid: bool = True,
                           alpha: float = 0.7,
                           label_fontsize: int = 8,
                           save_path: Optional[str] = None) -> Figure:
        """
        Create a scatter plot with optional labels.
        
        Args:
            df: Input DataFrame
            x_col: Column for x-axis
            y_col: Column for y-axis
            label_col: Column to use for point labels
            title: Chart title
            xlabel: X-axis label
            ylabel: Y-axis label
            figsize: Figure size (width, height)
            grid: Whether to show grid
            alpha: Point transparency
            label_fontsize: Font size for labels
            save_path: Path to save figure
            
        Returns:
            matplotlib Figure object
        """
        if figsize is None:
            figsize = self.style['figure_size']
        
        fig, ax = plt.subplots(figsize=figsize)
        ax.scatter(df[x_col], df[y_col], alpha=alpha)
        
        # Add labels if specified
        if label_col and label_col in df.columns:
            for _, row in df.iterrows():
                ax.text(row[x_col], row[y_col], row[label_col],
                       fontsize=label_fontsize, ha='right')
        
        if title:
            ax.set_title(title)
        ax.set_xlabel(xlabel or x_col)
        ax.set_ylabel(ylabel or y_col)
        
        if grid:
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            logger.info(f"Saved scatter plot to {save_path}")
        
        return fig
    
    def create_comparison_chart(self,
                               df: pd.DataFrame,
                               country_col: str,
                               value_cols: List[str],
                               title: Optional[str] = None,
                               ylabel: Optional[str] = None,
                               figsize: Optional[Tuple[int, int]] = None,
                               rotation: Optional[int] = None,
                               save_path: Optional[str] = None) -> Figure:
        """
        Create a grouped bar chart comparing multiple metrics.
        
        Args:
            df: Input DataFrame
            country_col: Column with country identifiers
            value_cols: List of columns to compare
            title: Chart title
            ylabel: Y-axis label
            figsize: Figure size (width, height)
            rotation: X-axis label rotation
            save_path: Path to save figure
            
        Returns:
            matplotlib Figure object
        """
        if figsize is None:
            figsize = (12, 6)
        if rotation is None:
            rotation = self.style['label_rotation']
        
        fig, ax = plt.subplots(figsize=figsize)
        
        df_plot = df.set_index(country_col)[value_cols]
        df_plot.plot(kind='bar', ax=ax, width=0.8)
        
        if title:
            ax.set_title(title)
        ax.set_ylabel(ylabel or 'Value')
        ax.set_xlabel('')
        ax.tick_params(axis='x', rotation=rotation)
        ax.legend(title='Metrics', bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            logger.info(f"Saved comparison chart to {save_path}")
        
        return fig
    
    def create_risk_index_chart(self,
                               df: pd.DataFrame,
                               country_col: str,
                               index_col: str,
                               title: str = "CBAM Comprehensive Risk Index",
                               ylabel: str = "Risk Index",
                               figsize: Optional[Tuple[int, int]] = None,
                               color: str = 'steelblue',
                               save_path: Optional[str] = None) -> Figure:
        """
        Create a specialized chart for risk index visualization.
        
        Args:
            df: Input DataFrame
            country_col: Column with country names
            index_col: Column with risk index values
            title: Chart title
            ylabel: Y-axis label
            figsize: Figure size (width, height)
            color: Bar color
            save_path: Path to save figure
            
        Returns:
            matplotlib Figure object
        """
        if figsize is None:
            figsize = self.style['figure_size']
        
        df_sorted = df.sort_values(by=index_col, ascending=False)
        
        fig, ax = plt.subplots(figsize=figsize)
        bars = ax.bar(df_sorted[country_col], df_sorted[index_col], color=color)
        
        # Color the top 3 bars differently
        if len(bars) >= 3:
            bars[0].set_color('darkred')
            bars[1].set_color('orangered')
            bars[2].set_color('orange')
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Country', fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            logger.info(f"Saved risk index chart to {save_path}")
        
        return fig
    
    def create_sensitivity_comparison(self,
                                     df: pd.DataFrame,
                                     country_col: str,
                                     scenario_cols: List[str],
                                     scenario_names: Optional[List[str]] = None,
                                     title: str = "Sensitivity Analysis",
                                     figsize: Optional[Tuple[int, int]] = None,
                                     save_path: Optional[str] = None) -> Figure:
        """
        Create a multi-scenario comparison chart for sensitivity analysis.
        
        Args:
            df: Input DataFrame
            country_col: Column with country names
            scenario_cols: List of columns with different scenario values
            scenario_names: Display names for scenarios
            title: Chart title
            figsize: Figure size
            save_path: Path to save figure
            
        Returns:
            matplotlib Figure object
        """
        if figsize is None:
            figsize = (14, 8)
        
        if scenario_names is None:
            scenario_names = scenario_cols
        
        fig, axes = plt.subplots(2, 3, figsize=figsize)
        axes = axes.flatten()
        
        for idx, (col, name) in enumerate(zip(scenario_cols, scenario_names)):
            if idx < len(axes) and col in df.columns:
                ax = axes[idx]
                df_sorted = df.sort_values(by=col, ascending=False)
                ax.bar(df_sorted[country_col], df_sorted[col])
                ax.set_title(name)
                ax.tick_params(axis='x', rotation=45, labelsize=8)
                ax.grid(axis='y', alpha=0.3)
        
        # Hide unused subplots
        for idx in range(len(scenario_cols), len(axes)):
            axes[idx].set_visible(False)
        
        fig.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            logger.info(f"Saved sensitivity comparison to {save_path}")
        
        return fig
    
    @staticmethod
    def show_all():
        """Display all created plots."""
        plt.show()
    
    @staticmethod
    def close_all():
        """Close all plot windows."""
        plt.close('all')
