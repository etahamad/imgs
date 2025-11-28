"""
Test script to directly call ComfyUI API with extra_data authentication
"""
import json
import requests
import uuid

# ComfyUI server URL
SERVER_URL = "http://127.0.0.1:8188"

# Your API key (replace with actual key)
API_KEY = ""

# Simple workflow with GeminiImage2Node
workflow = {
    "1": {
        "inputs": {
            "prompt": "A beautiful sunset over mountains",
            "model": "gemini-pro-latest",
            "seed": 12345,
            "aspect_ratio": "16:9",
            "resolution": "2K",
            "response_modalities": "IMAGE+TEXT"
        },
        "class_type": "GeminiImage2Node",
        "_meta": {
            "title": "Nano Banana Pro (Google Gemini Image)"
        }
    },
    "2": {
        "inputs": {
            "filename_prefix": "ComfyUI",
            "images": [
                "1",
                0
            ]
        },
        "class_type": "SaveImage",
        "_meta": {
            "title": "Save Image"
        }
    }
}

# Create payload with extra_data
client_id = str(uuid.uuid4())
payload = {
    "prompt": workflow,
    "client_id": client_id,
    "extra_data": {
        "api_key_comfy_org": API_KEY
    }
}

print("=" * 60)
print("Testing ComfyUI API with extra_data authentication")
print("=" * 60)
print(f"\nServer URL: {SERVER_URL}")
print(f"Client ID: {client_id}")
print(f"API Key: {API_KEY[:20]}...")
print(f"\nPayload structure:")
print(json.dumps({
    "prompt": "<workflow>",
    "client_id": client_id,
    "extra_data": {
        "api_key_comfy_org": API_KEY[:20] + "..."
    }
}, indent=2))

print("\n" + "=" * 60)
print("Sending request to /prompt endpoint...")
print("=" * 60)

try:
    response = requests.post(
        f"{SERVER_URL}/prompt",
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✓ Success! Response:")
        print(json.dumps(result, indent=2))
        
        if "prompt_id" in result:
            prompt_id = result["prompt_id"]
            print(f"\n✓ Prompt ID: {prompt_id}")
            print(f"\nYou can check the execution status by monitoring the websocket")
            print(f"or by checking: {SERVER_URL}/history/{prompt_id}")
    else:
        print(f"\n✗ Error! Response:")
        try:
            error_data = response.json()
            print(json.dumps(error_data, indent=2))
        except:
            print(response.text)
            
except requests.exceptions.RequestException as e:
    print(f"\n✗ Request failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Test completed")
print("=" * 60)

