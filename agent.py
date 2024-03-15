from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import FunctionTool
from llama_index.tools.google import GoogleCalendarToolSpec

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

gcal_tools = GoogleCalendarToolSpec().to_tool_list()

llm = OpenAI(model="gpt-4-0125-preview")

agent = OpenAIAgent.from_tools([linkedin_tool, meeting_transcript_tool, gcal_tools[0]], llm=llm, verbose=True, system_prompt="You are sales coach for Empatika Labs company. You help sales managers to prepare for meetings, analyze their sales calls and provide feedback.")

response = agent.chat("Search the upcoming sales calendar events on March 17th 2024.")

print(str(response))

response = agent.chat("Prepare a memo how to prepare for this sales call using info about the event participant from their LinkedIn profile.")
print(str(response))

response = agent.chat("Analyze the sales call and provide feedback.")

print(str(response))