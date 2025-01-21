# lógica de raspagem

com todas as url mapeadas e conhecendo os dados é hora de montar uma estratégia de raspagem. usando geradores dentro das funções da classe `PeneiraoSpider`, assim as urls são montadas com as informações dos geradores anteriores até onde estão as informações que serão extraídas.

## selecionando os campeonatos
como o objetivo não é extraír informação de todos os campeonatos disponíveis, precisamos filtrar os dados que são extraídos na função `parse_years`

```py title='peneirao_spider.py' linenums='35'
for i in contests:
           id = i[0]
           tournament_name = i[1]
           next_url = urljoin(
               response.url, f'/documentos-da-partida/rodadas/{id}/{year}'
           )
```
