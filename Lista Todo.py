import os
import json
from datetime import datetime

# Lista de tarefas
tarefas = []

# --- Funções de Persistência ---
def salvar_tarefas():
    with open("tarefas.json", "w") as f:
        json.dump(tarefas, f, indent=4)

def carregar_tarefas():
    global tarefas
    if os.path.exists("tarefas.json"):
        with open("tarefas.json", "r") as f:
            try:
                tarefas = json.load(f)   
            except(FileNotFoundError, json.JSONDecodeError):
                tarefas = []
    else:
        tarefas = []

# --- Funções de Gerenciamento de Tarefas ---
   
def adicionar_tarefa():
    tarefa = input("Digite a tarefa: ")

    # 🔹 Validação da prioridade
    prioridade = ""
    while prioridade not in ["baixa", "média", "alta"]:
        prioridade = input("Digite a prioridade (baixa/média/alta): ").lower()
        if prioridade not in ["baixa", "média", "alta"]:
            print("❌ Prioridade inválida! Digite apenas: baixa, média ou alta.")

    # 🔹 Validação da data (DD/MM/AAAA)
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

    #Salvando a tarefa
    tarefas.append({
        "tarefa": tarefa, 
        "concluida": False,
        "prioridade": prioridade,
        "prazo": prazo if prazo else "Sem prazo"
    })
    salvar_tarefas()
    print("✅ Tarefa adicionada com sucesso!")

def listar_tarefas():
    if not tarefas:
        print("Nenhuma tarefa encontrada.\n")
        return
    
    print("\n--- Lista de Tarefas ---")
    for i, t in enumerate(tarefas, 1):
        status = "✔️ " if t["concluida"] else " ❌ "
        prioridade = t.get("prioridade", "baixa")
        prazo = t.get("prazo", "Sem prazo")
        print(f"{i}. {t['tarefa']} [{status}] | Prioridade: {prioridade} | Prazo: {prazo}")
    print()

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

def menu():
    while True:
        print("=== ToDo List ===")
        print("1 - Adicionar tarefa")
        print("2 - Listar tarefas")
        print("3 - Concluir tarefa")
        print("4 - Remover tarefa")
        print("0 - Sair")
        
        opcao = input("Escolha: ")

        if opcao == "1":
            adicionar_tarefa()
            salvar_tarefas()
        elif opcao == "2":
            listar_tarefas()
            salvar_tarefas()
        elif opcao == "3":
            try:
                indice = int(input("Número da tarefa concluída: "))
                concluir_tarefa(indice)
                salvar_tarefas()
            except ValueError:
                print("Digite um número válido.\n")
        elif opcao == "4":
            try:
                indice = int(input("Número da tarefa para remover: "))
                remover_tarefa(indice)
                salvar_tarefas()
            except ValueError:
                print("Digite um número válido.\n")
        elif opcao == "0":
            print("Saindo!")
            salvar_tarefas()
            break
        else:
            print("Opção inválida.\n")

# --- Execução ---
if __name__ == "__main__":
    carregar_tarefas()
    menu()
    
