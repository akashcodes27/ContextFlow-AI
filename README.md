




pip install sqlalchemy psycopg2-binary
pip install redis
pip install qdrant-client
pip install sqlalchemy alembic passlib[bcrypt]
pip install python-jose[cryptography] passlib[bcrypt] python-multipart


To test postgres connection we did
docker compose exec postgres psql -U postgres -d contextflow 

contextflow=# \dt 
contextflow=# \d users

Command enables us to write SQL queries against the Postgres DB 
docker compose exec postgres psql -U postgres -d contextflow 





RAG dependencies 
pip install langchain
pip install langgraph
pip install langchain-community
pip install langchain-huggingface
pip install langchain-qdrant
pip install sentence-transformers
pip install pypdf
pip install python-docx
pip install unstructured
pip install fastembed