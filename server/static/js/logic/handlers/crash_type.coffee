initAddEditModal = (crashType={}) ->
  modal.clear()
  modal.header.text 'Название типа ДТП'
  form = new Form 'edit-crashType', 's12', modal.text
  form.addInputField 'name', 'text', 's12', 'Название', crashType.name

  modal.setAgreeHandler ->
    data = form.collectData()
    data.id = crashType.id
    AJAXSend obj:'crashType', act:'add_edit', data, (data) ->
      goto null, obj:'crashType', act:'show_all'


generateLine = (params, crashType) ->
  btnDelete = a 'secondary-content', icon('delete'), ->
    AJAXSend {obj: 'crashType', act: 'delete'}, id: crashType.id, ->
      goto null, params
  btnEdit = a 'secondary-content', icon('edit'), ->
    initAddEditModal crashType
    modal.show()
  return [tag('b', null, data=crashType.name), btnDelete, btnEdit]

window.crashTypeHandler = (params) ->
  switch params.act
    when 'show_all'
      coll = new Collection container, false
      VFTs = null

      AJAXLoad params, (data) ->
        for _id, crashType of data.crashTypes
          coll.addLine generateLine params, crashType
          null

      setTitle 'Типы ДТП'
      breadcrumb.push 'Типы ДТП', params

      floatingButton.addButton 'add', 'green', 'Добавить тип ДТП', ->
        initAddEditModal()
        modal.show()

