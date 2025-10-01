# arXiv API Client
Project to gather useful information from arXiv API
https://info.arxiv.org/help/api/user-manual.html#arxiv-api-users-manual

## Resources
These are objects that could be used in the projects 
- ArXiv Query Title 
- ID (contains the url to the paper)
- Updated 
- Total Results 
- Entry

## Elements
These are objects included in Resources
Entry
- Published 
- Updated 
- Paper Title
- Summary (abstract)
- Author (list of authors)
- arXiv comment 
- arXiv journal reference 
- Categories (arXiv, ACM, or MSC classification)

## Entities
These are objects that could become the database tables 
- Title 
- Summary 
- Total Results 

# Install 
##  Setting up this script 
No need to apply for an API key to use arXiv API, just install the requests library

- Ensure correct version of Ruby install (see `.ruby-version` for `rbenv`)
- Run `bundle install` to install dependencies

## Running this script 
