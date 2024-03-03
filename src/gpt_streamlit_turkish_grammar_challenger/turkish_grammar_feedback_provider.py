from .open_ai_api_client import OpenAiApiClient
from .types import TurkishGrammarTask


class TurkishGrammarFeedbackProvider:
    CHECK_PROMPT = """Task:
1. Comment on the provided grammar rules, Turkish phrase, and its Russian translation.
2. The feedback should be concise, focused on elucidating the principles of compound words in Turkish grammar, and provided in Russian. Explain word by word, see examples.

Objective:
- To deepen understanding of the construction of Turkish compound words for Russian speakers, using practical examples for illustrative purposes.

Input format:

Grammar rules: "[Grammar rules]"
Turkish sentence: "[Turkish sentence]"
Russian translation: "[Russian translation]"

Output format:

[Common grammar explanation]
[Suffix explanations]

Example Tasks:

Example #1:

Input:

Grammar rules: "Present Continuous Tense, Accusative Case"
Turkish sentence: "Kitabı okuyorum"
Russian translation: "Я читаю книгу"

Output:

**Present Continuous Tense** и **Accusative Case**.
- "Kitabı":
    - "kitap" - книга
    - "-ı" - аккузативный падеж, указывает на прямой объект
- "Okuyorum":
    - "oku" - читать
    - "-yor" - настоящее продолженное время
    - "-um" - первое лицо единственного числа

Example #2:

Input:

Grammar rules: "Possessive Forms, Plural Forms"
Turkish sentence: "Kedilerimi arıyorum"
Russian translation: "Я ищу своих кошек"

Output:

**Possessive Forms** и **Plural Forms**.
- "Kedilerimi":
    - "kedi" - кошка
    - "-ler" - множественное число
    - "-imi" - притяжательная форма в первом лице единственного числа, мои
- "Arıyorum":
    - "arı" - искать
    - "-yor" - настоящее продолженное время
    - "-um" - первое лицо единственного числа

Example #3:

Input:

Grammar rules: "Future Tense, Reflexive Pronouns"
Turkish sentence: "Kendimi tanıtacağım"
Russian translation: "Я представлюсь"

Output:

**Future Tense** и **Reflexive Pronouns**.
- "Kendimi":
    - "kendi" - сам
    - "-mi" - меня, демонстрирует использование рефлексивного местоимения в первом лице
- "Tanıtacağım":
    - "tanıt" - представлять
    - "-acağım" - будущее время в первом лице единственного числа


Proceed with the next task:

Grammar rules: "{grammar_rules}"
Turkish sentence: "{sentence}"
Russian translation: "{russian_translation}"
"""

    def __init__(self, api_client: OpenAiApiClient):
        self.api_client = api_client

    def provide(self, task: TurkishGrammarTask, user_answer: str) -> str:
        prompt = self.CHECK_PROMPT.format(
            grammar_rules=task["grammar_rules"],
            sentence=task["turkish_phrase"],
            russian_translation=task["russian_translation"],
        )
        grammar_explanation = self.api_client.get_completion(prompt)

        feedback = ""
        simple_feedback = (
            "Верно!" if task["turkish_phrase"] == user_answer else "Неверно."
        )
        feedback += "\n\n" + task["turkish_phrase"]
        feedback += "\n\n" + grammar_explanation

        feedback = f"""{simple_feedback}

{task["turkish_phrase"]}

{grammar_explanation}
"""
        print("Feedback:")
        print(feedback)

        return feedback
