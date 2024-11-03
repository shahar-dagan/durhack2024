from openai import OpenAI
import requests
from datetime import datetime

client = OpenAI(
    api_key="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"
)

# prompt = "Make an image of a boy waking up on a pirate ship. It should be in a cartoon style for a child friendly text adventure game"
# prompt = "A pirate crew"


def get_dalle_image_url(prompt):
    # response = client.images.generate(
    # model="dall-e-3",
    # prompt=prompt,
    # size="1024x1024",
    # quality="standard",
    # n=1,
    # )

    # image_url = response.data[0].url

    image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTkhAV70lOOVr2-gS3HXBVvR-wHv9IiTCmU8Q&s"

    # Download and save the image
    image_data = requests.get(image_url).content

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    with open(f"images/image_{timestamp}.png", "wb") as file:
        file.write(image_data)

    return image_url