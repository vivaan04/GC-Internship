import pandas as pd
from sqlalchemy import create_engine, text
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import time

class Query(BaseModel):
    query: str
    
class Update(BaseModel):
    company_name: str
    esg_link: str
    annual_report_link: str
    
class Prompt(BaseModel):
    prompt: str

app = FastAPI()

@app.post("/chat")

def chat(data: Prompt):
    start = time.time()
    OPENAI_API_KEY = 'OPENAI_API_KEY'
    client = OpenAI(api_key=OPENAI_API_KEY)
    assistant_id = 'asst_ROQk4qiwULbASTuEO52Rvfum'
    print("Starting a new conversation...")
    thread = client.beta.threads.create()
    print(f"New thread created with ID: {thread.id}")
    thread_id = thread.id
    # logging.info("User Input: %s",user_input)
    # print(f"User: {user_input}")
    # Add the user's message to the thread
    client.beta.threads.messages.create(thread_id=thread_id,
                                        role="user",
                                        content=data.prompt)

    # Run the Assistant
    run = client.beta.threads.runs.create(thread_id=thread_id,
                                            assistant_id=assistant_id)
    # logging.info("Ran the Assistant")
    # Check if the Run requires action (function call)
    while True:
        # logging.info("While Loop")
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id,
                                            run_id=run.id)
        print(f"Run status: {run_status.status}")
        if run_status.status == 'completed':
            # Retrieve and return the latest message from the assistant
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            response = messages.data[0].content[0].text.value

            print(f"Assistant response: {response}")
            break
        else:
            # logging.info("Sleep 5 seconds")
            time.sleep(5)  # Wait for a second before checking again
        
    p_time = time.time() - start
    print(f"Time take in seconds: {(p_time/60):.2f}s")
    output=f"User Query: {data.prompt}\n\nAssistant Response: {response}"
    return {"data": response, "status": "success"}

@app.post("/execute-query")
def execute_query(query: Query):
    if query.query.lower().startswith("select"):
        connection = create_engine("mysql+pymysql://root:@localhost/esgroadmap")
        conn = connection.connect()
        output = pd.read_sql_query(query.query, connection)
        conn.close()
        return {"data": output, "status": "success"}
    else:  
        return {"data": "Query must start with SELECT", "status": "error"}

@app.put("/update")  
def update(data: Update):
    try:
        connection = create_engine("mysql+pymysql://root:@localhost/esgroadmap")
        conn = connection.connect()
        if(data.annual_report_link == ""):
            query = text("""
            UPDATE `company_universe` 
            SET `Company sustainability / ESG reports page URL`=:esg_link 
            WHERE `Company`=:company_name
            """)
            params = { 
                'esg_link': data.esg_link, 
                'company_name': data.company_name
             }
        elif(data.esg_link == ""):
            query = text("""
            UPDATE `company_universe` 
            SET `Company annual reports page URL`=:annual_report_link
            WHERE `Company`=:company_name
            """)
            params = { 
                'annual_report_link': data.annual_report_link, 
                'company_name': data.company_name
             }
        else:
            query = text("""
            UPDATE `company_universe` 
            SET `Company annual reports page URL`=:annual_report_link, 
                `Company sustainability / ESG reports page URL`=:esg_link 
            WHERE `Company`=:company_name
            """)
            # Pass parameters as a dictionary
            params = {
                'annual_report_link': data.annual_report_link, 
                'esg_link': data.esg_link, 
                'company_name': data.company_name
            }
            
        conn.execute(query, params)
        conn.commit()
        conn.close()
        return {"data": "Data updated successfully", "status": "success"}
    except Exception as e:
        return {"data": str(e), "status": "error"}
