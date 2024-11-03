import torch
import requests
from PIL import Image
from io import BytesIO
from matplotlib import pyplot as plt

# We'll be exploring a number of pipelines today!
from diffusers import StableDiffusionPipeline


# Set device
device = (
    "mps"
    if torch.backends.mps.is_available()
    else "cuda"
    if torch.cuda.is_available()
    else "cpu"
)


# Load the pipeline
model_id = "stabilityai/stable-diffusion-2-1-base"

pipe = StableDiffusionPipeline.from_pretrained(model_id).to(device)


# Set up a generator for reproducibility
generator = torch.Generator(device=device).manual_seed(42)


def create_image_factory(
        resolution=(480, 640),
        num_inference_steps = 35
    ):
    def create_image(prompt):
        # Run the pipeline, showing some of the available arguments
        pipe_output = pipe(
            prompt=prompt, # What to generate
            height=resolution[0], 
            width=resolution[1],     # Specify the image size
            # guidance_scale=8,          # How strongly to follow the prompt
            num_inference_steps=num_inference_steps,    # How many steps to take
            generator=generator        # Fixed random seed
        )

        image = pipe_output.images[0]
        return image
    
    return create_image
