import multiprocessing
import time

from fastapi import FastAPI

from send_messages import start_check_if_there_message_to_send

app = FastAPI()


def start_sends():
    while True:
        start_check_if_there_message_to_send()
        time.sleep(5)


p = None


@app.get("/start")
async def start():
    global p
    if p is None:
        p = multiprocessing.Process(target=start_sends)
        p.start()
        return {"message": "Process started successfully."}
    else:
        return {"message": "Process is already running."}


@app.get("/end")
async def end():
    global p
    if p is not None:
        p.terminate()
        p = None
        return {"message": "Process terminated successfully."}
    else:
        return {"message": "No process is currently running."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
