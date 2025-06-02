import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
client = OpenAI(api_key=os.getenv("PASLAPTELE"))

class LithuanianQuestionCheck(BaseModel):
    is_lithuanian_language: bool

while True:
    klausimas = input("Įveskite klausimą: ")
    
    if klausimas.lower() == "exit":
        print("Viso!.")
        break
    
    check = client.chat.completions.create(
        model="gpt-4o",
        response_model=LithuanianQuestionCheck,
        messages=[
            {"role": "system", "content": "Nustatyk ar klausimas parašytas lietuvių kalba. Atsakymą pateik JSON formatu: {\"is_lithuanian_language\": true arba false}"},
            {"role": "user", "content": klausimas}
        ]
    )
    if check.is_lithuanian_language:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Atsakyk į klausimą lietuvių kalba."},
                {"role": "user", "content": klausimas}
            ]
        )
        
        print("Atsakymas:", response.choices[0].message.content)



