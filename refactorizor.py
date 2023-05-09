import os
import re
import sys
import git
from abc import ABC, abstractmethod

class Refactorizor(ABC):
    def __init__(self, changes):
        self.changes = changes

    @abstractmethod
    def apply_changes(self, change):
        pass

    @abstractmethod
    def update_codebase_md(self):
        pass

    @abstractmethod
    def commit_changes(self):
        pass

    def execute(self):
        for change in self.changes:
            self.apply_changes(change)

        self.update_codebase_md()
        self.commit_changes()

class PythonJavaScriptRefactorizor(Refactorizor):
    def apply_changes(self, change):
        change_type = change["change_type"]
        target_file = change["target_file"]

        if not os.path.exists(target_file):
            raise ValueError(f"File {target_file} not found")

        if change_type == "append":
            with open(target_file, "a") as f:
                f.write(change["content"])
        elif change_type == "replace":
            with open(target_file, "r") as f:
                content = f.read()

            updated_content = re.sub(change["search_pattern"], change["replacement"], content)

            if updated_content == content:
                raise ValueError(f"Search pattern '{change['search_pattern']}' not found in {target_file}")

            with open(target_file, "w") as f:
                f.write(updated_content)
        else:
            raise ValueError(f"Unknown change_type: {change_type}")

    def update_codebase_md(self):
        codebase_md_path = "CODEBASE.md"

        with open(codebase_md_path, "a") as f:
            f.write("\n\n## Recent Changes\n\n")

            for change in self.changes:
                f.write(f"- {change['description']}\n")

    def commit_changes(self):
        repo = git.Repo(os.getcwd())
        repo.index.add(["CODEBASE.md"] + [change["target_file"] for change in self.changes])

        commit_message = "Refactorizor script applied with the following changes:\n" + "\n".join([change["description"] for change in self.changes])
        repo.index.commit(commit_message)

if __name__ == "__main__":
    changes = [
        {
            "description": "Add error handling in chat_routes.py",
            "target_file": "backend/app/api/chat_routes.py",
            "search_pattern": r"input_data = request\.json\['message'\]",
            "replacement": (
                "input_data = request.json.get('message')\n"
                "if not input_data or not isinstance(input_data, str):\n"
                "    return jsonify({'error': 'Invalid input data'}), 400\n"
            ),
            "change_type": "replace"
        },
        {
            "description": "Add sanitize_input function to utils.js",
            "target_file": "frontend/src/utils.js",
            "content": (
                "\nexport function sanitize_input(input) {\n"
                "  const sanitized_input = input.replace(/</g, '&lt;').replace(/>/g, '&gt;');\n"
                "  return sanitized_input;\n"
                "}\n"
            ),
            "change_type": "append"
        },
        {
            "description": "Refactor Chat.js to use useReducer",
            "target_file": "frontend/src/components/Chat.js",
            "search_pattern": (
                r"import React, { useState } from 'react';\n"
                r"const \[messages, setMessages\] = useState\(\[\]\);"
            ),
            "replacement": (
                "import React, { useReducer } from 'react';\n"
                "const initialState = { messages: [] };\n"
                "const reducer = (state, action) => {\n"
                "  switch (action.type) {\n"
                "    case 'addMessage':\n"
                "      return { messages: [...state.messages, action.message] };\n"
                "    default:\n"
                "      return state;\n"
                "  }\n"
                "};\n"
                "const [state, dispatch] = useReducer(reducer, initialState);\n"
                "const { messages } = state;"
            ),
            "change_type": "replace"
        }
    ]

    refactorizor = PythonJavaScriptRefactorizor(changes)
    refactorizor.execute()