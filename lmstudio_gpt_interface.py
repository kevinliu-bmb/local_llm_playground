import json
import requests
import time

openai_api_key = "OPENAI_API_KEY_HERE"

# Initialize URLs and Headers
gpt3_url = "https://api.openai.com/v1/chat/completions"
gpt3_headers = {
    "Authorization": f"Bearer {openai_api_key}",  # Replace with your actual API key
    "Content-Type": "application/json"
}

local_llm_url = "http://localhost:1022/v1/chat/completions"
llm_headers = {"Content-Type": "application/json"}

# Function to get chat-based completion from GPT-3.5
def get_gpt3_chat_completion(messages):
    payload = {"model": "gpt-3.5-turbo", "messages": messages}
    response = requests.post(gpt3_url, headers=gpt3_headers, json=payload)

    print(f"GPT-3.5 Status Code: {response.status_code}")
    print(f"GPT-3.5 Raw Response: {response.text}")

    if response.status_code == 200:
        try:
            return json.loads(response.text)['choices'][0]['message']['content']
        except (KeyError, json.JSONDecodeError):
            print("Unexpected GPT-3.5 API response format.")
            return None
    else:
        print(f"Failed GPT-3.5 request. Status Code: {response.status_code}, Response: {response.text}")
        return None

# Function to get chat completion from LLM
def get_llm_chat_completion(messages):
    payload = {
        "messages": messages,
        "stop": ["Instruction:"],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }
    response = requests.post(local_llm_url, headers=llm_headers, json=payload)
    
    print(f"LLM Status Code: {response.status_code}")  # Debugging line
    print(f"LLM Raw Response: {response.text}")  # Debugging line
    time.sleep(10)  # Debugging line
    if response.status_code == 200:
        try:
            return json.loads(response.text)['choices'][0]['message']['content']
        except (KeyError, json.JSONDecodeError):
            print("Unexpected LLM API response format.")
            return None
    else:
        print(f"Failed LLM request. Status Code: {response.status_code}, Response: {response.text}")
        return None

if __name__ == "__main__":
    gpt3_input = "hello, how are you?"
    gpt3_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Translate the following English text to Spanish: {gpt3_input}"}
    ]

    gpt3_output = get_gpt3_chat_completion(gpt3_messages)

    if gpt3_output:
        llm_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": gpt3_output}
        ]
        llm_output = get_llm_chat_completion(llm_messages)

        if llm_output:
            print(f"LLM Output: {llm_output}")
