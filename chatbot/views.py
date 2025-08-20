import os
import requests
from django.shortcuts import render
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # this loads .env into environment variables

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def fetch_wikipedia_summary(query):
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + query.replace(" ", "_")
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("extract")
    return None

def chat_view(request):
    bot_response = ""
    user_message = ""

    if request.method == "POST":
        user_message = request.POST.get("message")

        # Try to get live info
        live_info = fetch_wikipedia_summary(user_message)

        messages = [
            {"role": "system", "content": "You are a helpful assistant that uses live data when available."}
        ]

        if live_info:
            messages.append({"role": "system", "content": f"Here is live info: {live_info}"})
        
        messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        bot_response = response.choices[0].message.content

    return render(request, "chatbot/chat.html", {
        "user_message": user_message,
        "bot_response": bot_response
    })
