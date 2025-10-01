# frozen_string_literal: true

require 'http'
require 'net/http'
require 'uri'
require 'pry'

def arxiv_api_path(path)
  "http://export.arxiv.org/api/#{path}"
end 


url = URI.parse(arxiv_api_path('query?search_query=all:information&start=0&max_results=5'))
init_res = Net::HTTP.get_response(url)


redirect_url = URI.parse(init_res['location'])
res = Net::HTTP.get_response(redirect_url) #data structure: xml 
# res.body 









