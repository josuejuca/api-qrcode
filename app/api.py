import io
import qrcode

from fastapi import FastAPI, Query
from starlette.responses import StreamingResponse

app = FastAPI()

@app.get('/')
def index():
    return {"API": "Online"}

@app.get('/qrcode')
def home():
    return {"JUCA Soft": "QR Code API"}

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
