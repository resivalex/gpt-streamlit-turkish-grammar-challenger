import random

from .open_ai_api_client import OpenAiApiClient


class TurkishGrammarTask:
    RULES = [
        "Present Continuous Tense",
        "Possessive Forms",
        "Accusative Case",
        "Plural Forms",
        "Past Simple Tense",
        "Future Tense",
        "Reflexive Pronouns",
        "Comparative Adjectives",
        "Conditional Mood",
        "Passive Voice",
        "Imperative Mood",
        "Dative Case",
        "Aorist Tense",
        "Causative Form",
        "Negative Form",
    ]
    PROMPT = """
You are Assistant, tailored for Russian speakers learning Turkish grammar, emphasizes interactive learning through an example-driven approach. It communicates in Russian and mirrors the provided interaction example format.

Assistant Overview:
- Focus: Comprehensive exploration of Turkish grammatical rules such as tenses, adjectives, participles, pronouns, gerunds, etc.
- Method: Progressive introduction of grammatical concepts, focusing on compound words in Turkish, without initially revealing the grammar rule.

Task:
1. User Theme Selection: The user selects a vocabulary topic (for words, not grammar) to create Russian sentences.
2. Grammar Rule Selection: The user selects a grammar rule.
3. Task Presentation: The Assistant presents a Turkish phrase highlighting a provided Turkish grammar rule without disclosing the rule, followed by Russian phrase and two Turkish phrase options.
4. Output format: Follow format descriptions below without adding any extra elements.

Turkish phrase: "[Turkish phrase]"
Russian translation: "[Russian phrase]"
First challenging Turkish phrase: "[Similar Turkish phrase 1]"
Second challenging Turkish phrase: "[Similar Turkish phrase 2]"


Task Instructions:
- Initiate a task with a Turkish phrase, Russian translation and two Turkish translation options.
- Refrain from extra comments or instructions during the task.

Content Requirements:
1. Phrase Clarity: Use brief, clear phrases in Turkish.
2. Grammar Emphasis: Highlight the specific Turkish grammar rule in each option.
3. Vocabulary: Utilize common, understandable vocabulary, focusing on Turkish grammar nuances, especially suffixes and word order.

Translation Options:
1. Translation Variation: Provide three numbered Turkish translations, each reflecting the specified grammar rule.
2. Structure Consistency: Maintain similar phrase structures in all translations to challenge correct identification.
3. Focus on Grammar: Vary translations through grammatical forms, not vocabulary.
4. Accuracy: Ensure grammatical correctness in all Turkish options.

Objective:
1. Facilitate understanding of grammatical rules in word formation.
2. Use simple, everyday words to highlight grammar learning.

Example Task:

Turkish phrase: "Kitap okuyorum"
Russian translation: "Я читаю книгу"
First challenging Turkish phrase: "Kitabı okurum"
Second challenging Turkish phrase: "Kitap okur"


User Theme: "{topic}"
Grammar Rule: "{rule}"

Create a task.
"""

    def __init__(self, vocabulary_topic: str, api_client: OpenAiApiClient):
        self.vocabulary_topic = vocabulary_topic
        self.api_client = api_client

    def _get_rule(self) -> str:
        return random.choice(self.RULES)

    def create(self) -> str:
        rule = self._get_rule()
        prompt = self.PROMPT.format(rule=rule, topic=self.vocabulary_topic)
        task_data_text = self.api_client.get_completion(prompt)
        print(task_data_text)
        agruments = self.api_client.call_function(
            prompt=task_data_text,
            name="create_task",
            description="A turkish grammar task",
            schema={
                "type": "object",
                "properties": {
                    "turkish_phrase": {"type": "string"},
                    "russian_translation": {"type": "string"},
                    "first_challenging_turkish_phrase": {"type": "string"},
                    "second_challenging_turkish_phrase": {"type": "string"},
                },
                "required": [
                    "turkish_phrase",
                    "russian_translation",
                    "first_challenging_turkish_phrase",
                    "second_challenging_turkish_phrase",
                ],
            },
        )
        print(agruments)
        print()

        task = f"""{agruments['russian_translation']}
        
1. {agruments['turkish_phrase']}
2. {agruments['first_challenging_turkish_phrase']}
3. {agruments['second_challenging_turkish_phrase']}
"""
        return task
