import base64
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GPT4_KEY')

def generate_image_description(image_data):
    # Encode the image data to base64
    encoded_image = base64.b64encode(image_data).decode('utf-8')

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "What’s in this image?"
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{encoded_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 100
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        # Extract and return the generated description
        if data and 'choices' in data and data['choices']:
            description = data['choices'][0]['message']['content']
            return description
        else:
            return "No description found"
    else:
        return "Failed to generate description"

