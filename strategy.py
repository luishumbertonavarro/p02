import datetime
from abc import ABC, abstractmethod
import pyautogui


class AccionEstrategia(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """

    @abstractmethod
    def realizar_accion(self, **kwargs):
        pass


class CapturarPantallaStrategyAccion(AccionEstrategia):
    def realizar_accion(self, direccion):
        e = str(datetime.datetime.now())
        f = e.replace(":", "")
        g = f.replace(".", "")
        h = g.replace(" ", "")
        pyautogui.screenshot(direccion + h + '.png')
