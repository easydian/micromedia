
class Controller
  constructor: () ->
    # get, post, delete, put
    @routes = [
      {path: "/",              http_method: "get",   method: "index" },
      {path: "/monitor",       http_method: "get",   method: "index" },
      {path: "/tasks",         http_method: "get",   method: "get_seeds"},
      {path: "/heartbeat/:id", http_method: "put",   method: "keep_alive"},
      {path: "/result/:id",    http_method: "put",   method: "raw_result"},
      {path: "/errorinfo/:id", http_method: "put",   method: "error_info"},
      {path: "/status",        http_method: "get",   method: "worker_status"}
      ]
    return
    
  #show the index page
  index: (req, res) ->    
    res.render 'index.ejs'

  get_seeds: (req, res) ->
    logger.info "--------->a request"
    res.json{
      "type":"sina",
      "roster":[
          "http://www.weibo.com/kaifulee",
          "http://weibo.com/nonoidea"
      ]
    }
  raw_result: (req, res) ->

  error_info: (req, res) ->

  work_status: (req, res) ->


module.exports = Controller
