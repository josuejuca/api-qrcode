import io
import qrcode
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()

# Configuração do CORS para permitir solicitações de todos os domínios
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Isso permite solicitações de todos os domínios
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Permita os métodos que você precisa
    allow_headers=["*"],  # Isso permite todos os cabeçalhos
)

# Template API Docs
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Rota Index 
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("api-qrcode.jinja", {"request": request})

# Rota QR Code 
@app.get('/qrcode')
def home():
    return {"JUCA Soft": "QR Code API"}

# Rota API v1 
@app.get("/qrcode/{texto}")
def QrAPI(texto: str, size: int = Query(default=200, description="Tamanho do QR Code")):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(texto)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((size, size))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


# Rota Padrão (text= , size= )
@app.get("/data")
def QRAPI(text: str = Query(..., description="Conteúdo do QR Code"), size: int = Query(default=200, description="Tamanho do QR Code")):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((size, size))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
