window.mainHandler = (params) ->
  switch params.act
    when 'show_all'
      coll = new Collection container

      coll.addLine "test1", null
      coll.addLine "test2", null
