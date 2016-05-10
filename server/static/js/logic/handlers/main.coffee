window.mainHandler = (params) ->
  switch params.act
    when 'show_all'
      coll = new Collection container

      coll.addLine "Транспортные средства", null
      coll.addLine "Типы ТС", gotoCallback null, obj:'vehicleType', act:'show_all'
      coll.addLine "Типы Параметров ТС", gotoCallback null, obj:'vehicleFeatureType', act:'show_all'
      coll.addLine "Параметры ТС", null
      coll.addLine "Водители", null
      coll.addLine "Организации", null
      coll.addLine "ДТП", null
      coll.addLine "Типы ДТП", null
      coll.addLine "РОЗЫСК", null

