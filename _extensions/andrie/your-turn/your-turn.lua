return {
  ['yourturn'] = function(args, kwargs, meta) 

    local use_index = args[2]
    if use_index == nil or use_index == "" then
      index = talse
    else
      index = true
    end

    -- Create the link target from the name
    local name = pandoc.utils.stringify(args[1])
    local target
    if use_index == true or use_index == 'true' then
      target = "../docs/exercises/" .. name .. "/index.html"
    else
      target = "../docs/exercises/" .. name .. "/" .. name .. ".html"
    end
    local link = pandoc.Link(pandoc.Str(name), target)
    link.attributes = {target = "_blank"}
    local msg_pre = "Complete the exercise on this page:"
    local msg_post = "..."

        -- Create the button using raw HTML
    local cmd = "window.open(\'%s\', \'_blank\')"
    local cmd = "console.log('Sending a message')"
    local txt = "Go to Exercise"
    local btn ='<button onclick="' .. cmd .. '">' .. txt ..'</button>'
    local button_html = string.format(btn, target)
    local button = pandoc.RawInline('html', button_html)

    return pandoc.Div({
      pandoc.Div({
        pandoc.Para(pandoc.Str(msg_pre)),
        pandoc.Para(link),
        pandoc.Para(pandoc.Str(msg_post)),
        pandoc.Para(button)
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

