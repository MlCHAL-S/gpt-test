import requests
import json  # Import the correct JSON module

while True:
    message: str = input('>>> ')
    # Open a streaming POST request
    with requests.post(
            'http://michal-pc:11434/api/chat',
            json={
                "model": "llama2",
                "messages": [
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                "stream": True
            },
            stream=True  # Enable streaming in requests
    ) as response:
        # Ensure the response was successful
        response.raise_for_status()

        # Read and print each chunk as it arrives
        for chunk in response.iter_lines(decode_unicode=True):
            if chunk:  # Avoid blank lines
                # Parse the JSON chunk using the built-in json module
                data = json.loads(chunk)
                print(data['message']['content'], end='', flush=True)
        print()  # Add a newline after the message is complete
