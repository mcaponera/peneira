from peneira.spiders.peneirao_spider import PeneiraoSpider
from peneira.items import PeneiraItem

EXPECTED_YEARS = [2025, 2024, 2023, 2022, 2021]
TOTAL_YEARS = len(EXPECTED_YEARS)
EXPECTED_CONTESTS = 10
EXPECTED_TURNS = 15
EXPECTED_GAMES = 15


def test_parse(html_response):
    test_spider = PeneiraoSpider()
    results = list(test_spider.parse(html_response))

    assert len(results) == TOTAL_YEARS

    expected_years = [2025, 2024, 2023, 2022, 2021]
    for req, year in zip(results, expected_years):
        assert (
            req.url
            == f'https://portaldegovernanca.cbf.com.br/documentos-da-partida/campeonatos/{year}'
        )
        assert req.callback == test_spider.parse_year
        assert req.meta == {'year': year}


def test_parse_year(json_response_contests):
    test_spider = PeneiraoSpider()
    results = list(test_spider.parse_year(json_response_contests))

    assert len(results) == EXPECTED_CONTESTS

    assert (
        results[0].url
        == 'https://portaldegovernanca.cbf.com.br/documentos-da-partida/rodadas/12569/2023'
    )
    assert results[0].meta == {
        'year': 2023,
        'id': 12569,
        'tournament_name': 'Amistoso - Seleção Brasileira Feminina',
    }

def test_parse_contest(json_response_turns):
    teste_spider = PeneiraoSpider()
    results = list(teste_spider.parse_contest(json_response_turns))

    assert len(results) == EXPECTED_TURNS

    assert results[0].meta == {
        'year': 2023,
        'id': 12553,
        'tournament_name': 'Brasileiro Feminino - A1',
    }
    assert (
        results[0].url
        == 'https://portaldegovernanca.cbf.com.br/documentos-da-partida/getAll/1/12553/2023'
    )

def test_parse_turn(json_response_tournament):
    test_spider = PeneiraoSpider()
    results = list(test_spider.parse_turn(json_response_tournament))

    assert len(results) == EXPECTED_GAMES

    item = results[0]
    assert isinstance(item, PeneiraItem)

    assert item['ano'] == 2023
    assert item['id_url'] == 12553
    assert item['campeonato'] == 'Brasileiro Feminino - A1'
    assert item['rodada'] == 1
    assert item['publicado'] == 'sim'
