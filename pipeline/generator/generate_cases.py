import csv
import json
import time
from openai import OpenAI

client = OpenAI()

PROMPT = open("pipeline/prompts/v1.txt", "r", encoding="utf-8").read()


def generate_cases():
    start = time.time()

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": PROMPT
            }
        ]
    )

    content = response.choices[0].message.content

    with open("pipeline/logs/run.log", "a", encoding="utf-8") as f:
        f.write(content + "\n")

    with open("pipeline/outputs/cases.json", "w", encoding="utf-8") as f:
        f.write(content)

    duration = time.time() - start

    print("Generation completed in", duration)


if __name__ == "__main__":
    generate_cases()
