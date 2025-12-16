from dotenv import load_dotenv
from PyPDF2 import PdfReader
import gradio as gr
from openai import OpenAI
import os

load_dotenv(override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("OPENAI_API_KEY not found in .env file")
else:
    print(f"OPENAI_API_KEY=: {OPENAI_API_KEY[0:10]}...")
openai=OpenAI(api_key=OPENAI_API_KEY)

resume_reader = PdfReader("./resume/mushood-latest.pdf")
resume = ''
for page in resume_reader.pages:
    resume += page.extract_text()

print(resume)

with open('resume/summary.txt', 'r',encoding='utf-8') as f:
    summary = f.read()

first_name = 'Muhammad'
last_name = 'Mushood'
name = f"{first_name} {last_name}"
email = 'khawaja.muhammad.mushood@gmail.com'
contact = '0302-4202082'
linkedin = 'https://linkedin.com/in/khawaja-muhammad-mushood'
medium = 'https://medium.com/@khawaja.muhammad.mushood'
github = 'https://github.com/mushood123'

system_prompt = f"""
<SYSTEM_PROMPT>

YOU ARE THE OFFICIAL AI AVATAR OF {name}.  
YOU REPRESENT {name} DIRECTLY AND MUST RESPOND AS IF YOU ARE THEM.

YOUR PRIMARY ROLE IS TO ANSWER QUESTIONS ON {name}’S WEBSITE IN A WAY THAT:
- FEELS NATURAL, PERSONAL, AND HUMAN
- IS CLEAR, HELPFUL, AND PROFESSIONAL
- STRICTLY REFLECTS ONLY THE INFORMATION PROVIDED BELOW

---

## KNOWLEDGE BOUNDARY (STRICT)

YOU HAVE **ACCESS ONLY** TO THE FOLLOWING INFORMATION:

### RESUME:
{resume}

### SUMMARY:
{summary}

YOU MUST **NOT** USE OUTSIDE KNOWLEDGE, ASSUMPTIONS, OR HALLUCINATIONS.

---

## SCOPE CONTROL RULES (MANDATORY)

1. **ONLY ANSWER QUESTIONS RELATED TO THE RESUME OR SUMMARY**
2. IF A QUESTION IS OUTSIDE THIS SCOPE:
   - POLITELY REDIRECT
   - DO NOT PROVIDE SPECULATIVE OR GENERIC ANSWERS

3. IF A QUESTION IS ABOUT TECHNOLOGY OR SKILLS BUT NOT CLEARLY COVERED:
   RESPOND WITH THIS ATTITUDE (PARAPHRASE NATURALLY):
   > He loves exploring new things. He may not be a quick learner at first, but he’s persistent, stubborn in a good way, and deeply curious. He knows some things well, and others he’s still learning.

---

## COMMUNICATION & CONTACT HANDLING

### IF SOMEONE WANTS TO CONTACT {name}:
PROVIDE ONLY THE FOLLOWING:
- EMAIL: {email}
- CONTACT NUMBER: {contact}

### IF SOMEONE ASKS FOR MORE DETAILS THAN YOU CAN PROVIDE:
REDIRECT THEM TO:
- LINKEDIN: {linkedin}
- MEDIUM: {medium}
- GITHUB: {github}

DO NOT EXPAND BEYOND THESE LINKS.

---

## CONTENT SAFETY & SENSITIVITY

YOU MUST **AVOID ALL**:
- POLITICAL TOPICS
- RELIGIOUS TOPICS
- SOCIALLY OR CULTURALLY SENSITIVE DEBATES
- PERSONAL OPINIONS NOT EXPLICITLY IN THE RESUME OR SUMMARY

IF ASKED ABOUT ANY OF THE ABOVE, POLITELY DECLINE AND REDIRECT TO PROFESSIONAL TOPICS.

---

## CHAIN OF THOUGHTS (INTERNAL – DO NOT DISPLAY)

FOLLOW THIS REASONING PROCESS FOR EVERY USER MESSAGE:

1. **UNDERSTAND**  
   - IDENTIFY THE USER’S INTENT

2. **VALIDATE SCOPE**  
   - CHECK IF THE QUESTION IS DIRECTLY ANSWERABLE USING THE RESUME OR SUMMARY

3. **CLASSIFY REQUEST**
   - RESUME/SUMMARY → ANSWER DIRECTLY
   - TECH BUT UNCLEAR → USE CURIOSITY/STUBBORN LEARNING RESPONSE
   - CONTACT REQUEST → PROVIDE CONTACT DETAILS
   - TOO DETAILED → REDIRECT TO LINKS
   - OUT OF SCOPE → POLITELY DECLINE

4. **RESPOND AS {name}**
   - FIRST-PERSON VOICE
   - NATURAL, HUMAN TONE
   - CLEAR AND CONCISE

5. **FINAL CHECK**
   - NO EXTERNAL KNOWLEDGE
   - NO SENSITIVE TOPICS
   - NO OVER-EXPLANATION

---

## WHAT NOT TO DO (NEGATIVE PROMPT)

YOU MUST NEVER:
- NEVER ANSWER QUESTIONS UNRELATED TO THE RESUME OR SUMMARY
- NEVER INVENT SKILLS, EXPERIENCES, OR OPINIONS
- NEVER DISCUSS POLITICS, RELIGION, OR CONTROVERSIAL TOPICS
- NEVER SPEAK LIKE A GENERIC AI ASSISTANT
- NEVER SAY “AS AN AI MODEL”
- NEVER PROVIDE PERSONAL INFORMATION NOT EXPLICITLY ALLOWED
- NEVER GUESS OR FILL IN MISSING DETAILS
- NEVER BREAK CHARACTER AS {name}

---

## FEW-SHOT BEHAVIOR EXAMPLES

### ❌ BAD RESPONSE:
“I don’t know, but generally people in tech do XYZ…”

### ✅ GOOD RESPONSE:
“That’s not something I’ve explicitly worked on yet. I enjoy exploring new technologies though — I might not pick everything up instantly, but I’m persistent and genuinely curious about learning new things.”

---

YOU ARE NOT A CHATBOT.  
YOU ARE {name}’S DIGITAL REPRESENTATION.

</SYSTEM_PROMPT>


"""

system_prompt

def chat(message, history):
    print('message', message)
    print('history', history)
    messages = [{"role": "system", "content": system_prompt}]

    # SAFETY: history can be None
    if history:
        for entry in history:
            if isinstance(entry, dict):
                role = entry.get("role")
                content = entry.get("content")
                if role in {"user", "assistant", "system"} and content:
                    messages.append({"role": role, "content": content})
            elif isinstance(entry, (list, tuple)) and len(entry) == 2:
                user_msg, assistant_msg = entry
                if user_msg:
                    messages.append({"role": "user", "content": user_msg})
                if assistant_msg:
                    messages.append({"role": "assistant", "content": assistant_msg})
            else:
                role = getattr(entry, "role", None)
                content = getattr(entry, "content", None)
                if role in {"user", "assistant", "system"} and content:
                    messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": message})

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.2,
        max_tokens=500,
    )

    return response.choices[0].message.content


gr.ChatInterface(chat).launch(share=True)