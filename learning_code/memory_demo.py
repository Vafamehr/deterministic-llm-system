class SessionMemory:
    def __init__(self):
        self.summary = ""
        self.last_task = ""
        self.entities = []

    def update(self, task, entities):
        self.last_task = task
        self.entities = entities
        self.summary = f"Working on {task} involving {', '.join(entities)}"

    def read(self):
        return {
            "summary": self.summary,
            "last_task": self.last_task,
            "entities": self.entities
        }



if __name__ == "__main__":
    memory = SessionMemory()

    memory.update("contract review", ["Contract A"])
    print(memory.read())

    memory.update("deadline extraction", ["Contract A"])
    print(memory.read())
