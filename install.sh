#!/bin/bash
set -e

# Dependências
sudo apt update
sudo apt install -y wmctrl xdotool devilspie2

# Caminhos
DESKTOP_SRC="WebApp-ChatGPT4319.desktop"
DESKTOP_DST="$HOME/.local/share/applications"
DEVIL_DIR="$HOME/.config/devilspie2"
SCRIPT_SRC_SH="chatgpt.sh"
SCRIPT_SRC_LUA="chatgpt.lua"

mkdir -p "$DESKTOP_DST"
mkdir -p "$DEVIL_DIR"

# Copiar arquivos (não mover)
cp -f "$DESKTOP_SRC" "$DESKTOP_DST/"
cp -f "$SCRIPT_SRC_SH" "$DEVIL_DIR/"
cp -f "$SCRIPT_SRC_LUA" "$DEVIL_DIR/"

# Permissão executável no script
chmod +x "$DEVIL_DIR/$(basename "$SCRIPT_SRC_SH")"

# Atualiza cache do menu
update-desktop-database "$DESKTOP_DST" >/dev/null 2>&1 || true

# Cria atalho em ~/.local/bin para abrir facilmente
mkdir -p "$HOME/.local/bin"
cat > "$HOME/.local/bin/chatgpt" <<'EOF'
#!/bin/bash
bash "$HOME/.config/devilspie2/chatgpt.sh"
EOF
chmod +x "$HOME/.local/bin/chatgpt"

# Garante que ~/.local/bin esteja no PATH em shells interativos
if ! echo "$PATH" | /bin/grep -q "$HOME/.local/bin"; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi

echo "Instalação concluída. Arquivos copiados."
echo "configure o atalho pelas configurações do sistema. adicione um atalho para o arquivo ~/.config/devilspie2/chatgpt.sh, recomendo o alt+espaço"

