# Synapx Autonomous Insurance Claims Processing Agent

## Overview
This project processes FNOL (First Notice of Loss) documents and automatically:
- Extracts claim fields
- Detects missing information
- Routes claims using predefined rules
- Provides explainable routing decisions

## Tech Stack
- Python
- pdfplumber
- FastAPI

## How to Run
```bash
pip install -r requirements.txt
python agent.py
