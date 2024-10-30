import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, chat, question):
        prompt_email = PromptTemplate.from_template(
    f"""
    ### WhatsApp Group Chat Messages:
    {chat}

    ### INSTRUCTION:
    YOu have given the WhatsApp group chat messages above and provide a short answer to the following question: "{question}".

    Each message includes the date it was sent, the sender's name, and the content of the message. 

    Your response should be a simple detailed answer with emojis if needed attach the date and sarcasm.

    Answer: 
    """
)


        print(prompt_email)
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"chat": str(chat), "question": question})
        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))