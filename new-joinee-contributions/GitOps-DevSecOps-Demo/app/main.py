from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>GitOps DevSecOps Demo</title>
        </head>
        <body>
            <h1>Welcome to GitOps & DevSecOps Demo</h1>
            <p>Application is running successfully 🚀</p>
        </body>
    </html>
    """
