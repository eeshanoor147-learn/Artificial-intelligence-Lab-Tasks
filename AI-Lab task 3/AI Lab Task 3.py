class ModelAgent:
    def __init__(self, desired_temperature):
        self.desired_temperature = desired_temperature
        self.previous_action = None

    def perceive(self, temperature):
        return temperature
    def act(self, temperature):

        if temperature < self.desired_temperature:
            action = "Turn on heater"
        else:
            action = "Turn off heater"

        if action == self.previous_action:
            return "No change needed"
        self.last_action = action
        return action
rooms = {
    "Living Room": 18,
    "Bedroom": 22,
    "Kitchen": 20,
    "Bathroom": 24
}
agent = ModelAgent(22)
for room, temp in rooms.items():
    temperature = agent.perceive(temp)
    action = agent.act(temperature)
    print(room, ":", action)