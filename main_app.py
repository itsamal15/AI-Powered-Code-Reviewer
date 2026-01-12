import streamlit as st
from pathlib import Path
import json
import pandas as pd

from radon.complexity import cc_visit
from radon.metrics import mi_visit
from pathlib import Path



# ---- Import Core Modules (Update paths as per your.logic) ---- #
from ai_powered.core.parser.python_parser import PythonParser
from ai_powered.core.docstring_engine.generator import DocstringGenerator
from ai_powered.core.validator.validator import CodeValidator
from ai_powered.core.reporter.coverage_reporter import CoverageReporter
from ai_powered.core.docstring_engine.docstring_writer import apply_docstring
from dashboard_ui.dashboard import render_dashboard

# Global storage path (User editable in UI)
DEFAULT_JSON_PATH = "storage/review_logs.json"

# ============================================================
# Custom CSS Styling
# ============================================================
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Home page specific styles */
    .home-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
        text-align: center;
    }
    
    .home-header h1 {
        margin: 0;
        font-size: 2.5em;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    /* Metric cards styling */
    .metric-card {
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        border-left-color: #764ba2;
    }
    
    .metric-label {
        color: #666;
        font-size: 0.9em;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }
    
    .metric-value {
        font-size: 2.5em;
        font-weight: 700;
        color: #667eea;
        margin: 0;
    }
    
    /* Info box styling */
    .info-box {
        background: linear-gradient(135deg, #e0f7ff 0%, #e8f5f9 100%);
        border-left: 5px solid #00bcd4;
        padding: 20px;
        border-radius: 8px;
        margin: 20px 0;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        border: none;
        padding: 12px 30px;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Divider styling */
    .divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 30px 0;
    }
    
    /* Page header styling */
    .page-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
    }
    
    .page-header h2 {
        margin: 0;
        font-size: 1.8em;
        font-weight: 700;
    }
    
    /* Code comparison styling */
    .code-section {
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid #e0e0e0;
    }
    
    .code-section-title {
        font-size: 1.1em;
        font-weight: 600;
        color: #667eea;
        margin-bottom: 15px;
        border-bottom: 2px solid #667eea;
        padding-bottom: 10px;
    }
    
    /* Styled subheader */
    h3 {
        color: #667eea;
        border-bottom: 2px solid #f0f0f0;
        padding-bottom: 10px;
        margin-top: 20px;
    }
    
    /* Function selector styling */
    .stSelectbox [data-testid="stSelectbox"] {
        border-radius: 8px;
    }
    
    /* Validation results styling */
    .validation-result {
        background: #f5f5f5;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
    }
    
    /* JSON display styling */
    .stJson {
        border-radius: 8px;
        background: #f8f9fa;
        padding: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# Helper Functions
# ============================================================

def scan_code(path_to_scan):
    parser = PythonParser()
    functions = parser.extract_functions(path_to_scan)
    coverage = CoverageReporter(functions)
    return functions, coverage.get_metrics()


def generate_docstring(selected_function, style="numpy"):
    generator = DocstringGenerator(style=style)
    return generator.generate_docstring(selected_function)


def validate_code(func_obj):
    validator = CodeValidator()
    return validator.validate(func_obj)


def save_logs(data, output_path):
    with open(output_path, "w") as file:
        json.dump(data, file, indent=4)


# ============================================================
# UI Layout 🎨
# ============================================================

st.set_page_config(page_title="AI Code Reviewer", layout="wide")
st.sidebar.title("🧠 AI Code Reviewer")

view = st.sidebar.selectbox("Select View", ["Home", "Docstrings", "Validation", "Metrics", "Dashboard"])

path_to_scan = st.sidebar.text_input("Path to scan", value="examples")
output_json_path = st.sidebar.text_input("Output JSON path", value=DEFAULT_JSON_PATH)

if st.sidebar.button("Scan"):
    st.session_state["functions"], st.session_state["metrics"] = scan_code(path_to_scan)
    st.sidebar.success("Scan completed")


# Initialize session state
if "functions" not in st.session_state:
    st.session_state["functions"] = {}
if "metrics" not in st.session_state:
    st.session_state["metrics"] = {}


# ============================================================
# HOME VIEW
# ============================================================

if view == "Home":
    # Styled header
    st.markdown("""
    <div class="home-header">
        <h1>📊 AI-Powered Code Reviewer</h1>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state["metrics"]:
        total = st.session_state["metrics"]["total_functions"]
        documented = st.session_state["metrics"]["documented"]
        coverage = st.session_state["metrics"]["coverage_percent"]

        # Styled metrics display
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📊 Coverage</div>
                <div class="metric-value">{coverage}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📁 Total Functions</div>
                <div class="metric-value">{total}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📝 Documented</div>
                <div class="metric-value">{documented}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Info section with styled box
        st.markdown("""
        <div class="info-box">
            <h3>ℹ️ Documentation Status</h3>
            <ul>
                <li>Coverage shows existing documentation only</li>
                <li>Previewed fixes do <strong>not</strong> update coverage</li>
                <li>Coverage updates only after real fixes are saved</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        if st.button("⬇️ Download Coverage Report JSON"):
            save_logs(st.session_state["metrics"], output_json_path)
            st.success("✅ Report saved successfully!")
    
    else:
        st.markdown("""
        <div class="info-box">
            <h3>👋 Welcome to AI Code Reviewer!</h3>
            <p>Start by scanning a folder in the sidebar to analyze your Python code quality and generate documentation.</p>
        </div>
        """, unsafe_allow_html=True)




# ============================================================
# VALIDATION VIEW
# ============================================================

elif view == "Validation":
    st.markdown("""
    <div class="page-header">
        <h2>🔍 Code Validation & Quality Analysis</h2>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.get("functions"):
        functions = st.session_state["functions"]

        # -----------------------------
        # Group functions by file
        # -----------------------------
        files = {}
        for func in functions.values():
            file_path = func["file"]
            files.setdefault(file_path, []).append(func)

        validator = CodeValidator()

        all_violations = {}

        for file_path in files:
            violations = validator.validate_file(file_path)
            if violations:
                all_violations[file_path] = violations

        total_functions = len(functions)
        files_with_issues = len(all_violations)

        # -----------------------------
        # Summary metrics
        # -----------------------------
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Functions", total_functions)
        col2.metric("Valid Files", len(files) - files_with_issues)
        col3.metric("Issues", sum(len(v) for v in all_violations.values()))


                # -----------------------------
        # Compliance bar chart
        # -----------------------------
        total_files = len(files)
        violating_files = len(all_violations)
        compliant_files = total_files - violating_files

        chart_df = pd.DataFrame({
            "Status": ["Compliant", "Violations"],
            "Count": [compliant_files, violating_files]
        })

        st.bar_chart(
            chart_df.set_index("Status"),
            height=300
        )

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        st.markdown("### 📋 Detailed Results")

        search_term = st.text_input(
            "🔎 Search files or functions...",
            placeholder="Type name..."
        ).lower()

        # -----------------------------
        # Render violations
        # -----------------------------
        if all_violations:
            for file_path, violations in all_violations.items():
                file_name = file_path.split("\\")[-1]

                if search_term and search_term not in file_name.lower():
                    continue

                with st.expander(f"📁 {file_name} ({len(violations)} violations)"):
                    for v in violations:
                        code = v["code"]
                        msg = v["message"]
                        line = v["line"]

                        if code.startswith("D1"):
                            st.error(f"🔴 {code} (line {line}): {msg}")
                        else:
                            st.warning(f"🟡 {code} (line {line}): {msg}")
        else:
            st.success("✅ No PEP 257 violations found!")

    else:
        st.info("👈 Please scan a folder first to run validation.")

# ============================================================
# DOCSTRING VIEW
# ============================================================

elif view == "Docstrings":
    st.markdown("""
    <div class="page-header">
        <h2>📝 Docstring Review & Enhancement</h2>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state["functions"]:
        func_names = list(st.session_state["functions"].keys())
        selected_func_name = st.selectbox("Select Function to Review", func_names)

        selected_func = st.session_state["functions"][selected_func_name]
        before_doc = selected_func.get("docstring") or ""

        # Function metadata
        with st.expander("📋 Function Details", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("File", selected_func.get("file", "N/A").split("\\")[-1])
            
            start_line = selected_func.get("lineno", "N/A")
            end_line = selected_func.get("end_lineno", "N/A")
            col2.metric("Start Line", start_line)
            col3.metric("End Line", end_line)
            
            col4.metric("Has Docstring", "✅ Yes" if before_doc.strip() else "❌ No")

        # Style selection
        st.markdown("### ⚙️ Configuration")
        style = st.selectbox("Choose Docstring Style", ["NumPy", "Google", "reST"])
        

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Before/After comparison
        st.markdown("### 📊 Comparison View")
        col_before, col_after = st.columns(2)
        
        with col_before:
            st.markdown("""
            <div class="code-section">
                <div class="code-section-title">❌ Before</div>
            </div>
            """, unsafe_allow_html=True)
            if before_doc.strip():
                st.success("Existing docstring found")
                st.code(before_doc, language='python')
            else:
                st.error("No existing docstring")
                st.code(f"def {selected_func_name}():\n    pass", language='python')

        with col_after:
            st.markdown("""
            <div class="code-section">
                <div class="code-section-title">✅ After (Preview)</div>
            </div>
            """, unsafe_allow_html=True)
            preview = generate_docstring(selected_func, style)
            st.success("Generated docstring")
            st.code(preview, language='python')
            
            # Accept button directly below generated docstring
            if st.button("✅ Accept & Apply", use_container_width=True, key="apply_docstring"):
                file_path = selected_func["file"]
                func_name = selected_func["name"]
                success = apply_docstring(file_path, func_name, preview)

                if success:
                    st.success("✔️ Docstring successfully applied!")
                    selected_func["docstring"] = preview
                    st.session_state["functions"][selected_func_name] = selected_func
                else:
                    st.error("Failed to apply docstring.")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="info-box">
            <h3>👈 No functions found</h3>
            <p>Please scan a folder first in the sidebar to get started!</p>
        </div>
        """, unsafe_allow_html=True)

elif view == "Metrics":
    st.markdown("""
    <div class="page-header">
        <h2>📐 Code Metrics</h2>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.get("functions"):
        st.info("👈 Scan a folder first to view metrics.")
        st.stop()

    # -----------------------------
    # File selector
    # -----------------------------
    files = sorted({f["file"] for f in st.session_state["functions"].values()})
    selected_file = st.selectbox("Select File", files)

    source = Path(selected_file).read_text()

    # -----------------------------
    # Maintainability Index
    # -----------------------------
    mi = round(mi_visit(source, False), 2)
    st.markdown("### Maintainability Index")
    st.metric("MI", mi)

    # -----------------------------
    # Cyclomatic Complexity
    # -----------------------------
    st.markdown("### Function Complexity")

    complexities = []
    for block in cc_visit(source):
        complexities.append({
            "name": block.name,
            "complexity": block.complexity,
            "line": block.lineno
        })

    st.json(complexities)

elif view == "Dashboard":
    render_dashboard()







# ============================================================
# METRICS VIEW
# ============================================================

# elif view == "Metrics":
#     st.markdown("""
#     <div class="page-header">
#         <h2>📊 Documentation Metrics & Analytics</h2>
#     </div>
#     """, unsafe_allow_html=True)

#     if st.session_state["metrics"]:
#         metrics = st.session_state["metrics"]
        
#         # Overview metrics
#         st.markdown("### 📈 Overview")
#         col1, col2, col3, col4 = st.columns(4)
        
#         with col1:
#             st.metric("Total Functions", metrics.get("total_functions", 0))
#         with col2:
#             st.metric("Documented", metrics.get("documented", 0))
#         with col3:
#             st.metric("Coverage", f"{metrics.get('coverage', 0)}%")
#         with col4:
#             gap = metrics.get("total_functions", 0) - metrics.get("documented", 0)
#             st.metric("To Document", gap)
        
#         st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
#         st.markdown("### 📋 Detailed Metrics")
        
#         tab1, tab2, tab3 = st.tabs(["Summary", "Raw Data", "Export"])
        
#         with tab1:
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.markdown("#### Statistics")
#                 for key, value in metrics.items():
#                     if key != "coverage":
#                         st.write(f"**{key.replace('_', ' ').title()}:** {value}")
#             with col2:
#                 st.markdown("#### Progress")
#                 coverage = metrics.get("coverage", 0)
#                 st.progress(coverage / 100)
#                 st.caption(f"Documentation coverage: {coverage}%")
#                 st.markdown("""
#                 **Coverage Guide:**
#                 - 🟢 90-100%: Excellent
#                 - 🟡 70-89%: Good
#                 - 🔴 Below 70%: Needs work
#                 """)
        
#         with tab2:
#             st.markdown("#### Full Metrics Data")
#             st.json(metrics)
        
#         with tab3:
#             st.markdown("#### Export Options")
#             col1, col2 = st.columns(2)
#             with col1:
#                 if st.button("💾 Save as JSON", use_container_width=True):
#                     save_logs(metrics, output_json_path)
#                     st.success(f"✅ Saved to {output_json_path}")
#             with col2:
#                 if st.button("📋 Copy JSON", use_container_width=True):
#                     st.code(json.dumps(metrics, indent=2), language="json")
#     else:
#         st.markdown("""
#         <div class="info-box">
#             <h3>📊 No metrics available</h3>
#             <p>Scan a folder first in the sidebar to generate metrics!</p>
#         </div>
#         """, unsafe_allow_html=True)





# '''
# elif view == "Validation":
#     st.markdown("""
#     <div class="page-header">
#         <h2>🔍 Code Validation & Quality Analysis</h2>
#     </div>
#     """, unsafe_allow_html=True)

#     if st.session_state["functions"]:
#         functions = st.session_state["functions"]
        
#         # Summary metrics
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.metric("Total Functions", len(functions))
#         with col2:
#             valid_count = sum(1 for f in functions.values() if validate_code(f).get("valid", True))
#             st.metric("Valid", valid_count)
#         with col3:
#             invalid = len(functions) - valid_count
#             st.metric("Issues", invalid)
        
#         st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
#         st.markdown("### 📋 Detailed Results")
#         search_term = st.text_input("🔎 Search functions...", placeholder="Type function name...")
        
#         filtered_functions = {
#             name: func for name, func in functions.items()
#             if search_term.lower() in name.lower()
#         } if search_term else functions
        
#         if filtered_functions:
#             for name, func in filtered_functions.items():
#                 results = validate_code(func)
#                 with st.expander(f"📌 {name}", expanded=False):
#                     col1, col2 = st.columns([1, 3])
#                     with col1:
#                         if results.get("valid", True):
#                             st.success("✅ Valid")
#                         else:
#                             st.error("⚠️ Issues")
#                     with col2:
#                         st.json(results)
#         else:
#             st.info(f"No functions matching '{search_term}'")

#     else:
#         st.markdown("""
#         <div class="info-box">
#             <h3>👈 No functions found</h3>
#             <p>Please scan a folder first in the sidebar to get started!</p>
#         </div>
#         """, unsafe_allow_html=True)
# '''