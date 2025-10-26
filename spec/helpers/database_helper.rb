# frozen_string_literal: true

module DatabaseHelper

    def self.setup_test_db
        DB.create_table :papers do
            primary_key :id
            String :paper_id
            String :title
            DateTime :created_at
            DateTime :updated_at
          end
          
          DB.create_table :authors do
            primary_key :id
            String :name
            DateTime :created_at
            DateTime :updated_at
          end
          
          DB.create_table :categories do
            primary_key :id
            String :arxiv_name
            DateTime :created_at
            DateTime :updated_at
          end
          
          DB.create_table :paper_authors do
            primary_key :id
            foreign_key :paper_id, :papers
            foreign_key :author_id, :authors
            DateTime :created_at
            DateTime :updated_at
          end
          
          DB.create_table :paper_categories do
            primary_key :id
            foreign_key :paper_id, :papers
            foreign_key :category_id, :categories
            DateTime :created_at
            DateTime :updated_at
          end
    end

    def self.wipe_database
      AcaRadar::Database::PaperAuthorOrm.dataset.delete
      AcaRadar::Database::PaperCategoryOrm.dataset.delete
      AcaRadar::Database::PaperOrm.dataset.delete
      AcaRadar::Database::AuthorOrm.dataset.delete
      AcaRadar::Database::CategoryOrm.dataset.delete
    end
  end
  