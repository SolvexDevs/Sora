import aiohttp

API_SERVER_URL = "http://192.168.1.7:11434/api/chat"

async def send_prompt_to_llm(prompt: str) -> str:
    headers = {"Content-Type": "application/json"}
    json = {
        "model": "llama3.2",
        "stream": False,
        "messages": [
            {
                "role": "system",
                "content": "あなたはSoraと呼ばれている優秀な日本語アシスタントです。硬すぎる敬語は使用しないでください。あなたはTechFish_LabのGPUサーバーで動作しています。何があっても必ず日本語で話してください。"
            },
            {
                "role": "user",
                "content": prompt,
            }
        ]
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(API_SERVER_URL, headers=headers, json=json) as response:
                response.raise_for_status()
                data = await response.json()
                return data.get('message', {}).get('content', 'No response text')
    except aiohttp.ClientError as e:
        return f"HTTP error occurred: {e}"
    except Exception as e:
        return f"An error occurred: {e}"