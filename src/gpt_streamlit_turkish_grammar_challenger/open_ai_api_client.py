from openai import OpenAI
import json


class OpenAiApiClient:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def get_completion(self, prompt: str) -> str:
        messages = [{"role": "user", "content": prompt}]
        completion = self.client.chat.completions.create(
            model="gpt-4-1106-preview", messages=messages
        )
        return completion.choices[0].message.content

    def call_function(
        self,
        prompt,
        name: str,
        description: str,
        schema: dict,
    ) -> dict:
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
            model="gpt-4-1106-preview",
            messages=messages,
            tools=tools,
            tool_choice={"type": "function", "function": {"name": name}},
        )
        func_arguments = completion.choices[0].message.tool_calls[0].function.arguments

        return json.loads(func_arguments)
