## Курсовий проект
Для свого курсового проекту:

- поділіть свої дані на тренувальні та тестувальні
- побудуйте бейзлайн (правила чи простий класифікатор)
- поміряйте якість роботи системи раніше побудованими метриками

Код для курсового проекту повинен бути у вашому репозиторії. У директорії students/ в теці з вашим іменем збережіть файл з посиланням на код бейзлайну. Опишіть ваші результати.

## Tesufr
Multilingual Text Summarizing Framework - https://github.com/serge-sotnyk/tesufr

На 13-квітня-2019 зроблено каркас фреймворку, який:

1. Дозволяє використовувати різні ядра для анотації (виділення ключових слів та саммарі) текстів на різних мовах.
2. Додано baseline ядро, яке майже незалежне від мови (індо-європейської групи), у якості саммарі віддає перщі N речень текста, а у якості ключових слів - M самих росповсюджених в тексті термів.
3. Розроблено систему підтримки абстрактних корпусів, та зроблено два провайдери для реальних корпусів - BBC News (саммарі) та Krapivin2009 (саммарі та ключові слова). Фреймворк, якщо для цих корпусів ще нема локальних файлів, загружає їх з мого Google Drive, та надалі віддає у стандартизованному виді. Далі будуть підтримані ще корпуси для саммарі, та ключових слів.
4. Перенесено розроблену раніше систему оцінки якості на базі метрик ROUGE/BLEU для саммарі, та F1 для ключових слів.

### Типовий код:

Анотація тексту

```
from nltk.corpus import udhr
...
processor = Processor()
text = udhr.raw('Italian-Latin1')
text_process_params = TextProcessParams(SummarySize.new_relative(0.1), keywords_number=10)
document = processor.process_text(text, text_process_params)
```

* Processor - клас, який керує обробкою тексту
* text_process_params - параметри обробки тексту. Зараз це кількість ключових слів, та речень в саммарі.
* Document - клас, який є контейнером для переробленого тексту, та має поля для колекції знайдених ключових слів, самарі, Named Entities, оригінального тексту, деталі обробки, ворнінги та помилки, які можуть бути на етапі обробки.

Для того, щоб створити нове ядро, треба реалізувати абстрактний клас CoreBase - https://github.com/serge-sotnyk/tesufr/blob/789b37fc5947bdcd5379aa8187eeba52dfe8d656/tesufr/cores/core_base.py

Прикладом такої реалізації є поки єдиний клас FallbackCore - https://github.com/serge-sotnyk/tesufr/blob/789b37fc5947bdcd5379aa8187eeba52dfe8d656/tesufr/cores/fallback_core.py. Але далі буде...

Перевірка якості анотації по двом підтриманим корпусам (https://github.com/serge-sotnyk/tesufr/blob/789b37fc5947bdcd5379aa8187eeba52dfe8d656/evaluate_with_corpora.py):

```
processor = Processor()
corpus = BbcNewsProvider()
metrics = evaluate_processor_on_corpus(processor, corpus, "BBC News")
print(metrics)

corpus = Krapivin2009Provider()
metrics = evaluate_processor_on_corpus(processor, corpus, "Krapivin2009")
print(metrics)
```

### Плани на майбутнє
1. Викладка як пакет Pypi (щоб можна було встановлювати за допомогою pip)
2. Нові ядра
3. Нові корпуси
4. REST API
