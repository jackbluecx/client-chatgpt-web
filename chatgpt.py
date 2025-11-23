#!/usr/bin/env python3
import gi
import sys
import subprocess
from pathlib import Path

gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.1")
gi.require_version("Gdk", "3.0")

from gi.repository import Gtk, WebKit2, Gio, Gdk

CHATGPT_URL = "https://chatgpt.com/"
APPLICATION_ID = "br.com.diegofc.ChatGPTBrowserUnico"

DATA_DIR = Path.home() / ".local" / "share" / APPLICATION_ID
DATA_DIR.mkdir(parents=True, exist_ok=True)


class ChatGPTApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id=APPLICATION_ID)
        self.window = None

    def on_key_press(self, widget, event):
        is_control_pressed = event.state & Gdk.ModifierType.CONTROL_MASK

        if is_control_pressed and event.keyval == Gdk.KEY_Escape:
            window_id = self.window.get_window().get_xid()
            try:
                subprocess.run(["xdotool", "windowminimize", str(window_id)], check=True)
                return True
            except:
                return False

        if event.keyval == Gdk.KEY_Escape:
            widget.hide()
            return True

        return False

    def do_activate(self):

        if self.window is None:
            print("WebKit2 antigo detectado — usando modo compatível.")

            context = WebKit2.WebContext.get_default()
            cookie_mgr = context.get_cookie_manager()
            cookie_mgr.set_accept_policy(WebKit2.CookieAcceptPolicy.ALWAYS)

            cookies_file = DATA_DIR / "cookies.sqlite"
            try:
                cookie_mgr.set_persistent_storage(
                    str(cookies_file),
                    WebKit2.CookiePersistentStorage.SQLITE
                )
            except:
                cookie_mgr.set_persistent_storage(
                    str(DATA_DIR / "cookies.txt"),
                    WebKit2.CookiePersistentStorage.TEXT
                )

            self.window = Gtk.ApplicationWindow(application=self, title="ChatGPT")
            self.window.set_default_size(900, 700)

            # Sempre no topo
            self.window.set_keep_above(True)

            self.webview = WebKit2.WebView.new_with_context(context)
            self.webview.load_uri(CHATGPT_URL)

            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.window.add(vbox)
            vbox.pack_start(self.webview, True, True, 0)

            button = Gtk.Button(label="Encerrar Serviço")
            button.connect("clicked", lambda *a: self.quit())
            vbox.pack_end(button, False, False, 5)

            self.window.connect("delete-event", self.on_close)
            self.window.connect("key-press-event", self.on_key_press)

            self.window.show_all()
            self.window.present()

        else:
            win = self.window
            gdk_win = win.get_window()

            if gdk_win is not None:
                state = gdk_win.get_state()

                # Se estiver focada, minimizar
                if state & Gdk.WindowState.FOCUSED:
                    xid = gdk_win.get_xid()
                    try:
                        subprocess.run(["xdotool", "windowminimize", str(xid)], check=True)
                        return
                    except:
                        pass

            win.present()

    def on_close(self, widget, event):
        widget.hide()
        return True


if __name__ == "__main__":
    print("Iniciando ChatGPT Browser...")
    app = ChatGPTApp()
    try:
        sys.exit(app.run(sys.argv))
    except KeyboardInterrupt:
        sys.exit(0)

