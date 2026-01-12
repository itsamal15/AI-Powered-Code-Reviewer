'''
class CoverageReporter:
    def __init__(self, functions):
        self.functions = functions

    def get_metrics(self):
        total = len(self.functions)
        documented = sum(1 for f in self.functions.values() if f["docstring"])
        coverage = round((documented / total) * 100, 2) if total else 0

        return {
            "total_functions": total,
            "documented": documented,
            "coverage": coverage
        }
'''
class CoverageReporter:
    def __init__(self, functions):
        self.functions = functions

    def get_metrics(self):
        total = len(self.functions)
        documented = sum(
            1 for f in self.functions.values() if f.get("docstring")
        )
        coverage = round((documented / total) * 100, 2) if total else 0

        return {
            "total_functions": total,
            "documented": documented,
            "coverage_percent": coverage
        }


def compute_coverage(functions, threshold=None):
    """
    Compute coverage report in structured format for UI + tests.
    """
    if not functions:
        aggregate = {
            "total_functions": 0,
            "documented": 0,
            "coverage_percent": 0
        }
    else:
        reporter = CoverageReporter(functions)
        aggregate = reporter.get_metrics()

    # Threshold check (optional)
    if threshold is not None:
        aggregate["meets_threshold"] = (
            aggregate["coverage_percent"] >= threshold
        )

    return {
        "aggregate": aggregate
    }
