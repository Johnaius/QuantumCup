from fastapi import FastAPI, HTTPException, Form

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

endpoint = os.getenv("ENDPOINT") or "<cognitive services endpoint>"
api_key = os.getenv("TEXT_ANALYTICS_API_KEY") or "<api key>"

@app.post("/analyze-sentiment")
async def analyze_sentiment(sendText: str = Form(...)):
    try:
        documents = [sendText]

        print("=== Analyze Sentiment Sample ===")

        client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

        results = client.analyze_sentiment(documents=documents)

        response_data = []

        for i, result in enumerate(results):
            if not result.is_error:
                sentiment_data = {
                    "document_text": documents[i],
                    "overall_sentiment": result.sentiment,
                    "confidence_scores": result.confidence_scores,
                    "sentences": [
                        {
                            "sentence_text": sentence.text,
                            "sentence_sentiment": sentence.sentiment,
                            "confidence_scores": sentence.confidence_scores,
                        }
                        for sentence in result.sentences
                    ],
                }
                response_data.append(sentiment_data)
            else:
                error_data = {"error": str(result.error)}
                response_data.append(error_data)

        return {"results": response_data}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))