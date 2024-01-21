from typing import TypedDict


class TurkishGrammarTask(TypedDict):
    grammar_rule: str
    vocabulary_topic: str
    turkish_phrase: str
    russian_translation: str
    first_challenging_turkish_phrase: str
    second_challenging_turkish_phrase: str
    turkish_options: list[str]
