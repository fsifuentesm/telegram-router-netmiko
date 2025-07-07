# telegram-router-netmiko
Script thats run an a command using netmiko and notify us if something breaks with a telegram bot

# Bot de Monitoreo de Servidores (Telegram)

Este bot permite enviar por Telegram un resumen de servidores vivos (`alive`) y caídos (`dead`) usando Python.  
Funciona sin necesidad de programación asíncrona, ideal para scripts rápidos o automatizados.

---

## ✅ Requisitos

- Python 3.7+
- Un bot de Telegram con su token (lo puedes crear en [@BotFather](https://t.me/BotFather))
- Tu propio `chat_id` (puedes obtenerlo usando el método `getUpdates`)

---

## 📦 Instalación

Ejecuta lo siguiente para instalar las dependencias necesarias:

```bash
pip install requests python-telegram-bot
```

---

## ⚙️ Configuración

1. Abre el archivo Python del proyecto.
2. Reemplaza las siguientes variables con tus datos:

```python
bot_token = 'TU_TOKEN_DE_BOT_AQUI'
chat_id = 'TU_CHAT_ID_AQUI'
```

---

## 🚀 Uso

Para correr el script y enviar los mensajes de estado de los servidores:

```bash
python main.py
```

Esto enviará dos mensajes a tu chat de Telegram:

- 🟢 Servidores Alive
- 🔴 Servidores Dead

---

## 🧠 Notas

- Si no has hablado con el bot desde tu cuenta, Telegram **no permitirá que te envíe mensajes**. Mándale primero un `/start`.
- Usa Markdown para resaltar texto, puedes personalizar los mensajes fácilmente.

---
