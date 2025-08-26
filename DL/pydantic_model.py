from pydantic import BaseModel
class User(BaseModel):
    id: int
    name: str
    age: int
    is_active: bool = True

user = User(id="123", name="Alice", age="30")

print(user)
print(user.model_dump())
print(user.model_dump_json())
