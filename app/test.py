from whatsappchat import WhatsAppChat
from chains import Chain

user_input = input("Enter question: ")
# user_input = "When is Anil Namilikonda wedding?"

wchat = WhatsAppChat()
wchat.load_portfolio()
llm = Chain()
messages = wchat.query_links(user_input)
# print(messages)
output = llm.write_mail(messages, user_input)

print("-"*50)
print(output)
# messages = llm.get_message(data)
