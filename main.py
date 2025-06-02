import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Load your OpenAI API key
load_dotenv()
api_key = os.getenv("PASLAPTELE")

# Define Pydantic model for structured output
class LithuanianQuestionCheck(BaseModel):
    is_lithuanian_language: bool

# Create a bound model for language check
model_check = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    api_key=api_key
).bind(
    response_model=LithuanianQuestionCheck,
    json_mode=True
)

# Create a regular model for answeringl
model_answer = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    api_key=api_key
)

# Start asking
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