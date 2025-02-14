import json
import re
from urllib.parse import urljoin

import scrapy

from peneira.items import PeneiraItem


class PeneiraoSpider(scrapy.Spider):
    name = 'peneira'
    start_urls = [
        'https://portaldegovernanca.cbf.com.br/documentos-da-partida'
    ]

    def parse(self, response):
        years_ = response.xpath("//select[@id='ano']/option/text()").extract()
        years = [int(year) for year in years_ if year.isdigit()]

        for year in years:
            next_url = urljoin(
                response.url, f'/documentos-da-partida/campeonatos/{year}'
            )
            yield scrapy.Request(
                url=next_url, callback=self.parse_year, meta={'year': year}
            )

    def parse_year(self, response):
        year = response.meta['year']
        contests_ = json.loads(response.text)
        contests = [
            (contest['id_campeonato'], contest['Campeonato_Categoria'])
            for contest in contests_
        ]

        for i in contests:
            if re.search(r'\bfemin', i[1], re.IGNORECASE):
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

    def parse_contest(self, response):
        year = response.meta['year']
        id = response.meta['id']
        tournament_name = response.meta['tournament_name']
        turns_ = json.loads(response.text)
        turns = [turn['Rodada'] for turn in turns_]

        for turn in turns:
            next_url = urljoin(
                response.url,
                f'/documentos-da-partida/getAll/{turn}/{id}/{year}',
            )

            yield scrapy.Request(
                url=next_url,
                callback=self.parse_turn,
                meta={
                    'year': year,
                    'id': id,
                    'tournament_name': tournament_name,
                },
            )

    def parse_turn(self, response):
        id = response.meta['id']
        year = response.meta['year']
        tournament_name = response.meta['tournament_name']
        games_ = response.json()

        for game in games_['dados']:
            p = PeneiraItem()

            match = re.search(r'onclick="(\w+)\(\);"', game['function_js'])
            function_name = match.group(1) if match else 'sim'

            p['ano'] = year
            p['id_url'] = id
            p['campeonato'] = tournament_name
            p['id_campeonato'] = game['Codigo_Campeonato']
            p['cod_categoria'] = game['Codigo_Categoria']
            p['time_mandante'] = game['TimeNomeMandante']
            p['time_mandante_UF'] = game['UFTimeMandante']
            p['resultado'] = game['Resultado']
            p['time_visitante'] = game['TimeNomeVisitante']
            p['time_visitante_UF'] = game['UFTimeVisitante']
            p['data_jogo'] = game['Jogo_DataOri']
            p['hora_jogo'] = game['Horario']
            p['num_jogo'] = game['Num_Jogo']
            p['rodada'] = game['Rodada']
            p['estadio'] = game['EstadioNomePopular']
            p['estadio_UF'] = game['UFEstadio']
            p['estadio_municipio'] = game['MunicipioEstadio']
            p['url_sumula'] = game['url_sumula']
            p['url_boletim'] = game['url_boletim']
            p['url_rdj'] = game['url_rdj']
            p['publicado'] = function_name

            yield p
