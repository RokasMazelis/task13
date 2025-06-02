import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# 1. Load API key from .env
load_dotenv()
api_key = os.getenv("PASLAPTELE")

# 2. Define Pydantic model for structured output
class LithuanianQuestionCheck(BaseModel):
    is_lithuanian_language: bool

# 3. Set up the model WITH bind() and proper structure
model_check = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    api_key=api_key
).bind(
    response_model=LithuanianQuestionCheck,
    json_mode=True
)

# 4. Standard model for answering questions
model_answer = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    api_key=api_key
)

# 5. Main loop
while True:
    klausimas = input("Įveskite klausimą, jei nori išeit 'exit': ")

    if klausimas.lower() == "exit":
        print("Viso!")
        break

    try:
        check = model_check.invoke([
            SystemMessage(content="Nustatyk ar klausimas parašytas lietuvių kalba. Atsakyk JSON formatu: {\"is_lithuanian_language\": true arba false}"),
            HumanMessage(content=klausimas)
        ])
    except Exception as e:
        print("Klaida tikrinant kalbą:", e)
        continue

    if check.is_lithuanian_language:
        response = model_answer.invoke([
            SystemMessage(content="Atsakyk į klausimą lietuvių kalba."),
            HumanMessage(content=klausimas)
        ])
        print("Atsakymas:", response.content)
    else:
        print("Klausimas užduotas nelietuviškai.")