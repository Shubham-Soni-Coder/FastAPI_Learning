from sqlmodel import SQLModel, Field

"This is the model file where i create boiler palate of the database"


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    phone: int
    address: str = Field(max_length=100)
