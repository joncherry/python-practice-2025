# Python Practice 2025

This is a project to demonstrate and enhance my python skills. This should help me in future roles on cool projects.

I was given these goals to try to include in the project:
- [X] 🐍 Core Python Skills
Proficiency in Python 3. Experience with writing modular, maintainable code. Debugging and exception handling.
- [X] 🔄 Data Integration & Middleware
Building REST API clients (e.g., using requests) Handling JSON, XML, and other structured payloads. Designing middleware for syncing data (orders, pricing, inventory) between systems.
- [X] 🌐 Web Scraping & Automation
Scraping data with tools like BeautifulSoup, lxml, or Selenium. Handling pagination, dynamic content, and headers/cookies. Respecting robots.txt / rate limits (ethical scraping)
- [ ] 📊 Data Handling & Cleaning
Cleaning structured data using pandas. Parsing and exploring unstructured data (e.g., free text, HTML, nested JSON) Familiarity with datetime manipulation, null handling, type coercion.
- [ ] 🧠 Data Exploration & Troubleshooting
Exploring datasets to identify issues or patterns. Writing scripts to validate, transform, or summarize datasets.
- [X] ☁️ Google Cloud / BigQuery / Google Sheets
Reading/writing to BigQuery using google-cloud-bigquery , pandas-gbq. Manipulating Google Sheets with gspread or Google Sheets API. Familiarity with service accounts and OAuth credentials.
- [ ] :books: Libraries: pandas, numpy , matplotlib, seaborn, and streamlit

The design of this project is will be directed by trying to hit these goals. The data used won't necessarily make sense or be useful. The goal is to demonstrate and practice skills.

examples of commands:

```
LOCAL_RUN_MODE=1 python3 ./src/main.py
 * Serving Flask app 'adapters.auth'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://localhost:8080
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 545-530-557
```

```
python3 ./terminalcli/main.py                                                   
commands available are:
    authorize
    clear_authorization {session_id}
    revoke_authorization {session_id}
    home_and_hay_report {session_id}
    amazon_report {session_id}
    motorola_report {session_id}
```

This will open the browser from the terminal to sign in with Google. After signing in with Google in the browser you will get a session ID to use in the terminal commands.
```
python3 ./terminalcli/main.py authorize
<!doctype html><html lang="en-US" dir="ltr"><head><base href="https://accounts.google.com/v3/signin......
```

```
python3 ./terminalcli/main.py home_and_hay_report 2b6bf57e-3c60-42a8-85fb-dec3c136f2f7
stateName,medianHomePrice,medianHayPrice,ratio
california,697509.3482622576,223.0,3127.844611041514
ohio,192234.5382798966,169.0,1137.482475028974
nevada,386433.58174731076,210.0,1840.1599130824322
delaware,335145.34594341426,160.0,2094.6584121463393
```

```
python3 ./terminalcli/main.py amazon_report 2b6bf57e-3c60-42a8-85fb-dec3c136f2f7
title,starRating,ratingsCount
Moto G - 2025 | Unlocked | Made for US 4/128GB | 50MP Camera | Forest Gray,4.2 out of 5 stars,"1,899"
Moto G Stylus 5G | 2024 | Unlocked | Made for US 8/256GB | 50MP Camera | Caramel Latte,4.6 out of 5 stars,"1,128"
Moto G Power 5G | 2023 | Unlocked | Made for US 4/128GB | 50 MPCamera | Mineral Black,4.2 out of 5 stars,"1,815"
```

```
python3 ./terminalcli/main.py motorola_report 2b6bf57e-3c60-42a8-85fb-dec3c136f2f7
title,price,link
motorola razr ultra 2025 PANTONE Mountain Trail,"$1,299.99",https://www.motorola.com/us/en/p/phones/razr/razr-ultra/pmipmhn40ms?pn=PB770068US
motorola razr ultra 2025 PANTONE Cabaret,"$1,299.99",https://www.motorola.com/us/en/p/phones/razr/razr-ultra/pmipmhn40ms?pn=PB770069US
motorola razr ultra 2025 PANTONE Mountain Trail,"$1,299.99",https://www.motorola.com/us/en/p/phones/razr/razr-ultra/pmipmhn40ms?pn=PB770022US
motorola razr ultra 2025 PANTONE Rio Red,"$1,299.99",https://www.motorola.com/us/en/p/phones/razr/razr-ultra/pmipmhn40ms?pn=PB770044US
```