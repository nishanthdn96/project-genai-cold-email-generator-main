import pandas as pd
import chromadb
import uuid


class WhatsAppChat:
    def __init__(self, file_path="./app/resource/output.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="context_db")


    import uuid

    def load_portfolio(self):
        print(self.collection.count())
        if not self.collection.count():
            count = 0
            total_messages = len(self.data)

            # Iterate over each message in the data
            for idx, row in self.data.iterrows():
                # Get the previous 4 messages
                pre_context = ""
                if idx > 0:
                    pre_context = " ".join(
                        f"Timestamp: {self.data.iloc[i]['Timestamp']}, Sender: {self.data.iloc[i]['Sender']}, Message: {str(self.data.iloc[i]['Message'])}"
                        for i in range(max(0, idx - 4), idx)
                    )

                # Get the next 4 messages
                post_context = ""
                if idx < total_messages - 1:
                    post_context = " ".join(
                        f"Timestamp: {self.data.iloc[i]['Timestamp']}, Sender: {self.data.iloc[i]['Sender']}, Message: {str(self.data.iloc[i]['Message'])}"
                        for i in range(idx + 1, min(total_messages, idx + 5))
                    )

                # Combine current message with context
                current_message = f"Timestamp: {row['Timestamp']}, Sender: {row['Sender']}, Message: {str(row['Message'])}"
                document = f"{pre_context} {current_message} {post_context}"

                # Add the document with a unique ID
                self.collection.add(documents=document, ids=[str(uuid.uuid4())])
                count += 1
                print(f"{count} records inserted")


    def query_links(self, question):
        res = self.collection.query(query_texts=question, n_results=5)
        return res.get("documents", [])[0]
