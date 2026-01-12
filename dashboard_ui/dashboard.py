# import json
# from pathlib import Path


# def load_pytest_results():
#     """
#     Load pytest results if available.

#     Returns:
#         dict | None
#     """
#     results_path = Path("pytest_results.json")

#     if not results_path.exists():
#         return None

#     try:
#         return json.loads(results_path.read_text())
#     except Exception:
#         return None


# def filter_functions(functions, search=None, status=None):
#     """
#     Filter functions by search term and documentation status.

#     Args:
#         functions (list[dict]): Function metadata
#         search (str | None): Search term for function name
#         status (str | None): "OK" (documented) or "Fix" (undocumented)

#     Returns:
#         list[dict]
#     """
#     filtered = functions

#     # ---- Search filter ----
#     if search:
#         search = search.lower()
#         filtered = [
#             f for f in filtered
#             if search in f.get("name", "").lower()
#         ]

#     # ---- Status filter ----
#     if status == "OK":
#         filtered = [
#             f for f in filtered
#             if f.get("has_docstring") is True
#         ]
#     elif status == "Fix":
#         filtered = [
#             f for f in filtered
#             if f.get("has_docstring") is False
#         ]

#     return filtered

import json
from pathlib import Path
import streamlit as st
import pandas as pd


# -------------------------------------------------
# Data helpers
# -------------------------------------------------

def load_pytest_results():
    """
    Load pytest results if available.

    Returns:
        dict | None
    """
    results_path = Path("storage/reports/pytest_results.json")

    if not results_path.exists():
        return None

    try:
        return json.loads(results_path.read_text())
    except Exception:
        return None


def filter_functions(functions, search=None, status=None):
    """
    Filter functions by search term and documentation status.
    """
    filtered = functions

    if search:
        search = search.lower()
        filtered = [
            f for f in filtered
            if search in f.get("name", "").lower()
        ]

    if status == "OK":
        filtered = [f for f in filtered if f.get("has_docstring")]
    elif status == "Fix":
        filtered = [f for f in filtered if not f.get("has_docstring")]

    return filtered




def render_dashboard():
    import streamlit as st
    import json
    import pandas as pd
    from pathlib import Path
    import subprocess

    # ---------------------------
    # Page header
    # ---------------------------
    st.markdown("""
    <div class="page-header">
        <h2>📊 Dashboard</h2>
    </div>
    """, unsafe_allow_html=True)

    # ---------------------------
    # Session state init
    # ---------------------------
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "Filters"

    if "tests_ran" not in st.session_state:
        st.session_state.tests_ran = False

    # ---------------------------
    # Top navigation buttons
    # ---------------------------
    cols = st.columns(5)

    if cols[0].button("🛠 Advanced Filters"):
        st.session_state.active_tab = "Filters"

    if cols[1].button("🔍 Search"):
        st.session_state.active_tab = "Search"

    if cols[2].button("📤 Export"):
        st.session_state.active_tab = "Export"

    if cols[3].button("🧪 Tests"):
        st.session_state.active_tab = "Tests"

    if cols[4].button("💡 Help & Tips"):
        st.session_state.active_tab = "Help"

    st.markdown("---")

    # =========================================================
    # 🧪 TESTS TAB
    # =========================================================
    if st.session_state.active_tab == "Tests":

        st.markdown("""
        <div style="background:#0ea5e9;padding:20px;border-radius:12px;color:white">
        <h3>🧪 Tests</h3>
        <p>Run and visualize pytest results</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("▶️ Run Tests"):
            with st.spinner("Running pytest..."):
                subprocess.run(
                    [
                        "pytest",
                        "tests",
                        "--json-report",
                        "--json-report-file=storage/reports/pytest_results.json",
                    ],
                    shell=True,
                )
            st.session_state.tests_ran = True
            st.success("Tests executed successfully!")

        # ---------------------------
        # Show results ONLY after Run Tests
        # ---------------------------
        if not st.session_state.tests_ran:
            st.info("No test results found. Click **Run Tests** to execute pytest.")
            return

        report_path = Path("storage/reports/pytest_results.json")
        if not report_path.exists():
            st.error("pytest report not found.")
            return

        results = json.loads(report_path.read_text())
        tests = results.get("tests", [])

        # ---------------------------
        # Aggregate by test file
        # ---------------------------
        suite_stats = {}

        for test in tests:
            suite = test["nodeid"].split("::")[0].replace("tests/", "").replace(".py", "")
            suite_stats.setdefault(suite, {"passed": 0, "failed": 0})

            if test["outcome"] == "passed":
                suite_stats[suite]["passed"] += 1
            elif test["outcome"] == "failed":
                suite_stats[suite]["failed"] += 1

        df = pd.DataFrame(
            [
                {
                    "Test Suite": suite.replace("_", " ").title(),
                    "Passed": stats["passed"],
                    "Failed": stats["failed"],
                }
                for suite, stats in suite_stats.items()
            ]
        ).set_index("Test Suite")

        # ---------------------------
        # BAR CHART (SECOND IMAGE STYLE)
        # ---------------------------
        st.markdown("### 📈 Test Results")
        st.bar_chart(df, height=350)

        # ---------------------------
        # Results list (green cards)
        # ---------------------------
        st.markdown("### 📋 Test Results by Category")

        for suite, stats in suite_stats.items():
            total = stats["passed"] + stats["failed"]

            if stats["failed"] == 0:
                st.success(f"✅ {suite.replace('_',' ').title()} — {stats['passed']}/{total} passed")
            else:
                st.warning(f"⚠️ {suite.replace('_',' ').title()} — {stats['passed']}/{total} passed")

    # =========================================================
    # 🛠 ADVANCED FILTERS
    # =========================================================
    # elif st.session_state.active_tab == "Filters":
    #     st.markdown("### 🛠 Advanced Filters")
    #     st.selectbox("Documentation status", ["All", "OK", "Fix"])
    elif st.session_state.active_tab == "Filters":

        st.markdown("""
        <div style="background:#0ea5e9;padding:18px;border-radius:12px;color:white">
            <h3>🛠 Advanced Filters</h3>
            <p>Filter dynamically by documentation status</p>
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------------------------
    # Load parsed functions (from session state)
    # -------------------------------------------------
        # functions = st.session_state.get("functions", [])

        functions = st.session_state.get("functions", {})

        if isinstance(functions, dict):
            functions = list(functions.values())


        if not functions:
            st.info("No functions found. Scan a folder first.")
            return

        total_count = len(functions)

    # -------------------------------------------------
    # Filter selector
    # -------------------------------------------------
        status = st.selectbox(
            "📄 Documentation status",
            ["All", "OK", "Fix"]
        )

    # -------------------------------------------------
    # Apply filter logic
    # -------------------------------------------------
        if status == "OK":
            filtered = [f for f in functions if f.get("has_docstring")]
        elif status == "Fix":
            filtered = [f for f in functions if not f.get("has_docstring")]
        else:
            filtered = functions
        showing_count = len(filtered)

    # -------------------------------------------------
    # Summary cards
    # -------------------------------------------------
        col1, col2 = st.columns(2)

        col1.markdown(f"""
        <div style="background:#0284c7;color:white;padding:20px;border-radius:12px;text-align:center">
            <h1>{showing_count}</h1>
            <p>Showing</p>
        </div>
        """, unsafe_allow_html=True)

        col2.markdown(f"""
        <div style="background:#0ea5e9;color:white;padding:20px;border-radius:12px;text-align:center">
            <h1>{total_count}</h1>
            <p>Total</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------
    # Results table
    # -------------------------------------------------
        # st.markdown("""
        # <table style="width:100%;border-collapse:collapse">
        #     <thead>
        #         <tr style="background:#0284c7;color:white">
        #             <th style="padding:10px;text-align:left">📁 FILE</th>
        #             <th style="padding:10px;text-align:left">🔧 FUNCTION</th>
        #             <th style="padding:10px;text-align:center">✅ DOCSTRING</th>
        #         </tr>
        #     </thead>
        #     <tbody>
        # """, unsafe_allow_html=True)

        # for fn in filtered:
        #     file_name = fn.get("file", fn.get("file_path", ""))
        #     func_name = fn.get("name", "")
        #     has_doc = fn.get("has_docstring", False)

        #     badge = (
        #         "<span style='background:#22c55e;color:white;padding:4px 10px;border-radius:999px'>Yes</span>"
        #         if has_doc else
        #         "<span style='background:#ef4444;color:white;padding:4px 10px;border-radius:999px'>No</span>"
        #     )
        #     st.markdown(f"""
        #     <tr style="border-bottom:1px solid #e5e7eb">
        #         <td style="padding:10px">{file_name}</td>
        #         <td style="padding:10px">{func_name}</td>
        #         <td style="padding:10px;text-align:center">{badge}</td>
        #     </tr>
        #     """, unsafe_allow_html=True)
        # st.markdown("""
        #     </tbody>
        # </table>
        # """, unsafe_allow_html=True)
        rows = []

        for fn in filtered:
            if not isinstance(fn, dict):
                continue

            rows.append({
                "File": fn.get("file") or fn.get("file_path", ""),
                "Function": fn.get("name", ""),
                "Docstring": "Yes" if fn.get("has_docstring") else "No"
            })

        df = pd.DataFrame(rows)
        def docstring_style(val):
            if val == "Yes":
                return (
                    "background-color:#22c55e;"
                    "color:white;"
                    "font-weight:600;"
                    "text-align:center;"
                    "border-radius:12px"
                )
            return (
                "background-color:#ef4444;"
                "color:white;"
                "font-weight:600;"
                "text-align:center;"
                "border-radius:12px"
            )
        
        
        styled_df = (
            df.style
            .applymap(docstring_style, subset=["Docstring"])
            .set_properties(**{"text-align": "left"}, subset=["File", "Function"])
        )
        row_height = 35
        table_height = min(500, (len(df) + 1) * row_height)

        df = df.reset_index(drop=True)


        st.dataframe(
            styled_df,
            use_container_width=True,
            height=table_height
        )



    # =========================================================
    # 🔍 SEARCH
    # =========================================================
    # elif st.session_state.active_tab == "Search":
    #     st.markdown("### 🔍 Search Functions")
    #     st.text_input("Enter function name")
    elif st.session_state.active_tab == "Search":

        st.markdown("""
        <div style="background:#0ea5e9;padding:18px;border-radius:12px;color:white">
            <h3>🔍 Search Functions</h3>
            <p>Instant search across all parsed functions</p>
        </div>
        """, unsafe_allow_html=True)

    # ---------------------------------
    # Load parsed functions
    # ---------------------------------
        functions = st.session_state.get("functions", {})

        if isinstance(functions, dict):
            functions = list(functions.values())

        if not functions:
            st.info("No functions available. Scan a folder first.")
            return

    # ---------------------------------
    # Search input
    # ---------------------------------
        query = st.text_input("🔎 Enter function name", placeholder="Type function name...")

        if not query:
            st.info("Start typing to search for a function.")
            return

        query_lower = query.lower()

        results = [
            fn for fn in functions
            if query_lower in fn.get("name", "").lower()
        ]

    # ---------------------------------
    # Result banner
    # ---------------------------------
        st.markdown(f"""
        <div style="background:#0284c7;color:white;padding:10px;border-radius:8px;
                text-align:center;margin-top:10px">
            {len(results)} result(s) found for "{query}"
        </div>
        """, unsafe_allow_html=True)

        if not results:
            return

    # ---------------------------------
    # Build table data
    # ---------------------------------
        rows = []
        for fn in results:
            rows.append({
                "File": fn.get("file", fn.get("file_path", "")),
                "Function": fn.get("name", ""),
                "Docstring": "Yes" if fn.get("has_docstring") else "No"
            })

        df = pd.DataFrame(rows).reset_index(drop=True)

    # ---------------------------------
    # Style docstring column
    # ---------------------------------
        def docstring_style(val):
            if val == "Yes":
                return "background-color:#22c55e;color:white;font-weight:bold;text-align:center"
            return "background-color:#ef4444;color:white;font-weight:bold;text-align:center"

        styled_df = (
            df.style
            .applymap(docstring_style, subset=["Docstring"])
            .set_properties(**{"text-align": "left"}, subset=["File", "Function"])
        )

    # ---------------------------------
    # Render table (no empty rows)
    # ---------------------------------
        row_height = 35
        table_height = min(400, (len(df) + 1) * row_height)

        st.dataframe(
            styled_df,
            use_container_width=True,
            height=table_height
        )


    # =========================================================
    # 📤 EXPORT
    # =========================================================
    # elif st.session_state.active_tab == "Export":
    #     st.markdown("### 📤 Export Data")
    #     st.download_button(
    #         "⬇️ Export JSON",
    #         data=json.dumps(results if "results" in locals() else {}, indent=2),
    #         file_name="analysis.json",
    #     )
    elif st.session_state.active_tab == "Export":

        st.markdown("""
        <div style="background:#0ea5e9;padding:18px;border-radius:12px;color:white">
            <h3>📤 Export Data</h3>
            <p>Download analysis results in JSON or CSV format</p>
        </div>
        """, unsafe_allow_html=True)

    # ---------------------------------
    # Load parsed functions
    # ---------------------------------
        functions = st.session_state.get("functions", {})

        if isinstance(functions, dict):
            functions = list(functions.values())

        if not functions:
            st.info("No data available. Scan a folder first.")
            return

        total = len(functions)
        documented = sum(1 for f in functions if f.get("has_docstring"))
        missing = total - documented

    # ---------------------------------
    # Export summary
    # ---------------------------------
        st.markdown("""
        <div style="background:#e0f2fe;padding:16px;border-radius:12px">
            <h4>📊 Export Summary</h4>
            <ul>
                <li><b>Total Functions:</b> {total}</li>
                <li><b>Documented:</b> {documented}</li>
                <li><b>Missing Docstrings:</b> {missing}</li>
            </ul>
        </div>
        """.format(
            total=total,
            documented=documented,
            missing=missing
        ), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------
    # Prepare export data
    # ---------------------------------
        export_rows = []
        for fn in functions:
            export_rows.append({
                "file": fn.get("file", fn.get("file_path", "")),
                "function": fn.get("name"),
                "has_docstring": fn.get("has_docstring"),
                "line_start": fn.get("lineno"),
                "line_end": fn.get("end_lineno"),
            })

        df = pd.DataFrame(export_rows)

    # ---------------------------------
    # Export buttons
    # ---------------------------------
        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                "📄 Export as JSON",
                data=json.dumps(export_rows, indent=2),
                file_name="analysis.json",
                mime="application/json",
                use_container_width=True
            )
            st.caption("📁 JSON format for programmatic access")

        with col2:
            st.download_button(
                "📊 Export as CSV",
                data=df.to_csv(index=False),
                file_name="analysis.csv",
                mime="text/csv",
                use_container_width=True
            )
            st.caption("📁 CSV format for Excel / spreadsheets")

    # =========================================================
    # 💡 HELP & TIPS
    # =========================================================
    elif st.session_state.active_tab == "Help":
        st.markdown("### 💡 Interactive Help & Tips")

        col1, col2 = st.columns(2)

        col1.info("""
        **Getting Started**
        - Enter path to scan
        - Click Scan
        - Review coverage
        - Generate docstrings
        """)

        col2.info("""
        **Docstring Styles**
        - Google
        - NumPy
        - reST
        """)

        st.info("""
        **Running Tests**
        - Click *Run Tests*
        - Results appear instantly
        - JSON stored in `storage/reports`
        """)






# -------------------------------------------------
# Dashboard UI
# -------------------------------------------------

# def render_dashboard():
#     st.markdown("""
#     <div class="page-header">
#         <h2>📊 Dashboard</h2>
#     </div>
#     """, unsafe_allow_html=True)

#     # results = load_pytest_results()

#     # # ---------------------------
#     # # Test Results Chart
#     # # ---------------------------
#     # st.markdown("### 📈 Test Results")

#     # if not results:
#     #     st.info("No pytest results found. Run tests to populate dashboard.")
#     #     return

#     # chart_rows = []
#     # summary_cards = []

#     # for suite, data in results.items():
#     #     if suite == "aggregate":
#     #         continue

#     #     passed = data.get("passed", 0)
#     #     failed = data.get("failed", 0)
#     #     total = passed + failed

#     #     chart_rows.append({
#     #         "Suite": suite.replace("_", " ").title(),
#     #         "Passed": passed,
#     #         "Failed": failed
#     #     })

#     #     summary_cards.append((suite, passed, total))

#     # df = pd.DataFrame(chart_rows).set_index("Suite")
#     # st.bar_chart(df, height=300)

#     # # ---------------------------
#     # # Test Status Cards
#     # # ---------------------------
#     # for suite, passed, total in summary_cards:
#     #     if passed == total:
#     #         st.success(f"✅ {suite.replace('_',' ').title()} — {passed}/{total} passed")
#     #     else:
#     #         st.warning(f"⚠️ {suite.replace('_',' ').title()} — {passed}/{total} passed")
#     results = load_pytest_results()

#     st.markdown("### 📈 Test Results")

#     if not results:
#         st.info("No pytest results found. Run tests to populate dashboard.")
#         return

#     summary = results.get("summary")

#     if not summary:
#         st.info("No test summary available.")
#         return
#     passed = summary.get("passed", 0)
#     failed = summary.get("failed", 0)
#     skipped = summary.get("skipped", 0)
#     total = summary.get("total", passed + failed + skipped)

#     st.bar_chart({
#         "Passed": passed,
#         "Failed": failed,
#         "Skipped": skipped
#     })

#     if failed == 0:
#         st.success(f"✅ All tests passed ({passed}/{total})")
#     else:
#         st.warning(f"⚠️ {failed} tests failed out of {total}")




#last working version
# def render_dashboard():
#     import json
#     import subprocess
#     import pandas as pd
#     import streamlit as st
#     from pathlib import Path

#     # ---------------------------
#     # Header
#     # ---------------------------
#     st.markdown("""
#     <div class="page-header">
#         <h2>📊 Dashboard</h2>
#     </div>
#     """, unsafe_allow_html=True)

#     # ---------------------------
#     # Session state
#     # ---------------------------
#     if "tests_ran" not in st.session_state:
#         st.session_state.tests_ran = False

#     # ---------------------------
#     # Tests Banner
#     # ---------------------------
#     st.markdown("""
#     <div style="
#         background: linear-gradient(90deg, #0ea5e9, #0284c7);
#         padding: 24px;
#         border-radius: 12px;
#         color: white;
#         margin-bottom: 16px;
#     ">
#         <h3>🧪 Tests</h3>
#         <p>Run and visualize pytest results</p>
#     </div>
#     """, unsafe_allow_html=True)

#     # ---------------------------
#     # Run Tests Button
#     # ---------------------------
#     if st.button("▶️ Run Tests"):
#         with st.spinner("Running pytest..."):
#             subprocess.run(
#                 [
#                     "pytest",
#                     "--json-report",
#                     "--json-report-file=storage/reports/pytest_results.json"
#                 ],
#                 capture_output=True,
#                 text=True
#             )
#         st.session_state.tests_ran = True
#         st.success("✅ Tests completed successfully")

#     # ---------------------------
#     # Show results ONLY after run
#     # ---------------------------
#     if not st.session_state.tests_ran:
#         st.info("No test results found. Click **Run Tests** to execute pytest and generate results.")
#         return

#     # ---------------------------
#     # Load pytest JSON
#     # ---------------------------
#     results_path = Path("storage/reports/pytest_results.json")

#     if not results_path.exists():
#         st.warning("Pytest report not found.")
#         return

#     results = json.loads(results_path.read_text())
#     tests = results.get("tests", [])

#     if not tests:
#         st.warning("No test case data found.")
#         return

#     # ---------------------------
#     # Aggregate by test file
#     # ---------------------------
#     suite_stats = {}

#     for test in tests:
#         nodeid = test.get("nodeid", "")
#         outcome = test.get("outcome", "")
#         suite = nodeid.split("::")[0]

#         suite_stats.setdefault(suite, {"passed": 0, "failed": 0})

#         if outcome == "passed":
#             suite_stats[suite]["passed"] += 1
#         elif outcome == "failed":
#             suite_stats[suite]["failed"] += 1

#     # ---------------------------
#     # Bar Chart (SECOND IMAGE)
#     # ---------------------------
#     rows = []
#     for suite, stats in suite_stats.items():
#         rows.append({
#             "Test Suite": suite.replace("tests/", "").replace(".py", ""),
#             "Passed": stats["passed"],
#             "Failed": stats["failed"]
#         })

#     df = pd.DataFrame(rows).set_index("Test Suite")

#     st.markdown("### 📈 Test Results")
#     st.bar_chart(df, height=350)

#     # ---------------------------
#     # Test Results by Category
#     # ---------------------------
#     st.markdown("### 📋 Test Results by Category")

#     for suite, stats in suite_stats.items():
#         passed = stats["passed"]
#         failed = stats["failed"]
#         total = passed + failed

#         label = (
#             suite.replace("tests/", "")
#                  .replace(".py", "")
#                  .replace("_", " ")
#                  .title()
#         )

#         if failed == 0:
#             st.success(f"✅ **{label}** — {passed}/{total} passed")
#         else:
#             st.warning(f"⚠️ **{label}** — {passed}/{total} passed")

#     # ---------------------------
#     # Download Report
#     # ---------------------------
#     st.markdown("---")
#     st.download_button(
#         "⬇️ Download Pytest Report JSON",
#         data=json.dumps(results, indent=2),
#         file_name="pytest_results.json",
#         mime="application/json"
#     )








# def render_dashboard():
#     import json
#     import pandas as pd
#     import streamlit as st
#     from pathlib import Path

#     st.markdown("""
#     <div class="page-header">
#         <h2>📊 Dashboard</h2>
#     </div>
#     """, unsafe_allow_html=True)

#     # ---------------------------
#     # Load pytest JSON report
#     # ---------------------------
#     results_path = Path("storage/reports/pytest_results.json")

#     if not results_path.exists():
#         st.info("No pytest results found. Run tests to populate dashboard.")
#         return

#     results = json.loads(results_path.read_text())
#     tests = results.get("tests", [])

#     if not tests:
#         st.info("No test case data found in report.")
#         return

#     # ---------------------------
#     # Suite-wise aggregation
#     # ---------------------------
#     suite_stats = {}

#     for test in tests:
#         nodeid = test.get("nodeid", "")
#         outcome = test.get("outcome", "")

#         # Group by test file
#         suite = nodeid.split("::")[0]  # tests/test_parser.py

#         suite_stats.setdefault(suite, {"passed": 0, "failed": 0})

#         if outcome == "passed":
#             suite_stats[suite]["passed"] += 1
#         elif outcome == "failed":
#             suite_stats[suite]["failed"] += 1

#     # ---------------------------
#     # Build DataFrame
#     # ---------------------------
#     rows = []
#     for suite, stats in suite_stats.items():
#         rows.append({
#             "Test Suite": suite.replace("tests/", "").replace(".py", ""),
#             "Passed": stats["passed"],
#             "Failed": stats["failed"]
#         })

#     df = pd.DataFrame(rows).set_index("Test Suite")

#     # ---------------------------
#     # Render bar chart (SECOND IMAGE)
#     # ---------------------------
#     st.markdown("### 📈 Test Results")
#     st.bar_chart(df, height=350)

#     st.markdown("### 📋 Test Results by Category")

#     for suite, stats in suite_stats.items():
#         passed = stats["passed"]
#         failed = stats["failed"]
#         total = passed + failed

#         label = (
#             suite.replace("tests/", "")
#                 .replace(".py", "")
#                 .replace("_", " ")
#                 .title()
#         )

#         if failed == 0:
#             st.success(f"✅ **{label}** — {passed}/{total} passed")
#         else:
#             st.warning(f"⚠️ **{label}** — {passed}/{total} passed")

#     # ---------------------------
#     # Enhanced UI Features
#     # ---------------------------
#     st.markdown("### ✨ Enhanced UI Features")

#     col1, col2, col3, col4 = st.columns(4)

#     col1.info("🔎 **Advanced Filters**\n\nFilter by status")
#     col2.info("🔍 **Search**\n\nFind functions")
#     col3.info("📤 **Export**\n\nJSON & CSV")
#     col4.info("ℹ️ **Help & Tips**\n\nQuick guide")

#     # ---------------------------
#     # Help & Usage Guide
#     # ---------------------------
#     with st.expander("📘 Advanced Usage Guide"):
#         st.markdown("""
#         ### 🚀 Getting Started
#         1. Scan your project using the sidebar  
#         2. Review coverage on Home  
#         3. Generate docstrings in Docstrings tab  
#         4. Validate against PEP 257  
#         5. Export reports  

#         ### 💡 Pro Tips
#         - Preview before applying docstrings  
#         - Fix validation issues iteratively  
#         - Track metrics regularly  

#         ### ⌨️ Keyboard Shortcuts
#         - **Ctrl + K**: Focus search  
#         - **Ctrl + Enter**: Apply docstring  
#         - **Esc**: Clear filters  
#         """)

#     st.markdown("---")
#     st.download_button(
#         "⬇️ Download Coverage Report JSON",
#         data=json.dumps(results, indent=2),
#         file_name="coverage_report.json",
#         mime="application/json"
#     )

