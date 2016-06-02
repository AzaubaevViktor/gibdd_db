vehicle_types = null
vehicle_feature_types = null
persons = null
vehicles = null

addToFormByVFT = (form, vehicle = {}) ->
  for id, vft of vehicle_feature_types
    # 0 -- date, 1 -- str, 2 -- number, 3 -- float number
    value = vehicle.features?[id] ? ""
    switch vft.variable_type
      when 0 # date
        form.addInputFieldPlaceholder "vft_#{id}", 'text', 's12 vft', vft.name, 'dd.mm.yyyy', value
      when 1 # str
        form.addInputFieldPlaceholder "vft_#{id}", 'text', 's12 vft' , vft.name, 'Текст', value
      when 2 # number
        form.addInputFieldPlaceholder "vft_#{id}", 'number', 's12 vft', vft.name, 'Число', value
      when 3 # float
        form.addInputFieldPlaceholder "vft_#{id}", 'text', 's12 vft', vft.name, 'Дробное число', value


showNeedVFT = (form, needed) ->
  for inputDiv in form.find('.vft')
    inputF = ($ inputDiv).find('input')
    inputFid = ($ inputF).attr('id')[4..]
    if inputFid in needed
      ($ inputDiv).show(200)
    else
      ($ inputDiv).hide(200)


getNeededFeatures = (vt_id) ->
  for k, v of vehicle_types[vt_id].features
    k

initModal = (vehicle = {}) ->
  modal.clear()
  modal.header.text 'Машина'
  form = new Form 'new-vehicle', 's12', modal.text

  # Тип ТС
  addOptVT = form.addOptionsField 'vehicle_type_id', 's6', 'Тип ТС'
  vtOpts = {}
  for id, v of vehicle_types
    vtOpts[id] = v.name
  addOptVT vtOpts, vehicle.vehicle_type_id ? 0

  VTInput = form.find('#vehicle_type_id')

  # Смена типа ТС
  optVt = form.find '#vehicle_type_id'
  optVt.change ->
    showNeedVFT(form, getNeededFeatures VTInput.val())

  # Владелец
  addOptChief = form.addOptionsField 'chief_id', 's6', 'Владелец'
  chOpts = {}
  for id, v of persons
    chOpts[id] = v.full_name
  addOptChief chOpts, vehicle.chief_id ? 0

  # Регистрационный номер
  form.addInputFieldPlaceholder 'reg_number', 'text', 's6', 'Регистрационный номер', 'Автоматический подбор', vehicle.reg_number ? ''

  # Фичи ТС
  addToFormByVFT(form, vehicle)

  # Скрывает/показывает поля фич
  showNeedVFT(form, getNeededFeatures VTInput.val())

  # Обработчик нажатия
  modal.setAgreeHandler ->
    data = form.collectData()
    data.id = vehicle.id
    AJAXSend obj: 'vehicle', act:'add_edit', data, (data) ->
      goto null, obj:'vehicle', act:'show_all'

tryInitAll = (coll) ->
  # Показывает всё, только если загрузились все три штуки
  if (vehicle_types? && persons? && vehicles? && vehicle_feature_types?)
    floatingButton.addButton 'add', 'green', 'Добавить машину', ->
      initModal()
      modal.show()

    for id, vehicle of vehicles
        vehicle.id = id
        generateLine coll, vehicle

generateLine = (coll, vehicle) ->
  btnDelete = a '', icon('delete'), ->
    AJAXSend {obj: 'vehicle', act:'delete'}, id: vehicle.id, ->
      goto null, obj: 'vehicle'

  btnEdit = a '', icon('edit'), ->
    initModal vehicle
    modal.show()

  featuresStr = ""
  for id, feature of vehicle.features
    featuresStr += "<b>#{vehicle_feature_types[id].name}:</b> #{feature}<br>"

  coll.addAvatarLine "#{vehicle.reg_number}",
    "<b>Владелец:</b> #{vehicle.c_name}<br>
     <b>Тип ТС:</b> #{vehicle.vt_name}<br>
     #{featuresStr}",
    [btnEdit, btnDelete]
  return


window.vehicleHandler = (params) ->
  switch params.act
    when 'show_all'
      vehicle_types = null
      vehicle_feature_types = null
      persons = null
      vehicles = null

      coll = new Collection container, aType=false, avatar=true

      AJAXLoad {obj: 'vehicleType', act: 'show_all'}, (data) ->
        vehicle_types = data.vehicleTypes
        tryInitAll(coll)
      AJAXLoad {obj: 'vehicleFeatureType', act:'show_all'}, (data) ->
        vehicle_feature_types = data.vehicleFeatureTypes
        tryInitAll(coll)
      AJAXLoad {obj: 'person', act: 'show_all'}, (data) ->
        persons = data.persons
        tryInitAll(coll)
      AJAXLoad params, (data) ->
        vehicles = data.vehicles
        tryInitAll(coll)

      setTitle 'Машины'
      breadcrumb.push 'Машины', params



