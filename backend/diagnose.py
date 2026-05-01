#!/usr/bin/env python3
"""Diagnostic script for the Mapgenius Solutions backend.

This script performs a series of checks that are commonly the cause of
"ERR_CONNECTION_REFUSED" when trying to start a FastAPI/Uvicorn server.
It verifies:

1. All project modules can be imported.
2. A .env file exists and contains a DATABASE_URL entry.
3. The pyodbc package (and underlying ODBC driver) is available.
4. All Python files have syntactically valid code.

The script prints clear, colour‑coded messages for each check and sets a
non‑zero exit code if any check fails.
"""

import os
import sys
import importlib
import traceback
from pathlib import Path

# Helper for coloured output (works on most terminals)
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

def print_success(message: str):
    print(f"{Colors.GREEN}✔ {message}{Colors.RESET}")

def print_error(message: str):
    print(f"{Colors.RED}✖ {message}{Colors.RESET}")

def print_warning(message: str):
    print(f"{Colors.YELLOW}! {message}{Colors.RESET}")

def check_imports(project_root: Path) -> bool:
    """Attempt to import every module in the project.

    Returns True if all imports succeed, False otherwise.
    """
    success = True
    sys.path.insert(0, str(project_root))
    for py_path in project_root.rglob("*.py"):
        # Skip test files and this diagnostic script itself
        if py_path.name.startswith("test_") or py_path.name == "diagnose.py":
            continue
        # Derive module name from file path
        rel_path = py_path.relative_to(project_root).with_suffix("")
        module_name = ".".join(rel_path.parts)
        try:
            importlib.import_module(module_name)
        except Exception as exc:
            success = False
            print_error(f"Failed to import module '{module_name}': {exc}")
            # Show a short traceback for context
            tb = traceback.format_exc().splitlines()[:3]
            for line in tb:
                print_warning(line)
    return success

def check_env_file(project_root: Path) -> bool:
    """Ensure a .env file exists and contains a DATABASE_URL variable.
    """
    env_path = project_root / ".env"
    if not env_path.is_file():
        print_error("'.env' file not found in project root.")
        return False
    # Load environment variables (simple parsing, no external deps)
    with env_path.open() as f:
        for line in f:
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            if key == "DATABASE_URL" and value:
                os.environ["DATABASE_URL"] = value
                print_success("DATABASE_URL found in .env.")
                return True
    print_error("DATABASE_URL not set in .env.")
    return False

def check_pyodbc() -> bool:
    """Verify that pyodbc can be imported and that an ODBC driver is reachable.
    """
    try:
        import pyodbc  # noqa: F401
    except ImportError:
        print_error("pyodbc package is not installed.")
        return False
    # Attempt a minimal driver list query – this will succeed even if no DSN is defined
    try:
        drivers = pyodbc.drivers()
        if not drivers:
            print_warning("pyodbc is installed but no ODBC drivers were detected.")
        else:
            print_success(f"pyodbc installed. Detected drivers: {', '.join(drivers)}")
        return True
    except Exception as exc:
        print_error(f"pyodbc import succeeded but driver query failed: {exc}")
        return False

def check_syntax(project_root: Path) -> bool:
    """Compile each .py file to ensure syntax is valid.
    """
    success = True
    for py_path in project_root.rglob("*.py"):
        if py_path.name == "diagnose.py":
            continue
        try:
            compile(py_path.read_text(encoding="utf-8"), str(py_path), "exec")
        except SyntaxError as exc:
            success = False
            print_error(f"Syntax error in {py_path}: {exc.msg} (line {exc.lineno})")
        except Exception as exc:
            # Unexpected read/encoding errors
            success = False
            print_error(f"Failed to read {py_path}: {exc}")
    if success:
        print_success("All Python files have valid syntax.")
    return success

def main():
    project_root = Path(__file__).resolve().parent.parent  # assumes script lives in backend/
    print("Running backend diagnostics for Mapgenius Solutions...\n")

    checks = {
        "Importability": check_imports(project_root),
        "Environment (.env)": check_env_file(project_root),
        "pyodbc driver": check_pyodbc(),
        "Syntax validation": check_syntax(project_root),
    }

    all_passed = all(checks.values())
    print("\nSummary:")
    for name, result in checks.items():
        symbol = f"{Colors.GREEN}OK{Colors.RESET}" if result else f"{Colors.RED}FAIL{Colors.RESET}"
        print(f" - {name}: {symbol}")

    if not all_passed:
        print_error("One or more checks failed. Resolve the above issues before running uvicorn.")
        sys.exit(1)
    else:
        print_success("All checks passed. You should be able to start uvicorn now.")
        sys.exit(0)

if __name__ == "__main__":
    main()
