import os
from env import EmailEnv

# OPTIONAL: OpenAI client
try:
    from openai import OpenAI
    client = OpenAI(base_url=os.getenv("API_BASE_URL"))
    MODEL = os.getenv("MODEL_NAME", "gpt-4o-mini")
    USE_LLM = True
except:
    USE_LLM = False

env = EmailEnv()

print("[START]")

def llm_agent(email):
    prompt = f"""
    Classify this email into one of: spam, important, normal.

    Email: {email}

    Answer only one word.
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip().lower()


def smart_agent(email):
    email = email.lower()

    if "win" in email or "free" in email:
        return "spam"
    elif "meeting" in email or "deadline" in email:
        return "important"
    else:
        return "normal"


state = env.reset()
done = False
total_reward = 0
steps = 0

while not done:
    print("[STEP]", state)

    if USE_LLM:
        action = llm_agent(state["email"])
    else:
        action = smart_agent(state["email"])

    state, reward, done, _ = env.step(action)

    total_reward += reward
    steps += 1

    print("Action:", action)
    print("Reward:", reward)

# FINAL SCORE
score = max(0, min(1, total_reward / steps))

print("[END]")
print("Final Score:", score)