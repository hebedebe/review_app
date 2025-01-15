import json
import uuid
import utils

class Review:
    def __init__(self, owner_username, rating, title, description, image_id = None, id = None, comments = [], reviews = [],
                 parent_uuid = None, owner_uuid = None):
        if id is None:
            self.id = utils.generate_uuid()
        else:
            self.id = id

        self.owner_username = owner_username
        self.owner_uuid = owner_uuid
        self.rating = rating
        self.title = title
        self.description = description
        self.image_id = image_id
        self.comments = comments
        self.reviews = reviews
        self.parent_uuid = parent_uuid

    def __str__(self):
        return f"Review with id {self.id}"


class User:
    def __init__(self, name, bio = "", image_id = None, id = None):
        self.name = name
        self.bio = bio
        self.image_id = image_id

        if id is None:
            self.uuid = utils.generate_uuid()
        else:
            self.uuid = id

    def __str__(self):
        return f"User {self.name} with uuid {self.uuid}"

    def load_from_disk():
        user_dict = utils.read_json_contents("user_data.json")
        name = user_dict["name"]
        bio = user_dict["bio"]
        image_id = user_dict["image_id"]
        id = user_dict["uuid"]
        user = User(name, bio, image_id, id)
        print("Loaded user data from disk successfully")
        return user

    def save_to_disk(self):
        with open("user_data.json", "w") as f:
            json_form = json.dumps({
                "name": self.name,
                "bio": self.bio,
                "image_id": self.image_id,
                "uuid": self.uuid
            })
            f.write(json_form)
            f.close()
        print("Saved user data to disk successfully")