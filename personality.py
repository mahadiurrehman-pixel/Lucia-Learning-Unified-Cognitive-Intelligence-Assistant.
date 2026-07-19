import json
import os 
import random
class LuciaPersonality:
    def __init__(self,config_path="config.json"):
        self.config=self.__load_config(config_path)
        self.name=self.config.get("name","LUCIA")
        self.tone=self.config.get("tone","professional_friendly")
        self.learning_mode = self.config.get("learning_mode",True)
        self.greeting={
            "first_time":["Welcome! 🚀 Main Lucia hoon — Learning Unified Cognitive Intelligence Assistant.\n Ek AI companion jo tumhe seekhne, sochne aur create karne mein empower karti hai. ✨""",
            "Tumhara naam kya hai? Batao batao, taake Lucia tumhe pehchan sake. ✨"
            ],
            "returning":["Hey {name}! 👋 Welcome back. Kaise ho? Lucia yahan hai — batao,\n aaj kis  cheez mein help chahiye? ✨","Hey {name}! 😊 Tum wapas aa gaye. Lucia khush hai tumhe dobara dekh kar. Batao,\naaj ka mission kya hai? 🚀","Hey {name}! 👋 Lucia is back with you.Kya explore karein aaj? 🚀"
            ],
            "morning":"Good morning, {user}! ☀️Aaj kuch naya seekhne, create karne aur grow karne ka din hai. Lucia tumhare sath hai! ✨",
            "evening":"Good evening, {user}! 🌆 Chalo dekhte hain, aaj ke goals mein se kya complete karna baaki hai. Lucia ready hai! 🚀"
        }
        self.response_templates = {
            "memory_saved": "✅ Yaad rakh liya! Main is information ko future ke liye save kar rahi hoon: {info}",
            "memory_found": "🧠 Haan {user}, mujhe yaad hai: {info}",
            "memory_not_found": "🤔 Mujhe iske baare mein abhi yaad nahi hai. Agar tum bata do to main ise yaad rakh sakti hoon!",
            "learning_confirm": "📚 Kya tum chahte ho ke main ye information yaad rakhun?\n\n'{info}'\n\n(haan/nahi)",
            "learning_saved": "✅ Great! Maine ye seekh liya aur save kar liya.",
            "emotion_stressed": "😟 Lag raha hai tum thode stressed ho. Koi baat nahi, Lucia tumhare sath hai. Chalo mil kar solve karte hain! ✨",
            "emotion_happy": "😊 Ye dekh kar acha laga ke tum khush ho! Keep growing 🚀",
            "emotion_neutral": "👍 Samajh gayi. Batao, Lucia tumhari kis cheez mein help kare?",
            "error": "⚠️ Sorry {user}, kuch unexpected problem aa gayi. Ek baar phir try karte hain.",
            "goodbye": "Bye {user}! 👋 Apna khayal rakhna. Lucia yahin hogi jab tum wapas aao ge. ✨",
            "dont_understand": "🤔 Mujhe ye clear nahi hua. Thoda aur explain kar do, main help karne ki koshish karti hoon.",
        }
        print(f"[PERSONALITY]  {self.name} personality loaded!")
    def __load_config(self,config_path):
        if os.path.exists(config_path):
            with open(config_path,"r",encoding="utf-8") as f:
                config =json.load(f)
                print(f"[PERSONALITY] : Config loaded from {config_path}")
                return config
        else:
            print("[PERSONALITY] config file not found using default")
            return{
                "name":"LUCIA",
                "tone":"professional_friendly",
                "learning_mode": True,
                "language":"hinglish"
            }
    def get_greeting(self, user_name=None, is_first_time=False):
        if is_first_time or not user_name:
            greeting=self.greeting["first_time"][0]
            extra=self.greeting["first_time"][1]
            return f"{greeting}\n{extra}"
        else:
            greeting=random.choice(self.greeting["returning"])
            return greeting.format(name=user_name)
    def format_response(self,template_key,**kwargs):
        template = self.response_templates.get(template_key,self.response_templates["dont_understand"])
        try:
            return template.format(**kwargs)
        except KeyError:
            return template
    def get_emotion_response(self,emotion):
        emotion_map={
            "stressed": self.response_templates["emotion_stressed"],
            "anxious": self.response_templates["emotion_stressed"],
            "worried": self.response_templates["emotion_stressed"],
            "happy": self.response_templates["emotion_happy"],
            "excited": self.response_templates["emotion_happy"],
            "neutral": self.response_templates["emotion_neutral"],
        }
        return emotion_map.get(emotion, self.response_templates["emotion_neutral"])
    def get_help_text(self):
        help_task=f"""
        
            ╔══════════════════════════════════════════════════════╗
            ║              🤖 Lucia - Help Guide                  ║
            ╠══════════════════════════════════════════════════════╣
            ║ 👋 MEMORY                                           ║
            ║ • Mera naam ALI hai      → Main yaad rakhungi    ║
            ║ • Mera naam kya hai?         → Main bata dungi      ║
            ║ • Tumhe kya yaad hai?        → Saari memories       ║
            ║ • Bhool ja [memory]          → Memory delete        ║
            ║                                                      ║
            ║ 📚 LEARNING                                         ║
            ║ • Ye yaad rakh...            → Save kar lungi       ║
            ║ • Hamara workflow ye hai...  → Future reference     ║
            ║ • Isko seekh lo              → Knowledge add        ║
            ║                                                      ║
            ║ 💬 CHAT                                             ║
            ║ • Koi bhi sawal pucho        → Main help karungi    ║
            ║ • Coding, AI, ideas          → Ready 🚀             ║
            ║ • Mood share karo            → Main samajhne ki     ║
            ║                                koshish karungi      ║
            ║                                                     ║
            ║ ⚙️ COMMANDS                                         ║
            ║ • help                       → Ye guide             ║
            ║ • status                     → Memory status        ║
            ║ • clear                      → Screen clear         ║
            ║ • bye / exit / quit          → Lucia band karo      ║
            ║                                                      ║
            ║ 💙 Tip: Jitna zyada hum baat karenge, utni hi        ║
            ║       personal aur useful assistance milegi.        ║
            ╚══════════════════════════════════════════════════════╝
            """
        return help_task
#------TEST------
# if __name__ == "__main__":

#     p = LuciaPersonality()

#     print("\n--- Pehli baar ---")
#     print(p.get_greeting(is_first_time=True))

#     print("\n--- Wapas aaya ---")
#     print(p.get_greeting("Mahadi"))

#     print("\n--- Memory saved ---")
#     print(p.format_response("memory_saved", info="company = TechCorp"))

#     print("\n--- Emotion ---")
#     print(p.get_emotion_response("happy"))

#     print("\n--- Help ---")
#     print(p.get_help_text())
