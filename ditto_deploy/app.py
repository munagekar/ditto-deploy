import http
import logging
import time

from fastapi import FastAPI, Request

app = FastAPI()
logger = logging.getLogger()


@app.post("/mutate/deployment")
async def mutate(request: Request):
    logger.debug("Got a Request")

    json_request = await request.json()
    admission_request = json_request["request"]
    print(admission_request)

    start_time = time.time()
    resp = {
        "apiVersion": "admission.k8s.io/v1",
        "kind": "AdmissionReview",
        "response": {
            "allowed": True,
            "uid": admission_request["uid"],
        },
    }
    end_time = time.time()
    time_ms = int((end_time - start_time) * 1000)
    logger.info("Returned Response in %s ms", time_ms)
    return resp


@app.get("/health", status_code=http.HTTPStatus.NO_CONTENT)
async def health():
    logger.debug("Got Health Request")
    return ""
