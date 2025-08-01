import sqlite3

def get_connection():
    return sqlite3.connect("resume_extractor.db", check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Jobs Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT NOT NULL
        )
    """)

    # Applications Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            job_id INTEGER,
            first_name TEXT,
            last_name TEXT,
            education TEXT,
            experience TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (job_id) REFERENCES jobs(id)
        )
    """)

    conn.commit()

    # Seed Jobs
    seed_jobs(conn)

    conn.close()

def seed_jobs(conn):
    cursor = conn.cursor()
    # Check if jobs already exist
    cursor.execute("SELECT COUNT(*) FROM jobs")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany("""
            INSERT INTO jobs (title, company, location) 
            VALUES (?, ?, ?)
        """, [
            ('Data Scientist', 'Google', 'Bangalore'),
            ('ML Engineer', 'Amazon', 'Hyderabad'),
            ('AI Researcher', 'Capegemini', 'Remote')
        ])
        conn.commit()

def add_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        raise Exception("Username already exists")
    finally:
        conn.close()

def verify_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def get_user_id(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_jobs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs")
    jobs = [{"id": row[0], "title": row[1], "company": row[2], "location": row[3]} for row in cursor.fetchall()]
    conn.close()
    return jobs

def apply_for_job(user_id, job_id, first_name, last_name, education, experience):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO applications (user_id, job_id, first_name, last_name, education, experience)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, job_id, first_name, last_name, education, experience))
    conn.commit()
    conn.close()

def has_applied(user_id, job_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM applications WHERE user_id=? AND job_id=?", (user_id, job_id))
    result = cursor.fetchone()
    conn.close()
    return result is not None
