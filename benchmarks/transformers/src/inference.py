from transformers import AutoTokenizer, pipeline


MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"


def build_sentiment_pipeline():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer_name = tokenizer.name_or_path
    sentiment = pipeline("sentiment-analysis", model=MODEL_NAME, tokenizer=tokenizer)
    return sentiment


classifier = build_sentiment_pipeline()
predictions = classifier(["copilot is helpful"])
first_prediction = predictions[0]