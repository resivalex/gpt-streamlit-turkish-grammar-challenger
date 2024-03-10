from typing import List
import anthropic
from anthropic import Anthropic
import re

from .protocols import FunctionParameter


class AnthropicApiClient:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)

    def get_completion(self, prompt: str) -> str:
        completion = self.client.complete(
            prompt=prompt,
            stop_sequences=[anthropic.HUMAN_PROMPT],
            model="claude-v1",
            max_tokens_to_sample=1000,
        )
        return completion.completion

    def call_function(
        self,
        prompt: str,
        name: str,
        description: str,
        parameters: List[FunctionParameter],
    ) -> dict[str, str]:
        tool = self._construct_tool_description(name, description, parameters)
        system_prompt = self._construct_system_prompt([tool])
        function_calling_message = self.client.complete(
            prompt=prompt,
            stop_sequences=[
                anthropic.HUMAN_PROMPT,
                anthropic.AI_PROMPT,
                "</function_calls>",
            ],
            model="claude-v1",
            max_tokens_to_sample=1024,
            system_prompt=system_prompt,
        ).completion
        return {
            param["name"]: self._extract_parameter_value(
                param["name"], function_calling_message
            )
            for param in parameters
        }

    def _construct_tool_description(
        self, name: str, description: str, parameters: list[dict[str, str]]
    ) -> str:
        parameters_xml = "\n".join(
            f"<parameter>\n<name>{param['name']}</name>\n<description>{param['description']}</description>\n</parameter>"
            for param in parameters
        )
        return (
            "<tool_description>\n"
            f"<tool_name>{name}</tool_name>\n"
            "<description>\n"
            f"{description}\n"
            "</description>\n"
            "<parameters>\n"
            f"{parameters_xml}\n"
            "</parameters>\n"
            "</tool_description>"
        )

    def _construct_system_prompt(self, tools: list[str]) -> str:
        return (
            "In this environment you have access to a set of tools you can use to answer the user's question.\n"
            "\n"
            "You may call them like this:\n"
            "<function_calls>\n"
            "<invoke>\n"
            "<tool_name>$TOOL_NAME</tool_name>\n"
            "<parameters>\n"
            "<$PARAMETER_NAME>$PARAMETER_VALUE</$PARAMETER_NAME>\n"
            "...\n"
            "</parameters>\n"
            "</invoke>\n"
            "</function_calls>\n"
            "\n"
            "Here are the tools available:\n"
            "<tools>\n" + "\n".join(tools) + "\n</tools>"
        )

    def _extract_parameter_value(self, parameter_name: str, message: str) -> str:
        match = re.search(
            f"<{parameter_name}>(.+?)</{parameter_name}>", message, re.DOTALL
        )
        return match.group(1) if match else ""
