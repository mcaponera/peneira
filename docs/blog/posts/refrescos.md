---
draft: true 
date: 2024-01-24 
categories:
  - desenvolvimento
tags:
  - pandas
authors:
  - mcaponera
---

# finalmente os refrescos

bom depois de raspar todas as páginas possíveis e todos os dados, algumas coisa vão ficando mais evidentes.

=== "'primera versão de `parser_year`'"

    ```py linenums='27'
        def parse_year(self, response):
        year = response.meta['year']
        contests_ = json.loads(response.text)
        contests = [
            (contest['id_campeonato'], contest['Campeonato_Categoria'])
            for contest in contests_
        ]
        # precisamos filtrar os campeonatos que possuam (r'(?i)\bfeminin')

        for i in contests:
            
            id = i[0]
            tournament_name = i[1]
            next_url = urljoin(
                response.url, f'/documentos-da-partida/rodadas/{id}/{year}'
            )

            yield scrapy.Request(
                url=next_url,
                callback=self.parse_contest,
                meta={
                    'year': year,
                    'id': id,
                    'tournament_name': tournament_name,
                },
            )
    ```

=== "'segunda versão `parser_year`'"

    ```py linenums='27'
      (r'(?i)\bfeminin')
    ```

aqui tem informações redundantes.

=== "primeira versão de `parser_turn()`"

      ```py linenums='75'
          def parse_turn(self, response):
              year = response.meta['year']
              id = response.meta['id']
              tournament_name = response.meta['tournament_name']
              games_ = response.json()

              for game in games_['dados']:
                  match = re.search(r'onclick="(\w+)\(\);"', game['function_js'])
                  function_name = match.group(1) if match else 'sim'
                  date_text = game['Jogo_DataOri']
                  date = datetime.datetime.strptime(date_text, '%d/%m/%Y').date()
                  year_date = datetime.datetime.strptime(str(year), '%Y').date()
                  time_text = game['Horario']
                  time = datetime.datetime.strptime(time_text, '%H:%M').time()

                  yield {
                      'ano': year_date,
                      'id_url': id,
                      'campeonato': tournament_name,
                      'id_campeonato': game['Codigo_Campeonato'],
                      'cod_categoria': game['Codigo_Categoria'],
                      'time_mandante': game['TimeNomeMandante'],
                      'time_visitante': game['TimeNomeVisitante'],
                      'time_mandante_UF': game['UFTimeMandante'],
                      'time_visitante_UF': game['UFTimeVisitante'],
                      'resultado': game['Resultado'],
                      'data_jogo': date,
                      'hora_jogo': time,
                      'num_jogo': game['Num_Jogo'],
                      'rodada': game['Rodada'],
                      'estadio': game['EstadioNomePopular'],
                      'estadio_UF': game['UFEstadio'],
                      'estadio_municipio': game['MunicipioEstadio'],
                      'url_sumula': game['url_sumula'],
                      'url_boletim': game['url_boletim'],
                      'url_rdj': game['url_rdj'],
                      'publicado': function_name,
                  }
      ```

=== "segunda versão de `parser_turn()`"

    ```py linenums='75'
        def parse_turn(self, response):
            year = response.meta['year']
            id = response.meta['id']
            tournament_name = response.meta['tournament_name']
            games_ = response.json()

            for game in games_['dados']:
                date_text = game['Jogo_DataOri']
                date = datetime.datetime.strptime(date_text, '%d/%m/%Y').date()
                year_date = datetime.datetime.strptime(str(year), '%Y').date()
                time_text = game['Horario']
                time = datetime.datetime.strptime(time_text, '%H:%M').time()

                yield {
                    'ano': year_date,
                    'id_url': id,
                    'campeonato': tournament_name,
                    'id_campeonato': game['Codigo_Campeonato'],
                    'cod_categoria': game['Codigo_Categoria'],
                    'time_mandante': game['TimeNomeMandante'],
                    'time_visitante': game['TimeNomeVisitante'],
                    'time_mandante_UF': game['UFTimeMandante'],
                    'time_visitante_UF': game['UFTimeVisitante'],
                    'resultado': game['Resultado'],
                    'data_jogo': date,
                    'hora_jogo': time,
                    'num_jogo': game['Num_Jogo'],
                    'rodada': game['Rodada'],
                    'estadio': game['EstadioNomePopular'],
                    'estadio_UF': game['UFEstadio'],
                    'estadio_municipio': game['MunicipioEstadio'],
                    'url_sumula': game['url_sumula'],
                    'url_boletim': game['url_boletim'],
                    'url_rdj': game['url_rdj'],
                }
    ```