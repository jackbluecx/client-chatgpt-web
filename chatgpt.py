#!/usr/bin/env python3
import gi
import sys
import subprocess
from pathlib import Path
from urllib.parse import urlparse

gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.1")
gi.require_version("Gdk", "3.0")

from gi.repository import Gtk, WebKit2, Gio, Gdk

CHATGPT_URL = "https://chatgpt.com/"
APPLICATION_ID = "br.com.diegofc.ChatGPTBrowserUnico"

DATA_DIR = Path.home() / ".local" / "share" / APPLICATION_ID
DATA_DIR.mkdir(parents=True, exist_ok=True)


def host_of(url):
    if not url:
        return ""
    try:
        p = urlparse(url)
        return (p.hostname or "").lower()
    except Exception:
        return ""


class ChatGPTApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id=APPLICATION_ID)
        self.window = None
        self.base_host = host_of(CHATGPT_URL)

    def on_key_press(self, widget, event):
        is_control_pressed = bool(event.state & Gdk.ModifierType.CONTROL_MASK)

        if is_control_pressed and event.keyval == Gdk.KEY_Escape:
            try:
                if self.window:
                    self.window.iconify()
                    return True
            except Exception:
                # fallback to xdotool if iconify not supported
                try:
                    gdk_win = self.window.get_window() if self.window else None
                    xid = gdk_win.get_xid() if gdk_win is not None else None
                    if xid:
                        subprocess.run(["xdotool", "windowminimize", str(xid)], check=True)
                        return True
                except Exception:
                    return False
            return False

        if event.keyval == Gdk.KEY_Escape:
            widget.hide()
            return True

        return False

    def _open_external(self, uri):
        if not uri:
            return
        try:
            Gio.AppInfo.launch_default_for_uri(uri, None)
        except Exception:
            # fallback to xdg-open
            try:
                subprocess.Popen(["xdg-open", uri])
            except Exception:
                pass

    def on_decide_policy(self, webview, decision, decision_type):
        if decision_type == WebKit2.PolicyDecisionType.NAVIGATION_ACTION:
            try:
                nav = decision.get_navigation_action()
                request = nav.get_request()
                uri = request.get_uri()
            except Exception:
                return False

            if not uri:
                return False

            uri_host = host_of(uri)
            # Se host diferente do host base, abrir externamente
            if uri_host and uri_host != self.base_host and not uri_host.endswith("." + self.base_host):
                self._open_external(uri)
                try:
                    decision.ignore()
                except Exception:
                    pass
                return True

        return False

    def on_create(self, webview, navigation_action):
        try:
            request = navigation_action.get_request()
            uri = request.get_uri()
        except Exception:
            return None

        if not uri:
            return None

        uri_host = host_of(uri)
        if uri_host and uri_host != self.base_host and not uri_host.endswith("." + self.base_host):
            self._open_external(uri)
            return None

        # Para new-window dentro do mesmo domínio, não criamos nova WebView e apenas permitimos padrão (ou criar uma WebView se desejar)
        return None

    def do_activate(self):

        if self.window is None:
            context = WebKit2.WebContext.get_default()
            cookie_mgr = context.get_cookie_manager()
            try:
                cookie_mgr.set_accept_policy(WebKit2.CookieAcceptPolicy.ALWAYS)
            except Exception:
                pass

            cookies_file = DATA_DIR / "cookies.sqlite"
            try:
                cookie_mgr.set_persistent_storage(
                    str(cookies_file),
                    WebKit2.CookiePersistentStorage.SQLITE
                )
            except Exception:
                try:
                    cookie_mgr.set_persistent_storage(
                        str(DATA_DIR / "cookies.txt"),
                        WebKit2.CookiePersistentStorage.TEXT
                    )
                except Exception:
                    pass

            self.window = Gtk.ApplicationWindow(application=self, title="ChatGPT")
            self.window.set_default_size(900, 700)
            self.window.set_keep_above(True)

            self.webview = WebKit2.WebView.new_with_context(context)
            # handlers para abrir links externos no navegador padrão
            self.webview.connect("decide-policy", self.on_decide_policy)
            self.webview.connect("create", self.on_create)

            self.webview.load_uri(CHATGPT_URL)

            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.window.add(vbox)
            vbox.pack_start(self.webview, True, True, 0)

            button = Gtk.Button(label="Encerrar Serviço")
            button.connect("clicked", lambda *a: self.quit())
            vbox.pack_end(button, False, False, 5)

            self.window.connect("delete-event", self.on_close)
            self.window.connect("key-press-event", self.on_key_press)
            self.window.set_wmclass("ChatGPT", "ChatGPT")
            self.window.show_all()
            self.window.present()

        else:
            win = self.window
            gdk_win = win.get_window()

            if gdk_win is not None:
                state = gdk_win.get_state()
                if state & Gdk.WindowState.FOCUSED:
                    try:
                        win.iconify()
                        return
                    except Exception:
                        try:
                            xid = gdk_win.get_xid()
                            subprocess.run(["xdotool", "windowminimize", str(xid)], check=True)
                            return
                        except Exception:
                            pass

            win.present()

    def on_close(self, widget, event):
        widget.hide()
        return True


if __name__ == "__main__":
    app = ChatGPTApp()
    try:
        sys.exit(app.run(sys.argv))
    except KeyboardInterrupt:
        sys.exit(0)

