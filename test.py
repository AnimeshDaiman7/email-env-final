from env import EmailEnv

env = EmailEnv()

print(env.reset())
print(env.state())
print(env.step("spam"))