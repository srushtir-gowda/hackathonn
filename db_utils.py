import sqlite3

# Create or connect to the SQLite database
conn = sqlite3.connect("recruitment.db")
cursor = conn.cursor()

# Create table for job postings
cursor.execute('''
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    skills TEXT, -- comma-separated skills or parsed with embeddings
    experience TEXT
)
''')

# Create table for candidates
cursor.execute('''
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    skills TEXT, -- comma-separated or embedded for matching
    experience TEXT,
    resume TEXT -- optional path to resume file or text
)
''')

# Create table for candidate-job matches
cursor.execute('''
CREATE TABLE IF NOT EXISTS matches (
    job_id INTEGER,
    candidate_id INTEGER,
    match_score REAL, -- score between 0 and 1 (or 0–100)
    shortlisted INTEGER DEFAULT 0, -- 1 if shortlisted
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    FOREIGN KEY (candidate_id) REFERENCES candidates(id),
    PRIMARY KEY (job_id, candidate_id)
)
''')

# Create table for interviews
cursor.execute('''
CREATE TABLE IF NOT EXISTS interviews (
    candidate_id INTEGER,
    job_id INTEGER,
    interview_time TEXT, -- ISO 8601 format (e.g., 2025-04-10T15:30)
    status TEXT CHECK (status IN ('Scheduled', 'Completed', 'Rejected', 'Pending')),
    FOREIGN KEY (candidate_id) REFERENCES candidates(id),
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    PRIMARY KEY (candidate_id, job_id)
)
''')

# Commit and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully.")
