import time
from typing import Any, Dict

import requests

from config.instagram import (
    INSTAGRAM_ACCESS_TOKEN,
    INSTAGRAM_API_VERSION,
    INSTAGRAM_IG_USER_ID,
)
from config.facebook import FACEBOOK_PAGE_ACCESS_TOKEN, FACEBOOK_PAGE_ID

GRAPH_BASE_URL = f"https://graph.facebook.com/{INSTAGRAM_API_VERSION}"


class InstagramPublishError(Exception):
    """Controlled error for Instagram publish flow."""


def _parse_response(response: requests.Response) -> Dict[str, Any]:
    try:
        data = response.json()
    except ValueError:
        data = {}

    if response.status_code >= 400:
        if isinstance(data, dict) and "error" in data:
            message = data["error"].get("message", str(data["error"]))
            raise InstagramPublishError(message)
        raise InstagramPublishError(response.text or "Instagram request failed")

    if isinstance(data, dict) and "error" in data:
        message = data["error"].get("message", str(data["error"]))
        raise InstagramPublishError(message)

    if not isinstance(data, dict):
        raise InstagramPublishError("Unexpected Instagram response format")

    return data


def _wait_until_container_is_ready(creation_id: str, access_token: str) -> None:
    url = f"{GRAPH_BASE_URL}/{creation_id}"
    deadline = time.time() + 45

    while time.time() < deadline:
        response = requests.get(
            url,
            params={
                "fields": "status_code,status,error_message",
                "access_token": access_token,
            },
            timeout=30,
        )
        data = _parse_response(response)
        status_code = (data.get("status_code") or "").upper()

        if status_code in {"FINISHED", "PUBLISHED"}:
            return
        if status_code in {"ERROR", "EXPIRED"}:
            raise InstagramPublishError(
                data.get("error_message")
                or f"Container is not publishable (status={status_code})"
            )

        time.sleep(2)

    raise InstagramPublishError("Timeout while waiting for media container readiness")


def _resolve_access_token() -> str:
    access_token = INSTAGRAM_ACCESS_TOKEN or FACEBOOK_PAGE_ACCESS_TOKEN
    if not access_token:
        raise InstagramPublishError(
            "Configure INSTAGRAM_ACCESS_TOKEN or FACEBOOK_PAGE_ACCESS_TEST"
        )
    return access_token


def _resolve_ig_user_id(access_token: str) -> str:
    if INSTAGRAM_IG_USER_ID:
        return INSTAGRAM_IG_USER_ID

    if not FACEBOOK_PAGE_ID:
        raise InstagramPublishError(
            "Configure INSTAGRAM_IG_USER_ID or FACEBOOK_PAGE_ID_TEST"
        )

    response = requests.get(
        f"{GRAPH_BASE_URL}/{FACEBOOK_PAGE_ID}",
        params={
            "fields": "instagram_business_account",
            "access_token": access_token,
        },
        timeout=30,
    )
    data = _parse_response(response)
    ig_user = data.get("instagram_business_account") or {}
    ig_user_id = ig_user.get("id")

    if not ig_user_id:
        raise InstagramPublishError(
            "No linked Instagram professional account found for FACEBOOK_PAGE_ID_TEST"
        )

    return ig_user_id


def publish_to_instagram(caption: str, image_url: str) -> str:
    if not image_url:
        raise InstagramPublishError(
            "Instagram publishing requires an image URL hosted on a public server"
        )

    access_token = _resolve_access_token()
    ig_user_id = _resolve_ig_user_id(access_token=access_token)

    create_container_url = f"{GRAPH_BASE_URL}/{ig_user_id}/media"
    create_payload = {
        "image_url": image_url,
        "caption": caption,
        "access_token": access_token,
    }

    create_response = requests.post(create_container_url, data=create_payload, timeout=30)
    create_data = _parse_response(create_response)
    creation_id = create_data.get("id")

    if not creation_id:
        raise InstagramPublishError("Instagram did not return a media container ID")

    _wait_until_container_is_ready(creation_id=creation_id, access_token=access_token)

    publish_url = f"{GRAPH_BASE_URL}/{ig_user_id}/media_publish"
    publish_payload = {
        "creation_id": creation_id,
        "access_token": access_token,
    }

    publish_response = requests.post(publish_url, data=publish_payload, timeout=30)
    publish_data = _parse_response(publish_response)
    media_id = publish_data.get("id")

    if not media_id:
        raise InstagramPublishError("Instagram did not return a published media ID")

    return media_id
