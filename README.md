# Pinterest Unshittifier

Fixes "broken" Pinterest filenames like `jpg`, `jpg(1)`, `png(12)` automatically.

## Installation (AUR)

```bash
yay -S pinterest-unshittifier-git

```

## Usage

```bash
systemctl --user enable --now pinterest-unshittifier.service

```

## How it works

* **Monitors** `~/Downloads` via `watchdog`.
* **Generates** random 8-char names.
* **Restores** missing extensions (`.jpg`, `.png`, etc.).

## Dev Setup

```bash
git clone https://github.com/Tok1shu/pinterest-unshittifier.git
python -m venv .venv && source .venv/bin/activate
pip install watchdog
python main.py

```


<img src="https://github.com/user-attachments/assets/41ef03c6-11b0-4857-a630-7feef84a9215" height="300" align="left" alt="XiKxmFjl">
<img src="https://github.com/user-attachments/assets/c82320bf-25f7-418a-853d-7e7a651016a8" height="300" alt="image">

<br clear="left"/>
