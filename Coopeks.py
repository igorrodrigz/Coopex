import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

def autenticar_usuario():
    usuario = usuario_var.get()
    senha = senha_var.get()

    # Implemente sua lógica de autenticação aqui
    # Por exemplo, verificar se o usuário e senha estão corretos
    if usuario == 'admin' and senha == 'senha123':
        criar_interface_principal()
    else:
        messagebox.showerror('Erro de Autenticação', 'Usuário ou senha incorretos.')


# Função para cadastrar um cliente no banco de dados
def cadastrar_cliente():
    nome = nome_var.get()
    endereco = endereco_var.get()
    telefone = telefone_var.get()
    email = email_var.get()

    if nome and endereco and telefone and email:
        cursor.execute('INSERT INTO clientes (nome, endereco, telefone, email) VALUES (?, ?, ?, ?)',
                       (nome, endereco, telefone, email))
        conn.commit()
        messagebox.showinfo('Cadastro de Cliente', 'Cliente cadastrado com sucesso!')
        nome_var.set('')
        endereco_var.set('')
        telefone_var.set('')
        email_var.set('')
    else:
        messagebox.showwarning('Cadastro de Cliente', 'Preencha todos os campos!')

# Função para cadastrar um veículo no banco de dados
def cadastrar_veiculo():
    placa = placa_var.get()
    tipo = tipo_var.get()
    cliente = cliente_var.get()

    if placa and tipo and cliente:
        cliente_id = cursor.execute('SELECT id FROM clientes WHERE nome = ?', (cliente,)).fetchone()[0]
        cursor.execute('INSERT INTO veiculos (placa, tipo, cliente_id) VALUES (?, ?, ?)',
                       (placa, tipo, cliente_id))
        conn.commit()
        messagebox.showinfo('Cadastro de Veículo', 'Veículo cadastrado com sucesso!')
        placa_var.set('')
        tipo_var.set('')
    else:
        messagebox.showwarning('Cadastro de Veículo', 'Preencha todos os campos!')

# ... (outras funções do programa)

# Função para exibir relatórios avançados
def exibir_relatorios_avancados():
    # Implemente a lógica para gerar relatórios avançados aqui
    pass

# Função para verificar e enviar notificações de aviso prévio de vencimento
def verificar_notificacoes():
    hoje = datetime.now()
    data_vencimento = hoje + timedelta(days=7)  # Aviso prévio com 7 dias de antecedência

    mensalidades = cursor.execute('SELECT c.nome, c.email FROM clientes c JOIN veiculos v ON c.id = v.cliente_id WHERE v.data_vencimento = ?', (data_vencimento.date(),)).fetchall()

    for mensalidade in mensalidades:
        nome_cliente, email_cliente = mensalidade
        mensagem = f'Prezado(a) {nome_cliente}, sua mensalidade vencerá em 7 dias. Por favor, efetue o pagamento.'
        # Implemente o envio de e-mail ou notificação aqui (exemplo: usando biblioteca smtplib)


# Criar uma conexão com o banco de dados SQLite
conn = sqlite3.connect('coopex_database.db')
cursor = conn.cursor()

# Criar a tabela de clientes (se não existir)
cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                endereco TEXT NOT NULL,
                telefone TEXT NOT NULL,
                email TEXT NOT NULL)''')

# Criar a tabela de veículos (se não existir)
cursor.execute('''CREATE TABLE IF NOT EXISTS veiculos (
                id INTEGER PRIMARY KEY,
                placa TEXT NOT NULL,
                tipo TEXT NOT NULL,
                cliente_id INTEGER NOT NULL,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id))''')

# Criar a interface gráfica principal
root = tk.Tk()
root.title('Coopex - Controle de Mensalidades')

# Notebook para organizar as abas
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Aba de Cadastro de Clientes
aba_cadastro_clientes = ttk.Frame(notebook)
notebook.add(aba_cadastro_clientes, text='Cadastro de Clientes')

# Labels e campos de entrada para cadastrar cliente
tk.Label(aba_cadastro_clientes, text='Cadastro de Cliente').pack()

tk.Label(aba_cadastro_clientes, text='Nome:').pack()
nome_var = tk.StringVar()
tk.Entry(aba_cadastro_clientes, textvariable=nome_var).pack()

tk.Label(aba_cadastro_clientes, text='Endereço:').pack()
endereco_var = tk.StringVar()
tk.Entry(aba_cadastro_clientes, textvariable=endereco_var).pack()

tk.Label(aba_cadastro_clientes, text='Telefone:').pack()
telefone_var = tk.StringVar()
tk.Entry(aba_cadastro_clientes, textvariable=telefone_var).pack()

tk.Label(aba_cadastro_clientes, text='E-mail:').pack()
email_var = tk.StringVar()
tk.Entry(aba_cadastro_clientes, textvariable=email_var).pack()

tk.Button(aba_cadastro_clientes, text='Cadastrar Cliente', command=cadastrar_cliente).pack()

# Aba de Cadastro de Veículos
aba_cadastro_veiculos = ttk.Frame(notebook)
notebook.add(aba_cadastro_veiculos, text='Cadastro de Veículos')

# Labels e campos de entrada para cadastrar veículo
tk.Label(aba_cadastro_veiculos, text='Cadastro de Veículo').pack()

tk.Label(aba_cadastro_veiculos, text='Placa:').pack()
placa_var = tk.StringVar()
tk.Entry(aba_cadastro_veiculos, textvariable=placa_var).pack()

tk.Label(aba_cadastro_veiculos, text='Tipo:').pack()
tipo_var = tk.StringVar()
tk.Entry(aba_cadastro_veiculos, textvariable=tipo_var).pack()

tk.Label(aba_cadastro_veiculos, text='Cliente:').pack()

clientes = cursor.execute('SELECT nome FROM clientes').fetchall()
if not clientes:
    messagebox.showwarning('Aviso', 'Nenhum cliente cadastrado. Cadastre clientes antes de prosseguir.')
else:
    cliente_var = tk.StringVar(value=clientes[0][0])  # Definir o valor padrão como o primeiro cliente
    tk.OptionMenu(aba_cadastro_veiculos, cliente_var, *[cliente[0] for cliente in clientes]).pack()

tk.Button(aba_cadastro_veiculos, text='Cadastrar Veículo', command=cadastrar_veiculo).pack()

# Aba de Relatórios Avançados
aba_relatorios = ttk.Frame(notebook)
notebook.add(aba_relatorios, text='Relatórios Avançados')

# Botão para exibir relatórios avançados
tk.Button(aba_relatorios, text='Exibir Relatórios Avançados', command=exibir_relatorios_avancados).pack()

# Iniciar a execução da interface gráfica
root.mainloop()

# Fechar conexão com o banco de dados
conn.close()
