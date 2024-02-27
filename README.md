# bloom-backend

# Project Setup

```shell
# Clone the repository to your local machine
; git clone https://github.com/JonnySB/bloom-backend

; cd bloom-backend

# Install dependencies and set up the virtual environment
; pipenv install

# Activate the virtual environment
; pipenv shell

# Create a test and development database (This assumes you have postgres)
; createdb BLOOM
; createdb BLOOM_test

# Seed the development database (ensure you have run `pipenv shell` first)
; python seed_dev_database.py

# Run the tests (with extra logging)
; pytest -sv

# Run the server
; python app.py
```
