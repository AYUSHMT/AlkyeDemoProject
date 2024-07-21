# Django REST API Project

This project is a simple blog-like application with Posts and Comments. It includes functionalities for user authentication, post and comment creation, liking posts, and more.

## Setup Instructions

### Prerequisites

- Python : python==3.10.7
- Django 3.0+ : Django==4.1.2
- Django REST Framework : djangorestframework==3.14.0
- Simple JWT for token-based authentication : djangorestframework-simplejwt==5.3.1
  
### Installation - setup

You can set it up with Docker and local also - With Docker after clone the repo step , follow the below 2 steps, 
1. You just need to build the image using -> docker build -t demo_img .
2. Run the image using -> docker run --name=demo-app -dit -p 8000:8000 demo_img 

1. **Clone the repository:**
   ```bash
   git clone -b demo https://github.com/AYUSHMT/AlkyeDemoProject.git
   cd AlkyeDemoProject
   ```
2. **Create a virtual environment and activate it:**
  ```python3 -m venv venv
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`
  ```
3. **Install the dependencies and Apply Migrations:**
  ```pip install -r requirements.txt
  python3 manage.py makemigrations
  python3 manage.py migrate
```
4. **Create a SuperUser:**
   ```python3 manage.py createsuperuser```
5. **Run the application:**
   ```python3 manage.py runserver 0.0.0.0:8000```

### Pre-requisites before testing

#### Features

- Used Function based views for the simplicity of code.
- Used Serializers in Django REST Framework (DRF) which are used to convert complex data types, such as Django model instances or querysets, into native Python data types that can then be easily rendered into JSON, XML, or other content types.
-  Added Likes and Pagination Feature (with Pagination no - 2).
-  Used Simple JWT for token-based authentication.
-  Added Basic Tests for models and API views.
-  In case of any queries while testing or with setup, feel free to contact me - ayush02rajput@gmail.com

#### Flow to test

1. Create a SuperUser using - python3 manage.py createsuperuser.
2. Retrieve the token of superuser for testing the actions.
3. U can either register a new user or use the superuser only for testing, for registering a new user use Register a User endpoint (http://localhost:8000/api/register/).
4. Try creating a post or multiple posts with different parameters values in request body using endpoint (http://localhost:8000/api/posts/). [Author name was ambiguous as I had a doubt of taking it automatically using request.user (from token) or should be taken from the request body. Currently I am taking that from the request body , can modify if needed]
5. Test Updating and deleting a post.
6. Test List Posts using http://localhost:8000/api/posts/.
7. Test Pagination with http://localhost:8000/api/postPagination/ (Pagination Count-2)
8. Test Create a Comment for a Post, then try listing comments for a post.
9. Can like & unlike a post using the same endpoint (http://localhost:8000/api/posts/Post1/like/) and verify the like count.
10. In case of any queries while testing or with setup, feel free to contact me - ayush02rajput@gmail.com.

### Sample Curl Requests for testing 

##### List Posts:
```- curl -X GET http://localhost:8000/api/posts/```

##### Create a Post:
- curl -X POST http://localhost:8000/api/posts/ -d '{"title": "Post1", "content": "This is the content of the post.", "author":"username"}' -H "Content-Type: application/json" -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"

##### Get Paginated Posts:
- curl -X GET http://localhost:8000/api/postPagination/
- curl -X GET "http://localhost:8000/api/postPagination/?page=2"

##### Get Post Details:
- curl -X GET http://localhost:8000/api/posts/Post1/

##### Update a Post:
- curl -X PUT http://localhost:8000/api/posts/Post1/ -d '{"title": "UpdatedPost", "content": "Updated content."}' -H "Content-Type: application/json" -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"

##### Delete a Post:
- curl -X DELETE http://localhost:8000/api/posts/Post1/ -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"

##### List Comments for a Post:
- curl -X GET http://localhost:8000/api/posts/Post1/comments/

##### Create a Comment for a Post:
- curl -X POST http://localhost:8000/api/posts/Post1/comments/ -d '{"text": "This is a comment."}' -H "Content-Type: application/json" -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"

##### Like a Post:
- curl -X POST http://localhost:8000/api/posts/Post1/like/ -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"

##### Get Token for a User:
- curl -X POST http://localhost:8000/api/token/ -d '{"username": "newuser", "password": "newpassword", "email": "newuser@example.com"}' -H "Content-Type: application/json"

##### Register a User:
- curl -X POST http://localhost:8000/api/register/ -d '{"username": "newuser", "password": "newpassword", "email": "newuser@example.com"}' -H "Content-Type: application/json" -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"










