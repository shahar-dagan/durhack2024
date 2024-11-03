# ./install_requirements.ps1

huggingface-cli login --token "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"


pip install -Uq diffusers ftfy accelerate
pip install -Uq git+https://github.com/huggingface/transformers
python ./experiment/create_images_2.py
