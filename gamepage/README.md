# Create new ENV 
python3 -m venv venv

# Activate new ENV
## Windows PowerShell
.venv\Scripts\Activate.ps1
## macOS and Linux
source .venv/bin/activate

# Install streamlit 
pip install streamlit

# Run app 
streamlit run api.py
