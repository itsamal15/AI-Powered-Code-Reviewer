from pathlib import Path
import ast
'''
def apply_docstring(file_path, lineno, new_docstring):
    """
    Insert a docstring inside a function body in a PEP 257 compliant way.
    """

    file_path = Path(file_path)
    lines = file_path.read_text().splitlines()

    # AST lineno is 1-based → convert to 0-based
    func_def_index = lineno - 1

    # Detect indentation of function body
    def_line = lines[func_def_index]
    base_indent = def_line[: len(def_line) - len(def_line.lstrip())]
    doc_indent = base_indent + " " * 4

    # Prepare formatted docstring
    formatted = []
    for line in new_docstring.splitlines():
        formatted.append(doc_indent + line if line.strip() else line)

    # Insert *after* function definition line
    insert_at = func_def_index + 1
    lines[insert_at:insert_at] = formatted

    file_path.write_text("\n".join(lines) + "\n")
    return True
'''


def apply_docstring(file_path, func_name, new_docstring):
    """
    Safely insert or replace a docstring for a specific function.
    """

    file_path = Path(file_path)
    source = file_path.read_text()
    tree = ast.parse(source)

    lines = source.splitlines()

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            # Determine indentation
            def_line = lines[node.lineno - 1]
            base_indent = def_line[: len(def_line) - len(def_line.lstrip())]
            doc_indent = base_indent + " " * 4

            formatted = [
                doc_indent + line if line.strip() else line
                for line in new_docstring.splitlines()
            ]

            # If docstring exists → replace
            if ast.get_docstring(node):
                doc_node = node.body[0]
                start = doc_node.lineno - 1
                end = doc_node.end_lineno
                lines[start:end] = formatted
            else:
                # Insert after def line
                insert_at = node.lineno
                lines[insert_at:insert_at] = formatted

            file_path.write_text("\n".join(lines) + "\n")
            return True

    return False

def remove_docstring(file_path, lineno):
    """
    Remove a docstring from a function body.
    """

    file_path = Path(file_path)
    lines = file_path.read_text().splitlines()

    # AST lineno is 1-based → convert to 0-based
    func_def_index = lineno - 1

    # Detect indentation of function body
    def_line = lines[func_def_index]
    base_indent = def_line[: len(def_line) - len(def_line.lstrip())]
    doc_indent = base_indent + " " * 4

    # Find docstring boundaries
    start_index = None
    end_index = None

    for i in range(func_def_index + 1, len(lines)):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith(('"""', "'''")):
            if start_index is None:
                start_index = i
                if stripped.count('"""') == 2 or stripped.count("'''") == 2:
                    end_index = i
                    break
            else:
                end_index = i
                break
        elif start_index is not None and not stripped:
            continue
        elif start_index is not None:
            break

    if start_index is not None and end_index is not None:
        del lines[start_index : end_index + 1]
        file_path.write_text("\n".join(lines) + "\n")
        return True

    return False



