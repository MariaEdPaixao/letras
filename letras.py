import requests
import os

#******* INTEGRANTES *******
# Laura de Oliveira Cintra - RM: 558843
# Maria Eduarda Alves da Paixão - RM: 558832
# Vinicius Saes - RM: 554456

#******* SOBRE A API VAGALUME *******
"""
 A API do Vagalume permite buscar letras de músicas, informações de artistas e, quando disponível, obter traduções
de músicas para o português, oferecendo uma maneira fácil de acessar conteúdos musicais.

"""

#******* RESPONSE/RETORNO DA API *******
"""
- letras da música:
"mus" : [{'id': 'id_da_musica', 'name': 'nome_da_musica', 'url': 'url_do_site_vagalume_com_a_musica', 'lang': 'idioma_da_musica (1 - PT/ 2- EN, P. EX)', 'text' = 'letra_da_musica_completa'}]

- tradução de músicas (se tiver):
"translate": [{'id': 'id_da_traducao', 'lang': 'idioma_da_traducao', 'url': 'url_do_site_vagalume_com_a_musica', 'text': 'musica_completa_traduzida'}]

- informações do artista:
'art': {'id': 'id_do_artista', 'name': 'nome_do_artista', 'url': 'url_do_site_vagalume_com_o_artista'}

-status da requisição:
'type': 'exact' -> se foi encontrada | 'type': 'notfound' -> se não foi encontrada
"""

# Faz uma requisição na api vagalume
# Parâmetro 1: artista -> str: nome do artista que será buscado na API 
# Parâmetro 2: nome_musica -> str: nome da música que será buscada na API 
# Parâmetro 3: api_key -> str: chave única de acesso para a API (adquirida no cadastro do site)
# Retorno: dict ou (|) None
def buscar_letra(artista: str, nome_musica: str, api_key: str) -> dict | None:
    # URL da API Vagalume
    endpoint = f"https://api.vagalume.com.br/search.php?art={artista}&mus={nome_musica}&apikey={api_key}"
    response = requests.get(endpoint)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro: {response.status_code} - {response.reason}")
        return None

# Verifica se nos dados passados pelo json a música foi encontrada
# Parâmetro 1: data -> dict: dicionário com as informações da resposta da API
# Retorno: bool
def musica_encontrada(data: dict) -> bool:
    tipo = data.get('type') # o get retorna o valor do item se ele existir, nesse caso retorna o valor de 'type'

    if tipo == 'exact':
        return True  # Encontrou
    else:
        return False  # Não encontrou
    
# Exibe a letra da música
# Parâmetro 1: data -> dict: dicionário com as informações da resposta da API
# Retorno: None
def exibir_letra(data: dict) -> None:
    for musica in data['mus']:
        letra = musica['text']    
        print(f"""\n=== {musica['name']} ===\n\n{letra}""")

# Verifica se nos dados passados pelo json existe uma tradução para a música
# Parâmetro 1: data -> dict: dicionário com as informações da resposta da API
# Retorno: bool
def verifica_traducao(data: dict) -> bool:
    if 'translate' in data['mus'][0]:
           return True
    return False

# Exibe a tradução da música
# Parâmetro 1: data -> dict: dicionário com as informações da resposta da API
# Retorno: None
def exibir_traducao(data: dict) -> None:
        traducao = data['mus'][0]['translate'][0]['text']
        print(f"\nTradução para português:\n\n== {data["mus"][0]["name"]} ==\n\n{traducao}")

# Apaga a tela, verificando o sistema operacional
# Retorno: None
def apaga_tela() -> None:
    os.system("cls" if os.name == "nt" else "clear")

# Exibe uma mensagem formatada.
# Parâmetro 1: carac -> str: O caractere que formará a mensagem
# Parâmetro 2: msg -> str: A mensagem que será exibida
# Retorno: None
def mensagem(carac:str, msg: str) -> None:
    tamanho = len(msg)
    print(f"\n{carac * tamanho}")
    print(msg)
    print(f"{carac * tamanho}")

# --------------- PROGRAMA PRINCIPAL


key = "330ac562342e051baba3befa6492a3b8"
apaga_tela()

print("\n=== Bem-vindo(a)! Digite o artista e a música para ver a letra e, se disponível, a tradução. Aproveite! ===")

exibir = True
while exibir:
    artista = input("\nDigite o nome completo do artista: ")
    nome_musica = input("Digite o nome da música: ")

    informacoes = buscar_letra(artista, nome_musica, key)
    
    apaga_tela()

    if musica_encontrada(informacoes):
        exibir_letra(informacoes)

        if verifica_traducao(informacoes):
            while True:
                mensagem("=", "Tradução disponível, deseja ver? [S]im ou [N]ão:")
                opcao = input("").upper()
                if opcao == "S":
                    apaga_tela()
                    exibir_traducao(informacoes)
                    break
                elif opcao == "N":
                    break
                else:
                    print("\nOpção inválida (S ou N)")
        else:
            mensagem("=", "Tradução não disponível.")

    else:
        print("== Música não encontrada! ==")

    while True:
            mensagem("=", "Quer pesquisar outra música? [S]im ou [N]ão: ")
            opcao = input().upper()
            if opcao == "S":
                apaga_tela()
                break
            elif opcao == "N":
                exibir = False
                break
            else:
                print("\nOpção inválida (S ou N)")

else:
    apaga_tela()
    mensagem("=","Agradecemos por usar nosso sistema! :)")

# música internacional -> no json, aparece a chave "translate", pois há tradução, e no indice 0 tem informações como id da tradução, entre outras, uma delas é a chave "text" que o value é o texto da tradução
# música nacional -> no json, não aparece a chave "translate", pois já está em português
