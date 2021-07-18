import os
import fitz
import json


def get_pdfs(folder="."):
    return [f for f in os.listdir(folder) if ".pdf" in f]


def parse_page_text(text: str):
    sentences = text.replace("\t", " ").split("\n")

    quote = ""
    explanation = ""
    end_quote_symbol = "”"
    start_source_symbol = "—"
    quote_found = False
    quote_source_found = False

    if len(sentences[0]) == 1:
        for index, sentence in enumerate(sentences):
            if index == 0:
                missing_char = sentence
            elif index == 1:
                date = sentence[:-2]
            elif index == 2:
                title = sentence
            else:
                if not quote_found:
                    if sentence[0] == start_source_symbol:
                        quote_found = True
                        quote_source = sentence
                        quote_source_found = True

                    if sentence[-1] != end_quote_symbol:
                        quote += sentence
                    else:
                        quote += sentence
                        quote_found = True
                else:
                    if not quote_source_found:
                        quote_source = sentence
                        quote_source_found = True
                        explanation += missing_char
                    else:
                        explanation += sentence
    else:
        for index, sentence in enumerate(sentences):
            if index == 0:
                date = sentence[:-2]
            elif index == 1:
                title = sentence
            else:
                if not quote_found:
                    if sentence[-1] != end_quote_symbol:
                        quote += sentence
                    else:
                        quote += sentence
                        quote_found = True
                else:
                    if not quote_source_found:
                        quote_source = sentence
                        quote_source_found = True
                    else:
                        explanation += sentence

    return date, title, quote, quote_source, explanation


def extract_text(pdf_file, start, end, breaks):
    entries = {}

    with fitz.open(pdf_file) as f:
        for page in f:
            if page.number < start:
                continue
            if page.number > end:
                break
            if page.number in breaks:
                continue

            date, title, quote, source, explanation = parse_page_text(page.getText())
            entries[date] = {
                "title": title,
                "quote": quote,
                "quote_source": source,
                "explanation": explanation
            }

    return entries


if __name__ == "__main__":

    # These are specific to Ishan's copy of the Daily Stoic
    start_page = 14
    end_page = 392
    skip = [45, 75, 107, 138, 139, 171, 202, 234, 266, 267, 298, 330, 361]

    data = extract_text("The Daily Stoic.pdf", start=start_page, end=end_page, breaks=skip)

    with open("Stoic_log.json", "w") as fout:
        json.dump(data, fout, indent=4)
