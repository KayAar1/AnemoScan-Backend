# ============================================================
#  AnemiaCare RAG Knowledge Base
#  All chunks are used to build the vector store at startup
# ============================================================

ANEMIA_CHUNKS = [

    # ── TYPES ──────────────────────────────────────────────
    "Iron-deficiency anemia is the most common type worldwide. It occurs when the body "
    "does not have enough iron to produce hemoglobin. Causes include poor diet, blood loss "
    "(heavy periods, ulcers), or poor iron absorption. It is especially common in women "
    "and children in Pakistan.",

    "Vitamin B12 deficiency anemia happens when the body lacks enough B12 to make healthy "
    "red blood cells. It is common in vegetarians, older adults, and people with digestive "
    "disorders like Crohn's disease. Symptoms include fatigue, numbness in hands and feet, "
    "memory problems, and a swollen tongue.",

    "Folate (Vitamin B9) deficiency anemia is similar to B12 anemia. It is common during "
    "pregnancy. Folic acid supplements are recommended for all pregnant women to prevent "
    "neural tube defects in the baby and to treat this type of anemia.",

    "Thalassemia is an inherited blood disorder common in Pakistan, especially in Sindh and "
    "Punjab. In thalassemia, the body makes abnormal hemoglobin. People with thalassemia "
    "trait (minor) are often asymptomatic but can pass it to children. Thalassemia major "
    "requires regular blood transfusions.",

    "Sickle cell anemia is a genetic disorder where red blood cells become crescent-shaped "
    "and break down quickly. It causes episodes of pain called 'crises', infections, and "
    "organ damage. It is managed with medications, hydration, and sometimes bone marrow "
    "transplants.",

    "Aplastic anemia is a rare but serious condition where the bone marrow stops making "
    "enough blood cells. It can be caused by autoimmune diseases, certain medications, "
    "radiation, or infections. Treatment includes blood transfusions and bone marrow "
    "transplants.",

    "Hemolytic anemia occurs when red blood cells are destroyed faster than they can be "
    "made. Causes include autoimmune conditions, infections, certain medications, and "
    "inherited conditions. Symptoms include jaundice, dark urine, and enlarged spleen.",

    # ── SYMPTOMS ───────────────────────────────────────────
    "Common symptoms of anemia include: persistent fatigue and weakness, pale or yellowish "
    "skin, shortness of breath during normal activity, dizziness or lightheadedness, "
    "headaches, cold hands and feet, chest pain, and fast or irregular heartbeat.",

    "In children, anemia symptoms include: poor concentration and weak performance in "
    "school, slow growth, irritability, loss of appetite, and frequent infections. "
    "Anemia in children under 5 is a serious concern and common in Pakistan.",

    "Severe anemia warning signs that need immediate medical attention: hemoglobin below "
    "7 g/dL, chest pain or difficulty breathing at rest, fainting, rapid heart rate over "
    "100 bpm at rest, swollen legs, or inability to perform daily activities.",

    "Pica is an unusual symptom of iron-deficiency anemia where the person craves non-food "
    "items like ice, dirt, clay, or chalk. If you or your child craves these things, it may "
    "indicate severe iron deficiency and you should see a doctor immediately.",

    # ── DIAGNOSIS ──────────────────────────────────────────
    "Anemia is diagnosed through a Complete Blood Count (CBC) blood test. Key values: "
    "Normal hemoglobin for adult women is 12–16 g/dL; for men 13.5–17.5 g/dL; for "
    "children 11–14 g/dL. Hemoglobin below these values indicates anemia.",

    "Other blood tests for anemia include: serum ferritin (measures iron stores), serum "
    "iron, TIBC (total iron binding capacity), vitamin B12 level, folate level, reticulocyte "
    "count, and peripheral blood smear. Your doctor will recommend the right tests.",

    # ── DIET & NUTRITION ───────────────────────────────────
    "Best iron-rich foods for anemia patients: red meat (beef, lamb, liver), chicken and "
    "fish, spinach (palak), lentils (daal masoor, daal chana), kidney beans (rajma), "
    "chickpeas (chana), fortified cereals, pumpkin seeds (kaddu ke beej), and tofu.",

    "Iron-rich Pakistani foods that are easily available and affordable: daal (lentils of "
    "all types), saag (mustard greens and spinach), aloo palak, chana curry, beef/mutton "
    "karahi, liver (kaleji), dates (khajoor), raisins (kishmish), and pomegranate (anar).",

    "Vitamin C dramatically increases iron absorption. Always pair iron-rich foods with a "
    "source of Vitamin C: lemon juice squeezed on daal or saag, orange juice with meals, "
    "tomatoes in curries, amla (Indian gooseberry), guava (amrood), and kiwi.",

    "Foods that BLOCK iron absorption and should be avoided around meals or iron supplements: "
    "tea (chai), coffee, milk and dairy products, calcium supplements, antacids, foods high "
    "in phytates like unsoaked whole grains. Wait at least 1 hour after eating these before "
    "taking iron supplements.",

    "Vitamin B12-rich foods for B12 deficiency anemia: meat and poultry, fish and seafood, "
    "eggs, milk and dairy products (dahi, paneer, milk). Vegetarians are at high risk of "
    "B12 deficiency and may need supplements. Fortified foods and B12 injections are used "
    "when diet alone is not enough.",

    "Folate-rich foods for folate deficiency anemia: dark green vegetables (spinach, "
    "methi/fenugreek, broccoli), lentils, chickpeas, kidney beans, liver, eggs, "
    "fortified cereals, oranges, and bananas. Cooking destroys folate, so eat some "
    "vegetables raw when possible.",

    "Foods that help build blood and are recommended in traditional Pakistani medicine: "
    "pomegranate juice (anar ka juice), beetroot, dates with milk, black sesame seeds "
    "(til), molasses (gurr/jaggery) mixed with milk, carrot juice, and almond milk. "
    "These are good supplements to a balanced diet.",

    "Hydration is important for anemia patients. Drink 8–10 glasses of water daily. "
    "Avoid excessive tea and coffee as they block iron absorption. Fresh fruit juices "
    "especially pomegranate, orange, and carrot are beneficial.",

    # ── MEDICATIONS ────────────────────────────────────────
    "Common iron supplements available in Pakistan: Ferrous sulfate (most common, "
    "cheapest), Ferrous gluconate (gentler on stomach), Ferrous fumarate, and Feosol. "
    "Iron syrups for children include Fer-In-Sol and locally available syrups. "
    "Always take as prescribed by your doctor.",

    "How to take iron supplements correctly: Take on an empty stomach or 1 hour before "
    "meals for best absorption. Take with a glass of orange juice or lemon water (Vitamin C "
    "helps absorption). Avoid taking with tea, milk, or antacids. If stomach upset occurs, "
    "take with a small meal.",

    "Common side effects of iron supplements: constipation, dark/black stools (normal and "
    "harmless), nausea, stomach cramps, and sometimes diarrhea. To reduce constipation: "
    "drink more water, eat fiber-rich foods, and if needed ask your doctor to switch to "
    "a gentler form like ferrous gluconate.",

    "Folic acid supplements (5mg daily) are prescribed for folate deficiency anemia and "
    "are essential during pregnancy. Vitamin B12 injections are given monthly for B12 "
    "deficiency anemia, especially when oral absorption is poor.",

    "Duration of iron supplement treatment: Most patients need to take iron for 3–6 months "
    "even after hemoglobin returns to normal — this is to replenish iron stores. Do not "
    "stop taking iron supplements early even if you feel better. Follow your doctor's "
    "advice on when to stop.",

    "Erythropoietin injections are prescribed for anemia caused by chronic kidney disease. "
    "Blood transfusions are used in severe anemia (Hb below 7) or thalassemia major. "
    "These are hospital procedures done under medical supervision.",

    # ── PRECAUTIONS & LIFESTYLE ────────────────────────────
    "Daily precautions for anemia patients: avoid overexertion and heavy physical activity "
    "until hemoglobin improves, rest when tired, avoid exposure to extreme cold, do light "
    "exercise like short walks when energy allows, and maintain a regular sleep schedule.",

    "Women with heavy menstrual periods (haiz) should track blood loss and discuss with "
    "their gynecologist as heavy periods are the most common cause of iron deficiency "
    "anemia in Pakistani women. Iron supplements may need to be taken continuously.",

    "Pregnant women with anemia: anemia during pregnancy is very dangerous. It increases "
    "risk of premature birth, low birth weight baby, and postpartum hemorrhage. Pregnant "
    "women should take prescribed iron + folic acid supplements and attend all antenatal "
    "checkups. Eat iron-rich foods at every meal.",

    "Cooking in iron pots (cast iron) can slightly increase the iron content of food. "
    "This is an affordable and traditional way to add a small amount of iron to the diet, "
    "especially useful in low-income households.",

    "Worm infections (intestinal parasites) are a common cause of anemia in Pakistan, "
    "especially in children. Deworming with medications like mebendazole or albendazole "
    "every 6 months is recommended for children in endemic areas. Good hand hygiene and "
    "clean water prevent reinfection.",

    "Prevent anemia in children: breastfeed exclusively for 6 months, introduce iron-rich "
    "solid foods at 6 months, give iron drops for premature or low birth weight babies, "
    "ensure the child eats daal, eggs, and meat regularly, and deworm every 6 months.",

    # ── APP SUPPORT ────────────────────────────────────────
    "The AnemiaCare app helps you track your hemoglobin levels over time, set medication "
    "reminders, log your daily diet, and learn about anemia management. Use the tracker "
    "to record your blood test results and share them with your doctor.",

    "To set a medication reminder in the AnemiaCare app: go to the Reminders section, "
    "tap 'Add Reminder', choose your medication (e.g., iron tablet), set the time, and "
    "enable notifications. The app will remind you daily to take your supplements.",

    "The AnemiaCare diet tracker helps you log iron-rich meals. After each meal, tap "
    "'Log Meal' and select what you ate. The app estimates your iron intake for the day "
    "and shows if you are meeting your daily recommended iron intake.",

]
