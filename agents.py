from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search,scrape_url 
import os
from dotenv import load_dotenv

load_dotenv()
#model setup
llm=ChatMistralAI(model="mistral-small-2506",temperature=0)
#1st agent 
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )
    
#2nd agent
def build_reader_agent():
        return create_agent(
            model=llm,
            tools=[scrape_url]
        )

#writer chain
writer_prompt=ChatPromptTemplate.from_messages(
    [("system","you are an expert research writer .write clear ,structured and insightful reports."),
    ("human","""write a detailed research report on the topic below.
    Topic:{topic}
    Research_Gathered:{research}
    Structure the report as:
    --Introduction
    --key_findings(minimum 3 well explained points)
    --conclusion 
    --sources(list all urls found in the research)
    be detailed,factual and professional.""" )]
)
writer_chain=writer_prompt |llm | StrOutputParser() 

#critic chain
critic_prompt=ChatPromptTemplate.from_messages([
    ("system","you are a sharp nd constructive research critic.be honest and specific"),
    ("human","""review the research report below and evaluate it strictly
    Report:{report}
    respond in this exact format:
    score:x/10
    
    strengths:
    -...
    -...
    areas to improve:
    -...
    -...
    one line verdict:
    ...
    """)
])
critic_chain=critic_prompt |llm | StrOutputParser() 

