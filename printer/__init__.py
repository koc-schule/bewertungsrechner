"""
Dieses Package ist für die Nutzung des Druckers zu verwenden.
"""

from escpos.printer import Usb
from PIL import Image
from pathlib import Path
import libusb
import usb.core
import usb.backend.libusb1
import libusb_package
import time