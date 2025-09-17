import os
import json

# Lista de tarefas
tarefas = []

# --- Funções de Persistência ---
def salvar_tarefas():
    with open("tarefas.json", "w") as f:
        json.dump(tarefas, f, indent=4)

def carregar_tarefas():
    global tarefas
    with open("tarefas.json", "r") as f:
        tarefas = json.load(f)


# --- Funções de Gerenciamento de Tarefas ---
   
def adicionar_tarefa(tarefa):
    tarefas.append({"tarefa": tarefa, "concluida": False})
    salvar_tarefas()
    print(f"Tarefa '{tarefa}' adicionada com sucesso!\n")

def listar_tarefas():
    if not tarefas:
        print("Nenhuma tarefa encontrada.\n")
        return
    print("\n--- Lista de Tarefas ---")
    for i, t in enumerate(tarefas, 1):
        status = " ✔️ " if t["concluida"] else " ❌ "
        print(f"{i}. {t['tarefa']} [{status}]")
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
            tarefa = input("Digite a tarefa: ")
            adicionar_tarefa(tarefa)
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
            print("Saindo... até mais!")
            salvar_tarefas()
            break
        else:
            print("Opção inválida.\n")

# --- Execução ---
if __name__ == "__main__":
    carregar_tarefas()
    menu()
    
