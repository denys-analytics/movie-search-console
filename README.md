<img width="770" height="380" alt="image" src="https://github.com/user-attachments/assets/47c97a25-853a-4642-bf72-6b12b18a26fb" />

 
 # 🎬 Movie Search Console Application (MongoDB Edition)

A fully interactive console-based application for searching movies, browsing results with pagination, and analyzing user search statistics stored in MongoDB.  
The project uses **MongoDB** both as the main movie database and as the analytics/logging database.  
Architecture is modular and allows connecting **any database type** (MongoDB, SQL, REST API sources) by replacing the connector module.

---

## 📁 Project Structure


```
my_project/
├── main.py                 # Entry point, interactive console menu
├── mongo_connector.py      # MongoDB connection and search queries
├── log_writer.py           # Logging search events into MongoDB
├── log_stats.py            # Retrieving statistics from MongoDB logs
├── formatter.py            # Table formatting and console output styling
├── utils.py                # User input validation utilities
├── config.py               # Application configuration (via environment variables)
├── ui.py                   # Console UI styling (NEO UI)
├── films.json              # Movie dataset (import into MongoDB)
├── categories.json         # Categories dataset
├── film_category.json      # Film-category relations
```


---

## 🚀 Features

### 🔍 Movie Search (MongoDB)
- Search by **keyword** (title)
- Search by **genre and year range**
- Search by **MPAA rating**

### 📊 Statistics (MongoDB)
- TOP‑N keyword searches  
- TOP‑N genre/year searches  
- TOP‑N rating searches  
- Latest unique search queries  

### 📑 Pagination
- Clean, intuitive navigation through search results  
- Dynamic table formatting  
- NEO UI console styling  

### 🛡 Input Validation & Security
The application includes multiple layers of protection:

- Validation of numeric input (IDs, years, ranges)
- Validation of menu commands
- Filtering of invalid characters in text fields
- Prevention of malformed input
- Safe query construction:
  - MongoDB queries use structured dictionaries
  - No string concatenation with raw user input
  - If adapted to SQL, the same structure prevents **SQL injection**

### 🔄 Multi‑Database Support
Although this edition uses MongoDB, the architecture allows:

- swapping the connector module (`mongo_connector.py`)
- adding new connectors:
  - `sql_connector.py` (PostgreSQL, MySQL, SQLite)
  - `api_connector.py` (REST API)
- keeping the same UI, validation, pagination, and logging logic

This makes the project flexible and extendable.

---

## 🧩 Modules Overview

### `main.py`
Interactive menu, search flow, pagination, statistics menu, and application lifecycle.

### `mongo_connector.py`
Handles MongoDB connection and provides search functions:
- `search_by_keyword`
- `search_by_genre_and_years`
- `search_by_rating`
- `get_genres`

Includes automatic data normalization (e.g., converting `release_year` from string to integer).

### `log_writer.py`
Writes search events to MongoDB and provides:
- `log_event`
- `log_search`
- `last_logs`
- `stats_by_event`

### `log_stats.py`
Generates formatted statistics tables from MongoDB logs.

### `formatter.py`
Dynamic table formatting for console output.

### `utils.py`
User input validation:
- integers  
- ranges  
- menu choices  
- pagination commands  
- text validation  

### `config.py`
Centralized configuration using **environment variables**:
- MongoDB URI  
- database name  
- collection names  
- UI width  
- pagination size  

No passwords or sensitive data are stored in the repository.

### `ui.py`
NEO UI styling:
- headers  
- blocks  
- info/success/error messages  

---

## 🛠 Requirements

- Python 3.10+
- `pymongo`

Install dependencies:

```bash
pip install pymongo


---


```

## 🌐 Creating MongoDB Atlas Cluster

### 1️⃣ Create an Atlas Account
Go to **https://www.mongodb.com/cloud/atlas** and register.

### 2️⃣ Create a Free Cluster
Choose **Shared Cluster (Free Tier)**.

### 3️⃣ Create a Database User
Navigate to: Security → Database Access → Add New User

Set:

- **username:** `db_user`  
- **password:** `your_password`  
- **privileges:** `Read/Write`

### 4️⃣ Get Your Connection String (URI)
Navigate to:
Connect → Connect your application

Copy the URI:


### 5️⃣ Add URI to Environment Variables
Create a `.env` file:

```env
MONGO_URI="mongodb+srv://db_user:your_password@cluster0.example.mongodb.net/movie_db?retryWrites=true&w=majority"
MONGO_DB="movie_db"
MONGO_COLLECTION_FILMS="films"
MONGO_COLLECTION_CATEGORIES="categories"
MONGO_COLLECTION_FILM_CATEGORY="film_category"
MONGO_COLLECTION_LOGS="search_events"
TIMEZONE="Europe/Berlin"
PAGE_SIZE=10
UI_WIDTH=60
```

### 📥 Importing Data into MongoDB

Before running the application, import JSON datasets using MongoDB Compass:

Open your database (e.g., movie_db)

Create collections:

films

categories

film_category

For each collection:

Open it

Click Import Data

Select the corresponding JSON file

## ▶️ Running the Application
## 1️⃣ Open terminal in project folder (Windows)
Open the project folder

Click the address bar

Type: cmd

Press Enter

## 2️⃣ Run the app
bash
python main.py

## 📌 Notes

- Update your MongoDB credentials in `config.py`.
- Ensure all JSON datasets are imported before running the application.
- The project is fully modular and easy to extend.

---

## 📜 License

This project is open-source and free to use.

**Author:** Denys Bidiuk  
