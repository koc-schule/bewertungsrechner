from __future__ import annotations
from . import *
from . import log

class PrinterLibrary:
    """
    Bibliothek für Operationen die den Ausdruck auf Kassenbond erleichtern.
    """
    #region Access
    base: PrinterLibrary = None
    isPrinterConnected: bool = False
    #endregion
    
    def __init__(self) -> None:
        """
        Initialisiert die Bibliothek sowie die benötigte `Usb` Instanz und. Die Bibliothek kann über
        `PrinterLibrary.base` aufgerufen werden.
        """
        # Neue `events.log` Datei anlegen, Liste und Dictionary anlegen, Drucker initialisieren und Assets hinzufügen
        log.reset()
        self.list: list[bool] = []
        self.dict: dict[str, bool] = {}
        self.initialize_printer()
        self.initialize_assets()
        PrinterLibrary.base = self
    
    #region Library Management
    def add(self, id: str, item: bool) -> bool:
        """
        Funktion für das Hinzufügen eines Templates/Assets in die Bibliothek

        Args:
            id (str): ID des Templates/Assets
            item (bool): Die Funktion des Templates/Assets

        Returns:
            bool: Die Funktion des Templates/Assets
        """
        self.list.append(item)
        self.dict[id] = item
        return item
    
    def get(self, function: str) -> bool:
        """
        Gibt das gesuchte Asset zurück

        Args:
            function (str): ID des Assets

        Returns:
            bool: Rückgabewert der Funktion
        """
        if function in self.dict:
            return self.dict[function]
        log.log("The given function is not represented in the library\n\t>>> Empty function returned (given statement will have no effect)")
        return lambda *args: ...
    
    def activate(self, function: str, **kwargs) -> bool:
        """
        Aktiviert ein Asset der Bibliothek

        Args:
            function (str): Name bzw. ID des Assets

        Returns:
            bool: True (nicht wichtig)
        """
        return self.get(function)(**kwargs)
    #endregion

    def initialize_printer(self) -> None:
        """
        Schließt den Printer an
        """
        # Zusammenfassung: Connected den Printer und fängt Fehler ab
        try:
            backend = libusb_package.get_libusb1_backend()
            log.log(f"Backend found: {bool(backend)}")
            dev = usb.core.find(backend=backend, find_all=True)

            if dev is None:
                log.log("Device could not be found")
                return
            else:
                log.log("Device found successfully")
                
            self.printer = Usb(0x28e9, 0x0289, 0, profile="ZJ-5870", backend=backend)
            
            log.log(f"Printer usable: {self.printer.is_usable()}")
            # log.log(f"Printer online: {self.printer.is_online()}") # Diese Funktion crasht irgendwie
        except Exception as e:
            log.log(str(e))
            PrinterLibrary.isPrinterConnected = False
        else:
            PrinterLibrary.isPrinterConnected = True
        
    
    def initialize_assets(self) -> None:
        """
        Initialisiert die Assets
        """
        self.add(
            "write_text",
            lambda **kwargs: PrinterLibrary.base.action_text(
                kwargs["text"],
                align=kwargs.get("align", "left"),
                bold=kwargs.get("bold", False),
                width=kwargs.get("width", 1),
                height=kwargs.get("height", 1),
                line_break=kwargs.get("line_break", True)
            )
        )
        self.add(
            "table_2",
            lambda **kwargs: PrinterLibrary.base.action_table_2(
                content=kwargs["content"],
                ratio=kwargs.get("ratio", (15, 15))
            )
        )
        self.add(
            "table_3",
            lambda **kwargs: PrinterLibrary.base.action_table_3(
                content=kwargs["content"],
                ratio=kwargs.get("ratio", (10, 10, 9))
            )
        )
        self.add(
            "line",
            lambda **kwargs: PrinterLibrary.base.action_text("-" * 31)
        )
        self.add(
            "break",
            lambda **kwargs: PrinterLibrary.base.action_text("")
        )
        
    @staticmethod    
    def action_text(text: str, align: str = "left", bold: bool = False, width: int = 1, height: int = 1, line_break: bool = True) -> bool:
        """
        Prints line of text onto the receipt.

        Args:
            text (str): The text to write
            align (str): The alginment of the text
            bold (bool): Bold text
            width (int): The width of the text
            height (int): The height of the text
        """
        if not PrinterLibrary.isPrinterConnected:
            print(text)
            log.log(text)
            return True
        PrinterLibrary.base.printer.set(align=align, bold=bold, width=width, height=height, double_height=False, double_width=False)
        PrinterLibrary.base.printer.text(f"{text}\n")
    
    @staticmethod
    def action_line():
        """
        Aktion für eine Line
        """
        PrinterLibrary.base.activate("write_text", text="-" * 31)
        
    @staticmethod        
    def action_table_2(content: list[tuple[str, str]], ratio: tuple[int, int]):
        """
        Aktion für Table mit zwei Spalten

        Args:
            content (list[tuple[str, str]]): Content
            ratio (tuple[int, int]): Verhältnis der Spalten
        """
        for left, right in content:
            ratio_right, ratio_left = ratio
            line = "{:<{}} {:>{}}".format(left, ratio_right, right, ratio_left)
            PrinterLibrary.base.activate("write_text", text=line, line_break=True)
            
    @staticmethod
    def action_table_3(content: list[tuple[str, str, str]], ratio: tuple[int, int, int]):
        """
        Aktion für Table mit drei Spalten

        Args:
            content (list[tuple[str, str]]): Content
            ratio (tuple[int, int]): Verhältnis der Spalten
        """
        for left, center, right in content:
            ratio_right, ratio_center, ratio_left = ratio
            line = "{:<{}} {:>{}} {:>{}}".format(left, ratio_right, center, ratio_center, right, ratio_left)
            PrinterLibrary.base.activate("write_text", text=line, line_break=True)