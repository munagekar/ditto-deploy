from typing import Any, Optional

DITTO_DEPLOY_KEY = "ditto-deploy"
METADATA_KEY = "metadata"
ANNOTATIONS_KEY = "annotations"

REPLICAS_ANNOTATION = "replicas"


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


def is_valid_annotated_resource(ar: str) -> bool:
    """
    Checks if the input string is a valid-annotated resource
      Must either be equal to "replicas" or container_name.requests|limits.resource_name
    Args:
        ar: annotated resource

    Returns:
        True if the input string is a valid-annotated resource else False
    """

    ar = ar.strip()
    if ar == REPLICAS_ANNOTATION:
        return True

    try:
        container_name, request_or_limit, resource = ar.split(".", 2)
    except ValueError:
        return False

    if request_or_limit not in ["requests", "limits", "*"]:
        return False

    return True


def is_valid_annotated_value(av: str) -> bool:
    return all(is_valid_annotated_resource(ar) for ar in av.split(","))


def create_response(
    uid: str, allowed: bool = True, code: Optional[int] = None, message: Optional[str] = None
) -> dict[str, Any]:
    """
    Create a AddmissionReview Response

    Args:
        message:

        uid: unique identifier for Admission request
        allowed: True if the admission is allowed else false
        code: HTTP Response Code, ignored if allowed is True
        message: Error message if any to be returned, ignored if allowed is True

    Returns:
        AdmissionReview Response

    References:
        https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/#response
    """
    resp: dict = {
        "apiVersion": "admission.k8s.io/v1",
        "kind": "AdmissionReview",
        "response": {
            "allowed": allowed,
            "uid": uid,
        },
    }

    if allowed is True:
        return resp

    status: dict = {}
    if code is not None or message is not None:
        resp["response"]["status"] = status

        if code is not None:
            status["code"] = code

        if message is not None:
            status["message"] = message

    return resp


def process_annotated_resource(ar):
    if ar != REPLICAS_ANNOTATION:
        raise NotImplementedError(f"Annotation={ar} not supported")
