'''import ast
from pathlib import Path


class PythonParser:
    def extract_functions(self, folder_path):
        folder = Path(folder_path)
        functions = {}

        for py_file in folder.rglob("*.py"):
            source = py_file.read_text()
            tree = ast.parse(source, filename=str(py_file))

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    docstring = ast.get_docstring(node)
                    functions[node.name] = {
                        "name": node.name,
                        "args": [arg.arg for arg in node.args.args],
                        "docstring": docstring or "",
                        
                        "file": str(py_file),
                        "lineno": node.lineno,
                        "end_lineno": node.end_lineno or node.lineno
                    }

        return functions
'''

import ast
from pathlib import Path


class PythonParser:
    def extract_functions(self, folder_path):
        folder = Path(folder_path)
        functions = {}

        for py_file in folder.rglob("*.py"):
            source = py_file.read_text()
            tree = ast.parse(source, filename=str(py_file))

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    docstring = ast.get_docstring(node)

                    # ---- Extract arguments with type hints ----
                    args = []
                    for arg in node.args.args:
                        arg_info = {
                            "name": arg.arg,
                            "type": ast.unparse(arg.annotation) if arg.annotation else None
                        }
                        args.append(arg_info)

                    # ---- Extract return type hint ----
                    return_type = ast.unparse(node.returns) if node.returns else None

                    functions[node.name] = {
                        "name": node.name,
                        "args": args,                      # <-- list of dicts
                        "returns": return_type,            # <-- NEW
                        "docstring": docstring or "",
                        "has_docstring": bool(docstring),
                        "file": str(py_file),
                        "lineno": node.lineno,
                        "end_lineno": node.end_lineno or node.lineno
                    }

        return functions
    


def parse_path(folder_path):
    """
    Parse all Python files in a folder.

    Returns:
        list[dict]: [{ file_path, functions }]
    """
    parser = PythonParser()
    functions = parser.extract_functions(folder_path)

    return [{
        "file_path": str(folder_path),
        "functions": list(functions.values())
    }]


def parse_file(file_path):
    """
    Parse a single Python file.

    Returns:
        dict: { file_path, functions }
    """
    file_path = Path(file_path)
    parser = PythonParser()

    source = file_path.read_text()
    tree = ast.parse(source, filename=str(file_path))

    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            docstring = ast.get_docstring(node)

            args = [{
                "name": arg.arg,
                "type": ast.unparse(arg.annotation) if arg.annotation else None
            } for arg in node.args.args]

            functions.append({
                "name": node.name,
                "args": args,
                "returns": ast.unparse(node.returns) if node.returns else None,
                "docstring": docstring or "",
                "has_docstring": bool(docstring),
                "file": str(file_path),
                "lineno": node.lineno,
                "end_lineno": node.end_lineno or node.lineno
            })

    return {
        "file_path": str(file_path),
        "functions": functions
    }
'''

import ast
from pathlib import Path


def parse_file(file_path: str) -> dict:
    """
    Parse a single Python file and extract function metadata.
    """
    file_path = Path(file_path)
    source = file_path.read_text(encoding="utf-8")

    tree = ast.parse(source, filename=str(file_path))
    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            docstring = ast.get_docstring(node)

            functions.append({
                "name": node.name,
                "args": [{"name": arg.arg} for arg in node.args.args],
                "has_docstring": bool(docstring),
                "docstring": docstring or "",
                "lineno": node.lineno,
                "end_lineno": getattr(node, "end_lineno", node.lineno),
                "file": str(file_path)
            })

    return {
        "file_path": str(file_path),
        "functions": functions
    }


# -------------------------------------------------
# Parse a folder (recursive)
# -------------------------------------------------

def parse_path(path: str) -> list:
    """
    Parse all Python files in a directory recursively.
    """
    path = Path(path)
    results = []

    if path.is_file() and path.suffix == ".py":
        results.append(parse_file(path))
        return results

    if not path.exists():
        return []

    for py_file in path.rglob("*.py"):
        results.append(parse_file(py_file))

    return results
'''