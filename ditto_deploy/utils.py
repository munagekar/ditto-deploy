from typing import Any, Optional

DITTO_DEPLOY_KEY = "ditto-deploy"
DITTO_DEPLOY_APPLIED_KEY = "ditto-deploy/applied"
METADATA_KEY = "metadata"
ANNOTATIONS_KEY = "annotations"

REPLICAS_ANNOTATION = "replicas"


def process_annotation_from_deployment(d: dict[str, Any]) -> Optional[str]:
    if METADATA_KEY not in d:
        return None
    metadata = d[METADATA_KEY]

    if ANNOTATIONS_KEY not in metadata:
        return None
    annotations: dict = metadata[ANNOTATIONS_KEY]

    annotations.pop(DITTO_DEPLOY_APPLIED_KEY, None)
    if DITTO_DEPLOY_KEY not in annotations:
        return None

    return annotations.pop(DITTO_DEPLOY_KEY)


def add_applied_annotation_to_deployment(d: dict[str, Any], patch: str) -> None:
    d[METADATA_KEY][ANNOTATIONS_KEY][DITTO_DEPLOY_APPLIED_KEY] = patch


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
        uid: str,
        allowed: bool = True,
        code: Optional[int] = None,
        message: Optional[str] = None,
        json_patch: Optional[str] = None,
) -> dict[str, Any]:
    """
    Create a AddmissionReview Response

    Args:
        message:

        uid: unique identifier for Admission request
        allowed: True if the admission is allowed else false
        code: HTTP Response Code, ignored if allowed is True
        message: Error message if any to be returned, ignored if allowed is True
        json_patch: Json Patch, ignored if allowed in false

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
        if json_patch is not None:
            resp["response"]["patchType"] = "JSONPatch"
            resp["response"]["patch"] = json_patch

        return resp

    status: dict = {}
    if code is not None or message is not None:
        resp["response"]["status"] = status

        if code is not None:
            status["code"] = code

        if message is not None:
            status["message"] = message

    return resp


def process_annotated_resource(ar, dn: dict, do: dict):
    """
    Process Deployment configuration for the given annotated resource

    Args:
        ar: annotated resource
        dn: deployment, modified in-place
        do: deployment, old

    Returns:

    """
    ar = ar.strip()
    if ar != REPLICAS_ANNOTATION:
        raise NotImplementedError(f"Annotation={ar} not supported")

    if ar == REPLICAS_ANNOTATION:
        dn["spec"]["replicas"] = do["spec"]["replicas"]


def process_annotated_value(av: str, dn: dict, do: dict) -> None:
    """
    Processes Deployment Configuration for the given annotated value

    Args:
        av: annotated value
        dn: deployment new, modified in-place
        do: deployment old
    """
    list(process_annotated_resource(ar, dn, do) for ar in av.split(","))
