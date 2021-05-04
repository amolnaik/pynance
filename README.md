
<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Acknowledgements](#acknowledgements)


<!-- ABOUT THE PROJECT -->
## About The Project
This is a lightweight streamlit app for understanding financial terms, fundamental ratios, and performance metrics. It uses fmpcloud to pull periodic data of stock prices, annual statements, balance sheets of listed companies in the US. The explanation of the terms used in the app is taken from Investopedia.

![Product Name Screen Shot][product-screenshot]

Select a symbol name of the company you want to assess. If the symbol does not match any name, then the selectbox will display search results matching the symbol. Select the company and press start. The app will display fundamental terms and display performance from historical financial statements.

### Built With
[Streamlit](https://streamlit.io/)

<!-- GETTING STARTED -->

### Prerequisites
Python3

### Installation
1. Get a free API Key at [https://fmpcloud.com](https://fmpcloud.io/)
2. Install dependencies
```sh
pip install -r requirements.txt
```
3. Run
```sh
streamlit run fundamentals_app.py
```

<!-- USAGE EXAMPLES -->
## Usage
Coming soon

<!-- ROADMAP -->
## Roadmap
Coming soon

<!-- CONTRIBUTING -->
## Contributing
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- LICENSE -->
## License
Distributed under the MIT License. See `LICENSE` for more information.

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Python Wrapper for fmpcloud API](https://github.com/razorhash/pyfmpcloud)


<!-- MARKDOWN LINKS & IMAGES -->
[product-screenshot]: screenshot.png
