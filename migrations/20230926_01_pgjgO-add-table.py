"""
add table user
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""
    CREATE TABLE users (
         uid BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
         created_at timestamp with time zone not null default current_timestamp,
         updated_at timestamp with time zone not null default current_timestamp,
         username varchar(128) unique not null,
         password varchar(128) not null
    )
    """,
    """
    DROP TABLE users;
    """
         )
]
