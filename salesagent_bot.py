import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

import os

from llama_index.agent.openai import OpenAIAgent

from agent import get_openai_agent

from docx import Document

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

agent = get_openai_agent()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = agent.chat("Search the upcoming sales calendar events on March 17th 2024. Format the response for Telegram message, use emoji.")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=str(response), parse_mode="Markdown")

    response = agent.chat("Prepare a memo how to prepare for this private jet services sales call using info about the event participant from their LinkedIn profile. Score this lead's success probability from 1 to 10 based on the LinkedIn profile information and the upcoming sales call event details. List possible topics or questions to discuss/ask to make the sales call successful. Format the response for Telegram message, use emoji.")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=str(response), parse_mode="Markdown")

    response = agent.chat("Analyze the sales call using meeting transcript that is downloaded by zoom meeting id. Score the sales call from 1 to 10. Format response for .docx file, use emoji")
    """Creates a meeting analysis document from agent response in doc format and sends it to the sales manager via Telegram."""
    meeting_analysis_document = str(response)
    
    doc = Document()

    doc.add_heading('Meeting Analysis', 0)
    doc.add_paragraph(meeting_analysis_document)
    doc.save('meeting_analysis.docx')

    with open('meeting_analysis.docx', 'rb') as file:
        await context.bot.send_document(chat_id=update.effective_chat.id, document=file, caption="📋 I've analyzed the sales call. Here's the meeting analysis document.")

    response = agent.chat("Update the CRM with the sales call score. Format the response for Telegram message, use emoji.")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=str(response), parse_mode="Markdown")

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.environ["TELEGRAM_BOT_TOKEN"]).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    application.run_polling()