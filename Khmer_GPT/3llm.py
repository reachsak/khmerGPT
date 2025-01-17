import os
from groq import Groq

client = Groq(
    # This is the default and can be omitted
    api_key="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",
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "In what continent is the American country",
        }
    ],
    model="llama3-8b-8192",
)
print(chat_completion.choices[0].message.content)