(($) ->
  jQuery.fn.dynTooltip = (title, pos='left', delay=50) ->
    $this = $ this
    $this.attr 'data-position', pos
    $this.attr 'data-tooltip', title
    $this.addClass 'tooltiped'

    return this.tooltip delay: delay)(jQuery)


