# Monopoly Deal Networked Game

This is a Python implementation of the Monopoly Deal card game that currently supports networked 2-player gameplay with a server and client architecture.

---

## Requirements

- Python 3.7 or higher
- Standard Python libraries (socket, threading, etc.)
- Currently, no additional dependencies are required (requirements.txt might be empty)

---

## Setup

1. **Create and activate a virtual environment:**

```bash
 python -m venv .venv
 source .venv/bin/activate   # macOS/Linux
 .venv\Scripts\activate      # Windows
```

2. **Install dependencies (if any):**
```bash
   pip install -r requirements.txt
```

---

## How to Run

1. **Start the server:**

   ```bash
   python server.py
   ```

The server listens on 127.0.0.1 (localhost) by default and waits for players to connect.

2. **Start clients:**

In a separate terminal, run:

```bash
   python client.py
```
