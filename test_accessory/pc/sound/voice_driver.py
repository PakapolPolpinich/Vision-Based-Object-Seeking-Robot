import speech_recognition as sr

class VoiceCommander:
    def __init__(self, mic_index=None, keywords={}):
        """
        Init Class
        :param mic_index: เลข Index ของไมค์ (ถ้าใส่ None จะใช้ Default Mic ของ Windows/Mac)
        :param keywords: Dictionary จับคู่ { "VALUE": ["คำพูด1", "คำพูด2"] }
        """
        self.mic_index = mic_index
        self.keywords = keywords
        self.recognizer = sr.Recognizer()
        
        # ตั้งค่าความไว (Sensitivity)
        self.recognizer.energy_threshold = 3000 
        self.recognizer.dynamic_energy_threshold = True

    def list_microphones(self):
        """แสดงรายการไมค์ทั้งหมด (เอาไว้เช็คเผื่อ Default Mic ไม่ดัง)"""
        print("\n🎧 --- รายชื่อไมค์ที่พบในคอมพิวเตอร์ ---")
        mics = sr.Microphone.list_microphone_names()
        for index, name in enumerate(mics):
            print(f"Index {index}: {name}")
        print("---------------------------------------\n")

    def listen(self):
        """
        ฟังก์ชันรับเสียง (Blocking Mode)
        รอจนกว่าจะพูดจบประโยค ถึงจะคืนค่า
        """
        try:
            # ใช้ไมค์ตาม Index ที่ระบุ (ถ้า None คือใช้ตัว Default)
            with sr.Microphone(device_index=self.mic_index) as source:
                print("\n🎤 กำลังฟัง... (พูดคำสั่งได้เลย)")
                
                # ปรับลดเสียงรบกวน (เช่น เสียงพัดลมคอม/แอร์)
                self.recognizer.adjust_for_ambient_noise(source, duration=0.6)
                
                try:
                    # รับเสียง (รอจนกว่าเสียงจะเงียบลง)
                    audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=5)
                    print("⏳ กำลังประมวลผล... (ส่งไป Google)")
                    
                    # แปลงเสียงเป็นข้อความ (Google API)
                    text = self.recognizer.recognize_google(audio, language="th-TH")
                    print(f"🗣️  คุณพูดว่า: '{text}'")
                    
                    # ตรวจสอบว่าตรงกับ Keyword ไหนไหม
                    for value, words in self.keywords.items():
                        for word in words:
                            if word in text:
                                return value # ✅ เจอคำสั่ง! คืนค่า Value ทันที
                                
                    print(f"❌ ได้ยินแต่ไม่เข้าใจคำสั่ง ('{text}')")
                    return None

                except sr.WaitTimeoutError:
                    return None
                except sr.UnknownValueError:
                    print("?? ฟังไม่ออก / เสียงเบาไป")
                    return None
                except sr.RequestError:
                    print("⚠️ เชื่อมต่อ Google ไม่ได้ (เช็คเน็ต)")
                    return None

        except OSError:
            print(f"🚫 Error: ไม่พบไมโครโฟน (Index: {self.mic_index})")
            print("👉 ลองรันคำสั่ง list_microphones() เพื่อดูเลขที่ถูกต้อง")
            return None