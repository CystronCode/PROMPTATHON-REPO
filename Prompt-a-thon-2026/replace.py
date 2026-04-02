import re
with open('index.html', 'r', encoding='utf-8') as f: content = f.read()

# Replace font
content = content.replace('family=Press+Start+2P', 'family=Orbitron:wght@600..900')
content = content.replace('"Press Start 2P"', '"Orbitron", sans-serif')

# SVG definitions
svgs = """const svgs = [
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect x="25" y="10" width="50" height="80" rx="10" stroke="#FFF" stroke-width="4" fill="none"/><path d="M40 25 Q50 10 60 25" stroke="#FFF" stroke-width="3" stroke-dasharray="2 4" fill="none"/></svg>',
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="35" stroke="#FFF" stroke-width="4" fill="none"/><path d="M50 15v35 M25 75l25-25 M75 75l-25-25" stroke="#FFF" stroke-width="5"/></svg>',
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="20" r="12" stroke="#FFF" stroke-width="3" fill="none"/><circle cx="20" cy="75" r="12" stroke="#FFF" stroke-width="3" fill="none"/><circle cx="80" cy="75" r=\"12\" stroke=\"#FFF\" stroke-width=\"3\" fill=\"none\"/><path d=\"M50 32l-22 31 M50 32l22 31 M32 75h36\" stroke=\"#FFF\" stroke-dasharray=\"4 4\" stroke-width=\"3\"/></svg>',
  '<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\"><rect x=\"25\" y=\"25\" width=\"50\" height=\"50\" stroke=\"#FFF\" stroke-width=\"6\" fill=\"none\"/><path d=\"M25 35h-15 M25 65h-15 M75 35h15 M75 65h15 M35 25v-15 M65 25v-15 M35 75v15 M65 75v15\" stroke=\"#FFF\" stroke-width=\"4\"/></svg>',
  '<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\"><rect x=\"15\" y=\"15\" width=\"70\" height=\"70\" rx=\"5\" stroke=\"#FFF\" stroke-width=\"4\" fill=\"none\"/><rect x=\"30\" y=\"15\" width=\"40\" height=\"20\" fill=\"none\" stroke=\"#FFF\" stroke-width=\"2\"/><rect x=\"35\" y=\"65\" width=\"30\" height=\"20\" stroke=\"#FFF\" stroke-width=\"2\" fill=\"none\"/></svg>',
  '<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\"><circle cx=\"50\" cy=\"50\" r=\"45\" stroke=\"#FFF\" stroke-width=\"3\" fill=\"none\"/><ellipse cx=\"50\" cy=\"50\" rx=\"15\" ry=\"45\" stroke=\"#FFF\" stroke-width=\"3\" fill=\"none\"/><path d=\"M5 50h90 M20 30h60 M20 70h60\" stroke=\"#FFF\" stroke-width=\"2\"/></svg>',
  '<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\"><rect x=\"25\" y=\"10\" width=\"50\" height=\"80\" rx=\"8\" stroke=\"#FFF\" stroke-width=\"4\" fill=\"none\"/><rect x=\"30\" y=\"15\" width=\"40\" height=\"60\" stroke=\"#FFF\" stroke-width=\"2\" fill=\"none\"/><circle cx=\"50\" cy=\"82\" r=\"3\" fill=\"#FFF\"/></svg>',
  '<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 100 100\"><path d=\"M50 10l35 20v40l-35 20l-35-20v-40z\" stroke=\"#FFF\" stroke-width=\"4\" fill=\"none\"/><circle cx=\"50\" cy=\"50\" r=\"12\" fill=\"#FFF\"/><path d=\"M50 25v13 M35 60l10-10 M65 60l-10-10 L20 40l25 10 M80 40l-25 10\" stroke=\"#FFF\" stroke-width=\"2\"/></svg>'
];
const eraImages = svgs.map((svg, i) => {
    let img = new Image();
    img.src = 'data:image/svg+xml;utf8,' + encodeURIComponent(svg.replace(/#FFF/g, ERAS[i].glowCol));
    return img;
});
"""

# We inject eraImages definition after ERAS
content = content.replace('        const ERAS = [', svgs + '\n        const ERAS = [')

# Completely replace drawBgLayers and drawBackground
bg_pattern = r'        function drawBgLayers\(\) \{.*?                \}\);\n            \}\);\n        \}'
content = re.sub(bg_pattern, '        function drawBgLayers() {\n            // background drawing handled directly inside drawBackground natively\n        }', content, flags=re.DOTALL)

draw_bg_pattern = r'        // ── Background ────────.*?        \}'
new_bg = '''        // ── Background ────────────────────────────────────────────────────────────
        function drawBackground() {
            const e = eraObj;
            // flat 2d background without 3d gradient
            ctx.fillStyle = e.bgTop;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw background animated carousel image
            ctx.save();
            ctx.globalAlpha = 0.15 + 0.05 * Math.sin(frame * 0.05);
            ctx.translate(canvas.width / 2, canvas.height / 2);
            ctx.rotate(frame * 0.005);
            let s = Math.min(canvas.width, canvas.height) * 0.8;
            s += Math.sin(frame * 0.03)*30; // subtle scaling animation
            if(eraImages[era % 8] && eraImages[era % 8].complete) {
                ctx.drawImage(eraImages[era % 8], -s/2, -s/2, s, s);
            }
            ctx.restore();
        }'''
content = re.sub(draw_bg_pattern, new_bg, content, flags=re.DOTALL)

# Update transition wiping to smooth fade
trans_pattern = r'            else if \(transitionTimer < 120.*?transitionAlpha = 0; \}'
content = re.sub(trans_pattern, '            else if (transitionTimer < 120) transitionAlpha = Math.max(0, 1 - (transitionTimer - 80) / 40);\n            else { gameState = \\\'playing\\\'; transitionAlpha = 0; }', content, flags=re.DOTALL)

# Refine space hold grav logic for smoother variable jumps
grav_pattern = r'                let grav = 0\.65;\n                if \(spaceHeld\).*?grav = 0\.25;\n                \}'
new_grav = '''                let grav = 0.65;
                if (spaceHeld && !this.agActive && this.vy < 0) grav = 0.25;
                else if (spaceHeld && this.agActive && this.vy > 0) grav = 0.25;'''
content = re.sub(grav_pattern, new_grav, content, flags=re.DOTALL)

content = content.replace("\\'playing\\'", "'playing'")

with open('index.html', 'w', encoding='utf-8') as f: f.write(content)
print('Success')
