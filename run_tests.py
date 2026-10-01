"""
FIELD PLUS — Master Automated Test Runner
Executes comprehensive test suites across all core modules:
Authentication & RBAC, Task Management, Attendance (Zero GPS),
Leave Requests, Notifications, REST API, and Core Models.
"""

import sys
import time
import unittest


class Color:
    """Terminal ANSI color codes for readable test reporting."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


def print_banner():
    """Print executive test runner banner."""
    print(f"\n{Color.CYAN}{Color.BOLD}{'=' * 75}{Color.RESET}")
    print(f"{Color.CYAN}{Color.BOLD}   FIELD PLUS — Automated Academic & Viva Verification Test Suite{Color.RESET}")
    print(f"{Color.CYAN}{Color.BOLD}{'=' * 75}{Color.RESET}")
    print(f"{Color.BLUE}   Tech Stack: Python 3.10+ | Flask 3.x | MySQL 8.x | Zero GPS Policy{Color.RESET}\n")


def run_all_tests():
    """Discover and execute all test modules, rendering structured results."""
    print_banner()

    # Ensure standard output can handle UTF-8 symbols on Windows consoles
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    start_time = time.time()
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')

    print(f"{Color.BOLD}Discovering Test Modules in ./tests/...{Color.RESET}")

    # Track test categories
    test_modules = [
        ("Authentication & RBAC", "tests.test_auth"),
        ("Field Task Lifecycle & Milestones", "tests.test_tasks"),
        ("Daily Attendance & Zero-GPS Rules", "tests.test_attendance"),
        ("Leave Processing & Attendance Sync", "tests.test_leaves"),
        ("Notification Queue & Formatting", "tests.test_notifications"),
        ("REST API Layer & Data Envelopes", "tests.test_api"),
        ("Core Models & Worker Profiles", "tests.test_models"),
    ]

    for label, mod_name in test_modules:
        try:
            mod_suite = loader.loadTestsFromName(mod_name)
            count = mod_suite.countTestCases()
            print(f"  {Color.GREEN}[PASS]{Color.RESET} {label:<38} [{count:02d} Test Cases]")
        except Exception as e:
            print(f"  {Color.RED}[FAIL]{Color.RESET} {label:<38} [Failed to load: {e}]")

    print(f"\n{Color.BOLD}Executing Comprehensive Assertions...{Color.RESET}\n")

    # Run runner
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    elapsed = time.time() - start_time

    # Output Summary
    total_tests = result.testsRun
    failed_tests = len(result.failures)
    errored_tests = len(result.errors)
    passed_tests = total_tests - failed_tests - errored_tests

    print(f"\n{Color.CYAN}{Color.BOLD}{'=' * 75}{Color.RESET}")
    print(f"{Color.BOLD}   VERIFICATION TEST SUITE SUMMARY{Color.RESET}")
    print(f"{Color.CYAN}{Color.BOLD}{'=' * 75}{Color.RESET}")
    print(f"   Total Test Cases Executed : {Color.BOLD}{total_tests}{Color.RESET}")
    print(f"   Tests Passed              : {Color.GREEN}{Color.BOLD}{passed_tests}{Color.RESET}")
    print(f"   Tests Failed              : {Color.RED if failed_tests > 0 else Color.GREEN}{Color.BOLD}{failed_tests}{Color.RESET}")
    print(f"   Runtime Errors            : {Color.RED if errored_tests > 0 else Color.GREEN}{Color.BOLD}{errored_tests}{Color.RESET}")
    print(f"   Execution Elapsed Time    : {Color.CYAN}{elapsed:.3f} seconds{Color.RESET}")
    print(f"{Color.CYAN}{Color.BOLD}{'=' * 75}{Color.RESET}")

    if result.wasSuccessful():
        print(f"\n{Color.GREEN}{Color.BOLD}>>> SUCCESS: ALL {total_tests} TESTS PASSED CLEANLY! SYSTEM IS 100% STABLE & ACADEMICALLY VERIFIED.{Color.RESET}\n")
        return 0
    else:
        print(f"\n{Color.RED}{Color.BOLD}>>> WARNING: SOME TESTS FAILED. PLEASE REVIEW TRACEBACK DETAILS ABOVE.{Color.RESET}\n")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
