import sys
from repository import repo

# creates tables and execute orders

repo.create_tables(sys.argv[1])
repo.execute_orders(sys.argv[2], sys.argv[3])
