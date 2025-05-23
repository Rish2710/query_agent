from internal_knowledgebase import search_reports
from external_apibase import fetch_external_reports
from probing_question import generate_probing_questions
from ticket_logger_slack_notifier import log_ticket


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
        
        # Stage 2: Search External API
        print("\n🤖 Searching External knowledge base!")
        reports = fetch_external_reports(query)
        if reports:
            print("\n🔍 External Reports Found:")
            for report in reports:
                print(f"📄 {report['title']}: {report['desc']}")
            
            feedback = input("\nAre these reports useful? (yes/no): ").strip().lower()
            if feedback == "yes":
                continue

        # Stage 3: Intelligent Probing
        print("\n🤖 No Matching Reports Found.")
        print("\n🤖 Let's refine your request further.")
        probing_questions = generate_probing_questions(query)
        probing_details = {}
        
        for question in probing_questions:
            answer = input(f"{question}: ")
            probing_details[question] = answer

        # Stage 4: Escalation
        print("\n🤖 No relevant reports found. Escalating to CSM team...")
        
        log_ticket(query, reports, probing_details)

        
if __name__ == "__main__":
    main()
