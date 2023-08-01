import tkinter as tk
from tkinter import messagebox
import pandas as pd
import json
from tkinter import ttk, messagebox
from datetime import datetime
import random
import string
from functools import partial

root = tk.Tk()
root.title("CRM MIS")


def main():


    # Interface de Login
    root.iconbitmap(r"C:\Users\lucas.santos\Desktop\CRM\src\logo_dbm_gr_8jK_icon.ico")
    login_frame = tk.Frame(root)
    login_frame.pack(padx=100, pady=100)
    
    lbl_username = tk.Label(login_frame, text="Usuário:")
    lbl_username.pack()

    entry_username = tk.Entry(login_frame)
    entry_username.pack()

    lbl_password = tk.Label(login_frame, text="Senha:")
    lbl_password.pack()

    entry_password = tk.Entry(login_frame, show="*")
    entry_password.pack()

    btn_login = tk.Button(login_frame, text="Login", command=lambda: login(entry_username.get(), entry_password.get()))
    btn_login.pack()

    root.mainloop()


def login(username, password):
    # Abra o arquivo JSON para leitura
    with open("users.json", "r") as file:
        users_data = json.load(file)

    # Verifique as credenciais do usuário com base no arquivo JSON
    for user in users_data["users"]:
        
        if user["matricula"] == username and user["senha"] == password:
            messagebox.showinfo("Login", "Login bem-sucedido!")
            global login_usuario
            login_usuario = user["matricula"]
            root.destroy()
            tela_inicial()
            return

    messagebox.showerror("Login", "Usuário ou senha incorretos.")

def tela_inicial():
    root = tk.Tk()
    root.iconbitmap(r"C:\Users\lucas.santos\Desktop\CRM\src\logo_dbm_gr_8jK_icon.ico")
    root.title("Tela de Comando")
    root.state("zoomed")

    #cadastrar novo usuario
    btn_cadastrar_usuario = tk.Button(root, text="Cadastrar Novo Usuário", command=cadastrar_usuario)
    btn_cadastrar_usuario.pack(pady=20)
    

    # Crie a interface da tela inicial do CRM
    # Adicione componentes e funcionalidades conforme os requisitos

    root.mainloop()


def cadastrar_usuario():
    # Crie uma nova janela para o formulário de cadastro de usuário
    janela_cadastro = tk.Toplevel()
    janela_cadastro.title("Cadastro de Novo Usuário")

    # Componentes do formulário de cadastro
    lbl_email = tk.Label(janela_cadastro, text="E-mail:")
    lbl_email.pack()

    entry_email = tk.Entry(janela_cadastro)
    entry_email.pack()

    lbl_matricula = tk.Label(janela_cadastro, text="Matrícula:")
    lbl_matricula.pack()

    entry_matricula = tk.Entry(janela_cadastro)
    entry_matricula.pack()

    lbl_nome = tk.Label(janela_cadastro, text="Nome Completo:")
    lbl_nome.pack()

    entry_nome = tk.Entry(janela_cadastro)
    entry_nome.pack()

    lbl_nivel_acesso = tk.Label(janela_cadastro, text="Nível de Acesso:")
    lbl_nivel_acesso.pack()

    # Campo SelectBox (ComboBox) para Nível de Acesso
    combo_nivel_acesso = ttk.Combobox(janela_cadastro, values=["Administrador", "Usuário"])
    combo_nivel_acesso.pack()

    # Botão de Salvar Cadastro
    btn_salvar = tk.Button(janela_cadastro, text="Salvar", command=partial(salvar_cadastro, entry_email.get(), entry_matricula.get(), entry_nome.get(), combo_nivel_acesso.get(), janela_cadastro))  # Utilize a função partial para passar o argumento adicional
    btn_salvar.pack()



def salvar_cadastro(email, matricula, nome, nivel_acesso, janela_cadastro):
    with open("users.json", "r") as file:
        users_data = json.load(file)
        senha_aleatoria = str(gerar_senha_aleatoria())

    # Obtenha o último ID na lista de usuários (caso exista algum usuário cadastrado)
    last_user = users_data["users"][-1] if users_data["users"] else None
    last_id = last_user["id"] if last_user else 0

    # Gere um novo ID para o usuário atual
    new_id = last_id + 1

    # Adicione a data e hora atual
    data_hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Adicione as informações do novo usuário ao dicionário, incluindo o ID, a data, hora e login do usuário cadastrante
    novo_usuario = {
        "id": new_id,
        "email": email,
        "matricula": matricula,
        "senha": senha_aleatoria,
        "nome": nome,
        "nivel_acesso": nivel_acesso,
        "data_hora_cadastro": data_hora_atual,
        "login_cadastrante": login_usuario
    }

    # Adicione o novo usuário à lista de usuários
    users_data["users"].append(novo_usuario)

    # Abra o arquivo JSON para escrita e salve os dados atualizados
    with open("users.json", "w") as file:
        json.dump(users_data, file, indent=4)

    # Exiba uma caixa de diálogo de informação informando que o cadastro foi salvo com sucesso
    messagebox.showinfo("Cadastro de Usuário", "Novo Usuário Cadastrado com Sucesso!")
    janela_cadastro.destroy()

def gerar_senha_aleatoria():
    caracteres = string.ascii_letters + string.digits  # Caracteres contendo letras e números
    senha = ''.join(random.choice(caracteres) for _ in range(6))  # Gera uma senha de 6 dígitos
    return senha



if __name__ == "__main__":
    main()
