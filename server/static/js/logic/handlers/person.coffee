persons = {'-1':"--------"}

initModal = (person={}) ->
  modal.clear()
  modal.header.text 'Создать нового владельца'
  form = new Form 'new-person', 's12', modal.text

  addOptions = form.addOptionsField 'is_organization', 's6', 'Тип'
  addOptions {0:'Человек', 1:'Организация'}, person.is_organization ? 0
  isOrgSelect = form.find '#is_organization'

  addOptions = form.addOptionsField 'chief_id', 's6', 'Владелец', (person.is_organization ? 0) == 0
  addOptions persons, person.chief ? -1
  chiefSelect = form.find '#chief_id'

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

window.personInfoModal = (p_id) ->
  modal.clear()
  modal.header.text 'Загружаем информацию...'
  modal.text.text 'Это займёт некоторое время'
  AJAXLoad {obj: 'person', act: 'show', id: p_id}, (person) ->
    modal.clear()
    modal.header.text "#{person.full_name} #{if person.is_organization then '(организация)' else ''}"
    chief = [""]
    if person.is_organization
      chief = ["<b>Владелец: </b>",
        a('', person.chief_full_name, ->
          personInfoModal person.chief_id
        ),
        "<br>"
      ]

    modal.text.append "<b>Адрес:</b> #{person.address}<br>"
    modal.text.append chief
    modal.text.append "<b>Транспортные средства:</b><br>"
    for v_id, vehicle of person.vehicles
      vehicleStr = "* #{vehicle.reg_number} (#{vehicle.vehicle_type_name})"
      modal.text.append [
        a('', vehicleStr,  ->
          vehicleInfoModal v_id
        ),
        "<br>"
      ]
    

generateLine = (coll, person) ->
  btnDelete = a '', icon('delete'), ->
    AJAXSend {obj: 'person', act: 'delete'}, id: person.id, ->
      goto null, obj:'person'
  btnEdit = a '', icon('edit'), ->
    initModal person
    modal.show()
  btnInfo = a '', icon('info'), ->
    personInfoModal person.id
    modal.show()

  about = "#{person.address}"
  if person.chief_full_name?
    about += "<br>Владелец: #{person.chief_full_name}"

  coll.addAvatarLine "#{person.full_name} #{if person.is_organization then '(организация)' else ''}",
    about, [btnInfo, btnEdit, btnDelete]
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