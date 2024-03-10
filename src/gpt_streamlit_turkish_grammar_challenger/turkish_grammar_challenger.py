from .open_ai_api_client import OpenAiApiClient
from .anthropic_api_client import AnthropicApiClient
from .turkish_grammar_task_creator import TurkishGrammarTaskCreator
from .turkish_grammar_feedback_provider import TurkishGrammarFeedbackProvider
from .types import TurkishGrammarTask


class TurkishGrammarChallenger:
    def __init__(
        self, openai_api_key: str, anthropic_api_key: str, vocabulary_topic: str
    ):
        api_client = None
        if openai_api_key != "":
            api_client = OpenAiApiClient(openai_api_key)
        if anthropic_api_key != "":
            api_client = AnthropicApiClient(anthropic_api_key)

        if api_client is None:
            raise ValueError("GPT client is not initialized")

        self.task_creator = TurkishGrammarTaskCreator(vocabulary_topic, api_client)
        self.feedback_provider = TurkishGrammarFeedbackProvider(api_client)

    def create_task(self) -> TurkishGrammarTask:
        return self.task_creator.create()

    def provide_feedback(self, task: TurkishGrammarTask, user_answer: str) -> str:
        return self.feedback_provider.provide(task, user_answer)
