 <h1>Онлайн интеллектуальный помощник в планировании пеших туристических маршрутов.</h1>
<h2>Общее описание</h2>
<p>Веб сервис предназначен для помощи в планировании пеших туристическиз маршрутов по городу Москва.</p>
<p>На сате размещены несколько статей по теме и галлерея с интересными достопримечательностями Москвы, где пользователь может открыть страницу конкретной достопримечательности.</p>
<p>Пользователь может создать и сохранить свой собственный маршрут из предоставленных достопримечательностей. 
  На странице маршрута созданного пользователем или из списка рекомендованных отображается список достопримечательностей в этом маршруте, 
  их адреса и описания, если маршрут создан пользователем он может его отредактировать или удалить.</p>
<p>Сервис строит оптимальный маршрут, проходящий через выбранные точки.</p>
<h2>Инструкции по установке</h2>
<p>Чтобы запустить проект локально на своём компьютере необходимо импортировать или скачать архив из  git репозитория.</p>
<p>Для развёртывания Django проекта проще всего использовать среду разработки PyCharm или самостоятельно развернуть виртуальную среду и скачать Django.</p>
<div>
  <p>В проекте используется ряд библиотек, которые нужно скачать:</p>
  <ul>
    <li>wikipedia (генерация крадких описаний)</li>
    <li>spacy с использованием модели ru_core_news_md (анализ текста для генерации тегов)</li>
    <li>geopandas, geopy (работа с координатами и адресами)</li>
    <li>osmnx (работа с картами)</li>
  </ul>
  <p>Библиотеки можноуствновить используя файл requirements.txt</p>
  
  <p>Если после установки этих библиотек, при маршрутизации возникнет ошибка "folium must be installed to use this optional feature" 
    необходимо установить библиотеку folium и после этого переустановить osmnx.</p>
  <p>Пеоед запуском проекта сгенерируйте граф дорожной сети запустив команды в python консоли:</p>
  <p>graph = ox.graph_from_place(place, network_type=mode)</p>
  <p>ox.save_graphml(graph, 'mos.graphml')</p>
  <p>.graphml файл разместите в корневой папке проекта.</p>
</div>
<p>Чтобы запустить проект можно использовать возможности среды или ввести в терминале "python manage.py runserver"</p>
<p>По умолчаснию проект запускается на localhost:8000</p>
<h2>Примеры использования</h2>
<p>Для навигации по страницам используется меню.
 Прийдя на сайт пользователь может прочитавт содержимое текстовой страницы перейти в галлерею, нажав на текст на картинке перейти на страницу заинтересовавшей достопримечательности.
 Наведя на ячейку меню Блог пользовател может выбрать в выпадающем меню заинтересовавшую его статью и изучить её.</p>
<p>Перейдя на страницу Мои маршруты если пользователь не авторизован открывается страница авторизации, на которой также размещена ссылка на страницу регистрации.</p>
<p>На Домашней странице и странице Мои маршруты размещена форма для выбора города поездки, по умолчанию Москва, при нажатии на кнопку Поехали открывается страница создания нового маршрута. 
 Поля названия и описания маршрута пользователь заполняет сам, для добавления в маршрут новой точки пользователь должен нажать на название интересующей его достопримечательности. Для сохранения нужно нажать кнопку сохранить.</p>
<p>На страницах Мои Маршруты, Рекомендации и Карта выводятся соответственно маршруты пользователя, супер пользователя и оба этих варианта.</p>
<p>При нажатии на название маршрута открывается страница маршрута с его названием, описанием, списком выбранных достопримечательностей и описаний к ним.</p>
<div>
 <p>На странице маршрута также размещено несколько кнопок.</p>
 <ul>
  <li>Редактировать (открывает страницу редактирования маршрута) (отсутствует если это рекомендованный маршрут)</li>
  <li>Удалить (удаляет маршрут, переадресовывает на страницу Мои маршруты) (отсутствует если это рекомендованный маршрут)</li>
  <li>Построить (на экран выводится построенный маршрут)</li>
 </ul>
</div>

 <p>Техническая документация: https://docs.google.com/document/d/1036RsnHIlXRHhNEgeC8zKbaZFEGDilM9yqGrMYucLP0/edit</p>
 <p>Инструкция по установке: https://docs.google.com/document/d/1LMeqQx0TgR-XotEamrzDjpOWD9zgpUf4oHeN4eD0rEw/edit</p>
 <p>Руководство пользователя: https://docs.google.com/document/d/1H3wlnOBEqlP47dqCiUycuvEGrHqUkLa_YIKUu45kYB8/edit</p>
