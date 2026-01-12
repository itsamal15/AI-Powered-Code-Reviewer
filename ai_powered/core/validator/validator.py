'''class CodeValidator:
    def validate(self, func_obj):
        report = {}

        doc = func_obj.get("docstring", "") or ""
        report["has_docstring"] = bool(doc.strip())

        report["missing_params"] = []

        # args are now dicts: {"name": ..., "type": ...}
        for arg in func_obj.get("args", []):
            arg_name = arg["name"]
            if arg_name not in doc:
                report["missing_params"].append(arg_name)

        report["status"] = (
            "PASS"
            if report["has_docstring"] and not report["missing_params"]
            else "FAIL"
        )

        return report
'''
import ast
from pathlib import Path


class CodeValidator:
    """
    PEP 257-based code validator (minimal ruleset).
    """

    def validate_file(self, file_path):
        """
        Validate a Python file and return violations.
        """
        source = Path(file_path).read_text()
        tree = ast.parse(source)
        lines = source.splitlines()

        violations = []

        for node in ast.walk(tree):
            # -----------------------------
            # Class validation (D101)
            # -----------------------------
            if isinstance(node, ast.ClassDef):
                if not ast.get_docstring(node):
                    violations.append({
                        "code": "D101",
                        "line": node.lineno,
                        "message": f"Missing docstring in public class {node.name}"
                    })

            # -----------------------------
            # Function validation (D103)
            # -----------------------------
            if isinstance(node, ast.FunctionDef):
                doc = ast.get_docstring(node)

                if not doc:
                    violations.append({
                        "code": "D103",
                        "line": node.lineno,
                        "message": f"Missing docstring in public function {node.name}"
                    })
                else:
                    # -----------------------------
                    # D202: No blank line after docstring
                    # -----------------------------
                    doc_node = node.body[0]
                    doc_end = doc_node.end_lineno

                    if doc_end < len(lines):
                        next_line = lines[doc_end].strip()
                        if next_line == "":
                            violations.append({
                                "code": "D202",
                                "line": doc_end + 1,
                                "message": (
                                    f"No blank lines allowed after function "
                                    f"docstring in {node.name}"
                                )
                            })

        return violations
