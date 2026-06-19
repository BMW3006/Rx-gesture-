# RX Gesture Control 🖐️

Mfumo wa kudhibiti volume ya simu kwa kutumia ishara za mkono (hand gestures)
zinazosomwa na kamera, kupitia browser + MediaPipe, kisha kutumwa kwa Termux
ili kuendesha amri za Android.

## Jinsi Inavyofanya Kazi

```
Kamera (Browser) → MediaPipe.js inasoma mkono → Inatambua gesture
        ↓
   HTTP request → Flask server (Termux)
        ↓
   termux-volume inabadilisha sauti
```

- **✋ Mkono Wazi (Open Palm)** → Ongeza volume
- **✊ Ngumi (Fist)** → Punguza volume

## Mahitaji

1. **Termux** (kutoka F-Droid, sio Play Store)
2. **Termux:API** app (kutoka F-Droid) + package: `pkg install termux-api`
3. **Python** + **Flask**

## Hatua za Kusakinisha

Fungua Termux na endesha amri hizi moja baada ya nyingine:

```bash
pkg update && pkg upgrade -y
pkg install python termux-api -y
pip install flask
termux-setup-storage
```

Sakinisha pia app ya **Termux:API** kutoka F-Droid:
https://f-droid.org/packages/com.termux.api/

## Jinsi ya Kuendesha

1. Hakikisha faili hizi mbili (`server.py` na `index.html`) ziko kwenye
   folder moja, kwa mfano:

```bash
mkdir -p ~/rx-gesture-control
cd ~/rx-gesture-control
# weka server.py na index.html humu
```

2. Endesha server:

```bash
python server.py
```

3. Fungua **browser** (Chrome/Firefox) kwenye simu hiyo hiyo, nenda:

```
http://127.0.0.1:5000
```

4. Bonyeza **"Anzisha Kamera"**, ruhusu (allow) ufikiaji wa kamera,
   kisha onyesha mkono wako mbele ya kamera:
   - Nyoosha vidole vyote (mkono wazi) → volume itaongezeka
   - Funga ngumi → volume itapungua

## Kutatua Matatizo (Troubleshooting)

| Tatizo | Suluhisho |
|---|---|
| `termux-volume: command not found` | Hakikisha umesakinisha `pkg install termux-api` NA app ya Termux:API kutoka F-Droid |
| Kamera haifunguki kwenye browser | Hakikisha umeruhusu (allow) "Camera" permission kwa browser hiyo kwenye Android Settings |
| Gesture haitambuliwi vizuri | Hakikisha mwanga wa kutosha, mkono uwe karibu na uonekane wazi kwenye kamera |
| Volume haibadiliki | Jaribu kuendesha `termux-volume` peke yake kwenye Termux kuona kama inafanya kazi |
| Server haifunguki kwenye browser | Hakikisha bado Termux inaendesha `python server.py` (usifunge dirisha) |

## Hatua Zinazofuata (baada ya hii kufanya kazi)

Mara tu hii ya msingi ikifanya kazi vizuri, tunaweza kuongeza:
- ✌️ Vidole viwili (peace sign) → kufungua app maalum
- 👍 Thumbs up → kupiga screenshot
- 👈👉 Kusogeza mkono kushoto/kulia → kubadili wimbo (next/previous track)
- Sauti (voice feedback) inayosema "Volume imeongezwa"
