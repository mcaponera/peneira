import json

import pytest
from scrapy.http import HtmlResponse, JsonResponse, Request


@pytest.fixture
def html_response():
    html = """
    <html>
        <div class="container pages-top">
        <div class="title">
            <h3>Documentos da Partida</h3>
        </div>

        <div class="content">
            <div class="filtros busca_cadastro">
                <span class="verde">Selecione o documento</span>
                <form>
                    <div class="form_group">
                        <div class="select-outter">
                            <select class="form-control" id="ano">
                                <option  value="ano">Todos os anos</option>
                                <option  value="2025">2025</option>
                                <option  value="2024">2024</option>
                                <option  value="2023">2023</option>
                                <option  value="2022">2022</option>
                                <option  value="2021">2021</option>
                            </select>
                        </div>
                    </div>
    </html>
    """
    url = 'https://portaldegovernanca.cbf.com.br/documentos-da-partida'
    request = Request(url=url)
    return HtmlResponse(
        url=url, request=request, body=html.encode('utf-8'), encoding='utf-8'
    )


@pytest.fixture
def json_response_contests():
    contest_json = [
        {
            'id_campeonato': 12559,
            'Campeonato_Categoria': 'Amistoso - Seleção Brasileira',
        },
        {
            'id_campeonato': 12569,
            'Campeonato_Categoria': 'Amistoso - Seleção Brasileira Feminina',
        },
        {
            'id_campeonato': 12553,
            'Campeonato_Categoria': 'Brasileiro Feminino - A1',
        },
        {
            'id_campeonato': 12563,
            'Campeonato_Categoria': 'Brasileiro Feminino - A2',
        },
        {
            'id_campeonato': 12567,
            'Campeonato_Categoria': 'Brasileiro Feminino - A3',
        },
        {
            'id_campeonato': 12572,
            'Campeonato_Categoria': 'Brasileiro Feminino - Sub-17',
        },
        {
            'id_campeonato': 12560,
            'Campeonato_Categoria': 'Brasileiro Feminino - Sub-20',
        },
        {
            'id_campeonato': 12555,
            'Campeonato_Categoria': 'Campeonato Brasileiro - Série A',
        },
        {
            'id_campeonato': 12556,
            'Campeonato_Categoria': 'Campeonato Brasileiro - Série B',
        },
        {
            'id_campeonato': 12561,
            'Campeonato_Categoria': 'Campeonato Brasileiro - Série C',
        },
        {
            'id_campeonato': 12562,
            'Campeonato_Categoria': 'Campeonato Brasileiro - Série D',
        },
        {
            'id_campeonato': 12557,
            'Campeonato_Categoria': 'Campeonato Brasileiro - Sub-20',
        },
        {
            'id_campeonato': 12570,
            'Campeonato_Categoria': 'Campeonato Brasileiro - SUB17',
        },
        {
            'id_campeonato': 12554,
            'Campeonato_Categoria': 'Copa do Brasil - Profissional',
        },
        {
            'id_campeonato': 12571,
            'Campeonato_Categoria': 'Copa do Brasil - Sub-20',
        },
        {
            'id_campeonato': 12558,
            'Campeonato_Categoria': 'Copa do Brasil - SUB17',
        },
        {
            'id_campeonato': 12568,
            'Campeonato_Categoria':
                'Copa do Mundo - Feminina 2023 - Seleção Brasileira Feminina',
        },
        {
            'id_campeonato': 12547,
            'Campeonato_Categoria': 'Copa do Nordeste - Eliminatórias ',
        },
        {
            'id_campeonato': 12550,
            'Campeonato_Categoria': 'Copa do Nordeste - Profissional',
        },
        {
            'id_campeonato': 12549,
            'Campeonato_Categoria': 'Copa Verde - Profissional',
        },
        {
            'id_campeonato': 12573,
            'Campeonato_Categoria': 'Eliminatorias - Copa 2026 ',
        },
        {
            'id_campeonato': 12564,
            'Campeonato_Categoria':
                'Liga de Desenvolvimento - Sub-13 Masculino',
        },
        {
            'id_campeonato': 12565,
            'Campeonato_Categoria':
                'Liga de Desenvolvimento - Sub-14 Feminino',
        },
        {
            'id_campeonato': 12566,
            'Campeonato_Categoria':
                'Liga de Desenvolvimento - Sub-16 Feminino',
        },
        {
            'id_campeonato': 12552,
            'Campeonato_Categoria': 'Supercopa do Brasil - Feminino',
        },
        {
            'id_campeonato': 12551,
            'Campeonato_Categoria': 'Supercopa do Brasil - Profissional',
        },
    ]

    json_body = json.dumps(contest_json).encode('utf-8')

    url = 'https://portaldegovernanca.cbf.com.br/documentos-da-partida/campeonatos/2023'
    request = Request(url=url, meta={'year': 2023})
    return JsonResponse(
        url=url,
        request=request,
        body=json_body,
    )


@pytest.fixture
def json_response_turns():
    turns_json = [
        {'Rodada': 1},
        {'Rodada': 2},
        {'Rodada': 3},
        {'Rodada': 4},
        {'Rodada': 5},
        {'Rodada': 6},
        {'Rodada': 7},
        {'Rodada': 8},
        {'Rodada': 9},
        {'Rodada': 10},
        {'Rodada': 11},
        {'Rodada': 12},
        {'Rodada': 13},
        {'Rodada': 14},
        {'Rodada': 15}
    ]

    json_body = json.dumps(turns_json).encode('utf-8')

    url = 'https://portaldegovernanca.cbf.com.br/documentos-da-partida/rodadas/12553/2023'
    request = Request(url=url, meta={
        'year': 2023,
        'id': 12553,
        'tournament_name': 'Brasileiro Feminino - A1'
    })
    return JsonResponse(
        url=url,
        request=request,
        body=json_body,
    )


@pytest.fixture
def json_response_tournament():
    with open('peneira/tests/turns.json', 'r') as file:
        tournament = json.load(file)

    url = 'https://portaldegovernanca.cbf.com.br/documentos-da-partida/getAll/1/12553/2023'
    request = Request(url=url, meta={
        'year': 2023,
        'id': 12553,
        'tournament_name': 'Brasileiro Feminino - A1'
    })

    return JsonResponse(
        url=url,
        request=request,
        body=json.dumps(tournament).encode('utf-8'),
    )