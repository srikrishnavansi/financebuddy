# FinSight - Your Finance Buddy 📈


FinSight is a conversational AI-powered application designed to assist users with their financial goals and plans. It uses the GPT-3.5 Turbo language model from OpenAI to provide friendly and helpful financial advice, answer questions, and perform web scraping tasks related to finance and market data.

## Features

- **Friendly Financial Advice:** FinSight adopts a warm and friendly tone, providing financial guidance as if it were your trusted friend.

- **Web Scraping Tool:** The application includes a web scraping tool to retrieve current information about financial investments, market data, and more from websites and the internet.

- **Interactive Chat Interface:** Users can interact with FinSight through a chat interface, asking questions, seeking advice, and receiving responses in real-time.

- **Easy Setup:** The application allows users to set up their API keys for OpenAI GPT-3.5 Turbo and Google Custom Search Engine (CSE) effortlessly.

## Installation

To run FinSight locally, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/srikrishnavansi/finsight.git
   ```

2. Navigate to the project directory:

   ```bash
   cd finsight
   ```

3. Create a virtual environment (recommended):

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

5. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Run the application:

   ```bash
   streamlit run app.py
   ```

7. Access FinSight in your web browser at `https://financebuddy-r624nya4ky.streamlit.app/`.

## Usage

- **Home Page:** When you first access the application, you'll be greeted with a welcome message on the home page. To get started, click on the "Settings" page and set up your API keys.

- **Settings:** On the "Settings" page, enter your OpenAI GPT-3.5 Turbo API key, Google CSE ID, and Google API key. Click "Submit" to save your settings.

- **Chat:** After setting up your API keys, go to the "Chat" page to interact with FinSight. Ask questions, seek financial advice, and use the web scraping tool to retrieve financial information.

## Dependencies

- [Streamlit](https://streamlit.io/)
- [Langchain](https://github.com/Langchain/langchain) (Custom conversational AI framework)
- [OpenAI GPT-3.5 Turbo](https://beta.openai.com/signup/)
- [Google Custom Search Engine (CSE)](https://developers.google.com/custom-search/docs/tutorial/creatingcse)
- [Chroma Vector Store](https://github.com/Langchain/chromadb)

## Contributors

- Suresh Ratlavath ([GitHub](https://github.com/sureshsgith))
