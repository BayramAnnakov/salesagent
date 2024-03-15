from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import FunctionTool

with open('bayram_linkedin_profile.txt','r') as file:
    profile = file.read()


def search_linkedin(name: str) -> str:
    """Searches LinkedIn profile for a given name and returns the profile information"""
    print(f"Searching LinkedIn for {name}")
    return profile

linkedin_tool = FunctionTool.from_defaults(fn=search_linkedin)

llm = OpenAI(model="gpt-4-0125-preview")

agent = OpenAIAgent.from_tools([linkedin_tool], llm=llm, verbose=True)

response = agent.chat("Prepare a memo how to prepare for a sales call with a customer Bayram Annakov using info from their LinkedIn profile.")
print(str(response))