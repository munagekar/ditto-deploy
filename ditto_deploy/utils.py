from typing import Any, Optional

DITTO_DEPLOY_KEY = "ditto-deploy"
METADATA_KEY = "metadata"
ANNOTATIONS_KEY = "annotations"


def read_annotation_from_deployment(d: dict[str, Any]) -> Optional[str]:
    if METADATA_KEY not in d:
        return None
    metadata = d[METADATA_KEY]

    if ANNOTATIONS_KEY not in d:
        return None
    annotations: dict = metadata[ANNOTATIONS_KEY]

    if DITTO_DEPLOY_KEY not in d:
        return None
    return annotations[DITTO_DEPLOY_KEY]


def create_response(uid: str) -> dict[str, Any]:
    resp = {
        "apiVersion": "admission.k8s.io/v1",
        "kind": "AdmissionReview",
        "response": {
            "allowed": True,
            "uid": uid,
        },
    }
    return resp
