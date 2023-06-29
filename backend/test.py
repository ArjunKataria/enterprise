import requests

# Set the URL for the chat API endpoint
url = 'http://0.0.0.0:5001/api/chat'

# Set the question you want to ask
question = "Hey my name is arjun"

# Create the request payload
payload = {'question': question}

# Send a POST request to the API endpoint
response = requests.post(url, json=payload)

# Check the response status code
if response.status_code == 200:
    # Extract the answer from the response
    answer = response.json().get('answer')
    print("Answer:", answer)
else:
    # Handle the error case
    print("Error:", response.json().get('error'))
