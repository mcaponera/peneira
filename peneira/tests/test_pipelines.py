import datetime

from peneira.pipelines import DataPipeline

EXPECTED_YEAR = 2022

def test_data_pipeline():
    item = {
        'ano': 2022,
        'campeonato': 'Brasileiro Feminino - Sub-20',
        'cod_categoria': 56,
        'data_jogo': '02/07/2022',
        'estadio': 'SESC Protásio Alves',
        'estadio_UF': 'RS',
        'estadio_municipio': 'Porto Alegre',
        'hora_jogo': '15:00',
        'id_campeonato': 1016,
        'id_url': 12579,
        'num_jogo': 89,
        'publicado': 'sim',
        'resultado': '2 X 0  ',
        'rodada': 1,
        'time_mandante': 'Internacional',
        'time_mandante_UF': 'RS',
        'time_visitante': 'São Paulo',
        'time_visitante_UF': 'SP',
        'url_boletim': [
            'href="https://conteudo.cbf.com.br/sumulas/2022/56101689b.pdf"'
        ],
        'url_rdj': [
            'href="https://conteudo.cbf.com.br/sumulas/2022/56101689rdj.pdf"'
        ],
        'url_sumula': [
            'href="https://conteudo.cbf.com.br/sumulas/2022/56101689se.pdf"'
        ],
    }

    pipeline = DataPipeline()

    processed_item = pipeline.process_item(item, spider=None)

    assert processed_item['ano'] == EXPECTED_YEAR
    assert processed_item['data_jogo'] == datetime.date(2022, 7, 2)
    assert processed_item['hora_jogo'] == datetime.time(15, 0)
    assert processed_item['url_boletim'] == [
        'https://conteudo.cbf.com.br/sumulas/2022/56101689b.pdf'
    ]
    assert processed_item['url_rdj'] == [
        'https://conteudo.cbf.com.br/sumulas/2022/56101689rdj.pdf'
    ]
    assert processed_item['url_sumula'] == [
        'https://conteudo.cbf.com.br/sumulas/2022/56101689se.pdf'
    ]
