def taskEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "title": item["title"],
        "is_open": item["is_open"],
        "created_at": item["created_at"],
    }
    
def tasksEntity(entity) -> list:
    return [taskEntity(item) for item in entity]