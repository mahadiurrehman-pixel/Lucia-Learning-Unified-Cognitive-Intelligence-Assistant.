from textblob import TextBlob
import re
from langdetect import detect as lang_detect, LangDetectException
import argostranslate.translate
import argostranslate.package
from rapidfuzz import fuzz, process


class LuciaNLP:
    def __init__(self):
        self.hinglish_strong_markers = {
            # Personal pronouns — ye sirf Hinglish mein hote hain
            "main", "mai", "mujhe", "mujhay", "mera", "meri", "mere",
            "hum", "humara", "hamara", "humari", "hamari",
            "tum", "tumhara", "tumhari", "aap", "aapka", "aapki",
            # Core Urdu/Hindi verbs — English mein nahi hote
            "hoon", "hain", "hoga", "hogi",
            "karo", "karna", "karta", "karti",
            "gaya", "gayi", "gaye", "aaya", "aayi", "aaye",
            "raha", "rahi", "rahe", "chahiye", "chahte", "chahti",
            # Core Urdu words
            "nahi", "nahin", "bilkul", "zaroor", "kyunki", "isliye",
            "kaise", "kahan", "kaun", "kitna", "kitni",
            # Pure Urdu greetings
            "shukriya", "meherbani", "shukria",
        }

        self.hinglish_support_markers = {
            # Casual address words
            "yaar", "bhai", "bhen", "dost", "janu", "jaan",
            "abbu", "ammi", "appa",
            # Expressions — sirf Hinglish mein
            "accha", "achha", "acha", "theek",
            "waise", "matlab",
            "arrey", "arre", "oho", "oye", "uff", "uffo",
            "mashallah", "inshallah", "alhamdulillah", "subhanallah",
            # Quantity words — Urdu specific
            "bahut", "bohot", "zyada", "thoda", "thodi",
            # Pure Urdu adjectives
            "bura", "sacha", "jhuta", "purana",
            "bada", "chota", "lambi", "choti", "garam", "thanda",
            # Urdu action words
            "batao", "bata", "dekho", "dekh", "suno", "sun",
            "ruko", "ruk",
            # Time — Urdu specific
            "aaj", "kal", "parso", "abhi",
            "subah", "shaam", "raat", "dopahar", "jaldi", "dheere",
            # Urdu particles
            "wala", "wali", "wale", "walay",
            # Common Urdu nouns
            "ghar", "kaam", "baat", "cheez", "jagah", "waqt",
            "paisa", "khana", "pani", "rishta", "zindagi",
            "dil", "dimag",
            # Emotions — Urdu
            "khush", "udaas", "gussa", "pareshan", "thaka", "thaki",
        }

        self.roman_urdu_markers = {
            "allah", "allaah", "quran", "namaz", "roza", "zakat",
            "masjid", "ibadat", "tawakkul",
            "walid", "walida", "beta", "beti", "behan",
            "chacha", "chachi", "mama", "mami", "nana", "nani",
            "dada", "dadi", "phupho", "phuppa", "khala", "khalu",
            "mohabbat", "ishq", "pyaar", "izzat", "sharam",
            "koshish", "umeed", "yakeen", "bharosa",
        }

        self.arabic_only_chars = set("ةىإأؤئءًٌٍَُِّْ")

        # Ye chars Urdu mein hote hain Arabic mein nahi
        self.urdu_only_chars = set("پچڈڑژگھ")
        self.emotion_keywords = {
            "stressed": [
                "stress", "pressure", "tension", "deadline", "pareshan",
                "mushkil", "problem", "issue", "frustrated", "thak",
                "tired", "exhausted", "overwhelmed", "pagal", "irritated",
                "burnout", "thaka hua", "load", "bohot kaam", "dimag kharab",
                "mental pressure", "heavy", "anxious", "ghabrahat", "restless",
                "bechain", "panic", "dar lag raha", "nervous", "worried",
                "chinta", "ulta seedha chal raha", "handle nahi ho raha",
                "control se bahar", "overthinking", "darr", "fas gaya"
            ],
            "happy": [
                "khush", "happy", "great", "awesome", "amazing", "perfect",
                "excellent", "wonderful", "accha", "badiya", "maza",
                "excited", "fantastic", "love", "enjoy", "celebrate",
                "smile", "mast", "shandar", "zabardast", "khushi",
                "proud", "grateful", "blessed", "satisfied",
                "relaxed", "peaceful", "sukoon", "maje me", "on top",
                "feeling good", "vibes", "positive mood", "khushiyan",
                "delighted", "cheerful"
            ],
            "sad": [
                "sad", "udaas", "dukhi", "upset", "disappointed", "hurt",
                "bura", "kharab", "depressed", "lonely", "akela", "miss",
                "cry", "rona", "heartbroken", "down", "low",
                "feeling low", "demotivated", "broken", "ignore",
                "reject", "chhod diya", "dhoka", "betrayed",
                "andar se toot gaya", "regret", "pachtawa",
                "empty", "numb", "thak gaya zindagi se"
            ],
            "confused": [
                "confused", "samajh nahi", "pata nahi", "kya karu",
                "confuse", "unclear", "lost", "help", "kaise", "problem",
                "doubt", "shak", "soch raha", "soch rahi", "unsure",
                "kya hoga", "decision nahi", "clear nahi", "guide karo",
                "samajh nahi aa raha", "mind blank", "soch me pad gaya",
                "uljhan", "confusion", "idea nahi", "clarity nahi",
                "kya sahi hai", "kya galat hai"
            ],
            "angry": [
                "angry", "gussa", "annoyed", "irritated", "naraz",
                "frustrated", "bakwas", "bekar", "worst",
                "hate", "chidh", "dimag kharab", "faltu",
                "ghussa aa raha", "furious", "rage", "toxic",
                "badtameez", "cheap", "insult", "dhoka diya",
                "bardasht nahi", "sakta nahi", "bhadak gaya",
                "triggered", "pissed off"
            ],
            "motivated": [
                "motivated", "ready", "lets go", "chalte", "start",
                "begin", "fired up", "tayyar", "josh", "energy",
                "focused", "goal", "achieve", "kar dunga", "kar lungi",
                "hard work", "determined", "inspired", "positive",
                "confidence", "self belief", "hustle", "grind",
                "never give up", "try again", "improve", "discipline",
                "success", "winner", "dream", "aim", "mission",
                "dedicated", "believe in myself",
                "strong banunga", "strong banungi"
            ]
        }

        self.intent_patterns = {
            "greeting": [
                r"\b(?:hello|hi|hey|hii|heyy|helo|hlo|holla|howdy)\b",
                r"\b(?:assalam(?:u alaikum)?|salam|salaam|wa alaikum salam|walaikum salam)\b",
                r"\b(?:namaste|namaskar|pranaam|adaab)\b",
                r"\b(?:kaise ho|kese ho|kaisi ho|kesi ho|kya haal|kya haal hai|kya chal raha|kya ho raha)\b",
                r"\b(?:how are you|how r u|how are u|hows you|how do you do|whats up|what's up|wassup|sup)\b",
                r"\b(?:good morning|good afternoon|good evening|good night)\b",
                r"\b(?:subah bakhair|shab bakhair|shab khair|subh bakhair)\b",
                r"\b(?:yo|aoa|aslkm|slm|heyyy|heyya)\b"
            ],
            "name_ask": [
                r"\b(?:mera naam kya hai|mera naam kya he|mera naam kia ha|mera naam kia hai|what is my name|what's my name)\b",
                r"\b(?:my name kya hai|naam batao|mera name batao|mujhe kya kehte ho)\b",
                r"\b(?:naam yaad hai|kaun hoon main|main kaun hoon|who am i)\b",
                r"\b(?:do you know my name|remember my name|do you remember my name)\b",
                r"\b(?:tumhe mera naam yaad hai|mera naam yaad hai kya|mera naam pata hai)\b"
            ],
            "name_tell": [
                r"\b(?:mera naam|mera name|my name is|my name's|naam mera)\b",
                r"\b(?:main hoon|mai hoon|i am|i'm|myself|i go by)\b",
                r"\b(?:naam hai|call me|you can call me|just call me|everyone calls me)\b",
                r"\bmujhe\s+\w+\s+(?:bulate|kehte|kehte hain|bulate hain)\b",
                r"\blog\s+mujhe\s+\w+\s+(?:bulate|kehte)\b",
                r"\b(?:mera naam\s+\w+\s+hai|my name is\s+\w+|i am\s+\w+)\b"
            ],
            "memory_ask": [
                r"\b(?:kya yaad hai|kya yaad rakha|kya yaad rakha hai|mujhe yaad karo)\b",
                r"\b(?:tumhe kia yaad|tumhe kya yaad|kia yaad ha|kya yaad hai)\b",
                r"\b(?:mere bare mein kya yaad|mere baare mein kya pata|mere baare me kya jaanti)\b",
                r"\b(?:what do you know about me|what do you remember|what do you know)\b",
                r"\b(?:do you remember|remember anything about me|kuch yaad hai)\b",
                r"\b(?:bata kya jaanti ho|tell me what you know|apni memory batao)\b",
                r"\b(?:memory check|check memory|kitni yaadein hain|kya kuch save hai)\b",
                r"\b(?:mere baare mein batao|mere bare mein batao|mujhe kya pata hai)\b"
            ],
            "memory_delete": [
                r"\b(?:bhool ja|bhool jao|sab kuch bhool ja|forget me|forget everything)\b",
                r"\b(?:delete|remove|hata de|hata do|mita de|mita do)\b",
                r"\b(?:clear memory|reset memory|memory clear karo|memory reset karo)\b",
                r"\b(?:sab bhool ja|sab kuch delete karo|sab data hata do)\b",
                r"\b(?:memory wipe|wipe memory|clean memory|fresh start karo)\b",
                r"\b(?:mujhe bhool ja|mujhe bhool jao|mera data delete karo)\b"
            ],
            "teach": [
                r"\b(?:hamara|hamari|humare|our)\s+(?:company|team|business|startup|organization|organisation|firm|brand|office)\b",
                r"\b(?:workflow|process|tarika|method|system|procedure|policy|rules|guidelines|steps|approach)\b",
                r"\b(?:ye yaad rakh|yeh yaad rakhna|remember this|note this|save this|store this)\b",
                r"\b(?:isay note kar|isey yaad rakhna|dhyan se yaad rakhna|isko save karo)\b",
                r"\b(?:seekh|seekh lo|learn this|jaan lo|know this|samajh lo|samajh lena)\b",
                r"\b(?:tumhe batata hoon|tumhe bata raha hoon|main tumhe seekhata hoon)\b",
                r"\b(?:ye important hai|yeh important hai|ye zaroori hai|yeh zaroori hai)\b"
            ],
            "help": [
                r"\b(?:help|help karo|help chahiye|madad chahiye|madad karo)\b",
                r"\b(?:assist|support|guide|guide karo|mujhe guide karo)\b",
                r"\b(?:kya kar sakti ho|tum kya kar sakti ho|tum kya kar sakte ho)\b",
                r"\b(?:features|commands|options|menu|capabilities|kya kya kar sakti ho)\b",
                r"\b(?:how to use|kaise use karu|kaise use karu tumhe|kaise kaam karta hai)\b",
                r"\b(?:guide karo|tutorial|mujhe batao kaise|samjhao mujhe)\b",
                r"\b(?:mujhe help chahiye|koi help karo|please help|plz help)\b"
            ],
            "status": [
                r"\b(?:status|memory status|statistics|stats|summary|overview)\b",
                r"\b(?:kitna yaad hai|kitni memory hai|memory kitni hai|kitna data save hai)\b",
                r"\b(?:kitni cheezein yaad hain|kitni baatein yaad hain|total memories)\b",
                r"\b(?:memory report|report de|meri info dikha|meri details dikha)\b",
                r"\b(?:kya kya save hai|kya kya stored hai|stored data|saved data)\b"
            ],
            "goodbye": [
                r"\b(?:bye|goodbye|bye bye|good bye|bbye|byee)\b",
                r"\b(?:alvida|allah hafiz|khuda hafiz|allah hafiz bhai)\b",
                r"\b(?:see you|see ya|see you later|catch you later|talk later)\b",
                r"\b(?:take care|apna khayal rakhna|apna khayal rakhein)\b",
                r"\b(?:phir milenge|milte hain|phir baat karte hain|bad mein baat karte hain)\b",
                r"\b(?:chalta hoon|chalta hun|chalti hoon|ab jaata hoon|ab jaati hoon)\b",
                r"\b(?:band karo|quit|exit|close|shutdown|close karo|band)\b",
                r"\b(?:ab sone ja raha|ab so raha|goodnight|raat ko milte hain)\b"
            ],
            "thanks": [
                r"\b(?:thanks|thank you|thx|ty|thank u|thankyou)\b",
                r"\b(?:shukriya|bohat shukriya|shukriya yaar|shukriya bhai)\b",
                r"\b(?:dhanyawad|bahut dhanyawad|bahut bahut dhanyawad)\b",
                r"\b(?:meherbani|teri meherbani|aapki meherbani)\b",
                r"\b(?:jazakallah|jazakallah khair|allah apko jazae khair de)\b",
                r"\b(?:appreciate it|i appreciate|really appreciate|appreciate your help)\b",
                r"\b(?:helpful tha|bahut helpful|acha laga|maza aaya|bohat acha)\b"
            ],
            "personal_info": [
                r"\b(?:mera|meri|mere|my)\s+(?:age|umar|birthday|janamdin|date of birth|dob)\b",
                r"\b(?:mera|meri|mere|my)\s+(?:phone|mobile|number|contact|whatsapp)\b",
                r"\b(?:mera|meri|mere|my)\s+(?:email|gmail|address|pata|location|city|shehar)\b",
                r"\b(?:mera|meri|mere|my)\s+(?:job|kaam|profession|career|designation|post)\b",
                r"\b(?:mera|meri|mere|my)\s+(?:workplace|school|college|university|office|company)\b",
                r"\b(?:mera|meri|mere|my)\s+(?:hobby|hobbies|interest|passion|favourite|favorite)\b",
                r"\b(?:main|mai|i)\s+(?:work at|work in|live in|study in|am from|belong to)\b",
                r"(?:mujhe|mujhay)\s+\w+\s+pasand",
                r"\b(?:mujhe acha lagta|i like|i love|i enjoy|mera shauq)\b",
                r"\b(?:main rehta hoon|main rehti hoon|i live|i stay|mera ghar)\b",
                r"\b(?:meri family|mera family|mere ghar mein|mere ghar me|mera bhai|meri behen)\b"
            ],
            "productivity_help": [
                r"\b(?:deadline|task|tasks|kaam|kaam hai|kya kaam|bohot kaam)\b",
                r"\b(?:work|project|projects|manage|organize|organise|management)\b",
                r"\b(?:schedule|plan|planning|priority|priorities|important|urgent)\b",
                r"\b(?:time|time management|routine|daily routine|weekly plan)\b",
                r"\b(?:calendar|meeting|meetings|reminder|reminders|alarm)\b",
                r"\b(?:focus|productivity|productive|efficient|efficiency)\b",
                r"\b(?:to do|todo|to-do|checklist|timetable|time table|list)\b",
                r"\b(?:goal|goals|target|achieve|achievement|complete|finish)\b",
                r"\b(?:busy|bahut busy|bohat busy|kaam ka bojh|kaam nahi ho raha)\b"
            ]
        }

        self.info_patterns = {
            "name": [
                r"\b(?:mera naam|mera name)\s+(?!kia\b|kya\b)([A-Za-z][A-Za-z\'\-]{2,30})\s+(?:hai|he|ha|h)\b",
                r"\b(?:mera naam|mera name)\s+([A-Za-z][A-Za-z\'\-]{2,30}?)(?:\s+(?:hai|he|hoon|hun|hain|tha|thi))?(?=$|[.,!?])",
                r"\b(?:my name is|my name's)\s+([A-Za-z][A-Za-z\'\-]{2,30}?)(?:\s+(?:hai|he|hoon))?(?=$|[.,!?])",
                r"\b(?:call me|you can call me|just call me|myself)\s+([A-Za-z][A-Za-z\'\-]{2,30}?)(?=$|[.,!?\s])",
                r"\b(?:mujhe|log mujhe)\s+([A-Za-z][A-Za-z\'\-]{2,30}?)\s+(?:bulate|kehte|bulao|bulana|kehna)\b"
            ],
            "nickname": [
                r"\b(?:mera nickname(?: hai)?|my nickname(?: is)?|mera short name(?: hai)?)\s+([A-Za-z][A-Za-z\s\.\'-]{1,30}?)(?=$|[.,!?])",
                r"\b(?:friends call me|sab mujhe|ghar wale mujhe)\s+([A-Za-z][A-Za-z\s\.\'-]{1,30}?)(?=$|[.,!?]|\s+(?:kehte|bulate)\b)"
            ],
            "age": [
                r"\b(?:meri age(?: hai)?|meri umar(?: hai)?|my age(?: is)?|age(?: is)?|umar(?: hai)?)\s+(\d{1,3})\b",
                r"\b(?:i am|i'm|main|mai)\s+(\d{1,3})\s*(?:years?\s*old|yrs?\s*old|saal(?: ka| ki)?|year old)\b",
            ],
            "company": [
                r"\b(?:meri company(?: ka naam)?|my company(?: name)?|company ka naam|company name)\s*(?:hai|is)?\s*([A-Za-z0-9][A-Za-z0-9&.,'()\-\/\s]{1,60}?)(?=$|[.,!?])",
                r"\b(?:i work at|i work in|i'm working at|i am working at|working at|working in)\s+([A-Za-z0-9][A-Za-z0-9&.,'()\-\/\s]{1,60}?)(?=$|[.,!?])",
                r"\b(?:main|mai)\s+([A-Za-z0-9][A-Za-z0-9&.,'()\-\/\s]{1,60}?)\s+(?:mein|me)\s+(?:kaam karta hoon|kaam karti hoon|work karta hoon|work karti hoon|job karta hoon|job karti hoon)\b"
            ],
            "profession": [
                r"\b(?:i am a|i'm a|i am an|i'm an|main ek)\s+([A-Za-z][A-Za-z\s\-\/&]{1,40}?)(?=$|[.,!?])",
                r"\b(?:my role(?: is)?|mera role(?: hai)?|mera profession(?: hai)?|my profession(?: is)?)\s+([A-Za-z][A-Za-z\s\-\/&]{1,40}?)(?=$|[.,!?])",
                r"\b(?:i work as|main kaam karta hoon as|main kaam karti hoon as)\s+([A-Za-z][A-Za-z\s\-\/&]{1,40}?)(?=$|[.,!?])"
            ],
            "email": [
                r"\b(?:mera email|meri email|my email|email id|mail id|email address|contact email|gmail)\s*(?:hai|is)?\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})\b",
                r"\b(?:reach me at|mail me at|contact me at)\s+([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})\b",
                r"\b([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})\b"
            ],
            "phone": [
                r"\b(?:mera phone(?: number)?|mera mobile(?: number)?|mera contact(?: number)?|my phone(?: number)?|my mobile(?: number)?|my number|mobile number|contact number|whatsapp number)\s*(?:hai|is)?\s*(\+?\d[\d\s\-\(\)]{7,17}\d)\b",
                r"\b(?:reach me on|call me on|text me on)\s*(\+?\d[\d\s\-\(\)]{7,17}\d)\b",
                r"\b(\+?\d[\d\s\-\(\)]{7,17}\d)\b"
            ],
            "city": [
                r"\b(?:main|mai|i)\s+(?:live in|stay in|am from|belong to)\s+([A-Za-z][A-Za-z\s\-]{1,40}?)(?=$|[.,!?])",
                r"\b(?:main|mai)\s+([A-Za-z][A-Za-z\s\-]{1,40}?)\s+(?:mein|me)\s+(?:rehta hoon|rehti hoon)\b",
                r"\b(?:meri city|mera city|my city|mera shehar|meri city ka naam)\s*(?:hai|is)?\s*([A-Za-z][A-Za-z\s\-]{1,40}?)(?=$|[.,!?])"
            ],
            "country": [
                r"\b(?:my country(?: is)?|mera country(?: hai)?|mera mulk(?: hai)?)\s+([A-Za-z][A-Za-z\s\-]{1,40}?)(?=$|[.,!?])",
                r"\b(?:i am from|main hoon from|mai hoon from)\s+([A-Za-z][A-Za-z\s\-]{1,40}?)(?=$|[.,!?])"
            ],
            "address": [
                r"\b(?:mera address|my address|mera pata|mera ghar ka pata)\s*(?:hai|is)?\s+(.+?)(?=$|[.!?])",
                r"\b(?:i live at|main rehta hoon at|main rehti hoon at)\s+(.+?)(?=$|[.!?])"
            ],
            "education": [
                r"\b(?:i study at|i study in|i am studying at|i'm studying at)\s+([A-Za-z0-9][A-Za-z0-9&.,'()\-\/\s]{1,60}?)(?=$|[.,!?])",
                r"\b(?:main|mai)\s+([A-Za-z0-9][A-Za-z0-9&.,'()\-\/\s]{1,60}?)\s+(?:mein|me)\s+(?:padhta hoon|padhti hoon|study karta hoon|study karti hoon)\b",
                r"\b(?:my school|my college|my university|mera school|mera college|meri university)\s*(?:hai|is)?\s*([A-Za-z0-9][A-Za-z0-9&.,'()\-\/\s]{1,60}?)(?=$|[.,!?])"
            ],
            "birthday": [
                r"\b(?:mera birthday|my birthday|mera janamdin|mera birth date|date of birth|dob)\s*(?:hai|is|on)?\s*([A-Za-z0-9,\/\-\s]{3,30}?)(?=$|[.,!?])",
                r"\b(?:i was born on|main paida hua tha|main paida hui thi)\s+([A-Za-z0-9,\/\-\s]{3,30}?)(?=$|[.,!?])"
            ],
            "preference": [
                r"\b(?:mujhe|mujhay)\s+(.+?)\s+(?:pasand hai|pasand he|pasand)\b",
                r"\b(?:i like|i love|i prefer|i enjoy|i am into|i'm into)\s+(.+?)(?=$|[.,!?]|\s+(?:aur|and)\b)",
                r"\b(?:mera favourite|mera favorite|meri favourite cheez|my favourite|my favorite|meri pasand)\s+(.+?)(?:\s+(?:hai|he|is)\b|$|[.,!?])",
                r"\b(?:mera shauq|meri hobby|my hobby|my hobbies|my interest|my interests)\s+(.+?)(?=$|[.,!?])"
            ],
            "dislike": [
                r"\b(?:mujhe|mujhay)\s+(.+?)\s+(?:pasand nahi|acha nahi lagta|achha nahi lagta|accha nahi lagta)\b",
                r"\b(?:i don't like|i do not like|i hate|i dislike)\s+(.+?)(?=$|[.,!?])"
            ],
            "hobby": [
                r"\b(?:mera hobby|meri hobby|my hobby|my hobbies|mera shauq|meri aadat)\s*(?:hai|is)?\s+(.+?)(?=$|[.,!?])",
                r"\b(?:i like to|i love to|mujhe .* karna pasand hai)\s+(.+?)(?=$|[.,!?])"
            ],
            "language": [
                r"\b(?:i speak|main bolta hoon|main bolti hoon|mujhe aati hai|my language is|meri language hai)\s+([A-Za-z,\s]+?)(?=$|[.,!?])",
                r"\b(?:mujhe|i know)\s+([A-Za-z,\s]+?)\s+(?:aati hai|languages?|zabaan)\b"
            ],
            "family": [
                r"\b(?:meri family|my family|mere ghar mein|mere ghar me)\s+(.+?)(?=$|[.!?])",
                r"\b(?:mera bhai|meri behen|mere walid|meri walida|my brother|my sister|my father|my mother)\s+(.+?)(?=$|[.!?])"
            ]
        }

        self.stop_words = {
            "mera", "meri", "mere", "hai", "hain", "ka", "ki", "ke",
            "ko", "se", "mein", "par", "ye", "wo", "kya", "kaise",
            "main", "hoon", "ho", "tha", "thi", "the", "hum", "tum",
            "aap", "is", "us", "ek", "do", "teen", "aur", "ya",
            "nahi", "mat", "na", "bhi", "to", "hi", "ne", "pe",
            "the", "a", "an", "is", "are", "was", "were",
            "have", "has", "had", "do", "does", "did",
            "i", "you", "he", "she", "it", "we", "they",
            "my", "your", "his", "her", "its", "our", "their",
            "this", "that", "these", "those", "of", "in", "on",
            "at", "to", "for", "with", "by", "from", "about",
            "mujhe", "batao", "bata", "naam", "kuch", "wala",
            "wali", "wale", "ab", "jab", "tab", "kab", "mai"
        }

        self._translation_cache = {}
        self._installed_lang_pairs = set()

        print("[NLP] Upgraded NLP Engine initialized!")

    def is_hinglish(self, text):
        text_lower = text.lower()
        words = set(text_lower.split())

       
        non_roman_count = sum(
            1 for c in text if not c.isascii()
        )
        if non_roman_count >= 3:
            return False

       
        if words & self.hinglish_strong_markers:
            return True

        if len(words & self.hinglish_support_markers) >= 2:
            return True


        if words & self.roman_urdu_markers:
            return True

        all_hinglish = (
            self.hinglish_strong_markers |
            self.hinglish_support_markers |
            self.roman_urdu_markers
        )
        hinglish_count = len(words & all_hinglish)
        total = len(words)

        if total > 0 and hinglish_count / total >= 0.20:
            return True

        return False
    def detect_language(self, text):
        non_roman = sum(1 for c in text if not c.isascii())

        if non_roman >= 3:
            text_chars = set(text)

            # Arabic specific chars check
            arabic_specific = text_chars & self.arabic_only_chars
            # Urdu specific chars check
            urdu_specific = text_chars & self.urdu_only_chars

            if arabic_specific and not urdu_specific:
                return "ar"  

            if urdu_specific:
                return "ur"  

            try:
                detected = lang_detect(text)
 
                if detected in ("ar", "ur", "fa"):
                    return detected
                return detected
            except LangDetectException:
                return "ur" 

        if self.is_hinglish(text):
            return "hinglish"

        try:
            if len(text.strip()) < 8:
                return "en"

            detected = lang_detect(text)

            if detected == "hi":
                roman_count = sum(
                    1 for c in text if c.isascii() and c.isalpha()
                )
                total_alpha = sum(1 for c in text if c.isalpha())
                if total_alpha > 0 and roman_count / total_alpha > 0.5:
                    return "hinglish"

            return detected

        except LangDetectException:
            return "en"


    def _is_valid_translation(self, original, translated):
        if not translated:
            return False

        # Length check — translated 5x se zyada nahi hona chahiye
        if len(translated) > len(original) * 5:
            return False

        # Repeated pattern check
        # Agar first 8 chars 4 baar repeat ho raha hai → garbage
        if len(translated) > 32:
            prefix = translated[:8]
            if translated.count(prefix) > 4:
                return False

        # Same as original check (translation nahi hui)
        if translated.strip().lower() == original.strip().lower():
            return False

        return True

    def _ensure_language_installed(self, from_code, to_code="en"):
        pair = f"{from_code}-{to_code}"
        if pair in self._installed_lang_pairs:
            return True
        try:
            argostranslate.package.update_package_index()
            available = argostranslate.package.get_available_packages()
            pkg = next(
                (p for p in available
                 if p.from_code == from_code
                 and p.to_code == to_code),
                None
            )
            if pkg:
                argostranslate.package.install_from_path(pkg.download())
                self._installed_lang_pairs.add(pair)
                print(f"[NLP] Language pack {pair} installed!")
                return True
            print(f"[NLP] Pack {pair} not found!")
            return False
        except Exception as e:
            print(f"[NLP] Install error: {e}")
            return False

    def translate_to_english(self, text, source_lang):
        cache_key = f"{source_lang}:{text}"
        if cache_key in self._translation_cache:
            return self._translation_cache[cache_key]

        try:
            installed = self._ensure_language_installed(
                source_lang, "en"
            )
            if not installed:
                return None  

            result = argostranslate.translate.translate(
                text, source_lang, "en"
            )
            if self._is_valid_translation(text, result):
                self._translation_cache[cache_key] = result
                return result
            else:
                print(
                    f"[NLP] Invalid translation detected "
                    f"for lang: {source_lang}"
                )
                return None  # Garbage hai → None return karo

        except Exception as e:
            print(f"[NLP] Translation error: {e}")
            return None
    def fuzzy_emotion_match(self, text, threshold=75):
        words = text.lower().split()
        emotion_scores = {}
        for emotion, keywords in self.emotion_keywords.items():
            score = 0
            for word in words:
                if len(word) < 3:
                    continue
                match = process.extractOne(
                    word, keywords, scorer=fuzz.ratio
                )
                if match and match[1] >= threshold:
                    score += 1
            if score > 0:
                emotion_scores[emotion] = min(score / 3.0, 1.0)
        return emotion_scores

    def detect_emotion(self, text, translated_text=None):
        text_lower = text.lower()
        emotion_score = {}

        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                emotion_score[emotion] = min(score / 3.0, 1.0)

        if translated_text:
            trans_lower = translated_text.lower()
            for emotion, keywords in self.emotion_keywords.items():
                score = sum(1 for kw in keywords if kw in trans_lower)
                if score > 0:
                    existing = emotion_score.get(emotion, 0)
                    emotion_score[emotion] = max(
                        existing, min(score / 3.0, 1.0)
                    )

        fuzzy_scores = self.fuzzy_emotion_match(text)
        for emotion, score in fuzzy_scores.items():
            if emotion not in emotion_score:
                emotion_score[emotion] = score * 0.8

        sentiment_text = translated_text if translated_text else text
        try:
            polarity = TextBlob(sentiment_text).sentiment.polarity
            if polarity > 0.3:
                emotion_score["happy"] = (
                    emotion_score.get("happy", 0) + polarity
                )
            elif polarity < -0.3:
                emotion_score["sad"] = (
                    emotion_score.get("sad", 0) + abs(polarity)
                )
        except Exception:
            pass

        if emotion_score:
            best = max(emotion_score, key=emotion_score.get)
            score = round(min(emotion_score[best], 1.0), 2)
            return best, score
        return "neutral", 0.0

    def analyze(self, text):
        result = {
            "emotion": "neutral",
            "emotion_score": 0.0,
            "intent": "general",
            "keywords": [],
            "extracted_info": {},
            "original_text": text,
            "detected_language": "en",
            "translated_text": None
        }

        detected_lang = self.detect_language(text)
        result["detected_language"] = detected_lang

        translated_text = None
        if detected_lang not in ("en", "hinglish"):
            translated_text = self.translate_to_english(
                text, detected_lang
            )
            result["translated_text"] = translated_text

        emotion, score = self.detect_emotion(text, translated_text)
        result["emotion"] = emotion
        result["emotion_score"] = score

        intent = self.detect_intent(text)
        if intent == "general" and translated_text:
            intent = self.detect_intent(translated_text)
        result["intent"] = intent

        keywords = self.extract_keywords(text)
        if translated_text:
            trans_keywords = self.extract_keywords(translated_text)
            merged = keywords + [
                k for k in trans_keywords if k not in keywords
            ]
            result["keywords"] = merged
        else:
            result["keywords"] = keywords

        extracted = self.extract_information(text)
        if not extracted and translated_text:
            extracted = self.extract_information(translated_text)
        result["extracted_info"] = extracted

        return result

    def detect_intent(self, text):
        text_lower = text.lower()
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return intent
        return "general"

    def extract_keywords(self, text):
        words = re.findall(r"\b\w+\b", text.lower())
        keywords = [
            w for w in words
            if w not in self.stop_words and len(w) > 2
        ]
        return list(dict.fromkeys(keywords))

    def extract_information(self, text):
        extracted = {}
        text_lower = text.lower()
        is_question = text.strip().endswith("?") or \
                      any(text_lower.startswith(w) for w in
                          ["kya", "what", "who", "kaun"])
        for info_type, patterns in self.info_patterns.items():
            if info_type == "name" and is_question:
                continue
            for pattern in patterns:
                match = re.search(pattern, text_lower, re.IGNORECASE)
                if match:
                    value = match.group(1).strip()
                    if info_type == "name":
                        value = value.capitalize()
                    extracted[info_type] = value
                    break
        return extracted

    def classify_text(self, text):
        text_lower = text.lower().strip()
        question_words = [
            "kya", "kaise", "kab", "kahan", "kaun", "kitna",
            "what", "how", "when", "where", "who", "which", "why"
        ]
        if text.endswith("?") or any(
            text_lower.startswith(w) for w in question_words
        ):
            return "question"
        command_words = [
            "batao", "dikhao", "karo", "save", "delete", "bhool",
            "show", "tell", "do", "find", "search", "help", "hata"
        ]
        if any(w in text_lower for w in command_words):
            return "command"
        all_emotion_words = [
            kw for kws in self.emotion_keywords.values() for kw in kws
        ]
        if sum(
            1 for w in text_lower.split() if w in all_emotion_words
        ) >= 2:
            return "emotional"
        return "statement"


# =================== FIXED TESTS ===================
if __name__ == "__main__":
    nlp = LuciaNLP()

    tests = [
        # Hinglish
        ("main bahut stressed hoon", "Hinglish — Basic"),
        ("yaar kya scene hai", "Hinglish — Casual"),
        ("bhai kal milte hain", "Hinglish — Short"),
        ("theek hai bro chal jaate", "Hinglish — Mixed"),
        ("bohot thak gaya hoon yaar", "Hinglish — Emotion"),
        ("kaam nahi ho raha dimag kharab", "Hinglish — Stressed"),
        ("main stresed hoon", "Hinglish — Spelling Mistake"),
        ("inshallah sab theek ho jaye ga", "Roman Urdu"),
        # English
        ("I am very happy today", "English"),
        ("feeling so stressed about work", "English"),  # ← Fix
        # Other
        ("أنا سعيد جداً", "Arabic"),                   # ← Fix
        ("Je suis stressé", "French"),
        ("Estoy muy feliz", "Spanish"),                 # ← Fix
        ("میں بہت خوش ہوں آج", "Urdu Script"),
    ]

    print("\n" + "=" * 55)
    print("   FIXED DETECTION TESTS")
    print("=" * 55)

    for text, label in tests:
        r = nlp.analyze(text)
        lang = r["detected_language"]

        expected_hinglish = "Hinglish" in label or "Roman Urdu" in label
        got_hinglish = lang == "hinglish"
        status = "✅" if (expected_hinglish == got_hinglish) else "❌"

        print(f"\n{status} [{label}]")
        print(f"   Input      : {text}")
        print(f"   Language   : {lang}")
        print(f"   Emotion    : {r['emotion']} ({r['emotion_score']})")
        print(f"   Translated : {r['translated_text']}")