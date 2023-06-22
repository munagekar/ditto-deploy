import base64
import http
import json
import jsonpatch  # type: ignore
import logging
import time
import copy

from fastapi import FastAPI, HTTPException, Request

from ditto_deploy.utils import create_response, is_valid_annotated_value, process_annotation_from_deployment, \
    process_annotated_value

app = FastAPI()

# Setup Logging with Uvicorn Settings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
uvicorn_access_logger = logging.getLogger("uvicorn.access")
log_level = uvicorn_access_logger.level
logger.setLevel(log_level)
logger.info("Application Logging Level: %s", log_level)

OLD_OBJECT_KEY = "oldObject"
OBJECT_KEY = "object"
UID_KEY = "uid"


@app.post("/mutate/deployment")
async def mutate(request: Request):
    logger.debug("Got a Request")
    json_request = await request.json()
    admission_request = json_request["request"]

    if UID_KEY not in admission_request:
        raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail="No UID in admission request")

    uid = admission_request["uid"]

    if OLD_OBJECT_KEY not in admission_request or OBJECT_KEY not in admission_request:
        raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail="Not a Update Request")

    old_object: dict = admission_request[OLD_OBJECT_KEY]
    new_object: dict = admission_request[OBJECT_KEY]
    new_object_master: dict = copy.deepcopy(new_object)

    logger.info("Old Object:\n%s", json.dumps(old_object, indent=2))
    logger.info("New Object:\n%s", json.dumps(new_object, indent=2))

    ditto_deploy_annotation = process_annotation_from_deployment(new_object)
    if ditto_deploy_annotation is None:
        logger.info("Skip: Ditto-Deploy patch not required")
        return create_response(uid)

    if not is_valid_annotated_value(ditto_deploy_annotation):
        logger.info("Denied: Invalid Annotation")
        return create_response(
            uid, allowed=False, code=http.HTTPStatus.UNPROCESSABLE_ENTITY, message="Invalid Annotation"
        )

    process_annotated_value(ditto_deploy_annotation, new_object, old_object)

    patch = jsonpatch.JsonPatch.from_diff(new_object_master, new_object)
    patch = base64.b64encode(str(patch).encode()).decode()

    logger.info("patch: %s", patch)

    start_time = time.time()
    resp = create_response(uid, json_patch=patch)
    end_time = time.time()
    time_ms = int((end_time - start_time) * 1000)
    logger.info("Returned Response in %s ms", time_ms)
    return resp


@app.get("/health", status_code=http.HTTPStatus.NO_CONTENT)
async def health():
    logger.debug("Got Health Request")
    return ""
