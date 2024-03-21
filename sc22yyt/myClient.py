import requests
import json

default_url = None
session = requests.Session()

def login(url):
    global default_url

    if not url.startswith(('http://', 'https://')):
        url = f'http://{url}'

    default_url = url

    login_url = f'{default_url}/api/login'

    # ask user to input username and password
    username = input("Username: ")
    password = input("Password: ")

    r = session.post(login_url, data={'username': username, 'password': password})

    if r.status_code == 200:
        print(r.text)
    else:
        print(r.text)

def logout():

    r = session.post(f"{default_url}/api/logout")

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
    
    r = session.post(f"{default_url}/api/stories", data=json_data, headers={'Content-Type': 'application/json'})
    
    if r.status_code == 201:
        print("Story posted successfully.")
    else:
        print("Failed to post story: " + r.text)

def news(id, cat, reg, date):
    if default_url is None:
        print("Error, authentication required")
        return

    query_params = {}
    if id:
        query_params['id'] = id
    if cat:
        query_params['category'] = cat
    if reg:
        query_params['region'] = reg
    if date:
        query_params['date'] = date
    
    stories_url = f'{default_url}/api/stories'
    
    response = session.get(stories_url, params=query_params)
    
    if response.status_code == 200:
        stories = response.json().get('stories', [])
        for story in stories:
            print(f"Headline: {story['headline']}, Category: {story['story_cat']}, Region: {story['story_region']}, Date: {story['story_date']}")
    else:
        print(f"Failed to get news: {response.text}")

def list():
    print("Services:")
    print("1. Register Agency")
    print("2. List Agencies")

    choice = input("Enter the number of the service (1/2): ")
    if choice == '1':
        register()
    elif choice == '2':
        list_agencies()
    else:
        print("Invalid input.")
        return

def register():
    agency_name = input("Agency name: ")
    url = input("Agency url: ")
    agency_code = input("Agency code: ")

    agency_data = {
        "agency_name": agency_name,
        "url": url,
        "agency_code": agency_code
    }

    response = session.post(f"{default_url}/api/directory/", json=agency_data)

    if response.status_code == 201:
        print("Agency registered successfully.")
    else:
        print(f"Error when registering agency. Status code: {response.status_code}")
        print(f"Response text: {response.text}")

def list_agencies():
    response = session.get(f'{default_url}/api/directory/')

    if response.status_code == 200:
        agencies = response.json().get('agency_list', [])
        for agency in agencies:
            print(f"Agency Name: {agency['agency_name']}, URL: {agency['url']}, Code: {agency['agency_code']}")
    else:
        print(f"Failed to list agencies: {response.text}")

def delete_story(story_key):
    response = session.delete(f"{default_url}/api/stories/{story_key}")
    
    if response.status_code == 200:
        print("Story deleted successfully.")
    else:
        print(f"Failed to delete story: {response.text}")

if __name__ == "__main__":
    while True:
        command = input("Enter command (login, logout, post, news, list, delete, exit): ")
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
        elif command_split[0].lower() == "delete" and len(command_split) == 2:
            delete_story(command_split[1])
        elif command_split[0].lower() == "news":
            valid_params = ['-id', '-cat', '-reg', '-date']
            id = None
            cat = None
            reg = None
            date = None

            invalid_param = False

            for part in command_split[1:]:
                # seperate the key and variable
                if '=' in part:
                    key, variable = part.split('=', 1)

                    # retrieve variable in quote
                    variable = variable.strip('"').strip("'")
                    if key in valid_params:
                        if key == '-id':
                            id = variable
                        elif key == '-cat':
                            cat = variable
                        elif key == '-reg':
                            reg = variable
                        elif key == '-date':
                            date = variable
                    else:
                        print(f"Invalid parameter: {key}")
                        invalid_param = True
                        break
                else:
                    print(f"Invalid parameter: {part}")
                    invalid_param = True
                    break
            
            if not invalid_param:
                news(id, cat, reg, date)
        elif command.lower() == "list":
            list()
        else:
            print("Unknown command. Please choose from: login, logout, post, news, list, delete, exit.")
