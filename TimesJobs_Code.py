import requests
import csv
from bs4 import BeautifulSoup

# ============================
# 🔍 Configuration
# ============================
SEARCH_TERM = input("What job are you looking for: ")
YEARS_OF_EXPERIENCE = int(input("How many years of experience are you looking for: "))
BASE_URL = f"https://m.timesjobs.com/mobile/jobs-search-result.html?txtKeywords={SEARCH_TERM}&cboWorkExp1={YEARS_OF_EXPERIENCE}&txtLocation="

# This will store all job dictionaries
all_jobs = []


# ============================
# 🧭 Scraping Function
# ============================
def scrape_jobs(url):
    """Scrape job listings from TimesJobs search results."""
    response = requests.get(url)
    response.raise_for_status()  # Raise an error if the request failed

    soup = BeautifulSoup(response.text, "html.parser")
    job_cards = soup.find_all("div", class_="srp-job-bx")

    for job in job_cards:
        # Extract job title and link
        title_tag = job.find("h3")
        job_title = title_tag.get_text(strip=True) if title_tag else "N/A"

        link_tag = job.find("a")
        job_link = link_tag.get("href") if link_tag else "N/A"

        # Extract company and listing time
        h4_tag = job.find("h4")
        if h4_tag:
            company_info = h4_tag.get_text(strip=True).split("|")
            company_name = company_info[0] if len(company_info) > 0 else "N/A"
            listing_time = company_info[1] if len(company_info) > 1 else "N/A"
        else:
            company_name = "N/A"
            listing_time = "N/A"

        # Extract skills list
        skills_tags = job.find_all("a", class_="srphglt")
        skills_list = " | ".join([s.get_text(strip=True) for s in skills_tags]) if skills_tags else "N/A"

        # Extract other details (location, experience, salary)
        location = job.find("div", class_="srp-loc")
        experience = job.find("div", class_="srp-exp")
        salary = job.find("div", class_="srp-sal")

        all_jobs.append({
            "Job Title": job_title,
            "Company": company_name,
            "Listing Time": listing_time,
            "Location": location.get_text(strip=True) if location else "N/A",
            "Experience": experience.get_text(strip=True) if experience else "N/A",
            "Salary": salary.get_text(strip=True) if salary else "N/A",
            "Skills": skills_list,
            "Job Link": job_link
        })


# ============================
# 📄 CSV Export Function
# ============================
def export_to_csv():
    """Export scraped jobs to a CSV file."""
    if not all_jobs:
        print("⚠️ No jobs found to export.")
        return

    file_path = f"{SEARCH_TERM}_Jobs_{YEARS_OF_EXPERIENCE}_Years.csv"
    header = all_jobs[0].keys()

    with open(file_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(all_jobs)

    print(f"✅ File saved successfully: {file_path}")


# ============================
# 🚀 Run the Script
# ============================
if __name__ == "__main__":
    scrape_jobs(BASE_URL)
    export_to_csv()
