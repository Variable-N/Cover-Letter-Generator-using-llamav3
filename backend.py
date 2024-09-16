from s_key import api_key
from langchain_groq import ChatGroq
import re
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate

llm = ChatGroq(
    temperature = 0,
    groq_api_key = api_key,
    model_name = "llama-3.1-70b-versatile"
)
def clean_whitespace(text):
        return re.sub(r'[ \t\n]+', lambda m: ' ' if ' ' in m.group() else m.group()[0], text).strip()

def generate_cover_letter(link, pdf):
    file_path = (f"/content/{pdf}")
    pdf_loader = PyPDFLoader(file_path)
    pages = pdf_loader.load_and_split()
    cv_information = ""
    for p in pages:
        cv_information += p.page_content + "\n"
    # print(cv_information)
    loader = WebBaseLoader(link)
    page_data = loader.load().pop().page_content
    # print(page_data)
    
    page_data = clean_whitespace(page_data)
    # print(page_data)


    prompt_extract = PromptTemplate.from_template(
        """
        ### SCRAPED TEXT FROM WEBSITE:
        {page_data}
        ### INSTRUCTION:
        The scraped text is from bdjobs, a website where people can find about job openings.
        Your job is to extract the job posting and return them in text format containing key informations. Make sure they are  separated by using \n.
        Only return the valid informations.
        ### VALID INFOs (NO PREAMBLE)
        """
    )

    chain_extract = prompt_extract | llm
    res = chain_extract.invoke(input = {'page_data': page_data})
    # print(res.content)
    job_description = res.content

    prompt_email = PromptTemplate.from_template(
        """
        ### JOB DESCRIPTION:
        {job_description}

        ### MY CV INFORMATION:
        {cv_information}
        ### Instruction:
        Your Task is to write a cover letter for this specific task. Use JOB DESCRIPTION and MY CV INFORMATION to create a
        perfect cover letter. You do not need to add all the information from CV to Cover letter. Just mention key things that goes
        with the given job description. Try to be concise and do not exceed more than a page.

        Do not provide a preamble.
        ### EMAIL (NO PREAMBLE):
        """
    )

    chain_email = prompt_email | llm
    res = chain_email.invoke({"job_description":str(job_description),'cv_information':cv_information})
    # print(res.content)
    return res.content