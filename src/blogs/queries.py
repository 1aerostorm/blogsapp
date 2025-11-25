from django.db import connection

def fetch_posts(author_id=None, sort_by='created_at', sort_order='desc', offset=0, limit=10):
    query = """
        SELECT 
            p.id,
            p.title,
            p.description,
            p.content,
            p.image,
            p.created_at,

            -- author
            a.id AS author_id,
            a.username AS author_username,
            a.email AS author_email,

            -- last comment
            lc.id AS last_comment_id,
            lc.content AS last_comment_body,
            lc.created_at AS last_comment_created_at,
            lc.username AS last_comment_author
        FROM blogs_post p

        JOIN blogs_account a ON p.author_id = a.id

        OUTER APPLY (
            SELECT TOP 1 *
            FROM blogs_comment c
            WHERE c.post_id = p.id
            ORDER BY c.created_at DESC
        ) lc
    """

    params = []
    if author_id:
        query += " WHERE a.id = %s"
        params.append(author_id)

    query += f" ORDER BY p.{sort_by} {sort_order}"

    query += " OFFSET %s ROWS FETCH NEXT %s ROWS ONLY"
    params.extend([offset, limit])

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        rows = cursor.fetchall()

    return rows

def submit_post(author_id, title, description, content=None, image=None):
    query = """
        INSERT INTO blogs_post (title, description, content, image, created_at, author_id)
        VALUES (%s, %s, %s, %s, GETDATE(), %s)
    """

    params = [
        title,
        description,
        content,
        image,
        author_id
    ]

    with connection.cursor() as cursor:
        cursor.execute(query, params)

def get_post(post_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                p.id,
                p.title,
                p.description,
                p.content,
                p.image,
                p.created_at,

                a.id AS author_id,
                a.username AS author_username,
                a.email AS author_email
            FROM blogs_post p
            JOIN blogs_account a ON p.author_id = a.id
            WHERE p.id = %s
        """, [post_id])
        post_row = cursor.fetchone()
    return post_row

def get_post_comments(post_id, offset=0, limit=20):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, username, content, created_at
            FROM blogs_comment
            WHERE post_id = %s
            ORDER BY created_at DESC
            OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
        """, [post_id, offset, limit])
        comments_rows = cursor.fetchall()
    return comments_rows