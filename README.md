# ReachOut2Me Social Media Web Application

This is a web application built with Django Restframework that enables users to sign up, log in, and create, edit, and delete posts with customized text, pictures, and links. Users can also like, comment/reply, and save posts, search for other users by username, follow and unfollow users to view their posts, and receive notifications. The application also includes chat functionality using websockets.

### Installation


To run this application locally, you will need to have Python 3.6 or higher installed on your computer. You will also need to install Django Restframework and other required packages using pip. Follow these steps to get started:

Clone the repository to your local machine.
Navigate to the project directory and create a new virtual environment using ```python -m venv env```.
Activate the virtual environment using ```source env/bin/activate``` on macOS/Linux or ```env\Scripts\activate``` on Windows.
Install the required packages using ```pip install -r requirements.txt```.
Run the migrations using ```python manage.py migrate```.
Start the development server using ```python manage.py runserver```.

### Usage
Once the development server is running, you can access the application in your web browser by visiting ```http://localhost:8000/```.

### Authentication
To use the features of the application, you will need to sign up for an account or log in if you already have one. From the homepage, click the "Sign up" or "Log in" button to get started.

### Creating, Editing, and Deleting Posts
Once you are logged in, you can create a new post by clicking the "New Post" button on the homepage. You can customize your post with text, pictures, and links. You can also edit or delete your posts from the post detail page.

### Liking, Commenting/Replying, and Saving Posts
You can like a post by clicking the heart icon on the post detail page. You can also comment or reply to a post by typing in the comment box and clicking the "Comment" or "Reply" button. You can save a post by clicking the bookmark icon on the post detail page.

### Searching for Users
You can search for other users by their username from the search bar on the homepage. Type in the username and click the search icon to view the search results.

### Following and Unfollowing Users
You can follow other users to view their posts on your homepage. To follow a user, click the "Follow" button on their profile page. To unfollow a user, click the "Unfollow" button on their profile page.

### Notifications
You will receive notifications when other users like, comment/reply, or follow your posts. You can view your notifications by clicking the bell icon on the navigation bar.

### Chat/Message
You can chat with other users in real-time using the chat feature. To start a chat, click the chat icon on the navigation bar and select a user from your list of followers.
