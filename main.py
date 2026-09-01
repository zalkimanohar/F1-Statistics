# main.py
from src.ingest import GoldDataIngester
from src.statistics import F1StatisticalEngine
from src.visualizer import F1Visualizer
from src.reporter import StatisticalReporter

def main():
    print("--- Starting F1 StatisticalOps Pipeline ---")
    
    # 1. Ingest Data
    ingester = GoldDataIngester()
    merged_df = ingester.get_merged_session_data()
    
    # 2. Run Statistics
    engine = F1StatisticalEngine(merged_df)
    stats_results = engine.run_all_analyses()
    
    # 3. Generate Visualizations (Generates all analytical plots)
    visualizer = F1Visualizer()
    visualizer.generate_all_plots(merged_df)
    
    # 4. Compile Report
    reporter = StatisticalReporter()
    reporter.generate_markdown_report(stats_results)
    
    print("--- Pipeline Execution Complete ---")

if __name__ == "__main__":
    main()