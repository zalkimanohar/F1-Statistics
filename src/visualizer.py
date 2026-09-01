# src/visualizer.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class F1Visualizer:
    def __init__(self, output_dir: str = "outputs/figures"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        sns.set_theme(style="darkgrid")

    def plot_grid_vs_finish(self, df: pd.DataFrame):
        """Generates a scatter plot with regression line for grid vs finish position with optimized bounds."""
        plt.figure(figsize=(8, 6))
        subset = df.dropna(subset=['grid_position', 'final_position'])
        
        sns.regplot(
            data=subset, x='grid_position', y='final_position', 
            scatter_kws={'alpha': 0.3}, line_kws={'color': 'red'}
        )
        plt.title("F1 Starting Grid Position vs. Final Position")
        plt.xlabel("Starting Grid Position")
        plt.ylabel("Final Position")
        
        # Adjust upper bounds to 35 to prevent cutting off extended historical grid positions
        plt.xlim(-1, 35)
        plt.ylim(-1, 35)
        
        plot_path = self.output_dir / "grid_vs_finish_regression.png"
        plt.savefig(plot_path, bbox_inches='tight')
        plt.close()

    def plot_position_distribution(self, df: pd.DataFrame):
        """Generates a distribution histogram for final race positions with KDE."""
        plt.figure(figsize=(8, 6))
        subset = df.dropna(subset=['final_position'])
        
        sns.histplot(subset['final_position'], bins=20, kde=True, color='purple')
        plt.title("Distribution of Final Finishing Positions")
        plt.xlabel("Final Position")
        plt.ylabel("Frequency")
        
        plot_path = self.output_dir / "finish_position_distribution.png"
        plt.savefig(plot_path, bbox_inches='tight')
        plt.close()

    def plot_points_by_grid(self, df: pd.DataFrame):
        """Generates a boxplot showing points earned per starting grid tier using modern hue mapping."""
        plt.figure(figsize=(10, 6))
        subset = df.dropna(subset=['grid_position', 'points']).copy()
        
        # Group grid positions into tiers for cleaner boxplotting
        bins = [0, 3, 10, 20]
        labels = ['Front Row (1-3)', 'Midfield (4-10)', 'Back Grid (11+)']
        subset['grid_tier'] = pd.cut(subset['grid_position'], bins=bins, labels=labels)
        
        sns.boxplot(data=subset, x='grid_tier', y='points', hue='grid_tier', palette='Set2', legend=False)
        plt.title("Points Distribution Across Starting Grid Tiers")
        plt.xlabel("Grid Tier")
        plt.ylabel("Points Awarded")
        
        plot_path = self.output_dir / "points_by_grid_tier.png"
        plt.savefig(plot_path, bbox_inches='tight')
        plt.close()

    def generate_all_plots(self, df: pd.DataFrame):
        """Executes all visualization routines."""
        print("Generating visual artifacts...")
        self.plot_grid_vs_finish(df)
        self.plot_position_distribution(df)
        self.plot_points_by_grid(df)
        print(f"All figures saved to {self.output_dir}")