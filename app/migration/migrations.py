from app.module import dbModule


MIGRATION_HEAD = int(input())

# input 0 to create table "test_table" with columns "test_id", "test_data"


def create_test_table():
    db_module = dbModule.Database()

    query = "CREATE TABLE test_table_2 (test_id INT AUTO_INCREMENT PRIMARY KEY, test_data VARCHAR(255))"

    db_module.execute(query)

    db_module.commit()


MIGRATIONS = [
    create_test_table
]


def run_migration():
    for migration in MIGRATIONS[MIGRATION_HEAD:]:
        migration()


run_migration()
