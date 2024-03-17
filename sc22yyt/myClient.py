import requests
import json

session = requests.Session()

def login(url):
    # ask user to input username and password
    username = input("Username: ")
    password = input("Password: ")

    r = session.post(url, data={'username': username, 'password': password})

    if r.status_code == 200:
        print(r.text)
    else:
        print(r.text)

def logout():

    r = session.post("http://localhost:8000/api/logout")

    if r.status_code == 200:
        print(r.text)
    else:
        print(r.text)

def post_story():
    headline = input("Story headline: ")
    category = input("Story category: ")
    region = input("Story region: ")
    details = input("Story details: ")
    
    if not headline:
        print("The headline cannot be blank.")
        return

    categories = ['pol', 'art', 'tech', 'trivia']
    if category not in categories:
        print(f"Not a valid category. Please choose from: 'pol', 'art', 'tech', 'trivia'.")
        return

    regions = ['uk', 'eu', 'w']
    if region not in regions:
        print(f"Not a valid region. Please choose from: 'uk', 'eu', 'w'.")
        return

    if not details:
        print("Details of the story cannot be blank.")
        return

    story_data = {
        "headline": headline,
        "category": category,
        "region": region,
        "details": details
    }
    
    json_data = json.dumps(story_data)
    
    r = session.post("http://localhost:8000/api/stories", data=json_data, headers={'Content-Type': 'application/json'})
    
    if r.status_code == 201:
        print("Story posted successfully.")
    else:
        print("Failed to post story: " + r.text)

def delete_story(story_key):
    response = session.delete(f"http://localhost:8000/api/stories/{story_key}")
    
    if response.status_code == 200:
        print("Story deleted successfully.")
    else:
        print(f"Failed to delete story: {response.text}")

if __name__ == "__main__":
    while True:
        command = input("Enter command: ")
        # split the command into parts
        command_split = command.split()

        # Check if the first part of the command is 'login' and the length of command is 2
        # second part of the command will be the url
        if command_split[0].lower() == "login" and len(command_split) == 2:
            # pass the 2nd part of the command as url to the login function
            login(command_split[1])
        elif command.lower() == "logout":
            logout()
        elif command.lower() == "post":
            post_story()
        elif command.lower() == "exit":
            break
        if command_split[0].lower() == "delete" and len(command_split) == 2:
            delete_story(command_split[1])
        else:
            print("Unknown command.")
