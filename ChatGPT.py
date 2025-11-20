#!/usr/bin/env python3
import gi
import sys
from pathlib import Path

gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.1")

from gi.repository import Gtk, WebKit2, Gio

CHATGPT_URL = "https://chatgpt.com/"
APPLICATION_ID = "br.com.diegofc.ChatGPTBrowserUnico"

DATA_DIR = Path.home() / ".local" / "share" / APPLICATION_ID
DATA_DIR.mkdir(parents=True, exist_ok=True)


class ChatGPTApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id=APPLICATION_ID)
        self.window = None

    def do_activate(self):

        if self.window is None:

            print("WebKit2 antigo detectado — usando modo compatível.")

            # =============================================================
            #   CONTEXTO PADRÃO (a única opção na sua versão)
            # =============================================================
            context = WebKit2.WebContext.get_default()

            # COOKIE MANAGER ANTIGO
            cookie_mgr = context.get_cookie_manager()

            # Política antiga: CookieAcceptPolicy
            cookie_mgr.set_accept_policy(WebKit2.CookieAcceptPolicy.ALWAYS)

            # Persistência REAL: sqlite se suportado
            cookies_file = DATA_DIR / "cookies.sqlite"

            try:
                cookie_mgr.set_persistent_storage(
                    str(cookies_file),
                    WebKit2.CookiePersistentStorage.SQLITE
                )
                print("Persistência de cookies ativada (SQLite).")
            except:
                cookie_mgr.set_persistent_storage(
                    str(DATA_DIR / "cookies.txt"),
                    WebKit2.CookiePersistentStorage.TEXT
                )
                print("Persistência TEXT usada (SQLite não suportado).")

            # =============================================================
            #   JANELA E WEBVIEW
            # =============================================================
            self.window = Gtk.ApplicationWindow(application=self, title="ChatGPT")
            self.window.set_default_size(900, 700)

            self.webview = WebKit2.WebView.new_with_context(context)
            self.webview.load_uri(CHATGPT_URL)

            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.window.add(vbox)

            vbox.pack_start(self.webview, True, True, 0)

            button = Gtk.Button(label="Encerrar Serviço")
            button.connect("clicked", lambda *a: self.quit())
            vbox.pack_end(button, False, False, 5)

            self.window.connect("delete-event", self.on_close)

            self.window.show_all()

        else:
            self.window.present()

    def on_close(self, widget, event):
        widget.hide()
        return True


if __name__ == "__main__":
    print("Iniciando ChatGPT Browser (modo compatível com WebKit2GTK antigo)...")
    app = ChatGPTApp()
    sys.exit(app.run(sys.argv))

