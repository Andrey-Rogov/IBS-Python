from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()
# app.mount("/templates", StaticFiles(directory="templates"), name="templates")
templates = Jinja2Templates(directory="templates")


@app.post("/int_to_roman/{number}", response_model=str)
def int_to_roman(number: int):
    vals = {'M': 1000, 'CM': 900, 'D': 500, 'CD': 400, 'C': 100, 'XC': 90,
            'L': 50, 'XL': 40, 'X': 10, 'IX': 9, 'V': 5, 'IV': 4, 'I': 1}
    curr = ""
    for val in vals:
        while number - vals[val] >= 0:
            curr += val
            number -= vals[val]
    return curr


@app.get("/")
async def read_item(request: Request):
    return templates.TemplateResponse("item.html",
                                      {'request': request})
