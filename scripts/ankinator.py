t import csv
import requests
import genanki
import time


def load_words(filename):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row['word'] for row in reader]


def translate_word(word, source='en', target='sv'):
    try:
        response = requests.post("https://libretranslate.com/translate", data={
            'q': word,
            'source': source,
            'target': target,
            'format': 'text'
        })

        print(f"Response for '{word}': {response.json()}")

        result = response.json()
        translation = result['translatedText'].strip()

        one_word_translation = translation.split()[0]
        return one_word_translation
    except Exception as e:
        print(f"Error translating '{word}': {e}")
        return ""


my_model = genanki.Model(
    1607392319,
    'Word + Translation Model',
    fields=[
        {'name': 'Word'},
        {'name': 'Translation'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Word}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Translation}}',
        },
    ])

my_deck = genanki.Deck(
    2059400110,
    'Oxford 3000 English-Swedish')

words = load_words('oxford500.csv')

for word in words:
    translation = translate_word(word)
    print(f"{word} -> {translation}")

    note = genanki.Note(
        model=my_model,
        fields=[word, translation])
    my_deck.add_note(note)

    time.sleep(1.5)

genanki.Package(my_deck).write_to_file('oxford3000_sv.apkg')
print("Anki deck created: oxford3000_sv.apkg")
