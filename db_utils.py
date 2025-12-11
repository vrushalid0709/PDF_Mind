import mysql.connector
import config

def get_db_connection():
    """Establishes connection to the database"""
    return mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )

def save_document(filename, summary, sentiment, keywords=None):
    """
    Saves the analysis results to the MySQL table.
    Returns a JSON-ready dictionary containing:
    - status
    - document_id
    - filename
    - data { summary, sentiment, keywords }
    """

    if keywords is None:
        keywords = []

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO documents (filename, summary, sentiment)
        VALUES (%s, %s, %s)
        """
        val = (filename, summary, sentiment)

        cursor.execute(sql, val)
        conn.commit()

        new_id = cursor.lastrowid

        cursor.close()
        conn.close()

        print(f"Saved to DB with ID: {new_id}")

        # Build JSON format to return
        return {
            "status": "success",
            "document_id": new_id,
            "filename": filename,
            "data": {
                "summary": summary,
                "sentiment": {
                    "label": sentiment,
                    "score": None  # Optional
                },
                "keywords": keywords,
                "db_record_id": new_id
            }
        }

    except Exception as e:
        print(f"Error saving to database: {e}")
        return {
            "status": "error",
            "error": str(e)
        }
