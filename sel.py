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

driver.get("")
driver.maximize_window()

wait = WebDriverWait(driver, 15)

search_box = wait.until(
    EC.element_to_be_clickable((By.NAME, "search_query"))
)

search_box.send_keys("tate mcrae")
search_box.send_keys(Keys.RETURN)

first_video = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "ytd-video-renderer a#video-title")
    )
)

print("Opening video:", first_video.get_attribute("title"))

first_video.click()

wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "video"))
)

time.sleep(5)

try:
    skip_button = WebDriverWait(driver, 6).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".ytp-skip-ad-button, .ytp-ad-skip-button")
        )
    )

    skip_button.click()
    time.sleep(2)

    print("Ad skipped")

except Exception:
    print("No skippable ad found")

driver.execute_script("""
    var player = document.getElementById('movie_player');

    player.unMute();
    player.setVolume(100);
    player.setPlaybackRate(2);

    var video = document.querySelector('video');

    video.muted = false;
    video.volume = 1.0;
    video.playbackRate = 2;
""")

time.sleep(2)

speed = driver.execute_script(
    "return document.querySelector('video').playbackRate;"
)

volume = driver.execute_script(
    "return document.querySelector('video').volume;"
)

print("Playback speed:", speed)
print("Volume:", volume)

driver.save_screenshot("youtube_video_2x.png")

print("Page title:", driver.title)
print("Current URL:", driver.current_url)