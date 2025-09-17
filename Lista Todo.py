# -*- coding: utf-8 -*-
# lista_todo.py
tarefas = []



def mostrar_tarefas():
    if not tarefas:
        print("\nNenhuma tarefa adicionada ainda.")
    else:
        print("\nLista de Tarefas:")
        for i, tarefa in enumerate(tarefas, start=1):
            print(f"{i}. {tarefa}")

def adicionar_tarefa():
    tarefa = input("\nDigite a nova tarefa: ")
    tarefas.append(tarefa)
    print(f"Tarefa '{tarefa}' adicionada com sucesso!")

def remover_tarefa():
    mostrar_tarefas()
    try:
        indice = int(input("\nDigite o número da tarefa que deseja remover: "))
        tarefa_removida = tarefas.pop(indice - 1)
        print(f"Tarefa '{tarefa_removida}' removida com sucesso!")
    except (ValueError, IndexError):
        print("Número inválido. Tente novamente.")

def menu():
    while True:
        print("\n=== LISTA TODO ===")
        print("1 - Ver tarefas")
        print("2 - Adicionar tarefa")
        print("3 - Remover tarefa")
        print("4 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            mostrar_tarefas()
        elif opcao == "2":
            adicionar_tarefa()
        elif opcao == "3":
            remover_tarefa()
        elif opcao == "4":
            print("Saindo... Até mais!")
            break
        else:
            print("Opção inválida! Tente novamente.")

menu()
