window.setTitle = (title) ->
  title ?= 'Неизвестная страница'
  document.title = "Расписания СТОПП: #{title}"


window.goto = (title, getParams) ->
  setTitle title
  get = ""
  for k, v of getParams
    get += "#{k}=#{v}&"
  window.history.pushState null, title, "?#{get}"
  newPageHandler()


newPageHandler = () ->
  EHR.unregistry()
  floatingButton.clear()
  modal.clear()
  progress.setProgress 0
  breadcrumb.popAll()
  ($ '.material-tooltip').remove()


  uri = parseUri window.location.toString()
  params = uri.queryKey
  if $.isEmptyObject params
    goto 'БД ГИБДД', obj:'main', act:'show_all'
    return

  handler = handlers[params.obj]
  container.empty()
  tableContainer.empty()
  if typeof handler == 'function'
    handler params
  else
    head = tag 'h4', '', 'Страница не найдена'
    p = tag 'p', '', 'Данной страницы не существует. Го <a onclick=goto("",{})>сюды</a>'
    container.append [head, p]


($ document).ready ->
  window.container = $ '#container'
  window.tableContainer = $ '#table-container'

  newPageHandler()

  # Вешаем обработчики на смену адреса
  window.addEventListener 'popstate', (e) ->
    newPageHandler()
  , false

  if current_browser[0] != 'chrome'
    Materialize.toast "<b>#{current_browser[0]}</b>, да?<br>
На этом браузере работа не протестирована,<br>
поэтому если что-то не работает -- твои проблемы.<br>
Не насилуй мозг и используй <a href='https://www.google.com/chrome/'>Google Chrome</a>
", 10000
