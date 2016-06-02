window.mainHandler = (params) ->
  switch params.act
    when 'show_all'
      coll = new Collection container

      coll.addLine "Транспортные средства", gotoCallback null, obj:'vehicle'
      coll.addLine "Типы ТС", gotoCallback null, obj:'vehicleType'
      coll.addLine "Типы Параметров ТС", gotoCallback null, obj:'vehicleFeatureType'
#      coll.addLine "Параметры ТС", gotoCallback null, obj:'vehicleTypeFeatureTypeLink'
      coll.addLine "Владельцы", gotoCallback null, obj:'person'
      coll.addLine "-ДТП", null
      coll.addLine "Типы ДТП", gotoCallback null, obj:'crashType'
      coll.addLine "-РОЗЫСК", null

