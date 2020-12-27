mkdir -p ~/.streamlit/
echo "[general]
email = \"stark050600@mail.ru\"
" > ~/.streamlit/credentials.toml
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml