import os

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
