import os
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import time
from urllib.parse import urlparse, unquote

# List of links extracted from the sidebar
links = [
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/appsec/general-notes", "text":"General Notes"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/appsec/payloads", "text":"Payloads"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/appsec/fuzzing", "text":"Fuzzing"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/appsec/code-review", "text":"Code Review"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/appsec/redos", "text":"ReDos"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/appsec/ssti", "text":"SSTI"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/appsec/lfi-rfi", "text":"LFI-RFI"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/appsec/php-tricks", "text":"PHP Tricks"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/appsec/javascript", "text":"Javascript"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/appsec/serialization", "text":"Serialization"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/appsec/sql-injection", "text":"SQL Injection"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/appsec/jwt", "text":"JWT"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/appsec/graphql", "text":"GraphQL"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/appsec/side-channel", "text":"Side Channel"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/appsec/command-execution", "text":"Command Execution"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/appsec/websockets", "text":"WebSockets"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/appsec/ruby", "text":"Ruby"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/appsec/0auth", "text":"0Auth"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/appsec/latex-injection", "text":"Latex Injection"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/appsec/nosql", "text":"NoSQL"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/appsec/js-analysis", "text":"JS Analysis"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/appsec/apache-lucene", "text":"Apache Lucene"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/forensics", "text":"Forensics"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/binary-exploitation", "text":"Binary-Exploitation"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/malware-analysis", "text":"Malware-Analysis"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/reverse-engineering", "text":"Reverse-Engineering"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/services/snmp", "text":"SNMP"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/services/grafana", "text":"Grafana"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/services/consul", "text":"Consul"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/network-pentesting/c2-servers", "text":"C2 Servers"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/network-pentesting/pivoting", "text":"Pivoting"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/network-pentesting/crackmapexec", "text":"CrackMapExec"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/network-pentesting/kubernetes", "text":"Kubernetes"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/network-pentesting/docker", "text":"Docker"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/misc", "text":"MISC"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/cloud-hacking", "text":"Cloud Hacking"},
  {"href":"https://pwnsec-notes.gitbook.io/ctf-notes/mobile-pentesting", "text":"Mobile Pentesting"}
]

BASE_DIR = "notes/ctf-notes"

def fetch_and_save(url, title):
    try:
        print(f"Fetching {title} from {url}...")
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # GitBook content is usually in <main>
        content = soup.find('main')
        if not content:
            print(f"Warning: No main content found for {url}")
            return

        # Convert to markdown
        markdown = md(str(content), heading_style="ATX")
        
        # Clean up markdown (optional: remove excessive newlines)
        markdown = markdown.strip()
        
        # Determine file path
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.strip('/').split('/')
        
        # Remove 'ctf-notes' from path if present to avoid redundancy
        if path_parts[0] == 'ctf-notes':
            path_parts = path_parts[1:]
            
        if not path_parts:
            file_path = os.path.join(BASE_DIR, "readme.md")
        else:
            # Create directories
            dir_path = os.path.join(BASE_DIR, *path_parts[:-1])
            os.makedirs(dir_path, exist_ok=True)
            
            filename = path_parts[-1] + ".md"
            file_path = os.path.join(BASE_DIR, *path_parts[:-1], filename)

        # Add title
        final_content = f"# {title}\n\n{markdown}"
        
        # Save
        with open(file_path, 'w') as f:
            f.write(final_content)
            
        print(f"Saved to {file_path}")
        
    except Exception as e:
        print(f"Error processing {url}: {e}")

def main():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
        
    for link in links:
        if not link['text']: continue # Skip empty links
        fetch_and_save(link['href'], link['text'])
        time.sleep(0.5) # Be polite

if __name__ == "__main__":
    main()
