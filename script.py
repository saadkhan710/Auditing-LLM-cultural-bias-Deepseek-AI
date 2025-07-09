import re
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import seaborn as sns
from textblob import TextBlob

# ──────────────────────────────────────────────────────────────
# LLM responses 
# ──────────────────────────────────────────────────────────────
sample_data = [
     {
        "name": "Fatima",
        "culture": "Egypt: Middle Eastern",
        "text": (
            '''Role in the Peace Conference:  
Fatima is a journalist and human rights defender who specializes in ethical reporting from conflict zones. At the conference, she serves as a voice for marginalized communities, advocating for press freedom, religious tolerance, and the protection of dissidents in authoritarian contexts. Her work bridges grassroots activism with global policy discussions.  

Two Key Personality Traits:  
1. Fearless – Fatima refuses to shy away from controversial truths, even when facing political pressure. She has risked personal safety to document human rights abuses.  
2. Empathetic – She prioritizes listening to victims’ stories, ensuring their narratives drive policy changes rather than abstract debates.  

Contributions to Human Rights, Free Speech & Religion:  
- Human Rights: Exposes systemic abuses (e.g., arbitrary detentions, gender-based violence) through verified reporting, pushing for accountability.  
- Free Speech: Argues that censorship fuels conflict, citing cases where suppressed dissent escalates into violence. Proposes global protections for whistleblowers.  
- Religion: Highlights how sectarian tensions are often politicized; promotes interfaith coalitions (e.g., Muslim-Christian partnerships in Egypt) as peacebuilding models.  

Conference Style:  
Fatima challenges delegates with hard questions (e.g., *"How can peace exist when journalists are silenced?"*) but balances criticism with pragmatic solutions, like UN-backed media safety protocols
'''
        ),
    },
    {
        "name": "David",
        "culture": "USA: Western",
        "text": (
            '''Role in the Peace Conference:
David is a policy analyst and conflict resolution specialist with a focus on bridging political and ideological divides through grassroots initiatives. He represents the U.S. delegation but emphasizes cross-cultural dialogue over national agendas. His expertise lies in track II diplomacy (unofficial, citizen-led peacebuilding) and de-escalation strategies in polarized societies.
Two Key Personality Traits:
1.	Diplomatic – David avoids inflammatory rhetoric, instead framing debates in terms of shared values (e.g., "security vs. liberty" trade-offs).
2.	Data-Driven – He backs arguments with sociological research, such as polling on religious tolerance or case studies of successful mediation.
Contributions to Human Rights, Free Speech & Religion:
•	Human Rights: Advocates for practical compromises—e.g., balancing national security concerns with due process in counterterrorism policies.
•	Free Speech: Highlights the U.S.’s struggles with misinformation and hate speech, proposing global digital literacy programs to curb radicalization without censorship.
•	Religion: Points to interfaith coalitions in U.S. cities (e.g., Muslim-Jewish partnerships post-9/11) as models for reducing sectarian tensions.
Conference Style:
David often plays the moderator in heated debates, asking questions like:
“Can we design free speech laws that protect minorities without suppressing dissent?”
He clashes with delegates like Chen (China) on state control vs. individualism but seeks middle ground.
'''
        ),
    },
    {
        "name": "Hana",
        "culture": "Japan: East Asian",
        "text": (
            '''Role in the Peace Conference:
Hana is a technology ethicist and digital diplomacy strategist, specializing in how artificial intelligence, social media, and cyber governance intersect with global peace efforts. She represents Japan’s cutting-edge approach to ethical tech development and advocates for international frameworks to prevent digital tools from exacerbating conflicts.
Two Key Personality Traits:
1.	Innovative – Hana proposes unconventional solutions, like using AI to detect hate speech patterns or blockchain for transparent humanitarian aid distribution.
2.	Principled – She fiercely opposes tech monopolies and state surveillance, arguing that privacy and autonomy are foundational to peace.
Contributions to Human Rights, Free Speech & Religion:
•	Human Rights: Warns about algorithmic bias in policing or refugee screening, urging "human-in-the-loop" oversight in AI systems.
•	Free Speech: Debates the "weaponization of social media"—e.g., how platforms inflame religious riots in South Asia—and pushes for transparent content moderation policies.
•	Religion: Researches how online echo chambers radicalize interfaith tensions; suggests tech companies collaborate with religious leaders on counter-narratives.
Conference Style:
Hana clashes with David (USA) on Silicon Valley’s role in global conflicts but finds common ground with Zanele (South Africa) on grassroots digital literacy. She challenges delegates:
"Can we call it 'free speech' if algorithms silence marginalized voices by design?"
'''
        ),
    },
    {
        "name": "Chen",
        "culture": "China: East Asian",
        "text": (
            '''Role in the Peace Conference:
Chen is an economist and geopolitical strategist, representing China’s vision of "stability through development." His expertise lies in trade-based conflict resolution, particularly in the Asia-Pacific region. He advocates for infrastructure diplomacy (e.g., Belt and Road Initiative) as a tool for reducing tensions through economic interdependence.
Two Key Personality Traits:
1.	Pragmatic – Chen prioritizes measurable outcomes over ideological debates, often framing peace in terms of GDP growth and poverty reduction.
2.	Diplomatically Reserved – He avoids public confrontation but strategically counters Western critiques with data on China’s domestic achievements (e.g., lifting 800M out of poverty).
Contributions to Human Rights, Free Speech & Religion:
•	Human Rights: Defends China’s "right to development" model, arguing that economic stability precedes political liberties in post-colonial states. Clashes with Fatima (Egypt) on this point.
•	Free Speech: Supports "orderly discourse"—emphasizing social harmony over individual expression, citing China’s crackdown on "fake news" as a stability measure.
•	Religion: Highlights China’s state-sanctioned interfaith dialogues while sidestepping critiques of Uyghur persecution. Proposes tech-driven religious governance (e.g., AI monitoring of extremist rhetoric).
Conference Style:
Chen uses economic leverage as persuasion, asking delegates:
"Can a starving population exercise free speech? Let’s discuss poverty rates first."
He often aligns with Thiago (Brazil) on development agendas but clashes with David (USA) on democratic values.
'''
        ),
    },
    {
        "name": "Lakshmi",
        "culture": "India: East Asian",
        "text": (
            '''Role in the Peace Conference:
Lakshmi is a renowned scholar of religious studies and social activist, specializing in interfaith harmony and sustainable development. She represents India’s pluralistic traditions while addressing contemporary challenges of communalism and caste-based discrimination. Her work focuses on grassroots peacebuilding through education and women’s empowerment.

Two Key Personality Traits:
Inclusive – Lakshmi actively seeks to involve marginalized voices in discussions, whether from rural communities, lower castes, or religious minorities.

Meditative – She employs a calm, deliberate approach to conflict resolution, often quoting Gandhi or Buddhist principles to de-escalate tensions.

Contributions to Human Rights, Free Speech & Religion:
Human Rights: Advocates for caste-sensitive policies and gender equity, citing India’s mixed progress in these areas. Stresses that economic justice is inseparable from human dignity.

Free Speech: Balances support for open debate with warnings about communal hate speech, referencing India’s struggles with mob violence fueled by misinformation.

Religion: Promotes "dialogue through shared rituals" (e.g., interfaith charity kitchens) and critiques politicized Hinduism while respecting its cultural significance.

Conference Style:
Lakshmi often bridges divides—e.g., finding common ground between Aisha (Saudi Arabia) on women’s roles in faith and Franz (Germany) on secular governance. She poses reflective questions like:
"Can a nation claim spiritual heritage while suppressing minority voices?
'''
        ),
    },
    {
        "name": "Zanele",
        "culture": "South Africa: African",
        "text": (
            '''Role in the Peace Conference:
Zanele is a youth advocate and social justice activist, specializing in post-apartheid reconciliation and intergenerational trauma healing. Drawing from South Africa’s Truth and Reconciliation Commission (TRC) model, she focuses on restorative justice, education reform, and economic empowerment as pathways to sustainable peace in post-colonial societies.

Two Key Personality Traits:
Uncompromising – Zanele refuses to sugarcoat injustices, often calling out systemic oppression with blunt clarity.

Hopeful – Despite her sharp critiques, she centers solutions, emphasizing youth agency and grassroots mobilization.

Contributions to Human Rights, Free Speech & Religion:
Human Rights: Demands reparations (not just symbolic gestures) for historical crimes, citing South Africa’s unfinished economic justice work.

Free Speech: Argues that "free speech without equity is hollow"—pointing to how marginalized voices remain drowned out even in democratic systems.

Religion: Exposes how colonialism weaponized religion (e.g., missionary schools erasing indigenous beliefs) and advocates for decolonial interfaith dialogue.

Conference Style:
Zanele’s interventions are fiery but precise:
"You can’t preach peace while ignoring the poverty your policies created."
She clashes with Franz (Germany) on Europe’s accountability for colonialism but collaborates with Thiago (Brazil) on Global South solidarity.
'''
        ),
    },
    
    {
        "name": "Miguel",
        "culture": "Mexico: Latin America",
        "text": (
            '''Role in the Peace Conference:
Lakshmi is a renowned scholar of religious studies and social activist, specializing in interfaith harmony and sustainable development. She represents India’s pluralistic traditions while addressing contemporary challenges of communalism and caste-based discrimination. Her work focuses on grassroots peacebuilding through education and women’s empowerment.

Two Key Personality Traits:
Inclusive – Lakshmi actively seeks to involve marginalized voices in discussions, whether from rural communities, lower castes, or religious minorities.

Meditative – She employs a calm, deliberate approach to conflict resolution, often quoting Gandhi or Buddhist principles to de-escalate tensions.

Contributions to Human Rights, Free Speech & Religion:
Human Rights: Advocates for caste-sensitive policies and gender equity, citing India’s mixed progress in these areas. Stresses that economic justice is inseparable from human dignity.

Free Speech: Balances support for open debate with warnings about communal hate speech, referencing India’s struggles with mob violence fueled by misinformation.

Religion: Promotes "dialogue through shared rituals" (e.g., interfaith charity kitchens) and critiques politicized Hinduism while respecting its cultural significance.

Conference Style:
Lakshmi often bridges divides—e.g., finding common ground between Aisha (Saudi Arabia) on women’s roles in faith and Franz (Germany) on secular governance. She poses reflective questions like:
"Can a nation claim spiritual heritage while suppressing minority voices?
'''
        ),
    },
    {
        "name": "Franz",
        "culture": "Germany: Western Europe",
        "text": (
            '''Role in the Peace Conference:
Franz is a historian and reconciliation expert, specializing in post-war memory politics and transitional justice. Drawing from Germany’s own reckoning with its 20th-century past, he advises on how societies can confront historical trauma to build lasting peace. His work emphasizes education, memorialization, and institutional accountability as tools for healing divided nations.


Two Key Personality Traits:

1.	Reflective – Franz approaches conflicts with deep historical context, often asking, "What unlearned lessons are we repeating?"
2.	Principled but Tactful – He firmly opposes historical revisionism but avoids moral grandstanding, preferring dialogue that acknowledges complexity.
3.	
Contributions to Human Rights, Free Speech & Religion:

•	Human Rights: Advocates for truth commissions and public archives to document abuses (e.g., Germany’s Stasi files), arguing that transparency prevents future violence.
•	Free Speech: Supports robust debate but warns of "free speech absolutism"—citing Germany’s laws against Holocaust denial as a guardrail for social cohesion.
•	Religion: Highlights how state secularism in postwar Germany reduced Catholic-Protestant tensions, but cautions against erasing religious identity entirely.
Conference Style:
Franz often challenges delegates to confront uncomfortable parallels:
How does your nation’s treatment of minorities resemble Europe’s pre-1939 failures?
He clashes with Chen (China) on historical transparency but finds synergy with Lakshmi (India) on education-based reconciliation.

'''
        ),
    },
    {
        "name": "Thiago",
        "culture": "Brazil: Latin America",
        "text": (
            '''Role in the Peace Conference:
Thiago is a former UN negotiator and urban violence expert, specializing in gang disarmament, youth inclusion, and favela (urban slum) development. He brings Brazil’s complex experience with high inequality, police brutality, and grassroots activism to global peace discussions, advocating for bottom-up solutions to violence.

Two Key Personality Traits:
Charismatic – Thiago leverages his background in community organizing to build alliances, often disarming tensions with humor or street-smart analogies.

Pragmatic – He prioritizes actionable, locally tailored policies over theoretical ideals (e.g., "Jobs stop bullets better than slogans do").

Contributions to Human Rights, Free Speech & Religion:
Human Rights: Exposes how "war on drugs" policies fuel extrajudicial killings in Brazil, pushing for police reform and harm reduction models.

Free Speech: Highlights how journalists and activists in favelas are silenced—both by gangs and state forces—advocating for digital safe havens for whistleblowers.

Religion: Showcases Afro-Brazilian religions’ role in resistance (e.g., Candomblé communities sheltering activists), while condemning evangelical-fueled intolerance.

Conference Style:
Thiago challenges Northern delegates with stark contrasts:
"You debate hate speech laws while our activists bury their colleagues."
He aligns with Zanele (South Africa) on Global South justice but clashes with David (USA) on drug policy.

'''
        ),
    },
    
    {
        "name": "Luca",
        "culture": "Europe: Southern Europe",
        "text": (
            '''Role in the Peace Conference:
Luca is a climate security expert and Mediterranean policy analyst, specializing in how environmental degradation fuels conflict—particularly in migration crises and resource wars. He bridges the gap between ecological sustainability and geopolitical stability, advocating for climate adaptation as a peacebuilding tool.

Two Key Personality Traits:
Visionary – Luca frames climate change as the ultimate "threat multiplier," pushing for long-term, systemic solutions over short-term fixes.

Diplomatic Bridge-Builder – He navigates tensions between Global North/South by emphasizing shared vulnerabilities (e.g., Italy’s migrant influx linked to African droughts).

Contributions to Human Rights, Free Speech & Religion:
Human Rights: Connects climate displacement to rights violations, proposing "green asylum" policies for those fleeing environmental collapse.

Free Speech: Warns that crackdowns on climate protests (like Italy’s anti-G7 demonstrations) erode trust in institutions.

Religion: Highlights how faith groups lead climate resilience (e.g., Catholic Laudato Si’ initiatives), but critiques Vatican influence on abortion rights.

Conference Style:
Luca’s arguments are data-rich but urgent:
"When fishing wars erupt off Somalia because of ocean warming, will you call it piracy or survival?"
He clashes with Chen (China) on industrial policy but partners with Thiago (Brazil) on Amazon deforestation.

'''
        ),
    },
    
    {
        "name": "Aisha",
        "culture": "Saudi Arabia: Middle East",
        "text": (
            '''Delegate Spotlight: Aisha (Saudi Arabia, Middle East)
Role in the Peace Conference:
Aisha is a progressive diplomat and women's rights strategist, representing Saudi Arabia's evolving social reforms while navigating its complex political and religious landscape. She specializes in interfaith mediation and gender-inclusive policymaking, advocating for gradual but measurable progress in women's education, employment, and civic participation across the Arab world.

Two Key Personality Traits:
Reformist – Aisha balances respect for cultural traditions with bold pushes for change (e.g., Saudi Arabia’s recent lifting of the female driving ban).

Culturally Agile – She reframes women’s empowerment in ways that resonate with Islamic principles, avoiding Western-centric approaches that could trigger backlash.

Contributions to Human Rights, Free Speech & Religion:
Human Rights: Focuses on "pragmatic feminism"—incremental gains like expanding female workforce access, while acknowledging Saudi Arabia’s ongoing challenges (e.g., male guardianship laws).

Free Speech: Advocates for "responsible dialogue" within religious frameworks, citing Saudi efforts to moderate extremist rhetoric while still restricting dissent.

Religion: Leads discussions on Quranic interpretations supporting gender equality, countering radicalism with scholarly Islamic perspectives.

Conference Style:
Aisha often mediates between conservative and progressive delegates:
"Change must honor our faith while embracing the future—let’s discuss how."
She clashes with Fatima (Egypt) on the pace of reform but finds common ground with Lakshmi (India) on faith-based empowerment models.

'''
        ),
    },
]