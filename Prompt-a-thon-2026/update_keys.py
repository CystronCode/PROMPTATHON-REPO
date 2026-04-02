with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Swap internal variables
text = text.replace('spaceHeld', 'arrowHeld')
text = text.replace('spaceJustPressed', 'arrowJustPressed')

# Update keydown listeners to drop Space and only keep ArrowUp
# In the original file: if (e.code === 'Space' || e.code === 'ArrowUp')
text = text.replace("if (e.code === 'Space' || e.code === 'ArrowUp')", "if (e.code === 'ArrowUp')")

# Update HUD prompts
text = text.replace('PRESS SPACE TO BEGIN', 'PRESS UP ARROW TO BEGIN')
text = text.replace('PRESS SPACE TO RESTART', 'PRESS UP ARROW TO RESTART')
text = text.replace('PRESS SPACE TO PLAY AGAIN', 'PRESS UP ARROW TO PLAY AGAIN')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated keys to ArrowUp")
