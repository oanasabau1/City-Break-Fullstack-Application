# Citybreak-Fullstack-Application

A fullstack citybreak application built with React, Flask, SQLAlchemy, and Docker. This application allows users to manage events and weather data for various cities, including functionalities to add, edit, and delete records, as well as search for data by city and/or date.

## Docker Containerization


Docker is a platform that uses containerization technology to package applications and their dependencies into a standardized unit called a container. Containers are lightweight, portable, and ensure consistency across different environments. Docker provides tools to create, manage, and orchestrate these containers, allowing developers to build and deploy applications more efficiently.

In this project, Docker is used to containerize the database service.

To build and run the container, run the following command:

```
docker run --name CitybreakDB -e MYSQL_ROOT_PASSWORD=myrootpw -e MYSQL_USER=myuser -e MYSQL_PASSWORD=mypassword -e MYSQL_DATABASE=citybreak -p 3306:3306 -d mysql
```

After this step is done, clone the repository and enjoy your citybreak application, manage your data and start preparing for your next holiday!

Below there are some previews of the application, as well how the endpoints are called in the backend:


![Screenshot 2024-08-25 133843](https://github.com/user-attachments/assets/1b73914c-4407-4e73-af89-0dbf816dfcca)
![Screenshot 2024-08-25 133927](https://github.com/user-attachments/assets/4e5337f6-be95-4c28-8217-1782c764ffc7)
![Screenshot 2024-08-25 133900](https://github.com/user-attachments/assets/ab59a7ed-acb7-4aad-bdaf-2e2152ee061e)
![Screenshot 2024-08-25 134000](https://github.com/user-attachments/assets/cca95995-0fb4-4487-ba2c-816b8911a7df)
