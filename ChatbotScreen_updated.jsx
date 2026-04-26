import { useState, useRef, useEffect } from 'react';
import {
  View, Text, StyleSheet, TextInput, TouchableOpacity,
  ScrollView, KeyboardAvoidingView, Platform, ActivityIndicator
} from 'react-native';
import { useRouter } from 'expo-router';

// ── IMPORTANT: Replace with your Render.com URL after deploying ──
// Example: 'https://anemiacare-rag-backend.onrender.com'
// For local testing use: 'http://192.168.x.x:5000'  (your PC's local IP)
const BACKEND_URL = 'https://AnemoScan.onrender.com';

const LANG_LABELS = { en: '🇬🇧 EN', ur: '🇵🇰 UR', sd: '🏳️ SD' };

const QUICK_REPLIES = {
  en: [
    'What foods are good for anemia?',
    'What are symptoms of anemia?',
    'How should I take iron supplements?',
    'What precautions should I follow?',
  ],
  ur: [
    'خون کی کمی کے لیے کون سی غذائیں اچھی ہیں؟',
    'خون کی کمی کی علامات کیا ہیں؟',
    'آئرن سپلیمنٹ کیسے لیں؟',
    'کون سی احتیاطی تدابیر اختیار کریں؟',
  ],
  sd: [
    'انيميا لاءِ ڪهڙيون کاڌيون سٺيون آهن؟',
    'انيميا جون علامتون ڇا آهن؟',
    'آئرن سپليمينٽ ڪيئن وٺجي؟',
    'ڪهڙيون احتياطي تدبيرون اختيار ڪجن؟',
  ],
};

const PLACEHOLDERS = {
  en: 'Ask me anything about anemia...',
  ur: 'خون کی کمی کے بارے میں کچھ بھی پوچھیں...',
  sd: 'انيميا بابت ڪجهه به پڇو...',
};

const WELCOME = {
  en: "Hi! 👋 I'm your AnemiaCare assistant — powered by AI + medical knowledge base. Ask me about diet, symptoms, medications, or precautions!",
  ur: "السلام علیکم! 👋 میں آپ کا AnemiaCare اسسٹنٹ ہوں — AI اور طبی معلومات سے لیس۔ خوراک، علامات، ادویات یا احتیاطی تدابیر کے بارے میں پوچھیں!",
  sd: "هيلو! 👋 آئون توهان جو AnemiaCare اسسٽنٽ آهيان — AI ۽ طبي ڄاڻ سان ليس. خوراڪ، علامتن، دوائن يا احتياطن بابت پڇو!",
};

export default function ChatbotScreen() {
  const router = useRouter();
  const scrollRef = useRef(null);
  const [lang, setLang] = useState('en');
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([
    { role: 'assistant', content: WELCOME['en'] }
  ]);

  useEffect(() => {
    setTimeout(() => scrollRef.current?.scrollToEnd({ animated: true }), 100);
  }, [messages]);

  const switchLang = (l) => {
    setLang(l);
    setMessages([{ role: 'assistant', content: WELCOME[l] }]);
  };

  const sendMessage = async (text) => {
    const userText = text || input.trim();
    if (!userText) return;
    setInput('');

    const userMsg = { role: 'user', content: userText };
    const updatedMessages = [...messages, userMsg];
    setMessages(updatedMessages);
    setLoading(true);

    try {
      // Build clean history (exclude welcome messages)
      const welcomeTexts = Object.values(WELCOME);
      const history = updatedMessages
        .filter(m => !welcomeTexts.includes(m.content))
        .slice(0, -1)  // exclude the message we're about to send
        .map(m => ({ role: m.role, content: m.content }));

      const response = await fetch(`${BACKEND_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userText,
          history: history,
          language: lang,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || `Server error ${response.status}`);
      }

      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.reply,
      }]);

    } catch (error) {
      console.log('Chat error:', error.message);
      const errorMessages = {
        en: `❌ ${error.message}. Please check your connection and try again.`,
        ur: `❌ ${error.message}. براہ کرم اپنا انٹرنیٹ چیک کریں اور دوبارہ کوشش کریں۔`,
        sd: `❌ ${error.message}. مهرباني ڪري پنهنجو انٽرنيٽ چيڪ ڪريو.`,
      };
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: errorMessages[lang],
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={Platform.OS === 'ios' ? 90 : 0}
    >
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()}>
          <Text style={styles.backText}>‹ Back</Text>
        </TouchableOpacity>
        <View style={styles.headerCenter}>
          <Text style={styles.headerEmoji}>🩸</Text>
          <View>
            <Text style={styles.headerTitle}>AnemiaCare Bot</Text>
            <Text style={styles.headerStatus}>● AI + RAG Powered</Text>
          </View>
        </View>
        <View style={styles.langRow}>
          {Object.entries(LANG_LABELS).map(([key, label]) => (
            <TouchableOpacity
              key={key}
              style={[styles.langBtn, lang === key && styles.langBtnActive]}
              onPress={() => switchLang(key)}
            >
              <Text style={[styles.langText, lang === key && styles.langTextActive]}>
                {label}
              </Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      <ScrollView
        ref={scrollRef}
        style={styles.messages}
        contentContainerStyle={styles.messagesContent}
        showsVerticalScrollIndicator={false}
      >
        {messages.map((msg, index) => (
          <View
            key={index}
            style={[styles.bubble, msg.role === 'user' ? styles.userBubble : styles.botBubble]}
          >
            {msg.role === 'assistant' && <Text style={styles.botIcon}>🩸</Text>}
            <View style={[
              styles.bubbleInner,
              msg.role === 'user' ? styles.userBubbleInner : styles.botBubbleInner
            ]}>
              <Text style={[
                styles.bubbleText,
                msg.role === 'user' ? styles.userText : styles.botText
              ]}>
                {msg.content}
              </Text>
            </View>
          </View>
        ))}

        {loading && (
          <View style={[styles.bubble, styles.botBubble]}>
            <Text style={styles.botIcon}>🩸</Text>
            <View style={styles.typingBubble}>
              <ActivityIndicator size="small" color="#c0392b" />
              <Text style={styles.typingText}>Searching knowledge base...</Text>
            </View>
          </View>
        )}

        {messages.length <= 1 && !loading && (
          <View style={styles.quickReplies}>
            <Text style={styles.quickRepliesTitle}>Quick Questions:</Text>
            {QUICK_REPLIES[lang].map((q, i) => (
              <TouchableOpacity key={i} style={styles.quickBtn} onPress={() => sendMessage(q)}>
                <Text style={styles.quickBtnText}>{q}</Text>
              </TouchableOpacity>
            ))}
          </View>
        )}
      </ScrollView>

      <View style={styles.inputRow}>
        <TextInput
          style={styles.input}
          value={input}
          onChangeText={setInput}
          placeholder={PLACEHOLDERS[lang]}
          placeholderTextColor="#bbb"
          multiline
          maxLength={500}
          onSubmitEditing={() => sendMessage()}
        />
        <TouchableOpacity
          style={[styles.sendBtn, (!input.trim() || loading) && styles.sendBtnDisabled]}
          onPress={() => sendMessage()}
          disabled={!input.trim() || loading}
        >
          <Text style={styles.sendIcon}>➤</Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff5f5' },
  header: {
    backgroundColor: '#c0392b', paddingTop: 50, paddingBottom: 14,
    paddingHorizontal: 16, flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between',
  },
  backText: { color: '#ffb3b3', fontSize: 18, fontWeight: '600' },
  headerCenter: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  headerEmoji: { fontSize: 28 },
  headerTitle: { color: '#fff', fontWeight: 'bold', fontSize: 15 },
  headerStatus: { color: '#a8e6a3', fontSize: 11, marginTop: 1 },
  langRow: { flexDirection: 'row', gap: 4 },
  langBtn: { paddingHorizontal: 8, paddingVertical: 4, borderRadius: 12, backgroundColor: 'rgba(255,255,255,0.2)' },
  langBtnActive: { backgroundColor: '#fff' },
  langText: { fontSize: 10, color: '#ffb3b3', fontWeight: '700' },
  langTextActive: { color: '#c0392b' },
  messages: { flex: 1 },
  messagesContent: { padding: 16, paddingBottom: 8 },
  bubble: { flexDirection: 'row', marginBottom: 12, alignItems: 'flex-end' },
  userBubble: { justifyContent: 'flex-end' },
  botBubble: { justifyContent: 'flex-start' },
  botIcon: { fontSize: 20, marginRight: 8, marginBottom: 4 },
  bubbleInner: { maxWidth: '78%', borderRadius: 18, padding: 12 },
  userBubbleInner: { backgroundColor: '#c0392b', borderBottomRightRadius: 4 },
  botBubbleInner: { backgroundColor: '#fff', borderBottomLeftRadius: 4, shadowColor: '#000', shadowOpacity: 0.06, shadowRadius: 4, elevation: 2 },
  bubbleText: { fontSize: 14, lineHeight: 20 },
  userText: { color: '#fff' },
  botText: { color: '#333' },
  typingBubble: { backgroundColor: '#fff', borderRadius: 18, borderBottomLeftRadius: 4, padding: 12, flexDirection: 'row', alignItems: 'center', gap: 8, shadowColor: '#000', shadowOpacity: 0.06, shadowRadius: 4, elevation: 2 },
  typingText: { color: '#888', fontSize: 13 },
  quickReplies: { marginTop: 8 },
  quickRepliesTitle: { fontSize: 12, color: '#999', marginBottom: 8, fontWeight: '600' },
  quickBtn: { backgroundColor: '#fff', borderRadius: 20, paddingHorizontal: 14, paddingVertical: 10, marginBottom: 8, borderWidth: 1.5, borderColor: '#e57373' },
  quickBtnText: { color: '#c0392b', fontSize: 13, fontWeight: '600' },
  inputRow: { flexDirection: 'row', padding: 12, backgroundColor: '#fff', borderTopWidth: 1, borderTopColor: '#f0e0e0', alignItems: 'flex-end', gap: 10 },
  input: { flex: 1, backgroundColor: '#fff5f5', borderRadius: 22, paddingHorizontal: 16, paddingVertical: 10, fontSize: 14, borderWidth: 1.5, borderColor: '#e0c0c0', maxHeight: 100, color: '#333' },
  sendBtn: { width: 44, height: 44, borderRadius: 22, backgroundColor: '#c0392b', justifyContent: 'center', alignItems: 'center' },
  sendBtnDisabled: { backgroundColor: '#e0a0a0' },
  sendIcon: { color: '#fff', fontSize: 16, fontWeight: 'bold' },
});
