return {
  ['yourturn'] = function(args, kwargs, meta) 
    local name = "exercises/" .. pandoc.utils.stringify(args[1])
    local target = "../" .. name .. ".html"
    local link = pandoc.Link(pandoc.Str(name), target)
    local msg_pre = "Go to "
    local msg_post = " and complete the exercise."
    return pandoc.Div({
      pandoc.Div(
        pandoc.Para{
          pandoc.Str(msg_pre), link, pandoc.Str(msg_post),
        },
        pandoc.Attr("", {"your-turn-link"}, {style='width:70%;'})
      ),
      pandoc.Div(
        pandoc.Image(
          "", --caption
          "../images/keep-calm-and-take-your-turn.png", --source
          "" --title,
        ),
        pandoc.Attr("", {"your-turn-image"}, {style='width:30%;'})
      )
    },
    pandoc.Attr("", {"your-turn-container"}, {style='display:flex;'}) 
  )
  end
}

