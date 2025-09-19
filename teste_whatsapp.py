import requests

def enviar_alerta_whatsapp(numero, mensagem, apikey):
    try:
        url = f"https://api.callmebot.com/whatsapp.php?phone={numero}&text={mensagem}&apikey={apikey}"
        resposta = requests.get(url)
        if resposta.status_code == 200:
            print("✅ Notificação enviada com sucesso!")
        else:
            print("❌ Erro ao enviar mensagem:", resposta.text)
    except Exception as e:
        print("⚠️ Falha ao enviar notificação:", e)

# --- Teste ---
numero = "5512996599479"
apikey = "2038085"
mensagem = "🚀 Teste automático da ToDo List funcionando!"

enviar_alerta_whatsapp(numero, mensagem, apikey)
