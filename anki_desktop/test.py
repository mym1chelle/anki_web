import aiohttp
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.post(
                'http://127.0.0.1:8000/cards/',
                json={"question": "mz", "question_type": 0, "answer": "string", "answer_type": 0, "style": 0, "deck_id": 0},
                headers={
                    'Authorization': f'Bearer UwJGV8KFJLlFVfbWV4_AYMO3-6pqOw2R9iVD2gN2xTo'
                }
        ) as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            print("Body:", html)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())

# create = requests.post(url="http://127.0.0.1:8000/cards/", json=True,
#                        data='{"question": "mz", "question_type": 0, "answer": "string", "answer_type": 0, "style": 0, "deck_id": 0}',
#                        headers={
#                            'Authorization': f'Bearer Tn7bbTlA2ieP03Ttg9pHcWaEw4phkSiM5cOWlMTcPfo'
#                        }
#                        )
#
# print(create.text)


# подключение к Fast API