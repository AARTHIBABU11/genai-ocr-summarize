import os
from transformers import pipeline

# 🔥 CACHE FIX
os.environ["HF_HOME"] = "./hf_cache"
os.environ["TRANSFORMERS_CACHE"] = "./hf_cache"

model_name = "google/flan-t5-small"

summarizer = pipeline(
    "summarization",
    model=model_name
)

# ----------------------------
# SAFE TOKEN-BASED CHUNKING
# ----------------------------
def chunk_text(text, max_chars=1000):
    """
    Safer than word split (avoids 512 token crash indirectly)
    """
    for i in range(0, len(text), max_chars):
        yield text[i:i + max_chars]


# ----------------------------
# MAIN SUMMARIZER
# ----------------------------
def summarize_long_text(text):
    summaries = []

    for chunk in chunk_text(text):
        chunk = chunk.strip()
        if not chunk:
            continue

        try:
            result = summarizer(
                chunk,
                max_length=120,
                min_length=30,
                do_sample=False
            )

            summaries.append(result[0]["summary_text"])

        except Exception as e:
            print("Skipping chunk due to error:", e)

    return " ".join(summaries)