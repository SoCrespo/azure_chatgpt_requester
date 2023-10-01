# encoding = utf-8

import json
import logging
import time

import requests

logging.basicConfig(level=logging.INFO)


class AzureChatGPTRequester:
    """
    Requester class for the Azure GPT model.
    """

    def __init__(
        self,
        api_uri: str,
        api_key: str,
        api_version: str,
        deployment_name: str,
        assistant_message: str = '',
        temperature: float = 0.1,
        timeout_connect=10,
        timeout_read=60,
        initial_sleep_time=10,
        max_retries=3,
        token_limit=4_096,
              ):
        """
        Initialize the class with the following parameters:
        - api_uri: base uri of the GPT model in Azure. Example: "https://my-open-ai-service.openai.azure.com/' 
        - api_key: key to access the GPT model.
        - api_version: version of the GPT model.
        - deployment_name: name of the deployment of the GPT model on Azure.
        - assistant_message: optional prompt to GPT model to orientate the conversation tone.
        - temperature: temperature parameter of the GPT model. Between 0 and 1. The lower the temperature, the more conservative the GPT model.
        - timeout_connect: timeout in seconds to reach the GPT model.
        - timeout_read: timeout in seconds to read the response from the GPT model.
        - initial_sleep_time: initial sleep time in seconds before retrying to reach the GPT model.
        - max_retries: maximum number of retries to reach the GPT model. On each retry, sleep during
        - self.initial_sleep_time seconds * retry number.
        - token_limit: maximum number of tokens to send to the GPT model. The GPT 3.5 standard model has a limit of 4_096 tokens.

        """
        self.api_uri = api_uri
        self.api_key = api_key
        self.api_version = api_version
        self.deployment_name = deployment_name
        self.assistant_message = assistant_message
        self.temperature = temperature
        self.timeout = (timeout_connect, timeout_read)
        self.initial_sleep_time = initial_sleep_time
        self.max_retries = max_retries
        self.url = f"{self.api_uri}/openai/deployments/{self.deployment_name}/chat/completions?api-version={self.api_version}"
        self.headers = {"Content-Type": "application/json", "api-key": self.api_key}
        logging.info(f"Requester is ready.")


    def _get_response(self, text: str) -> requests.Response:
        """
        Request the GPT model with a text. Return requests.Response object.
        Retry strategy on timeout: self.max_retries times, with an initial sleep time of self.initial_sleep_time seconds.
        On each retry, sleep time equals by self.initial_sleep_time seconds * retry number.
        In case of errors where API cannot be reched (status code >= 400), retry with a random sleep time between 0
        and self.initial_sleep_time seconds * retry number.

        """
        messages = [
                {"role": "user", "content": f"{text}"},
            ]
        if self.assistant_message:
            messages.insert(0, {"role": "system", "content": self.assistant_message})


        data = {
            "messages": messages,
            "temperature": self.temperature,
        }

        retries = 0
        while retries <= self.max_retries:
            try:
                response = requests.post(
                    self.url,
                    headers=self.headers,
                    data=json.dumps(data),
                    timeout=self.timeout,
                )
                response.raise_for_status()  # Raise an exception if there's an HTTP error
                return response
            except requests.exceptions.RequestException as e:
                if retries == self.max_retries:
                    raise Exception(
                        f"{e} error. Max retries ({self.max_retries}) reached."
                    )
                else:
                    retries += 1
                    sleep_time = retries * self.initial_sleep_time
                    logging.info(
                        f"{e} error, sleeping for {sleep_time} seconds and retrying."
                    )
                    time.sleep(sleep_time)
                    continue
        return response

    def just_request(self, text: str) -> requests.Response:
        """Straighforward request to the GPT model, no retry strategy on timeout. Return requests.Response object."""
        data = {
            "messages": [
                {"role": "system", "content": "You are a concise assistant."},
                {"role": "user", "content": f"{text}"},
            ],
            "temperature": self.temperature,
        }
        response = requests.post(
            self.url, headers=self.headers, data=json.dumps(data), timeout=self.timeout
        )
        return response

    def ask(self, text: str) -> str:
        """
        Request the GPT model with a text. Return string.
        Retry strategy on timeout: self.max_retries times, with an initial sleep time of self.initial_sleep_time seconds.
        On each retry, sleep time equals by self.initial_sleep_time seconds * retry number.
        """
        response = self._get_response(text)

        try:
            result = response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            result = f"----- Error code {response.status_code} - {e} on request: {response.text}"
        return result
