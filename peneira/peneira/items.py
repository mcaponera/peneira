from typing import Annotated, Literal
from pydantic import BaseModel, HttpUrl
from datetime import date, time

import scrapy


class PeneiraItemSchema(BaseModel):
    ano: int
    id_url: int
    campeonato: str
    id_campeonato: str
    cod_categoria: str
    time_mandante: str
    time_visitante: str
    time_mandante_UF: str
    time_visitante_UF: str
    resultado: str
    data_jogo: date
    hora_jogo: time
    num_jogo: int
    rodada: int
    estadio: str
    estadio_UF: str
    estadio_municipio: str
    url_sumula: HttpUrl
    url_boletim: HttpUrl
    url_rdj: HttpUrl
    publicado: str


class PeneiraItem(scrapy.Item):
    ano = scrapy.Field()
    id_url = scrapy.Field()
    campeonato = scrapy.Field()
    id_campeonato = scrapy.Field()
    cod_categoria = scrapy.Field()
    time_mandante = scrapy.Field()
    time_visitante = scrapy.Field()
    time_mandante_UF = scrapy.Field()
    time_visitante_UF = scrapy.Field()
    resultado = scrapy.Field()
    data_jogo = scrapy.Field()
    hora_jogo = scrapy.Field()
    num_jogo = scrapy.Field()
    rodada = scrapy.Field()
    estadio = scrapy.Field()
    estadio_UF = scrapy.Field()
    estadio_municipio = scrapy.Field()
    url_sumula = scrapy.Field()
    url_boletim = scrapy.Field()
    url_rdj = scrapy.Field()
    publicado = scrapy.Field()
