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
                # 🔹 Corrigir tarefas antigas sem prazo ou prioridade
                for t in tarefas:
                    if "prazo" not in t:
                        t["prazo"] = "Sem prazo"
                    if "prioridade" not in t:
                        t["prioridade"] = "baixa"
            except (FileNotFoundError, json.JSONDecodeError):
                tarefas = []
    else:
        tarefas = []

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

    # Salvar a tarefa
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
        status = "✔️" if t["concluida"] else "❌"
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
    if not tarefas:
        print("Nenhuma tarefa encontrada.\n")
        return
    
    hoje = datetime.now()
    atrasadas = []

    for i, t in enumerate(tarefas, 1):
        prazo = t.get("prazo", "Sem prazo")
        if prazo != "Sem prazo" and not t["concluida"]:
            try:
                data_prazo = datetime.strptime(prazo, "%d/%m/%Y")
                if data_prazo < hoje:
                    atrasadas.append((i, t))
            except ValueError:
                pass  # ignora prazos inválidos antigos
    
    if not atrasadas:
        print("Nenhuma tarefa atrasada.\n")
    else:
        print("\n--- Tarefas Atrasadas ---")
        for i, t in atrasadas:
            status = "✔️" if t["concluida"] else "❌"
            print(f"{i}. {t['tarefa']} [{status}] | Prioridade: {t['prioridade']} | Prazo: {t['prazo']}")
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
        elif opcao == "0":
            print("Saindo! Até mais 👋")
            salvar_tarefas()
            break
        else:
            print("Opção inválida.\n")

# --- Execução ---
if __name__ == "__main__":
    carregar_tarefas()
    menu()
