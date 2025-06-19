# Bible-Gui App

## Overview
This is a gui version of the Terminal Bible App (https://github.com/davidrose07/Bible). It is a python based gui application designed to easily navigate between different versions, books, chapters, and verses. It has red-lettering(still under development) for the gospels.

## Features

* **Multiple Bible Translations:** Includes support for various Bible translations like NIV, NLT, and more.
* **Graphical User Interface (GUI):** Built with the `PyQt5` library for an interactive gui-based interface.
* **Red Letter Support:** Identifies and highlights the words of Jesus in red (if supported by the translation).
* **Search and Navigation:** Quickly navigate through books, chapters, and verses. *Search function is under construction.*
* **Robust Logging:** Logs errors and app behavior to a rotating log file using Python's `logging` module. All major components now include debug-level function entry logs.
* **Docker Support:** A Dockerfile is provided for containerized installation and distribution. The container build will not fail if optional dependencies like PyHyphen cannot be installed.

## Requirements

* Python 3.10
* Recommended to use a virtual environment if setting up locally
* Install dependencies:
* Linux (Debian/Ubuntu preferred)
* Bash shell
* Internet connection (for package installation)

## Docker Setup
If you want to run this application with docker then you can use the docker_install.sh file and it will set it up for you.

```bash
chmod +x docker_install.sh
./docker_install.sh
```
The install file will build and run the docker file. It will also create a symlink in your local/bin called bible-gui

To run the docker file:
```bash
    docker run -it bible-gui
```
* **Local Setup**
If you're installing locally (without Docker), use the `setup.py` script:

```bash
pip install -e .    Use the -e flag to make the script editable
```

run with command: bible-gui


### Adding Translations

To add a new Bible translation:

1. Place the XML file for the translation in the `translations` directory.
2. Ensure the XML file follows the correct format:

   * Root tag: `<bible>`
   * Books: `<b n="BookName">`
   * Chapters: `<c n="ChapterNumber">`
   * Titles: `<v n="0">Title Name</v>`
   * Verses: `<v n="VerseNumber">Verse text</v>`
     Example:

```xml
<bible>
  <b n="Matthew">
    <c n="5">
      <v n="0">Add title here</v>
      <v n="1">Verse text here</v>
      <v n="2">Another verse...</v>
    </c>
  </b>
</bible>
```

Known Issues:

* When verses that require red lettering have Jesus and others talking, use different quote styles (e.g., double quotes for Jesus, single quotes for others) to ensure only Jesus' words are red-lettered.

