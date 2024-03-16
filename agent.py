from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import FunctionTool
from llama_index.tools.google import GoogleCalendarToolSpec

import requests
import requests_cache
import os
import csv

from typing import Dict, Any

from utils import get_zoom_token
from crm import insert_or_update_customer
from salesagentincentives_client import create_job, complete_job, fund_job, release_payment

requests_cache.install_cache('api_cache', expire_after=3600)



def search_linkedin(firstName: str, lastName: str, companyName: str) -> str:
    """Searches LinkedIn profile for person's first and last name, company name and returns the profile information"""
    print(f"Searching LinkedIn for {firstName} {lastName} from {companyName}")

    headers = {'Authorization': 'Bearer ' + os.environ['PROXYCURL_API_KEY']}
    api_endpoint = 'https://nubela.co/proxycurl/api/linkedin/profile/resolve'

    params = {
        "first_name": firstName,
        "last_name": lastName,
        "company_domain": companyName,
        "enrich_profile": "enrich",
    }

    response = requests.get(api_endpoint,
                        params=params,
                        headers=headers)
    
    return response.json().get('profile')

def get_meeting_transcript(meeting_id: str) -> str:
    """Gets the transcript of a meeting with a given Zoom meeting ID"""
    print(f"Getting transcript for meeting {meeting_id}")

    zoom_token = get_zoom_token()

    meeting_id = "84625563686"

    headers = {'Authorization': 'Bearer ' + zoom_token}

    response = requests.get(f'https://api.zoom.us/v2/meetings/{meeting_id}/recordings', headers=headers)

    """looks through all recording_files and finds the one with the transcript"""
    recording_files = response.json().get('recording_files')

    for recording_file in recording_files:
        if recording_file.get('file_type') == 'TRANSCRIPT':
            transcript_download_url = recording_file.get('download_url')
            break
    
    print("Transcript download URL:", transcript_download_url)

    response = requests.get(transcript_download_url, headers=headers)

    print("Transcript:", response.text)

    with open('bad_sales_call.txt','r') as file:
        call_transcript = file.read()

    return call_transcript





def update_crm(customer_id: str, customer_full_name: str, customer_company:str, sales_call_score: int, lead_score: int, topics: str) -> str:
    """Updates the CRM with the sales call score and lead score"""
    print(f"Updating CRM for customer {customer_id} with sales call score {sales_call_score}, lead success probability {lead_score}")

    data = [customer_id, customer_full_name, customer_company, sales_call_score, lead_score]

    insert_or_update_customer(*data)

    return f"Updated the CRM for customer {customer_id} with sales call score {sales_call_score}, lead success probability {lead_score}"

def create_onchain_sales_job() -> str:
    """Creates a job on the blockchain for the sales manager to review"""
    print("Creating a job on the blockchain for the sales manager to review")
    job_id = create_job()

    fund_job(job_id)
    
    return f"Created a job with ID {job_id} on the blockchain for the sales manager to review"

def complete_onchain_sales_job(job_id: int, sales_performance_score: int) -> str:
    """Completes the job on the blockchain with the performance score. Pays bonus if performance score is above the threshold and congratulates the sales manager."""
    print(f"Completing job {job_id} on the blockchain")

    complete_job(job_id, sales_performance_score*10)

    release_payment(job_id)

    if sales_performance_score > 7:
        return f"Completed job {job_id} on the blockchain with performance score {sales_performance_score}. Bonus paid to the sales manager."
    else:
        return f"Completed job {job_id} on the blockchain with performance score {sales_performance_score}. No bonus paid to the sales manager."

def get_openai_agent() -> OpenAIAgent:

    linkedin_tool = FunctionTool.from_defaults(fn=search_linkedin)

    meeting_transcript_tool = FunctionTool.from_defaults(fn=get_meeting_transcript)

    crm_update_tool = FunctionTool.from_defaults(fn=update_crm)

    gcal_tools = GoogleCalendarToolSpec().to_tool_list()

    create_onchain_sales_job_tool = FunctionTool.from_defaults(fn=create_onchain_sales_job)

    complete_onchain_sales_job_tool = FunctionTool.from_defaults(fn=complete_onchain_sales_job)

    llm = OpenAI(model="gpt-4-0125-preview")

    agent = OpenAIAgent.from_tools([linkedin_tool, meeting_transcript_tool, gcal_tools[0], crm_update_tool, create_onchain_sales_job_tool, complete_onchain_sales_job_tool], llm=llm, verbose=True, system_prompt="You are sales coach for a company that offers private jet services. You help sales managers to prepare for meetings, analyze their sales calls and provide feedback.")

    return agent