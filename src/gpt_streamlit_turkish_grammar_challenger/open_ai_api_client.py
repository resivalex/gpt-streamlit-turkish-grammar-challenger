from typing import List
from openai import OpenAI
import json

from .protocols import FunctionParameter


GPT_CHEAP_MODEL = "gpt-3.5-turbo"
GPT_SMART_MODEL = "gpt-4-turbo-preview"

COMPLETION_MODEL = GPT_CHEAP_MODEL
FUNCTION_MODEL = GPT_CHEAP_MODEL


class OpenAiApiClient:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def get_completion(self, prompt: str) -> str:
        messages = [{"role": "user", "content": prompt}]
        completion = self.client.chat.completions.create(
            model=COMPLETION_MODEL, messages=messages
        )
        return completion.choices[0].message.content

    def _fix_encoded_symbols(self, text: str) -> str:
        if "\\u" in text:
            return text.encode("utf-8").decode("unicode-escape")

        return text

    def call_function(
        self,
        prompt: str,
        name: str,
        description: str,
        parameters: List[FunctionParameter],
    ) -> dict[str, str]:
        schema = {
            "type": "object",
            "properties": {param["name"]: {"type": "string"} for param in parameters},
            "required": [param["name"] for param in parameters],
        }
        messages = [{"role": "user", "content": prompt}]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": description,
                    "parameters": schema,
                },
            }
        ]
        completion = self.client.chat.completions.create(
            model=FUNCTION_MODEL,
            messages=messages,
            tools=tools,
            tool_choice={"type": "function", "function": {"name": name}},
        )
        func_arguments = completion.choices[0].message.tool_calls[0].function.arguments

        result = json.loads(func_arguments)

        for key, value in result.items():
            if isinstance(value, str):
                result[key] = self._fix_encoded_symbols(value)

        return result
