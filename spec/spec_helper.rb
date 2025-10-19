# frozen_string_literal: true

require 'yaml'
require 'minitest/autorun'
require 'minitest/rg'
require 'vcr'
require 'webmock'
require 'simplecov'

<<<<<<< HEAD
=======
require_relative '../app/models/gateways/arxiv_api'
require_relative '../helper/arxiv_api_parser'

>>>>>>> b57bdd0153fed0feeeb37a65429240b2687bb6c9
CONFIG = YAML.safe_load_file('config/secrets.yml', aliases: true)
CORRECT = YAML.safe_load_file('spec/fixtures/arxiv_results.yml', aliases: true)

CASSETTES_FOLDER = 'spec/fixtures/cassettes'
CASSETTE_FILE = 'arxiv_api'

SimpleCov.start
