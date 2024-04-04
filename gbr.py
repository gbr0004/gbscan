import requests
from termcolor import colored
import ipaddress
import random

def generate_random_ip():
    # Gera um endereço IP aleatório
    return colored(str(ipaddress.IPv4Address(random.randint(0, 2**32 - 1))), 'red')

def check_sql_injection(url):
    try:
        payload = "'"
        response = requests.get(url + payload)
        response.raise_for_status()
        if "SQL syntax" in response.text:
            return colored("Vulnerabilidade de SQL DETECTADA!!", 'green')
        return colored("Nenhuma vulnerabilidade de SQL detectada.", 'red')
    except requests.exceptions.RequestException as e:
        return colored(f"Erro na solicitação: {str(e)}", 'red')

def check_xss(url):
    try:
        payload = "<script>alert('XSS')</script>"
        response = requests.get(url, params={"input": payload})
        response.raise_for_status()
        if payload in response.text:
            return colored("XSS vulnerabilidade DETECTADA!", 'green')
        return colored("Nenhuma vulnerabilidade de XSS detectada", 'red')
    except requests.exceptions.RequestException as e:
        return colored(f"Erro na solicitação: {str(e)}", 'red')

def check_csrf(url):
    csrf_token = ""
    try:
        response = requests.get(url)
        response.raise_for_status()
        if "csrf_token" in response.text:
            csrf_token = response.text.split("csrf_token = ")[1].split(";")[0]
    except requests.exceptions.RequestException as e:
        return colored(f"Erro ao obter o token CSRF: {str(e)}", 'red')

    if csrf_token:
        payload = {"csrf_token": csrf_token}
        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            if "CSRF token invalido" not in response.text:
                return colored("CSRF vulnerabilidade DETECTADA!", 'green')
        except requests.exceptions.RequestException as e:
            return colored(f"Erro na solicitação POST: {str(e)}", 'red')
    return colored("Nenhuma vulnerabilidade CSRF detectada", 'red')

def check_ssrf(url):
    try:
        payload = "http://localhost"
        response = requests.get(url, params={"input": payload})
        response.raise_for_status()
        if "Error connecting" not in response.text:
            return colored("SSRF vulnerabilidade DETECTADA!", 'green')
        return colored("Nenhuma vulnerabilidade de SSRF detectada.", 'red')
    except requests.exceptions.RequestException as e:
        return colored(f"Erro na solicitação: {str(e)}", 'red')

def check_lfi(url):
    try:
        payload = "../../../etc/passwd"
        response = requests.get(url, params={"file": payload})
        response.raise_for_status()
        if "root:" in response.text:
            return colored("Vulnerabilidade LFI DETECTADA", 'green')
        return colored("Nenhuma vulnerabilidade LFI detectada", 'red')
    except requests.exceptions.RequestException as e:
        return colored(f"Erro na solicitação: {str(e)}", 'red')

def check_rce(url):
    try:
        payload = ";ls"
        response = requests.get(url, params={"input": payload})
        response.raise_for_status()
        if "bin" in response.text:
            return colored("Vulnerabilidade RCE DETECTADA!", 'green')
        return colored("Nenhuma vulnerabilidade RCE detectada.", 'red')
    except requests.exceptions.RequestException as e:
        return colored(f"Erro na solicitação: {str(e)}", 'red')

def scan_website(url):
    print(f"\nVarrendo: {url}")
    print(check_sql_injection(url))
    print(check_xss(url))
    print(check_csrf(url))
    print(check_ssrf(url))
    print(check_lfi(url))
    print(check_rce(url))

# URL do seu Telegram (substitua com o seu link real)
telegram_link = "https://t.me/gbr0004"

def main_menu():
    print("\nMenu Principal:")
    print("1. Realizar nova varredura")
    print("2. Varredura em lote a partir de arquivo .txt")
    print("3. Sair do programa")

def perform_batch_scan(file_name):
    try:
        with open(file_name, 'r') as file:
            urls = file.read().splitlines()

        for url in urls:
            # Verifica se o link é válido antes de realizar a varredura
            if is_valid_url(url):
                scan_website(url)
            else:
                print(f"Link inválido: {url}")
    except FileNotFoundError:
        print("Arquivo não encontrado.")
    except Exception as e:
        print(f"Erro ao realizar a varredura em lote: {str(e)}")

def is_valid_url(url):
    return url.startswith("http://") or url.startswith("https://")

def main():
    art = f'''
     ██████╗ ██████╗ ██████╗ 
    ██╔════╝ ██╔══██╗██╔══██╗
    ██║  ███╗██████╔╝██████╔╝
    ██║   ██║██╔══██╗██╔══██╗
    ╚██████╔╝██████╔╝██║  ██║
     ╚═════╝ ╚═════╝ ╚═╝  ╚═╝
        
    Link do Telegram: {https://t.me/redsecgb}
    SEU IP: {generate_random_ip()}
    '''

    print(art)

    while True:
        main_menu()
        opcao = input("Escolha uma opção (1, 2 ou 3): ")

        if opcao == '1':
            user_url = input("Digite o URL do site:  ")
            try:
                print("\nVarrendo...")
                scan_website(user_url)
            except:
                print("Algo deu errado. Verifique o URL e tente novamente.")
        elif opcao == '2':
            file_name = input("Digite o nome do arquivo .txt: ")
            print("\nVarrendo em lote...")
            perform_batch_scan(file_name)
        elif opcao == '3':
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
