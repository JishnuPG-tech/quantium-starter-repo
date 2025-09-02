# Soul Foods Dashboard - Test Suite

## Overview
This test suite validates the Soul Foods Pink Morsel Dashboard application using pytest.

## Test Requirements (Task 5)
- Test 1: Header is present
- Test 2: Visualization is present
- Test 3: Region picker is present

## Running Tests
```bash
pytest test_dash_simple.py -v
```

## Test Files
- test_dash_simple.py - Main test suite
- test_utils.py - Test utility functions
- pytest.ini - Pytest configuration

## Expected Results
All tests should PASS because:
- Header contains Soul Foods Pink Morsel
- Chart component exists with ID sales-chart
- Radio buttons exist with ID region-filter

Created for Quantium Data Science Virtual Experience - Task 5
