# This is in rough shape

import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Options
options = Options()
# Go fast
options.page_load_strategy = 'eager'
# Disable notifications
options.add_argument("--disable-notifications")
# Enable location
# options.add_experimental_option("prefs", {"profile.default_content_setting_values.geolocation": 1})


service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://leetcode.com/")
# Explicit wait (Conditional wait)
wait = WebDriverWait(driver, 10)

# Problems directory
driver.get("https://leetcode.com/problemset/all/")

# Get daily problem
wait.until(EC.presence_of_all_elements_located((By.XPATH, "/html/body")))  # Wait for body to load


def wait_for_daily():
    # Wait for daily to load
    time.sleep(1)  # Find a different EC
    prob_num_str = driver.find_element(By.PARTIAL_LINK_TEXT, ". ").text
    index = prob_num_str.index(".")
    prob_num_int = int(prob_num_str[:index])
    if prob_num_int == 1:
        wait_for_daily()
    else:
        return prob_num_int


wait_for_daily()

# Open daily problem
problem_location = driver.find_element(By.PARTIAL_LINK_TEXT, ". ")
problem_title = problem_location.text
problem_location.click()


# Scrape problem info
def get_qd():
    # Get qd_content (qd = question description?)
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login/Sign up")))
    qd_content_raw = driver.find_element(By.ID, "qd-content").text.replace(problem_title, "")
    qd_content_split = qd_content_raw.split()
    if "Accepted" in qd_content_split:
        return qd_content_split
    else:
        get_qd()


# Uncut qd
qd_content_raw = get_qd()

# Get first slice index
first_index = 9
if qd_content_raw[8] != "Companies":
    first_index -= 1

# Get second slice
second_index = qd_content_raw.index("Accepted")

qd_content = qd_content_raw[first_index:second_index]

# Get description
end_of_description = qd_content.index("Example")
qd_description = qd_content[:end_of_description]

# Get Examples
end_of_examples = qd_content.index("Constraints:")
qd_examples = qd_content[end_of_description:end_of_examples]

# Get Constraints
qd_constraints = qd_content[end_of_examples:]

# Ignore constraints for formatting
qd = [qd_description, qd_examples]


# Formatting
def find_indices(qd_section):
    # Find sentences by full stop
    indices = []
    for i, v in enumerate(qd_section):
        if v[-1] == ".":
            indices.append(i + 1)
    return indices


def get_sentences(qd_section):
    section_indices = find_indices(qd_section)
    start_index = 0
    sentence_list = []
    for i in section_indices:
        sentence_list.append(qd_section[start_index:i])
        start_index = i
    return sentence_list

# TODO: Pull Input and expected Output as test
def split_examples():
    pass


def shorten_line(line):
    new_line_indices = []
    new_lines = []
    start_index = 0
    if len(line) > 120:
        for i in range(0, len(line), 120):
            new_line_indices.append(i)
        for index in new_line_indices:
            new_lines.append(line[start_index:index])
            start_index = index
        new_lines.append(line[start_index:])
        return new_lines
    else:
        return line


def final_formatting(qd_section):
    qd_section_sentences = [" ".join(sentence) for sentence in get_sentences(qd_section)]
    qd_section_commented = [f"{sentence}\n" for sentence in qd_section_sentences]
    # Write to py file
    for v in qd_section_commented:
        if len(v) > 120:
            for line in shorten_line(v):
                if line != "":
                    with open("daily.py", "a") as pyfile:
                        pyfile.write(f"\n#{line}")
        else:
            with open("daily.py", "a") as pyfile:
                pyfile.write(f"#{v}")

# Problem name
with open("daily.py", "a") as pyfile:
    pyfile.write(f"#{problem_title}\n\n\n")

# Description/Examples
for q in qd:
    final_formatting(q)

# Constraints
# Need to get formatting from html for this,
# it's in a list tag, probably could have used bs4 for all formatting

while True:
    pass
