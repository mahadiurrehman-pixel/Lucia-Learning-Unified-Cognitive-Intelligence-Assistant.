import sys
import os
import ollama
from learning import LuciaLearning
from memory import LuciaMemory
from personality import LuciaPersonality
from nlp_engine import LuciaNLP


class LUCIA:
    def __init__(self):
        print("\n" + "=" * 60)
        print("LUCIA initializing.....")
        print("=" * 60 + "\n")

        self.memory = LuciaMemory()
        self.personality = LuciaPersonality("config.json")
        self.nlp = LuciaNLP()
        self.learning = LuciaLearning(self.memory, self.nlp)
        self.is_running = True
        self.waiting_for_confirmation = False
        self.current_user = None

        self.conversation_history = []
        self.max_history = 6

        self.ollama_model = "llama3.2:3b"
        self.ollama_available = self._check_ollama()

        saved_name = self.memory.get_memory("name", "personal_info")
        if saved_name:
            self.current_user = saved_name

        print("\n" + "=" * 60)
        print("LUCIA V 0.2 is ready")
        print("=" * 60 + "\n")

    def _check_ollama(self):
        try:
            ollama.list()
            print("[LUCIA] ✅ Ollama connected!")
            return True
        except Exception:
            print("[LUCIA] ⚠️ Ollama not found — fallback mode active")
            return False

    def start(self):
        if self.current_user:
            print(
                f"\nLUCIA: "
                f"{self.personality.get_greeting(self.current_user)}"
            )
        else:
            print(
                f"\nLUCIA: "
                f"{self.personality.get_greeting(is_first_time=True)}"
            )

        while self.is_running:
            try:
                user_input = input("\nYou: ").strip()

                if not user_input:
                    print("LUCIA: Kuch to bolo")
                    continue

                response = self.process_input(user_input)

                # ✅ FIX: Sirf tab print karo jab still running ho
                if response:
                    print(f"\nLUCIA: {response}")

            except KeyboardInterrupt:
                print("\n")
                self._safe_shutdown()
                break
            except Exception as e:
                print(f"\nLUCIA: ⚠️ Error: {str(e)}")
                print("   Koi baat nahi, phir se try karo!")

    def process_input(self, text):
        if self.waiting_for_confirmation:
            return self._handle_confirmation(text)

        analysis = self.nlp.analyze(text)
        intent = analysis["intent"]
        emotion = analysis["emotion"]
        emotion_score = analysis["emotion_score"]
        extracted_info = analysis["extracted_info"]
        text_type = self.nlp.classify_text(text)

        self._show_debug(analysis, text_type)

        # ✅ FIX 1: History PEHLE update karo
        # Taake Ollama call mein current message available ho
        self.conversation_history.append({
            "role": "user",
            "content": text
        })

        # History trim — user message add hone ke baad
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = (
                self.conversation_history[-self.max_history:]
            )

        response = self._handle_intent(
            intent, text, analysis, extracted_info, emotion
        )

        special_intents = {
            "greeting", "goodbye", "thanks", "help",
            "status", "name_ask", "name_tell",
            "memory_ask", "memory_delete"
        }

        if (
            emotion_score > 0.5
            and emotion not in ["neutral", "happy"]
            and intent not in special_intents
        ):
            emotion_response = self.personality.get_emotion_response(
                emotion
            )
            response = f"{emotion_response}\n\n{response}"

        # ✅ FIX 1: Assistant response bhi history mein add karo
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })

        self.memory.save_conversation(
            user_message=text,
            lucia_response=response,
            emotion_detected=emotion,
            intent_detected=intent
        )

        return response

    def _handle_intent(
        self, intent, text, analysis, extract_info, emotion
    ):
        if intent == "greeting":
            if self.current_user:
                return self.personality.get_greeting(self.current_user)
            else:
                return self.personality.get_greeting(is_first_time=True)

        elif intent == "name_tell":
            if "name" in extract_info:
                name = extract_info["name"]
                self.memory.save_memory("name", name, "personal_info")
                self.current_user = name
                return (
                    f"Welcome aboard, {name}! 🚀\n"
                    f"Lucia ne tumhara naam yaad rakh liya. 🧠✨\n"
                    f"Ab batao, aaj kya karein?"
                )
            else:
                return "Tumhara naam clearly batao."

        elif intent == "name_ask":
            name = self.memory.get_memory("name", "personal_info")
            if name:
                return f"🧠 Tumhara naam {name} hai!"
            else:
                return self.personality.format_response(
                    "memory_not_found"
                )

        elif intent == "memory_ask":
            return self._show_memories()

        elif intent == "memory_delete":
            return self._handle_delete(text, analysis["keywords"])

        elif intent == "teach":
            return self._handle_teaching(text)

        elif intent == "help":
            return self.personality.get_help_text()

        elif intent == "status":
            return self._show_status()

        elif intent == "goodbye":
            user = self.current_user or "dost"
            # ✅ FIX 2: Pehle response banao
            response = self.personality.format_response(
                "goodbye", user=user
            )
            # ✅ FIX 2: Phir shutdown — memory.close() baad mein
            self.is_running = False
            return response

        elif intent == "thanks":
            user = self.current_user or "dost"
            return f"Koi baat nahi, {user}! Main hoon na! 😊"

        elif intent == "personal_info":
            return self._handle_personal_info(text, extract_info)

        elif intent == "productivity_help":
            return self._handle_productivity(text, emotion)

        else:
            return self._handle_general(text, analysis)

    def _handle_confirmation(self, text):
        text_lower = text.lower().strip()
        self.waiting_for_confirmation = False

        positive = {
            "haan", "ha", "yes", "y", "ji", "ok",
            "okay", "save", "correct", "sahi", "bilkul",
            "zaroor", "theek"
        }
        negative = {
            "nahi", "na", "no", "n", "mat",
            "cancel", "galat", "wrong", "nope"
        }

        if text_lower in positive:
            return self.learning.confirm_learning(True)
        elif text_lower in negative:
            return self.learning.confirm_learning(False)
        else:
            self.waiting_for_confirmation = True
            return "Sirf 'haan' ya 'nahi' bolo - save karun kya?"

    def _handle_teaching(self, text):
        result = self.learning.process_teaching(text)
        self.waiting_for_confirmation = True
        return result["message"]

    def _handle_personal_info(self, text, extracted_info):
        saved_something = False
        response_parts = []

        for info_type, value in extracted_info.items():
            self.memory.save_memory(info_type, value, "personal_info")
            response_parts.append(
                self.personality.format_response(
                    "memory_saved",
                    info=f"{info_type} = {value}"
                )
            )
            saved_something = True

        if saved_something:
            return "\n".join(response_parts)
        else:
            self.memory.save_memory(
                "personal_note", text, "personal_info"
            )
            return self.personality.format_response(
                "memory_saved", info=text
            )

    def _handle_productivity(self, text, emotion):
        import random
        if emotion in ["stressed", "anxious", "worried"]:
            tips = [
                "🎯 Aaj ke top 3 priorities likho.",
                "⭐ Sabse mushkil task se shuru karo.",
                "⏰ 25 min focus, 5 min break — Pomodoro!",
                "📝 Bade task ko chhote steps mein divide karo.",
                "😌 5 deep breaths lo. Phir shuru karte hain.",
            ]
        else:
            tips = [
                "📋 Tasks ki clear list bana lo.",
                "⭐ Priority do: High, Medium, Low.",
                "✅ Har complete task check karo.",
                "🎯 Ek waqt mein ek task — focus!",
            ]

        selected = random.sample(tips, min(3, len(tips)))
        response = "Ye try karo:\n\n"
        for tip in selected:
            response += f"{tip}\n"
        response += "\nKoi specific task hai jismein help chahiye?"
        return response

    def _handle_delete(self, text, keywords):
        deleted = []

        for kw in keywords:
            existing = self.memory.get_memory(kw)
            if existing:
                self.memory.delete_memory(kw)
                deleted.append(kw)

        if deleted:
            items = ", ".join(f"'{d}'" for d in deleted)
            return f"🗑️ Bhool gayi: {items}"

        return (
            "Kya bhoolna hai? Clearly batao.\n"
            "Jaise: 'bhool ja mera naam'"
        )

    def _handle_general(self, text, analysis):
        keywords = analysis["keywords"]
        extracted_info = analysis["extracted_info"]
        emotion = analysis["emotion"]

        if extracted_info:
            response_parts = []
            for key, value in extracted_info.items():
                self.memory.save_memory(key, value, "auto_extracted")
                response_parts.append(f"{key}: {value}")
            return (
                f"Main ne ye note kar liya: "
                f"{', '.join(response_parts)}\n"
                f"Aur kuch batana hai?"
            )

        if keywords:
            for kw in keywords:
                results = self.memory.search_memory(kw)
                if results:
                    info = "\n".join([
                        f"  • {r['key']}: {r['value']}"
                        for r in results[:3]
                    ])
                    return (
                        f"'{kw}' ke baare mein mujhe ye pata hai:"
                        f"\n\n{info}"
                    )

        if self.ollama_available:
            return self._get_ollama_response(text, analysis)

        return self.personality.format_response("dont_understand")

    def _get_ollama_response(self, text, analysis):
        emotion = analysis.get("emotion", "neutral")
        intent = analysis.get("intent", "general")
        lang = analysis.get("detected_language", "en")

        memory_context = ""
        all_mem = self.memory.get_all_memories("personal_info")
        if all_mem:
            lines = [
                f"- {m['key']}: {m['value']}"
                for m in all_mem[:5]
            ]
            memory_context = "\nUSER INFO:\n" + "\n".join(lines)

        knowledge_context = ""
        if analysis["keywords"]:
            for kw in analysis["keywords"][:2]:
                results = self.memory.get_learned_info(kw)
                if results:
                    knowledge_context += (
                        f"\nKNOWLEDGE about {kw}:\n"
                        f"{results[0]['content']}\n"
                    )

        system_prompt = f"""You are Lucia — a smart, warm AI assistant.

PERSONALITY:
- Respond in Hinglish (Roman Urdu + English mix)
- Be warm, friendly, like a helpful friend
- Keep responses focused (2-4 sentences)
- Match tone with emotion: {emotion}
- User's language detected: {lang}

RULES:
1. Always Hinglish mein jawab do
2. Short aur clear raho
3. Agar emotional ho → empathize first
4. End with a helpful question ya suggestion
5. Never be robotic
{memory_context}
{knowledge_context}

CONTEXT:
- User emotion: {emotion}
- User intent: {intent}
"""
        # ✅ FIX 1: Ab history already updated hai process_input mein
        # Isliye sirf last 4 entries use karo (current message include)
        messages = [
            {"role": "system", "content": system_prompt}
        ] + self.conversation_history[-4:]

        try:
            response = ollama.chat(
                model=self.ollama_model,
                messages=messages,
                options={
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 120,
                    "num_ctx": 2048,
                    "num_thread": 4
                }
            )
            return response["message"]["content"].strip()

        except Exception as e:
            print(f"[LUCIA] Ollama error: {e}")
            return self.personality.format_response("dont_understand")

    def _show_memories(self):
        all_memories = self.memory.get_all_memories()
        if not all_memories:
            return "Abhi meri memory khaali hai. Kuch batao!"

        response = "Mujhe ye sab yaad hai:\n\n"
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
        ollama_status = (
            "✅ Active" if self.ollama_available else "❌ Offline"
        )

        status = f"""
╔══════════════════════════════════════╗
║       🤖 LUCIA Status Report        ║
╠══════════════════════════════════════╣
║                                      ║
║  📊 Memories    : {len(all_memories):<20}║
║  💬 Conversations: {len(recent_convos):<19}║
║  📚 Learned     : {len(learned):<20}║
║  👤 User        : {str(self.current_user or 'Unknown'):<20}║
║  🧠 Ollama      : {ollama_status:<20}║
║  🟢 Status      : Active             ║
║                                      ║
╚══════════════════════════════════════╝
"""
        return status

    def _show_debug(self, analysis, text_type):
        print(f"\n   ┌─── 🔍 NLP Analysis ───")
        print(f"   │ Emotion : {analysis['emotion']} ({analysis['emotion_score']})")
        print(f"   │ Intent  : {analysis['intent']}")
        print(f"   │ Type    : {text_type}")
        print(f"   │ Lang    : {analysis.get('detected_language', 'en')}")
        print(f"   │ Keywords: {analysis['keywords'][:5]}")
        print(f"   │ Info    : {analysis['extracted_info']}")
        print(f"   └────────────────────────")

    def _safe_shutdown(self):
        """Gracefully band karo"""
        self.is_running = False
        try:
            self.memory.close()
        except Exception:
            pass

        print("\n" + "═" * 60)
        print("  🔒 LUCIA v0.2 shutting down...")
        print("  💾 All memories saved!")
        print("  👋 Goodbye!")
        print("═" * 60 + "\n")

    def shutdown(self):
        self._safe_shutdown()


if __name__ == "__main__":
    lucia = LUCIA()
    lucia.start()