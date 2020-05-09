# Task6

Using docker in our previous web application. 


Create web application using Python and Flask:

* Run the application in Docker.
* Add persistent volume for MongoDB.
* Mount upload directory to upload directory inside flask-simple container.
* Render auth from on `localhost:5000`.
* Image upload function in cabinet  `http://localhost:5000/cabinet/`.
* Image is saved to `upload` folder.
* Function that returns uploaded image `http://localhost:5000/upload/<image_name>.png`.
* User's avatar in `cabinet`.
* Has secret pagefor athenticated users on `http://localhost:5000/cabinet`.
* Allow register new users on `http://localhost:5000/register`.
* Allow users to logout.
    `
