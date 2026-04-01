#!/usr/bin/env python3
"""
Bluesky auto-poster for Luna Bolt.
Publishes one post per run from the content queue.
Run daily via: python3 bluesky_autoposter.py
"""

import json
from pathlib import Path
from atproto import Client

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR.parent / ".env"
STATE_FILE = BASE_DIR / "bluesky_state.json"

QUIZ_URL = "yantahari.github.io/choose-your-own-self-help/"
QUIZ_URL_ES = "yantahari.github.io/choose-your-own-self-help/es.html"

# Load credentials
def load_env():
    creds = {}
    with open(ENV_PATH) as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                creds[k] = v
    return creds

# Post queue (alternates EN and ES)
POSTS = [
    # Week 1
    f"Need self-help to choose your self-help? 🔮\n\n16 alternative therapies. Humor. Science. A Woo-Woo Meter.\n\nTake the free quiz:\n{QUIZ_URL}\n\n#selfhelp #humor #books",

    f"Magufómetro: la escala definitiva.\n\n1/5 — La ciencia asiente.\n3/5 — La ciencia se rasca la cabeza.\n5/5 — La ciencia se ha ido a tomar un café.\n\nHaz el test:\n{QUIZ_URL_ES}\n\n#terapiasalternativas #humor",

    f"\"Meditation isn't about clearing your mind. It's about catching it when it wanders off and dragging it back. Like walking a hyperactive dog.\"\n\n— Choose Your Own Self-Help\n\n#mindfulness #meditation #humor",

    f"\"Es como si alguien tirara una aspirina al Atlántico, recogiera un vaso de agua en la playa y te dijera: esto te quita el dolor de cabeza.\"\n\nHomeopatía: 4/5 en el Magufómetro.\n\n#homeopatía #humor",

    f"What brings you to the cosmic consultation room?\n\nA) Stress\nB) Emotional mess\nC) Physical problem\nD) I want MORE\n\nDiscover your therapy:\n{QUIZ_URL}\n\n#quiz #selfhelp",

    f"No puedo tomar decisiones esta semana porque Mercurio está retrógrado.\n\nTampoco la semana pasada porque la Luna estaba en Escorpio.\n\nBásicamente, el universo no quiere que haga nada.\n\n#astrología #humor",

    f"WOO-WOO BINGO: How many therapies have you tried?\n\n0 = Immaculate Skeptic\n1-4 = Curious Dabbler\n5-8 = Spiritual Explorer\n9-12 = Grand Wooster\n13-16 = Ascended Master\n\nYour level?\n\n#WooWooBingo",

    # Week 2
    f"A quantum coach told me my particles were misaligned. I asked for my quantum physicist's number but he didn't have one.\n\n#coaching #humor #quantum",

    f"\"Tengo ansiedad.\" Haz yoga.\n\"Me duele la espalda.\" Haz yoga.\n\"Se me ha roto el coche.\" Haz yoga.\n\"Estoy en un incendio.\" Haz yoga, pero rápido.\n\n#yoga #humor",

    f"ABUNDANCE: The natural state of the universe that is always about to arrive but never quite does. Like the plumber.\n\nFrom the Irreverent Glossary.\n\n#glossary #abundance #humor",

    f"SOLTAR: Dejar de agarrarte a algo que te hace daño. Suena simple, pero hay cursos de 500€ para aprender a hacerlo.\n\nLa ironía de pagar para soltar es un koan zen.\n\n#soltar #humor",

    f"COMFORT ZONE: The place where you're comfortable. Self-help insists you leave it.\n\nCuriously, the comfort zone of self-help gurus includes yachts and conferences in Bali.\n\n#comfortzone #humor",

    f"Llevo tres semanas visualizando un Porsche. Solo ha llegado el recibo de la luz.\n\nEl envío cósmico debe ser lento.\n\n#leydelatracción #manifestación #humor",

    f"Reiki is the only therapy where someone treats you without touching you, remotely, without you knowing.\n\nIt's the spam of the spiritual world: energy you didn't subscribe to.\n\n#reiki #humor",

    # Week 3
    f"If crystals heal, are mountains hospitals? Are mines pharmacies? Are jewelers doctors?\n\nAnd if I swallow a diamond, do I become immortal?\n\n(Don't try it.)\n\n#crystals #humor",

    f"¿Te duele la rodilla? No te arrodillas ante la vida.\n¿Alergia? Tu cuerpo rechaza algo simbólicamente.\n¿Golpe en el meñique? La mesita estaba ahí.\n\n#biodescodificación #humor",

    f"FLOW: Doing nothing and pretending it's a spiritual decision.\n\n#flow #glossary #humor",

    f"Akashic Records: cosmic Google without ads.\n\nYou search 'why is my love life a mess' and it says you were a Tibetan monk in a past life.\n\nThat explains everything. Or nothing.\n\n#akashicrecords #humor",

    f"YO SUPERIOR: La versión mejorada de ti que vive en un plano espiritual elevado.\n\nComo tú, pero sin ansiedad, sin deudas y sin adicción al móvil.\n\nBásicamente, tu versión de LinkedIn.\n\n#humor",

    f"16 therapies. 1 quiz. Infinite excuses.\n\nFind YOUR therapy match:\n{QUIZ_URL}\n\n#ChooseYourOwnSelfHelp #WooWooBingo",

    # Week 4
    f"\"Lo siento, perdóname, gracias, te amo.\"\n\nLo digo al levantarme, al acostarme y cuando mi jefe me pide un informe para ayer.\n\nAún no funciona con Hacienda.\n\n#hooponopono #humor",

    f"According to NLP, if you look up-left you're remembering, up-right you're lying.\n\nTry it on your partner when they explain why they were late.\n\nResults not guaranteed.\n\n#NLP #humor",

    f"Bach Flowers: choosing an emotional Pokémon, herbal shop edition.\n\n\"I choose you, Rescue Remedy!\"\n\n38 identical bottles. 38 ways of falling apart. 1 bottle of brandy disguised as medicine.\n\n#bachflowers #humor",

    f"Complete the sentence:\n\n\"I can't _____ because Mercury is retrograde.\"\n\nBest answers go in the next book 📚\n\n#mercuryretrograde #humor",

    f"Mi vecina hizo Feng Shui: el baño estaba en la \"zona de la riqueza\".\n\nSolución: cerrar siempre la tapa del váter.\n\nAhora cierra la tapa por motivos financieros.\n\n#fengshui #humor",

    f"MERCURY RETROGRADE: A real astronomical phenomenon turned into the universal excuse for everything going wrong.\n\nCorrelation ≠ causation. But it does = many memes.\n\n#mercuryretrograde #humor",

    f"Constelaciones Familiares: la única terapia en la que desconocidos actúan de tus parientes y lo hacen mejor que los originales.\n\n#constelaciones #humor",

    f"ENERGY: The most used and least understood word in alternative vocabulary.\n\nIn physics: precise definition.\nIn self-help: anything you feel and can't explain.\n\n#energy #humor",

    f"¿Ya has hecho el test? 16 terapias te esperan.\n\nDesde mindfulness (1/5) hasta Registros Akáshicos (5/5 full magufada).\n\nTest gratis:\n{QUIZ_URL_ES}\n\n#EligeTuPropiaAutoayuda",

    f"Have you taken the quiz yet?\n\nFrom mindfulness (1/5 on the Woo-Woo Meter) to Akashic Records (5/5 full woo).\n\nFree quiz:\n{QUIZ_URL}\n\n#ChooseYourOwnSelfHelp #books",
]


def main():
    creds = load_env()

    # Load state
    if STATE_FILE.exists():
        state = json.loads(STATE_FILE.read_text())
    else:
        state = {"next_index": 0, "posted": []}

    idx = state["next_index"]
    if idx >= len(POSTS):
        print("All posts published! Queue exhausted.")
        return

    # Login and post
    client = Client()
    client.login(creds["BLUESKY_HANDLE"], creds["BLUESKY_APP_PASSWORD"])

    text = POSTS[idx]
    post = client.send_post(text=text)
    print(f"Post {idx+1}/{len(POSTS)} published: {post.uri}")
    print(f"Text: {text[:80]}...")

    # Update state
    state["next_index"] = idx + 1
    state["posted"].append({"index": idx, "uri": post.uri})
    STATE_FILE.write_text(json.dumps(state, indent=2))


if __name__ == "__main__":
    main()
