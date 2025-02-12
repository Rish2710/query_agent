from internal_knowledgebase import search_reports


def main():
    print("Welcome to the Analytics Query Agent! Type 'exit' to quit.")
    
    while True:
        query = input("\nEnter your analytics report request: ").strip()
        if query.lower() == "exit":
            break
        
        # Stage 1: Search internal reports
        reports = search_reports(query)

        if reports:
            print("\n🔍 Matching Internal Reports Found:")
            for report in reports:
                print(f"📄 {report['title']}: {report['desc']}")

            feedback = input("\nAre these reports useful? (yes/no): ").strip().lower()
            if feedback == "yes":
                continue

        
if __name__ == "__main__":
    main()
