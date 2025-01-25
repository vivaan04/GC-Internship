import sys
from playwright.sync_api import sync_playwright
from threading import Event

def open_internship_links():
    # Read the selected links passed through stdin (each line will have description and URL)
    selected_lines = sys.stdin.read().strip().split('\n')


    # Check if selected_lines is empty
    if not selected_lines or all(line == "" for line in selected_lines):
        print("No valid input provided, exiting...")
        sys.exit(1)

    print("Selected lines:", selected_lines)

    browser = None
    try:
        # Start Playwright manually
        with sync_playwright() as playwright:
            print("Playwright started.")
            browser = playwright.chromium.launch(
                headless=False
            )
            print("Browser launched.")

            # Create a context
            context = browser.new_context()

            # Loop through each line and extract the URL
            for line in selected_lines:
                print(f"Opening: {line}")
                # Open a new tab and navigate to the URL
                page = context.new_page()
                
                page.goto(line)

                # page.set_viewport_size({"width": 1920, "height": 1080})




            print("Browser will remain open. Terminate manually to exit.")

            # Wait indefinitely without closing the browser
            event = Event()
            try:
                event.wait()  # Wait for keyboard interrupt (Ctrl+C)
            except KeyboardInterrupt:
                print("\nCaught KeyboardInterrupt, preparing to close browser.")

    finally:
        # Ensure the browser is closed properly only if it's still valid
        if browser:
            try:
                browser.close()
                print("Browser closed.")
            except Exception as e:
                print(f"Error during browser closing: {e}")

if __name__ == "__main__":
    open_internship_links()
