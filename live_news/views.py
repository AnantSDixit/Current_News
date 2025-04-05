from django.shortcuts import render
import requests
from django.http import JsonResponse
from transformers import pipeline
import json
from django.views.decorators.csrf import csrf_exempt



# Load the text generation model
generator = pipeline("text-generation", model="gpt2")

NEWS_API_KEY = "31bb8b7b29e04b1b98d8215d1f67819c"
NEWS_API_URL = "https://newsapi.org/v2/everything"

def fetch_news(query):
    """Fetch current news based on the user query using NewsAPI."""
    params = {
        'q': query,
        'apiKey': NEWS_API_KEY,
        'pageSize': 5,  # Return top 5 results
        'sortBy': 'publishedAt'
    }
    response = requests.get(NEWS_API_URL, params=params)
    if response.status_code == 200:
        return response.json()['articles']
    else:
        return []

def generate_answer(query, context):
    """Generate a relevant answer based on the context of the news articles."""
    generator.tokenizer.pad_token = generator.tokenizer.eos_token
    full_context = " ".join([article['title'] + ". " + article['description'] for article in context])
    input_text = f"Question: {query}\nContext: {full_context}\nAnswer:"
    #generator.tokenizer.pad_token = generator.tokenizer.eos_token
    #max_length=150
    return generator(input_text, max_new_tokens=150, truncation=True, padding=True, num_return_sequences=1)[0]['generated_text']

def index(request):
    """Render the homepage."""
    return render(request, 'index.html')
@csrf_exempt
def query(request):
    """API endpoint to accept user query and return the generated answer."""
    try:
        user_query = json.loads(request.body).get('query')
        if not user_query:
            return JsonResponse({"error": "No query provided"}, status=400)
        
        # Fetch current news based on the user query
        news_articles = fetch_news(user_query)
        
        if not news_articles:
            return JsonResponse({"error": "No news articles found"}, status=404)
        
        # Generate a relevant answer using the news articles as context
        answer = generate_answer(user_query, news_articles)
        
        return JsonResponse({"answer": answer})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
