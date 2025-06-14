#!/usr/bin/env python3

from controller import *



def main() -> None:
    application = QApplication([])
    controller = Controller()
    application.exec_()

if __name__ == "__main__":
    main()