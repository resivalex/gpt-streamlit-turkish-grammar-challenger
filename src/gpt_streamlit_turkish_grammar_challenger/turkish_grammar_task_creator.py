import random
import json

from .open_ai_api_client import OpenAiApiClient
from .types import TurkishGrammarTask


class TurkishGrammarTaskCreator:
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
    PROMPT = """Task:
1. You are provided with a vocabulary topic and a grammar rule.
2. Present a Turkish phrase with its Russian translation and two additional Turkish phrases. These phrases are designed to help Russian speakers understand Turkish grammar by illustrating the correct use of the selected rule and challenging them with similar phrases.

Objective:
1. To facilitate the understanding of Turkish grammatical rules for Russian speakers through practical, interactive examples.
2. To emphasize learning through an example-driven approach, focusing on grammar nuances and vocabulary in context.
3. To aid in distinguishing correct grammatical forms from similar but incorrect ones, enhancing grammar learning.

Content Requirements:
1. Phrase Clarity: Use brief, clear phrases in Turkish to ensure understanding.
2. Grammar Emphasis: Highlight the specific Turkish grammar rule in each option, focusing on nuances like suffixes and word order.
3. Vocabulary: Utilize common, understandable vocabulary that is relevant to the selected topic.
4. Linguistic Accuracy: Ensure that Turkish and Russian phrases accurately represent the grammatical essence, considering the specificities of the Russian language.

Translation Options:
1. Translation Variation: Provide three Turkish translations, each reflecting the specified grammar rule but varying in grammatical forms rather than vocabulary.
2. Structure Consistency: Maintain similar phrase structures in all translations to challenge correct identification, using the same set of words.
3. Accuracy: Ensure grammatical correctness in the main Turkish option, with variations in the challenging phrases.

Input format:

Grammar rule: "[Grammar rule]"
Vocabulary topic: "[Vocabulary topic]"

Output format:

Grammar rule: "[Grammar rule]"
Vocabulary topic: "[Vocabulary topic]"
Correct Turkish phrase: "[Turkish phrase]"
Russian translation: "[Russian phrase]"
First challenging Turkish phrase: "[Similar Turkish phrase 1]"
Second challenging Turkish phrase: "[Similar Turkish phrase 2]"

Example Task:

Input:

Grammar rule: "Present Continuous Tense"
Vocabulary topic: "Досуг"

Output:

Grammar rule: "Present Continuous Tense"
Vocabulary topic: "Досуг"
Correct Turkish phrase: "Kitap okuyorum"
Russian translation: "Я читаю книгу"
First challenging Turkish phrase: "Kitabı okurum"
Second challenging Turkish phrase: "Kitap okur"

{pre_instruction}Proceed with the next task:

Grammar rule: "{rule}"
Vocabulary topic: "{topic}"
"""

    PREVIOUS_SENTENCES_PROMPT_TEMPLATE = """Previously used Turkish sentences:
{sentences}

Create a different Turkish phrase from listed above to maintain the diversity and quality of the tasks.

"""

    def __init__(self, vocabulary_topic: str, api_client: OpenAiApiClient):
        self.vocabulary_topic = vocabulary_topic
        self.api_client = api_client

        self.history = []

    def _get_rule(self) -> str:
        return random.choice(self.RULES)

    def _build_pre_instruction(self) -> str:
        if not self.history:
            return ""

        last_history_items = self.history[-10:]
        sentence_list = [f"- {sentence}" for sentence in last_history_items]
        sentences = "\n".join(sentence_list)

        return self.PREVIOUS_SENTENCES_PROMPT_TEMPLATE.format(sentences=sentences)

    def create(self) -> TurkishGrammarTask:
        rule = self._get_rule()

        prompt = self.PROMPT.format(
            rule=rule,
            topic=self.vocabulary_topic,
            pre_instruction=self._build_pre_instruction(),
        )
        task_data_text = self.api_client.get_completion(prompt)
        print("Task data:")
        print(task_data_text)
        arguments = self.api_client.call_function(
            prompt=task_data_text,
            name="create_task",
            description="A turkish grammar task",
            schema={
                "type": "object",
                "properties": {
                    "grammar_rule": {"type": "string"},
                    "vocabulary_topic": {"type": "string"},
                    "turkish_phrase": {"type": "string"},
                    "russian_translation": {"type": "string"},
                    "first_challenging_turkish_phrase": {"type": "string"},
                    "second_challenging_turkish_phrase": {"type": "string"},
                },
                "required": [
                    "grammar_rule",
                    "vocabulary_topic",
                    "turkish_phrase",
                    "russian_translation",
                    "first_challenging_turkish_phrase",
                    "second_challenging_turkish_phrase",
                ],
            },
        )
        arguments["turkish_options"] = [
            arguments["first_challenging_turkish_phrase"],
            arguments["second_challenging_turkish_phrase"],
            arguments["turkish_phrase"],
        ]
        random.shuffle(arguments["turkish_options"])
        print("Task arguments:")
        print(json.dumps(arguments, indent=2, ensure_ascii=False))
        print()
        self.history.append(arguments["turkish_phrase"])

        return arguments
