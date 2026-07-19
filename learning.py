from nlp_engine import LuciaNLP
from memory import LuciaMemory

class LuciaLearning:
    def __init__(self,memory,nlp):
        self.memory=memory
        self.nlp=nlp
        self.pending_item=[]
        print("[LEARNING] learning system initialzed!")
    def process_teaching(self,text):
        analysis=self.nlp.analyze(text)
        keywords = analysis["keywords"]
        topic =self.__identify_topic(text,keywords)
        content = self.__clean_content(text)
        learning_item={
            "topic":topic,
            "content":content,
            "keywords":keywords,
            "confirmed":False
        }
        self.pending_item.append(learning_item)
        return{
            "topic": topic,
            "content":content,
            "need_confirmation":True,
            "message": f"📚 Main ne ye samjha:\n\n"
                       f"   Topic: {topic}\n"
                       f"   Info: {content}\n\n"
                       f"   Kya ye sahi hai? Save kar lun? (haan/nahi)"
        }
    def confirm_learning(self,confirmed=True):
        if not self.pending_item:
            return "Kuch Pending nhi ha save ke liye"
        item=self.pending_item.pop()
        if confirmed:
            self.memory.save_learned_info(
                topic=item["topic"],
                contents=item["content"],
                verified=True
            )
            self.memory.save_memory(
                key=item["topic"],
                value=item["content"],
                category="learned_knowledge"
            )
            return f"✅ Seekh liya! '{item['topic']}' save ho gaya."
        else:
            return "❌ Okay, ye information discard kar di."
    def __identify_topic(self,text,keywords):
        text_lower=text.lower()
        # Topic mapping
        topic_hints = {
            "workflow": [
                "workflow", "work flow", "process", "procedure", "tarika", "tareeqa",
                "method", "step", "steps", "system", "how it works", "kaise hota hai",
                "kaam ka flow", "sequence", "pipeline", "operation"
            ],

            "company": [
                "company", "organization", "organisation", "firm", "office", "startup",
                "business", "brand", "enterprise", "workplace", "comapny", "idara"
            ],

            "team": [
                "team", "group", "member", "members", "colleague", "colleagues",
                "staff", "employee", "employees", "coworker", "co-worker",
                "manager", "lead", "leader", "boss", "crew", "department"
            ],

            "project": [
                "project", "assignment", "task", "tasks", "kaam", "work", "job",
                "deliverable", "milestone", "module", "feature", "implementation",
                "execution", "initiative"
            ],

            "rule": [
                "rule", "rules", "policy", "policies", "niyam", "guideline",
                "guidelines", "instruction", "instructions", "protocol", "principle",
                "restriction", "compliance", "discipline", "qanoon"
            ],

            "preference": [
                "pasand", "prefer", "like", "favorite", "favourite", "choice",
                "priority", "interested", "interest", "love", "enjoy", "option",
                "selection", "taste"
            ],

            "schedule": [
                "schedule", "time", "timing", "routine", "calendar", "timetable",
                "time table", "plan", "agenda", "slot", "availability", "day plan",
                "weekly plan", "monthly plan", "shift"
            ],

            "tool": [
                "tool", "software", "app", "application", "use", "platform",
                "system", "portal", "dashboard", "website", "service", "utility",
                "program", "script", "automation"
            ],

            "deadline": [
                "deadline", "due date", "last date", "time limit", "urgent",
                "asap", "jaldi", "fauran", "end date", "submission date", "target date"
            ],

            "meeting": [
                "meeting", "call", "zoom", "google meet", "discussion", "sync",
                "standup", "stand-up", "session", "briefing", "catchup", "1 on 1",
                "one on one"
            ],

            "client": [
                "client", "customer", "buyer", "user", "consumer", "partner",
                "stakeholder", "vendor", "customer issue", "client requirement"
            ],

            "product": [
                "product", "service", "feature", "item", "solution", "offering",
                "package", "plan", "subscription", "version"
            ],

            "support": [
                "support", "help", "assist", "assistance", "madad", "guide",
                "guidance", "issue", "problem", "ticket", "complaint", "query"
            ],

            "training": [
                "training", "learn", "learning", "course", "tutorial", "onboarding",
                "practice", "guide", "documentation", "manual", "lesson", "teach"
            ],

            "communication": [
                "message", "email", "mail", "chat", "call", "communication",
                "inform", "notify", "update", "report", "reply", "response"
            ],

            "performance": [
                "performance", "speed", "efficiency", "productivity", "result",
                "output", "improvement", "optimize", "optimization", "quality"
            ],

            "problem": [
                "problem", "issue", "bug", "error", "trouble", "mushkil",
                "masla", "fault", "glitch", "crash", "failure", "blocker"
            ],

            "priority": [
                "priority", "important", "urgent", "critical", "high priority",
                "top priority", "main thing", "zaroori", "ahm", "focus"
            ],

            "goal": [
                "goal", "target", "objective", "mission", "aim", "purpose",
                "result", "outcome", "achievement", "milestone"
            ],

            "finance": [
                "finance", "budget", "cost", "price", "payment", "salary",
                "expense", "revenue", "profit", "invoice", "bill", "paisa"
            ],

            "security": [
                "security", "secure", "password", "privacy", "access", "permission",
                "authorization", "authentication", "2fa", "otp", "data protection"
            ],

            "technology": [
                "technology", "tech", "api", "database", "server", "frontend",
                "backend", "code", "coding", "programming", "deployment", "integration"
            ],

            "document": [
                "document", "docs", "documentation", "file", "record", "report",
                "sheet", "excel", "pdf", "notes", "form", "paperwork"
            ],

            "location": [
                "location", "address", "place", "city", "office location",
                "branch", "site", "venue", "jagah", "pata"
            ],

            "role": [
                "role", "position", "designation", "responsibility", "duty",
                "job title", "post", "zimmedari", "farz"
            ],

            "customer_service": [
                "customer service", "service desk", "support team", "helpline",
                "complaint", "feedback", "response time", "resolution"
            ],

            "marketing": [
                "marketing", "promotion", "advertising", "campaign", "social media",
                "branding", "lead generation", "audience", "reach", "engagement"
            ],

            "sales": [
                "sales", "selling", "lead", "prospect", "conversion", "deal",
                "revenue", "offer", "discount", "purchase", "order"
            ],

            "hr": [
                "hr", "human resources", "recruitment", "hiring", "interview",
                "leave", "attendance", "payroll", "employee policy"
            ],

            "leave": [
                "leave", "vacation", "holiday", "off day", "day off", "chutti",
                "sick leave", "casual leave", "annual leave"
            ],

            "attendance": [
                "attendance", "present", "absent", "check in", "check out",
                "punch", "login time", "logout time", "haazri"
            ],

            "remote_work": [
                "remote", "work from home", "wfh", "hybrid", "onsite", "office work",
                "home office", "remote job"
            ]
        }
        found_topic=[]
        for topic, hints in topic_hints.items():
            for hint in hints:
                if hint in text_lower:
                    found_topic.append(topic)
                    break
        if found_topic:
            return "_".join(found_topic[:2])
        elif keywords:
            return "_".join(keywords[:2])
        else:
            return "general_info"
    def __clean_content(self,text):
        prefixes_to_remove = [
            "ye yaad rakh ke", "yaad rakh", "note kar",
            "save kar", "seekh le", "jaan le",
            "batata hoon", "bata raha hoon",
            "sun", "dekh", "samajh"
        ]
        content = text
        for prefix in prefixes_to_remove:
            if content.lower().startswith(prefix):
                content=content[len(prefix):].strip()
        return content.strip()
    def get_learned_topics(self):
        all_knowledge=self.memory.get_all_memories("learned_knowledge")
        if not all_knowledge:
            return "Abhi tak kuch nahi seekha. Mujhe kuch sikhao! 😊"
        topics="📚 Maine ye seekha hai:\n\n"
        for i , item in enumerate(all_knowledge,1):
            topics += f"  {i}. {item['key']}: {item['value']}\n"
        return topics
    def search_knowledge(self,query):
        results = self.memory.get_learned_info(query)
        if results:
            response = f"📚 '{query}' ke baare mein ye pata hai:\n\n"
            for r in results:
                verified = "✅" if r["verified"] else "⚠️"
                response += f"  {verified} {r['content']}\n"
            return response
        return None
# #------TEST------
# if __name__ == "__main__":

#     memory   = LuciaMemory()
#     nlp      = LuciaNLP()
#     learning = LuciaLearning(memory, nlp)

#     print("\n--- Test 1: Process Teaching ---")
#     result = learning.process_teaching(
#         "Hamari company ka workflow ye hai: pehle design karo, phir code, phir test"
#     )
#     print(result["message"])

#     print("\n--- Test 2: Confirm (haan) ---")
#     print(learning.confirm_learning(True))

#     print("\n--- Test 3: Learned Topics ---")
#     print(learning.get_learned_topics())

#     print("\n--- Test 4: Search Knowledge ---")
#     print(learning.search_knowledge("workflow"))

#     memory.close()