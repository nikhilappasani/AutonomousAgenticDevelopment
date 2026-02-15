"""
LLM Tools
Wrappers for Azure OpenAI interactions
"""
import os
import logging
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

logger = logging.getLogger(__name__)

def get_llm():
    """Get configured Azure OpenAI client"""
    return AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        temperature=0,
    )

async def generate_plan(story_title: str, description: str, criteria: list, context: str) -> str:
    """Generate implementation plan using LLM"""
    llm = get_llm()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Senior Software Architect. Create a detailed technical implementation plan."),
        ("user", """
        STORY: {title}
        DESCRIPTION: {description}
        CRITERIA: {criteria}
        
        EXISTING CONTEXT:
        {context}
        
        Output a step-by-step implementation plan:
        """)
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    logger.info(f"🧠 Generating plan for: {story_title}")
    return await chain.ainvoke({
        "title": story_title,
        "description": description,
        "criteria": "\n- ".join(criteria),
        "context": context
    })

async def generate_code_implementation(story_title: str, implementation_plan: str) -> str:
    """Generate Python code based on the plan"""
    llm = get_llm()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Python Developer. Write clean, production-ready code."),
        ("user", """
        Implement the following feature based on the plan.
        
        FEATURE: {title}
        
        PLAN:
        {plan}
        
        REQUIREMENTS:
        - Return ONLY the Python code.
        - Include proper docstrings and type hints.
        - No markdown formatting (like ```python). Just the raw code.
        """)
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    logger.info(f"💻 Generating code for: {story_title}")
    return await chain.ainvoke({
        "title": story_title,
        "plan": implementation_plan
    })
