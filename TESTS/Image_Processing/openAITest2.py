import requests
import numpy as np
import cv2
from scipy.spatial.distance import cosine

# URL to CLIP API
url = "https://api.openai.com/v1/images/generations"

# First image
img1 = 'Image_Processing\photos\Test\Reference\STANDARD.jpg'
# Second image
img2 = 'Image_Processing\photos\Test\Reference\WIN_20230123_10_46_27_Pro.jpg'

# Function to encode an image using CLIP
def encode_image(img, api_key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    model = "image-alpha-001"
    data = {
        "model": model,
        "data": [{"image": img}]
    }

    resp = requests.post(url, headers=headers, json=data)

    if resp.status_code != 200:
        raise ValueError("Failed to encode image")

    response_text = resp.json()
    encoded_img = response_text["data"][0]["features"][0]
    return encoded_img

# Function to compare two images using CLIP
def compare_images(img1, img2, api_key):
    encoded_img1 = encode_image(img1, api_key)
    encoded_img2 = encode_image(img2, api_key)

    similarity = 1 - cosine(encoded_img1, encoded_img2)
    return similarity

# Your OpenAI API Key
api_key = "YOUR_API_KEY"

similarity = compare_images(img1, img2, api_key)
print("Similarity:", similarity)