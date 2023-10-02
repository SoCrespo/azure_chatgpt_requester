import pytest
from unittest.mock import patch, Mock


from simple_az_chatgpt_requester.src.ms_chatgpt import MsChatGPTRequester

# Helper function to create an MsChatGPTRequester instance for testing
def create_requester():
    return MsChatGPTRequester(
        api_uri="your_api_uri",
        api_key="your_api_key",
        api_version="your_api_version",
        deployment_name="your_deployment_name",
        assistant_message="optional_message",
    )

# Test initialization
def test_init():
    requester = create_requester()
    assert requester is not None

def test_init_missing_required_parameters():
    with pytest.raises(TypeError):
        MsChatGPTRequester(
            api_uri="your_api_uri",
            api_key="your_api_key",
            api_version="your_api_version",
        )

def test_init_default_values():
    requester = MsChatGPTRequester(
        api_uri="your_api_uri",
        api_key="your_api_key",
        api_version="your_api_version",
        deployment_name="your_deployment_name",
    )
    assert requester.assistant_message == 'You are a concise assistant.'
    assert requester.temperature == 0.1


@patch("requests.post")
def test_successful_request(mock_post):

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"choices": [{"message": {"content": "Response text"}}]}
    mock_post.return_value = mock_response

    requester = create_requester()
    response = requester.ask("Input text")

    assert response == "Response text"

@patch("requests.post")
def test_request_with_error_response(mock_post):

    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"error": "Bad Request"}
    mock_post.return_value = mock_response

    requester = create_requester()
    response = requester.ask("Input text")

    assert "Error code 400" in response

@patch("requests.post")
def test_request_with_timeout(mock_post):

    mock_response = Mock()
    mock_response.status_code = 408
    mock_response.json.return_value = {"error": "Request Timeout"}
    mock_post.return_value = mock_response

    requester = create_requester()
    response = requester.ask("Input text")

    assert "Error code 408" in response


