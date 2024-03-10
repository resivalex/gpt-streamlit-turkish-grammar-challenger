from typing import Protocol, TypedDict, Dict


class FunctionParameter(TypedDict):
    name: str
    description: str


class GptApiClient(Protocol):
    def get_completion(self, prompt: str) -> str:
        ...

    def call_function(
        self,
        prompt: str,
        name: str,
        description: str,
        parameters: list[FunctionParameter],
    ) -> Dict[str, str]:
        ...
