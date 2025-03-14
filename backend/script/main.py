import os
import psycopg2
from transformers import GPTNeoXForCausalLM, GPTNeoXTokenizer
from configparser import ConfigParser

# Load the model and tokenizer
model_name = "EleutherAI/gpt-neox-20b"
tokenizer = GPTNeoXTokenizer.from_pretrained(model_name)
model = GPTNeoXForCausalLM.from_pretrained(model_name)

# Load the fine-tuned model ID (optional)
with open('../models/fine_tuned_model/model_id.txt', 'r') as f:
    fine_tuned_model_id = f.read().strip()

def generate_query(user_input):
    inputs = tokenizer(user_input, return_tensors="pt")
    outputs = model.generate(inputs["input_ids"], max_length=100)
    query = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return query

def config(filename='../config/config.yaml', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')
    return db

def fetch_results(query):
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

# Main function to handle input and output
if __name__ == "__main__":
    user_input = input("Enter your query: ")
    sql_query = generate_query(user_input)
    print(f"Generated SQL Query: {sql_query}")
    results = fetch_results(sql_query)
    print("Results:")
    for row in results:
        print(row)
