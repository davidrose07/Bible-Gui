# 📖 Bible-Gui App

A graphical interface for exploring multiple Bible translations with ease.
This is the GUI version of the [Terminal Bible App](https://github.com/davidrose07/Bible), built with Python and PyQt5.

---

## 🚀 Overview

Bible-Gui is a Python-based application that provides an intuitive GUI to navigate Bible translations, books, chapters, and verses.
Red-letter support is included (currently under development) for highlighting the words of Jesus in the Gospels.

---

## ✨ Features

* **Multiple Translations** — Support for various Bible versions like NLT, NIV, and others.
* **User-Friendly GUI** — Built with `PyQt5` for a clean and interactive interface.
* **Red Letter Support** — Highlights Jesus’ words in red (for supported translations).
* **Book/Chapter/Verse Navigation** — Easily browse between sections of the Bible.
* **Logging** — Errors and activity are logged via Python’s `logging` module with rotating log files.
* **Docker Support** — Containerized setup with graceful fallback if optional packages (like PyHyphen) fail to install.

---

## ⚙️ Requirements

* Python 3.10+
* Bash shell (for setup scripts)
* Linux (Debian/Ubuntu preferred)
* Internet connection (for installing dependencies)
* \[Optional] Docker for containerized execution

---

## 🐳 Docker Setup

To install and run via Docker:

```bash
chmod +x docker_install.sh
./docker_install.sh
```

This script:

* Builds the Docker image
* Creates a symlink in `~/bin` or `/usr/local/bin` as `bible-gui`

To run the app:

```bash
docker run -it bible-gui
```

---

## 🧪 Local Setup (Without Docker)

Create and activate a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

Install in editable mode:

```bash
pip install -e .
```

Run the app with:

```bash
bible-gui
```

---

## 📥 Adding Translations

To add a new Bible translation:

1. Place the XML file in the `translations/` directory.
2. Ensure the XML follows this structure:

```xml
<bible>
  <b n="Matthew">
    <c n="5">
      <v n="0">Title of the section</v>
      <v n="1">Blessed are the poor in spirit...</v>
      <v n="2">Blessed are those who mourn...</v>
    </c>
  </b>
</bible>
```

* `<b>`: Book name (e.g., Matthew)
* `<c>`: Chapter number
* `<v>`: Verse number (0 is optional title)

---

## 🛠️ Known Issues

* **Red-letter precision**: When verses contain both Jesus' and others' dialogue, use different quote styles (e.g., double quotes for Jesus, single quotes for others) to correctly isolate His words for red-lettering.

---

## 📜 License

MIT License

---

## 🙏 Acknowledgments

* PyQt5 for GUI
* Original CLI version: [Bible Terminal App](https://github.com/davidrose07/Bible)
* Bible XML translations from public or permissively licensed sources
