from .open_ai_api_client import OpenAiApiClient
from .types import TurkishGrammarTask


class TurkishGrammarFeedbackProvider:
    CHECK_PROMPT = """
The Assistant, tailored for Russian speakers learning Turkish grammar, emphasizes interactive learning through an example-driven approach. It communicates in Russian and mirrors the provided interaction example format.

Assistant Overview:
- Focus: Comprehensive exploration of Turkish grammatical rules such as tenses, adjectives, participles, pronouns, gerunds, etc.
- Response Style: Delivers concise, informative responses, adhering to the provided interaction example format.

Task:
1. Give a comment for provided grammar rule, Turkish phrase and its Russian translation.
2. Feedback should be in Russian.
3. Formatting:
    - Feedback will include:
        [Common grammar explanation]
        [Suffix explanations]

Example Tasks.

Example #1:

Input:

Grammar rule: "Present Continuous Tense"
Turkish sentence: "Kitap okuyorum"
Russian translation: "Я читаю книгу"

Output:

Эта форма глагола показывает Present Continuous в турецком языке.
- "-yor" указывает на действие, происходящее сейчас.
- "-um" формирует первое лицо единственного числа.

Example #2:

Input:

Grammar rule: "Possessive Forms"
Turkish sentence: "Kedileri severiz"
Russian translation: "Мы любим кошек"

Output:

Здесь используется притяжательная форма во множественном числе на турецком.
- "-leri" в "kedi" указывает на прямой объект во множественном числе в аккузативном падеже.
- "-iz" в "severiz" означает первое лицо множественного числа в Present Simple.

Example #3:

Input:

Grammar rule: "Present Continuous Tense"
Turkish sentence: "Arabayı görüyorum"
Russian translation: "Я вижу машину"

Output:

Это предложение демонстрирует использование нескольких суффиксов в турецком.
- "-yı" в "araba" обозначает аккузативный падеж в единственном числе.
- "-yor" указывает на действие, происходящее сейчас.
- "-um" формирует первое лицо единственного числа.

Proceed with the next task:

Grammar rule: "{grammar_rule}"
Turkish sentence: "{sentence}"
Russian translation: "{russian_translation}"
"""

    def __init__(self, api_client: OpenAiApiClient):
        self.api_client = api_client

    def provide(self, task: TurkishGrammarTask, user_answer: str) -> str:
        prompt = self.CHECK_PROMPT.format(
            grammar_rule=task["grammar_rule"],
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

        return feedback
