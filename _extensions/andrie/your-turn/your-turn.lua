quarto.doc.add_html_dependency({
  name = "yourturnIframeContainer",
  version = "0.1.0",
  scripts = {"yourturn-iframeContainer.js"},
})

insert_your_turn = function(args, kwargs, meta) 

    local use_index = args[2]
    if use_index == nil or use_index == "" then
      use_index = true
    else
      use_index = false
    end

    -- Create the link target from the name
    local name = pandoc.utils.stringify(args[1])
    local target
    if use_index == true or use_index == 'true' then
      target = "exercises/" .. name .. "/index.html"
    else
      target = "exercises/" .. name .. "/" .. name .. ".html"
    end
    -- local link = pandoc.Link(pandoc.Str(name), target)
    local link = pandoc.Link(name, target)
    link.attributes = {target = "_blank"}
    local msg_pre = "Complete the exercise on this page:"
    local msg_post = "..."

    -- Create the button using raw HTML
    local json_msg = '{ "from": "your-turn", "target": "' .. target .. '" }'
    json_msg = json_msg:gsub('"', '\'')  -- Escape quotes
    local cmd =  "window.top.postMessage('" .. target .. "', '*')";

    local txt = "Go to Exercise"
    local btn_style = 'style="background-color: #72994E; font-size: 1em; border-radius: 15px; padding: 0.5em 1em;"'
    local btn ='<button ' .. btn_style .. ' onclick="' .. cmd .. '">' .. txt ..'</button>'
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


insert_container = function(args, kwargs, meta)
  local msg = pandoc.Div(
    '',
    pandoc.Attr(
      "messageDisplay", -- id
      {}, -- classes
      {style = "margin-top: 20px; padding: 10px; border: 1px solid #123233;"} -- attributes
    )
  )
  local iframe = pandoc.Div(
    '',
    pandoc.Attr(
      "yourturnContainer", -- id
      {}, -- classes
      {style = "margin-top: 20px; position: absolute; left: 25px; width: calc(100vw - 50px);"} -- attributes
    )
  )
  return {msg, iframe}
end


return {
  ['yourturn'] = insert_your_turn,
  ['yourturnIframeContainer'] = insert_container
}

