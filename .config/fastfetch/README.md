# Fastfetch Config 

───────────────────────────────────────────────  
 °˖* ૮( • ᴗ ｡)っ🍸 shheersh - Dionysus vers. 1.0   
 ───────────────────────────────────────────────  

## Custom animated **Fastfetch**.


![Fastfetch Demo Gif](../../assets/demo-fastfetch.gif)  
---

##  Features
  - Minimal info layout 
  - **Animated Ascii** via `animated-fastfetch.sh` 
  - Fast load.

![Fastfetch Demo Png](../../assets/demo-fastfetch.png)

```
fastfetch/  
├── config.conf  
├── myascii.txt  
├── animated-fastfetch.sh  
├── frames_colour/  
├── demo.gif  
└── demo.png  
```

## Usage
Add to your `~/.bashrc` or `~/.zshrc` (or whatever shell rc you use):
```
####  Animated Fastfetch Splash
if [[ -n $PS1 ]]; then
   ~/.config/fastfetch/animated-fastfetch.sh 0.05
  clear
fi
```
Frames live in `frames_colour` can be changed to whatever.

**Note:** animated-fastfetch.sh caches your fastfetch setting for faster load, SO if you make edits please remember to `rm -f ~/.cache/fastfetch.txt`.. I'm aware there is fast fetch. 
 

