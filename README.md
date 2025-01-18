# raspador
| páginas de interesse | url |
| - | - |
| principal | https://portaldegovernanca.cbf.com.br/documentos-da-partida |
| `/campeonato/{ano}` |https://portaldegovernanca.cbf.com.br/documentos-da-partida/campeonatos/2021 |
| `rodadas/{id_campeonato}/{ano}` | https://portaldegovernanca.cbf.com.br/documentos-da-partida/rodadas/12503/2021 |
| `getAll/{rodada}/{id_campeonato}/{ano}` | https://portaldegovernanca.cbf.com.br/documentos-da-partida/getAll/1/12503/2021 |

## explorando 
```python
anos_req = requests.get('https://portaldegovernanca.cbf.com.br/documentos-da-partida')
anos_lista = anos_req.xpath("//div[2]/div[2]/div/form/div/div/select[@id='ano']/option/text()").extract()
# out:  `['Todos os anos', '2025', '2024', '2023', '2022', '2021']`

anos_lista = []
for ano in anos:
    if ano.isdigit():
        anos_lista.append(ano)
```

 a resposta de `'https://portaldegovernanca.cbf.com.br/documentos-da-partida/campeonatos/{ano}'` é um json
```python
competicoes_{ano} = json.loads(response.text)

# out:  
#    {
#           'Campeonato_Categoria': 'Amistoso - Seleção Brasileira Feminina',
#           'id_campeonato': 12503
#    },

```
a próxima url é formada por: `<url-principal>/rodadas/{id_camponato}/{ano}` e tem como resposta:

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
#Out[80]: dict_keys(['dados', 'conteudo_url'])
jogos['dados'][1].keys()
#Out[81]: dict_keys(['TimeNomeMandante', 'TimeNomeVisitante', 'UFTimeMandante', 'UFTimeVisitante', 'Resultado', 'Jogo_DataOri', 'Horario', 'Num_Jogo', 'Rodada', 'EstadioNomePopular', 'UFEstadio', 'MunicipioEstadio', 'Codigo_Campeonato', 'Codigo_Categoria', 'url_sumula', 'url_boletim', 'url_rdj', 'function_js'])
jogos['dados'][1]
#Out[90]: 
#    {'TimeNomeMandante': 'Chile',
#    'TimeNomeVisitante': 'Venezuela',
#    'UFTimeMandante': None,
#    'UFTimeVisitante': None,
#    'Resultado': '- x -',
#    'Jogo_DataOri': '25/11/2021',
#    'Horario': '18:00',
#    'Num_Jogo': 3,
#    'Rodada': 1,
#    'EstadioNomePopular': 'Arena da Amazônia',
#    'UFEstadio': 'AM',
#    'MunicipioEstadio': 'Manaus',
#    'Codigo_Campeonato': 1000,
#    'Codigo_Categoria': 67,
#    'url_sumula': '',
#    'url_boletim': '',
#    'url_rdj': '',
#    'function_js': 'onclick="docNaoPublicado();"'}
```
