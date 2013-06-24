require './micromedia/config'

console.log "main...."
console.log "micromedia"

Server = require './micromedia/server'
new Server().start()