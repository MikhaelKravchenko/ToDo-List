import json

users_file_name = './data/users.json'

def checkIfUserExists(user_name):
    global users_file_name
    all_users = None

    with open(users_file_name, 'r') as users_file:
        all_users = json.load(users_file)
    
    for obj in all_users['users']:
        if obj['user_name'] == user_name:
            return True

    return False


def addUserToDB(user_name):
    global users_file_name
    all_users = None

    with open(users_file_name, 'r') as users_file:
        all_users = json.load(users_file)

    with open(users_file_name, 'w') as users_file:
        all_users['users'].append({"user_name": user_name})
        json.dump(all_users, users_file, indent=4, sort_keys=True)

    json_data = {
        'counter': 0,
        'todos': []
    }

    user_todos_file_name = './data/todos/%s.json' % user_name

    with open(user_todos_file_name, 'w') as user_todos_file:
        json.dump(json_data, user_todos_file, indent=4, sort_keys=True)


def addToDoItemToDB(user_name, description):
    json_data = None
    user_todos_file_name = './data/todos/%s.json' % user_name
    
    with open(user_todos_file_name, 'r') as user_todos_file:
        json_data = json.load(user_todos_file)

    json_data['counter'] = int(json_data['counter']) + 1
    json_data['todos'].append({"item_id": json_data['counter'], "description": description, "completed": False})

    with open(user_todos_file_name, 'w') as user_todos_file:
        json.dump(json_data, user_todos_file, indent=4, sort_keys=True)


def getAllToDoItemsFromDB(user_name):
    json_data = None
    user_todos_file_name = './data/todos/%s.json' % user_name

    with open(user_todos_file_name, 'r') as user_todos_file:
        json_data = json.load(user_todos_file)

    return json_data['todos']


def markToDoItemAsComplete(user_name, item_id):
    json_data = None

    with open(getToDoFileName(user_name), 'r') as todos_file:
        json_data = json.load(todos_file)

    counter = json_data['counter']
    todos = json_data['todos']
    item_to_mark = None

    for item in todos:
        if int(item['item_id']) == int(item_id):
            item_to_mark = item

    if item_to_mark == None:
        return False
    
    todos.remove(item_to_mark)
    item_to_mark['completed'] = True
    todos.append(item_to_mark)

    json_data = {
        'counter': counter,
        'todos': todos
    }
    
    with open(getToDoFileName(user_name), 'w') as todos_file:
        json.dump(json_data, todos_file, indent=4, sort_keys=True)

    return True


def isUserLoggedIn(session):
    return session.get('username') != None


def getToDoFileName(user_name):
    return './data/todos/%s.json' % user_name
