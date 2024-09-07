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
    model="llama3-70b-8192",
)
print(chat_completion.choices[0].message.content)