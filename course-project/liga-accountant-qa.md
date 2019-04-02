## Бухгалтерська питально-відповідальна система

### Завдання

Бухгалтери щоденно шукають інформацію, пов'язану зі звітністю. Наприклад:
- порядок заповнення форми 1ПДВ
- призначення платежу при сплаті податків
- термін подання звітності по ЄСВ
- розмір податку у другої групи ФОП
- пдв при анулюванні свідоцтва

Автоматизація такого пошуку зекономить багато часу. Потрібно розробити систему, яка на вхід отримує запит, а на вихід видає текстову відповідь на цей запит, наприклад, абзац із закону чи дату з календаря.

Критерій успіху - внутрішні метрики (TBD) та human evaluation.

### Дані

Приклади запитів можна виділити із загальної [бази запитів](https://www.dropbox.com/s/03gxvwue6egzf09/search_queries%20(1).csv?dl=0) компанії Ліга:Закон.

Дані для пошуку відповідей:
- тексти законів (100 тис) - неструктуровані дані, але містять мітку класу документу 
- аналітичні матеріали (10 тис) - неструктуровані дані, але містять мітку класу документу 
- календар з термінами подання звітності - структуровані дані

Приклади нормативних документів можна знайти тут: https://ips.ligazakon.net/search?search_group=500-0000.0003. (Ті, що з замками, в інтрфейсі повністю не покажуться.)