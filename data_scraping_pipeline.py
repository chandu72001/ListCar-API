import subprocess

# sequence of scripts to run (relative paths)
scripts = [
    "scraper/listing_ids.py",
    "scraper/scrape.py",
    "data/data_cleaning.py",
    "data/db_connection.py",
    "data/db_schema.py",
    "data/data_insertion.py"
]

def run_pipeline(scripts):
    for script in scripts:
        print(f"\n🔄 Running {script}...")
        result = subprocess.run(["python", script], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Error running {script}")
            print(result.stderr)
            break
        else:
            print(f"Finished {script}")
            print(result.stdout)

if __name__ == "__main__":
    run_pipeline(scripts)
