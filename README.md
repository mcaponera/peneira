# peneira
raspador dos campeonatos nacionais de futebol de mulheres, usando `python` e o framework [`scrapy`](https://docs.scrapy.org/en/latest/index.html), a ideia inicial é atualizar gradualmente o link das súmulas de 2024 na Wikipedia da série A1 do brasileirão que estão quebrados (e talvez construir uma api 🙈).


| páginas de interesse | url |
| - | - |
| principal | https://portaldegovernanca.cbf.com.br/documentos-da-partida |
| `/campeonato/{ano}` | https://portaldegovernanca.cbf.com.br/documentos-da-partida/campeonatos/2021 |
| `rodadas/{id_campeonato}/{ano}` | https://portaldegovernanca.cbf.com.br/documentos-da-partida/rodadas/12503/2021 |
| `getAll/{rodada}/{id_campeonato}/{ano}` | https://portaldegovernanca.cbf.com.br/documentos-da-partida/getAll/1/12503/2021 |

## das configurações
algumas configurações são necessárias para o servidor aceitar as requisições feitas pelo `scrapy`, em especial `USER_AGENT` e `DEFAULT_REQUEST_HEADERS`, o  [htttpbin.org/headers](https://httpbin.org/headers) pode ajudar nisso, não pesar a mão na quantidade de requisições e no tempo entre elas também é interessante (`DOWNLOAD_DELAY`, `CONCURRENT_REQUESTS`, `CONCURRENT_REQUESTS_PER_DOMAIN`), habilitar o AutoThrottle é importante

## estrutura das páginas e o escopo da raspagem
usando 
```python
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
 a resposta de `'https://portaldegovernanca.cbf.com.br/documentos-da-partida/campeonatos/{ano}'` é um json

```python
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
a próxima url é formada por: `<url-principal>/rodadas/{id_campeonato}/{ano}` e tem como resposta:

```
[{'Rodada': 1},
 {'Rodada': 2},
 {'Rodada': 3},
 {'Rodada': 4},
 {'Rodada': 5},
 {'Rodada': 6}]

```
a última url é formada da seguinte maneira `<url-principal>/getAll/{rodada}/{id_campeonato}/{ano}` e retorna um json:

```python
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
dessa forma temos a maior parte dos itens de interesse mapeados. temos os padrões para a formação das urls, e as informações que queremos recuperar. o objetivo é iterar sobre as informações disponíveis sobres todos os campeonatos de times profissionais até sub-17 de futebol de mulheres.

```json
1: {id_campeonato: 12583, Campeonato_Categoria: "Brasileiro Feminino - A1"}
2: {id_campeonato: 12588, Campeonato_Categoria: "Brasileiro Feminino - A2"}
3: {id_campeonato: 12592, Campeonato_Categoria: "Brasileiro Feminino - A3"}
4: {id_campeonato: 12597, Campeonato_Categoria: "Brasileiro Feminino - Sub-17"}
5: {id_campeonato: 12579, Campeonato_Categoria: "Brasileiro Feminino - Sub-20"}
22: {id_campeonato: 12590, Campeonato_Categoria: "Liga de Desenvolvimento - Sub-14 Feminino"}
23: {id_campeonato: 12591, Campeonato_Categoria: "Liga de Desenvolvimento - Sub-16 Feminino"}
24: {id_campeonato: 12576, Campeonato_Categoria: "Supercopa do Brasil - Feminino"}
```

## estrutura
