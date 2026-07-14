# Command Reference

A running collection of commands worth remembering — copy/paste ready.

---

## Git / GitHub

**Standard push flow (scoped configs → dotfiles → GitHub):**
```bash
cd ~/dotfiles
for dir in hypr waybar swaync kitty rofi yazi btop; do
    rm -rf .config/"$dir"
    cp -r ~/.config/"$dir" .config/ 2>/dev/null
done

# sanity check before committing — should be empty
grep -rli "password\|token\|api_key\|secret" .config/ 2>/dev/null

git status
git add -A
git commit -m "describe what changed"
git push
```

**If push is rejected (remote has commits you don't have locally):**
```bash
git pull --rebase origin main
git push
```

**Fix wrong commit author email retroactively across ALL history (one-time fix, already done):**
```bash
cp -r ~/dotfiles ~/dotfiles-backup   # always back up first
cd ~/dotfiles
git log --format='%ae' | sort -u     # check what emails exist
git filter-repo --email-callback 'return b"bruhcomedoe@gmail.com"' --force
git remote add origin git@github.com:IridescentGlow/hyprland-dotfiles.git
git push --force origin main
```

**Fix just the most recent commit's email:**
```bash
git commit --amend --author="luminara <bruhcomedoe@gmail.com>" --no-edit
git push --force
```

---

## Docker / Pi-hole

**Run Pi-hole, bound only to real network IP (avoids port 53 conflict with libvirt's dnsmasq):**
```bash
sudo docker run -d \
  --name pihole \
  -p 192.168.8.32:53:53/tcp -p 192.168.8.32:53:53/udp \
  -p 8080:80/tcp \
  -e TZ="Africa/Addis_Ababa" \
  -e FTLCONF_webserver_api_password="yourpassword" \
  -v pihole_etc:/etc/pihole \
  -v pihole_dnsmasq:/etc/dnsmasq.d \
  --restart=unless-stopped \
  pihole/pihole:latest
```

**Check container status / remove if broken:**
```bash
sudo docker ps -a
sudo docker rm pihole
```

**Dashboard:** `http://192.168.8.32:8080/admin`

**Point this machine's DNS at Pi-hole (temporary/manual method):**
```bash
sudo nano /etc/resolv.conf
# nameserver 192.168.8.32
```
(NetworkManager may overwrite this on reconnect — not a permanent fix, just quick testing)

---

## Virtual Machines / virsh (Kioptrix lab)

**Find your libvirt network's real subnet:**
```bash
virsh --connect qemu:///system net-list --all
virsh --connect qemu:///system net-dumpxml default
```

**Find your real (non-virtual) network IP:**
```bash
ip -4 addr show | grep -v '192.168.122\|127.0.0.1' | grep inet
# or
ip route get 1.1.1.1 | grep -oP 'src \K\S+'
```

**Scan the lab network for live hosts:**
```bash
sudo nmap -sn 192.168.122.0/24
```

**Full port + service/version scan (the real first step of any box):**
```bash
mkdir -p ~/<boxname>/nmap
sudo nmap -sC -sV -p- --reason -oA ~/<boxname>/nmap/initial <target-ip>
```

**Targeted Samba vulnerability check:**
```bash
sudo nmap -p 139,445 --script "smb-os-discovery,smb-vuln*" <target-ip>
```
(remember: quote the `--script` value in zsh, or the `*` gets glob-expanded and errors out)

---

## Hyprland / SwayNC troubleshooting

**Force-clear a stuck swaync D-Bus lock (common when testing config changes):**
```bash
busctl --user call org.freedesktop.DBus /org/freedesktop/DBus org.freedesktop.DBus GetConnectionUnixProcessID s org.erikreider.swaync
kill -9 <PID_returned_above>
pgrep swaync   # should print nothing
setsid swaync &
```

**Check for CSS parse errors (any `!important` here breaks GTK's swaync parser):**
```bash
swaync 2>&1 | grep -i "error\|junk\|not a valid"
```

**Hyprland live config changes (Lua provider — `hyprctl keyword` does NOT work here):**
```bash
hyprctl eval "hl.config({ decoration = { blur = { size = 10 } } })"
```

**Check current Hyprland config for parse errors:**
```bash
hyprctl -j configerrors
```

---

## System / Package Management

**BlackArch install:**
```bash
curl -O https://blackarch.org/strap.sh
chmod +x strap.sh
sudo ./strap.sh
sudo pacman -Syy   # if mirror sync fails, edit /etc/pacman.d/blackarch-mirrorlist first
sudo pacman -S --needed blackarch-officials
```

**Generate a scoped, explicit-only package list (for dotfiles/install.sh):**
```bash
pacman -Qqen > pkglist-pacman.txt   # official repo packages
pacman -Qqem > pkglist-aur.txt      # AUR packages
```
