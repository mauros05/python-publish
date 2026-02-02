import os
from config.facebook import (FACEBOOK_API_VERSION, FACEBOOK_PAGE_ACCESS_TOKEN, FACEBOOK_PAGE_ID)

GRAPH_BASE_URL = f"https://graph.facebook.com/{FACEBOOK_API_VERSION}"

def pubish_to_facebook(message: str, image_url: str | None = None):
    if not FACEBOOK_PAGE_ACCESS_TOKEN:
        raise ValueError("FACEBOOK_PAGE_ACCESS_TOKEN is not configured")

    # 📸 Post con image

    if image_url:
        url = f"{GRAPH_BASE_URL}/{FACEBOOK_PAGE_ID}/photos"
        payload = {
            "url"
        }



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
