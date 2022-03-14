import sqlite3
       

class DataBase:
    __instance = False
    
    def __new__(cls, *args: list, **kwargs: dict):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        else:
            print("Класс БД уже создан!")
        return cls.__instance
    
    def __init__(self, path: str) -> None:
        if self.__instance is None:
            return 
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.cursor = self.db.cursor()
        self.create_database()
    
    def create_database(self):
        with self.db:
            self.cursor.execute("""
                           CREATE TABLE IF NOT EXISTS films (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               title text,
                               cover text,
                               director text,
                               actors text, 
                               data_created text,
                               description text,
                               link text,
                               hls_link text
                           )
                           """)
    
    def add_film(self, film):
        with self.db:
            self.cursor.execute("INSERT INTO films (title, cover, director, actors, data_created, description, link, hls_link) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (film.title, film.cover, film.director, film.actors, film.data_created, film.description, film.link, film.hls_link))

    def get_films(self, page_range):
        return self.cursor.execute(f"SELECT * FROM films WHERE id BETWEEN {page_range[0]} and {page_range[1]}").fetchall()
    
    def get_film(self, _id):
        return self.cursor.execute("SELECT * FROM films WHERE id = ?", (_id,)).fetchone()
    
    def find_by_title(self, query):
        return self.cursor.execute(f"SELECT * FROM films WHERE title_lower LIKE '%{query.lower()}%'").fetchall()
    
    def get_count_films(self):
        return self.cursor.execute("SELECT COUNT(*) FROM films").fetchone()