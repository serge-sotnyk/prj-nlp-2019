# Тема - Multi-label sentiment analysis classification

## Задача
Вхід: tweet або висловлювання відповідного розміру

Вихід:
- anger
- disgust		
- fear 	
- joy
- love
- optimism
- pessimism
- sadness
- suprise	
- trust
- нейтральний (відсутнє емоційного забарвлення)

## Dataset 
Первинна вибірка - CodaLab (https://competitions.codalab.org/competitions/17751#learn_the_details-overview).

Плани: скомпонувати інші вибірки в одну, за допомогою Twitter API витягти дані за тегами/смайлами.
Наприклад, взяти позитивні/негативні сети промаркувати як оптимізм/песимізм, використати вибірку діалогів з друзів (http://doraemon.iis.sinica.edu.tw/emotionlines/download.html)

## Domain
Орієнтовно невеликі довжиною повідомлення з соціальних мереж. Надалі можливе додання вибірок про ресторани й готелі (yelp dataset), фільми imdb (https://www.kaggle.com/iarunava/imdb-movie-reviews-dataset).

## Метрики оцінки
Стандартні метрики для multi-label класифікації.

Human evaluation - зібрати невелику вибірку самотужки.

## Методи
Спочатку спробувати стандарні підходи, планується використати cемантичні тезаруси: WordNet-Affect, SenticNet.




