import nltk
import re
from typing import List

nltk.download('punkt_tab')


def count_sentences(text: str) -> int:
    """Zlicza liczbę zdań w tekście."""
    sentences = nltk.sent_tokenize(text, language='polish')
    return len(sentences)


def count_words(text: str) -> int:
    """Zlicza liczbę słów w tekście."""
    words = nltk.word_tokenize(text, language='polish')
    return len(words)


def count_syllables(word: str) -> int:
    """Zlicza sylaby w słowie."""
    word = re.sub(r'[^a-zA-ZąęóśłżźćńĄĘÓŚŁŻŹĆŃ]', '', word)
    syllables = re.findall(r'[aeiouyąęóśłżźćń]', word, re.IGNORECASE)
    return len(syllables)


def gunning_fog_index(text: str) -> float:
    """Oblicza współczynnik mglistości Gunninga."""
    sentences_count = count_sentences(text)
    words_count = count_words(text)
    complex_words_count = len(
        [word for word in nltk.word_tokenize(text, language='polish') if count_syllables(word) >= 3])

    if words_count == 0:
        return 0.0

    index = 0.4 * ((words_count / sentences_count) + (100 * complex_words_count / words_count))
    return index


def flesch_reading_ease(text: str) -> float:
    """Oblicza indeks czytelności Flescha."""
    sentences_count = count_sentences(text)
    words_count = count_words(text)
    syllables_count = sum(count_syllables(word) for word in nltk.word_tokenize(text, language='polish'))

    if words_count == 0:
        return 0.0

    score = 206.835 - (1.015 * (words_count / sentences_count)) - (84.6 * (syllables_count / words_count))
    return score


if __name__ == "__main__":
    # Przykładowe zdania do testowania
    sample_text = """
    W dzisiejszych czasach technologia rozwija się w szybkim tempie. 
    Coraz więcej osób korzysta z Internetu. To wpływa na nasze życie w wielu aspektach.
    """

    # Testowanie funkcji
    gfi = gunning_fog_index(sample_text)
    fre = flesch_reading_ease(sample_text)

    print(f"Gunning Fog Index: {gfi:.2f}")
    print(f"Flesch Reading Ease: {fre:.2f}")
