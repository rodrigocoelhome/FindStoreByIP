import subprocess
import re
import csv

# Nome do arquivo que contém a lista de IPs
arquivo_entrada = "ips.txt"
arquivo_saida = "resultado_ping.csv"

# Função para carregar os IPs do arquivo
def carregar_ips(arquivo):
    try:
        with open(arquivo, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo}' não foi encontrado.")
        return []

# Função para executar o ping e capturar o número da loja
def get_store_number(ip):
    try:
        # Executa o ping -a no Windows com shell=True e timeout aumentado
        result = subprocess.run(f"ping -a {ip}", capture_output=True, text=True, timeout=10, shell=True)
        output = result.stdout

        # Expressão regular para capturar **apenas os 4 dígitos após "LJ"**
        match = re.search(r"LJ(\d{4})", output)

        if match:
            return match.group(1)  # Retorna apenas os 4 dígitos
        else:
            return "Desconhecido"
    except subprocess.TimeoutExpired:
        return "Timeout"
    except Exception as e:
        return f"Erro: {str(e)}"

# Carregar a lista de IPs do arquivo
ips = carregar_ips(arquivo_entrada)

if not ips:
    print("Nenhum IP encontrado no arquivo. Verifique o conteúdo de 'ips.txt'.")
else:
    # Criar uma lista com os resultados
    results = []
    for ip in ips:
        store_number = get_store_number(ip)
        results.append((ip, store_number))
        print(f"{ip} -> Loja: {store_number}")

    # Salvar os resultados em um arquivo CSV
    with open(arquivo_saida, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["IP", "Número da Loja"])
        writer.writerows(results)

    print(f"Resultados salvos em '{arquivo_saida}'")
