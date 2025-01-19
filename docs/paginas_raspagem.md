# estrutura das páginas e o escopo da raspagem

## páginas de interesse

navegando pelo site e com a ajuda do devtools, conseguimos identificar como as urls são montadas dinamicamente, a seguir a lista com as urls que precisamos montar:

| páginas de interesse | url |
| - | - |
| principal | https://portaldegovernanca.cbf.com.br/documentos-da-partida |
| `/campeonato/{ano}` | https://portaldegovernanca.cbf.com.br/documentos-da-partida/campeonatos/2021 |
| `rodadas/{id_campeonato}/{ano}` | https://portaldegovernanca.cbf.com.br/documentos-da-partida/rodadas/12503/2021 |
| `/getAll/{rodada}/{id_campeonato}/{ano}` | https://portaldegovernanca.cbf.com.br/documentos-da-partida/getAll/1/12503/2021 |

## `/documentos-da-partida`

```py title="lógica da extração" 
anos_req = requests.get('https://portaldegovernanca.cbf.com.br/documentos-da-partida')
anos_lista = anos_req.xpath(
    "//div[2]/div[2]/div/form/div/div/select[@id='ano']/option/text()"
    ).extract()

# Out[73]  `['Todos os anos', '2025', '2024', '2023', '2022', '2021']`

anos_lista = []
for ano in anos:
    if ano.isdigit():
        anos_lista.append(int(ano))
```
assim podemos construir a próxima url.

## `/documentos-da-partida/campeonatos/{ano}`

```py title="lógica de extração"
competicoes = json.loads(response.text)

# Out[75]:  
#    {
#           'Campeonato_Categoria': 'Amistoso - Seleção Brasileira Feminina',
#           'id_campeonato': 12503
#    },

info_campeonatos = [(competicoes['id_campeonato'], competicoes['Campeonato_Categoria']) for competicoe in competicoes]
print(info_campeonatos)
# Out[76]:
# [(12502, 'Amistoso - Seleção Brasileira de Futsal'), (12503, 'Amistoso - Seleção Brasileira Feminina'), ...]
```

## `rodadas/{id_campeonato}/{ano}` 

``` title="texto do response"
[{'Rodada': 1},
 {'Rodada': 2},
 {'Rodada': 3},
 {'Rodada': 4},
 {'Rodada': 5},
 {'Rodada': 6}]

```
## `getAll/{rodada}/{id_campeonato}/{ano}`

a última url é formada da seguinte maneira `<url-principal>/getAll/{rodada}/{id_campeonato}/{ano}` e retorna um json com as informações que queremos:

```py title="resposta final"
jogos.keys()

# Out[80]: dict_keys(['dados', 'conteudo_url'])

jogos['dados'][1].keys()

# Out[81]: dict_keys(
#       [
#           'TimeNomeMandante', 
#           'TimeNomeVisitante', 
#           'UFTimeMandante', 
#           'UFTimeVisitante', 
#           'Resultado', 
#           'Jogo_DataOri', 
#           'Horario', 
#           'Num_Jogo', 
#           'Rodada', 
#           'EstadioNomePopular', 
#           'UFEstadio', 
#           'MunicipioEstadio', 
#           'Codigo_Campeonato', 
#           'Codigo_Categoria', 
#           'url_sumula', 
#           'url_boletim', 
#           'url_rdj', 
#           'function_js'
#       ]
#   )


jogos['dados'][1]

#Out[90]: 
#   {
#       'TimeNomeMandante': 'Chile',
#       'TimeNomeVisitante': 'Venezuela',
#       'UFTimeMandante': None,
#       'UFTimeVisitante': None,
#       'Resultado': '- x -',
#       'Jogo_DataOri': '25/11/2021',
#       'Horario': '18:00',
#       'Num_Jogo': 3,
#       'Rodada': 1,
#       'EstadioNomePopular': 'Arena da Amazônia',
#       'UFEstadio': 'AM',
#       'MunicipioEstadio': 'Manaus',
#       'Codigo_Campeonato': 1000,
#       'Codigo_Categoria': 67,
#       'url_sumula': '',
#       'url_boletim': '',
#       'url_rdj': '',
#       'function_js': 'onclick="docNaoPublicado();"'
#   }
```
dessa forma temos a maior parte dos itens de interesse mapeados. temos os padrões para a formação das urls, e as informações que queremos recuperar.