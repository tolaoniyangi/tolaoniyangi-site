"""Ring + label on the clicked intersection in the traffic Fig. 3 clip frames."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
d=sys.argv[1]; X,Y=702,503; START=17          # frame where the map has settled
ACC=(226,81,43); INK=(20,20,19)
font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',17,index=0)
fs=sorted(f for f in os.listdir(d) if f.endswith('.png'))
for i,f in enumerate(fs):
    if i<START: continue
    a=min(1,(i-START)/8)                      # fade in over ~0.25s
    im=Image.open(d+f).convert('RGBA'); ov=Image.new('RGBA',im.size,(0,0,0,0)); dr=ImageDraw.Draw(ov)
    al=int(255*a); r=17
    dr.ellipse((X-r-2,Y-r-2,X+r+2,Y+r+2),outline=(255,255,255,al),width=5)
    dr.ellipse((X-r,Y-r,X+r,Y+r),outline=ACC+(al,),width=3)
    text="Selected intersection"; w=dr.textlength(text,font=font); h=30; x1=X-r-14; x0=x1-w-24
    dr.line((x1,Y,X-r-3,Y),fill=(255,255,255,al),width=2)
    dr.rounded_rectangle((x0,Y-h/2,x1,Y+h/2),radius=h/2,fill=(255,255,255,al))
    dr.text((x0+12,Y-10),text,font=font,fill=INK+(al,))
    Image.alpha_composite(im,ov).convert('RGB').save(d+f)
print(len(fs),"frames")
