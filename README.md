# Description
A simple script that scrapes data from the Cambridge SU event calendar and generates an ICS file from it.

A public Google Calendar that is regularly updated with the events can be found [here](https://calendar.google.com/calendar/u/0?cid=ZWQxM2E1MWY2M2Y4ZDMzNWI1NTY5ZTVlMTg0YzExN2I0MTVhZjQyMzg1MDY5Mjc3NjhhYTU1ZGU5MTdlNTI5YUBncm91cC5jYWxlbmRhci5nb29nbGUuY29t).

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
