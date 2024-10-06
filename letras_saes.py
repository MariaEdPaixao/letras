import requests
import os

#******* INTEGRANTES *******
# Laura de Oliveira Cintra - RM: 558843
# Maria Eduarda Alves da paixão - RM: 558832
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

- lang (O idioma da música encontrada). 
1 (Português Brasil), 2 (Inglês), 3 (Espanhol), 4 (Francês), 5 (Alemão), 6 (Italiano), 7 (Holandês), 8 (Japonês), 9 (Português Portugal). O valor 999999 é reservado para "Outros".
"""

# Faz uma requisição na api vagalume
# Parâmetro 1: artista -> str: nome do artista que será buscado na API 
# Parâmetro 2: nome_musica -> str: nome da música que será buscada na API 
# Parâmetro 3: api_key -> str: chave única de acesso para a API (adquirida no cadastro do site)
# Retorno: dict
def buscar_letra(artista: str, nome_musica: str, api_key: str) -> dict:
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
        print("A música não foi encontrada.")
        return False  # Não encontrou
    
# Exibe a letra da música
# Parâmetro 1: data -> dict: dicionário com as informações da resposta da API
# Retorno: None
def exibir_letra(data: dict) -> None:
    if musica_encontrada(data):
        for musica in data['mus']:
            idioma = 1
            apaga_tela()
            traducao = musica.get('translate', False)
            if traducao:
                idioma = define_idioma(musica)
                apaga_tela()
                if idioma > 1 and idioma <= 9:
                    traducao = musica['translate']
                    letra = traducao[idioma-2]['text']
                    print(f"""\n=== {musica['name']} ===\n\n{letra}""")
                else:
                    letra = musica['text']
                    print(f"""\n=== {musica['name']} ===\n\n{letra}""")
            else:
                letra = musica['text']
                print(f"""\n=== {musica['name']} ===\n\n{letra}""")
    else: 
        print("Letra não encontrada.")
        
        
def define_idioma(musica:dict) -> None:
    dicionario_idiomas = {
        1 : "Português Brasil",
        2 : "Inglês",
        3 : "Espanhol",
        4 : "Francês",
        5 : "Alemão",
        6 : "Italiano",
        7 : "Holandês",
        8 : "Japonês",
        9 : "Português Portugal",
    }
    traducoes = musica.get("translate")
    while True:
        if len(traducoes) > 1:
            try:
                print("Esoclha o idioma da letra: ")
                print(f"{1} - {dicionario_idiomas[musica["lang"]]} (Original)\n")
                for i in range(0, len(traducoes), 1):
                    print(f"{i+2} - {dicionario_idiomas[traducoes[i]["lang"]]}\n")
                idioma = int(input("Escolha: "))
                if 1 <= idioma <= 9:
                    
                    return idioma
                else:
                    apaga_tela()
                    print("**Opção inválida! digite novamente**\n")
            except:
                apaga_tela()
                print("**Opção inválida! digite novamente**\n")
        else:
            try:
                idioma = int(input(f"""Escolha o idioma da letra: \n1 - {dicionario_idiomas[musica["lang"]]} (Original) \n2 - {dicionario_idiomas[traducoes[0]["lang"]]} \nEscolha: """))
                if 1 <= idioma <= 2:
                    return idioma
                else:
                    apaga_tela()
                    print("**Opção inválida! digite novamente**\n")
            except:
                apaga_tela()
                print("**Opção inválida! digite novamente**\n")

# Apaga a tela, verificando o sistema operacional
# Retorno: None
def apaga_tela() -> None:
    os.system("cls" if os.name == "nt" else "clear")

# --------------- PROGRAMA PRINCIPAL


key = "330ac562342e051baba3befa6492a3b8"
apaga_tela()

print("\n=== Bem-vindo(a)! Digite o artista e a música para ver a letra e, se disponível, a tradução. Aproveite! ===")

exibir = True
while exibir:
    apaga_tela()
    artista = input("\nDigite o nome completo do artista: ")
    nome_musica = input("Digite o nome da música: ")

    data = buscar_letra(artista, nome_musica, key)
    
    apaga_tela()
    if musica_encontrada(data):
        exibir_letra(data)
        # exibir_traducao(data)
        
    else:
        print("Artista ou música inválidos.")

    while True:
            print("------------------------------------------------------------------")
            opcao = input("\nQuer pesquisar outra música? [S]im ou [N]ão: ").upper()
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
    print("\nAgradecemos por usar nosso sistema! :)")

buscar_letra( "twenty one pilots", "Doubt", key) # no json, aparece a chave "translate", pois há tradução, e no indice 0 tem informações como id da tradução, entre outras, uma delas é a chave "text" que o value é o texto da tradução

buscar_letra( "3030", "Vai lá", key) # no json, não aparece a chave "translate", pois já está em português
