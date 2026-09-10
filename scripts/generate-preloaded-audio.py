#!/usr/bin/env python3
"""Generate ~3-minute all-ages TTS WAV demos for voiceFaithfulness preloads.

Uses macOS `say` + `afconvert`. Run from apps/voiceFaithfulness:
  python3 scripts/generate-preloaded-audio.py
"""

from __future__ import annotations

import json
import subprocess
import tempfile
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "preloaded"
MANIFEST = OUT / "manifest.json"
RATE = 16000
# No trailing silence pad; natural spoken length should land near ~3 minutes.

# Natural US English voices available on recent macOS.
VOICE_A = "Flo"
VOICE_B = "Eddy"


def silence_frames(seconds: float) -> bytes:
    n = int(RATE * seconds)
    return b"\x00\x00" * n


def say_to_wav(text: str, voice: str, dest: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        aiff = Path(tmp) / "clip.aiff"
        subprocess.run(
            ["say", "-v", voice, "-r", "165", "-o", str(aiff), text],
            check=True,
        )
        subprocess.run(
            [
                "afconvert",
                "-f",
                "WAVE",
                "-d",
                f"LEI16@{RATE}",
                "-c",
                "1",
                str(aiff),
                str(dest),
            ],
            check=True,
        )


def concat_wavs(parts: list[Path], dest: Path) -> float:
    frames = bytearray()
    for i, part in enumerate(parts):
        with wave.open(str(part), "rb") as w:
            assert w.getnchannels() == 1
            assert w.getsampwidth() == 2
            assert w.getframerate() == RATE
            frames.extend(w.readframes(w.getnframes()))
        if i < len(parts) - 1:
            frames.extend(silence_frames(0.55))
    with wave.open(str(dest), "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(RATE)
        out.writeframes(bytes(frames))
    return len(frames) / (RATE * 2)


# All-ages dialogue turns: (voice, text). ~400–500 words total per recording.
RECORDINGS: list[dict] = [
    {
        "id": "preload-01",
        "title": "A walk in the park",
        "turns": [
            (VOICE_A, "Good morning. Thanks for meeting me at the park. The air feels cooler today, and the trees along this path still have a lot of green leaves."),
            (VOICE_B, "I am glad we came early. Look at how many birds are hopping near the fountain. I brought a small notebook so we can list interesting things we notice without using our phones."),
            (VOICE_A, "That is a nice idea. I see a family flying a kite near the open field. The kite is shaped like a fish and the kids are taking turns holding the string. Everyone seems patient and cheerful."),
            (VOICE_B, "Over by the benches, two people are sharing tea from a thermos. A dog on a leash is sitting quietly while its owner ties a shoe. The path is wide enough for strollers and bikes if everyone stays aware."),
            (VOICE_A, "Let us walk toward the pond. The water looks calm. There are ducks floating near the reeds, and someone is reading on a blanket under a willow tree. I like how quiet it feels even though the city is close."),
            (VOICE_B, "I notice a gardener watering young plants beside the playground. The playground has soft ground and clear signs about sharing the swings. A teacher is counting students before they leave for the bus."),
            (VOICE_A, "Should we sit for a minute on this hill? From here we can see the whole loop trail. I am grateful for shade, water fountains, and trash cans that make it easy to keep the park clean."),
            (VOICE_B, "Yes. Before we go, let us pick up any litter we find near our spot and thank the park staff if we see them. Small habits keep places welcoming for everyone who visits after us."),
            (VOICE_A, "Agreed. Next weekend we could bring a simple picnic and invite a neighbor. For now, this slow walk was enough. My favorite moment was the kite and the calm pond."),
            (VOICE_B, "Mine was the notebook idea and watching the ducks. Ready to head back? We can stop for fruit on the way home and plan another outdoor morning soon."),
        ],
    },
    {
        "id": "preload-02",
        "title": "How plants grow",
        "turns": [
            (VOICE_A, "Today we are learning how plants grow from a seed. A seed is a tiny package with a baby plant inside and food to help it start. When it gets water, warmth, and air, it can wake up."),
            (VOICE_B, "First the seed softens. A root grows downward to drink water and hold the plant in soil. Then a shoot grows upward toward light. That early stage is called germination."),
            (VOICE_A, "Leaves help the plant make food using sunlight, water, and carbon dioxide. This is photosynthesis. The plant builds sugars that become stems, more leaves, flowers, and sometimes fruit."),
            (VOICE_B, "Roots also take minerals from soil. Healthy soil has tiny organisms that recycle old leaves. Gardeners add compost so plants get a balanced meal without harsh chemicals."),
            (VOICE_A, "Different plants need different care. A cactus stores water and likes dry soil. Lettuce likes cooler weather and regular moisture. Reading a seed packet helps you choose the right place."),
            (VOICE_B, "Pollination matters too. Bees, butterflies, wind, and people can move pollen so flowers make seeds. Without pollinators, many fruits and vegetables would be harder to grow."),
            (VOICE_A, "If we plant beans in a cup with paper towels, we can watch roots and shoots for a week. We should keep the towel damp, not soaking, and place the cup near a bright window."),
            (VOICE_B, "Measuring growth each day teaches patience. Plants do not rush, yet they change in clear steps. That is a good lesson for school projects and for life."),
            (VOICE_A, "When our bean is taller, we can move it into a pot with soil. Support the stem gently. Water at the base and avoid soaking the leaves late at night."),
            (VOICE_B, "To summarize: seed, root, shoot, leaves, food from light, and care that matches the plant. If we remember those ideas, we can grow something kind and useful at home."),
        ],
    },
    {
        "id": "preload-03",
        "title": "Library story hour",
        "turns": [
            (VOICE_A, "Welcome to story hour. Please find a seat on the rug. Today we will hear a short tale about a lighthouse keeper who shares books with visiting sailors."),
            (VOICE_B, "Before we begin, remember library manners: soft voices, gentle hands with books, and waiting for your turn to speak. If you need to leave, walk quietly so others can listen."),
            (VOICE_A, "In our story, the keeper lights the lamp every evening. One stormy night, a young sailor arrives wet and tired. The keeper offers dry socks, warm soup, and a stack of adventure books."),
            (VOICE_B, "The sailor reads aloud about islands and maps. The keeper listens and then shows a journal of weather notes. They trade ideas about courage, kindness, and learning from mistakes."),
            (VOICE_A, "After the storm, the sailor returns the books carefully. He promises to bring a new story from the next harbor. The keeper smiles because sharing knowledge made the night less lonely."),
            (VOICE_B, "Now let us talk about the story. What did the characters do that was helpful? How did reading change their evening? Raise your hand if you want to share one idea."),
            (VOICE_A, "Great answers. Kindness and curiosity worked together. Libraries are like that lighthouse: a steady place with light for anyone who needs information or comfort."),
            (VOICE_B, "Before you go, choose one book from the display table. You may borrow it with your library card. Ask a librarian if you want recommendations about friendship, science, or art."),
            (VOICE_A, "Thank you for listening so well. Next week we will explore poems about rivers. Bring a favorite word to share if you like. Enjoy your books and return them on time."),
            (VOICE_B, "Story hour is finished. Please push in chairs, say goodbye, and walk to the checkout desk. We are glad you visited the library today."),
        ],
    },
    {
        "id": "preload-04",
        "title": "Cooking a simple soup",
        "turns": [
            (VOICE_A, "Let us make a simple vegetable soup. Wash your hands first. We will use carrots, celery, onion, potatoes, broth, a little oil, salt, and herbs."),
            (VOICE_B, "I will chop the vegetables into similar sizes so they cook evenly. Keep fingers tucked when using a knife, or ask an adult for help if you are still learning."),
            (VOICE_A, "Warm the pot on medium heat with a spoon of oil. Add onion, carrot, and celery. Stir until they smell sweet and soft. This builds flavor without rushing."),
            (VOICE_B, "Add potatoes and broth. Bring the soup to a gentle simmer. Skim any foam. Add thyme or parsley. Taste carefully after it cools on a spoon."),
            (VOICE_A, "While it cooks, set the table and pour water. Cooking is easier when cleanup tools are ready: a towel, a compost bowl for peels, and a place for the lid."),
            (VOICE_B, "After twenty minutes, check whether the potatoes are tender. If yes, turn off the heat. We can mash a few pieces to thicken the soup naturally."),
            (VOICE_A, "Serve in bowls and let it cool enough to eat safely. Fresh bread on the side is optional. Leftovers go in labeled containers in the fridge."),
            (VOICE_B, "What did we practice? Planning ingredients, safe knife habits, patient simmering, tasting thoughtfully, and sharing a meal. That is a complete kitchen lesson."),
            (VOICE_A, "Next time we could add beans or corn. Changing one ingredient teaches flexibility. Cooking does not have to be fancy to be nourishing."),
            (VOICE_B, "Agreed. Thank you for helping. The kitchen is clean, the soup smells wonderful, and we cooked as a team."),
        ],
    },
    {
        "id": "preload-05",
        "title": "Weather and seasons",
        "turns": [
            (VOICE_A, "Weather is what happens outside today. Seasons are longer patterns through the year. Both affect clothes, travel, farming, and outdoor plans."),
            (VOICE_B, "In spring, days warm and plants wake up. Summer often brings longer light and more heat. Autumn cools and many leaves change color. Winter can be cold with shorter days."),
            (VOICE_A, "Clouds form when moist air rises and cools. Rain falls when droplets grow heavy. Snow forms when the air is cold enough. Wind is air moving from high to low pressure."),
            (VOICE_B, "A forecast uses measurements and models to estimate what may happen next. It is not a promise, so we prepare with layers, water, and backup indoor activities."),
            (VOICE_A, "Severe weather needs extra care. During thunder, go indoors and avoid tall isolated trees. In heavy snow, give snowplows room and check on neighbors who may need help."),
            (VOICE_B, "Keeping a simple journal helps. Write the date, temperature, sky condition, and one observation. Over months you will see patterns that match the seasons."),
            (VOICE_A, "Farmers and gardeners use seasons to decide planting times. Cities plan festivals and school calendars around weather too. Understanding seasons builds community awareness."),
            (VOICE_B, "Today looks partly cloudy and mild. That is good for a short walk if we bring a light jacket. Tomorrow might be wetter, so we will pack an umbrella."),
            (VOICE_A, "Remember: observe, prepare, and stay curious. Weather science connects math, geography, and everyday choices."),
            (VOICE_B, "Yes. Let us check the forecast together each morning this week and compare it with what we actually see. That is practical learning."),
        ],
    },
    {
        "id": "preload-06",
        "title": "Making friends at school",
        "turns": [
            (VOICE_A, "Starting at a new school can feel big. A good first step is a friendly hello and your name. You do not need a perfect speech."),
            (VOICE_B, "Look for group activities where joining is welcome: library club, art table, or a class project. Shared tasks make conversation easier than standing alone."),
            (VOICE_A, "Listening well is a friendship skill. Ask a question about someone else's interests, then wait for the answer. People feel respected when they are heard."),
            (VOICE_B, "If you disagree, keep your words kind. You can say you see it differently and still be teammates. Respect builds trust faster than winning an argument."),
            (VOICE_A, "Include others who seem left out. Invite someone to sit with you at lunch. Small invitations matter more than big performances."),
            (VOICE_B, "Online spaces at school should follow the same values: no rumors, no mean jokes about appearance, and tell a trusted adult if someone is unsafe."),
            (VOICE_A, "Friendship takes time. Not every classmate will be a close friend, and that is okay. Aim for courtesy with everyone and deeper connection with a few."),
            (VOICE_B, "When you make a mistake, apologize clearly and repair what you can. Saying sorry without excuses shows maturity."),
            (VOICE_A, "Celebrate others' successes. Cheering for a classmate's presentation or goal makes the whole room safer for trying."),
            (VOICE_B, "To sum up: greet, listen, include, respect, and repair. Those habits help friendships grow in a healthy way."),
        ],
    },
    {
        "id": "preload-07",
        "title": "Pets and kindness",
        "turns": [
            (VOICE_A, "Pets depend on us for food, water, shelter, exercise, and gentle handling. Kindness to animals is part of being a responsible caregiver."),
            (VOICE_B, "Before adopting, learn what a pet needs. A dog may need daily walks. A cat needs a clean litter box. Fish need the right water temperature."),
            (VOICE_A, "Speak softly near animals. Sudden loud noises can scare them. Ask the owner before petting, and let the animal approach if it wants contact."),
            (VOICE_B, "Children can help with age-appropriate chores: filling water bowls, brushing with supervision, or reading near a calm pet for quiet company."),
            (VOICE_A, "Veterinary visits keep pets healthy. Vaccines, checkups, and parasite prevention are acts of care, not extras."),
            (VOICE_B, "Never tease an animal with food or touch. If a pet growls or hides, give space and tell an adult. Safety protects both people and animals."),
            (VOICE_A, "Wildlife is different from pets. Enjoy birds and squirrels from a distance. Do not feed wild animals human snacks that can harm them."),
            (VOICE_B, "If you cannot keep a pet, talk with family about fostering, volunteering at a shelter, or supporting rescue groups with supplies."),
            (VOICE_A, "Kindness includes patience during training. Reward good behavior and keep sessions short and positive."),
            (VOICE_B, "Animals remind us to slow down and notice needs beyond our own. That empathy often spills into how we treat people too."),
        ],
    },
    {
        "id": "preload-08",
        "title": "Recycling at home",
        "turns": [
            (VOICE_A, "Recycling works best when we sort correctly. Clean bottles, cans, and paper usually belong in recycling. Food-soiled items often do not."),
            (VOICE_B, "Check your local rules. Some places accept certain plastics only. When unsure, rinse the item and look at the number on the bottom or the city website."),
            (VOICE_A, "Reduce and reuse come first. A refillable bottle prevents waste before recycling is needed. Cloth bags replace many disposable ones."),
            (VOICE_B, "Set up simple bins at home: landfill, recycling, and compost if available. Labels help everyone in the household participate."),
            (VOICE_A, "Flatten cardboard to save space. Keep batteries and electronics out of regular bins; many stores offer special drop-off."),
            (VOICE_B, "Contamination is a common problem. One greasy pizza box can spoil a load. When in doubt, ask rather than wish it away."),
            (VOICE_A, "School projects can measure how much recycling your class collects in a month. Graphs make the effort visible and motivating."),
            (VOICE_B, "Remember why we recycle: to save energy, reduce mining and logging pressure, and keep neighborhoods cleaner."),
            (VOICE_A, "Today let us rinse jars after breakfast and place them in the right bin. Small routines beat occasional big cleanups."),
            (VOICE_B, "Yes. Recycling is a team habit. When we do it carefully, we turn everyday trash into resources again."),
        ],
    },
    {
        "id": "preload-09",
        "title": "Music practice tips",
        "turns": [
            (VOICE_A, "Effective music practice is short, focused, and regular. Fifteen mindful minutes can beat one distracted hour."),
            (VOICE_B, "Start with a warm-up: slow scales or easy patterns. Prepare your hands, breath, or voice before hard passages."),
            (VOICE_A, "Break a difficult measure into tiny pieces. Play it slowly with a metronome, then increase speed only when it feels steady."),
            (VOICE_B, "Record yourself sometimes. Listening back reveals timing and tone better than guessing while you play."),
            (VOICE_A, "Rest briefly between repetitions. Muscles and attention need recovery. Stretch your shoulders and shake out tension."),
            (VOICE_B, "Set one clear goal per session, such as cleaner rhythm in the chorus. Finishing a goal feels better than wandering."),
            (VOICE_A, "Be kind to yourself when you miss notes. Mistakes are information. Mark the spot and return with a plan."),
            (VOICE_B, "Practice performing for family in a friendly living-room concert. Sharing music builds confidence for school events."),
            (VOICE_A, "Care for your instrument: clean it, store it safely, and tell a teacher if something feels broken."),
            (VOICE_B, "Music is a language of patience. Steady practice turns effort into expression that others can enjoy."),
        ],
    },
    {
        "id": "preload-10",
        "title": "Visiting a museum",
        "turns": [
            (VOICE_A, "A museum visit is more fun with a plan. Pick two galleries so you are not exhausted, and leave time to sit and sketch or jot notes."),
            (VOICE_B, "Read labels without rushing. Ask what materials were used and why the artist or scientist might have chosen them."),
            (VOICE_A, "Use indoor voices and keep a safe distance from displays. Flash photography may be restricted to protect artwork."),
            (VOICE_B, "If a docent offers a short tour, join in. Questions like how and why open richer conversations than yes or no."),
            (VOICE_A, "Children can play I-spy with colors and shapes. Adults can connect exhibits to books or places you already know."),
            (VOICE_B, "Museum shops and cafes are optional. The main treasure is looking closely and remembering one idea to tell someone later."),
            (VOICE_A, "Accessibility matters. Ask staff about elevators, quiet rooms, or large-print guides if anyone in your group needs them."),
            (VOICE_B, "Afterward, share favorite exhibits on the ride home. Drawing a postcard of one object helps memory stick."),
            (VOICE_A, "Museums preserve stories from many cultures and times. Visiting with respect means listening even when ideas are new."),
            (VOICE_B, "Let us choose the natural history hall and the community quilt exhibit today. Ready when you are."),
        ],
    },
]


def extend_turns(title: str, turns: list) -> list:
    """Add a short recap so spoken length approaches ~3 minutes."""
    extra = [
        (
            VOICE_A,
            f"Before we finish our conversation about {title.lower()}, let us name two takeaways we can use tomorrow. "
            "First, stay curious and notice details. Second, treat people and places with care.",
        ),
        (
            VOICE_B,
            "I also want to practice explaining this topic in my own words. Teaching a friend is a strong way to learn. "
            "If I forget a step, I can look at notes or ask a clear question.",
        ),
        (
            VOICE_A,
            "We should schedule a little review later this week. Ten focused minutes is enough. "
            "Consistency beats cramming, whether we are studying nature, cooking, music, or friendship skills.",
        ),
        (
            VOICE_B,
            f"Thank you for talking through {title.lower()} with me. I feel more prepared and calm. "
            "Let us end here, tidy our space, and carry one kind action into the rest of the day.",
        ),
        (
            VOICE_A,
            "One more thought: good learning is shared. If someone nearby is confused, we can offer help without judgment. "
            "That keeps classrooms, kitchens, parks, and libraries welcoming for everyone.",
        ),
        (
            VOICE_B,
            "Agreed. I am ready to stop recording this practice conversation. The ideas were clear, the pace was steady, "
            "and the examples stayed appropriate for all ages.",
        ),
    ]
    return list(turns) + extra


for _rec in RECORDINGS:
    _rec["turns"] = extend_turns(_rec["title"], _rec["turns"])


def build_one(rec: dict) -> float:
    out_wav = OUT / f"{rec['id']}.wav"
    with tempfile.TemporaryDirectory() as tmp:
        parts: list[Path] = []
        for i, (voice, text) in enumerate(rec["turns"]):
            part = Path(tmp) / f"turn-{i:02d}.wav"
            say_to_wav(text, voice, part)
            parts.append(part)
        duration = concat_wavs(parts, out_wav)
    print(f"wrote {out_wav.name} ({duration:.1f}s)")
    return duration


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    durations: dict[str, int] = {}
    for rec in RECORDINGS:
        durations[rec["id"]] = int(round(build_one(rec)))

    # Keep blocked demo pointing at audible content but ineligible by policy.
    blocked_src = OUT / "preload-01.wav"
    blocked_dst = OUT / "preload-blocked.wav"
    blocked_dst.write_bytes(blocked_src.read_bytes())

    manifest = {
        "recordings": [
            {
                "id": rec["id"],
                "title": rec["title"],
                "source_type": "preloaded",
                "audio_path": f"data/preloaded/{rec['id']}.wav",
                "duration_seconds": durations[rec["id"]],
                "all_ages_eligible": True,
            }
            for rec in RECORDINGS
        ]
        + [
            {
                "id": "preload-blocked",
                "title": "[Blocked demo] Bad data sample — will fail",
                "source_type": "preloaded",
                "audio_path": "data/preloaded/preload-blocked.wav",
                "duration_seconds": durations["preload-01"],
                "all_ages_eligible": False,
                "demo_fail": True,
            }
        ]
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"updated {MANIFEST}")


if __name__ == "__main__":
    main()
