from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

# Initialize Chrome browser
driver = webdriver.Chrome()

# Define XPaths for book details
def get_xpath_for_book(i):
    return {
        "title": f"//tr[{i}]//a[@class='bookTitle']/span",
        "author": f"//tr[{i}]//a[@class='authorName']/span",
        "rating": f"//tr[{i}]//span[@class='minirating']",
        "score": f"//tr[{i}]//a[contains(text(),'score')]"
    }

# Extract text from a specified element
def get_element_text(xpath):
    try:
        return driver.find_element(By.XPATH, xpath).text
    except Exception:
        return None

# Clean and convert rating and votes 
def clean_rating_votes(rating_text):
    try:
        avg_rating, votes = rating_text.split(' avg rating — ')
        avg_rating = float(avg_rating.strip())
        votes = int(votes.replace(' ratings', '').replace(',', '').strip())
        return avg_rating, votes
    except Exception:
        return None, None

# Clean and convert score 
def clean_score(score_text):
    try:
        return int(score_text.split(': ')[1].replace(',', '').strip())
    except Exception:
        return None

# Function to scrape a page
def scrape_page(page, writer):
    url = f"https://www.goodreads.com/list/show/1.Best_Books_Ever?page={page}"
    driver.get(url)
    time.sleep(3)
    print(f"Scraping page {page}")

    for i in range(1, 101):
        try:
            xpaths = get_xpath_for_book(i)
            book_title = get_element_text(xpaths["title"])
            author_name = get_element_text(xpaths["author"])
            rating_text = get_element_text(xpaths["rating"])
            score_text = get_element_text(xpaths["score"])

            if rating_text and score_text:
                avg_rating, votes = clean_rating_votes(rating_text)
                score = clean_score(score_text)

                if book_title and author_name and avg_rating is not None and votes is not None and score is not None:
                    writer.writerow([
                        i + (page - 1) * 100,
                        book_title,
                        author_name,
                        avg_rating,
                        votes,
                        score
                    ])
        except Exception as e:
            print(f"Error scraping book {i} on page {page}: {e}")

# Main
with open("books.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Index', 'Book Name', 'Author', 'Rating', 'Number of Votes', 'Score'])
    
    for page in range(1, 101):
        scrape_page(page, writer)

driver.quit()
