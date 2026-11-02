# Agile & DevOps Lab -- Complete Codes and Similar Samples

This README consolidates Docker commands, Dockerfiles, Python sample
apps, PyTest introduction/testing examples, and Selenium examples. Extra
practice samples are illustrative; website selectors can change.

## Contents

-   Docker commands
-   Dockerfiles and sample Python programs
-   PyTest introduction and core lab samples
-   Additional PyTest samples
-   Selenium scripts and locators
-   Run checklist

# 1. Docker Commands

## Images

``` bash
docker pull python:3.11
docker images
docker rmi python:3.11
docker image prune
```

## Containers

``` bash
docker run hello-world
docker run -it ubuntu bash
docker run -d --name mycontainer nginx
docker ps
docker ps -a
docker stop mycontainer
docker start mycontainer
docker restart mycontainer
docker rm mycontainer
docker rm -f mycontainer
docker exec -it mycontainer bash
docker logs mycontainer
docker inspect mycontainer
docker stats
```

## Build, tag, login, push

``` bash
docker build -t python-file .
docker tag python-file YOUR_DOCKERHUB_USERNAME/python-file:latest
docker login
docker push YOUR_DOCKERHUB_USERNAME/python-file:latest
```

## Cleanup

``` bash
docker container prune
docker network prune
docker image prune
docker system prune
```

# 2. Dockerfiles and Python Samples

## Basic Dockerfile

**Dockerfile**

``` dockerfile
FROM python:3.11
COPY my_script.py .
CMD ["python", "my_script.py"]
```

**my_script.py**

``` python
print("Hello from Docker!")
```

``` bash
docker build -t python-file .
docker run --rm python-file
```

## Dockerfile with WORKDIR

``` dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY my_script.py .
CMD ["python", "my_script.py"]
```

## Python app with requirements

**Dockerfile**

``` dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

**requirements.txt**

``` text
requests
```

**app.py**

``` python
import requests
response = requests.get("https://example.com", timeout=10)
print("Status:", response.status_code)
```

## Flask in Docker

**Dockerfile**

``` dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir flask
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
```

**app.py**

``` python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Flask in Docker!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

``` bash
docker build -t flask-demo .
docker run --rm -p 5000:5000 flask-demo
```

Open `http://localhost:5000`.

## Nginx static HTML Dockerfile

``` dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 80
```

**index.html**

``` html
<!DOCTYPE html>
<html><head><title>Docker Demo</title></head>
<body><h1>Hello from Nginx Docker container!</h1></body></html>
```

``` bash
docker build -t nginx-html .
docker run --rm -p 8080:80 nginx-html
```

# 3. PyTest -- Introduction and Core Samples

Install and run:

``` bash
python -m pip install pytest
pytest
pytest -v
pytest -v -s
pytest test_file.py
```

Pytest test files/functions typically start with `test_`. Assertions
verify expected values.

## Basic arithmetic -- test_task1_basic.py

``` python
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-2, -3) == -5

def test_add_zero():
    assert add(10, 0) == 10
```

## Substring -- test_task2_substring.py

``` python
def test_substring():
    string = "Hello World"
    substring = "World"
    assert substring in string

def test_substring_not_present():
    string = "Hello World"
    substring = "Python"
    assert substring not in string
```

## Markers -- test_task3_markers.py

``` python
import pytest

@pytest.mark.great
def test_greater():
    assert 10 > 5

@pytest.mark.great
def test_greater_equal():
    assert 10 >= 10

@pytest.mark.small
def test_less():
    assert 5 < 10
```

Run `pytest -v -m great` or `pytest -v -m small`. Optional pytest.ini:

``` ini
[pytest]
markers =
    great: greater comparison tests
    small: smaller comparison tests
```

## Fixture -- test_task4_fixture.py

``` python
import pytest

@pytest.fixture
def sample_data():
    return [1, 2, 3, 4, 5]

def test_length(sample_data):
    assert len(sample_data) == 5

def test_first_element(sample_data):
    assert sample_data[0] == 1

def test_contains_value(sample_data):
    assert 3 in sample_data
```

# 4. Additional PyTest Sample Codes

## Calculator -- calculator.py

``` python
def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

**test_calculator.py**

``` python
import pytest
from calculator import add, subtract, multiply, divide

def test_add(): assert add(4, 6) == 10
def test_subtract(): assert subtract(10, 3) == 7
def test_multiply(): assert multiply(3, 4) == 12
def test_divide(): assert divide(10, 2) == 5

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
```

## Parametrize -- test_parametrize.py

``` python
import pytest

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3), (5, 5, 10), (-1, 1, 0), (0, 0, 0)
])
def test_add(a, b, expected):
    assert a + b == expected
```

## Skip and xfail -- test_skip_xfail.py

``` python
import pytest

@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature():
    assert True

@pytest.mark.xfail(reason="Known bug; expected to fail")
def test_known_bug():
    assert 2 * 2 == 5
```

## Strings and lists -- test_string_list.py

``` python
def test_string_upper():
    assert "hello".upper() == "HELLO"

def test_string_startswith():
    assert "pytest".startswith("py")

def test_list_append():
    values = [1, 2]
    values.append(3)
    assert values == [1, 2, 3]

def test_list_length():
    assert len(["a", "b", "c"]) == 3
```

## Fixture setup/teardown -- test_fixture_yield.py

``` python
import pytest

@pytest.fixture
def resource():
    print("Setup: create resource")
    data = {"status": "ready"}
    yield data
    print("Teardown: clean up resource")

def test_resource_status(resource):
    assert resource["status"] == "ready"
```

Run with `pytest -v -s test_fixture_yield.py`.

## Login validation -- login.py

``` python
def validate_login(username, password):
    if not username or not password:
        return False
    return username == "admin" and password == "admin123"
```

**test_login.py**

``` python
from login import validate_login

def test_valid_credentials():
    assert validate_login("admin", "admin123") is True

def test_wrong_password():
    assert validate_login("admin", "wrong") is False

def test_empty_username():
    assert validate_login("", "admin123") is False

def test_empty_password():
    assert validate_login("admin", "") is False
```

## PyTest command cheat sheet

``` bash
pytest
pytest -v
pytest -s
pytest test_calculator.py
pytest test_calculator.py::test_add
pytest -k "divide"
pytest -m great
pytest -x
pytest --tb=short
pytest --junitxml=report.xml
```

# 5. Selenium -- Setup and Sample Automation

Install:

``` bash
python -m pip install selenium
```

Selenium 4 often manages drivers through Selenium Manager. Have Chrome
or another supported browser installed. Website selectors and consent
pages may change.

## Google search -- test_selenium.py

``` python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
try:
    driver.get("https://www.google.com")
    box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    box.send_keys("Selenium Python")
    box.send_keys(Keys.ENTER)
    WebDriverWait(driver, 10).until(EC.title_contains("Selenium Python"))
    print("Page title:", driver.title)
finally:
    driver.quit()
```

## YouTube search -- test_youtube.py

``` python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
try:
    driver.get("https://www.youtube.com")
    box = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.NAME, "search_query"))
    )
    box.send_keys("Python tutorial")
    box.send_keys(Keys.ENTER)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "video-title"))
    )
    print("Search completed:", driver.title)
finally:
    driver.quit()
```

## Open first YouTube result -- test_youtube_video.py

``` python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
try:
    driver.get("https://www.youtube.com")
    box = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.NAME, "search_query"))
    )
    box.send_keys("Python programming tutorial")
    box.send_keys(Keys.ENTER)
    video = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, "video-title"))
    )
    video.click()
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "video"))
    )
    print("Video page:", driver.title)
finally:
    driver.quit()
```

## Page title and URL assertions -- test_page_checks.py

``` python
from selenium import webdriver

def test_python_website_title():
    driver = webdriver.Chrome()
    try:
        driver.get("https://www.python.org")
        assert "Python" in driver.title
        assert driver.current_url.startswith("https://www.python.org")
    finally:
        driver.quit()
```

## Selenium form interaction -- test_form_interaction.py

``` python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
try:
    driver.get("https://www.selenium.dev/selenium/web/web-form.html")
    field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "my-text"))
    )
    field.send_keys("Hello Selenium")
    driver.find_element(By.TAG_NAME, "button").click()
    message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "message"))
    )
    print(message.text)
    assert "Received" in message.text
finally:
    driver.quit()
```

## Dropdown -- test_dropdown.py

``` python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome()
try:
    driver.get("https://www.selenium.dev/selenium/web/web-form.html")
    dropdown = Select(driver.find_element(By.NAME, "my-select"))
    dropdown.select_by_value("2")
    assert dropdown.first_selected_option.get_attribute("value") == "2"
finally:
    driver.quit()
```

## Explicit wait -- test_explicit_wait.py

``` python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
try:
    driver.get("https://www.selenium.dev")
    link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Downloads"))
    )
    link.click()
    WebDriverWait(driver, 10).until(EC.url_contains("downloads"))
    print("Navigated:", driver.current_url)
finally:
    driver.quit()
```

## Selenium locator reference

``` python
driver.find_element(By.ID, "element-id")
driver.find_element(By.NAME, "element-name")
driver.find_element(By.CLASS_NAME, "class-name")
driver.find_element(By.TAG_NAME, "input")
driver.find_element(By.LINK_TEXT, "Exact link text")
driver.find_element(By.PARTIAL_LINK_TEXT, "Partial text")
driver.find_element(By.CSS_SELECTOR, "input[type='text']")
driver.find_element(By.XPATH, "//button[@type='submit']")
```

# 6. Quick Run Checklist

**Docker** 1. Keep Dockerfile and app files in one folder. 2. Build:
`docker build -t my-image .` 3. Run: `docker run --rm my-image` 4.
Publish ports for web apps using `-p host:container`.

**PyTest** 1. Install: `python -m pip install pytest` 2. Use filenames
`test_*.py`. 3. Run all: `pytest -v` 4. Run one file:
`pytest -v test_file.py`.

**Selenium** 1. Install: `python -m pip install selenium` 2. Install a
supported browser. 3. Run script: `python test_selenium.py` 4. Or
execute test file: `pytest -v test_page_checks.py`. 5. Close browser in
a `finally` block with `driver.quit()`.

------------------------------------------------------------------------

**End of README --- Docker, PyTest, Selenium, and extra similar sample
codes in one consolidated reference.**
