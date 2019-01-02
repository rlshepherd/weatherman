require 'rubygems'
require 'sinatra'
require 'sinatra/activerecord'
require 'sqlite3'
require 'json'

ActiveRecord::Base.establish_connection(
  :adapter => "sqlite3",
  :database => "../raspberry-pi/weather.db"
)

class Weather < ActiveRecord::Base
  self.table_name = "weather"
end

get '/weather/latest' do
  @weather = Weather.last
  content_type :json
  { data: @weather}.to_json
end

get "/weather/range" do
  @weather = Weather.where("datetime >= :start_date AND datetime <= :end_date",
                          {start_date: params[:start_date], end_date: params[:end_date]})
  content_type :json
  {data: @weather}.to_json
end
