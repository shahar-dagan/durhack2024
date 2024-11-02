./install_requirements.ps1

huggingface-cli login --token "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"

rm "C:\\Users\\henry\\Downloads\\stable_diffusion_cache"
python ./experiment/create_images.py
