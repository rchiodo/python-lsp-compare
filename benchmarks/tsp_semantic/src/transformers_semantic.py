from transformers import AutoTokenizer, pipeline


MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"


def make_sentiment_pipeline() -> tuple[str, object]:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer_name = tokenizer.name_or_path
    sentiment = pipeline("sentiment-analysis", model=MODEL_NAME, tokenizer=tokenizer)
    return tokenizer_name, sentiment


tokenizer_name, classifier = make_sentiment_pipeline()
predictions = classifier(["copilot helps with benchmarks"])
first_label = predictions[0]["label"]
