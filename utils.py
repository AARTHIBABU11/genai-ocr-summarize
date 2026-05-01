def clean_text(text):
    # remove repeated whitespace
    text = " ".join(text.split())

    # remove duplicate sentences (basic cleanup)
    sentences = list(dict.fromkeys(text.split(".")))

    return ".".join(sentences)