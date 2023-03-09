from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWebEngineWidgets import *
from PySide6.QtWebEngineCore import *

import requests
import qdarktheme


class MyBrowser():

    def __init__(self):

        self.window = QWidget()
        self.window.setWindowTitle("Xenon | Be Colourless")

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal = QHBoxLayout()
        self.horizontal.setContentsMargins(10, 10, 10, 0)

        self.url_bar = QLineEdit()
        self.url_bar.mousePressEvent = lambda _: self.url_bar.selectAll(
        ) if not self.url_bar.hasSelectedText() else self.url_bar.deselect()
        self.url_bar.returnPressed.connect(
            lambda: self.navigate(self.url_bar.text()))

        self.go_btn = QPushButton("-->")
        self.go_btn.setMinimumHeight(25)
        self.go_btn.setMinimumWidth(50)

        self.back_btn = QPushButton("<")
        self.back_btn.setMinimumHeight(25)
        self.back_btn.setMinimumWidth(50)

        self.forward_btn = QPushButton(">")
        self.forward_btn.setMinimumHeight(25)
        self.forward_btn.setMinimumWidth(50)

        self.stop_btn = QPushButton("X")
        self.stop_btn.setMinimumHeight(25)
        self.stop_btn.setMinimumWidth(50)

        self.home_btn = QPushButton("")
        self.home_btn.setMinimumHeight(25)
        self.home_btn.setMinimumWidth(50)

        self.url_bar.setTextMargins(5, 0, 5, 0)

        self.horizontal.addWidget(self.back_btn)
        self.horizontal.addWidget(self.forward_btn)
        self.horizontal.addWidget(self.home_btn)
        self.horizontal.addWidget(self.url_bar)
        self.horizontal.addWidget(self.stop_btn)
        self.horizontal.addWidget(self.go_btn)

        self.browser = QWebEngineView(self.window)

        self.browser.settings().setAttribute(
            QWebEngineSettings.FullScreenSupportEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.browser.settings().setAttribute(
            QWebEngineSettings.JavascriptCanOpenWindows, True)

        self.browser.page().fullScreenRequested.connect(
            lambda request: self.handle_fullscreen_requested(request))

        self.go_btn.clicked.connect(lambda: self.navigate(self.url_bar.text()))
        self.back_btn.clicked.connect(self.browser.back)
        self.forward_btn.clicked.connect(self.browser.forward)
        self.home_btn.clicked.connect(
            lambda: self.browser.setUrl(QUrl("https://search.nnisarg.xyz")))
        self.stop_btn.clicked.connect(self.browser.stop)

        self.layout.addLayout(self.horizontal)
        self.layout.addWidget(self.browser)

        self.browser.setUrl(QUrl("https://search.nnisarg.xyz"))
        self.url_bar.setPlaceholderText("Type here")

        self.browser.urlChanged.connect(
            lambda: self.format_url(self.browser.url().toString()))
        self.browser.loadFinished.connect(lambda: self.window.setWindowTitle(
            "%s | Xenon - Be Colourless" % self.browser.page().title()))

        self.window.setLayout(self.layout)
        self.window.show()

        reload_shortcut = QShortcut(QKeySequence("Ctrl+r"), self.window)
        self.browser.connect(reload_shortcut, SIGNAL('activated()'), self.browser, SLOT('reload()'))

        jump_to_search_shortcut = QShortcut(QKeySequence("Ctrl+l"), self.window)
        self.browser.connect(jump_to_search_shortcut, SIGNAL('activated()'), self.url_bar, SLOT('setFocus()'))
        self.browser.connect(jump_to_search_shortcut, SIGNAL('activated()'), self.url_bar, SLOT('selectAll()'))

    def handle_fullscreen_requested(self, request):

        request.accept()

        if request.toggleOn():
            self.horizontal.setContentsMargins(0, 0, 0, 0)
            self.browser.showFullScreen()
            self.back_btn.hide()
            self.forward_btn.hide()
            self.home_btn.hide()
            self.url_bar.hide()
            self.go_btn.hide()
            self.stop_btn.hide()
        else:
            self.horizontal.setContentsMargins(10, 10, 10, 0)
            self.browser.showNormal()
            self.back_btn.show()
            self.forward_btn.show()
            self.home_btn.show()
            self.url_bar.show()
            self.go_btn.show()

    def navigate(self, url):

        if url.startswith("@y "):
            url = "https://youtube.com/search?q=" + url.removeprefix("@y ")

        elif url.startswith("@g "):
            url = "https://google.com/search?q=" + url.removeprefix("@g ")

        elif not url.startswith("http") and not url.startswith("file://"):
            url = "http://" + url
            self.url_bar.setText(url)

        try:
            response = requests.get(url)
        except:
            url = url.removeprefix("http://")
            url = "https://search.nnisarg.xyz/search?q=" + url

        self.browser.setUrl(QUrl(url))

        shown_url = self.browser.url().toString()
        self.format_url(shown_url)

    def format_url(self, url):

        url = url.removesuffix("/")

        if url.startswith("https://"):
            url = url.removeprefix("https://")
        elif url.startswith("http://"):
            url = url.removeprefix("http://")
        if url != "search.nnisarg.xyz" and url != "search.nnisarg.xyz/search?q=":
            self.url_bar.setText(url)
        else:
            self.url_bar.clear()
            self.url_bar.setPlaceholderText("Type here")

        self.url_bar.clearFocus()

if __name__ == "__main__":
    # import os
    # import sys

    # os.environ[
    #     "QTWEBENGINE_CHROMIUM_FLAGS"
    # ] = "--blink-settings=forceDarkModeEnabled=true"
    # app = QApplication(sys.argv)

    app = QApplication([])
    app.setApplicationName("Xenon | Be Colourless")
    app.setStyleSheet(qdarktheme.load_stylesheet())
    window = MyBrowser()
    app.exec()
