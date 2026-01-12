from annotated_types import doc
from ai_powered.core.docstring_engine.llm_integration import (
    generate_docstring_content
)

class DocstringGenerator:
    def __init__(self, style="numpy", use_llm=True):
        self.style = style.lower()
        self.use_llm = use_llm

    def generate_docstring(self, func_obj):
        content = generate_docstring_content(func_obj) if self.use_llm else {}

        summary = content.get("summary", "")
        args = content.get("args", {})
        returns = content.get("returns", "")
        raises = content.get("raises", {})

        if self.style == "numpy":
            return self._numpy(summary, args, returns, func_obj)

        if self.style == "google":
            return self._google(summary, args, returns, func_obj)

        if self.style == "rest":
            return self._rest(summary, args, returns, raises, func_obj)

        return f'"""{summary}"""'

    def _numpy(self, summary, args, returns, func_obj):
        doc = f'"""\n{summary}\n\n'

        # Parameters
        if func_obj["args"]:
            doc += "Parameters:\n"
            for arg in func_obj["args"]:
                name = arg["name"]
                arg_type = arg.get("type") or "TYPE"
                description = args.get(name, "DESCRIPTION")
                doc += f"{name} : {arg_type}\n    {description}\n"
            doc += "\n"
        # Returns
        doc += "Returns:\n"
        if func_obj.get("returns"):
            doc += f"{func_obj['returns']}:  {returns}\n"
        else:
            doc += f"TYPE:  {returns}\n"
        doc += '"""'
        return doc

  #  def _google(self, summary, args, returns):
        '''doc = f'"""\n{summary}\n\n'
        if args:
            doc += "Args:\n"
            for k, v in args.items():
                doc += f"    {k} (TYPE): {v}\n"
            doc += "\n"
        doc += f"Returns:\n    TYPE: {returns}\n"
        doc += '"""'
        return doc'''
    # def _google(self, summary, args, returns, func_obj):
    #     doc = f'"""\n{summary}\n\n'

    #     if args:
    #         doc += "Args:\n"
    #         for arg in func_obj["args"]:
    #             name = arg["name"]
    #             arg_type = arg.get("type") or "TYPE"
    #             description = args.get(name, "DESCRIPTION")
    #             doc += f"    {name} ({arg_type}): {description}\n"
    #         doc += "\n"
    #     doc += f"Returns:\n"
    #     if func_obj.get("returns"):
    #         doc += f"    {func_obj['returns']}: {returns}\n"
    #     else:
    #         doc += f"    TYPE: {returns}\n"
    #     doc += '"""'
    #     return doc
    def _google(self, summary, args, returns, func_obj):
        doc = f'"""\n{summary}\n\n'

        # ALWAYS render Args if function has parameters
        if func_obj["args"]:
            doc += "Args:\n"
            for arg in func_obj["args"]:
                name = arg["name"]
                arg_type = arg.get("type") or "TYPE"
                description = args.get(name, "DESCRIPTION")
                doc += f"    {name} ({arg_type}): {description}\n"
            doc += "\n"
        doc += "Returns:\n"
        if func_obj.get("returns"):
            doc += f"    {func_obj['returns']}: {returns or 'DESCRIPTION'}\n"
        else:
            doc += f"    TYPE: {returns or 'DESCRIPTION'}\n"

        doc += '"""'
        return doc



    def _rest(self, summary, args, returns, raises, func_obj):
        doc = f'"""\n{summary}\n\n'

        # Parameters
        for arg in func_obj["args"]:
            name = arg["name"]
            arg_type = arg.get("type") or "TYPE"
            description = args.get(name, "DESCRIPTION")
            doc += f":param {arg_type} {name}: {description}\n"

        # Returns
        doc += f":returns: {returns}\n"
        if func_obj.get("returns"):
            doc += f":rtype: {func_obj['returns']}\n"

        # Raises
        for exc, reason in raises.items():
            doc += f":raises {exc}: {reason}\n"

        doc += '"""'
        return doc

