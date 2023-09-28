"""
add table wallet
"""


from yoyo import step

__depends__ = {'20230926_01_pgjgO-add-table'}

steps = [
    step(
        """
        CREATE TABLE wallets (
            uid BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            address varchar(128) unique not null,
            user_id BIGINT NOT NULL,
            score BIGINT NOT NULL CHECK(score >= 0),
            created_at timestamp with time zone not null default current_timestamp,
            updated_at timestamp with time zone not null default current_timestamp
            );
        """,
        """
        DROP TABLE wallets;
        """
    )
]
