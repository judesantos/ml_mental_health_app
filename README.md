# ML CI/CD

The **ml_ci_cd project** demonstrates best practices for code management and highlights the use of various developer tools and resources to deploy machine learning models in production through continuous integration and continuous delivery (CI/CD) processes.

## Table of Contents
- [Introduction](#introduction)
- [Processes and Technologies](#processes-and-technologies)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Introduction
**ML CI/CD** is built with a robust development workflow that utilizes a variety of tools and frameworks to optimize scalability, maintainability, and high-quality software practices.

Makefile:
    At its core, **ML CI/CD** uses a **Makefile** to automate repetitive development tasks, like installing dependencies with Poetry, running tests, linting the codebase with Flake8, building the package, and cleaning up artifacts. This ensures that the development process is consistent and easy to manage across team members.

Poetry:
    Dependency management and packaging are handled by **Poetry**, which provides a structured and reproducible environment for development and production.
    Poetry excels over venv and conda by combining seamless dependency management, packaging, and environment isolation into a single, intuitive tool.

Flake8:
    **Flake8** is employed to enforce clean code practices by adhering to PEP 8 standards, with additional linting checks integrated into the CI/CD pipeline via **GitHub Actions**. This ensures that the codebase remains maintainable and free from errors.

SqlAlchemy:
    For data access, the project uses **SQLAlchemy**, a powerful ORM that simplifies database interactions through declarative models and supports both synchronous and asynchronous operations, making it highly suitable for modern, scalable applications.
    Databases are preferred over CSV files in production due to their scalability, support for concurrent access, and ability to enforce data integrity through constraints. It offers optimized query performance with indexing, transactional support (ACID), and robust security features like authentication and encryption. Databases handle complex relationships, provides tools for recovery, integrates seamlessly with APIs for data access. Supports audit trails and reliable operations in multi-user environments, suitable for large, complex, and dynamic datasets.

Jupyter:
    During the development phase, **Jupyter Notebooks** are used for prototyping and experimenting with machine learning models. Once validated, the exploratory code is transformed into production-ready application code, ensuring reproducibility and maintaining a clear boundary between research and deployment.

The project adopts a clean and modular code architecture, promoting separation of concerns with layers for data access, business logic, and API interactions.

Flask:
    The web application is powered by **Flask**, which serves as a lightweight framework for building RESTful APIs that expose model predictions and manage requests. To enhance performance, the application integrates **asynchronous APIs**, allowing it to handle high concurrency efficiently, especially for I/O-bound tasks.

Loguru:
    Logging is managed using **Loguru**, providing structured, readable, and easily configurable logs for debugging and monitoring the system. Log rotation and retention policies are also integrated to ensure effective logging management.

Git, Github Actions:
    Finally, **GitHub Actions** is used to automate CI/CD workflows, running tests, linting, and code quality checks on every commit or pull request. This ensures that the application is thoroughly validated before being deployed to staging or production environments. By combining these tools and practices, the project delivers a scalable, maintainable, and high-quality solution for deploying machine learning models in production.

## Other Resources
- **Git**: Version control for codebase management.
- **Unit Testing**: Ensures functionality and reliability of code.

## Project Structure
```
.env
.env-development
.gitignore
data/
    rent_apartments.csv
logs/
    app.log
Makefile
models/
    rf_db_v1
notebooks/
    random_forest_model.ipynb
poetry.lock
pyproject.toml
README.md
setup.cfg
src/
    config/
        __init__.py
        db.py
        logging.py
        model.py
    db/
        rent_apartment.py
    model/
        pipeline/
            collection.py
            preparation.py
            rf_model.py
        service.py
    runner.py
```
### Key Directories and Files

- **data/**: Contains the dataset files used for training and evaluation.
- **logs/**: Stores log files generated during the execution of the project.
- **models/**: Contains saved models and related artifacts.
- **notebooks/**: Jupyter notebooks for exploratory data analysis and model development.
- **src/**: Main source code directory.
  - **config/**: Configuration files and scripts.
    - `db.py`: Database configuration and connection setup.
    - `logging.py`: Logging configuration.
    - `model.py`: Model configuration.
  - **db/**: Database-related scripts.
    - `rent_apartment.py`: Script for handling rent apartment data.
  - **model/**: Model-related scripts.
    - **pipeline/**: Scripts for data collection, preparation, and model training.
      - `collection.py`: Data loading script.
      - `preparation.py`: Model preparation script.
      - `rf_model.py`: Random forest model training script.
    - `service.py`: Service layer for model operations.
  - `runner.py`: Main script to run the project.

### Configuration Files

- **.env**: Environment variables for the project.
- **.env-development**: Environment variables for the development environment.
- **Makefile**: Contains make commands like installation, running, and testing.
- **pyproject.toml**: Project configuration file for Poetry.
- **setup.cfg**: Configuration file for setup tools. Flake8 configuration settings.

## Installation
To set up the project:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/yourproject.git
    cd yourproject
    ```

2. **Install Poetry** (if not already installed):
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

3. **Set up environment variables**:
    - Copy the `.env-example` file to `.env` and update the variables as needed:
    ```bash
    cp .env-example .env
    ```

4. **Initialize the database** (if applicable):

5. **Install the necessary dependencies**:
    ```bash
    make install
    ```

    This command will:
    - Install all required Python packages listed in `pyproject.toml`.
    - Set up the virtual environment managed by Poetry.

After completing these steps, the project should be set up and ready to use.


## Usage
To train a model, run:
```bash
make run
```

## Testing
To run the test suite, use:
```bash
make test
```

This command runs all unit tests and provides detailed reports on test coverage. The testing suite is designed to validate code correctness and ensure functionality across all components.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

