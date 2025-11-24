#!/bin/bash

# Nome do seu programa
PROGRAM_NAME="gui_simple"
# Nome do arquivo principal Python
PYTHON_FILE="gui_simple.py"
# Nome do script auxiliar Shell
SHELL_FILE="auto_off.sh"

# --- 0. Mover Arquivos para a Pasta Home ---

echo "Movendo arquivos de código para a pasta Home do usuário: ~/"

# Move o script Python e o Shell para a pasta Home
mv "$PYTHON_FILE" "$HOME/"
mv "$SHELL_FILE" "$HOME/"
chmod +x "$HOME/$SHELL_FILE"

echo "Arquivos movidos e permissões atualizadas para o script shell."

# Define o comando de execução final que agora usa o caminho padronizado na Home
EXEC_COMMAND="python3 $HOME/$PYTHON_FILE"

# --- 1. Instalação de Dependências ---

echo "Iniciando a instalação de dependências. Será solicitado o uso de sudo."

# Tenta identificar o gerenciador de pacotes e instala o Python e pip, se necessário
if command -v apt-get &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip
elif command -v dnf &> /dev/null; then
    sudo dnf install -y python3 python3-pip
elif command -v pacman &> /dev/null; then
    sudo pacman -Sy --noconfirm python python-pip
else
    echo "Não foi possível identificar um gerenciador de pacotes suportado. Instale python3 e python3-pip manualmente."
fi

# Instala as dependências do projeto listadas no requirements.txt
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "Dependências do projeto instaladas via requirements.txt."
else
    echo "Arquivo requirements.txt não encontrado."
fi

# --- 2. Criação do Arquivo .desktop ---

# Cria o conteúdo do arquivo .desktop
DESKTOP_CONTENT="[Desktop Entry]
Name=$PROGRAM_NAME
Comment=Script de inicialização automática do $PROGRAM_NAME
Exec=nohup $EXEC_COMMAND &
Terminal=false
Type=Application
X-GNOME-Autostart-enabled=true
"

# Define o nome do arquivo e o caminho
DESKTOP_FILE="$HOME/.local/share/applications/$PROGRAM_NAME.desktop"

# Escreve o conteúdo no arquivo .desktop
echo "$DESKTOP_CONTENT" > "$DESKTOP_FILE"
chmod +x "$DESKTOP_FILE"

echo "Arquivo .desktop criado em: $DESKTOP_FILE"

# --- 3. Criação do Atalho de Inicialização ---

# Define a pasta de inicialização para o usuário atual
AUTOSTART_DIR="$HOME/.config/autostart"

# Verifica se a pasta existe e a cria se necessário
mkdir -p "$AUTOSTART_DIR"

# Cria um link simbólico do .desktop para a pasta de inicialização
LINK_TARGET="$AUTOSTART_DIR/$PROGRAM_NAME.desktop"
ln -sf "$DESKTOP_FILE" "$LINK_TARGET"

echo "Atalho de inicialização automática criado em: $LINK_TARGET"
echo "Instalação e configuração de inicialização concluídas. Seu programa está na sua pasta Home."
