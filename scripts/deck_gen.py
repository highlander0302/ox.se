import csv
import random
import uuid
from pathlib import Path

import genanki

INPUT_CSV = "../csv/academic650.csv"
FILE_NAME = "../decks/academic650.apkg"
DECK_NAME = "Academic650"


class AnkiDeckBuilder:
    """
    Builds an Anki deck (front = word, back = translation) from a CSV file.

    Expected CSV format:
    word,translation
    hello,hej
    """

    def __init__(self, input_csv: str | Path):
        self.input_csv = Path(input_csv)

        self.model_id = self._random_id()
        self.deck_id = self._random_id()

        self.model = self._build_model()
        self.deck = genanki.Deck(self.deck_id, DECK_NAME)

    def build_from_csv(self) -> int:
        pairs = self._load_pairs()
        if not pairs:
            raise ValueError("No valid (word, translation) pairs found in CSV")

        random.shuffle(pairs)

        for word, translation in pairs:
            self._add_note(word, translation)

        return len(pairs)

    def export(self) -> Path:
        output_path = Path(FILE_NAME)
        genanki.Package(self.deck).write_to_file(output_path)
        return output_path

    def _build_model(self) -> genanki.Model:
        return genanki.Model(
            self.model_id,
            "Word + Translation Model",
            fields=[
                {"name": "Word"},
                {"name": "Translation"},
            ],
            templates=[
                {
                    "name": "Card 1",
                    "qfmt": '<div class="word">{{Word}}</div>',
                    "afmt": """
                        <div class="word">{{Word}}</div>
                        <hr id="answer">
                        <div class="translation">{{Translation}}</div>
                    """,
                }
            ],
            css="""
            .card {
                font-family: Arial;
            }

            .word {
                text-align: center;
                font-size: 40px;
                font-weight: bold;
            }

            .translation {
                text-align: center;
                font-size: 28px;
            }
            """,
        )

    def _add_note(self, word: str, translation: str) -> None:
        note = genanki.Note(
            model=self.model,
            fields=[word, translation],
        )
        self.deck.add_note(note)

    def _load_pairs(self) -> list[tuple[str, str]]:
        pairs: list[tuple[str, str]] = []

        with self.input_csv.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise ValueError("CSV must contain a header row")

            headers = {h.lower().strip(): h for h in reader.fieldnames}
            word_key = headers.get("word")
            translation_key = headers.get("translation")

            if not word_key or not translation_key:
                raise ValueError(
                    f"CSV headers must include 'word' and 'translation'. "
                    f"Found: {reader.fieldnames}"
                )

            for row in reader:
                word = (row.get(word_key) or "").strip()
                translation = (row.get(translation_key) or "").strip()
                if word and translation:
                    pairs.append((word, translation))

        return pairs

    @staticmethod
    def _random_id() -> int:
        """
        genanki requires integer IDs.
        UUID4 gives randomness; trimmed to safe size.
        """
        return uuid.uuid4().int >> 96


def main() -> None:
    if not FILE_NAME or not DECK_NAME:
        raise ValueError("FILE_NAME and DECK_NAME must be set explicitly")

    builder = AnkiDeckBuilder(input_csv=INPUT_CSV)
    count = builder.build_from_csv()
    output_file = builder.export()

    print(f"Deck created: {output_file}")
    print(f"Deck name: {DECK_NAME}")
    print(f"Cards: {count}")


if __name__ == "__main__":
    main()
