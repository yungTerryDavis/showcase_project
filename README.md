# PC Firm
Project to practice FastAPI and SQLAlchemy skills, using sql-ex tasks for PC Firm schema.

## Prepare environment
1. Rename example.env to .env and fill in with your values, with reference to config.
2. Create venv and install dependencies
```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## Launch
```sh
# Launch database
docker-compose up -d

# Launch server
uvicorn main:app
```