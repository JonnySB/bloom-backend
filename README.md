# drip-backend

# Project Setup

```shell
# Clone the repository to your local machine
; git clone https://github.com/JonnySB/drip-backend

; cd drip-backend

# Install dependencies and set up the virtual environment
; pipenv install

# Activate the virtual environment
; pipenv shell

# Create a test and development database (This assumes you have postgres)
; createdb DRIP
; createdb DRIP_test

# Seed the development database (ensure you have run `pipenv shell` first)
; python seed_dev_database.py

# Run the tests (with extra logging)
; pytest -sv

# Run the server
; python app.py
```
