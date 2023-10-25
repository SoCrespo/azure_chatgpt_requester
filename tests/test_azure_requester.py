import pytest
import requests
from time import time
from unittest.mock import patch, Mock

from ..src.chatgpt_requester.azure import Requester

json_content_OK = {"choices": [{"message": {"content": "Response text"}}]}
json_content_too_many_tokens = {"error": {
    "message": "This model's maximum context length is 8192 tokens. However, your messages resulted in 10083 tokens. Please reduce the length of the messages.",
    "type": "invalid_request_error",
    "param": "messages",
    "code": "context_length_exceeded"
    }
}
json_content_other_error = {"error": "Bad Request"}

timeout_connect=1
timeout_read=3
initial_sleep_time=0.1
max_retries = 2

# Helper function to create an Requester instance for testing
def create_requester():
    return Requester(
        api_uri="your_api_uri",
        api_key="your_api_key",
        api_version="your_api_version",
        api_deployment_name="your_api_deployment_name",
        assistant_message="optional_message",
        timeout_connect=timeout_connect,
        timeout_read=timeout_read,
        initial_sleep_time=initial_sleep_time,
        max_retries=max_retries,
    )

# Test initialization
def test_init():
    requester = create_requester()
    assert requester is not None

def test_init_missing_required_parameters():
    with pytest.raises(TypeError):
        Requester(
            api_uri="your_api_uri",
            api_key="your_api_key",
            api_version="your_api_version",
        )

def test_init_default_values():
    requester = Requester(
        api_uri="your_api_uri",
        api_key="your_api_key",
        api_version="your_api_version",
        api_deployment_name="your_api_deployment_name",
    )
    assert requester.assistant_message == 'You are a concise assistant.'
    assert requester.temperature == 0.1


@patch("requests.post")
def test_ask_OK_successful_request(mock_post):
    mock_response = Mock(
        status_code=200,
        json=Mock(return_value=json_content_OK)
    )
    mock_post.return_value = mock_response
    requester = create_requester()
    result = requester.ask("Input text")
    assert result == "Response text"


@patch("requests.post")
def test_ask_with_too_many_tokens_raises_ValueError(mock_post):
    mock_response = Mock(
        status_code=400,
        json=Mock(return_value=json_content_too_many_tokens),
        text=str(json_content_too_many_tokens)
    )
    mock_post.return_value = mock_response
    requester = create_requester()
    with pytest.raises(ValueError) as e:
        requester.ask("Input text")

@patch("requests.post")
def test_ask_with_other_error_raises_Exception(mock_post):
    mock_response = Mock(
        status_code=400,
        json=Mock(return_value=json_content_other_error),
    )
    mock_post.return_value = mock_response
    requester = create_requester()
    with pytest.raises(Exception) as e:
        requester.ask("Input text")


@patch("requests.post")
def test_ask_handle_timeout_final_attempt_ok(mock_post):
    final_mock = Mock(status_code=200, json=Mock(return_value=json_content_OK))
    mock_post.side_effect = [requests.exceptions.Timeout] * (max_retries - 1) + [final_mock]
    requester = create_requester()
    result = requester.ask("Input text")
    assert result == "Response text"


@patch("requests.post")
def test_ask_handle_timeout_abort(mock_post):
    mock_post.side_effect = [requests.exceptions.Timeout] * (max_retries + 1)
    requester = create_requester()
    start = time()
    with pytest.raises(TimeoutError):
         requester.ask("Input text")

@patch("requests.post")
def test_ask_does_retry_on_timeout(mock_post):
    mock_post.side_effect = [requests.exceptions.Timeout] * (max_retries + 1)
    requester = create_requester()
    start = time()
    with pytest.raises(TimeoutError):
        requester.ask("Input text")
    end = time()
    elapsed = end - start
    expected_duration = max_retries * initial_sleep_time
    assert elapsed >= expected_duration



