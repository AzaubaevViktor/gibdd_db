persons = {'-1':"--------"}

initModal = (person={}) ->
  modal.clear()
  modal.header.text 'Создать нового владельца'
  form = new Form 'new-person', 's12', modal.text

  addOptions = form.addOptionsField 'is_organization', 's6', 'Тип'
  addOptions {0:'Человек', 1:'Организация'}, person.is_organization ? 0
  isOrgSelect = form.find '#is_organization'

  addOptions = form.addOptionsField 'chief', 's6', 'Владелец', (person.is_organization ? 0) == 0
  addOptions persons, person.chief ? -1
  chiefSelect = form.find '#chief'

  isOrgSelect.change ->
    chiefSelect.prop('disabled', '0' == isOrgSelect.val())
    $('select').material_select()

  form.addInputField 'full_name', 'text', 's12', 'Полное имя/название', person.full_name ? ""
  form.addInputField 'address', 'text', 's12', 'Адрес', person.address ? ""
  modal.setAgreeHandler ->
    data = form.collectData()
    data.id = person.id
    AJAXSend obj:'person', act:'add_edit', data, (data) ->
      goto null, obj:'person'

generateLine = (coll, person) ->
  btnDelete = a '', icon('delete'), ->
    AJAXSend {obj: 'person', act: 'delete'}, id: person.id, ->
      goto null, obj:'person'
  btnEdit = a '', icon('edit'), ->
    initModal person
    modal.show()
  about = "#{person.address}"
  if person.chief_full_name?
    about += "<br>Владелец: #{person.chief_full_name}"

  coll.addAvatarLine "#{person.full_name} #{if person.is_organization then '(организация)' else ''}",
    about, [btnEdit, btnDelete]
  return

window.personHandler = (params) ->
  switch params.act
    when 'show_all'
      coll = new Collection container, aType=false, avatar=true
      
      AJAXLoad params, (data) ->
        for id, person of data.persons
          person.id = id
          generateLine coll, person
          if 0 == person.is_organization
            persons[id] = person.full_name

      setTitle 'Владельцы'
      breadcrumb.push 'Владельцы', params

      floatingButton.addButton 'add', 'green', 'Добавить владельца', ->
        initModal()
        modal.show()