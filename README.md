# Description
A simple script that scrapes data from the Cambridge SU event calendar and generates an ICS file from it.

# Why?
I built this because I didn't see an easy way to import the SU events into my Google Calendar. 
Hopefully this will be useful to others until the SU releases their own official export feature.

# How to Use?

First clone the repository and cd into it.

Create a virtual environment and install the necessary dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the script
```bash
python main.py
```
# Roadmap
- Allow filtering of events before generating ICS
