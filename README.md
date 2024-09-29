# Go [BreakWordTraps] FinTax
# HackYeah 2024

## Opis projektu

Projekt przetwarza dane wideo, analizując zarówno komponenty wizualne, jak i dźwiękowe, aby generować różne metryki, takie jak analiza sentymentu, transkrypcje i wskaźniki czytelności. W projekcie wykorzystywane są modele uczenia maszynowego, takie jak OpenAI GPT-4 do podsumowywania i analizy sentymentu, Whisper do transkrypcji oraz VAD (Voice Activity Detection) do wykrywania pauz w mowie.

Celem projektu jest dostarczenie szczegółowych metryk dotyczących nagrań wideo, takich jak analiza sentymentu mówcy, struktura mowy, zmiany tematów oraz trudność czytania za pomocą wskaźników takich jak Gunning Fog i Flesch Reading Ease. Wszystkie wygenerowane metryki są przesyłane do frontend'u w celu wizualizacji.

## Funkcje

- **Przetwarzanie wideo**: Ekstrakcja klatek i dźwięku z wideo do dalszej analizy.
- **Transkrypcja**: Użycie Whisper (model OpenAI) do transkrypcji dźwięku na tekst.
- **Analiza sentymentu**: Analiza sentymentu zarówno na podstawie klatek wideo, jak i treści audio.
- **Struktura mowy i analiza tematów**: Wykrywanie zmian tematów i ocena struktury mowy.
- **Wskaźniki czytelności**: Obliczanie wskaźników Gunning Fog i Flesch Reading Ease w celu oceny jasności i czytelności tekstu.
- **Generowanie metryk**: Generowanie słów na minutę (WPM), czasowej analizy sentymentu oraz pauz w mowie.

## Architektura

1. **Przetwarzanie wideo**: 
   - Ekstrakcja klatek i dźwięku z wideo.
   - Przeprowadzanie OCR (Optical Character Recognition) na klatkach wideo w celu wyodrębnienia tekstu widocznego na ekranie (jeśli występuje).

2. **Przetwarzanie dźwięku**:
   - Ekstrakcja dźwięku z wideo.
   - Zastosowanie wykrywania aktywności mowy (VAD) do identyfikacji pauz w mowie.
   - Transkrypcja dźwięku przy użyciu Whisper.
   
3. **Przetwarzanie tekstu**:
   - Analiza transkrybowanego tekstu pod kątem struktury i spójności.
   - Wykrywanie zmian tematów przy użyciu GPT-4.
   - Obliczanie wskaźników czytelności (Gunning Fog, Flesch Reading Ease).
   
4. **Frontend**:
   - Wyświetlanie wygenerowanych metryk (podsumowanie, sentyment, czytelność itp.) oraz analiza wideo.

![Architektura systemu](BWT.drawio.png)

## Wymagania

- Python 3.12
- Poetry
- Biblioteki (automatycznie instalowane przez Poetry):
  - torch
  - opencv-python
  - matplotlib
  - easyocr
  - nltk
  - jupyter
  - openai-whisper
  - webrtcvad
  - python-dotenv
  - pydub
  - fastapi
  - pandas
  - plotly

## Instalacja

1. Sklonuj repozytorium:

```bash
git clone <repo_url>
```

2. Zainstaluj zależności przy użyciu Poetry:

```bash
poetry install
poetry shell
```

3. Zainstaluj dodatkowe zależności przy użyciu pip:

```bash
pip install openai-whisper librosa
```

4. Skonfiguruj zmienne środowiskowe w pliku `.env`:

```bash
# .env
OPENAI_API_KEY=<twoj_openai_api_key>
```

5. Uruchom serwer FastAPI:

```bash
python src/main.py
```

6. Aby uruchomić aplikację frontendową, użyj:

```bash
streamlit run src/frontend.py
```

## Użytkowanie

1. Prześlij plik wideo za pośrednictwem frontend'u.
2. System wyodrębni dźwięk, wykryje pauzy, przetranskrybuje mowę i wygeneruje różne metryki (sentyment, wskaźniki czytelności itp.).
3. Wyniki zostaną wyświetlone na frontendzie, w tym wykresy wykrywania pauz, liczba słów na minutę oraz podsumowania treści wideo.

## Struktura katalogów

```
.
├── BWT.drawio.png          # Diagram architektury
├── Makefile                # Komendy build i setup
├── notebooks               # Notatniki Jupyter do prototypowania
│   ├── 01_transcribe.ipynb
│   └── 02_extract_audio.ipynb
├── poetry.lock             # Plik lock Poetry
├── pyproject.toml          # Konfiguracja projektu Poetry
├── README.md               # Plik README projektu
└── src                     # Kod źródłowy
    ├── data                # Przechowywanie danych
    │   ├── OutData
    │   ├── VadOutData
    │   └── Videos
    ├── frontend.py         # Frontend na Streamlit
    ├── main.py             # Backend na FastAPI
    ├── metrics             # Wskaźniki czytelności i inne metryki
    ├── ocr                 # OCR do tekstu w klatkach wideo
    ├── OpenAINodes         # Podsumowanie i analiza tematów GPT-4
    ├── pathManager         # Zarządzanie ścieżkami
    ├── transcription       # Transkrypcja na podstawie Whisper
    ├── VAD                 # Wykrywanie aktywności mowy
    ├── video_processing    # Narzędzia do przetwarzania wideo/dźwięku
    └── whisper             # Wrapper do transkrypcji Whisper
```

## Licencja

Projekt objęty licencją **CC-BY-NC-ND**.
