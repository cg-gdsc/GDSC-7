import asyncio
import datetime as dt
import random
import dotenv
import uvicorn

from async_timeout import timeout
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.submission.create_submission import create_submission
from src.static.ChatBedrockWrapper import TOKEN_COUNTER, get_total_number_of_tokens, get_total_cost, get_token_details

dotenv.load_dotenv()


class Payload(BaseModel):
    prompt: str
    timeout: int = 5*60  # 5 minutes


app = FastAPI()


@app.get("/")
async def health_check():
    return {"message": "Server is running. You may direct queries to api"}


@app.post("/run")
async def run_task(payload: Payload):
    call_id = dt.datetime.now().strftime("%Y%m%d%H%M%S%f") + f'_{random.randint(0, 1_000_000)}'
    TOKEN_COUNTER[call_id] = {}
    try:
        submission = create_submission(call_id=call_id)

        async def run_submission(prompt: str):
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, submission.run, prompt)

        # can raise TimeoutError
        async with timeout(payload.timeout):
            start_time = asyncio.get_event_loop().time()
            result = await run_submission(payload.prompt)
            end_time = asyncio.get_event_loop().time()
            time_diff = end_time - start_time

        return JSONResponse(content={
            "result": result,
            "time": time_diff,
            "timed_out": False,
            'tokens': get_total_number_of_tokens(call_id),
            'cost': get_total_cost(call_id),
            'token_details': get_token_details(call_id)
        })

    except asyncio.TimeoutError as e:
        return JSONResponse(content={
            "result": None,
            "time": None,
            "timed_out": True,
            'tokens': get_total_number_of_tokens(call_id),
            'cost': get_total_cost(call_id),
            'token_details': get_token_details(call_id)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        del TOKEN_COUNTER[call_id]


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
