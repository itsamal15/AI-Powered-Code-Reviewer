# # tests/test_dashboard.py

# """Tests for dashboard UI."""

# from dashboard_ui.dashboard import load_pytest_results, filter_functions


# def test_dashboard_loads_pytest_results():
#     """Test loading pytest results (may be None if not generated)."""
#     data = load_pytest_results()
#     assert data is None or isinstance(data, dict)


# def test_filter_functions_search():
#     """Test function filtering by search term."""
#     functions = [
#         {"name": "test_function", "has_docstring": True, "file_path": "test.py"},
#         {"name": "other_function", "has_docstring": False, "file_path": "test.py"}
#     ]
    
#     filtered = filter_functions(functions, search="test", status=None)
#     assert len(filtered) == 1
#     assert filtered[0]["name"] == "test_function"


# def test_filter_functions_status():
#     """Test function filtering by status."""
#     functions = [
#         {"name": "documented", "has_docstring": True, "file_path": "test.py"},
#         {"name": "undocumented", "has_docstring": False, "file_path": "test.py"}
#     ]
    
#     filtered_ok = filter_functions(functions, search=None, status="OK")
#     assert len(filtered_ok) == 1
    
#     filtered_fix = filter_functions(functions, search=None, status="Fix")
#     assert len(filtered_fix) == 1


# def test_filter_functions_combined():
#     """Test combining search and status filters."""
#     functions = [
#         {"name": "test_doc", "has_docstring": True, "file_path": "test.py"},
#         {"name": "test_undoc", "has_docstring": False, "file_path": "test.py"},
#         {"name": "other_doc", "has_docstring": True, "file_path": "test.py"}
#     ]
    
#     filtered = filter_functions(functions, search="test", status="OK")
#     assert len(filtered) == 1
#     assert filtered[0]["name"] == "test_doc"

# tests/test_dashboard.py

"""Tests for dashboard helper functions."""

from dashboard_ui.dashboard import load_pytest_results, filter_functions


def test_dashboard_loads_pytest_results():
    """
    load_pytest_results should return:
    - None if file does not exist
    - dict if file exists and is valid JSON
    """
    data = load_pytest_results()

    assert data is None or isinstance(data, dict)


def test_filter_functions_search():
    """Filter functions by search term."""
    functions = [
        {"name": "test_function", "has_docstring": True, "file_path": "test.py"},
        {"name": "other_function", "has_docstring": False, "file_path": "test.py"},
    ]

    filtered = filter_functions(functions, search="test")

    assert len(filtered) == 1
    assert filtered[0]["name"] == "test_function"


def test_filter_functions_status_ok():
    """Filter only documented functions."""
    functions = [
        {"name": "documented", "has_docstring": True, "file_path": "test.py"},
        {"name": "undocumented", "has_docstring": False, "file_path": "test.py"},
    ]

    filtered = filter_functions(functions, status="OK")

    assert len(filtered) == 1
    assert filtered[0]["name"] == "documented"


def test_filter_functions_status_fix():
    """Filter only undocumented functions."""
    functions = [
        {"name": "documented", "has_docstring": True, "file_path": "test.py"},
        {"name": "undocumented", "has_docstring": False, "file_path": "test.py"},
    ]

    filtered = filter_functions(functions, status="Fix")

    assert len(filtered) == 1
    assert filtered[0]["name"] == "undocumented"


def test_filter_functions_combined_search_and_status():
    """Combine search + status filters."""
    functions = [
        {"name": "test_doc", "has_docstring": True, "file_path": "test.py"},
        {"name": "test_undoc", "has_docstring": False, "file_path": "test.py"},
        {"name": "other_doc", "has_docstring": True, "file_path": "test.py"},
    ]

    filtered = filter_functions(functions, search="test", status="OK")

    assert len(filtered) == 1
    assert filtered[0]["name"] == "test_doc"

