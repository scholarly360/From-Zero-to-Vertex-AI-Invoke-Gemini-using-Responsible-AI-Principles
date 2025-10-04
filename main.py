""" GCP FastAPI example with Google Gemini AI (with Safety Content Filters) """

import httpx, os, uuid
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from vellox import Vellox
from pydantic import BaseModel
from typing import Optional
from google import genai
from pathlib import Path
from google.genai.types import (
    GenerateContentConfig,
    HarmCategory,
    HarmBlockThreshold,
    HttpOptions,
    SafetySetting,
)

safety_settings = [
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
]

app = FastAPI()
_security = HTTPBearer(auto_error=False)
API_TOKEN = os.getenv("API_TOKEN", "") # set while deploying
client = genai.Client()
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")  # current Vertex default

class SummarizeTextRequest(BaseModel):
    text: Optional[str] = None

def require_token(creds: HTTPAuthorizationCredentials = Depends(_security)):
    if not creds or creds.scheme.lower() != "bearer" or creds.credentials != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token")

""" Simple endpoint """
@app.get("/health", dependencies=[Depends(require_token)])
def health():
    return {"message": "Hello Running (Securely)!"}

""" Simple summarize as Markdown """
@app.post("/summarize", dependencies=[Depends(require_token)])
async def summarize(req: SummarizeTextRequest):
    if not req.text:
        raise HTTPException(400, "Provide 'text'.")
    source = req.text
    prompt = (""" Summarize in one paragraph clearly as markdown \n\n---\n""" + source)
    resp = client.models.generate_content(model=MODEL, contents=prompt,  config=GenerateContentConfig(
        safety_settings=safety_settings,
    ))
    if(resp.text is None):
        return({"summary": resp.candidates[0]}) # type: ignore
    return {"summary": resp.text}


""" Wrap FastAPI (ASGI) so it looks like a Cloud Run function """
vellox = Vellox(app=app, lifespan="off")
""" This is your function entrypoint for GCP """
def handler(request):
    return vellox(request)