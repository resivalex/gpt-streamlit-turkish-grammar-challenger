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
1. You are provided with a vocabulary topic and grammar rules.
2. Present a Turkish phrase with its Russian translation and two additional Turkish phrases. These phrases are designed to help Russian speakers understand Turkish grammar by illustrating the correct use of the selected rules and challenging them with similar phrases.

Objective:
1. To facilitate the understanding of Turkish grammatical rules for Russian speakers through practical, interactive examples.
2. To emphasize learning through an example-driven approach, focusing on grammar nuances and vocabulary in context.
3. To aid in distinguishing correct grammatical forms from similar but incorrect ones, enhancing grammar learning.

Content Requirements:
1. Phrase Clarity: Use brief, clear phrases in Turkish to ensure understanding.
2. Grammar Emphasis: Highlight the specific Turkish grammar rules in each option, focusing on nuances like suffixes and word order.
3. Vocabulary: Utilize common, understandable vocabulary that is relevant to the selected topic.
4. Linguistic Accuracy: Ensure that Turkish and Russian phrases accurately represent the grammatical essence, considering the specificities of the Russian language.

Translation Options:
1. Translation Variation: Provide three Turkish translations, each reflecting the specified grammar rules but varying in grammatical forms rather than vocabulary.
2. Structure Consistency: Maintain similar phrase structures in all translations to challenge correct identification, using the same set of words.
3. Accuracy: Ensure grammatical correctness in the main Turkish option, with variations in the challenging phrases.

Input format:

Grammar rules: "[Specific grammar rules to apply]"
Vocabulary topic: "[Selected vocabulary topic to take words from]"

Output format:

Grammar rules: "[Applied grammar rules]"
Vocabulary topic: "[Chosen vocabulary topic]"
Correct Turkish phrase: "[Turkish phrase illustrating the rules]"
Russian translation: "[Accurate Russian translation of the Turkish phrase]"
First challenging Turkish phrase: "[First challenging Turkish phrase, closely resembling the correct phrase in structure and vocabulary, making it challenging to distinguish]"
Second challenging Turkish phrase: "[Second challenging Turkish phrase, closely resembling the correct phrase in structure and vocabulary, making it challenging to distinguish]"

Example Tasks:

Example #1:

Input:

Grammar rules: "Past Simple Tense, Possessive Forms"
Vocabulary topic: "Досуг"

Output:

Grammar rules: "Past Simple Tense, Possessive Forms"
Vocabulary topic: "Досуг"
Correct Turkish phrase: "Kitabımı okudum"
Russian translation: "Я прочитал свою книгу"
First challenging Turkish phrase: "Kitabımı okuyordum"
Second challenging Turkish phrase: "Kitabım okundu"

Example #2:

Input:

Grammar rules: "Future Tense, Comparative Adjectives"
Vocabulary topic: "Путешествия"

Output:

Grammar rules: "Future Tense, Comparative Adjectives"
Vocabulary topic: "Путешествия"
Correct Turkish phrase: "Yarın daha erken kalkacağım"
Russian translation: "Завтра я встану раньше"
First challenging Turkish phrase: "Yarın erken kalkmayı düşünüyorum"
Second challenging Turkish phrase: "Yarın erken kalkacak birini bekliyorum"

Example #3:

Input:

Grammar rules: "Plural Forms, Dative Case"
Vocabulary topic: "Семья"

Output:

Grammar rules: "Plural Forms, Dative Case"
Vocabulary topic: "Семья"
Correct Turkish phrase: "Aileme hediyeler aldım"
Russian translation: "Я купил подарки для своей семьи"
First challenging Turkish phrase: "Ailem için hediyeler düşünüyordum"
Second challenging Turkish phrase: "Aileme hediyeler alınacak"

{pre_instruction}Proceed with the next task:

Grammar rules: "{rules}"
Vocabulary topic: "{topic}"
"""

    PREVIOUS_SENTENCES_PROMPT_TEMPLATE = """Previously used Turkish sentences:
{sentences}

Create a Turkish phrase different from listed above to maintain the diversity and quality of the tasks.

"""

    def __init__(self, vocabulary_topic: str, api_client: OpenAiApiClient):
        self.vocabulary_topic = vocabulary_topic
        self.api_client = api_client

        self.history = []

    def _get_rules(self) -> list:
        return random.sample(self.RULES, 2)

    def _build_pre_instruction(self) -> str:
        if not self.history:
            return ""

        last_history_items = self.history[-10:]
        sentence_list = [f"- {sentence}" for sentence in last_history_items]
        sentences = "\n".join(sentence_list)

        return self.PREVIOUS_SENTENCES_PROMPT_TEMPLATE.format(sentences=sentences)

    def create(self) -> TurkishGrammarTask:
        rules = self._get_rules()
        rules_text = ", ".join(rules)

        prompt = self.PROMPT.format(
            rules=rules_text,
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
                    "grammar_rules": {"type": "string"},
                    "vocabulary_topic": {"type": "string"},
                    "turkish_phrase": {"type": "string"},
                    "russian_translation": {"type": "string"},
                    "first_challenging_turkish_phrase": {"type": "string"},
                    "second_challenging_turkish_phrase": {"type": "string"},
                },
                "required": [
                    "grammar_rules",
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
