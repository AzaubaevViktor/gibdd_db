window.getBrowser = ->
  ua = navigator.userAgent
  fbName = () ->
    if (ua.search(/MSIE/) > -1) then return "ie"
    if (ua.search(/Firefox/) > -1) then return "firefox"
    if (ua.search(/Opera/) > -1) then return "opera"
    if (ua.search(/Chrome/) > -1) then return "chrome"
    if (ua.search(/Safari/) > -1) then return "safari"
    if (ua.search(/Konqueror/) > -1) then return "konqueror"
    if (ua.search(/Iceweasel/) > -1) then return "iceweasel"
    if (ua.search(/SeaMonkey/) > -1) then return "seamonkey"

  bName = fbName()

  getVersion = (bName) ->
    switch (bName)
      when "ie" then return (ua.split("MSIE ")[1]).split(";")[0]
      when "firefox" then return ua.split("Firefox/")[1]
      when "opera" then return ua.split("Version/")[1]
      when "chrome" then return (ua.split("Chrome/")[1]).split(" ")[0]
      when "safari" then return (ua.split("Version/")[1]).split(" ")[0]
      when "konqueror" then return (ua.split("KHTML/")[1]).split(" ")[0]
      when "iceweasel" then return (ua.split("Iceweasel/")[1]).split(" ")[0]
      when "seamonkey" then return ua.split("SeaMonkey/")[1]

  version = getVersion(bName)

  return [bName,version.split(".")[0],version]

window.current_browser = getBrowser()