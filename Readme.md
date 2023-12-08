# GC-Internship

## Training 1: 

We will be going through this quick 32 minute video that will help us learn the industry standards and practices when it comes to python coding.

This will help us better understand how to collobarate and be a part of a development team.

Click on the image below to get started.

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/25P5apB4XWM/0.jpg)](https://www.youtube.com/watch?v=25P5apB4XWM)

----------------------------------------------------------------------------------------------------------------------------------------------------
## Task 1:

Here is an in depth look at the task at hand and how it benefits your career growth. (Use this kind of language/keywords in your resume)

    Create a directory structure as shown in the video:

    Learning: Understanding how to organize code and project files in a structured manner.
    Insight: Importance of maintaining a clear and organized directory structure for code readability and maintainability.
    Contribution: Improved project structure for better collaboration and scalability.

    Use clean Code Practices:

    Learning: Applying principles like readability, maintainability, and simplicity in writing code.
    Insight: The impact of clean code on debugging, collaboration, and long-term project health.
    Contribution: Enhancing code quality and making it easier for others to understand and contribute.

    Create requirements.txt:

    Learning: Understanding dependency management and version control for Python projects.
    Insight: The importance of specifying project dependencies for reproducibility.
    Contribution: Facilitating a smooth setup for others by providing a clear list of dependencies.

    Use black to format the code:

    Learning: Applying automated code formatting tools for consistency.
    Insight: The role of code formatters in maintaining a consistent style across the codebase.
    Contribution: Consistent and automatically formatted code for improved readability.

    Use flake8 to check the code:

    Learning: Performing static code analysis to identify potential issues and adherence to coding standards.
    Insight: The benefits of static analysis in catching errors and maintaining code quality.
    Contribution: Code that meets coding standards and is less prone to bugs and issues.

    Use Pytest to test the code:

    Learning: Writing and running unit tests for code reliability and functionality.
    Insight: The significance of testing in identifying and preventing bugs.
    Contribution: Ensuring that the code functions as intended and providing a safety net for future changes.

    For the same Google script, implement all these guides:

    Learning: Integrating multiple tools and practices into a real-world project.
    Insight: Practical application of best practices for a cohesive development workflow.
    Contribution: A fully-optimized and well-structured project that adheres to industry best practices.


## Resource 1: View this Course at your liesure. 

### MIT Missing Semester Parts 1-7

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/2sjqTHE0zok/0.jpg)](https://www.youtube.com/watch?v=2sjqTHE0zok)

----------------------------------------------------------------------------------------------------------------------------------------------------
## Training 2

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/jAWLQFi4USk/0.jpg)](https://www.youtube.com/watch?app=desktop&v=jAWLQFi4USk)
# Dockerfile for Python 3.10.7 Slim Buster Image with API Application

Docker is a containerization platform that streamlines the development,
deployment, and management of applications. Containers provide a consistent
and isolated environment, ensuring applications run consistently across
different environments.

# Use the official Python 3.10.7 slim-buster image as the base
FROM python:3.10.7-slim-buster

# Set the working directory inside the container to /app
ENV APP_HOME /app
WORKDIR $APP_HOME

# Ensure Python prints statements and logs immediately to facilitate debugging
ENV PYTHONUNBUFFERED 1
# Expose port 8000 to allow external access
EXPOSE 8000

# Install necessary Python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
COPY ./install.sh .
RUN pip install -r requirements.txt

# Copy the entire local project into the container
COPY . .

# Install additional system-level dependencies (e.g., wget)
RUN apt-get update \
    && apt-get install -y wget 

# Copy local scripts (install.sh and start_headless.sh) into the container
# Make the scripts executable and run them
RUN chmod +x install.sh && ./install.sh
RUN chmod +x start_headless.sh && ./start_headless.sh

# Set the default command to run when the container starts
CMD ["python3", "api_app.py"]



----------------------------------------------------------------------------------------------------------------------------------------------------
