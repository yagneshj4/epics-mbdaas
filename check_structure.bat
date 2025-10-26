@echo off
echo ================================================================================
echo EPICS MBDAaaS - Complete Project Structure Verification
echo ================================================================================
echo.

REM Core folders that must exist
echo [Checking Core Folders...]
if exist "catalog" (echo ✓ catalog) else (echo ✗ catalog)
if exist "configs" (echo ✓ configs) else (echo ✗ configs)
if exist "data\raw" (echo ✓ data\raw) else (echo ✗ data\raw)
if exist "data\anonymized" (echo ✓ data\anonymized) else (echo ✗ data\anonymized)
if exist "data\hive\pseudonym_mappings" (echo ✓ data\hive) else (echo ✗ data\hive)
if exist "experiments" (echo ✓ experiments) else (echo ✗ experiments)
if exist "models\trained" (echo ✓ models\trained) else (echo ✗ models\trained)
if exist "pipelines" (echo ✓ pipelines) else (echo ✗ pipelines)
if exist "results\tables" (echo ✓ results\tables) else (echo ✗ results\tables)
if exist "services" (echo ✓ services) else (echo ✗ services)
if exist "src" (echo ✓ src) else (echo ✗ src)

echo.
echo [Checking 3 Real Datasets...]
if exist "data\raw\cybersecurity\cybersecurity_threat_detection_logs.csv" (
    echo ✓ Dataset 1: Cybersecurity Logs
) else (
    echo ✗ Dataset 1: Cybersecurity Logs - MISSING
)

if exist "data\raw\login_behavior\rba-dataset.csv" (
    echo ✓ Dataset 2: Login Behavior (RBA)
) else (
    echo ✗ Dataset 2: Login Behavior - MISSING
)

if exist "data\raw\smart_grid\smart_grid_dataset.csv" (
    echo ✓ Dataset 3: Smart Grid Monitoring
) else (
    echo ✗ Dataset 3: Smart Grid - MISSING
)

echo.
echo [Checking Key Files...]
if exist "pipelines\bootstrap_pipeline.py" (echo ✓ Bootstrap Pipeline) else (echo ✗ Bootstrap Pipeline)
if exist "pipelines\detection_pipeline.py" (echo ✓ Detection Pipeline) else (echo ✗ Detection Pipeline)
if exist "services\api.py" (echo ✓ REST API) else (echo ✗ REST API)
if exist "services\dashboard.py" (echo ✓ Dashboard) else (echo ✗ Dashboard)
if exist "epics_production.py" (echo ✓ Main Orchestrator) else (echo ✗ Main Orchestrator)

echo.
echo ================================================================================
echo Project Structure Verification Complete
echo ================================================================================
pause
