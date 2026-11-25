# Builds web/public/resume.pdf (one page, email only, no phone number). Text follows TJ's final marketing resume.
# Edit the DATA below, then:  python3 tools/resume/build_resume_pdf.py   (needs: pip install reportlab)
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'web', 'public', 'resume.pdf')

NAME = 'Mohammed Tahmid Jalal (TJ)'
LINE = 'Marketing coordinator  |  Coquitlam, BC  |  tahmidjalal8@gmail.com  |  linkedin.com/in/tahmidjalal'
SUMMARY = ('Marketing coordinator running social media, paid media, events, web and reputation for Cloverdale Paint, a Canadian '
           'paint manufacturer with 82 stores and a national dealer network. Grew Instagram and Facebook 348%, led Colour of '
           'the Year 2027 launch events with 2,500+ attendees, and created two buy-Canadian campaigns, including 30 Days of '
           'Made in Canada. Works directly with senior leadership and uses AI tools to produce content faster.')
SKILLS = [
 ('Marketing', 'campaign management, content strategy, brand positioning, event marketing, retail and B2B marketing, dealer marketing, partnership marketing, product launch'),
 ('Social and paid media', 'Instagram, Facebook, LinkedIn, TikTok, community management, Meta Ads Manager, geofencing, audience targeting, retargeting, A/B testing, CPC and CPM optimization'),
 ('Web, email, analytics and reputation', 'GA4, Meta Business Suite, campaign reporting, SEO, copywriting, Sitefinity CMS, intranet, Shopify, email marketing (Salesforce), Google Business Profile, Eventbrite'),
 ('Content, design and AI', 'video production, direction and editing, graphic and label design, Adobe Creative Suite, Canva, Claude, Claude Code, ChatGPT, Gemini, workflow automation'),
]
JOBS = [
 ('Cloverdale Paint Inc.', 'Marketing coordinator, Surrey, BC', 'April 2026 - present', [
   'Grew Instagram and Facebook 348% with original, trend-based video, carousel and meme content; top posts reached 50,000 to 100,000+ views. Manage three LinkedIn pages (industrial, corporate, specifier and designer) with about 12,000 combined followers.',
   'Led creative and on-site execution of the Colour of the Year 2027 colour edit booths, drawing 1,000+ attendees in Vancouver and 1,500+ in Toronto, including travelling to run the Toronto launch on site, working directly with the president and CEO.',
   'Created the Canadian by Canadian campaign and now leading 30 Days of Made in Canada, featuring 30 Canadian businesses across web and social and reaching audiences outside the paint industry.',
   'Built retail-focused campaigns and community partnerships to grow awareness among homeowners and small painters; partnered with BCAA on the Fan Club VIP program and designed member email wireframes.',
   'Run Meta and geofenced campaigns for authorized dealers across Canada, targeted by location, age and job title, on budgets around $2,000, including a $500 per month awareness campaign for Cloverdale\'s largest dealer in Ontario\'s Chinese community.',
   'Manage online reputation for 82 locations, handling 80 to 150 Google reviews weekly and resolving complaints with stores and HR; turned negative feedback on a product launch into marketing content.',
   'Manage the website, intranet, SEO blogs, monthly sale campaigns and product labels; built a Claude Code and Canva workflow that turns a 1,921-colour database into 4K colour palette videos.']),
 ('Jaalik Tech', 'Digital marketing (self-initiated agency)', '2022 - present', [
   'Paid Meta and TikTok campaigns, content and Shopify stores for small client brands, using audience segmentation and A/B creative testing.']),
 ('Skechers', 'Product specialist, Metro Vancouver', 'July 2025 - March 2026', [
   'Supported product launches through customer outreach and in-store brand messaging.']),
 ('Telus Communications', 'Area sales manager, Metro Vancouver', 'October 2023 - May 2025', [
   'Managed residential and business sales, consistently meeting targets.']),
]
AI = None
EDU = 'Simon Fraser University, Burnaby, BC: Bachelor of Science, Information and Interactive Arts and Technology (in progress)'
LANG = 'Arabic (native), English, Bengali, Hindi, Urdu'
REF = 'Signed manager testimonial and references available on request.'

ink = colors.HexColor('#1a1a1a'); mute = colors.HexColor('#555555')
H = ParagraphStyle('h', fontName='Helvetica-Bold', fontSize=20, leading=24, textColor=ink)
C = ParagraphStyle('c', fontName='Helvetica', fontSize=9, leading=12, textColor=mute)
S = ParagraphStyle('s', fontName='Helvetica-Bold', fontSize=9.5, leading=12, textColor=ink, spaceBefore=9, spaceAfter=2)
B = ParagraphStyle('b', fontName='Helvetica', fontSize=8.9, leading=11.4, textColor=ink)
J = ParagraphStyle('j', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=ink, spaceBefore=5)
R = ParagraphStyle('r', fontName='Helvetica', fontSize=9, leading=12, textColor=mute)
L = ParagraphStyle('l', parent=B, leftIndent=11, bulletIndent=1)

def esc(t): return t.replace('&', '&amp;')
st = [Paragraph(esc(NAME), H), Paragraph(esc(LINE), C), Spacer(1, 6), Paragraph(esc(SUMMARY), B),
      Paragraph('CORE SKILLS', S), HRFlowable(width='100%', thickness=0.5, color=mute), Spacer(1, 3)]
st += [Paragraph(f'<b>{esc(k)}:</b> {esc(v)}', B) for k, v in SKILLS]
st += [Paragraph('EXPERIENCE', S), HRFlowable(width='100%', thickness=0.5, color=mute)]
for org, role, when, pts in JOBS:
    blk = [Paragraph(f'{esc(org)} <font name="Helvetica" size="9" color="#555555">| {esc(role)} | {when}</font>', J)]
    blk += [Paragraph(esc(p), L, bulletText='\u2022') for p in pts]
    st.append(KeepTogether(blk))
st += [Paragraph('EDUCATION AND LANGUAGES', S), HRFlowable(width='100%', thickness=0.5, color=mute), Spacer(1, 3),
       Paragraph(esc(EDU), B), Paragraph('Languages: ' + esc(LANG), B), Paragraph('References: ' + esc(REF), B)]
SimpleDocTemplate(OUT, pagesize=letter, leftMargin=0.7*inch, rightMargin=0.7*inch, topMargin=0.6*inch, bottomMargin=0.55*inch,
                  title='TJ resume', author='TJ').build(st)
print('wrote', os.path.abspath(OUT))
