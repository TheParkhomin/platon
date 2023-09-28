"""
add table wallet
"""


from yoyo import step

__depends__ = {'20230926_01_pgjgO-add-table'}

steps = [
    step(
        """
        CREATE TABLE wallets (
            uid UUID NOT NULL UNIQUE PRIMARY KEY,
            user_id BIGINT NOT NULL,
            score BIGINT NOT NULL,
            created_at timestamp with time zone not null default current_timestamp,
            updated_at timestamp with time zone not null default current_timestamp
            );
        """,
        """
        DROP TABLE wallets;
        """
    )
]
