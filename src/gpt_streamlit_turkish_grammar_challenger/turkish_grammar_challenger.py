from .open_ai_api_client import OpenAiApiClient
from .turkish_grammar_task_creator import TurkishGrammarTaskCreator
from .turkish_grammar_feedback_provider import TurkishGrammarFeedbackProvider
from .types import TurkishGrammarTask


class TurkishGrammarChallenger:
    def __init__(self, openai_api_key: str, vocabulary_topic: str):
        self.api_client = OpenAiApiClient(openai_api_key)
        self.task_creator = TurkishGrammarTaskCreator(vocabulary_topic, self.api_client)
        self.feedback_provider = TurkishGrammarFeedbackProvider(self.api_client)

    def create_task(self) -> TurkishGrammarTask:
        return self.task_creator.create()

    def provide_feedback(self, task: TurkishGrammarTask, user_answer: str) -> str:
        return self.feedback_provider.provide(task, user_answer)
