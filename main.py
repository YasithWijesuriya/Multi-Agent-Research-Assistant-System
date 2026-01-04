import os
from dotenv import load_dotenv
from graph.workflow import create_research_workflow
from utils.state import create_initial_state  # මේක import කරන්න

load_dotenv()

def run_research(topic: str):
    """Research process එක run කරනවා"""
    
    print(f"\n🔍 Starting research on: {topic}\n")
    print("=" * 60)
    
    app = create_research_workflow()
    
    # Helper function එක use කරල state එක create කරනවා
    initial_state = create_initial_state(topic)
    
    # Workflow එක execute කරනවා
    last_step_data ={}
    for step in app.stream(initial_state):
                # 👉 app.stream() කියන්නේ
                # workflow එක step-by-step run කරලා,
                # එක් agent එකක් complete වුනාම,
                # result එක return කරන generator එකක්.
        agent_name = list(step.keys())[0]
#todo           [0] කියන්නේ?
#todo          list(step.keys())[0]
#todo          👉 Meaning:
#todo          List එකේ පළමු element එක,ඒක තමයි agent name එක

        print(f"\n✅ {agent_name.upper()} completed")
        print("-" * 60)
        # සෑම පියවරකදීම ලැබෙන දත්ත variable එකට දාගන්න
        # එවිට loop එක ඉවර වෙද්දී මෙහි ඉතිරි වන්නේ අවසාන step එකේ දත්තයි
        last_step_data = step[agent_name]

      
    
    print("\n🧠 SYSTEM LOGS")
    print("=" * 60)
    for log in last_step_data.get("logs", []):
        print(log)

    return last_step_data.get("final_report", "No report generated")

def main():
    """Main function"""
    
    print("\n🤖 ResearchHub - AI Research Assistant")
    print("=" * 60)
    
    topic = input("\nEnter research topic: ").strip()
    
    if not topic:
        print("❌ Please provide a valid topic!")
        return
    
    try:
        final_report = run_research(topic)
        
        print("\n" + "=" * 60)
        print("📄 FINAL RESEARCH REPORT")
        print("=" * 60)
        print(final_report)
        
        filename = f"report_{topic.replace(' ', '_')[:30]}.txt"
        with open(filename, "w", encoding="utf-8") as f:

    #!    "w" Write mode
	#!    File එක නැත්තම් 👉 CREATE
	#!    File එක තියෙනවා නම් 👉 OVERWRITE

            f.write(final_report)
        print(f"\n💾 Report saved to: {filename}")

#           open() → file open / create කරනවා
#          "w" → write mode (file save reason)
#           with → safe open + auto close
#           write() → content disk එකට ලියනවා
#           print() → user ට message එක
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()