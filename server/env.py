import random

class EmailEnv:
    def __init__(self):
        self.easy = [
            ("Win money now!!!", "spam"),
            ("Free lottery offer", "spam"),
        ]

        self.medium = [
            ("Meeting at 5pm", "important"),
            ("Project deadline tomorrow", "important"),
        ]

        self.hard = [
            ("Hello friend", "normal"),
            ("Just checking in", "normal"),
        ]

        self.emails = self.easy + self.medium + self.hard

        self.current = None
        self.steps = 0
        self.max_steps = 3

    def reset(self):
        self.steps = 0
        self.current = random.choice(self.emails)
        return self.state()

    def state(self):
        return {
            "email": self.current[0],
            "step": self.steps
        }

    def step(self, action):
        correct = self.current[1]

        # Better reward shaping
        if action == correct:
            reward = 1.0
        elif correct in action or action in correct:
            reward = 0.5
        else:
            reward = -0.2   # penalty (ADVANCED!)

        self.steps += 1
        done = self.steps >= self.max_steps

        # next email
        self.current = random.choice(self.emails)

        return self.state(), reward, done, {}
