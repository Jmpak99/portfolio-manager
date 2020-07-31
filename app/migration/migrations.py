from app.module import db_query_module


MIGRATION_HEAD = int(input())

# input 0 to create table "test_table" with columns "test_id", "test_data"

db = db_query_module.Database()
# connection and cursor should be reusable

def create_test_table():
    query = "CREATE TABLE test_table (test_id INT AUTO_INCREMENT PRIMARY KEY, test_data VARCHAR(255))"

    db.execute(query)

    db.commit()

MIGRATIONS = [
    create_test_table
]


def run_migration():
    for migration in MIGRATIONS[MIGRATION_HEAD:]:
        migration()


run_migration()
