from controller import mainWindowController
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import traceback
import logging
import sys
log = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
log.addHandler(handler)


def show_exception_box(log_msg):
    """Checks if a QApplication instance is available and shows a messagebox with the exception message.
    If unavailable (non-console application), log an additional notice.
    """
    if QApplication.instance() is not None:
        errorbox = QMessageBox()
        errorbox.setText("Oops. An unexpected error occured:\n{0}".format(log_msg))
        errorbox.exec_()
    else:
        log.debug("No QApplication instance available.")


class UncaughtHook(QObject):
    _exception_caught = pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(UncaughtHook, self).__init__(*args, **kwargs)

        # this registers the exception_hook() function as hook with the Python interpreter
        sys.excepthook = self.exception_hook

        # connect signal to execute the message box function always on main thread
        self._exception_caught.connect(show_exception_box)

    def exception_hook(self, exc_type, exc_value, exc_traceback):
        """Function handling uncaught exceptions.
        It is triggered each time an uncaught exception occurs.
        """
        if issubclass(exc_type, KeyboardInterrupt):
            # ignore keyboard interrupt to support console applications
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
        else:
            exc_info = (exc_type, exc_value, exc_traceback)
            log_msg = '\n'.join([''.join(traceback.format_tb(exc_traceback)),
                                 '{0}: {1}'.format(exc_type.__name__, exc_value)])
            log.critical("Uncaught exception:\n {0}".format(log_msg), exc_info=exc_info)

            # trigger message box show
            self._exception_caught.emit(log_msg)


if __name__ == '__main__':
    qt_exception_hook = UncaughtHook()
    # following couple of lines is a tweak to enable ipython --gui='qt'
    app = QApplication.instance()  # checks if QApplication already exists
    if not app:  # create QApplication if it doesnt exist
        app = QApplication(sys.argv)
    # Create and display the splash screen
    splash_pix = QPixmap(':/nurbs_patch.png')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    splash.setEnabled(False)
    # splash.setMask(splash_pix.mask())
    splash.show()
    splash.showMessage("<h1><font color='green'>Welcome to Curve Editor</font></h1>", Qt.AlignBottom | Qt.AlignCenter, Qt.black)

    mainWin = mainWindowController.Window()
    mainWin.showMaximized()
    splash.finish(mainWin)
    app.exec_()

