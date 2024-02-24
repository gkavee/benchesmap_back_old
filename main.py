import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from benches.router import router as benches_router
from users.router import router as users_router
from auth.router import router as auth_router

app = FastAPI(
    title='Bench app'
)

origins = [
    "http://localhost:8000",
    'http://localhost:5173',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Cookie", "Set-Cookie", "Access-Control-Allow-Credential", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin", "Access-Control-Allow-Methods", "Authorization"],
)


app.include_router(benches_router)
app.include_router(users_router)
app.include_router(auth_router)

sentry_sdk.init(
    dsn="https://cf05c30c2c4add8e4e7c2b4768ca76bf@o4506769756192768.ingest.sentry.io/4506769757503488",
    enable_tracing=True,
    integrations=[
        StarletteIntegration(
            transaction_style="endpoint"
        ),
        FastApiIntegration(
            transaction_style="endpoint"
        ),
    ]
)

@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0