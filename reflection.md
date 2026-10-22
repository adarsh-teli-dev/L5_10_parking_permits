# Lab 5: Static Code Analysis Reflection

## 1. What is static code analysis, and why is it important?

Static code analysis is the process of examining source code without executing the program. It helps identify potential bugs, security vulnerabilities, coding standard violations, and maintainability issues. In this lab, I used Pylint, Bandit, and Flake8 to analyze the Campus Parking Permit Manager. These tools helped me identify problems early and improve the reliability, readability, and quality of the Python program.

## 2. What issues did you identify and fix in the program?

I identified several issues in the original `parking_system.py` file. These included a mutable default argument, overly broad exception handling, inconsistent expiry-date formatting, and file operations without context managers. The program also accepted invalid parking zones and vehicle plate values. I improved the code by using `None` for the optional list argument, handling expected exceptions explicitly, validating input values, standardizing date formatting, and using `with open()` for file operations. These changes made the program safer and easier to maintain.

## 3. How did Pylint, Bandit, and Flake8 help improve the code?

Pylint helped identify code-quality problems and potential programming errors. Bandit helped examine the code for common security vulnerabilities and insecure coding patterns. Flake8 helped identify style violations, formatting problems, and deviations from Python's PEP 8 guidelines. Each tool served a different purpose, and using all three provided a more comprehensive review than relying on a single tool. I also manually inspected the program because some functional problems might not be detected by static analysis tools.

## 4. What did you learn from this lab, and how can static analysis be used in future projects?

This lab taught me that code can run without errors and still contain bugs, security risks, and poor programming practices. I learned the importance of validating inputs, handling exceptions appropriately, managing files safely, and maintaining consistent coding standards. In future projects, I can integrate static analysis tools into my development workflow and use them before committing code or submitting a project. Regular analysis can help detect problems early, improve maintainability, and support the development of more reliable Python applications.