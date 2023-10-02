# Simple MS Azure ChatGPT Requester

This is a Python class for making requests to the Microsoft Azure ChatGPT model. It allows you to send a prompt and content to the API and get the response as string. 

Warning: as is, this code is stateless: it does not keep track of the conversation history. In other words, each request is independent from the previous ones. 

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

1. Before using this code, make sure you have Python 3.10 or higher installed.

2. We recommend using a virtual environment to install the required Python libraries. You can create a virtual environment using `venv`:

```bash
python -m venv ./.venv
```
Then, activate the virtual environment:

```bash
source ./.venv/bin/activate
```
(may vary according to your operating system and shell)
    
3. Install the library:
```bash
pip install git+https://github.com/SoCrespo/ms_chatgpt_requester.git
```
4. Create an Azure account and subscribe to the [Azure ChatGPT model](https://azure.microsoft.com/en-us/services/cognitive-services/chatbot/). You will need to create a resource group and a resource of type "Cognitive Services". You will also need to create a deployment of the GPT model. You can find more information on how to do this [here](https://learn.microsoft.com/fr-fr/azure/ai-services/openai/how-to/create-resource?pivots=web-portal#create-a-resource). Subscription to this service is submitted to application.

You'll get the following information from your Azure account, which you'll need to use this code:
- API base URL
- API key
- API version
- Deployment name.



## Usage

The `MsChatGPTRequester` class allows you to make requests to the Microsoft Azure GPT model. Here's how you can use it:

```python
# Import the class
from ms_chatgpt import MsChatGPTRequester

# Create an instance of the requester
requester = MsChatGPTRequester(
    api_uri='YOUR_API_URI',
    api_key='YOUR_API_KEY',
    api_version='YOUR_API_VERSION',
    deployment_name='YOUR_DEPLOYMENT_NAME',
)

# Ask a question to the GPT model
response = requester.ask("Can you tell me a joke?")
print(response)
```

## Configuration

You need to provide the following configuration parameters when creating an instance of `MsChatGPTRequester`:

Mandatory:
- `api_uri`: Base URI of the GPT model in Azure.
- `api_key`: API key to access the GPT model.
- `api_version`: Version of the GPT model.
- `deployment_name`: Name of the deployment of the GPT model on Azure.

Optional:
- `assistant_message` (optional): An optional prompt to the GPT model to orientate the conversation tone. Default is "You are a concise assistant".
- `temperature`: Temperature parameter of the GPT model. It controls the randomness of the generated responses. A lower value makes the responses more conservative. Default is 0.1.
- `timeout_connect`: Timeout in seconds to reach the GPT model. Default is 10 seconds.
- `timeout_read`: Timeout in seconds to read the response from the GPT model. Default is 60 seconds.
- `initial_sleep_time`: Initial sleep time in seconds before retrying to reach the GPT model. Default is 10 second.
- `max_retries`: Maximum number of retries to reach the GPT model in case of timeouts. Default is 3.
- `token_limit`: Maximum number of tokens to send to the GPT model. Default is the GPT 3.5 standard model limit of 4,096 tokens.

## Retry Strategy

The `MsChatGPTRequester` class includes a retry strategy for handling timeouts when reaching the GPT model. It will retry a specified number of times with increasing sleep times between retries. If the maximum number of retries is reached and the GPT model is still unreachable, an exception will be raised.

## Methods

- `just_request(text: str)`: Make a straightforward request to the GPT model without retrying on timeouts. Returns a `requests.Response` object.

- `ask(text: str)`: Make a request to the GPT model with a text and apply the retry strategy on timeouts. Returns the response as a string.

## License

This code is provided under the [MIT License](LICENSE). You are free to use and modify it for your own purposes.