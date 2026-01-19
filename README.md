# AI-Powered Code Reviewer

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![AI & NLP](https://img.shields.io/badge/AI%20%26%20NLP-Enabled-green.svg)](https://github.com)
[![LLM Integration](https://img.shields.io/badge/LLM-Groq-orange.svg)](https://console.groq.com/)
[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)](https://github.com)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Overview

**AI-Powered Code Reviewer** is an intelligent Python code analysis and documentation platform that leverages Large Language Models (LLMs) and Natural Language Processing (NLP) to automatically review, analyze, and generate comprehensive documentation for Python code. Built with Streamlit for an intuitive web-based interface, this tool helps developers maintain code quality, generate professional docstrings, and ensure compliance with coding standards.

The platform uses state-of-the-art transformer-based LLMs (specifically Groq-powered models) to provide intelligent code insights, automated documentation generation, and comprehensive code quality metrics—making it ideal for both individual developers and enterprise teams.

## Key Features

- **Intelligent Code Analysis**: Uses LLM-based analysis to review Python code and identify improvements
- **Automated Docstring Generation**: Generates comprehensive docstrings in multiple formats (Google, NumPy, reStructuredText)
- **Code Quality Metrics**: Calculates complexity scores, maintainability index, and code coverage
- **Python Code Parsing**: Extracts function signatures, arguments, and code structure using AST parsing
- **Code Validation**: Validates Python code syntax and structure before analysis
- **Coverage Reporting**: Generates detailed coverage reports in JSON format
- **Interactive Dashboard**: Beautiful Streamlit-based dashboard for visual code analysis and reviews
- **LLM-Configurable**: Flexible LLM configuration supporting multiple AI providers (currently Groq)
- **Prompt Engineering**: Advanced prompt templates for precise code analysis and documentation
- **Batch Processing**: Analyze multiple Python files simultaneously
- **Professional Reports**: Generate professional review reports and export logs

## Techniques Used

### Natural Language Processing (NLP)
- **Text Analysis**: Analyzes code comments, docstrings, and function names using NLP techniques
- **Code-to-Text Generation**: Converts code structure into human-readable summaries
- **Semantic Understanding**: Understands code purpose and generates contextually appropriate documentation

### Prompt Engineering
- **Optimized Prompts**: Carefully engineered prompts for docstring generation and code analysis
- **Role-Based Prompting**: Uses specialized prompts for different code elements (functions, classes, modules)
- **Context-Aware Generation**: Includes code context in prompts for accurate analysis
- **Few-Shot Learning**: Leverages examples to guide LLM output formatting

### LLM-Based Text Generation
- **Transformer Models**: Utilizes state-of-the-art transformer-based LLMs from Groq
- **Temperature Control**: Configurable temperature for balancing creativity and determinism
- **Token Optimization**: Manages context window efficiently for cost and performance
- **Structured Output**: Generates JSON-structured responses for reliable parsing

## Technology Stack

### Programming Language
- **Python 3.9+**: Core programming language

### Libraries & Frameworks
- **Streamlit**: Interactive web-based user interface and dashboard
- **LangChain**: LLM orchestration and integration framework
- **Groq API (LangChain-Groq)**: High-performance LLM inference
- **Python AST Module**: Abstract Syntax Tree parsing for code analysis
- **Radon**: Code complexity and maintainability metrics
- **Pydocstyle**: Docstring convention checker
- **Pytest**: Testing framework with JSON report generation
- **Pandas**: Data manipulation and analysis

### AI/ML Technologies
- **Large Language Models (LLMs)**: Groq-powered transformer models for code understanding and generation
- **Natural Language Processing**: Text generation and analysis
- **Vector Embeddings**: Semantic understanding of code context (via LangChain)

### LLM Details
- **Model Type**: Transformer-based Large Language Models
- **Provider**: Groq (Ultra-fast LLM inference)
- **Supported Models**: Configurable LLM models (currently optimized for Groq's model family)
- **Configuration**: LLM provider, model name, API key, temperature, and token limits are fully configurable
- **Integration**: Seamlessly integrated via LangChain for flexible provider switching
- **Performance**: Optimized for low-latency responses suitable for real-time code review

## Project Structure

```
AI-Powered-Code-Reviewer/
│
├── ai_powered/                          # Core application package
│   ├── core/                            # Core functionality modules
│   │   ├── parser/                      # Code parsing module
│   │   │   └── python_parser.py        # Python AST parser
│   │   ├── docstring_engine/            # Docstring generation module
│   │   │   ├── generator.py            # Docstring format generator
│   │   │   ├── llm_integration.py      # LLM API integration
│   │   │   └── docstring_writer.py     # Applies docstrings to code
│   │   ├── review_engine/               # Code review module
│   │   │   └── ai_review.py            # AI-based review logic
│   │   ├── reporter/                    # Report generation
│   │   │   └── coverage_reporter.py    # Coverage report generator
│   │   └── validator/                   # Code validation
│   │       └── validator.py            # Syntax and structure validator
│   └── cli/                             # Command-line interface
│       └── commands.py                  # CLI command definitions
│
├── dashboard_ui/                        # Web dashboard
│   └── dashboard.py                     # Streamlit dashboard application
│
├── tests/                               # Test suite
│   ├── test_parser.py                  # Parser tests
│   ├── test_generator.py                # Generator tests
│   ├── test_llm_integration.py          # LLM integration tests
│   ├── test_validator.py                # Validator tests
│   ├── test_coverage_reporter.py        # Reporter tests
│   └── test_dashboard.py                # Dashboard tests
│
├── examples/                            # Example Python files
│   ├── sample_a.py                      # Sample code for testing
│   └── sample_b.py                      # Sample code for testing
│
├── storage/                             # Data storage directory
│   ├── review_logs.json                # Stored code review logs
│   └── reports/                         # Generated reports
│
├── main_app.py                          # Main Streamlit application entry point
├── groq_test.py                         # Groq API testing script
├── requirements.txt                     # Project dependencies
├── pytest.ini                           # Pytest configuration
└── README.md                            # Project documentation
```

## Installation Steps

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Groq API key (obtain from [https://console.groq.com/](https://console.groq.com/))

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/AI-Powered-Code-Reviewer.git
cd AI-Powered-Code-Reviewer
```

### Step 2: Create a Virtual Environment (Recommended)
```bash
# On Windows
python -m venv project101
project101\Scripts\activate

# On macOS/Linux
python3 -m venv project101
source project101/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_groq_api_key_here
LLM_MODEL=mixtral-8x7b-32768
TEMPERATURE=0.7
MAX_TOKENS=2000
```

Replace `your_groq_api_key_here` with your actual Groq API key.

### Step 5: Verify Installation
```bash
pytest -v
```

All tests should pass successfully.

## How to Run the Project Locally

### Option 1: Run the Web Dashboard (Recommended)
```bash
streamlit run main_app.py
```

This will:
- Start a local Streamlit web server (default: http://localhost:8501)
- Open the interactive dashboard in your default browser
- Allow you to upload Python files for analysis, generate docstrings, and view reports

### Option 2: Run Tests
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_parser.py -v

# Generate JSON report
pytest --json-report --json-report-file=storage/reports/pytest_results.json
```

### Option 3: Test LLM Integration
```bash
python groq_test.py
```

This script verifies that your Groq API key is configured correctly and the LLM is accessible.

### Option 4: Analyze a Python File
```python
from ai_powered.core.parser.python_parser import PythonParser
from ai_powered.core.docstring_engine.generator import DocstringGenerator

# Parse a Python file
parser = PythonParser()
functions = parser.parse_file("path/to/your/file.py")

# Generate docstrings
generator = DocstringGenerator(style="google", use_llm=True)
for func in functions:
    docstring = generator.generate_docstring(func)
    print(docstring)
```

## Certification Use Case

### For Infosys Certification Programs

**AI-Powered Code Reviewer** demonstrates proficiency in:

1. **AI & Machine Learning**
   - Integration of Large Language Models (LLMs) in production applications
   - Prompt engineering for specialized tasks
   - NLP pipeline implementation

2. **Python Development**
   - Object-oriented programming with modular architecture
   - Advanced Python features (AST, decorators, context managers)
   - Testing and quality assurance practices

3. **Full-Stack Application Development**
   - Backend: Python-based core modules and APIs
   - Frontend: Interactive Streamlit web application
   - Data persistence: JSON-based storage and reporting

4. **Cloud & API Integration**
   - REST API integration with Groq LLM services
   - Environment variable management for secure API key handling
   - Error handling and graceful API failure management

5. **DevOps & Deployment Readiness**
   - Modular, production-ready code structure
   - Comprehensive testing with pytest
   - Requirements management and dependency tracking
   - Scalable architecture for enterprise use

### Business Value
- **Automated Code Quality Assurance**: Reduces manual code review time
- **Consistent Documentation**: Ensures uniform docstring formatting
- **Developer Productivity**: Frees developers from routine documentation tasks
- **Compliance**: Helps maintain coding standards and best practices
- **Knowledge Transfer**: Auto-generated documentation aids onboarding

## Usage Examples

### Example 1: Generate Docstrings from Dashboard
1. Open http://localhost:8501 in your browser
2. Navigate to "Docstring Generator" section
3. Upload a Python file or paste code
4. Select docstring style (Google, NumPy, or reStructuredText)
5. Click "Generate Docstrings"
6. Review and download the documented code

### Example 2: Analyze Code Quality
1. Upload Python files through the dashboard
2. View code complexity metrics (Cyclomatic Complexity, Maintainability Index)
3. Get AI-powered recommendations for improvements
4. Export detailed reports

### Example 3: Batch Process Multiple Files
1. Place Python files in a directory
2. Use the batch processing feature
3. Generate comprehensive analysis reports
4. Export results in JSON format for integration with CI/CD pipelines

## Testing

The project includes comprehensive unit tests:

```bash
# Run all tests with coverage
pytest --cov=ai_powered tests/

# Run specific test class
pytest tests/test_generator.py::TestDocstringGenerator -v

# Run with specific Python version
python -m pytest tests/
```

## Configuration

### LLM Configuration (Fully Customizable)
Edit the LLM parameters in your `.env` file or through the dashboard:
- `LLM_MODEL`: Change to any Groq-supported model (mixtral-8x7b-32768, llama-2, etc.)
- `TEMPERATURE`: Adjust creativity (0.0-2.0, default: 0.7)
- `MAX_TOKENS`: Control response length
- `GROQ_API_KEY`: Your API key for authentication

### Code Analysis Configuration
- Modify complexity thresholds in `ai_powered/core/reporter/coverage_reporter.py`
- Customize docstring styles in `ai_powered/core/docstring_engine/generator.py`
- Adjust validation rules in `ai_powered/core/validator/validator.py`

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Performance Considerations

- **LLM Inference**: Groq provides ultra-fast inference (<1s per request)
- **Batch Processing**: Optimized for analyzing multiple files efficiently
- **Caching**: Results are cached to minimize redundant API calls
- **Memory Usage**: Suitable for both local and cloud deployments

## Troubleshooting

### Issue: "GROQ_API_KEY not found"
**Solution**: Ensure your `.env` file is in the root directory and contains the correct API key.

### Issue: "ModuleNotFoundError"
**Solution**: Run `pip install -r requirements.txt` and verify the virtual environment is activated.

### Issue: Streamlit app not loading
**Solution**: Ensure port 8501 is available. If not, run:
```bash
streamlit run main_app.py --server.port 8502
```

### Issue: LLM requests timing out
**Solution**: Check your internet connection and Groq API status. Increase timeout in configuration if needed.


## Acknowledgments

- **Groq**: For providing ultra-fast LLM inference
- **LangChain**: For simplifying LLM integration
- **Streamlit**: For the interactive dashboard framework
- **Python Community**: For excellent code analysis tools (Radon, Pydocstyle)

---

**Last Updated**: January 2026  
**Version**: 1.0.0  
**Status**: Completed
