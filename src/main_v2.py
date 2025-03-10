import asyncio
import os
from openai import AsyncOpenAI

async def main():
    client = AsyncOpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )

    # model: gpt-4o-mini-realtime-preview-2024-12-17
    # model: gpt-4o-realtime-preview-2024-12-17
    async with client.beta.realtime.connect(model="gpt-4o-realtime-preview") as connection:
        await connection.session.update(session={'modalities': ['text']})

        await connection.conversation.item.create(
            item={
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": "Say hello!"}],
            }
        )
        await connection.response.create()

        async for event in connection:
            if event.type == 'response.text.delta':
                print(event.delta, flush=True, end="")

            elif event.type == 'response.text.done':
                print()

            elif event.type == "response.done":
                break

asyncio.run(main())