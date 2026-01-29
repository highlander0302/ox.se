# ox.se 🇬🇧➡️🇸🇪 (Work in Progress)

**⚠️ Note:** This script is currently under development and **not fully functional**. The main blocker is finding a reliable and free API for accurate English-to-Swedish translations. Once that’s in place, the rest of the flow will be polished and finalized.

---

## What is ox.se?

**ox.se** is a Python script designed to help you build your own Swedish vocabulary deck for Anki — automatically.  
You provide a `.csv` file with a list of English words, and the script will:

1. Translate each word to Swedish  
2. Format the data correctly  
3. Generate an Anki-compatible file (`.apkg`) that you can import into the Anki app

Perfect for learners who want to boost their Swedish with a custom flashcard deck!

---

## Features (Planned / In Progress)

- [x] Read `.csv` file of English words
- [ ] Translate to Swedish using an API (not yet finalized)
- [x] Generate `.apkg` Anki deck using `genanki`
- [x] Option to customize deck name, tags, or notes
- [x] Handle API errors and retry logic

---

## Usage (Coming Soon)

When it's complete, usage will look something like:

```bash
python oxse.py input.csv --deck-name "My Swedish Deck"
