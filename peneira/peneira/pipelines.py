import datetime

from itemadapter import ItemAdapter


class DataPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Transformação de datas (campo 'data_jogo')
        date_text = adapter.get('data_jogo')
        if date_text:
            try:
                date = datetime.datetime.strptime(date_text, '%d/%m/%Y').date()
                adapter['data_jogo'] = date
            except ValueError:
                print(f"Formato de data inválido 'data_jogo': {date_text}")

        # Transformação de URLs
        for url_field in ['url_sumula', 'url_boletim', 'url_rdj']:
            url_value = adapter.get(url_field)
            if url_value and isinstance(url_value, list):
                adapter[url_field] = [
                    self._clean_url(url) for url in url_value
                ]
            elif url_value and isinstance(url_value, str):
                adapter[url_field] = self._clean_url(url_value)

        # Transformação de hora
        time_text = adapter.get('hora_jogo')
        if time_text:
            try:
                time = datetime.datetime.strptime(time_text, '%H:%M').time()
                adapter['hora_jogo'] = time
            except ValueError:
                print(f"Formato de hora inválido 'hora_jogo': {time_text}")

        return item

    def _clean_url(self, url):
        if url.startswith('href="') and url.endswith('"'):
            return url[6:-1]
        return url
