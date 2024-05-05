# Welcome to myLibrary

myLibrary is a web-based Library Management System designed to streamline the management of library resources by librarians/administrators. It facilitates the maintenance of records for both books and users, enabling efficient operations within the library environment.

## Features
- **Bootstrap Front-end**: The user interface is built using Bootstrap, providing a clean and responsive design for ease of use.
- **Python Flask Backend**: The backend functionality is powered by Python Flask, ensuring robust and efficient performance.

## How to Run

Follow these steps to set up and run myLibrary on your system:

1. **Clone the Repository**: Obtain the myLibrary source code by cloning the repository into your local system.

2. **Create a Virtual Environment**: Set up a virtual environment using the command `virtualenv <env_name>`, for example, `virtualenv env`.

3. **Activate the Virtual Environment**:
   - For Linux: Execute `source ./env/bin/activate`.
   - For Windows: Run `env\Scripts\activate`.

4. **Install Requirements**: Install all required dependencies by executing `pip install -r requirements.txt`.

5. **Database Configuration**:
   - Create a database for your library.
   - In the `app.py` file, modify the database connection settings according to your database configuration (e.g., MySQL).

6. **Run the Application**: Execute the command `python3 app.py` to start the application. Alternatively, you can use `python` instead of `python3`.

7. **Admin Setup**: Manually add administrators to the database to grant access and manage library operations.

## Getting Started

With the application up and running, you can now begin managing your library efficiently. Utilize the provided features to maintain book records, manage user information, and perform necessary library operations seamlessly.

Feel free to explore and customize myLibrary to suit the specific needs of your library environment. If you encounter any issues or have questions, refer to the documentation or reach out to the developer for assistance.

Happy library management with myLibrary!
