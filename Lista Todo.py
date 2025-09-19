"""
==================================================
  Projeto: Lista ToDo em Python
  Descrição: Sistema simples de gerenciamento de tarefas
==================================================

📌 Funcionalidades implementadas:
 - Adicionar tarefas
 - Listar tarefas (todas, concluídas, pendentes, atrasadas)
 - Concluir tarefas
 - Editar tarefas (nome, prioridade e prazo)
 - Remover tarefas
 - Ordenar por prioridade e prazo
 - Exportar tarefas para CSV e TXT
 - Notificação inteligente via WhatsApp (CallMeBot)

🚀 Futuras implementações:
 - Interface web com Flask
 - Banco de dados SQLite (substituir JSON)
 - Dashboard de produtividade
 - Usuários com autenticação

Autor: EnzoGabs277
Data de criação: Setembro/2025
==================================================
"""
import os
import json
import csv
import requests
from datetime import datetime

# Lista de tarefas
tarefas = []

WHATSAPP_PHONE = "5512996599479"  # Seu número no formato internacional
API_KEY = "2038085"  # Sua chave fornecida pelo CallMeBot


# --- Funções de Persistência ---
def salvar_tarefas():
    with open("tarefas.json", "w", encoding="utf-8") as f:
        json.dump(tarefas, f, indent=4, ensure_ascii=False)

def carregar_tarefas():
    global tarefas
    if os.path.exists("tarefas.json"):
        with open("tarefas.json", "r", encoding="utf-8") as f:
            try:
                tarefas = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                tarefas = []
    else:
        tarefas = []

# --- Função para enviar mensagem pelo WhatsApp ---
def enviar_whatsapp(mensagem: str):
    try:
        url = (
            f"https://api.callmebot.com/whatsapp.php?"
            f"phone={WHATSAPP_PHONE}&text={mensagem}&apikey={API_KEY}"
        )
        requests.get(url)
        print("📲 Notificação enviada pelo WhatsApp!")
    except Exception as e:
        print(f"❌ Erro ao enviar WhatsApp: {e}")




# --- Funções Auxiliares ---
def prioridade_valor(prioridade):
    mapa = {"alta": 1, "média": 2, "baixa": 3}
    return mapa.get(prioridade, 4)

def ordenar_tarefas(criterio="prioridade"):
    if criterio == "prioridade":
        return sorted(tarefas, key=lambda t: prioridade_valor(t["prioridade"]))
    elif criterio == "prazo":
        return sorted(
            tarefas,
            key=lambda t: datetime.strptime(t["prazo"], "%d/%m/%Y")
            if t["prazo"] != "Sem prazo" else datetime.max
        )
    return tarefas

def contar_atrasadas():
    hoje = datetime.now()
    return sum(
        1 for t in tarefas
        if t.get("prazo", "Sem prazo") != "Sem prazo"
        and not t.get("concluida", False)
        and datetime.strptime(t["prazo"], "%d/%m/%Y") < hoje
    )

# --- Funções de Exportação ---
def exportar_csv():
    with open("tarefas.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Tarefa", "Concluída", "Prioridade", "Prazo"])
        for t in tarefas:
            writer.writerow([
                t.get("tarefa", ""),
                "Sim" if t.get("concluida", False) else "Não",
                t.get("prioridade", "baixa"),
                t.get("prazo", "Sem prazo")
            ])
    print("✅ Tarefas exportadas para tarefas.csv")

def exportar_txt():
    with open("tarefas.txt", "w", encoding="utf-8-sig") as f:
        for i, t in enumerate(tarefas, 1):
            status = "✔️" if t.get("concluida", False) else "❌"
            prioridade = t.get("prioridade", "baixa")
            prazo = t.get("prazo", "Sem prazo")
            f.write(f"{i}. {t.get('tarefa', '')} [{status}] | Prioridade: {prioridade} | Prazo: {prazo}\n")
    print("✅ Tarefas exportadas para tarefas.txt")

# --- Função Resumo Diário ---
def resumo_diario():
    hoje = datetime.now().strftime("%d/%m/%Y")
    pendentes = [t for t in tarefas if not t["concluida"]]
    concluidas = [t for t in tarefas if t["concluida"]]
    atrasadas = [
        t for t in pendentes
        if t["prazo"] != "Sem prazo"
        and datetime.strptime(t["prazo"], "%d/%m/%Y") < datetime.now()
    ]

    resumo = (
        f"📅 Resumo Diário - {hoje}\n"
        f"Total: {len(tarefas)}\n"
        f"✔️ Concluídas: {len(concluidas)}\n"
        f"❌ Pendentes: {len(pendentes)}\n"
        f"⚠️ Atrasadas: {len(atrasadas)}"
    )

    print("\n" + resumo + "\n")
    enviar_whatsapp(resumo)



# --- Funções de Gerenciamento de Tarefas ---
def adicionar_tarefa():
    tarefa = input("Digite a tarefa: ")

    prioridade = ""
    while prioridade not in ["baixa", "média", "alta"]:
        prioridade = input("Digite a prioridade (baixa/média/alta): ").lower()
        if prioridade not in ["baixa", "média", "alta"]:
            print("❌ Prioridade inválida! Digite apenas: baixa, média ou alta.")

    prazo = None
    while True:
        entrada = input("Digite o prazo (DD/MM/AAAA) ou pressione Enter para deixar em branco: ")
        if entrada == "":
            break
        try:
            prazo = datetime.strptime(entrada, "%d/%m/%Y").strftime("%d/%m/%Y")
            break
        except ValueError:
            print("❌ Data inválida! Use o formato DD/MM/AAAA.")

    tarefas.append({
        "tarefa": tarefa,
        "concluida": False,
        "prioridade": prioridade,
        "prazo": prazo if prazo else "Sem prazo"
    })
    salvar_tarefas()
    print("✅ Tarefa adicionada com sucesso!")

def listar_tarefas(lista=None):
    if not tarefas:
        print("Nenhuma tarefa encontrada.\n")
        return
    
    if lista is None:
        lista = tarefas

    print("\n--- Lista de Tarefas ---")
    for i, t in enumerate(lista, 1):
        status = "✔️ " if t["concluida"] else "❌"
        prioridade = t.get("prioridade", "baixa")
        prazo = t.get("prazo", "Sem prazo")
        print(f"{i}. {t['tarefa']} [{status}] | Prioridade: {prioridade} | Prazo: {prazo}")
    print()

def listar_tarefas_filtradas(filtro="todas"):
    filtradas = []
    for t in tarefas:
        if filtro == "concluidas" and not t["concluida"]:
            continue
        elif filtro == "pendentes" and t["concluida"]:
            continue
        filtradas.append(t)
    listar_tarefas(filtradas)


def listar_tarefas_atrasadas():
    hoje = datetime.now()
    atrasadas = []
    for t in tarefas:
        if t["prazo"] != "Sem prazo" and not t["concluida"]:
            try:
                data_prazo = datetime.strptime(t["prazo"], "%d/%m/%Y")
                if data_prazo < hoje:
                    atrasadas.append(t)
            except ValueError:
                continue
    if atrasadas:
        print("\n--- Tarefas Atrasadas ---")
        listar_tarefas(atrasadas)
    else:
        print("\nNenhuma tarefa atrasada encontrada.\n")


def concluir_tarefa(indice):
    if 0 < indice <= len(tarefas):
        tarefas[indice - 1]["concluida"] = True
        salvar_tarefas()
        print(f"Tarefa {indice} concluída!\n")
    else:
        print("Índice inválido.\n")

def remover_tarefa(indice):
    if 0 < indice <= len(tarefas):
        removida = tarefas.pop(indice - 1)
        salvar_tarefas()
        print(f"Tarefa '{removida['tarefa']}' removida!\n")
    else:
        print("Índice inválido.\n")


def editar_tarefa(indice):
    if 0 < indice <= len(tarefas):
        tarefa = tarefas[indice - 1]
        print(f"Editando tarefa: {tarefa['tarefa']}")

        novo_nome = input("Novo nome (Enter para manter): ")
        if novo_nome.strip():
            tarefa["tarefa"] = novo_nome

        nova_prioridade = input("Nova prioridade (baixa/média/alta ou Enter para manter): ").lower()
        if nova_prioridade in ["baixa", "média", "alta"]:
            tarefa["prioridade"] = nova_prioridade

        novo_prazo = input("Novo prazo (DD/MM/AAAA ou Enter para manter): ")
        if novo_prazo.strip():
            try:
                tarefa["prazo"] = datetime.strptime(novo_prazo, "%d/%m/%Y").strftime("%d/%m/%Y")
            except ValueError:
                print("❌ Data inválida! Mantendo a anterior.")

        salvar_tarefas()
        print("✅ Tarefa editada com sucesso!\n")
    else:
        print("Índice inválido.\n")


# --- Menu Principal ---
def menu():
    while True:
        print("=== ToDo List ===")
        print("1 - Adicionar tarefa")
        print("2 - Listar todas as tarefas")
        print("3 - Listar tarefas concluídas")
        print("4 - Listar tarefas pendentes")
        print("5 - Concluir tarefa")
        print("6 - Remover tarefa")
        print("7 - Editar tarefa")
        print("8 - Listar tarefas ordenadas por prioridade")
        print("9 - Listar tarefas ordenadas por prazo")
        print("10 - Listar tarefas atrasadas")
        print("11 - Exportar tarefas para CSV")
        print("12 - Exportar tarefas para TXT")
        print("0 - Sair")
        
        opcao = input("Escolha: ")

        if opcao == "1":
            adicionar_tarefa()
        elif opcao == "2":
            listar_tarefas_filtradas("todas")
        elif opcao == "3":
            listar_tarefas_filtradas("concluidas")
        elif opcao == "4":
            listar_tarefas_filtradas("pendentes")
        elif opcao == "5":
            try:
                indice = int(input("Número da tarefa concluída: "))
                concluir_tarefa(indice)
            except ValueError:
                print("Digite um número válido.\n")
        elif opcao == "6":
            try:
                indice = int(input("Número da tarefa para remover: "))
                remover_tarefa(indice)
            except ValueError:
                print("Digite um número válido.\n")
        elif opcao == "7":
            try:
                indice = int(input("Número da tarefa para editar: "))
                editar_tarefa(indice)
            except ValueError:
                print("Digite um número válido.\n")
        elif opcao == "8":
            listar_tarefas(ordenar_tarefas("prioridade"))
        elif opcao == "9":
            listar_tarefas(ordenar_tarefas("prazo"))
        elif opcao == "10":
            listar_tarefas_atrasadas()
        elif opcao == "11":
            exportar_csv()
        elif opcao == "12":
            exportar_txt()
        elif opcao == "0":
            print("Saindo! Até mais 👋")
            salvar_tarefas()
            break
        else:
            print("Opção inválida.\n")

# --- Execução ---
if __name__ == "__main__":
    carregar_tarefas()
    resumo_diario()   # 🔹 Exibe só na abertura
    menu()
