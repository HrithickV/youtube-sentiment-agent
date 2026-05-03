from transformers import pipeline

def load_sentiment_model():
    print("Loading-sentimental-model..")
    model = pipeline("sentiment-analysis")
    print("model-loaded!!")
    return model

def analyze_sentiment(model, text):

    text = text[:512]
    result = model(text)[0]
    label = result["label"]
    score = result["score"]
    return label, score

if __name__ == "__main__":
    model = load_sentiment_model()
    label, score = analyze_sentiment(model, "This video is absolutely amazing!")
    print(f"Label: {label}, Score: {score}")