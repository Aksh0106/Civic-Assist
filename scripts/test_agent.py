from agent.agent import CitizenIssueAgent

agent = CitizenIssueAgent()

sample = "Open manhole near school, dangerous for kids."
result = agent.run(sample)

for k, v in result.items():
    print(f"{k.upper()}:\n{v}\n")
