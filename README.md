# AzureChatGPT Requester

This is a Python class for making requests to the Azure ChatGPT  model. It allows you to send a prompt and content to the API and get the response as string. 

Warning: as is, this code is stateless: it does not keep track of the conversation history. In other words, each request is independent from the previous ones. If you want to keep track of the conversation history, you need to modify the code to keep track of the previous requests and send them along with the new request.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Configuration](#configuration)
- [Retry Strategy](#retry-strategy)
- [Methods](#methods)
- [Example](#example)
- [License](#license)

## Prerequisites

We recommend using a virtual environment to install the required Python libraries. You can create a virtual environment using `venv`:

```bash
python -m venv venv
```

Before using this code, make sure you have the following:

- Python 3.6 or higher installed.
- Required Python libraries installed. You can install them using `pip`:

    ```bash
    pip install requests
    ```

## Getting Started

1. Clone or download this repository to your local machine.

2. Import the `AzureChatGPTRequester` class into your Python script.

## Usage

The `AzureChatGPTRequester` class allows you to make requests to the Azure GPT model. Here's how you can use it:

```python
# Import the class
from azure_chatgpt_requester import AzureChatGPTRequester

# Create an instance of the requester
requester = AzureChatGPTRequester(
    api_base='YOUR_API_BASE_URL',
    api_key='YOUR_API_KEY',
    api_version='YOUR_API_VERSION',
    deployment_name='YOUR_DEPLOYMENT_NAME',
)

# Ask a question to the GPT model
response = requester.ask("Can you tell me a joke?")
print(response)
```

## Configuration

You need to provide the following configuration parameters when creating an instance of `AzureChatGPTRequester`:

- `api_base`: Base URL of the GPT model in Azure.
- `api_key`: API key to access the GPT model.
- `api_version`: Version of the GPT model.
- `deployment_name`: Name of the deployment of the GPT model on Azure.
- `assistant_message` (optional): An optional prompt to the GPT model to orientate the conversation tone.
- `temperature`: Temperature parameter of the GPT model. It controls the randomness of the generated responses. A lower value makes the responses more conservative.
- `timeout_connect`: Timeout in seconds to reach the GPT model.
- `timeout_read`: Timeout in seconds to read the response from the GPT model.
- `initial_sleep_time`: Initial sleep time in seconds before retrying to reach the GPT model.
- `max_retries`: Maximum number of retries to reach the GPT model in case of timeouts.
- `token_limit`: Maximum number of tokens to send to the GPT model. The GPT 3.5 standard model has a limit of 4,096 tokens.

## Retry Strategy

The `AzureChatGPTRequester` class includes a retry strategy for handling timeouts when reaching the GPT model. It will retry a specified number of times with increasing sleep times between retries. If the maximum number of retries is reached and the GPT model is still unreachable, an exception will be raised.

## Methods

- `just_request(text: str)`: Make a straightforward request to the GPT model without retrying on timeouts. Returns a `requests.Response` object.

- `ask(text: str)`: Make a request to the GPT model with a text and apply the retry strategy on timeouts. Returns the response as a string.

## Example

You can find an example of how to use this code in the [example.py](example.py) file included in this repository.

## License

This code is provided under the [MIT License](LICENSE). You are free to use and modify it for your own purposes.