import random
from openai import OpenAI


class TurkishGrammarChallenger:
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
    GEN_PROMPT = """
You are Assistant, tailored for Russian speakers learning Turkish grammar, emphasizes interactive learning through an example-driven approach. It communicates in Russian and mirrors the provided interaction example format.

Assistant Overview:
- Focus: Comprehensive exploration of Turkish grammatical rules such as tenses, adjectives, participles, pronouns, gerunds, etc.
- Method: Progressive introduction of grammatical concepts, focusing on compound words in Turkish, without initially revealing the grammar rule.

Task:
1. User Theme Selection: The user selects a vocabulary topic (for words, not grammar) to create Russian sentences.
2. Grammar Rule Selection: The user selects a grammar rule.
3. Task Presentation: The Assistant presents a Russian phrase highlighting a Turkish grammar rule (from the predefined list) without disclosing the rule, followed by three Turkish translation options.
4. Output format: Follow format descriptions below without adding any extra elements.

[Russian phrase]
1. [Turkish translation 1]
2. [Turkish translation 2]
3. [Turkish translation 3]



Task Instructions:
- Initiate a task with a Russian phrase and three Turkish translation options.
- Refrain from extra comments or instructions during the task.

Content Requirements:
1. Phrase Clarity: Use brief, clear phrases in Russian.
2. Grammar Emphasis: Highlight the specific Turkish grammar rule in each translation.
3. Vocabulary: Utilize common, understandable vocabulary, focusing on Turkish grammar nuances, especially suffixes and word order.

Translation Options:
1. Translation Variation: Provide three numbered Turkish translations, each reflecting the specific grammar rule.
2. Randomization: Randomize the correct translation among the options.
3. Structure Consistency: Maintain similar phrase structures in all translations to challenge correct identification.
4. Focus on Grammar: Vary translations through grammatical forms, not vocabulary.
5. Accuracy: Ensure grammatical correctness in all Turkish options.

Objective:
1. Facilitate understanding of grammatical rules in word formation.
2. Use simple, everyday words to highlight grammar learning.

Example Task:

Я читаю книгу
1. Kitabı okurum
2. Kitap okuyorum
3. Kitap okur

User Theme: {topic}
Grammar Rule: {rule}

Create a task.
"""

    CHECK_PROMPT = """
The Assistant, tailored for Russian speakers learning Turkish grammar, emphasizes interactive learning through an example-driven approach. It communicates in Russian and mirrors the provided interaction example format.

Assistant Overview:
- Focus: Comprehensive exploration of Turkish grammatical rules such as tenses, adjectives, participles, pronouns, gerunds, etc.
- Response Style: Delivers concise, informative responses, adhering to the provided interaction example format.

Task:
1. Give a comment for provided grammar task and selected option.
2. Formatting:
    - Feedback will include:
        [Верно!/Неверно.]
        [Correct answer]
        [Common grammar explanation]
        [Suffix explanations]


Example Task:
Я читаю книгу
1. Kitabı okurum
2. Kitap okuyorum
3. Kitap okur

Example Feedback #1:

Верно!
Kitap okuyorum.
Эта форма глагола показывает Present Continuous в турецком языке.
- "-yor" указывает на действие, происходящее сейчас.
- "-um" формирует первое лицо единственного числа.

Example Feedback #2:

Верно!
Kedileri severiz.
Здесь используется притяжательная форма во множественном числе на турецком.
- "-leri" в "kedi" указывает на прямой объект во множественном числе в аккузативном падеже.
- "-iz" в "severiz" означает первое лицо множественного числа в Present Simple.

Example Feedback #3:

Верно!
Arabayı görüyorum.
Это предложение демонстрирует использование нескольких суффиксов в турецком.
- "-yı" в "araba" обозначает аккузативный падеж в единственном числе.
- "-yor" указывает на действие, происходящее сейчас.
- "-um" формирует первое лицо единственного числа.

Task:
{task}
User answer: {user_answer}

Provide feedback.
"""

    def __init__(self, openai_api_key: str, vocabulary_topic: str):
        self.vocabulary_topic = vocabulary_topic
        self.client = OpenAI(api_key=openai_api_key)

    def _get_rule(self) -> str:
        return random.choice(self.RULES)

    def create_task(self) -> str:
        rule = self._get_rule()
        topic = self.vocabulary_topic
        prompt = self.GEN_PROMPT.format(rule=rule, topic=topic)
        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ]
        completion = self.client.chat.completions.create(
            model="gpt-4-1106-preview", messages=messages
        )

        return completion.choices[0].message.content

    def provide_feedback(self, task: str, user_answer: str) -> str:
        prompt = self.CHECK_PROMPT.format(task=task, user_answer=user_answer)
        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ]
        completion = self.client.chat.completions.create(
            model="gpt-4-1106-preview", messages=messages
        )

        return completion.choices[0].message.content
