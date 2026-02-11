from typing import Optional
import requests
from config.facebook import (FACEBOOK_API_VERSION, FACEBOOK_PAGE_ACCESS_TOKEN, FACEBOOK_PAGE_ID)

GRAPH_BASE_URL = f"https://graph.facebook.com/{FACEBOOK_API_VERSION}"

class FacebookPublishError(Exception):
    """Error controlado de Facebook"""
    pass

def publish_to_facebook(message: str, image_url: Optional[str] = None) -> str:
    if not FACEBOOK_PAGE_ACCESS_TOKEN:
        raise FacebookPublishError("FACEBOOK_PAGE_ACCESS_TOKEN is not configured")

    if image_url:
        # Post con image + texto
        url = f"{GRAPH_BASE_URL}/{FACEBOOK_PAGE_ID}/photos"
        payload = {
            "url": image_url,
            "caption": message,
            "published": "true",
            "access_token": FACEBOOK_PAGE_ACCESS_TOKEN
        }
    else:
        # Post solo texto
        url=f"{GRAPH_BASE_URL}/{FACEBOOK_PAGE_ID}/feed"
        payload = {
            "message": message,
            "access_token": FACEBOOK_PAGE_ACCESS_TOKEN
        }

    response = requests.post(url, data=payload)

    if response.status_code != 200:
        raise FacebookPublishError(response.text)

    data = response.json()

    if "error" in data:
        raise FacebookPublishError(data["error"]["message"])

    # Facebook retorna diferentes claves segun el endpoint
    return data.get("post_id") or data.get("id")

def publish_text_post(message):
    url = f"{GRAPH_BASE_URL}/{FACEBOOK_PAGE_ID}/feed"

    payload = {
        "message": message,
        "access_token": FACEBOOK_PAGE_ACCESS_TOKEN
    }

    response = requests.post(url, data=payload)

    if response.status_code != 200:
        raise Exception(f"Facebook error: {response.text}")

    return response.json()

def publish_to_facebook_mock(text, image_url):

    """
    Simulacion de publicación de Facebook"
    No llama a Facebook real.
    """

    print("Mock Facebook post")
    print(f"Texto: {text}")
    print(f"Image: {image_url}")

    # Id que facebook devolveria

    fake_facebook_post_id = "fb_mock_123456"

    return{
        "success":True,
        "facebook_post_id": fake_facebook_post_id
    }
