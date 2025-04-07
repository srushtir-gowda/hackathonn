import sqlite3
from typing import Dict

# === CONFIG ===
DB_PATH = "agents.db"

# === MOCK LLM WRAPPER ===
def query_ollama(prompt: str) -> Dict:
    print("🧠 Prompt sent to LLM:\n", prompt[:300], "...\n")
    return {
        "score": 87,
        "shortlist": True,
        "reasons": ["Strong Python and SQL experience", "Relevant backend development"],
    }

# === DATABASE SETUP (ONLY RUN ONCE TO ADD TEST DATA) ===
def insert_test_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY, description TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS candidates (id INTEGER PRIMARY KEY, resume_text TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS shortlisted (job_id INTEGER, candidate_id INTEGER, score INTEGER, reasons TEXT)")

    cur.execute("INSERT OR REPLACE INTO jobs (id, description) VALUES (?, ?)", (
        1,
        "Looking for a software engineer with strong Python and SQL skills, and 2+ years of experience in backend development."
    ))
    cur.execute("INSERT OR REPLACE INTO candidates (id, resume_text) VALUES (?, ?)", (
        2,
        "Experienced backend developer with expertise in Python, SQL, Django, and REST APIs. 3 years of work experience in SaaS startups."
    ))

    conn.commit()
    conn.close()

# === FETCH TEXTS ===
def fetch_text_from_db(job_id: int, candidate_id: int) -> Dict[str, str]:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT description FROM jobs WHERE id=?", (job_id,))
    job = cur.fetchone()

    cur.execute("SELECT resume_text FROM candidates WHERE id=?", (candidate_id,))
    candidate = cur.fetchone()

    conn.close()

    if not job or not candidate:
        raise ValueError("Invalid job ID or candidate ID.")

    return {
        "job_description": job[0],
        "resume": candidate[0]
    }

# === SHORTLIST FUNCTION ===
def shortlist_candidate(job_id: int, candidate_id: int) -> None:
    print("🚀 Starting shortlisting process...")

    try:
        texts = fetch_text_from_db(job_id, candidate_id)
        jd = texts["job_description"]
        resume = texts["resume"]

        prompt = f"""You are an AI recruiter. Based on the Job Description (JD) and Resume, score the match between 0 and 100.
Also say whether the candidate should be shortlisted, and give 1-2 short reasons.

JD: {jd}

Resume: {resume}

Return in JSON:
{{"score": int, "shortlist": bool, "reasons": list of str}}
"""
        result = query_ollama(prompt)

        if result["shortlist"]:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("INSERT INTO shortlisted (job_id, candidate_id, score, reasons) VALUES (?, ?, ?, ?)",
                        (job_id, candidate_id, result["score"], "; ".join(result["reasons"])))
            conn.commit()
            conn.close()

            print(f"✅ Candidate {candidate_id} shortlisted with score {result['score']}.")
            print("📌 Reasons:", *result["reasons"], sep="\n- ")
        else:
            print(f"❌ Candidate {candidate_id} not shortlisted. Score: {result['score']}")
            print("📌 Reasons:", *result["reasons"], sep="\n- ")

    except Exception as e:
        print("❗ Error during shortlisting:", str(e))


# === RUN EVERYTHING ===
if __name__ == "__main__":
    insert_test_data()  # Comment this line if DB already exists
    shortlist_candidate(job_id=1, candidate_id=2)
