
from lab2_model import ClassroomAgent
agent = ClassroomAgent()

percepts = [
    (29, True),
    (29, True),
    (20, True),
    (26, True),
    (19, True),
    (29, False)
]

print("STATEFUL CLASSROOM AGENT")

for step, percept in enumerate(percepts, 1):
    previous = agent.previous_mode
    target, send = agent.act(*percept)

    if send:
        result = "Send command"
    else:
        result = "No command needed"

    print(
        "Step:", step,
        "| Previous:", previous,
        "| Percept:", percept,
        "| Target:", target,
        "| Result:", result
    )
