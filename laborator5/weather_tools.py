import os
import json
import random
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


def get_current_weather(city: str) -> str:
    temperatures = {
        "bucuresti": (18, 28),
        "cluj-napoca": (12, 22),
        "timisoara": (14, 24),
        "iasi": (10, 20),
        "constanta": (16, 26),
        "brasov": (8, 18),
        "sibiu": (10, 20),
    }

    temp_range = temperatures.get(city.lower().strip(), (5, 15))
    temp = random.randint(*temp_range)
    conditions = random.choice(["senin", "partial noros", "noros", "ploaie usoara"])
    return json.dumps({
        "city": city.title(),
        "temperature": f"{temp}°C",
        "condition": conditions,
    })


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Obtine vremea curenta pentru un oras",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Numele orasului",
                    }
                },
                "required": ["city"],
            },
        },
    }
]

oras = input("Introdu numele orasului: ")

messages = [
    {"role": "user", "content": f"Cum e vremea la {oras}?"}
]

model = os.getenv("LLM_MODEL", "llama3.1")
response = client.chat.completions.create(
    model=model,
    messages=messages,
    tools=tools,
    tool_choice="auto",
)

choice = response.choices[0]

if choice.finish_reason == "tool_calls":
    tool_call = choice.message.tool_calls[0]
    if tool_call.function.name == "get_current_weather":
        args = json.loads(tool_call.function.arguments)
        result = get_current_weather(**args)

        messages.append(choice.message)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result,
        })

        final = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
        )
        print(final.choices[0].message.content)
else:
    print(choice.message.content)
