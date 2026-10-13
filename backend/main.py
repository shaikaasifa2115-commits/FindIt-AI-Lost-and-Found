from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import client, items_collection
from models import LostItem, FoundItem
from bson import ObjectId
from ai_matching import find_matching_items


app = FastAPI(title="AI Lost and Found API")


# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Check whether an identical report already exists
def find_duplicate(item_data, status):
    return items_collection.find_one({
        "item_name": item_data["item_name"],
        "description": item_data["description"],
        "location": item_data["location"],
        "date": item_data["date"],
        "contact": item_data["contact"],
        "status": status,
    })


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "AI Lost and Found API is running!"
    }


# Test MongoDB connection
@app.get("/db-test")
def database_test():
    try:
        client.admin.command("ping")

        return {
            "message": "MongoDB connection successful!"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"MongoDB connection failed: {str(e)}"
        )


# Report a lost item
@app.post("/items/lost")
def report_lost_item(item: LostItem):
    try:
        item_data = item.model_dump()
        item_data["status"] = "lost"

        # Prevent duplicate lost-item reports
        existing_item = find_duplicate(item_data, "lost")

        if existing_item:
            raise HTTPException(
                status_code=409,
                detail="This lost item has already been reported."
            )

        # Save the new lost item
        result = items_collection.insert_one(item_data)

        lost_item = items_collection.find_one({
            "_id": result.inserted_id,
            "status": "lost"
        })

        if not lost_item:
            raise HTTPException(
                status_code=500,
                detail="Lost item was saved but could not be retrieved."
            )

        # Retrieve found items
        found_items = list(
            items_collection.find({
                "status": "found"
            })
        )

        # Find AI matches
        matches = find_matching_items(
            lost_item,
            found_items
        )

        return {
            "message": "Lost item added successfully!",
            "item_id": str(result.inserted_id),
            "matches": matches
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error reporting lost item: {str(e)}"
        )


# Report a found item
@app.post("/items/found")
def report_found_item(item: FoundItem):
    try:
        item_data = item.model_dump()
        item_data["status"] = "found"

        # Prevent duplicate found-item reports
        existing_item = find_duplicate(item_data, "found")

        if existing_item:
            raise HTTPException(
                status_code=409,
                detail="This found item has already been reported."
            )

        # Save the new found item
        result = items_collection.insert_one(item_data)

        found_item = items_collection.find_one({
            "_id": result.inserted_id,
            "status": "found"
        })

        if not found_item:
            raise HTTPException(
                status_code=500,
                detail="Found item was saved but could not be retrieved."
            )

        # Retrieve lost items
        lost_items = list(
            items_collection.find({
                "status": "lost"
            })
        )

        # Find AI matches
        matches = find_matching_items(
            found_item,
            lost_items
        )

        return {
            "message": "Found item added successfully!",
            "item_id": str(result.inserted_id),
            "matches": matches
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error reporting found item: {str(e)}"
        )


# Find found items matching a lost item
@app.get("/items/{lost_item_id}/matches")
def get_matches(lost_item_id: str):

    if not ObjectId.is_valid(lost_item_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid lost item ID."
        )

    try:
        lost_item = items_collection.find_one({
            "_id": ObjectId(lost_item_id),
            "status": "lost"
        })

        if not lost_item:
            raise HTTPException(
                status_code=404,
                detail=(
                    "Lost item not found. "
                    "Check that the ID belongs to an item "
                    "whose status is 'lost'."
                )
            )

        found_items = list(
            items_collection.find({
                "status": "found"
            })
        )

        matches = find_matching_items(
            lost_item,
            found_items
        )

        return {
            "lost_item": {
                "item_id": str(lost_item["_id"]),
                "item_name": lost_item.get("item_name"),
                "description": lost_item.get("description"),
                "location": lost_item.get("location"),
                "date": lost_item.get("date")
            },
            "matches": matches
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error finding matches: {str(e)}"
        )


# Find lost items matching a found item
@app.get("/found-items/{found_item_id}/matches")
def get_matches_for_found_item(found_item_id: str):

    if not ObjectId.is_valid(found_item_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid found item ID."
        )

    try:
        found_item = items_collection.find_one({
            "_id": ObjectId(found_item_id),
            "status": "found"
        })

        if not found_item:
            raise HTTPException(
                status_code=404,
                detail=(
                    "Found item not found. "
                    "Check that the ID belongs to an item "
                    "whose status is 'found'."
                )
            )

        lost_items = list(
            items_collection.find({
                "status": "lost"
            })
        )

        matches = find_matching_items(
            found_item,
            lost_items
        )

        return {
            "found_item": {
                "item_id": str(found_item["_id"]),
                "item_name": found_item.get("item_name"),
                "description": found_item.get("description"),
                "location": found_item.get("location"),
                "date": found_item.get("date")
            },
            "matches": matches
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error finding matches: {str(e)}"
        )