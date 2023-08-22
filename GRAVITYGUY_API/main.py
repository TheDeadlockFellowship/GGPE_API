from fastapi import FastAPI
from core.database import Database
from daos.model_dao import ModelDao
from daos.input_dao import InputDao
from daos.runs_dao import RunDao
from endpoints.server_route import router4
from endpoints.run_route import init_routes3, router3
from endpoints.input_route import init_routes2, router2
from endpoints.model_route import init_routes1, router1
from core.TablesCreation import create_tables

# Initialize the database connection pool
db = Database()
db.initialize()
create_tables()

# Create an instance of the ItemDAO
run_dao = RunDao(db)
model_dao = ModelDao(db)
input_dao = InputDao(db)
# Initialize the routes with the ItemDAO
init_routes3(run_dao)
init_routes2(input_dao)
init_routes1(model_dao)

# Create the FastAPI app and include the routes
app = FastAPI()
app.include_router(router1)
app.include_router(router2)
app.include_router(router3)
app.include_router(router4)

# Run the FastAPI app with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)




