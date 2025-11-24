ChatGPT Browser Único

Este é um script Python que cria um aplicativo de desktop minimalista e dedicado para acessar o ChatGPT, usando GTK3 e WebKit2. Ele mantém a janela sempre visível (always on top) e permite ocultar ou minimizar rapidamente a aplicação.

Dependências

Este programa requer o Python 3 e algumas bibliotecas específicas do GTK e do sistema de janelas do Linux:

Python 3: O interpretador.

GObject Introspection (PyGObject): O binding que permite ao Python interagir com bibliotecas GTK.

WebKit2GTK: O motor de renderização do navegador.

xdotool: Uma ferramenta de linha de comando para manipular janelas X11, necessária para a função de minimizar (Ctrl+Esc).

Instalação

Siga os comandos abaixo para instalar as dependências no seu sistema Linux (testado em distribuições baseadas em Debian/Ubuntu).

1. Instalar Bibliotecas Essenciais

Instale as dependências principais via apt:

# Atualiza a lista de pacotes
sudo apt update

# Instala o Python 3 e as bibliotecas GTK/WebKit2 necessárias
sudo apt install python3 python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.1


2. Instalar xdotool

O xdotool é necessário para a funcionalidade de minimizar a janela usando a combinação de teclas Ctrl + Esc:

sudo apt install xdotool


3. Rodar o Programa

Salve o código Python em um arquivo chamado chatgpt_browser.py.

Torne o arquivo executável:

chmod +x chatgpt_browser.py


Execute o aplicativo:

./chatgpt_browser.py


Atalhos de Teclado

Escape (Esc): Oculta a janela (hides the window).
