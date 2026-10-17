"""Make a narrated walkthrough from real saved API evidence (macOS build helper)."""
import json, pathlib, re, subprocess, textwrap
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

HERE=pathlib.Path(__file__).resolve().parent
DATA=json.loads((HERE/'live_verification.json').read_text())
OUT=HERE/'video_build';OUT.mkdir(exist_ok=True)
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
BOLD='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def font(n,b=False):return ImageFont.truetype(BOLD if b else FONT,n)
def text(draw,xy,value,width=70,size=23,color='#423139',bold=False):
    x,y=xy
    value=re.sub(r'[*`]', '',value)
    for paragraph in value.splitlines():
        for line in textwrap.wrap(paragraph,width=width) or ['']:
            draw.text((x,y),line,font=font(size,bold),fill=color);y+=size+9
    return y
def fit_text(draw,box,value,size=21):
    """Wrap by rendered width and fit the complete reply inside its panel."""
    x,y,right,bottom=box
    value=re.sub(r'[*`]', '',value).replace('\\n','\n')
    for chosen in range(size,13,-1):
        face=font(chosen);lines=[]
        for paragraph in value.splitlines():
            line=''
            for word in paragraph.split():
                candidate=(line+' '+word).strip()
                if face.getlength(candidate)>right-x and line:
                    lines.append(line);line=word
                else:line=candidate
            lines.append(line)
        if len(lines)*(chosen+8)<=bottom-y:break
    assert len(lines)*(chosen+8)<=bottom-y, 'Reply cannot fit without truncation.'
    for line in lines:
        draw.text((x,y),line,font=face,fill='#423139');y+=chosen+8
    return y
slides=[]
slides.append(('Petal & Crumb Atelier','Real Gemini conversation and model tool calls',
    'Flora answers from a PDF and text summary, routes messages, collects customer enquiries, and records feedback. This narrated walkthrough presents actual results captured from the deployed app.',None))
titles=['Grounded business answer','Conversation memory and calculation','A booking enquiry, not a confirmed reservation','Missing name: no lead recorded','Complete contact details: real lead tool','Unknown question: feedback tool','Customer complaint: feedback tool']
narrations=[
 'First, Flora answers a business question using the verified profile. Glaze and Sip costs thirty eight dollars per person.',
 'The next question refers to that experience without repeating its name. Flora remembers Glaze and Sip and calculates one hundred fifty two dollars for four people.',
 'Now the guest requests a reservation for four. Flora gathers the contact information. Recording an enquiry does not confirm availability or a booking.',
 'The guest provides an email, but no name. The phrase I am interested is not accepted as a customer name, and the lead tool is not called.',
 'The guest now provides Noor Haddad and a fictional email. Gemini calls record customer interest. The application saves the record and returns the actual successful result to the model.',
 'Valet service is absent from the business documents. Gemini calls record feedback, logs the exact question, and explains that a human must confirm the answer.',
 'A complaint about stale pastries follows the feedback route and is recorded through the same tool. No business policy or resolution is invented.'
]
for title,narration,item in zip(titles,narrations,DATA['cases']):slides.append((title,item['message'],narration,item))
slides.append(('Reflection and regression checks','Draft, revised reply, and actual outcomes',
    'Here the draft inferred Noor from an email address. The reflection removed that unsupported name and still requested the full name before recording a lead. This is an actual saved draft and revision. Twenty five offline regression tests also check history, contact validation, failed storage, outages, and tool execution.',DATA['cases'][3]))
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
segments=[]
for i,(title,subtitle,narration,item) in enumerate(slides):
    im=Image.new('RGB',(1280,720),'#faf6f0');d=ImageDraw.Draw(im)
    d.rectangle((0,0,1280,12),fill='#865369')
    text(d,(60,37),'PETAL & CRUMB ATELIER  /  AGENT-POWERED BUSINESS ASSISTANT',width=100,size=16,color='#865369',bold=True)
    text(d,(60,83),title,width=60,size=36,color='#3e2935',bold=True)
    if item:
        d.rounded_rectangle((55,155,845,634),radius=18,fill='#ffffff',outline='#dfcdd3',width=2)
        y=text(d,(80,177),'GUEST',size=15,color='#865369',bold=True)
        y=text(d,(80,y+6),subtitle,width=63,size=21)
        y=text(d,(80,y+22),'FLORA',size=15,color='#865369',bold=True)
        fit_text(d,(80,y+6,820,615),item['reply'])
        d.rounded_rectangle((875,155,1225,634),radius=18,fill='#f0e5e8')
        t=item['trace'];y=text(d,(900,179),'ACTUAL TURN EVIDENCE',size=15,bold=True,color='#865369')
        y=text(d,(900,y+20),'Route: '+t['intent'],width=25,size=20,bold=True)
        y=text(d,(900,y+17),'History messages: '+str(t['history_messages']),width=25,size=19)
        events=t['tool_calls']
        y=text(d,(900,y+20),'Tools: '+('none' if not events else ''),width=24,size=19,bold=True)
        for event in events:
            y=text(d,(900,y+6),event['name'],width=25,size=18)
            y=text(d,(900,y+6),'Status: '+event['result']['status'],width=25,size=18,color='#326348',bold=True)
        text(d,(900,max(y+25,470)),'Reflection: draft and revised reply captured',width=23,size=18)
    else:
        text(d,(65,190),subtitle,width=65,size=29,color='#865369',bold=True)
        text(d,(65,264),'Three routes: general question, lead collection, feedback / unknown question.\n\nTwo model-called tools. Short-term memory. PDF and TXT grounding. Gradio. Reflection.',width=72,size=25)
    if i==len(slides)-1:
        d.rectangle((60,155,1220,635),fill='#fff')
        t=item['trace']
        text(d,(80,175),'ORIGINAL DRAFT',size=16,bold=True,color='#865369')
        fit_text(d,(80,220,610,610),t['draft'])
        text(d,(670,175),'REVISED REPLY',size=16,bold=True,color='#865369')
        fit_text(d,(670,220,1195,610),t['revised'])
    d.text((60,672),'Captured live Gemini API evidence • Fictional customer details • '+DATA['captured_at'][:10],font=font(15),fill='#786a70')
    d.text((1165,672),f'{i+1}/{len(slides)}',font=font(16),fill='#786a70')
    img=OUT/f'{i:02}.png';im.save(img)
    speech=OUT/f'{i:02}.txt';speech.write_text(narration)
    audio=OUT/f'{i:02}.aiff'
    subprocess.run(['say','-v','Samantha','-r','162','-f',str(speech),'-o',str(audio)],check=True)
    segment=OUT/f'{i:02}.mp4'
    subprocess.run([ffmpeg,'-y','-loglevel','error','-loop','1','-i',str(img),'-i',str(audio),'-c:v','libx264','-tune','stillimage','-preset','fast','-c:a','aac','-shortest','-pix_fmt','yuv420p','-r','24',str(segment)],check=True)
    segments.append(segment)
manifest=OUT/'concat.txt';manifest.write_text(''.join("file '"+str(p)+"'\n" for p in segments))
subprocess.run([ffmpeg,'-y','-loglevel','error','-f','concat','-safe','0','-i',str(manifest),'-c','copy',str(HERE/'petal_and_crumb_demo.mp4')],check=True)
print('Narrated walkthrough created from actual live API evidence.')
