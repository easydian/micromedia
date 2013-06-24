# Configuration

global.config = {
  LOG_LEVEL: "info",
  LISTEN_PORT: 6565,
}

global.Async        = require 'async'
global.Step         = require 'step'
global.logger       = new (require './logger')("micromedia")





