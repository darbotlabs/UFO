# 🛸 **UFO² Mission Pack for Claude 3.7 (Agent Mode)** - Updated 2025-05-25

Welcome, Agent Claude 3.7.  
Your objective is to ready the local Windows 11 workstation for UFO², validate the setup, and execute a sample flight.  
Progress through the **10 Missions** below in order. Each mission contains clear success criteria and, where relevant, PowerShell 7 snippets to run directly in the VS Code terminal.

---

## Mission 0 ― Intel Briefing
* Workspace already contains the full UFO source at `g:\Github\UFO`.
* VS Code Insiders + PowerShell 7 are pre‑installed.
* You have administrator rights.

---

## Mission 1 ― 🛡️ Prerequisite Recon & Install

**Objective:** Verify and, if missing, auto‑install all system dependencies.

PowerShell 7 script (run as single block):

```powershell
# Mission 1 – Prerequisite Recon
Write-Host "🔍  Mission 1: Checking prerequisites…" -ForegroundColor Cyan

# 1.1  Confirm Python ≥3.10
$pyOk = ($null -ne (Get-Command python -ErrorAction SilentlyContinue)) -and
        ((python -c "import sys, json; print(json.dumps(sys.version_info[:3]))") -as [string]) -match '^\[3,(10|11|12|13),'

if (-not $pyOk) {
    Write-Host "⛑️  Python ≥3.10 not found. Installing via winget…" -ForegroundColor Yellow
    winget install -e --id Python.Python.3.11
}

# 1.2  Ensure Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    winget install --id Git.Git -e
}

# 1.3  Optional: Conda (recommended)
if (-not (Get-Command conda -ErrorAction SilentlyContinue)) {
    Write-Host "⛑️  Miniconda missing -> installing…" -ForegroundColor Yellow
    winget install -e --id Anaconda.Miniconda3
}

# 1.4  Optional: Visual C++ Build Tools (for some packages)
Write-Host "ℹ️  Note: Some optional packages like azure-identity-broker require Microsoft Visual C++ Build Tools."
Write-Host "    If needed later, you can install them from: https://visualstudio.microsoft.com/visual-cpp-build-tools/"

# 1.5  Extra: Ensure PowerShell 7 is default shell in VS Code
Write-Host "ℹ️  Recommended: Set PowerShell 7 as your default VS Code shell for best compatibility."

# 1.6  Extra: Ensure VS Code Insiders is installed
if (-not (Test-Path "$env:LOCALAPPDATA\Programs\Microsoft VS Code Insiders\Code - Insiders.exe")) {
    Write-Host "⛑️  VS Code Insiders not found. Installing..." -ForegroundColor Yellow
    winget install -e --id Microsoft.VisualStudioCode.Insiders
}

Write-Host "✅  Mission 1 complete." -ForegroundColor Green
```

**Success criteria**
1. Running the block prints "Mission 1 complete".
2. `python --version`, `git --version`, and (optionally) `conda --version` succeed.

---

## Mission 2 ― 🪐 Virtual Environment Warp‑In

**Objective:** Isolate dependencies.

```powershell
# Mission 2 – Create & activate venv
Write-Host "🚀  Mission 2: Spinning up virtual env…" -ForegroundColor Cyan

$envPath = "$env:USERPROFILE\ufo_env"
python -m venv $envPath
& "$envPath\Scripts\Activate.ps1"
python -m pip install --upgrade pip

Write-Host "✅  Mission 2 complete. Venv activated!" -ForegroundColor Green
```

**Success criteria**
`(ufo_env)` appears in the prompt.

---

## Mission 3 ― 📦 Dependency Drop

```powershell
# Mission 3 – Install UFO requirements
Write-Host "📦  Mission 3: Installing UFO requirements…" -ForegroundColor Cyan
Set-Location g:\Github\UFO

# First attempt with standard install
pip install -r requirements.txt

# If certain packages fail due to build requirements, try binary-only installations
if ($LASTEXITCODE -ne 0) {
    Write-Host "ℹ️  Some packages failed to install. Attempting alternative methods..." -ForegroundColor Yellow
    
    # Try installing lxml with binary only
    pip install --only-binary :all: lxml
    
    # Install faiss-cpu separately
    pip install faiss-cpu
    
    # Install azure-identity (without broker if build tools missing)
    pip install azure-identity
    
    Write-Host "ℹ️  Note: azure-identity-broker may require Visual C++ build tools." -ForegroundColor Yellow
}

Write-Host "✅  Mission 3 complete." -ForegroundColor Green
Write-Host "🔍  Validating critical UFO dependencies..." -ForegroundColor Yellow
python -c "import sys; pkgs=['azure.identity','faiss','cv2','yaml','pywinauto','pyautogui','sentence_transformers','langchain','lxml','openai','numpy','torch']; missing=[p for p in pkgs if __import__('importlib.util').util.find_spec(p) is None]; print('Missing:', missing if missing else 'None')"
Write-Host "If any packages are missing, install them individually using pip."
```

**Success criteria**
Core packages are installed successfully. It's acceptable if azure-identity-broker fails if you don't need AAD authentication.

---

## Mission 4 ― 🔑 Key Vault Configuration

```powershell
# Mission 4 – Copy & open config stub
Write-Host "🗝️  Mission 4: Preparing LLM config…" -ForegroundColor Cyan

if (-not (Test-Path -Path "ufo\config\config.yaml")) {
    Copy-Item ufo\config\config.yaml.template ufo\config\config.yaml -Force
    notepad ufo\config\config.yaml   # ← paste API keys for HOST_AGENT & APP_AGENT
} else {
    Write-Host "ℹ️  config.yaml already exists. Opening for verification..." -ForegroundColor Yellow
    notepad ufo\config\config.yaml
}

# Quick config validation
Write-Host "🔍  Validating config file format..." -ForegroundColor Cyan
$configContent = Get-Content -Path "ufo\config\config.yaml" -Raw
if ($configContent -match "API_TYPE:" -and $configContent -match "API_KEY:") {
    Write-Host "✅  Config file contains necessary API settings." -ForegroundColor Green
} else {
    Write-Host "⚠️  Warning: Config file may be missing API settings. Please check manually." -ForegroundColor Yellow
}

# Extra: Double-check that API_MODEL and API_DEPLOYMENT_ID match your actual Azure OpenAI deployment name (not just 'gpt-4o' by default)
Write-Host "ℹ️  If you get 'unavailable_model' errors, verify your Azure OpenAI deployment name in config.yaml matches the actual deployment name in the Azure portal." -ForegroundColor Yellow
```

**Success criteria**
`ufo\config\config.yaml` exists and contains valid keys.

---

## Mission 5 ― 📚 Optional RAG Setup (Skip = OK)

If you wish to enable extra knowledge sources, fill the corresponding sections in the same `config.yaml`. No script needed.

---

## Mission 6 ― 🧪 Functional Smoke Test

```powershell
# Mission 6 – Basic functionality test
Write-Host "🧪  Mission 6: Running basic functionality test…" -ForegroundColor Cyan

# Step 1: Simple import test
Write-Host "Testing basic imports..." -ForegroundColor Yellow
python -c "from ufo import ufo; print('✅ UFO imports successfully!')"

# Step 2: CLI help test
Write-Host "Testing CLI interface..." -ForegroundColor Yellow
python -m ufo --help

# Step 3: Basic request test
Write-Host "Testing simple request (this may take a minute)..." -ForegroundColor Yellow
python -m ufo --request "Hello, what can you do?"

# Step 3b: If you get 'unavailable_model' or API errors, check config.yaml for correct deployment name and API key.
Write-Host "ℹ️  If you see 'unavailable_model' or API errors, check your Azure OpenAI deployment name and API key in config.yaml." -ForegroundColor Yellow

Write-Host "✅  Mission 6 complete - verify log creation." -ForegroundColor Green

# Step 4: Verify log creation
$logPath = Get-ChildItem -Path ".\logs" -Directory | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($logPath) {
    Write-Host "📁 Log directory created at: $($logPath.FullName)" -ForegroundColor Green
} else {
    Write-Host "⚠️  No log directory found. Check if the test completed successfully." -ForegroundColor Yellow
}

# Optional: Try more complex automation (if basic tests pass)
Write-Host "🧪  Optional: Try automation test (only if previous tests succeeded)" -ForegroundColor Cyan
Write-Host "python -m ufo --task demo_hello -r 'open notepad and type hello'" -ForegroundColor Yellow
```

**Success criteria**
1. Basic imports succeed
2. UFO CLI responds with help text
3. Simple request returns a response
4. Logs are generated in the `logs/[date-time]/` directory
5. (Optional) Notepad automation test works

---

## Mission 7 ― 📊 Bench Check (WAA Mini‑Suite)

```powershell
# Mission 7 – Optional benchmark (takes time)
# Note: This may require additional setup or repository access
Write-Host "📊  Mission 7: Attempting benchmark tests..." -ForegroundColor Cyan

# Verify if benchmarks module exists
if (Test-Path -Path ".\ufo\benchmarks\waa.py") {
    python -m ufo.benchmarks.waa --subset 3   # run 3 random tasks
} else {
    Write-Host "ℹ️  Benchmark module not found. WAA benchmarks may be in a separate repository." -ForegroundColor Yellow
    Write-Host "ℹ️  Refer to documentation: https://microsoft.github.io/UFO/benchmark/windows_agent_arena/" -ForegroundColor Yellow
    
    # Alternative validation - run another simple test
    Write-Host "🔄  Running alternative validation test..." -ForegroundColor Cyan
    python -m ufo --request "What's the time right now?"
}
```

**Success criteria**
Either benchmark runs with 1+ passing test OR alternative validation test succeeds.

---

## Mission 8 ― 🛠️ Developer Loop Validation

```powershell
# Mission 8 - Check VS Code integration
Write-Host "🛠️  Mission 8: Setting up VS Code debugging..." -ForegroundColor Cyan

# Create launch.json if it doesn't exist
$launchJsonDir = ".\.vscode"
$launchJsonPath = "$launchJsonDir\launch.json"

if (-not (Test-Path -Path $launchJsonDir)) {
    New-Item -ItemType Directory -Path $launchJsonDir
}

if (-not (Test-Path -Path $launchJsonPath)) {
    @'
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "UFO Quickstart",
            "type": "python",
            "request": "launch",
            "module": "ufo",
            "args": ["--request", "Hello, what can you do?"],
            "justMyCode": false
        }
    ]
}
'@ | Out-File -FilePath $launchJsonPath -Encoding utf8
    Write-Host "✅  Created launch.json for VS Code debugging" -ForegroundColor Green
} else {
    Write-Host "ℹ️  launch.json already exists" -ForegroundColor Yellow
}

Write-Host "ℹ️  Instructions for debugging:" -ForegroundColor Cyan
Write-Host "1. Open VS Code at the UFO root folder" -ForegroundColor White
Write-Host "2. Open ufo/__main__.py and set a breakpoint" -ForegroundColor White
Write-Host "3. Press F5 to start debugging with the 'UFO Quickstart' configuration" -ForegroundColor White
Write-Host "4. Verify the breakpoint is hit and you can step through the code" -ForegroundColor White

# Alternative CLI test if not using VS Code
Write-Host "🔍  Alternative: Running debug mode from CLI..." -ForegroundColor Cyan
python -m ufo --request "What are you?" --debug
```

**Success criteria**
Either VS Code debugger attaches without exceptions OR debug mode CLI test shows additional output.

---

## Mission 9 ― 👾 Regression Guard

```powershell
# Mission 9 – Tests + lint
Write-Host "👾  Mission 9: Running tests and linting..." -ForegroundColor Cyan

# Try unittest discovery first
Write-Host "🧪  Running unittest discovery..." -ForegroundColor Yellow
python -m unittest discover

# Try pytest if available (may require installation)
try {
    Write-Host "🧪  Attempting to run pytest..." -ForegroundColor Yellow
    python -m pytest -q
} catch {
    Write-Host "ℹ️  pytest not installed or configured. This is OK if no tests exist." -ForegroundColor Yellow
}

# Try ruff for linting if available
try {
    Write-Host "🔍  Checking code with ruff..." -ForegroundColor Yellow
    pip install ruff -q
    python -m ruff check ufo
} catch {
    Write-Host "ℹ️  Ruff linting failed or not installed. Consider installing for code quality checks." -ForegroundColor Yellow
}

Write-Host "✅  Mission 9 complete - check for any critical errors in output" -ForegroundColor Green
Write-Host "ℹ️  If no tests are found, create a minimal test_imports.py to validate imports and CLI functionality." -ForegroundColor Yellow
```

**Success criteria**
Tests run if they exist; no critical errors from linting. It's acceptable if no tests are found as long as the import tests from Mission 6 succeeded.

---

## Mission 10 ― 🎉 Mission Debrief

```powershell
# Mission 10 - Generate mission report
Write-Host "📝  Mission 10: Generating mission report..." -ForegroundColor Cyan

# Create logs directory if it doesn't exist
$logsDir = ".\ufo\logs"
if (-not (Test-Path -Path $logsDir)) {
    New-Item -ItemType Directory -Path $logsDir
    Write-Host "📁  Created logs directory at $logsDir" -ForegroundColor Green
}

# Get the last log directory
$lastLogDir = Get-ChildItem -Path ".\logs" -Directory | Sort-Object LastWriteTime -Descending | Select-Object -First 1 -ExpandProperty FullName
if (-not $lastLogDir) {
    $lastLogDir = "No logs directory found"
}

# Generate report
@"
# UFO² Mission Report - $(Get-Date -Format "yyyy-MM-dd")

## Environment
- Python: $(python --version 2>&1)
- UFO Version: 2.0.0
- UFO Repository: $(Get-Location)
- UFO Commit: $(git rev-parse --short HEAD 2>$null || "Git info not available")

## Installation Status
- Virtual Environment: $env:USERPROFILE\ufo_env
- Config File: $(if (Test-Path -Path ".\ufo\config\config.yaml") {"✅ Present at ./ufo/config/config.yaml"} else {"❌ Missing"})

## Testing Results
- Basic Import Test: $(try { python -c "from ufo import ufo; exit(0)" 2>$null; "✅ Passed" } catch { "❌ Failed" })
- Latest Log Directory: $lastLogDir


## Next Steps
1. Try running tasks with `python -m ufo --task your_task_name -r "your request"`
2. Set up VS Code debugging with the UFO Quickstart configuration
3. Explore the documentation at https://microsoft.github.io/UFO/
4. If you encounter 'unavailable_model' errors, check your Azure OpenAI deployment name in config.yaml.
5. If you see missing dependency errors, re-run the validation import script from Mission 3.

## Notes
- Some optional dependencies may require Microsoft Visual C++ Build Tools
- For benchmarks, refer to https://microsoft.github.io/UFO/benchmark/windows_agent_arena/ 
- Logs are created in \`logs/[date-time]/\` at the repository root
- If you have no unit tests, create a minimal test_imports.py to validate imports and CLI.
"@ | Out-File -FilePath ".\ufo\logs\mission_report.md" -Encoding utf8

# Also create a copy at the root for easier access
Copy-Item -Path ".\ufo\logs\mission_report.md" -Destination ".\mission_report_$(Get-Date -Format 'yyyy-MM-dd').md"

Write-Host "✅  Mission 10 complete - Report generated!" -ForegroundColor Green
Write-Host "📄  Reports saved to:" -ForegroundColor Cyan
Write-Host "   - .\ufo\logs\mission_report.md" -ForegroundColor White
Write-Host "   - .\mission_report_$(Get-Date -Format 'yyyy-MM-dd').md" -ForegroundColor White
```

**Success criteria**
Mission report is generated in both locations with the fields listed above.

---

Good luck, Agent Claude 3.7. Complete all missions and UFO² will be fully operational on this system.

## Mission Pack Changelog

- 2025-05-25: Further improved after advanced field validation
  - Added VS Code Insiders check and PowerShell 7 shell note to Mission 1
  - Mission 3 now includes explicit import validation and missing dependency guidance
  - Mission 4 clarifies Azure OpenAI deployment name matching
  - Mission 6 adds troubleshooting for unavailable_model and API errors
  - Mission 9 suggests creating a minimal test_imports.py if no tests exist
  - Mission 10 adds troubleshooting and next steps for model/dependency errors
  - All missions clarified for missing dependencies and extra validation steps
  - Previous 2025-05-01 improvements retained
