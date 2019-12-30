from controller import mainWindowController
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
# Qt error message traceback
sys._excepthook = sys.excepthook
def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
sys.excepthook = my_exception_hook
# Install qt debug message handler
def qt_message_handler(mode, context, message):
    if mode == QtInfoMsg:
        mode = 'INFO'
    elif mode == QtWarningMsg:
        mode = 'WARNING'
    elif mode == QtCriticalMsg:
        mode = 'CRITICAL'
    elif mode == QtFatalMsg:
        mode = 'FATAL'
    else:
        mode = 'DEBUG'
    print('qt_message_handler: line: %d, func: %s(), file: %s' % (
          context.line, context.function, context.file))
    print('  %s: %s\n' % (mode, message))
if __name__ == '__main__':
    qInstallMessageHandler(qt_message_handler)
    app = QApplication([])
    mainWin = mainWindowController.Window()
    mainWin.showMaximized()
    sys.exit(app.exec_())