---
title: Email RL Environment
emoji: 📧
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---
force rebuild

# 📧 Email Classification RL Environment (OpenEnv)

## 🚀 Overview

This project implements a **real-world Reinforcement Learning (RL) environment** using the OpenEnv specification.
The environment simulates an **email classification system**, where an AI agent learns to categorize emails into:

* 📩 **Spam**
* 📌 **Important**
* 💬 **Normal**

This environment is designed to evaluate and train intelligent agents in a **practical automation scenario** used in real-world applications such as email filtering and prioritization.

---

## 🎯 Objectives

* Build a fully functional OpenEnv-compatible environment
* Simulate a realistic classification task (not a toy problem)
* Design meaningful reward signals
* Evaluate agent performance with structured scoring

---

## 🧠 Environment Design

### 🔹 State Space

Each state contains:

```json
{
  "email": "<email content>",
  "step": <current step number>
}
```

---

### 🔹 Action Space

The agent can choose one of the following actions:

* `"spam"`
* `"important"`
* `"normal"`

---

### 🔹 Transition Logic

* The environment randomly selects emails from different difficulty levels
* Each step presents a new email
* Episodes consist of **multiple steps (multi-step RL environment)**

---

## 📊 Tasks & Difficulty Levels

The environment includes **3 levels of tasks**:

### 🟢 Easy

* Obvious spam emails
* Example: `"Win money now!!!"`

### 🟡 Medium

* Structured work-related emails
* Example: `"Meeting at 5pm"`

### 🔴 Hard

* Ambiguous casual emails
* Example: `"Hello friend"`

---

## 🎁 Reward Function

The reward system is designed to provide **dense feedback**:

| Condition                | Reward |
| ------------------------ | ------ |
| Correct classification   | +1.0   |
| Partial match            | +0.5   |
| Incorrect classification | -0.2   |

✔ Encourages correct decisions
✔ Penalizes wrong actions
✔ Supports learning over time

---

## 🔁 Episode Structure

* Each episode runs for **multiple steps (default: 3)**
* The environment resets after completion
* Provides continuous feedback across steps

---

## 🤖 Agent Design

### 1. Rule-Based Agent (Default)

* Uses keyword-based logic
* Fast and deterministic

### 2. LLM-Based Agent (Optional)

* Uses OpenAI API for classification
* Controlled via environment variables:

```bash
API_BASE_URL=<your_api_url>
MODEL_NAME=<model_name>
HF_TOKEN=<optional>
```

✔ Falls back to rule-based agent if API is unavailable

---

## 📈 Evaluation

The agent’s performance is measured using:

```text
Final Score = Average reward per step (normalized to [0,1])
```

✔ Ensures fair and consistent evaluation
✔ Matches hackathon scoring constraints

---

## 🛠️ Project Structure

```
.
├── env.py              # Environment implementation
├── inference.py       # Agent execution script
├── openenv.yaml       # Environment configuration
├── Dockerfile         # Container setup
├── README.md          # Documentation
```

---

## ▶️ How to Run

### 🔹 Local Execution

```bash
python inference.py
```

---

### 🔹 Expected Output

```
[START]
[STEP] {'email': 'Win money now!!!'}
Action: spam
Reward: 1.0
...
[END]
Final Score: 0.66
```

---

## 🐳 Docker Support

Build and run:

```bash
docker build -t email-env .
docker run email-env
```

---

## ☁️ Deployment

This project is deployed on **Hugging Face Spaces** using Docker:

👉 (Add your Space link here)

---

## ✅ OpenEnv Compliance

✔ Implements:

* `reset()`
* `step()`
* `state()`

✔ Includes:

* Typed environment logic
* Structured logs `[START] → [STEP] → [END]`
* Reward in range `[0,1]`
* Multiple tasks with graders

---

## 🔍 Key Features

* Real-world simulation (email automation)
* Multi-step RL environment
* Reward shaping with penalties
* Hybrid AI agent (rule-based + LLM)
* Clean modular design
* Dockerized deployment

---

## 🚀 Why This Project Stands Out

* Not a toy environment — solves a real problem
* Supports both classical and LLM-based agents
* Designed for evaluation, not just simulation
* Easily extensible for advanced RL research

---

## 📌 Future Improvements

* Add dataset-driven email corpus
* Train RL agents (DQN / PPO)
* Add web UI (Gradio / Streamlit)
* Improve LLM prompting & scoring

---

## 👨‍💻 Author

**Animesh Daiman**

---

## 🏁 Conclusion

This project demonstrates how reinforcement learning environments can be applied to **real-world automation problems**, providing a foundation for building intelligent, adaptive systems.

---
