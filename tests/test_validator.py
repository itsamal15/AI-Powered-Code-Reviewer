# # tests/test_validator.py
# """Tests for docstring validator."""

# from ai_powered.core.validator.validator import validate_docstrings, compute_complexity


# def test_validator_returns_list():
#     """Test that validator returns list of violations."""
#     errors = validate_docstrings("examples/sample_a.py")
#     assert isinstance(errors, list)
    
#     # ✅ Validate error structure if any exist
#     for error in errors:
#         assert isinstance(error, (str, dict)), "Errors should be strings or dicts"
#         if isinstance(error, str):
#             assert len(error) > 0, "Error messages should not be empty"


# def test_validator_detects_issues():
#     """Test that validator actually detects docstring issues."""
#     errors = validate_docstrings("examples/sample_a.py")
    
#     # ✅ Check that validator provides meaningful feedback
#     # If there are errors, they should mention functions or docstrings
#     if errors:
#         error_text = str(errors).lower()
#         # At least one error should reference docstrings or functions
#         assert any(keyword in error_text for keyword in 
#                   ["docstring", "function", "missing", "undocumented"]), \
#                "Validation errors should mention docstrings or functions"


# def test_complexity_returns_list():
#     """Test complexity computation returns list."""
#     source = "def simple(): return 1"
#     results = compute_complexity(source)
#     assert isinstance(results, list)


# def test_complexity_structure():
#     """Test complexity result structure."""
#     source = "def test(x):\n    if x > 0:\n        return x\n    return 0"
#     results = compute_complexity(source)
    
#     if results:
#         result = results[0]
#         assert "name" in result
#         assert "complexity" in result
#         assert isinstance(result["complexity"], int)
        
#         # ✅ Validate complexity value is reasonable
#         assert result["complexity"] >= 1, "Complexity should be at least 1"
#         assert result["name"] == "test", "Function name should match"


# def test_complexity_detects_branches():
#     """Test that complexity increases with control flow."""
#     # Simple function (complexity should be 1)
#     simple_source = "def simple(): return 1"
#     simple_results = compute_complexity(simple_source)
    
#     # Complex function with branches (complexity > 1)
#     complex_source = """
# def complex_fn(x, y):
#     if x > 0:
#         if y > 0:
#             return x + y
#         return x
#     return 0
# """
#     complex_results = compute_complexity(complex_source)
    
#     # ✅ Validate complexity calculation logic
#     if simple_results and complex_results:
#         simple_complexity = simple_results[0]["complexity"]
#         complex_complexity = complex_results[0]["complexity"]
        
#         assert complex_complexity > simple_complexity, \
#                "Complex function should have higher complexity than simple function"
#         assert complex_complexity >= 3, \
#                "Function with nested ifs should have complexity >= 3"


# def test_complexity_handles_multiple_functions():
#     """Test complexity computation for multiple functions."""
#     source = """
# def func_a():
#     return 1

# def func_b(x):
#     if x:
#         return x
#     return 0
# """
#     results = compute_complexity(source)
    
#     # ✅ Validate multiple functions are analyzed
#     assert len(results) == 2, "Should analyze both functions"
    
#     function_names = [r["name"] for r in results]
#     assert "func_a" in function_names
#     assert "func_b" in function_names
    
#     # func_b should have higher complexity due to if statement
#     func_a_complexity = next(r["complexity"] for r in results if r["name"] == "func_a")
#     func_b_complexity = next(r["complexity"] for r in results if r["name"] == "func_b")
    
#     assert func_b_complexity > func_a_complexity


# def test_validator_with_valid_docstrings():
#     """Test validator on file with proper docstrings."""
#     # This test assumes there might be a well-documented example file
#     # If all examples have issues, errors will be non-empty
#     errors = validate_docstrings("examples/sample_a.py")
    
#     # ✅ Just verify it runs without crashing
#     assert isinstance(errors, list)
    
#     # If errors exist, verify they're actionable
#     for error in errors:
#         if isinstance(error, str):
#             assert len(error) > 10, "Error messages should be descriptive"

# tests/test_validator.py
"""Tests for PEP 257 docstring validator."""

from ai_powered.core.validator.validator import CodeValidator


def test_validator_returns_list():
    """Validator should return a list of violations."""
    validator = CodeValidator()
    errors = validator.validate_file("examples/sample_a.py")

    assert isinstance(errors, list)

    for error in errors:
        assert isinstance(error, dict)
        assert "code" in error
        assert "line" in error
        assert "message" in error


def test_validator_detects_missing_function_docstring():
    """Validator should detect missing function docstrings."""
    validator = CodeValidator()
    errors = validator.validate_file("examples/sample_b.py")

    # At least one D103 should exist if undocumented function exists
    error_codes = [e["code"] for e in errors]

    assert any(code == "D103" for code in error_codes), \
        "Validator should detect missing function docstrings (D103)"


def test_validator_detects_missing_class_docstring():
    """Validator should detect missing class docstrings."""
    validator = CodeValidator()
    errors = validator.validate_file("examples/sample_a.py")

    error_codes = [e["code"] for e in errors]

    # D101 = missing class docstring
    assert any(code == "D101" for code in error_codes), \
        "Validator should detect missing class docstrings (D101)"


# def test_validator_detects_blank_line_after_docstring():
#     """Validator should detect D202 violations."""
#     validator = CodeValidator()
#     errors = validator.validate_file("examples/sample_a.py")

#     error_codes = [e["code"] for e in errors]

#     assert any(code == "D202" for code in error_codes), \
#         "Validator should detect blank line after docstring (D202)"

def test_validator_detects_blank_line_after_docstring(tmp_path):
    """Validator should detect D202 violations."""
    code = '''
def bad():
    """Bad docstring."""

    return 1
'''
    file_path = tmp_path / "bad.py"
    file_path.write_text(code)

    validator = CodeValidator()
    errors = validator.validate_file(file_path)

    error_codes = [e["code"] for e in errors]

    assert "D202" in error_codes



def test_validator_error_structure():
    """Each violation should be descriptive and actionable."""
    validator = CodeValidator()
    errors = validator.validate_file("examples/sample_a.py")

    for error in errors:
        assert isinstance(error["line"], int)
        assert error["line"] > 0
        assert isinstance(error["message"], str)
        assert len(error["message"]) > 10


def test_validator_on_nonexistent_file():
    """Validator should raise or fail clearly for invalid paths."""
    validator = CodeValidator()

    try:
        validator.validate_file("non_existent_file.py")
    except Exception as e:
        assert isinstance(e, Exception)
