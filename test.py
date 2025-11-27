import aiohttp
import asyncio
import json
from io import BytesIO

# ComfyUI API Configuration
COMFYUI_HOST = "127.0.0.1"
COMFYUI_PORT = 8188
BASE_URL = f"http://{COMFYUI_HOST}:{COMFYUI_PORT}"

async def test_connection():
    """Test if ComfyUI API is accessible"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BASE_URL}/system_stats") as response:
                if response.status == 200:
                    data = await response.json()
                    print("✓ Connected to ComfyUI API")
                    print(f"System Stats: {json.dumps(data, indent=2)}")
                    return True
                else:
                    print(f"✗ Connection failed: Status {response.status}")
                    return False
    except Exception as e:
        print(f"✗ Connection error: {e}")
        return False

async def upload_image(file_path, subfolder="", overwrite=False):
    """Upload an image to ComfyUI"""
    try:
        async with aiohttp.ClientSession() as session:
            # Prepare the file for upload
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            # Create form data
            data = aiohttp.FormData()
            data.add_field('image',
                          file_data,
                          filename=file_path.split('/')[-1],
                          content_type='image/png')
            
            if subfolder:
                data.add_field('subfolder', subfolder)
            if overwrite:
                data.add_field('overwrite', 'true')
            
            # Upload
            url = f"{BASE_URL}/upload/image"
            async with session.post(url, data=data) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"✓ Upload successful: {result}")
                    return result
                else:
                    error = await response.text()
                    print(f"✗ Upload failed: {error}")
                    return None
                    
    except Exception as e:
        print(f"✗ Upload error: {e}")
        return None

async def get_queue():
    """Get current queue status"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BASE_URL}/queue") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"Queue status: {json.dumps(data, indent=2)}")
                    return data
                else:
                    print(f"✗ Failed to get queue: Status {response.status}")
                    return None
    except Exception as e:
        print(f"✗ Queue error: {e}")
        return None

async def get_history(prompt_id=None):
    """Get execution history"""
    try:
        url = f"{BASE_URL}/history"
        if prompt_id:
            url += f"/{prompt_id}"
            
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"History: {json.dumps(data, indent=2)}")
                    return data
                else:
                    print(f"✗ Failed to get history: Status {response.status}")
                    return None
    except Exception as e:
        print(f"✗ History error: {e}")
        return None

async def prompt_workflow(workflow_json):
    """Submit a workflow for execution"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{BASE_URL}/prompt",
                json={"prompt": workflow_json}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"✓ Workflow queued: {result}")
                    return result
                else:
                    error = await response.text()
                    print(f"✗ Workflow failed: {error}")
                    return None
    except Exception as e:
        print(f"✗ Workflow error: {e}")
        return None

async def main():
    """Run all tests"""
    print("=" * 50)
    print("Testing ComfyUI API Connection")
    print("=" * 50)
    
    # Test 1: Check connection
    print("\n[1] Testing connection...")
    connected = await test_connection()
    
    if not connected:
        print("\n⚠ Make sure ComfyUI is running on localhost:8188")
        return
    
    # Test 2: Get queue
    print("\n[2] Getting queue status...")
    await get_queue()
    
    # Test 3: Get history
    print("\n[3] Getting history...")
    await get_history()
    
    # Test 4: Upload image (uncomment and provide a valid path)
    # print("\n[4] Uploading image...")
    # await upload_image("path/to/your/image.png")
    
    print("\n" + "=" * 50)
    print("Tests completed!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
