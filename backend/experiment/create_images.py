# # https://huggingface.co/learn/diffusion-course/unit1/2

# import numpy as np
# import torch
# import torch.nn.functional as F
# from matplotlib import pyplot as plt
# from PIL import Image

# from diffusers import StableDiffusionPipeline


# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# model_id = "sd-dreambooth-library/mr-potato-head"
# pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to(device)


# prompt = "an abstract oil painting of sks mr potato head by picasso"
# image = pipe(prompt, num_inference_steps=50, guidance_scale=7.5).images[0]
# image



# from diffusers import DiffusionPipeline
# import torch

# # Load the model from Hugging Face
# pipe = DiffusionPipeline.from_pretrained(
#     "stabilityai/stable-diffusion-3.5-medium",
#     use_auth_token=True,  # Use this if you have a token set up
#     cache_dir="C:\\Users\\henry\\Downloads\\stable_diffusion_cache"  # Optional: Specify a local directory
# )

# # Move the model to GPU if available
# pipe = pipe.to("cuda") if torch.cuda.is_available() else pipe.to("cpu")

# # Run inference with a prompt
# prompt = "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"

# # Generate image
# image = pipe(prompt).images[0]
# # Save the image
# image.save("astronaut_created_image.png")
# print("Image saved successfully.")



import requests
# You can access the image with PIL.Image for example
import io
from PIL import Image

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3.5-medium"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	print(response.content)
	print(response.status_code)		
	assert response.status_code == 200

	return response.content
image_bytes = query({
	"inputs": "Astronaut riding a horse",
})
image = Image.open(io.BytesIO(image_bytes))
