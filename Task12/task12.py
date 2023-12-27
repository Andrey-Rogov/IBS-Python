from collections import Counter
import pandas as pd
from numpy import NaN
from io import BytesIO
from fastapi import FastAPI, HTTPException, UploadFile, Request
import logging
from logger import logger
import time
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI(title='Practice Tasks 1-2')

# Disabling uvicorn standard logging
uvicorn_error = logging.getLogger("uvicorn.error")
uvicorn_error.disabled = True
uvicorn_lifespan_on_logger = logging.getLogger("uvicorn.lifespan.on")
uvicorn_lifespan_on_logger.disabled = True


class MyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # By default, in logger we can access only few parameters such as filename or log level name
        # So we add extra values in logger and modify Formatter in logger.py with corresponding names
        s = time.time()
        response = await call_next(request)
        logger.info('Custom logs', extra={"exec_time": time.time() - s,
                                          "http_method": request.method,
                                          'url': request.url.path,
                                          'status_code': response.status_code,
                                          })
        return response


app.add_middleware(MyMiddleware)


@app.post("/average_age_by_position")
def average_age_by_position(file: UploadFile):
    """
    :param file: Data file.

    :return: Average age for each position in given data
    """
    contents = file.file.read()
    buffer = BytesIO(contents)
    employees_data = pd.read_csv(buffer)
    buffer.close()
    file.file.close()
    if not set(employees_data.columns) >= {'Имя', 'Возраст', 'Должность'}:
        raise HTTPException(status_code=400, detail='Missing or wrong column names')
    try:
        pos_age = {pos: employees_data.loc[employees_data['Должность'] == pos]['Возраст'].mean()
                   for pos in employees_data['Должность'].unique()}
        # Because /core/json_encoder.py does not allow NaN values, we have to change it to None
        for pos in pos_age:
            pos_age[pos] = None if (pos_age[pos]) is NaN else pos_age[pos]
    except Exception as err:
        raise HTTPException(status_code=400, detail=err)
    return pos_age


@app.post("/find_in_different_registers")
def find_in_different_registers(words: list[str]):
    """
    :param words: List of words in arbitrary case.

    :return: List of case-unique words.
    """
    unique_counter = Counter(words)
    for word in unique_counter:
        if unique_counter[word] > 1:
            words = [i for i in words if i.lower() != word.lower()]
    return list(set(map(lambda x: x.lower(), words)))
