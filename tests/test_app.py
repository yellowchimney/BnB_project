from playwright.sync_api import Page, expect

# Tests for your routes go here

"""
# We can render the index page
# """
def test_get_index(page, test_web_address):
    # We load a virtual browser and navigate to the /index page
    page.goto(f"http://{test_web_address}/")

    # We look at the <p> tag
    header_tag = page.locator("h1")

    # We assert that it has the text "This is the homepage."
    expect(header_tag).to_have_text("ShireBnB")


def test_get_sign_up_returns_sign_up_form(page, test_web_address):
    page.goto(f"http://{test_web_address}/sign_up")
    heading = page.locator("h1")
    expect(heading).to_have_text("Sign Up")  


def test_get_sign_in_returns_sign_in_form(page: Page, test_web_address):
    page.goto(f"http://{test_web_address}/sign_in")
    heading = page.locator("h1")
    # heading.wait_for()
    expect(heading).to_have_text("Sign In") 



def test_post_sign_up_redirects_to_all_spaces(page: Page, test_web_address):
    page.goto(f"http://{test_web_address}/sign_up")

    page.fill("input[name='username']", "testuser")
    page.fill("input[name='email']", "testuser@example.com")
    page.fill("input[name='password']", "password123")
    page.fill("input[name='phone_number']", "1234567890")
    page.click("button[type='submit']")
    page.wait_for_load_state("networkidle")  # Waits until network is quiet

    print("Current URL after submission:", page.url)
    print("Page content after submission:")
    print(page.content())

    page.wait_for_url(f"http://{test_web_address}/all_spaces", timeout=5000)

    expect(page).to_have_url(f"http://{test_web_address}/all_spaces")
    expect(page.locator("h1")).to_have_text("ShireBnB") 


def test_post_sign_in_redirects_to_all_spaces(page: Page, test_web_address):

    page.goto(f"http://{test_web_address}/sign_in")

    page.fill("input[name='username']", "testuser")
    page.fill("input[name='password']", "password123")
    page.click("button[type='submit']")

    expect(page).to_have_url(f"http://{test_web_address}/all_spaces")


def test_get_all_spaces_shows_list_of_spaces(page: Page, test_web_address):
    page.goto(f"http://{test_web_address}/all_spaces")
    heading = page.locator("h1")
    expect(heading).to_have_text("ShireBnB") 

def test_create_space_route(page, test_web_address):
    page.goto(f"http://{test_web_address}/sign_in")
    page.fill("input[name=username]", "testuser")
    page.fill("input[name=password]", "password123")
    page.click("text='Login'")

    page.goto(f"http://{test_web_address}/create_space")
    # page.wait_for_selector("form[action='/create space']", timeout=5000)
    page.fill("input[name=name]", "Bag End")
    page.fill("textarea[name=description]", "Hobbit Hut")
    page.fill("input[name=price_per_night]", '10')

    page.click("text='Create Space'")

    h1_tags = page.locator("h1")
    expect(h1_tags).to_have_text("Bag End")

def test_dashboard_route(page, test_web_address):

    page.goto(f"http://{test_web_address}/sign_in")
    page.fill("input[name=username]", "Gromit")
    page.fill("input[name=password]", "passw0rd1")
    page.click("button[type=submit]")
    
    page.goto(f"http://{test_web_address}/dashboard/1")
    h1_tags = page.locator("h1")
    expect(h1_tags).to_have_text("Gromit's Profile")

# def test_approve_booking_route(page, test_web_address):
#     page.goto(f"http://{test_web_address}/sign_in")
#     page.fill("input[name=username]", "Gromit")
#     page.fill("input[name=password]", "passw0rd1")
#     page.click("button[type=submit]")
#     page.goto(f"http://{test_web_address}/dashboard/1")

#     approve_button = page.locator("form[action^='/approve_booking'] button").first
#     approve_button.click()
#     cancel_button = page.locator("form[action^='/decline_booking'] button").first
#     expect(cancel_button).to_have_text("Cancel")

