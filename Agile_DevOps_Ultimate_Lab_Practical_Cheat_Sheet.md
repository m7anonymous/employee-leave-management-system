# ULTIMATE LAB PRACTICAL CHEAT SHEET
## Agile Methodology & DevOps Lab — 20CP408P • Semester VII

**Based on the 11 labs in the submitted lab PDF**  
Git • AWS EC2 / CloudFormation • JIRA • GitHub Actions • Docker • PyTest • Selenium

> Exam strategy: identify the task → create the correctly named file → paste code → run the exact command → verify output.

---

# LAB 1 — Git Version Control

## Core terms
- **Version Control:** tracks changes, recovers earlier versions, preserves history, supports teamwork.
- **Git:** distributed version control system (Linus Torvalds, 2005).
- **CVCS:** one central repository; network dependency.
- **DVCS:** each developer has a full repository copy; supports offline work.
- **Repository:** files and history.
- **Staging area:** changes prepared for commit.
- **Commit:** saved record/snapshot.
- **Branch:** independent development line.
- **Merge:** combines branches.
- **Pull Request (PR):** request to review and merge a branch.

## Commands and lab workflow
```bash
git init
git status
git add .                         # stage all
git add filename
git commit -m "First commit"
git remote add origin <url>
git push -u origin main
git branch Naitik
git checkout Naitik
git push -u origin branch2
git clone <url>
git branch
git merge <branch>
touch hello.txt                   # Git Bash/Linux
nano hello.txt
cat hello.txt
```

**Workflow:** create GitHub repo → `git init` → create files → `git status` → `git add .` → `git commit` → add remote → `git push` → branch/checkout → create PR → merge → clone when needed.

**Result:** Successfully created and managed a Git repository, performed basic commands, created branches, pushed changes, and merged using a pull request.

---

# LABS 2–3 — AWS EC2 + CloudFormation + Intrinsic Functions

## Theory / definitions
- **AWS:** cloud platform offering compute, storage, networking and database services.
- **EC2:** virtual server.
- **t3.micro:** instance type used in the lab.
- **AMI:** OS image (Amazon Linux 2023).
- **VPC:** isolated network.
- **Subnet:** smaller network inside VPC.
- **Security Group:** virtual firewall.
- **Elastic IP:** static public IPv4.
- **Private IP:** internal address.
- **EC2 Instance Connect:** console connection method.
- **CloudFormation:** Infrastructure as Code (IaC), provisions consistent resources from templates.

## CloudFormation components
- `AWSTemplateFormatVersion`: template version.
- `Description`: purpose.
- `Parameters`: user inputs.
- `Resources`: AWS resources.
- `Outputs`: values after stack deployment.
- `!Ref`: returns parameter/resource identifier.
- `!GetAtt`: gets a resource attribute, e.g. `MyEC2Instance.PrivateIp`.

## EC2 stack template (indentation cleaned for readability)
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Simple EC2 stack with Security Group and Elastic IP

Parameters:
  InstanceType:
    Description: EC2 instance type
    Type: String
    Default: t3.micro
  LatestAmiId:
    Description: Latest Amazon Linux 2023 AMI via SSM
    Type: AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>
    Default: /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64
  VpcId:
    Type: AWS::EC2::VPC::Id
  SubnetId:
    Type: AWS::EC2::Subnet::Id

Resources:
  InstanceSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Allow SSH and HTTP inbound
      VpcId: !Ref VpcId
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
      Tags:
        - Key: Name
          Value: AgileLab-SG

  MyEC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: !Ref InstanceType
      ImageId: !Ref LatestAmiId
      SubnetId: !Ref SubnetId
      SecurityGroupIds:
        - !Ref InstanceSecurityGroup
      Tags:
        - Key: Name
          Value: AgileLab-Instance

  MyElasticIP:
    Type: AWS::EC2::EIP
    Properties:
      Domain: vpc
      InstanceId: !Ref MyEC2Instance
      Tags:
        - Key: Name
          Value: AgileLab-EIP

Outputs:
  InstanceId:
    Description: EC2 Instance ID
    Value: !Ref MyEC2Instance
  PrivateIP:
    Description: Private IP address
    Value: !GetAtt MyEC2Instance.PrivateIp
  ElasticIP:
    Description: Elastic (Public) IP address
    Value: !Ref MyElasticIP
```

**Practical:** CloudFormation → create stack/upload template → select VPC and subnet within it → create stack → inspect Outputs for InstanceId, PrivateIP, ElasticIP.

**Security group ports**
| Rule | Purpose |
|---|---|
| TCP 22 / SSH | Remote shell; restrict to trusted IPs in practice |
| TCP 80 / HTTP | Web traffic |
| `0.0.0.0/0` | Any IPv4 address; broad |

---

# LAB 4 — JIRA Scrum Project

JIRA tracks tasks/bugs and supports Scrum/Kanban, sprint planning, backlog and reports.

## Terms
| Term | Meaning |
|---|---|
| Project | Collection of related work |
| Epic | Large feature grouping stories |
| Story | User requirement |
| Task | Specific activity |
| Bug | Defect/error |
| Sprint | Fixed iteration, usually 1–4 weeks |
| Backlog | Prioritized pending work |
| Assignee | Person responsible |
| Issue | Generic work item |
| Scrum Board | Visual status board |

## PDF practical — Student Management System
1. Create a team-managed Scrum project:
   - Project Name: **Student Management System**
   - Project Key: **SMS**
2. Create Epic: **Student Registration Module**
3. Create stories:
   - US1 Student registration into portal
   - US2 Admin verification of student details
   - US3 Secure student login
   - US4 Student profile updates
4. Create tasks:
   - Design Registration Page
   - Create Database
   - Develop Login Page
   - Test Registration
5. Create bugs:
   - BUG1 Login button not working
   - BUG2 Registration page crashes on empty input
6. Create Sprint 1 (2 weeks); move stories from backlog to sprint.
7. Start sprint and update board:
   `To Do → In Progress → Testing → Done`
8. Review reports: Sprint Report, Burndown Chart, Velocity Report, Backlog View.

- **Backlog:** all pending work, prioritized and continually updated.
- **Sprint:** selected work for fixed duration.
- **Burndown:** remaining work over time.
- **Velocity:** work completed across sprints.

---

# LABS 5–6 — GitHub Actions / CI-CD

GitHub Actions automates build/test/deploy. Workflow YAML resides in `.github/workflows`.

## Components
- **Workflow:** automation.
- **Event/trigger:** `push`, `pull_request`, `workflow_dispatch`, `schedule`, `release`.
- **Job:** group of steps on same runner.
- **Step:** task such as checkout/install/test.
- **Action:** reusable component.
- **Runner:** machine (Linux/Windows/macOS) executing jobs.
- **Secrets:** secure tokens/keys.
- **CI:** integrate changes frequently and run build/tests.
- **CD:** automate deployment/release of tested code.

## Basic Python CI workflow
```yaml
name: Python CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install pytest
        run: pip install pytest
      - name: Run tests
        run: pytest -v
```

## PDF Calculator CI workflow — structure
The lab’s Java workflow uses Java 17 (Temurin), compiles `Calculator.java`, uploads `Calculator.class` as an artifact, then test jobs download it. A matrix tests addition, negative operands, subtraction, multiplication, division, decimal division, divide-by-zero, invalid operator and non-numeric input. A separate missing-args job tests missing input. A final job depends on test and missing-args and checks their results.

```yaml
name: Calculator CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '17'
      - name: Compile
        run: javac Calculator.java
      - uses: actions/upload-artifact@v4
        with:
          name: calculator-class
          path: Calculator.class
          retention-days: 1

  test:
    needs: build
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        case:
          - {name: addition, a: "3", op: "+", b: "4", expected: "7", expect_failure: false}
          - {name: division, a: "10", op: "/", b: "2", expected: "5", expect_failure: false}
          - {name: divide-zero, a: "5", op: "/", b: "0", expected: "", expect_failure: true}
    steps:
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '17'
      - uses: actions/download-artifact@v4
        with:
          name: calculator-class
      # Matrix case is passed to run step as environment variables;
      # shell compares actual output/exit code with expected result.
  missing-args:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: calculator-class
      - name: Missing arguments should fail
        run: |
          if java Calculator 5 +; then
            echo "FAIL: expected non-zero exit code"
            exit 1
          fi
          echo "PASS: missing argument correctly rejected"

  all-tests-passed:
    needs: [test, missing-args]
    if: always()
    runs-on: ubuntu-latest
    steps:
      - run: |
          if [ "${{ needs.test.result }}" != "success" ] || [ "${{ needs.missing-args.result }}" != "success" ]; then
            echo "One or more test jobs failed."
            exit 1
          fi
          echo "All test jobs passed."
```

> **YAML note:** the PDF extraction had inconsistent indentation in places. YAML indentation is significant; use consistent spaces. The matrix excerpt above illustrates structure, not a complete replacement for the lab’s entire workflow.

---

# LABS 7–8 — Docker

## Concepts
- **Docker:** containerizes an app with dependencies into isolated environments.
- **Image:** blueprint/template containing app and dependencies.
- **Container:** instance of an image.
- **Dockerfile:** recipe for building image.
- **Docker Hub:** registry to store/share images.
- Advantages: portability, isolation, consistency, lightweight deployment.

## Commands
```bash
docker pull mysql
docker run mysql
docker rm <container_id>
docker exec -it MYSQL /bin/bash
docker inspect <container>
docker build -t image_name .
docker push image_name
docker images
docker ps
docker ps -a
docker stop <container>
docker start <container>
docker rmi <image>
docker login
exit
```

## PDF Docker practical
```python
# my_script.py
print("Hello from Docker!")
```

```dockerfile
# Dockerfile
FROM python:3.11
COPY my_script.py .
CMD ["python", "my_script.py"]
```

Run from the directory containing both files:
```bash
docker build -t naitik002/python_file .
docker run naitik002/python_file
docker login
docker push naitik002/python_file
```

**Dockerfile instructions:** `FROM` selects base image; `COPY` copies files; `CMD` sets default startup command.

**Workflow:** create app → Dockerfile → build image → run container → verify → push.

---

# LABS 9–10 — PyTest

PyTest is a Python testing framework.

## Discovery rules
- File: `test_*.py` or `*_test.py`
- Function: name starts with `test_`
- `assert` verifies a condition.
- **Fixture:** reusable setup/data.
- **Marker:** label to group/select tests.
- **Parameterization:** run one test with multiple input combinations.

## Commands (PowerShell)
```powershell
pytest
pytest -v
pytest -k great -v        # names containing "great"
pytest -m great -v        # tests tagged with marker great
pytest test_task4_fixture.py -v
```

## Task 1 — `test_task1_basic.py`
```python
def test_greater():
    num = 100
    assert num > 50

def test_greater_equal():
    num = 100
    assert num >= 100

def test_less():
    num = 100
    assert num < 200
```

## Task 2 — `test_task2_substring.py` (same assertions; use `-k great`)
```python
def test_greater():
    num = 100
    assert 100 > 50

def test_greater_equal():
    num = 100
    assert 100 >= 100

def test_less():
    num = 100
    assert 100 < 200
```

## Task 3 — `test_task3_markers.py`
```python
import pytest

@pytest.mark.great
def test_greater():
    assert 100 > 50

@pytest.mark.great
def test_greater_equal():
    assert 100 >= 100

@pytest.mark.less
def test_less():
    assert 100 < 200

# Run:
# pytest -m great -v
```

## Task 4 — `test_task4_fixture.py`
```python
import pytest

@pytest.fixture
def input_value():
    return 10

def test_addition(input_value):
    assert input_value + 5 == 15

# Run:
# pytest test_task4_fixture.py -v
```

## Other useful examples — skip, xfail, parameterization
```python
import pytest

@pytest.mark.parametrize("a,b,expected", [(2, 3, 5), (10, 5, 15)])
def test_add(a, b, expected):
    assert a + b == expected

@pytest.mark.skip(reason="not implemented")
def test_future():
    assert True

@pytest.mark.xfail(reason="expected failure")
def test_known_bug():
    assert 1 == 2
```

### If PyTest says “collected 0 items”
1. Check current directory has test files.
2. Filenames must start `test_` (or end `_test.py`).
3. Functions must start `test_`.
4. Confirm saved extension is `.py`, not `.py.txt`.
5. Run one explicitly:
```powershell
pytest -v test_task1_basic.py
```

---

# LAB 11 — Selenium

Selenium is an open-source browser automation tool for web testing. WebDriver controls the browser; Web Element is an HTML element; Locator identifies an element.

## Locator strategies
| Locator | Example |
|---|---|
| ID | `By.ID, "login"` |
| Name | `By.NAME, "q"` |
| Class name | `By.CLASS_NAME, "button"` |
| XPath | `By.XPATH, "//button"` |
| CSS Selector | `By.CSS_SELECTOR, "button#submit"` |

## Common functions
- `driver.get(url)`: open URL.
- `driver.find_element(By..., value)`: locate element.
- `send_keys(text)`: type/keyboard input.
- `click()`: click element.
- `driver.maximize_window()`: maximize.
- `driver.save_screenshot(file)`: screenshot.
- `driver.quit()`: close browser/session.
- `WebDriverWait` + expected conditions: wait until element ready.

## Task 1 — `test_selenium.py` (Google search)
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.get("https://www.google.com")
driver.maximize_window()

search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Selenium Python Tutorial")
search_box.send_keys(Keys.RETURN)

time.sleep(3)
driver.save_screenshot("google_search_result.png")
driver.quit()
```

## Task 2 — `test_youtube.py` (YouTube search)
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.get("https://www.youtube.com")
driver.maximize_window()

wait = WebDriverWait(driver, 10)
search_box = wait.until(EC.element_to_be_clickable((By.NAME, "search_query")))
search_box.send_keys("today's news")
search_box.send_keys(Keys.RETURN)

wait.until(EC.presence_of_element_located((By.ID, "video-title")))
time.sleep(2)
driver.save_screenshot("youtube_todays_news.png")
print("Page title:", driver.title)
print("Current URL:", driver.current_url)
```

## Task 3 — `test_youtube_video.py` (open video, attempt skip ad, 2x playback)
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--autoplay-policy=no-user-gesture-required")
driver = webdriver.Chrome(options=options)
driver.get("https://www.youtube.com")
driver.maximize_window()
wait = WebDriverWait(driver, 15)

search_box = wait.until(EC.element_to_be_clickable((By.NAME, "search_query")))
search_box.send_keys("today's news")
search_box.send_keys(Keys.RETURN)

first_video = wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "ytd-video-renderer a#video-title")))
print("Opening video:", first_video.get_attribute("title"))
first_video.click()

wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "video")))
time.sleep(5)

try:
    skip_button = WebDriverWait(driver, 6).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, ".ytp-skip-ad-button, .ytp-ad-skip-button")))
    skip_button.click()
    time.sleep(2)
    print("Ad skipped")
except Exception:
    print("No skippable ad found")

script = ("var player = document.getElementById('movie_player');"
          "player.unMute(); player.setVolume(100); player.setPlaybackRate(2);"
          "var video = document.querySelector('video');"
          "video.muted = false; video.volume = 1.0; video.playbackRate = 2;")
driver.execute_script(script)

time.sleep(2)
speed = driver.execute_script("return document.querySelector('video').playbackRate;")
volume = driver.execute_script("return document.querySelector('video').volume;")
print("Playback speed:", speed)
print("Volume:", volume)
driver.save_screenshot("youtube_video_2x.png")
print("Page title:", driver.title)
print("Current URL:", driver.current_url)
```

## Install / run
```powershell
pip install selenium
python test_selenium.py
python test_youtube.py
python test_youtube_video.py
```

> YouTube’s UI/selectors can change. Modern Selenium generally manages ChromeDriver when a compatible Chrome installation is available.

---

# LAST-MINUTE PRACTICAL QUICK CHECK

| Lab | Remember |
|---|---|
| Git | `init → add → commit → remote → push`; branch/checkout/PR/merge |
| AWS | Parameters / Resources / Outputs; `!Ref` / `!GetAtt`; ports 22 SSH, 80 HTTP |
| JIRA | SMS project; Epic; 4 stories; 4 tasks; 2 bugs; 2-week Sprint |
| GitHub Actions | `.github/workflows/*.yml`; event → runner → jobs → steps; CI build/test |
| Docker | Dockerfile `FROM/COPY/CMD`; `build -t name .` → `run name` → login → push |
| PyTest | `test_` filename/function; `assert`; `-v`, `-k`, `-m`; fixture input=10 |
| Selenium | webdriver → get → find_element → send_keys → screenshot → quit |

# FAST VIVA ONE-LINERS

- **Git:** distributed version control system to track code changes and collaborate.
- **Git vs GitHub:** Git is the tool; GitHub hosts remote repositories and collaboration.
- **IaC:** managing infrastructure through configuration/templates rather than manual setup.
- **EC2:** AWS virtual server service.
- **CloudFormation:** provisions AWS infrastructure from templates.
- **JIRA Epic:** large feature grouping related stories.
- **Sprint:** fixed-length Scrum iteration.
- **CI:** frequent integration with automated build and tests.
- **Runner:** machine executing GitHub Actions jobs.
- **Docker image vs container:** image is blueprint; container is its instance.
- **Dockerfile:** instructions for building a Docker image.
- **PyTest fixture:** reusable test setup/data.
- **PyTest marker:** label to group/select tests.
- **Selenium WebDriver:** API/tool controlling browser actions.
- **XPath/CSS selector:** methods to locate HTML elements.

---

## Source note
This cheat sheet is based on the lab PDF’s extracted content. Some CloudFormation and GitHub Actions YAML in the PDF extraction showed indentation inconsistencies; those sections are noted and formatting is cleaned where presented. The GitHub Actions matrix excerpt is a structural outline rather than a complete transcription of every matrix test step.
