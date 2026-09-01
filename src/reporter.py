# src/reporter.py
from datetime import datetime
from pathlib import Path

class StatisticalReporter:
    def __init__(self, output_dir: str = "outputs/reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_markdown_report(self, stats_results: dict) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        desc = stats_results.get("descriptive", {})
        grid_stats = stats_results.get("grid_vs_position", {})
        podium = stats_results.get("podium_conversion", {})
        ml_recs = stats_results.get("ml_recommendations", [])
        
        season_min = desc.get('season_min', 1950)
        season_max = desc.get('season_max', 2026)
        recs_bullets = "\n".join([f"* {rec}" for rec in ml_recs])

        report_content = f"""# F1 StatisticalOps Detailed Analytical Report
*Generated on: {timestamp}*

## 1. Executive Summary
This report provides dynamic, deep-dive statistical insights derived from the latest F1 Gold datasets spanning seasons **{season_min} to {season_max}**. It bridges descriptive baseline distributions with inferential correlation models and regression analysis to evaluate race predictability.

---

## 2. Descriptive Statistics & Dispersion Metrics
* **Sample Size Analyzed:** `{grid_stats.get('sample_size', 0):,}` session entries
* **Starting Grid Position Tendencies:**
  * Mean: `{desc.get('grid_mean', 0):.2f}` | Median: `{desc.get('grid_median', 0):.1f}`
  * Variance: `{desc.get('grid_variance', 0):.2f}` | Standard Deviation: `{desc.get('grid_std', 0):.2f}`
  * Skewness: `{desc.get('grid_skewness', 0):.2f}` | Kurtosis: `{desc.get('grid_kurtosis', 0):.2f}`
* **Final Finishing Position Tendencies:**
  * Mean: `{desc.get('finish_mean', 0):.2f}` | Median: `{desc.get('finish_median', 0):.1f}`
  * Variance: `{desc.get('finish_variance', 0):.2f}` | Standard Deviation: `{desc.get('finish_std', 0):.2f}`
  * Skewness: `{desc.get('finish_skewness', 0):.2f}` | Kurtosis: `{desc.get('finish_kurtosis', 0):.2f}`

---

## 3. Probability & Sampling Insights
* **Total Tracked Poles:** `{podium.get('total_poles', 0):,}`
* **Pole-to-Win Conversion Rate:** `{podium.get('pole_win_probability', 0) * 100:.2f}%`

---

## 4. Hypothesis Testing & Regression Analysis
* **Pearson Correlation Coefficient:** `{grid_stats.get('pearson_correlation', 0):.4f}` *(p-value: `{grid_stats.get('pearson_p_value_str', '< 1.0e-15')}`)*
* **Spearman Rank Correlation:** `{grid_stats.get('spearman_correlation', 0):.4f}` *(p-value: `{grid_stats.get('spearman_p_value_str', '< 1.0e-15')}`)*
* **Linear Regression Model Fit ($R^2$):** `{grid_stats.get('r_squared', 0):.4f}`
* **Podium Logistic Pseudo-$R^2$ (Non-Linear Proxy):** `{grid_stats.get('podium_logistic_pseudo_r2', 0):.4f}`

---

## 5. Comprehensive Visual Artifacts

### A. Grid Position vs. Final Position Regression Fit
Evaluates linear dependency and variance between starting slots and race outcomes.
![Grid vs Finish](../figures/grid_vs_finish_regression.png)

### B. Final Position Distribution Histogram
Highlights the distribution profile and density across all finishing slots.
![Position Distribution](../figures/finish_position_distribution.png)

### C. Points Earned Across Starting Grid Tiers
Analyzes performance outcomes segmented by starting performance brackets.
![Points by Grid Tier](../figures/points_by_grid_tier.png)

---

## 6. Intelligent Recommendations for Engineering & ML Teams
*Programmatically evaluated based on live statistical performance thresholds from the current F1 dataset run:*

{recs_bullets}
"""
        report_path = self.output_dir / f"detailed_statistical_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_path, "w") as f:
            f.write(report_content)
            
        print(f"Detailed report successfully compiled at {report_path}")
        return str(report_path)