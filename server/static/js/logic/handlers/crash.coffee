crashTypes = null
vehicles = null

generateLine = (coll, crash) ->
  btnDelete = a '', icon('delete'), ->
    AJAXSend {obj: 'crash', act: 'delete'}, {id: crash.id}, ->
      goto null, obj:'crash'
  btnEdit = a '', icon('edit'), gotoCallback null, obj:'crash', act:'show', id:crash.id
    
  about = "По адресу #{crash.address}. #{crash.about}"

  coll.addAvatarLine "#{crash.date}",
    about, [btnEdit, btnDelete]
  return

initAddEdit = (form, crash={}) ->
  if crashTypes? && vehicles?
    form.addInputField 'cdate', 'date', 's4', 'Дата происшествия', crash.cdate
    form.addInputField 'victims', 'number', 's4', 'Количество пострадавших', crash.victims
    form.addInputFieldPlaceholder 'damage_cost', 'text', 's4', 'Ущерб', '1000.00', crash.damage_cost

    addCTOpts = form.addOptionsField 'crash_type_id', 's6', 'Тип происшествия'
    ctOpts = {}
    for id, ct of crashTypes
      ctOpts[id] = ct.name
    addCTOpts ctOpts, crash.crash_type_id ? 0

    form.addInputField 'address', 'text', 's6', 'Адрес', crash.address
    form.addInputField 'about', 'text', 's6', 'Описание происшествия', crash.about
    form.addInputField 'cause', 'text', 's6', 'Причина', crash.cause
    form.addInputField 'road_condition', 'text', 's12', 'Дорожные условия', crash.road_condition

    form.addEl tag 'h5', '', 'Машины, участвовавшие в происшествии:'
    for id, vehicle of vehicles
      form.addCheckBox "vehicle_#{id}", 's3', vehicle.reg_number, crash.vehicles? && (1 * id in crash.vehicles)

    form.addRow()

    btnCommit = a 'btn', 'Добавить/Обновить', ->
      data = form.collectData()
      data.id = crash.id
      AJAXSend obj: 'crash', act:'add_edit', data, (data) ->
        goto null, obj:'crash'

    form.addEl btnCommit


window.crashHandler = (params) ->
  crashTypes = null
  vehicles = null
  breadcrumb.push 'ДТП', obj: 'crash'
  switch params.act
    when 'show_all'
      coll = new Collection container, aType=false, avatar=true

      AJAXLoad params, (data) ->
        crashes = data.crashes
        for id, crash of crashes
          generateLine coll, crash

      setTitle 'ДТП'

      floatingButton.addButton 'add', 'green', 'Добавить ДТП', gotoCallback null, {obj:'crash', act:'add'}
        
    when 'add'
      setTitle 'Добавить ДТП'
      breadcrumb.push 'Добавить', {obj: 'crash', act:'add'}
      form = new Form 'new-edit-crash', 's12', container
      AJAXLoad {obj:'crashType', act:'show_all'}, (data) ->
        crashTypes = data.crashTypes
        initAddEdit(form)

      AJAXLoad {obj:'vehicle', act:'show_all'}, (data) ->
        vehicles = data.vehicles
        initAddEdit(form)

    when 'show'
      setTitle 'Редактировать ДТП'
      breadcrumb.push 'Обновить', {obj: 'crash', act:'add'}
      form = new Form 'new-edit-crash', 's12', container
      crash = null

      AJAXLoad params, (data) ->
        crash = data

        AJAXLoad {obj:'crashType', act:'show_all'}, (data) ->
          crashTypes = data.crashTypes
          initAddEdit(form, crash)

        AJAXLoad {obj:'vehicle', act:'show_all'}, (data) ->
          vehicles = data.vehicles
          initAddEdit(form, crash)