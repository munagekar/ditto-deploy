import http
import json
import logging
import time

from fastapi import FastAPI, HTTPException, Request

app = FastAPI()
logger = logging.getLogger()

OLD_OBJECT_KEY = "oldObject"
OBJECT_KEY = "object"


@app.post("/mutate/deployment")
async def mutate(request: Request):
    logger.debug("Got a Request")

    json_request = await request.json()
    admission_request = json_request["request"]

    if OLD_OBJECT_KEY not in admission_request or OBJECT_KEY not in admission_request:
        raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail="Not a Update Request")

    old_object: dict = admission_request[OLD_OBJECT_KEY]
    new_object: dict = admission_request[OBJECT_KEY]

    logger.info("Old Object:\n%s", json.dumps(old_object))
    logger.info("New Object:\n%s", json.dumps(new_object))

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
