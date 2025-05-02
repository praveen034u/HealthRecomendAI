import json
import requests
from langchain.memory import ConversationBufferMemory
from langchain.schema import AIMessage, HumanMessage
from fastapi import FastAPI, Request, Response

# --- Set up memory to keep track of the session ---
memory = ConversationBufferMemory(return_messages=True)


app = FastAPI()


@app.post("/ai-assistance")
 # --- Function to send prompt to external API and update memory ---
def call_api_with_memory(new_input):
    prompt = build_context_prompt(memory, new_input)

    url = "https://us-central1-aiplatform.googleapis.com/v1/projects/1000351595826/locations/us-central1/endpoints/9120516022611214336:predict"
    headers = {
        "Authorization": "Bearer ya29.a0AZYkNZjmNqvJeNi2tiWEwvIBZx7Aemz8KJ6zo6c0Kdqib6ZHPE8PSPM7X02ucrwxcdb-yFZhJbI9NOFCcAcz2zoEpq4kpKm3WSq7Mo77AUXsvEA1o72n-jDgZIOkVbAed5m4s4RGiit77ExvlIHtPMKB3c5Qjms3B_p85bHqTdAgpyt1Ucf9v-wdra10buhxT-xYq9-xuq7d_-aZsWWuYJO5RuiYCPWm1XyUUbcDRtc5gNGtj60_VKVtQoU074QNyyRwXgONY510HkLOYqX6P0fY2vQC14GSa05-t2KLg-02jfDTRp5X-tPYCCnbL_l-as0926QqNmWjUkEAORrU_oJ6XWnFZM1nZDmRFIoWiX3XFRZ36Jk4ORNsHFfnJTzl7uyJ9UHMJG0s3FwJe3C2_-dzJvoOdxYkHtOBaCgYKATISARESFQHGX2MiF_3P6bkUEzYLTMXv0VDiSg0427",
        "Content-Type": "application/json"
    }
    payload = {
        "instances": [
            {"inputs": prompt}
        ],
        "parameters": {
            "temperature": 0.5,
            "max_new_tokens": 128,
            "top_k": 50,
            "top_p": 0.9
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    response_text = response.text.strip()

    # Update memory with user input and AI response
    memory.chat_memory.add_user_message(new_input)
    memory.chat_memory.add_ai_message(response_text)

    return response_text

# --- Function to build full conversation history as input prompt ---
def build_context_prompt(memory, new_input):
    history = memory.load_memory_variables({})["history"]
    user_messages = [msg.content for msg in history if isinstance(msg, HumanMessage)]
    ai_messages = [msg.content for msg in history if isinstance(msg, AIMessage)]
    predictions = extract_all_predictions(ai_messages)

    conversation = "You are a compassionate and knowledgeable virtual health assistant.\n\nConversation History:\n"
    for user_msg, ai_msg in zip(user_messages, predictions):
        conversation += f"User: {user_msg}\nAssistant: {ai_msg}\n"

    full_prompt = conversation + f"User: {new_input}\nAssistant:"
    return full_prompt

 # --- Function to extract predictions from AI messages ---
def extract_all_predictions(ai_messages):
    all_predictions = []
    for msg in ai_messages:
        if msg:
            try:
                parsed_json = json.loads(msg)
                predictions = parsed_json.get("predictions", [])
                if isinstance(predictions, list):
                    all_predictions.extend(predictions)
            except (json.JSONDecodeError, AttributeError):
                pass  # Ignore invalid messages
    return all_predictions

