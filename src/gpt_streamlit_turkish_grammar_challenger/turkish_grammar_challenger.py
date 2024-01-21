from .open_ai_api_client import OpenAiApiClient
from .turkish_grammar_task import TurkishGrammarTask
from .turkish_grammar_feedback import TurkishGrammarFeedback


class TurkishGrammarChallenger:
    def __init__(self, openai_api_key: str, vocabulary_topic: str):
        self.api_client = OpenAiApiClient(openai_api_key)
        self.task_creator = TurkishGrammarTask(vocabulary_topic, self.api_client)
        self.feedback_provider = TurkishGrammarFeedback(self.api_client)

    def create_task(self) -> str:
        return self.task_creator.create()

    def provide_feedback(self, task: str, user_answer: str) -> str:
        return self.feedback_provider.provide(task, user_answer)
