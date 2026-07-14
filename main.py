import sys 
import os
from learning import LuciaLearning
from memory import LuciaMemory
from personality import LuciaPersonality
from nlp_engine import LuciaNLP
class LUCIA:
    def __init__(self):
        print("\n"+"="*60)
        print("LUCIA initializing.....")
        print("="*60+"\n")
        self.memory=LuciaMemory()
        self.personality=LuciaPersonality("config.json")
        self.nlp=LuciaNLP()
        self.learning=LuciaLearning(self.memory,self.nlp)
        self.is_running=True
        self.waiting_for_confirmation=False
        self.current_user=None
        saved_name=self.memory.get_memory("name","personal_info")
        if saved_name:
            self.current_user=saved_name
        print("\n"+"="*60)
        print("LUCIA V 0.1 is ready")
        print("="*60+"\n")
    def start(self):
        if self.current_user:
            print(f"\nLUCIA: {self.personality.get_greeting(self.current_user)}")
        else:
            print(f"\nLUCIA: {self.personality.get_greeting(is_first_time=True)}")
        while self.is_running:
            try:
                user_input=input("\nYou: ").strip()
                if not user_input:
                    print("LUCIA: Kuch to bolo ")
                    continue
                response=self.process_input(user_input)
                print(f"\nLUCIA: {response}")
            except KeyboardInterrupt:
                #close by cntrl + c
                print("\n")
                self.shutdown()
            except Exception as e:
                print(f"\n🤖 LUCIA: ⚠️ Ek error aa gaya: {str(e)}")
                print("   Koi baat nahi, phir se try karo!") 
    def process_input(self,text):
        if self.waiting_for_confirmation:
            return self._handle_confirmation(text)
        analysis=self.nlp.analyze(text)
        intent = analysis["intent"]
        emotion=analysis["emotion"]
        emotion_score=analysis["emotion_score"]
        keywords=analysis["keywords"]
        extracted_info=analysis["extracted_info"]
        text_type=self.nlp.classify_text(text)
        self._show_debug(analysis,text_type)
        response=self._handle_intent( intent, text, analysis, extracted_info, emotion)
        self.memory.save_conversation(
            user_message=text,
            lucia_response=response,
            emotion_detected=emotion,
            intent_detected=intent
        )
        if emotion_score > 0.5  and emotion not in ["neutral","happy"]:
            emotion_response = self.personality.get_emotion_response(emotion)
            response = f"{emotion_response}\n\n{response}"
        return response
    def _handle_intent(self,intent,text,analysis,extract_info,emotion):
        if intent == "greeting":
            if self.current_user:
                return self.personality.get_greeting(self.current_user)
            else:
                return self.personality.get_greeting(is_first_time=True)
        elif intent == "name_tell":
            if "name" in extract_info:
                name = extract_info["name"]
                self.memory.save_memory("name",name,"personal_info")
                self.current_user=name
                return(
                    f"Welcome aboard, {name}! 🚀\n"
                    f"Lucia ne tumhara naam yaad rakh liya hai. 🧠✨\n"
                    f"Ab batao, aaj hum kya seekhenge, create karenge ya solve karenge?"
                )
            else:
                return "Tumhara name kia ha? Clearly batao."
        elif intent == "name_ask":
            name = self.memory.get_memory("name", "personal_info")
            if name:
                return f"🧠 Tumhara naam {name} hai!"
            else:
                return self.personality.format_response("memory_not_found")
        elif intent == "memory_ask":
            return self._show_memories()
        elif intent == "memory_delete":
            return self._handle_delete(text,analysis["keywords"])
        elif intent == "teach":
            return self._handle_teaching(text)
        elif intent == "help":
            return self.personality.get_help_text()
        elif intent == "status":
            return self._show_status()
        elif intent == "goodbye":
            self.shutdown()
            user = self.current_user or "dost"
            return self.personality.format_response("goodbye", user=user)
        elif intent == "thanks":
            user = self.current_user or "dost"
            return f"Koi baat nahi, {user}! Main hoon na! 😊"
        elif intent == "personal_info":
            return self._handle_personal_info(text, extract_info)
        elif intent == "productivity_help":
            return self._handle_productivity(text, emotion)
        else:
            return self._handle_general(text, analysis)
    def _handle_confirmation(self,text):
        text_lower=text.lower().strip()
        self.waiting_for_confirmation=False
        if text_lower in ["haan", "ha", "yes", "y", "ji", "ok", "okay", "save", "correct", "sahi"]:
            return self.learning.confirm_learning(True)
        elif text_lower in ["nahi", "na", "no", "n", "mat", "cancel", "galat", "wrong"]:
            return self.learning.confirm_learning(False)
        else:
            self.waiting_for_confirmation = True
            return "Sirf 'haan' ya 'nahi' bolo - save karun kya?"
    def _handle_teaching(self,text):
        result = self.learning.process_teaching(text)
        self.waiting_for_confirmation=True
        return result["message"]
    def _handle_personal_info(self,text,extracted_info):
        saved_something=False
        response_part=[]
        for info_type , value in extracted_info.items():
            self.memory.save_memory(info_type,value,"personal_info")
            response_part.append(
                self.personality.format_response(
                    "memory_saved",
                    info=f"{info_type}={value}"
                )
            )
            saved_something=True
        if saved_something:
            return "\n".join(response_part)
        else:
            self.memory.save_memory(
                "personal_note",
                text,
                "personal_info"
            )
            return self.personality.format_response(
                "memory_saved",
                info=text
            )
    def _handle_productivity(self,text,emotion):
        tips=[]
        if emotion in ["stressed","anxious","worried"]:
            tips = [
                "🎯 Aaj ke top 3 priorities likho. Sab kuch ek saath karna zaroori nahi hota.",
                "⭐ Sabse mushkil ya important task se shuru karo. (Eat the Frog 🐸)",
                "⏰ 25 minutes focus, phir 5 minutes ka break. Pomodoro magic! 🍅",
                "📝 Agar koi task bada lag raha hai, usse chhote aur simple steps mein divide kar do.",
                "🚶 Thodi der walk ya stretch kar lo. Kabhi kabhi 5 minutes hi energy wapas le aate hain.",
                "💧 Pani pee lo! Hydrated rehna bhi productivity ka hissa hai.",
                "🎧 Agar focus nahi ban raha, distraction-free environment try karo.",
                "🚀 Progress perfection se zyada important hoti hai. Bas next step lo.",
                "😌 Agar stress feel ho raha hai, 5 deep breaths lo. Phir dobara shuru karte hain.",
                "✨ Chhoti wins ko celebrate karna mat bhoolo. Har step tumhe goal ke kareeb le jaata hai!"
            ]
        else:
            tips = [
                "📋 Aaj ke tasks ki ek clear list bana lo. Pehla step hamesha clarity hota hai.",
                "⭐ Tasks ko priority do: High, Medium aur Low. Pehle important kaam complete karo.",
                "⏰ Har task ke liye realistic time set karo taake focus bana rahe.",
                "✅ Jab koi task complete ho jaye to usse check karo — progress dekhna motivation deta hai.",
                "📊 Din ke end mein apna review karo: kya achieve kiya aur kal kya improve karna hai?",
                "🎯 Ek waqt mein ek task par focus karo. Multitasking aksar productivity kam kar deti hai.",
                "🚀 Chhoti progress bhi progress hoti hai. Bas consistently aage badhte raho!"
            ]
        response="Ye try karo:\n\n"
        for tip in tips:
            response+=f"{tip}\n"
        response+="\nKoi specific task hai jismein help chahiye?"
        return response
    def _handle_delete(self,text,keywords):
        if keywords:
            for kw in keywords:
                existing=self.memory.get_memory(kw)
                if existing:
                    self.memory.delete_memory(kw)
                    return f"🗑️ '{kw}' ko bhool gayi main."
        return "Kya bhoolna hai? Clearly batao, jaise: 'bhool ja name'"
    def _handle_general(self,text,analysis):
        keywords=analysis["keywords"]
        extracted_info=analysis["extracted_info"]
        if extracted_info:
            response=[]
            for key,value in extracted_info.items():
                self.memory.save_memory(key,value,"auto_extracted")
                response.append(f"{key}: {value}")
            return (
                f"Main ne ye note kar liya: {', '.join(response)}\n"
                f"Aur kuch batana hai?"
            )
        if len(text.split())>8:
            return self._handle_teaching(text)
        if keywords:
            for kw in keywords:
                results = self.memory.search_memory(kw)
                if results:
                    info = "\n".join(
                        [f"  • {r['key']}: {r['value']}" for r in results[:3]])
                    return f"'{kw}' ke baare mein mujhe ye pata hai:\n\n{info}"
        return self.personality.format_response("dont_understand")
    def _show_memories(self):
        all_memories= self.memory.get_all_memories()
        if not all_memories:
            return "Abhi meri memory khaali hai. Kuch batao! "
        response="Mujhe ye sab yaad hai:\n\n"
        categories = {}
        for mem in all_memories:
            cat = mem["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(mem)
        
        for cat, items in categories.items():
            response += f"  📁 {cat.upper()}:\n"
            for item in items:
                response += f"     • {item['key']}: {item['value']}\n"
            response += "\n"
        
        return response
    def _show_status(self):
        all_memories = self.memory.get_all_memories()
        recent_convos = self.memory.get_recent_conversations(10)
        learned = self.memory.get_all_memories("learned_knowledge")
        
        status = f"""
╔══════════════════════════════════════╗
║       🤖 LUCIA Status Report        ║
╠══════════════════════════════════════╣
║                                      ║
║  📊 Memories: {len(all_memories):>20} ║
║  💬 Conversations: {len(recent_convos):>15} ║
║  📚 Learned Topics: {len(learned):>14} ║
║  👤 Current User: {str(self.current_user or 'Unknown'):>16} ║
║  🟢 Status: Active                  ║
║                                      ║
╚══════════════════════════════════════╝
"""
        return status
    
    def _show_debug(self, analysis, text_type):  
        print(f"\n   ┌─── 🔍 NLP Analysis ───")
        print(f"   │ Emotion: {analysis['emotion']} ({analysis['emotion_score']})")
        print(f"   │ Intent: {analysis['intent']}")
        print(f"   │ Type: {text_type}")
        print(f"   │ Keywords: {analysis['keywords']}")
        print(f"   │ Info: {analysis['extracted_info']}")
        print(f"   └────────────────────────")
    
    def shutdown(self):
        self.is_running = False
        self.memory.close()
        
        print("\n" + "═" * 60)
        print("  🔒 LUCIA v0.1 shutting down...")
        print("  💾 All memories saved!")
        print("  👋 Goodbye!")
        print("═" * 60 + "\n")
if __name__ == "__main__":
    lucia = LUCIA()
    lucia.start()