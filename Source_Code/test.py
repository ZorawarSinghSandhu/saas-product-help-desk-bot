from groq import Groq
import os
from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict
import json

class Person(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    Name: str
    Age: int
    Nationality: str


class JsonSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    People: list[Person]
    

paragraph = "John Miller is a 34-year-old American teacher who enjoys helping students develop their skills and confidence. Priya Sharma is a 28-year-old Indian software developer who works on innovative technology projects. Carlos Rodriguez is a 41-year-old Mexican architect known for designing sustainable buildings. Emma Wilson is a 25-year-old British journalist who loves traveling and writing about different cultures. Hiroshi Tanaka is a 37-year-old Japanese scientist who conducts research in the field of environmental conservation."


load_dotenv(override=True)

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)
chat = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "I need you to extract and provide me the details of the people in the text provided. Return only valid JSON."
        },
        
        {
            "role": "user",
            "content": paragraph
        }
    ],
    model="openai/gpt-oss-20b",
    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "Invoice_Schema",
            "strict": True,
            "schema": JsonSchema.model_json_schema()
        }
    }
)

result = json.loads(chat.choices[0].message.content)

print(json.dumps(result, indent=4))