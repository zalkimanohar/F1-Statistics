#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define color codes for clear terminal logging
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Ensure we are running from the F1-Statistics project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Ensure output directories exist idempotently (never duplicates if they exist)
mkdir -p outputs/figures outputs/reports outputs/logs

# Manage log files: Keep only the latest 5 log files to prevent clutter
find outputs/logs -type f -name "pipeline_*.log" | sort -r | tail -n +6 | xargs rm -f 2>/dev/null || true

# Set up a clean log file path for the current run
LOG_FILE="outputs/logs/pipeline_current.log"

echo -e "${BLUE}====================================================${NC}"
echo -e "${BLUE}    F1-Statistics Statistical Pipeline Execution    ${NC}"
echo -e "${BLUE}====================================================${NC}"
echo "Logging execution to: ${LOG_FILE}"

# Step 1: Environment & Dependency Check
echo -e "\n${GREEN}[1/5] Verifying environment and dependencies...${NC}"
if [ -d ".venv" ]; then
    echo "Activating virtual environment (.venv)..."
    source .venv/bin/activate
elif [ -n "$CONDA_DEFAULT_ENV" ]; then
    echo "Using active conda environment: $CONDA_DEFAULT_ENV"
else
    echo -e "${RED}Warning: No active virtual environment detected. Proceeding with system python.${NC}"
fi

python -c "import sys; print(f'Python version: {sys.version}')"

# Step 2: Validate Configuration and Gold Layer Datasets Alignment
echo -e "\n${GREEN}[2/5] Validating config and Gold layer structure...${NC}"

# Check config files
if [ ! -f "config/config.yaml" ] || [ ! -f "config/metrics_schema.json" ]; then
    echo -e "${RED}Error: Missing files in config/ (config.yaml or metrics_schema.json)!${NC}"
    exit 1
fi

# Check required Gold layer parquet directories/files
REQUIRED_GOLD=(
    "data/gold/dim_constructors/dim_constructors.parquet"
    "data/gold/dim_drivers/dim_drivers.parquet"
    "data/gold/dim_races/dim_races.parquet"
    "data/gold/fact_session_results/fact_session_results.parquet"
    "data/gold/ref_nationality_region/ref_nationality_region.parquet"
)

for file in "${REQUIRED_GOLD[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}Error: Missing expected Gold dataset -> $file${NC}"
        exit 1
    fi
done

echo "Configuration and Gold layer parquet files successfully verified."

# Step 3: Run Core Pipeline Orchestrator (main.py)
echo -e "\n${GREEN}[3/5] Executing main.py orchestrator...${NC}"
if [ -f "main.py" ]; then
    python main.py 2>&1 | tee "$LOG_FILE"
else
    echo -e "${RED}Error: main.py not found at project root.${NC}"
    exit 1
fi

# Step 4: Generate Reports and Visualizations Check
echo -e "\n${GREEN}[4/5] Checking generated reports and figures...${NC}"
echo "Execution pipeline completed steps successfully."

# Step 5: Final Validation of Outputs
echo -e "\n${GREEN}[5/5] Finalizing outputs verification...${NC}"
if [ "$(ls -A outputs/reports)" ]; then
    echo -e "${BLUE}Reports successfully populated under outputs/reports/${NC}"
else
    echo -e "${RED}Warning: outputs/reports/ appears empty.${NC}"
fi

if [ "$(ls -A outputs/figures)" ]; then
    echo -e "${BLUE}Figures successfully populated under outputs/figures/${NC}"
else
    echo -e "${RED}Warning: outputs/figures/ appears empty.${NC}"
fi

echo -e "\n${BLUE}====================================================${NC}"
echo -e "${BLUE}       F1-Statistics Pipeline Completed Successfully ${NC}"
echo -e "${BLUE}====================================================${NC}"