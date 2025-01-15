from storage_classes import Review, User

test_user = User.load_from_disk()#("test_name")

print(test_user)
test_user.save_to_disk()