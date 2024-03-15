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

with open('bad_sales_call.txt','r') as file:
    call_transcript = file.read()

def get_meeting_transcript(meeting_id: str) -> str:
    """Gets the transcript of a meeting with a given ID"""
    print(f"Getting transcript for meeting {meeting_id}")
    return call_transcript

meeting_transcript_tool = FunctionTool.from_defaults(fn=get_meeting_transcript)

llm = OpenAI(model="gpt-4-0125-preview")

agent = OpenAIAgent.from_tools([linkedin_tool, meeting_transcript_tool], llm=llm, verbose=True, system_prompt="You are sales coach for Empatika Labs company. You help sales managers to prepare for meetings, analyze their sales calls and provide feedback.")

response = agent.chat("Prepare a memo how to prepare for a sales call with a customer Bayram Annakov using info from their LinkedIn profile.")
print(str(response))

response = agent.chat("Analyze the sales call with Bayram Annakov and provide feedback.")

print(str(response))