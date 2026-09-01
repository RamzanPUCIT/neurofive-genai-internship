import os
import json
from dotenv import load_dotenv
from groq import Groq
from prompt import SYSTEM_PROMPT

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "openai/gpt-oss-120b"


def analyze_resume(resume_text: str, target_role: str) -> dict:
    """Resume text + target role leta hai, structured feedback json return karta hai."""

    user_message = f"""Target role: {target_role}

Resume text:
\"\"\"
{resume_text}
\"\"\"

Analyse this resume against the target role and return the json object."""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
        max_tokens=3000,
    )

    return json.loads(response.choices[0].message.content)