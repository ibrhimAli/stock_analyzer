# utils.py
import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def summarize_output(output_text):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-4"
        messages=[
            {"role": "system", "content": "You are a stock trader expert also an expert in AI, you will write a detailed summary to the customer to tell wither to BUY or SELL. You must reply in pure egyptian language/accent"},
            {"role": "user", "content": f"Please check: {output_text}"}
        ],
        max_tokens=600,
        temperature=0.7,
    )
    return response.choices[0].message['content'].strip()
