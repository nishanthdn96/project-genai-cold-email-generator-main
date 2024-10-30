import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from whatsappchat import WhatsAppChat

from chains import Chain
# from whatsappchat import Portfolio
from utils import clean_text


def create_streamlit_app( wchat, llm):
    st.title("📧 Whatsapp GPT.")
    url_input = st.text_input("Enter your question:", value="")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            # loader = WebBaseLoader([url_input])
            # data = clean_text(loader.load().pop().page_content)
            # portfolio.load_portfolio()
            wchat.load_portfolio()
            messages = wchat.query_links(url_input)
# print(messages)
            output = llm.write_mail(messages, url_input)

            # jobs = llm.extract_jobs(data)
            # for job in jobs:
            #     skills = job.get('skills', [])
            #     links = portfolio.query_links(skills)
            #     email = llm.write_mail(job, links)
            st.code(output, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    wchat = WhatsAppChat()
    chain = Chain()
    # portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Enjoy pandago group chat", page_icon="📧")
    create_streamlit_app(wchat, chain)


