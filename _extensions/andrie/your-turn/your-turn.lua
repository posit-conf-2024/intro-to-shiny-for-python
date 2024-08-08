
-- workhorse function
insert_it = function(type, name, use_index) 
    -- Create the link target from the name
    local target
    local prefix
    local msg_pre = ''
    local img_src = ''
    local txt
    local btn_colour
    if type == "yourturn" then
      msg_pre = "Complete the exercise on this page:"
      img_src = "../images/keep-calm-and-take-your-turn.png"
      txt = "Open Exercise"
      btn_colour = "#72994E"
      font_colour = "#FFFFFF"
      prefix = "exercises/"
    else 
      msg_pre = "View the app on this page:"
      img_src = "../images/keep-calm-and-view-the-app.png"
      txt = "View the App"
      btn_colour = "#4A6B79"
      font_colour = "#FFFFFF"
      prefix = "apps/"
    end
    if use_index == true or use_index == 'true' then
      target = prefix .. name .. "/index.html"
    else
      target = prefix .. name .. "/" .. name .. ".html"
    end
    -- local link = pandoc.Link(pandoc.Str(name), target)
    local link = pandoc.Link(name, target)
    link.attributes = {target = "_blank"}

    local msg_post = "..."

    -- Create the button using raw HTML
    local json_msg = '{ "from": "your-turn", "target": "' .. target .. '" }'
    json_msg = json_msg:gsub('"', '\'')  -- Escape quotes
    local cmd =  "window.top.postMessage('" .. target .. "', '*')";

    local btn_style = 'style="background-color: ' .. btn_colour .. '; color:' .. font_colour .. '; font-size: 1em; border-radius: 15px; padding: 0.5em 1em;"'
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
          -- "../images/keep-calm-and-take-your-turn.png", --source
          img_src, --source
          "" --title,
        ),
        pandoc.Attr("", {"your-turn-image"}, {style='width:30%;'})
      )
    },
    pandoc.Attr("", {"your-turn-container"}, {style='display:flex;'}) 
  )
end

-- your turn
insert_your_turn = function(args, kwargs, meta) 
  local use_index = args[2]
  if use_index == nil or use_index == "" then
    use_index = true
  else
    use_index = false
  end
  local name = pandoc.utils.stringify(args[1])
  return insert_it("yourturn", name, use_index)
end

insert_view_app = function(args, kwargs, meta) 
  local use_index = args[2]
  if use_index == nil or use_index == "" then
    use_index = true
  else
    use_index = false
  end
  local name = pandoc.utils.stringify(args[1])
  return insert_it("yourview", name, use_index)
end


insert_container = function(args, kwargs, meta)
  quarto.doc.add_html_dependency({
    name = "yourturnIframeContainer",
    version = "0.1.0",
    scripts = {
      "yourturn-iframeContainer.js",
      "iframe-resizer.parent.js"
    },
  })

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

insert_child = function(args, kwargs, meta)
  quarto.doc.add_html_dependency({
    name = "yourturnIframeChild",
    version = "0.1.0",
    scripts = {
      "iframe-resizer.child.js"
    },
  })
  return ''
end


return {
  ['yourturn'] = insert_your_turn,
  ['yourview'] = insert_view_app,
  ['yourturnIframeContainer'] = insert_container,
  ['yourturnChild'] = insert_child
}

