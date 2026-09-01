#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Initializing F-1 StatisticalOps project structure..."

# 1. Create directories
mkdir -p config
mkdir -p data/gold
mkdir -p src
mkdir -p outputs/reports
mkdir -p outputs/figures
mkdir -p notebooks
mkdir -p scripts

# 2. Create base files with placeholder headers or empty states
touch config/config.yaml
touch config/metrics_schema.json

touch src/__init__.py
touch src/ingest.py
touch src/statistics.py
touch src/visualizer.py
touch src/reporter.py

touch notebooks/exploratory_stats.py
touch scripts/run_statistical_pipeline.sh

touch requirements.txt
touch main.py

# 3. Populate run_statistical_pipeline.sh with a basic template
cat << 'EOF' > scripts/run_statistical_pipeline.sh
#!/usr/bin/env bash
echo "Starting F-1 StatisticalOps pipeline..."
python3 main.py
echo "Pipeline execution complete."
EOF

# Make the automation script executable
chmod +x scripts/run_statistical_pipeline.sh

echo "Project structure successfully created!"
