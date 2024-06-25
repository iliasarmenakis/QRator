from bs4 import BeautifulSoup

def add_pay_here_button(file_path):
    try:
        # Read the HTML file
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        # Create the "Pay Here" button element with inline CSS
        button_html = '''
        <div style="display: flex; justify-content: center; align-items: center; margin-top: 20px;">
            <button onclick="window.location.href='boxsite'" style="
                background-color: #32CD32;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border: none;
                border-radius: 4px;
            ">Pay Here</button>
        </div>
        '''
        button_soup = BeautifulSoup(button_html, 'html.parser')

        # Add the button at the bottom of the body
        if soup.body:
            soup.body.append(button_soup)
        else:
            # If the body tag doesn't exist, create it and add the button
            soup.append(soup.new_tag('body'))
            soup.body.append(button_soup)

        # Write the modified HTML back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))

        print(f"Button added successfully to {file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # Specify the path to the HTML file
    file_path = '/home/kali/Desktop/qrator/templates/index.html'  # Change this to the path of your HTML file
    add_pay_here_button(file_path)
