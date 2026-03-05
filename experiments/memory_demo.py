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
    
    def summarize_interaction(self, user_input):
        if "contract" in user_input.lower():
            self.last_task = "contract analysis"

        if "deadline" in user_input.lower():
            self.summary += " Tracking deadlines."

        if "payment" in user_input.lower():
            self.summary += " Reviewing payment terms."

class LongTermMemory:
    def __init__(self):
        self.user_profile = {
            "domain": None,
            "jurisdiction": None,
            "preferences": []
        }

    def update_profile(self, domain=None, jurisdiction=None, preference=None):
        if domain:
            self.user_profile["domain"] = domain
        if jurisdiction:
            self.user_profile["jurisdiction"] = jurisdiction
        if preference:
            self.user_profile["preferences"].append(preference)

    def read(self):
        return self.user_profile

def build_context(session_memory, long_term_memory):
    session = session_memory.read()
    profile = long_term_memory.read()

    context = f"""
    Task Summary: {session['summary']}
    Last Task: {session['last_task']}
    Entities: {', '.join(session['entities'])}

    Domain: {profile['domain']}
    Jurisdiction: {profile['jurisdiction']}
    Preferences: {', '.join(profile['preferences'])}
    """

    return context.strip()


# if __name__ == "__main__":
#     memory = SessionMemory()

    # memory.update("contract review", ["Contract A"])
    # print(memory.read())

    # memory.update("deadline extraction", ["Contract A"])
    # print(memory.read())

if __name__ == "__main__":
    memory = SessionMemory()

    memory.summarize_interaction("Review Contract A")
    memory.summarize_interaction("Focus on payment terms")
    memory.summarize_interaction("Now extract deadlines")

    print(memory.read())

    ltm = LongTermMemory()
    ltm.update_profile(domain="immigration law", jurisdiction="Texas", preference="concise answers")

    print(ltm.read())

    context_block = build_context(memory, ltm)
    print("\n--- Context Sent to LLM ---")
    print(context_block)



