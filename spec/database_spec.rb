# frozen_string_literal: true

require 'spec_helper'
require 'sequel' 
DB = Sequel.sqlite  
Sequel::Model.db = DB     

require_relative 'helpers/database_helper'
DatabaseHelper.setup_test_db

require_relative '../app/infrastructure/database/orm/paper_orm'
require_relative '../app/infrastructure/database/orm/author_orm'
require_relative '../app/infrastructure/database/orm/category_orm'
require_relative '../app/infrastructure/database/orm/paper_authors_orm'
require_relative '../app/infrastructure/database/orm/paper_categories_orm'


module AcaRadar
  module Database
    RSpec.describe 'Database Integration' do
      before(:each) do
        DatabaseHelper.wipe_database
      end

      # PaperOrm basic CRUD

      describe PaperOrm do
        let(:paper_info) { { paper_id: 'p123', title: 'AcaRadar Study' } }

        it 'creates and retrieves a paper' do
          paper = described_class.create(paper_info)
          found = described_class.first(paper_id: 'p123')
          expect(found.title).to eq('AcaRadar Study')
        end

        it 'finds or creates correctly' do
          first = described_class.find_or_create(paper_info)
          second = described_class.find_or_create(paper_info)
          expect(second.id).to eq(first.id)
          expect(described_class.count).to eq(1)
        end

        it 'tracks timestamps on creation' do
          paper = described_class.create(paper_info)
          expect(paper.created_at).not_to be_nil
          expect(paper.updated_at).not_to be_nil
        end
      end


      # AuthorOrm

      describe AuthorOrm do
        let(:author_info) { { name: 'Alice' } }

        it 'creates and retrieves an author' do
          author = described_class.create(author_info)
          found = described_class.first(name: 'Alice')
          expect(found.name).to eq('Alice')
        end

        it 'finds or creates without duplication' do
          first = described_class.find_or_create(author_info)
          second = described_class.find_or_create(author_info)
          expect(second.id).to eq(first.id)
          expect(described_class.count).to eq(1)
        end
      end


      # CategoryOrm

      describe CategoryOrm do
        let(:cat_info) { { arxiv_name: 'cs.AI' } }

        it 'creates and retrieves a category' do
          category = described_class.create(cat_info)
          found = described_class.first(arxiv_name: 'cs.AI')
          expect(found.arxiv_name).to eq('cs.AI')
        end

        it 'finds or creates without duplication' do
          first = described_class.find_or_create(cat_info)
          second = described_class.find_or_create(cat_info)
          expect(second.id).to eq(first.id)
          expect(described_class.count).to eq(1)
        end
      end


      # PaperAuthorOrm (junction)

      describe PaperAuthorOrm do
        it 'links papers and authors' do
          paper = PaperOrm.create(paper_id: 'p123', title: 'Joint Paper')
          author = AuthorOrm.create(name: 'Bob')
          link = described_class.find_or_create(paper_id: paper.id, author_id: author.id)

          expect(link.paper_id).to eq(paper.id)
          expect(link.author_id).to eq(author.id)
          expect(paper.authors.map(&:name)).to include('Bob')
        end
      end


      # PaperCategoryOrm (junction)

      describe PaperCategoryOrm do
        it 'links papers and categories' do
          paper = PaperOrm.create(paper_id: 'p999', title: 'Deep Learning')
          category = CategoryOrm.create(arxiv_name: 'cs.LG')
          link = described_class.find_or_create(paper_id: paper.id, category_id: category.id)

          expect(link.paper_id).to eq(paper.id)
          expect(link.category_id).to eq(category.id)
          expect(paper.categories.map(&:arxiv_name)).to include('cs.LG')
        end
      end


      # Full relationship integration

      describe 'relationships across all ORMs' do
        it 'handles paper-author-category relations correctly' do
          paper = PaperOrm.create(paper_id: 'p111', title: 'AI Research')
          author1 = AuthorOrm.create(name: 'Alice')
          author2 = AuthorOrm.create(name: 'Bob')
          cat = CategoryOrm.create(arxiv_name: 'cs.AI')

          paper.add_author(author1)
          paper.add_author(author2)
          paper.add_category(cat)

          expect(paper.authors.map(&:name)).to contain_exactly('Alice', 'Bob')
          expect(paper.categories.map(&:arxiv_name)).to contain_exactly('cs.AI')

          # check back-links
          expect(author1.papers.map(&:title)).to include('AI Research')
          expect(cat.papers.map(&:title)).to include('AI Research')
        end
      end
    end
  end
end
