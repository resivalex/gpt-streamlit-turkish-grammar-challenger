from openai import OpenAI


class OpenAiApiClient:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def get_completion(self, prompt: str) -> str:
        messages = [{"role": "user", "content": prompt}]
        completion = self.client.chat.completions.create(
            model="gpt-4-1106-preview", messages=messages
        )
        return completion.choices[0].message.content
