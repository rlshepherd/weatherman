require 'sinatra'
get '/' do
  "hello from #{`uname -a`}"
end

