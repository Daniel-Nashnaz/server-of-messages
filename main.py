import multiprocessing
import time

from fastapi import FastAPI

from send_messages import start_check_if_there_message_to_send

app = FastAPI()


def start_sends():
    while True:
        start_check_if_there_message_to_send()
        time.sleep(5)


p = multiprocessing.Process(target=start_sends)


@app.get("/start")
async def start():
    p.start()


@app.get("/end")
async def end():
    p.terminate()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8080, reload=True)
