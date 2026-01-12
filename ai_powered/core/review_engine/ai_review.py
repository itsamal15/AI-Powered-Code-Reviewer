class AIReviewEngine:
    def review(self, function_data):
        improvements = []

        if not function_data.get("docstring"):
            improvements.append("Add a docstring")

        if len(function_data["args"]) == 0:
            improvements.append("Consider using meaningful parameters if function is generic")

        return improvements
