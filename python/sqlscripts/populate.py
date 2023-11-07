import psycopg2

# Establish a connection to the database by creating a cursor object
# The PostgreSQL server must be accessed through the PostgreSQL APP or Terminal Shell

# conn = psycopg2.connect("dbname=suppliers port=5432 user=postgres password=postgres")

# Or:
conn = psycopg2.connect(host="postgres", port = 5432, database="auto_marking_api", user="ZibkEQqKrTzNJjcTjNOzlthOTygrTMqw", password="RrMXGW9y1mSXNEAhKY2Yk63MaJyVluZFGzMUBjMmt4Dai8QOvv65L4SbG4sjP4yB")

# Create a cursor object
cur = conn.cursor()

# A sample query of all data from the "vendors" table in the "suppliers" database
cur.execute("""SELECT * FROM questions_question""")
query_results = cur.fetchall()
print(query_results)

# Close the cursor and connection to so the server can allocate
# bandwidth to other requests
cur.close()
conn.close()