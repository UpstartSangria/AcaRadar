# frozen_string_literal: true

require 'rspec/core/rake_task'
require_relative 'require_app'

CODE = 'app/'

task :run do
  sh 'bundle exec puma'
end

# Run all specs under spec/
desc 'Run all RSpec tests'
RSpec::Core::RakeTask.new(:spec) do |t|
  t.pattern = 'spec/**/*_spec.rb'
  t.rspec_opts = ['--format documentation']
end

task :default => :spec

namespace :db do
  task :config do
    require 'sequel'
    require_relative 'config/environment'

    def app = AcaRadar::App
  end

  desc 'Run migration'
  task migrate: :config do
    Sequel.extension :migration
    puts "Migrating #{app.environment} database to latest"
    Sequel::Migrator.run(app.db, 'db/migrations')
  end

  desc 'Wipe records from all tables'
  task wipe: :config do
    if app.environment == :production
      puts 'Do not damage the production database!'
      return
    end

    require_app(%w[models infrastructure])
    require_relative 'spec/helpers/database_helper'
    DatabaseHelper.wipe_database
  end

  desc 'Delete dev or test database file (set correct RACK_ENV)'
  task drop: :config do
    if app.environment == :production
      puts 'Do not damage production database!'
      return
    end

    FileUtils.rm(AcaRadar::App.config.DB_FILENAME)
    puts "Deleted #{AcaRadar::App.config.DB_FILENAME}"
  end
end

desc 'Run application console'
task :console do
  sh 'pry -r ./load_all'
end

namespace :vcr do
  desc 'delete cassette fixtures'
  task :wipe do
    sh 'rm spec/fixtures/cassettes/*.yml' do |ok, _|
      puts(ok ? 'Cassettes deleted' : 'No cassettes found')
    end
  end
end

namespace :quality do
  desc 'run all static-analysis quality checks'
  task all: %i[rubocop reek flog]

  desc 'code style linter'
  task :rubocop do
    sh 'rubocop'
  end

  desc 'code smell detector'
  task :reek do
    sh 'reek'
  end

  desc 'complexity analysis'
  task :flog do
    sh "flog #{CODE}"
  end
end
