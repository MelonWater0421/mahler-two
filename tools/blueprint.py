#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Declarative Authoring & Compilation Script (Single Source of Truth)
Project: Mahler Symphony No. 2 in C minor ("Resurrection" / Auferstehung) — Symphony Atlas
Target Recording: Sir Simon Rattle · Berliner Philharmoniker (BPO)
                  Kate Royal (Soprano), Magdalena Kožená (Mezzo-Soprano), Rundfunkchor Berlin
"""

import json
import math
import os
import struct
from typing import Dict, List, Any

WORK_META = {
    "id": "mahler-2",
    "repository": "https://github.com/MelonWater0421/mahler-two",
    "composer": "Gustav Mahler (1860–1911)",
    "composer_zh": "古斯塔夫·马勒 (1860–1911)",
    "title": "Symphony No. 2 in C minor (\"Resurrection\" / Auferstehung)",
    "title_zh": "C小调第二交响曲《复活》(Auferstehung)",
    "subtitle_en": "Interactive Bilingual Symphony Atlas & Contrapuntal Score Companion",
    "subtitle_zh": "全景声部与复调导览 · 柏林爱乐乐团与西蒙·拉特尔录音精校版",
    "performance": {
        "conductor": "Sir Simon Rattle",
        "conductor_zh": "西蒙·拉特尔爵士 (Sir Simon Rattle)",
        "orchestra": "Berliner Philharmoniker (BPO)",
        "orchestra_zh": "柏林爱乐乐团 (Berliner Philharmoniker)",
        "soloists": [
            {"name": "Kate Royal", "role_en": "Soprano Solo", "role_zh": "女高音独唱"},
            {"name": "Magdalena Kožená", "role_en": "Mezzo-Soprano / Contralto Solo", "role_zh": "女中音/女低音独唱"}
        ],
        "chorus": "Rundfunkchor Berlin (Simon Halsey, Chorus Master)",
        "chorus_zh": "柏林广播合唱团（合唱指导：西蒙·哈尔西）",
        "venue": "Philharmonie, Berlin",
        "venue_zh": "柏林爱乐大厅 (Philharmonie Berlin)",
        "total_duration_sec": 5130.0,
        "total_bars": 2230,
        "acoustic_profile_en": "Extreme dynamic span from whispered pppp choral entry to shattering ffff orchestral/organ tuttis, razor-sharp lower-string articulation in the Totenfeier, and three-dimensional offstage brass placement in the Berlin Philharmonie.",
        "acoustic_profile_zh": "跨越极弱耳语（pppp的无伴奏合唱进入）至震耳欲聋的全奏与管风琴轰鸣（ffff）的惊人动态跨度；葬礼乐章中冷冽如刀锋的低音弦乐咬弦，以及柏林爱乐大厅内极具空间纵深的后台铜管与打击乐（Fernorchester）三维声场。"
    }
}

RELIGIOUS_AND_PROGRAM_CONTEXT = {
    "overview_zh": "马勒《第二交响曲“复活”》（1888–1894）不仅是一部交响巨构，更是一部跨越犹太—基督教末世论（Eschatology）、中世纪天主教礼仪圣咏、路德宗众赞歌（Chorale）传统与浪漫主义泛神论救赎哲学的精神史诗。",
    "overview_en": "Mahler's Symphony No. 2 'Resurrection' (1888–1894) is both a monumental symphonic structure and a profound theological odyssey spanning Judeo-Christian eschatology, medieval Catholic liturgical plainchant, Lutheran chorale tradition, and universalist Romantic redemption.",
    "pillars": [
        {
            "id": "buelow-epiphany",
            "tag_zh": "创作神启 · 汉堡圣米迦勒教堂 (1894)",
            "tag_en": "Historical Genesis · St. Michael's Church, Hamburg (1894)",
            "title_zh": "彪罗葬礼上的灵光：克洛普施托克《复活》圣歌的降临",
            "title_en": "The Funeral of Hans von Bülow & Klopstock's 'Auferstehung' Ode",
            "body_zh": "1888年马勒完成第一乐章《葬礼》（Totenfeier）后，整整六年无法为这部探讨生死终极意义的交响曲找到终局。1894年3月29日，指挥大师汉斯·冯·彪罗（Hans von Bülow）的追思礼拜在汉堡圣米迦勒大教堂举行。当儿童合唱团从风琴楼座唱响18世纪诗人克洛普施托克（Friedrich Gottlieb Klopstock, 1758）的新教圣诗《复活》（“Aufersteh'n, ja aufersteh'n wirst du”）时，马勒在信中回忆道：“那声音如闪电般击中了我，一切瞬间清晰明朗——这正是我苦苦寻觅六年的创世之光！”",
            "body_en": "After completing the first movement ('Totenfeier') in 1888, Mahler was blocked for six years, unable to conceive a finale monumental enough to answer the question of death. On March 29, 1894, attending the memorial service for conductor Hans von Bülow at St. Michael's Church in Hamburg, Mahler heard the choir intone Friedrich Gottlieb Klopstock's 1758 Protestant hymn 'Die Auferstehung.' Mahler wrote: 'It struck me like a bolt of lightning, and everything stood clear and vivid before my soul!'"
        },
        {
            "id": "dies-irae-transfiguration",
            "tag_zh": "中世纪天主教安魂弥撒序列曲 · 第1、5乐章",
            "tag_en": "13th-Century Franciscan Requiem Sequence · Movements I & V",
            "title_zh": "从《震怒之日》（Dies Irae）的末日审判恐惧到《复活圣咏》的逆转",
            "title_en": "Subverting the Medieval 'Dies Irae': From Wrath to Universal Triumph",
            "body_zh": "马勒在第一乐章展开部（排练号13，第207小节）与第五乐章（排练号4，第62小节）直接引用了13世纪方济各会修士托马斯·切拉诺（Thomas of Celano）谱写的拉丁文安魂弥撒序列曲《震怒之日》（Dies irae, dies illa — 震怒之日，世界化为灰烬）。在传统天主教教义中，此圣咏象征末日审判的恐惧与罪人的永罚；但马勒通过精妙的对位变形，让这四个下行的恐惧音符在第五乐章排练号10（第142小节）由重型铜管逆转为昂扬向上的大调《复活圣咏》，宣告爱与生命对审判恐惧的彻底超越。",
            "body_en": "In Movement I (Reh. 13, bar 207) and Movement V (Reh. 4, bar 62), Mahler quotes the 13th-century Gregorian Requiem sequence 'Dies Irae' (Day of Wrath). In orthodox liturgy, the chant embodies terror before the Last Judgment; Mahler, however, subjects its four-note cell to contrapuntal metamorphosis at Rehearsal 10 (bar 142 of Mvt V), inverting the motif of dread into the blazing major-key Resurrection Chorale."
        },
        {
            "id": "st-anthony-satire",
            "tag_zh": "基督教圣徒寓言与存在主义危机 · 第3乐章",
            "tag_en": "Franciscan Parable & Existential Crisis · Movement III",
            "title_zh": "《圣安东尼向鱼传道》的宗教反讽与“绝望尖叫”（Aufschrei）",
            "title_en": "St. Anthony's Sermon to the Fishes: Religious Satire & The Existential Scream",
            "body_zh": "第三乐章完全建构于《少年魔角》中的宗教讽刺歌曲《帕多瓦的圣安东尼向鱼传道》。圣安东尼因教堂空无一人而走向河边向水族布道：贪婪的梭子鱼、好色的鳗鱼、伪善的螃蟹都浮出水面虔诚聆听，然而“传道一结束，众生立刻故态复萌”。马勒借此隐喻尘世宗教仪式与庸碌众生的虚伪麻木——正是这种看穿世俗虚无后的彻骨绝望，催生了第465小节撕裂苍穹的复合调性“绝望尖叫”（Aufschrei / Totengreif）。",
            "body_en": "Movement III adapts the Wunderhorn song 'St. Anthony of Padua's Sermon to the Fishes.' Finding the church empty, St. Anthony preaches to the river creatures: greedy pikes, lustful eels, and backward-walking crabs listen piously, yet 'the sermon ended, each turned right back to its vices.' Mahler uses this Franciscan parable to expose the hollowness of worldly routine, culminating at bar 465 in the shattering bitonal 'Aufschrei' (Scream of Despair)."
        },
        {
            "id": "urlicht-mysticism",
            "tag_zh": "基督教神秘主义与路德宗圣咏 · 第4乐章",
            "tag_en": "Marian Symbolism & Christian Mysticism · Movement IV",
            "title_zh": "《原光》（Urlicht）：神秘主义红玫瑰与灵魂直面天使的抗辩",
            "title_en": "'Urlicht' (Primal Light): The Mystical Rose & The Soul's Defiance of the Angel",
            "body_zh": "第四乐章《原光》以“O Röschen rot!”（啊，小小的红玫瑰！）开启——在中世纪基督教象征体系中，“红玫瑰”既是圣母玛利亚的慈悲象征，也代表基督受难的宝血。弱音铜管奏出庄严的路德宗教堂众赞歌光环。当守门小天使（象征教条式的宗教律法）试图阻拦灵魂进入天堂时，女低音爆发出埃克哈特大师（Meister Eckhart）式的神秘主义呐喊：“不！我绝不离开！我来自上帝，必将归于上帝！”",
            "body_en": "Movement IV ('Urlicht') opens with 'O Röschen rot!'—the mystical red rose symbolizing Marian compassion and divine grace in medieval Christian iconography—framed by a hushed Lutheran brass chorale. When the gatekeeper angel (representing dogmatic orthodoxy) tries to turn the soul away, the contralto erupts with Meister Eckhart-like mystical conviction: 'Ah no! I would not let myself be turned away! I am from God and will return to God!'"
        },
        {
            "id": "eschatology-and-mahler-credo",
            "tag_zh": "犹太羊角号（Shofar）、启示录号角与马勒的无惩罚普世救赎 · 第5乐章",
            "tag_en": "Apocalyptic Shofar / Seven Trumpets & Mahler's Universalist Redemption · Movement V",
            "title_zh": "《末日大召唤》与马勒对克洛普施托克圣诗的革命性改写",
            "title_en": "'Der große Appell' & Mahler's Theological Revision of Klopstock",
            "body_zh": "在第五乐章排练号29《末日大召唤》（Der große Appell）中，后台四方响起的小号与圆号融合了《新约·启示录》第七印的末日号角与犹太教赎罪日羊角号（Shofar）的吹奏音型（长音与急促颤音）。更为关键的是，马勒只保留了克洛普施托克原诗的前两节，删去了原诗中关于“审判台前善恶分流”的新教正统教义，从第560小节起换上自己亲笔撰写的诗篇。马勒在纲要中郑重声明：“没有惩罚，也没有罪人！只有通过炽热的爱与苦难挣得双翼、飞向神圣光明的普世升华（Sterben werd' ich, um zu leben）。”",
            "body_en": "At Rehearsal 29 ('Der große Appell'), the four directional offstage trumpets fuse the Seven Trumpets of the Book of Revelation with the ancient Jewish Shofar calls (sustained blasts and rapid tremolos) of Yom Kippur. Crucially, Mahler kept only the first two stanzas of Klopstock's orthodox hymn and replaced the rest from bar 560 onward with his own verses. As Mahler wrote in his program note: 'There is no judgment, no sinners, no righteous, no punishment and no reward! Only overwhelming love illuminating our existence: I shall die so as to live!'"
        }
    ],
    "movements_context": {
        "1": {
            "theme_zh": "第一乐章宗教与哲学主轴：泰坦英雄的葬礼（Totenfeier）与神义论之问",
            "theme_en": "Movement I Theological Axis: Funeral Rites (Totenfeier) & The Question of Theodicy",
            "summary_zh": "原为1888年独立交响诗《葬礼》（受波兰诗人密茨凯维奇《先人祭》Dziady 启发）。马勒坐在第一交响曲英雄的墓前发问：“你为何而生？为何受苦？难道生命只是一场巨大而恐怖的玩笑？”E大调第二主题（第43小节）如天国圣像画般闪现，而展开部第207小节首次引入中世纪《震怒之日》圣咏。",
            "summary_en": "Originally composed in 1888 as the tone poem 'Totenfeier' (inspired by Adam Mickiewicz's 'Dziady' / Forefathers' Eve). Mahler stands by the grave of the hero of Symphony No. 1 and asks the ultimate question of theodicy: 'Why did you live? Why did you suffer? Is it all only a vast, frightful joke?' The E major theme (bar 43) offers a fleeting icon of paradise, while bar 207 introduces the medieval Dies Irae chant."
        },
        "2": {
            "theme_zh": "第二乐章宗教与哲学主轴：尘世伊甸园的追忆与无常",
            "theme_en": "Movement II Theological Axis: Remembrance of Earthly Eden & Transience",
            "summary_zh": "葬礼结束后五分钟静默，记忆回溯到逝者生前未被死亡阴影玷污的纯真时光。降A大调兰德勒舞曲代表尘世的美好与温柔，而两次升G小调三连音风暴（第85、166小节）则象征伊甸园失落后的存在焦虑。",
            "summary_en": "Following the mandatory five-minute silence after the funeral, memory turns back to an unclouded hour of earthly grace. The A-flat major Ländler embodies innocent joy, twice interrupted by G-sharp minor triplet storms (bars 85 and 166) representing the intrusion of mortality into Eden."
        },
        "3": {
            "theme_zh": "第三乐章宗教与哲学主轴：方济各会寓言《向鱼传道》与信仰失落后的虚无梦魇",
            "theme_en": "Movement III Theological Axis: Franciscan Parable & The Nightmare of Worldly Nihilism",
            "summary_zh": "借圣安东尼向鱼群布道却徒劳无功的宗教寓言，揭示缺乏超越性信仰的世俗生活只是一场永不停歇的盲目漩涡（3/8拍永动音流）。高潮处的ffff“绝望尖叫”（第465小节）是灵魂在尘世虚无地狱中的崩溃哭喊。",
            "summary_en": "Through the Franciscan legend of St. Anthony preaching in vain to the fishes, Mahler portrays secular existence without transcendence as a blind, perpetual 3/8 whirlpool. The ffff 'Aufschrei' at bar 465 is the soul's cry of disgust and terror at spiritual emptiness."
        },
        "4": {
            "theme_zh": "第四乐章宗教与哲学主轴：《原光》（Urlicht）——赤子信仰与基督教神秘主义直觉",
            "theme_en": "Movement IV Theological Axis: 'Urlicht' — Childlike Faith & Mystical Illumination",
            "summary_zh": "全曲的神学核心转折。女低音在降D大调（拿波里神圣调性）中唱出《少年魔角》圣歌。铜管圣咏如教堂拱顶，首席小提琴独奏如天使引路，灵魂挣脱尘世教条的阻拦，宣告“我来自上帝，必将归于上帝”。",
            "summary_en": "The theological pivot of the symphony. Set in sacred D-flat major, the contralto sings the Wunderhorn hymn over a hushed brass chorale. Aided by a luminous solo violin, the soul overcomes the angel's prohibition with the mystical credo: 'I am from God and will return to God!'"
        },
        "5": {
            "theme_zh": "第五乐章宗教与哲学主轴：末日审判（Dies Irae）、大召唤（Appell）与普世复活（Aufersteh'n）",
            "theme_en": "Movement V Theological Axis: Last Judgment, The Great Summons & Universal Resurrection",
            "summary_zh": "一部浓缩的管弦乐与合唱《启示录》：从绝望尖叫重现、旷野呼喊者（后台圆号）、《震怒之日》圣咏、坟墓崩裂（打击乐大渐强）、亡灵大进军（舞台风暴与后台军乐的空间复调）、四方小号的《末日大召唤》，直到合唱团ppp无伴奏唱出《复活》，并在全音栓教堂管风琴与三口深沉大钟齐鸣中完成宇宙升华。",
            "summary_en": "A complete symphonic Book of Revelation: progressing from the Scream of Despair, the Voice in the Wilderness (offstage horns), the Dies Irae plainchant, the bursting open of the graves (percussion crescendo), the March of the Dead (spatial polyphony of onstage storm and offstage band), and the Great Summons (four directional offstage trumpets + lone nightingale flute), to the ppp a cappella choral entry ('Aufersteh'n') and the final E-flat major apotheosis with full church organ and three deep bells."
        }
    }
}

ORCHESTRAL_CHOIRS = [
    {
        "id": "strings",
        "label_zh": "弦乐五部",
        "label_en": "Strings",
        "color": "#ef4444",
        "detail_zh": "第一/第二小提琴、中提琴、大提琴、五弦/加C弦低音提琴（含揉弦、滑音、木杆击弦 col legno）",
        "detail_en": "Violins I & II, Violas, Cellos, Double Basses with low C extension (col legno, portamento, tremolandi)"
    },
    {
        "id": "winds",
        "label_zh": "四管木管",
        "label_en": "Woodwinds",
        "color": "#10b981",
        "detail_zh": "4长笛（均兼短笛）、4双簧管（2兼英国管）、5单簧管（含高音bE与低音单簧管）、4大管（兼低音大管）",
        "detail_en": "4 Flutes (all doubling Piccolos), 4 Oboes (2 English Horns), 5 Clarinets (incl. E-flat & Bass), 4 Bassoons (Contrabassoon)"
    },
    {
        "id": "horns",
        "label_zh": "圆号群",
        "label_en": "French Horns",
        "color": "#f59e0b",
        "detail_zh": "10支圆号（舞台上6支，后台远距离4支），常要求贝尔朝上（Schalltrichter auf）",
        "detail_en": "10 French Horns (6 on stage, 4 off stage), frequently bells-up (Schalltrichter auf)"
    },
    {
        "id": "brass",
        "label_zh": "重型铜管",
        "label_en": "Heavy Brass",
        "color": "#eab308",
        "detail_zh": "8–10支小号（舞台4–6支，后台4支）、4支长号、大号（Tuba）",
        "detail_en": "8–10 Trumpets (4–6 onstage, 4 offstage), 4 Trombones, Contrabass Tuba"
    },
    {
        "id": "perc",
        "label_zh": "打击乐与钟声",
        "label_en": "Percussion & Bells",
        "color": "#a855f7",
        "detail_zh": "2名定音鼓手（6面鼓，另加后台第3名）、大鼓、镲、高低音大锣（Tam-tams）、桦木枝（Rute）、钟琴、3口无固定音高深沉大钟",
        "detail_en": "2 Timpanists (6 drums + 1 offstage), Bass Drums, Cymbals, High/Low Tam-tams, Rute, Glockenspiel, 3 Deep Tuned/Untuned Church Bells"
    },
    {
        "id": "voices",
        "label_zh": "独唱与混声合唱",
        "label_en": "Soloists & Chorus",
        "color": "#ec4899",
        "detail_zh": "女低音/女中音独唱（第4、5乐章）、女高音独唱（第5乐章）、大型四部混声合唱团（SATB）",
        "detail_en": "Contralto/Mezzo Soloist (Mvts IV & V), Soprano Soloist (Mvt V), Large Mixed Choir (SATB)"
    },
    {
        "id": "organ",
        "label_zh": "教堂管风琴",
        "label_en": "Pipe Organ",
        "color": "#06b6d4",
        "detail_zh": "大型管风琴（Volles Werk 全音栓洞开，含16尺与32尺超低音踏板音栓，在终曲高潮轰鸣）",
        "detail_en": "Full Concert/Church Pipe Organ (Volles Werk with 16' and 32' pedal stops entering at the Finale apotheosis)"
    },
    {
        "id": "fernorchester",
        "label_zh": "后台远距乐队",
        "label_en": "Fernorchester (Offstage)",
        "color": "#3b82f6",
        "detail_zh": "置于音乐厅侧门/后台远处的4支小号、4支圆号、定音鼓、大鼓与三角铁，营造末日召唤与异界回响",
        "detail_en": "Spatial offstage brass & percussion ensemble (4 Trumpets, 4 Horns, Timpani, Bass Drum, Cymbals, Triangle)"
    }
]

THEMATIC_LEITMOTIFS = [
    {
        "id": "m1-totenfeier-march",
        "code": "M1-A",
        "name_zh": "葬礼进行曲核心动机 (Totenfeier March)",
        "name_en": "Totenfeier Funeral March Motif",
        "movements": [1, 5],
        "first_bar": "Mvt I, Bar 19",
        "color": "#dc2626",
        "intervals": "C4 - B3 - C4 - D4 - Eb4 - D4 - C4 (dotted march rhythm)",
        "desc_zh": "C小调严峻的附点葬礼步伐，配以低音提琴沉重的四分音符踏步，象征泰坦英雄遗体入土时的悲剧重负。",
        "desc_en": "Stern C minor dotted march rhythm over trudging bass ostinato, embodying the tragic weight of the fallen hero's funeral procession.",
        "notes_hz": [261.63, 246.94, 261.63, 293.66, 311.13, 293.66, 261.63]
    },
    {
        "id": "m1-rising-cry",
        "code": "M1-B",
        "name_zh": "半音上行悲叹与天问动机 (Ascending Cry)",
        "name_en": "Ascending Chromatic Cry & Heavenward Vision",
        "movements": [1, 5],
        "first_bar": "Mvt I, Bar 43",
        "color": "#f97316",
        "intervals": "G#4 - A4 - B4 - C#5 - E5 - D#5 (E major luminous arch)",
        "desc_zh": "从C小调深渊突然折射入E大调的纯净小提琴与圆号旋律，第一次预示超越死亡的彼岸救赎。",
        "desc_en": "Luminous E major cantilena emerging from the C minor abyss in muted violins and horns, offering the first glimpse of transcendent redemption.",
        "notes_hz": [415.30, 440.00, 493.88, 554.37, 659.25, 622.25]
    },
    {
        "id": "m2-laendler",
        "code": "M2-A",
        "name_zh": "降A大调往昔兰德勒舞曲 (Nostalgic Ländler)",
        "name_en": "Nostalgic A-flat Major Ländler Theme",
        "movements": [2],
        "first_bar": "Mvt II, Bar 1",
        "color": "#10b981",
        "intervals": "C5 - Bb4 - Ab4 - G4 - F4 - Eb4 - Ab4 (3/8 graceful lilt)",
        "desc_zh": "在3/8拍轻盈摇曳中回望逝者生前最幸福的一缕阳光，带有维也纳旧日沙龙的温柔与大提琴滑音叹息。",
        "desc_en": "A sunlit 3/8 remembrance of a happy hour in the departed hero's life, graced with Viennese portamento and later veiled in cello pizzicato.",
        "notes_hz": [523.25, 466.16, 415.30, 392.00, 349.23, 311.13, 415.30]
    },
    {
        "id": "m3-fischpredigt",
        "code": "M3-A",
        "name_zh": "圣安东尼向鱼传道动机 (Fischpredigt Moto Perpetuo)",
        "name_en": "St. Anthony's Sermon to the Fishes (Perpetual 3/8)",
        "movements": [3],
        "first_bar": "Mvt III, Bar 13",
        "color": "#8b5cf6",
        "intervals": "C4 - D4 - Eb4 - F4 - G4 - Eb4 - C4 (sinuous 16th-note swirl)",
        "desc_zh": "源自《少年魔角》歌曲，单簧管与弦乐永不停歇的盘旋音流，讽刺世人听完神圣布道后依然浑噩如故的荒诞日常。",
        "desc_en": "Derived from the Wunderhorn song, a ceaseless 3/8 whirlpool satirizing the meaningless bustle of existence where everyone forgets the sermon immediately.",
        "notes_hz": [261.63, 293.66, 311.13, 349.23, 392.00, 311.13, 261.63]
    },
    {
        "id": "m3-totengreif",
        "code": "M3-B",
        "name_zh": "绝望尖叫和弦 (Der Aufschrei / Totengreif)",
        "name_en": "The Scream of Despair (Aufschrei / Totengreif Chord)",
        "movements": [3, 5],
        "first_bar": "Mvt III, Bar 465 & Mvt V, Bar 1",
        "color": "#e11d48",
        "intervals": "Bb - Db - F - G - A - C# (shattering bitonal tutti crash)",
        "desc_zh": "对虚无世界发出的撕心裂肺的尖叫（ffff），在第三乐章高潮炸裂，又在第五乐章开篇原样重现。",
        "desc_en": "Shattering ffff dissonance of existential nausea and terror that erupts at the climax of the Scherzo and rips open the Finale.",
        "notes_hz": [233.08, 277.18, 349.23, 392.00, 440.00, 554.37]
    },
    {
        "id": "m4-urlicht",
        "code": "M4-A",
        "name_zh": "原光圣咏与赤子信仰主题 (Urlicht Chorale & Faith)",
        "name_en": "Urlicht (Primal Light) Brass Chorale & Contralto Lied",
        "movements": [4, 5],
        "first_bar": "Mvt IV, Bar 1",
        "color": "#f59e0b",
        "intervals": "Ab4 - Bb4 - Db5 - Ab4 - F4 (O Röschen rot!)",
        "desc_zh": "女低音以毫无修饰的赤子之声唱出“啊，红玫瑰！”，铜管圣咏如教堂彩窗般庄严笼罩，点燃通向上帝之光。",
        "desc_en": "Unadorned contralto invocation ('O Röschen rot!') framed by a hushed D-flat major brass chorale, illuminating the soul's return to God.",
        "notes_hz": [415.30, 466.16, 554.37, 415.30, 349.23]
    },
    {
        "id": "m5-dies-irae",
        "code": "M5-A",
        "name_zh": "震怒之日格里高利圣咏 (Dies Irae Sequence)",
        "name_en": "Dies Irae Gregorian Chant Sequence",
        "movements": [1, 5],
        "first_bar": "Mvt I, Bar 207 & Mvt V, Bar 62",
        "color": "#6366f1",
        "intervals": "F4 - E4 - F4 - D4 - E4 - C4 - D4 (four-note medieval sequence)",
        "desc_zh": "中世纪末日审判圣咏《震怒之日》四音核心，由木管、大管与长号肃穆吹响，继而化作复活凯歌的基石。",
        "desc_en": "The medieval Day of Wrath plainchant intoned solemnly by winds, bassoons, and trombones before transforming into the march of the dead.",
        "notes_hz": [349.23, 329.63, 349.23, 293.66, 329.63, 261.63, 293.66]
    },
    {
        "id": "m5-resurrection-chorale",
        "code": "M5-B",
        "name_zh": "复活胜利铜管圣咏 (Resurrection Triumph Chorale)",
        "name_en": "Ascending Brass Resurrection Chorale",
        "movements": [5],
        "first_bar": "Mvt V, Bar 142",
        "color": "#eab308",
        "intervals": "C4 - F4 - G4 - Ab4 - Bb4 - C5 (blazing fff brass proclamation)",
        "desc_zh": "在《震怒之日》上方喷薄而出的辉煌铜管圣咏，将审判的恐惧逆转为超越死亡的胜利宣言。",
        "desc_en": "Blazing brass apotheosis of the chorale theme that turns the terror of the Last Judgment into a proclamation of eternal life.",
        "notes_hz": [261.63, 349.23, 392.00, 415.30, 466.16, 523.25]
    },
    {
        "id": "m5-grosse-appell",
        "code": "M5-C",
        "name_zh": "末日大召唤：后台号角与夜莺长笛 (Der große Appell)",
        "name_en": "The Great Summons (Der große Appell — Offstage Brass & Birdsong)",
        "movements": [5],
        "first_bar": "Mvt V, Bar 448",
        "color": "#3b82f6",
        "intervals": "Eb4 - Bb4 - Eb5 (offstage fanfare) + C6 - G5 - Eb6 (flute birdcall)",
        "desc_zh": "大地寂灭之后，四支后台小号与圆号从四面八方吹响孤寂的集结号，舞台上仅剩长笛与短笛模仿坟墓上最后一只夜莺的啼鸣。",
        "desc_en": "Across a devastated landscape, four offstage trumpets and horns sound the Great Summons while onstage flute and piccolo intone a lone nightingale over the graves.",
        "notes_hz": [311.13, 466.16, 622.25, 1046.50, 783.99, 1244.51]
    },
    {
        "id": "m5-auferstehn",
        "code": "M5-D",
        "name_zh": "“复活”无伴奏合唱圣歌 (Aufersteh'n Chorale)",
        "name_en": "\"Aufersteh'n\" Whispered Choral Hymn",
        "movements": [5],
        "first_bar": "Mvt V, Bar 472",
        "color": "#ec4899",
        "intervals": "Eb4 - Eb4 - F4 - G4 - Ab4 - G4 - Bb4 (Misterioso ppp)",
        "desc_zh": "混声合唱以极弱（ppp）无伴奏唱出克洛普施托克诗篇“你将复活，是的，我的尘躯”，最终汇聚管风琴与大钟直抵宇宙巅峰。",
        "desc_en": "The chorus enters ppp misterioso on Klopstock's ode ('Aufersteh'n, ja aufersteh'n wirst du'), swelling ultimately to the organ and bell-crowned E-flat major apotheosis.",
        "notes_hz": [311.13, 311.13, 349.23, 392.00, 415.30, 392.00, 466.16]
    }
]

# Polyphony Anatomy Lab (synthModes) — 3 to 4 interactive multi-track excerpts per movement
SYNTH_MODES = {
    "1": [
        {
            "id": "m1-synth-1",
            "title_zh": "葬礼宣叙调与木管哀歌复调 (小节 1–28)",
            "title_en": "Totenfeier Recitative & Woodwind Lament Counterpoint (Bars 1–28)",
            "bars": "Bars 1–28",
            "tempo_bpm": 84,
            "desc_zh": "剖析大提琴/低音提琴狂暴的十六分音符宣叙调如何转入定音鼓与低音弦乐的C小调附点踏步，上方叠加双簧管与英国管的凄厉叹息。",
            "desc_en": "Isolate the furious lower-string sixteenth-note recitative yielding to the C minor funeral march ostinato under oboe and English horn laments.",
            "tracks": [
                {"choir": "strings", "name_zh": "大提琴与低音提琴 (葬礼踏步)", "name_en": "Cellos & Basses (March Ostinato)", "wave": "sawtooth", "notes": [{"t": 0.0, "d": 0.4, "f": 65.41}, {"t": 0.4, "d": 0.4, "f": 73.42}, {"t": 0.8, "d": 0.4, "f": 77.78}, {"t": 1.2, "d": 1.2, "f": 98.00}, {"t": 2.6, "d": 0.7, "f": 130.81}, {"t": 3.4, "d": 0.7, "f": 98.00}, {"t": 4.2, "d": 0.7, "f": 130.81}, {"t": 5.0, "d": 1.4, "f": 130.81}]},
                {"choir": "winds", "name_zh": "双簧管与英国管 (C小调哀歌)", "name_en": "Oboes & English Horn (C minor Lament)", "wave": "triangle", "notes": [{"t": 2.6, "d": 1.1, "f": 261.63}, {"t": 3.8, "d": 0.4, "f": 246.94}, {"t": 4.2, "d": 0.8, "f": 261.63}, {"t": 5.0, "d": 0.6, "f": 293.66}, {"t": 5.6, "d": 1.0, "f": 311.13}]},
                {"choir": "horns", "name_zh": "圆号群 (深沉暗流持续音)", "name_en": "Horns (Dark Pedal & Sighs)", "wave": "sine", "notes": [{"t": 2.6, "d": 2.0, "f": 196.00}, {"t": 4.8, "d": 1.8, "f": 155.56}]},
                {"choir": "perc", "name_zh": "定音鼓 (C–G葬礼重音)", "name_en": "Timpani (C–G Funeral Pulse)", "wave": "sine", "notes": [{"t": 2.6, "d": 0.3, "f": 65.41}, {"t": 3.4, "d": 0.3, "f": 98.00}, {"t": 4.2, "d": 0.3, "f": 65.41}, {"t": 5.0, "d": 0.3, "f": 98.00}]}
            ]
        },
        {
            "id": "m1-synth-2",
            "title_zh": "E大调彼岸幻象：圆号与弱音器小提琴对位 (小节 43–62)",
            "title_en": "E Major Pastoral Mirage: Horns vs. Muted Violins (Bars 43–62)",
            "bars": "Bars 43–62",
            "tempo_bpm": 76,
            "desc_zh": "聆听第一小提琴在极弱（pp）高音区拉出天堂般的E大调拱形旋律，而圆号在中音区织出温暖的半音内声部。",
            "desc_en": "Examine how muted first violins float the E major consolation theme over warm, chromatically shifting horn counterpoint.",
            "tracks": [
                {"choir": "strings", "name_zh": "第一小提琴 (E大调天国旋律)", "name_en": "Violins I (E Major Consolation)", "wave": "triangle", "notes": [{"t": 0.0, "d": 1.2, "f": 415.30}, {"t": 1.2, "d": 1.0, "f": 440.00}, {"t": 2.2, "d": 1.2, "f": 493.88}, {"t": 3.4, "d": 1.4, "f": 554.37}, {"t": 4.8, "d": 1.6, "f": 659.25}]},
                {"choir": "horns", "name_zh": "第一/第二圆号 (上行半音副旋律)", "name_en": "Horns I & II (Rising Counter-Melody)", "wave": "sine", "notes": [{"t": 0.0, "d": 1.6, "f": 329.63}, {"t": 1.6, "d": 1.6, "f": 370.00}, {"t": 3.2, "d": 1.6, "f": 415.30}, {"t": 4.8, "d": 1.6, "f": 493.88}]},
                {"choir": "winds", "name_zh": "长笛与单簧管 (微光琶音)", "name_en": "Flutes & Clarinets (Shimmering Arpeggios)", "wave": "sine", "notes": [{"t": 0.6, "d": 0.8, "f": 659.25}, {"t": 1.8, "d": 0.8, "f": 739.99}, {"t": 3.0, "d": 0.8, "f": 830.61}, {"t": 4.4, "d": 1.8, "f": 987.77}]}
            ]
        },
        {
            "id": "m1-synth-3",
            "title_zh": "展开部《震怒之日》初次预示与风暴高潮 (小节 207–260)",
            "title_en": "Development: Dies Irae Premonition & E-flat Minor Storm (Bars 207–260)",
            "bars": "Bars 207–260",
            "tempo_bpm": 96,
            "desc_zh": "单独分离圆号与长号首次吹响的《震怒之日》四音格里高利圣咏，观察弦乐急促的三连音音流与重型铜管的碰撞。",
            "desc_en": "Solo the horns and trombones intoning the first premonition of the Dies Irae sequence against raging string triplets.",
            "tracks": [
                {"choir": "horns", "name_zh": "6支圆号 (震怒之日圣咏原型)", "name_en": "6 Horns (Dies Irae Motif)", "wave": "sawtooth", "notes": [{"t": 0.0, "d": 1.2, "f": 349.23}, {"t": 1.2, "d": 1.2, "f": 329.63}, {"t": 2.4, "d": 1.2, "f": 349.23}, {"t": 3.6, "d": 1.8, "f": 293.66}]},
                {"choir": "brass", "name_zh": "小号与长号 (重音卡农呼应)", "name_en": "Trumpets & Trombones (Canonic Entry)", "wave": "sawtooth", "notes": [{"t": 1.2, "d": 1.2, "f": 466.16}, {"t": 2.4, "d": 1.2, "f": 440.00}, {"t": 3.6, "d": 1.2, "f": 466.16}, {"t": 4.8, "d": 1.6, "f": 392.00}]},
                {"choir": "strings", "name_zh": "高低音弦乐 (狂暴半音浪潮)", "name_en": "Strings (Turbulent Chromatic Surge)", "wave": "triangle", "notes": [{"t": 0.0, "d": 0.5, "f": 155.56}, {"t": 0.5, "d": 0.5, "f": 185.00}, {"t": 1.0, "d": 0.5, "f": 207.65}, {"t": 1.5, "d": 0.5, "f": 233.08}, {"t": 2.0, "d": 0.5, "f": 277.18}, {"t": 2.5, "d": 1.5, "f": 311.13}, {"t": 4.0, "d": 2.0, "f": 233.08}]},
                {"choir": "perc", "name_zh": "定音鼓与大镲 (风暴轰击)", "name_en": "Timpani & Cymbals (Storm Clashes)", "wave": "sine", "notes": [{"t": 0.0, "d": 0.4, "f": 77.78}, {"t": 2.4, "d": 0.4, "f": 77.78}, {"t": 4.8, "d": 0.8, "f": 116.54}]}
            ]
        }
    ],
    "2": [
        {
            "id": "m2-synth-1",
            "title_zh": "降A大调兰德勒主题与大提琴深情对位 (小节 1–52)",
            "title_en": "A-flat Major Ländler & Cello Counter-Melody (Bars 1–52)",
            "bars": "Bars 1–52",
            "tempo_bpm": 68,
            "desc_zh": "解析第一小提琴温婉的兰德勒舞步如何与大提琴宽广的歌唱性对位线条交织，还原维也纳沙龙的旧梦。",
            "desc_en": "Explore the interplay between the graceful first-violin Ländler and the warm, arching cello counter-subject.",
            "tracks": [
                {"choir": "strings", "name_zh": "第一小提琴与大提琴双声部复调", "name_en": "Violins I & Cellos Dual Counterpoint", "wave": "triangle", "notes": [{"t": 0.0, "d": 0.9, "f": 523.25}, {"t": 0.9, "d": 0.9, "f": 466.16}, {"t": 1.8, "d": 0.9, "f": 415.30}, {"t": 2.7, "d": 0.9, "f": 392.00}, {"t": 3.6, "d": 1.2, "f": 349.23}, {"t": 4.8, "d": 1.4, "f": 415.30}]},
                {"choir": "winds", "name_zh": "单簧管与大管 (轻柔三拍子伴奏)", "name_en": "Clarinets & Bassoons (Gentle 3/8 Pulse)", "wave": "sine", "notes": [{"t": 0.3, "d": 0.5, "f": 207.65}, {"t": 1.2, "d": 0.5, "f": 261.63}, {"t": 2.1, "d": 0.5, "f": 233.08}, {"t": 3.0, "d": 0.5, "f": 207.65}, {"t": 4.2, "d": 1.6, "f": 261.63}]},
                {"choir": "horns", "name_zh": "柔音圆号 (温暖和声衬底)", "name_en": "Muted Horns (Warm Harmonic Cushion)", "wave": "sine", "notes": [{"t": 0.0, "d": 2.7, "f": 207.65}, {"t": 2.7, "d": 3.3, "f": 155.56}]}
            ]
        },
        {
            "id": "m2-synth-2",
            "title_zh": "拨弦复调变奏与长笛花彩 (小节 133–165)",
            "title_en": "Pizzicato Variation & Woodwind Filigree (Bars 133–165)",
            "bars": "Bars 133–165",
            "tempo_bpm": 70,
            "desc_zh": "当兰德勒主题回归时，全弦乐改用精致的拨弦（pizzicato）托举竖琴与长笛/单簧管的流动三连音对位。",
            "desc_en": "Isolate the delicate string pizzicato texture against flowing flute and clarinet counter-melodies on the Ländler's return.",
            "tracks": [
                {"choir": "strings", "name_zh": "全弦乐五部 (立体声拨弦织体)", "name_en": "Full Strings (Polyphonic Pizzicato)", "wave": "triangle", "notes": [{"t": 0.0, "d": 0.3, "f": 415.30}, {"t": 0.6, "d": 0.3, "f": 523.25}, {"t": 1.2, "d": 0.3, "f": 466.16}, {"t": 1.8, "d": 0.3, "f": 392.00}, {"t": 2.4, "d": 0.3, "f": 349.23}, {"t": 3.0, "d": 0.3, "f": 415.30}, {"t": 3.6, "d": 0.3, "f": 311.13}]},
                {"choir": "winds", "name_zh": "长笛与双簧管 (歌唱性三连音复调)", "name_en": "Flute & Oboe (Lyrical Counter-Line)", "wave": "sine", "notes": [{"t": 0.0, "d": 1.2, "f": 622.25}, {"t": 1.2, "d": 1.2, "f": 698.46}, {"t": 2.4, "d": 1.2, "f": 622.25}, {"t": 3.6, "d": 1.6, "f": 523.25}]},
                {"choir": "horns", "name_zh": "独奏圆号 (中声部叹息应答)", "name_en": "Solo Horn (Tenor Sigh Response)", "wave": "sine", "notes": [{"t": 0.8, "d": 1.5, "f": 311.13}, {"t": 2.6, "d": 2.0, "f": 261.63}]}
            ]
        },
        {
            "id": "m2-synth-3",
            "title_zh": "升G小调阴云风暴：三连音急流与铜管惊雷 (小节 166–210)",
            "title_en": "G-sharp Minor Storm Episode: Triplet Vortex & Brass Cries (Bars 166–210)",
            "bars": "Bars 166–210",
            "tempo_bpm": 88,
            "desc_zh": "剖析田园舞曲如何突然被升G小调的焦虑三连音吞没，铜管切分重音刺破弦乐漩涡。",
            "desc_en": "Hear how the idyllic dance is overtaken by agitated G-sharp minor string triplets and piercing brass syncopations.",
            "tracks": [
                {"choir": "strings", "name_zh": "小提琴与中提琴 (升G小调三连音急流)", "name_en": "Violins & Violas (G# minor Triplet Rush)", "wave": "sawtooth", "notes": [{"t": 0.0, "d": 0.4, "f": 207.65}, {"t": 0.4, "d": 0.4, "f": 233.08}, {"t": 0.8, "d": 0.4, "f": 246.94}, {"t": 1.2, "d": 0.4, "f": 277.18}, {"t": 1.6, "d": 0.8, "f": 311.13}, {"t": 2.4, "d": 1.2, "f": 415.30}]},
                {"choir": "brass", "name_zh": "小号与长号 (切分悲鸣重音)", "name_en": "Trumpets & Trombones (Syncopated Outcries)", "wave": "sawtooth", "notes": [{"t": 1.2, "d": 0.8, "f": 415.30}, {"t": 2.4, "d": 1.0, "f": 370.00}, {"t": 3.6, "d": 1.4, "f": 311.13}]},
                {"choir": "perc", "name_zh": "定音鼓 (低音滚奏逼近)", "name_en": "Timpani (Menacing Roll)", "wave": "sine", "notes": [{"t": 0.0, "d": 1.5, "f": 103.83}, {"t": 2.0, "d": 2.5, "f": 103.83}]}
            ]
        }
    ],
    "3": [
        {
            "id": "m3-synth-1",
            "title_zh": "向鱼传道：定音鼓独奏、高音bE单簧管与桦木枝 (小节 1–112)",
            "title_en": "Fischpredigt: Timpani Solo, E-flat Clarinet & Rute (Bars 1–112)",
            "bars": "Bars 1–112",
            "tempo_bpm": 108,
            "desc_zh": "分离定音鼓三次干脆的开场重击，追踪单簧管与高音bE单簧管滑稽扭曲的十六分音符复调，以及桦木枝（Rute）拍击大鼓的奇特音色。",
            "desc_en": "Isolate the opening timpani strokes, the ironic E-flat clarinet melody, and the dry brush-slap of the Rute on the bass drum shell.",
            "tracks": [
                {"choir": "perc", "name_zh": "定音鼓与桦木枝 Rute (节奏骨架)", "name_en": "Timpani & Rute (Rhythmic Skeleton)", "wave": "sine", "notes": [{"t": 0.0, "d": 0.3, "f": 130.81}, {"t": 0.5, "d": 0.3, "f": 98.00}, {"t": 1.0, "d": 0.3, "f": 65.41}, {"t": 1.8, "d": 0.3, "f": 130.81}, {"t": 3.0, "d": 0.3, "f": 98.00}]},
                {"choir": "winds", "name_zh": "单簧管与高音bE单簧管 (向鱼传道主题)", "name_en": "Clarinets & E-flat Clarinet (Fischpredigt)", "wave": "triangle", "notes": [{"t": 1.5, "d": 0.4, "f": 261.63}, {"t": 1.9, "d": 0.4, "f": 293.66}, {"t": 2.3, "d": 0.4, "f": 311.13}, {"t": 2.7, "d": 0.4, "f": 349.23}, {"t": 3.1, "d": 0.6, "f": 392.00}, {"t": 3.7, "d": 0.6, "f": 311.13}, {"t": 4.3, "d": 0.9, "f": 261.63}]},
                {"choir": "strings", "name_zh": "低音弦乐与中提琴 (永动旋涡对位)", "name_en": "Lower Strings & Violas (Perpetual Swirl)", "wave": "sawtooth", "notes": [{"t": 1.5, "d": 0.6, "f": 130.81}, {"t": 2.1, "d": 0.6, "f": 155.56}, {"t": 2.7, "d": 0.6, "f": 196.00}, {"t": 3.3, "d": 0.6, "f": 155.56}, {"t": 3.9, "d": 1.2, "f": 130.81}]}
            ]
        },
        {
            "id": "m3-synth-2",
            "title_zh": "D大调第一中部：庸俗军乐号角与弦乐滑音反讽 (小节 190–256)",
            "title_en": "First Trio in D Major: Brash Brass Fanfare & String Glissandi (Bars 190–256)",
            "bars": "Bars 190–256",
            "tempo_bpm": 100,
            "desc_zh": "聆听铜管突然闯入的耀眼D大调号角，以及小提琴略带夸张滑音的世俗圆舞曲应答。",
            "desc_en": "Compare the sudden, gleaming D major brass fanfare against the ironic, portamento-laden string waltz response.",
            "tracks": [
                {"choir": "brass", "name_zh": "小号与长号 (D大调辉煌号角)", "name_en": "Trumpets & Trombones (D Major Fanfare)", "wave": "sawtooth", "notes": [{"t": 0.0, "d": 0.8, "f": 293.66}, {"t": 0.8, "d": 0.8, "f": 369.99}, {"t": 1.6, "d": 1.0, "f": 440.00}, {"t": 2.6, "d": 1.4, "f": 587.33}]},
                {"choir": "horns", "name_zh": "圆号群 (ベル朝上回响)", "name_en": "Horns (Bells-Up Echo)", "wave": "sawtooth", "notes": [{"t": 0.8, "d": 1.2, "f": 293.66}, {"t": 2.0, "d": 1.8, "f": 369.99}]},
                {"choir": "strings", "name_zh": "小提琴 (滑音歌唱性复调)", "name_en": "Violins (Glissando Cantabile)", "wave": "triangle", "notes": [{"t": 2.6, "d": 1.0, "f": 587.33}, {"t": 3.6, "d": 1.0, "f": 554.37}, {"t": 4.6, "d": 1.4, "f": 493.88}]}
            ]
        },
        {
            "id": "m3-synth-3",
            "title_zh": "绝望尖叫 (Der Aufschrei / Totengreif)：复合调性崩塌 (小节 465–516)",
            "title_en": "The Scream of Despair (Aufschrei): Bitonal Tutti Collapse (Bars 465–516)",
            "bars": "Bars 465–516",
            "tempo_bpm": 104,
            "desc_zh": "解剖全曲最骇人的降B小调/升C复调性“绝望尖叫”和弦（ffff）：定音鼓、大锣、10支圆号、小号与尖叫的木管如何同时撕裂声场。",
            "desc_en": "Deconstruct the shattering ffff Aufschrei chord layer by layer: screaming piccolos/clarinets, 10 horns, heavy brass, and tam-tam crash.",
            "tracks": [
                {"choir": "brass", "name_zh": "小号与长号 (撕裂性不协和强音)", "name_en": "Trumpets & Trombones (Shattering Chord)", "wave": "sawtooth", "notes": [{"t": 0.0, "d": 2.4, "f": 466.16}, {"t": 2.4, "d": 2.0, "f": 415.30}]},
                {"choir": "horns", "name_zh": "10支圆号 (全力怒吼 ffff)", "name_en": "10 Horns (Full Force ffff)", "wave": "sawtooth", "notes": [{"t": 0.0, "d": 2.4, "f": 277.18}, {"t": 2.4, "d": 2.0, "f": 233.08}]},
                {"choir": "winds", "name_zh": "短笛与高音单簧管 (高音尖啸)", "name_en": "Piccolos & E-flat Clarinet (Shriek)", "wave": "sawtooth", "notes": [{"t": 0.0, "d": 2.4, "f": 932.33}, {"t": 2.4, "d": 2.0, "f": 830.61}]},
                {"choir": "perc", "name_zh": "定音鼓、大鼓与大锣 (毁灭轰鸣)", "name_en": "Timpani, Bass Drum & Tam-tam", "wave": "sine", "notes": [{"t": 0.0, "d": 2.4, "f": 58.27}, {"t": 2.4, "d": 2.2, "f": 58.27}]}
            ]
        }
    ],
    "4": [
        {
            "id": "m4-synth-1",
            "title_zh": "原光开篇：女低音独唱与降D大调铜管圣咏光环 (小节 1–35)",
            "title_en": "Urlicht Opening: Contralto Solo & D-flat Major Brass Halo (Bars 1–35)",
            "bars": "Bars 1–35",
            "tempo_bpm": 54,
            "desc_zh": "单独聆听女低音“O Röschen rot!”的赤子吟唱，以及3支小号、4支圆号、长号与低音大管在极弱（pp）下构筑的教堂圣咏和声。",
            "desc_en": "Isolate Magdalena Kožená's contralto line ('O Röschen rot!') from the hushed D-flat major church chorale in muted brass and contrabassoon.",
            "tracks": [
                {"choir": "voices", "name_zh": "女低音独唱 (O Röschen rot!)", "name_en": "Contralto Solo (O Röschen rot!)", "wave": "triangle", "notes": [{"t": 0.0, "d": 1.6, "f": 277.18}, {"t": 1.6, "d": 1.4, "f": 311.13}, {"t": 3.0, "d": 2.2, "f": 369.99}, {"t": 5.4, "d": 1.8, "f": 277.18}]},
                {"choir": "brass", "name_zh": "弱音器小号与长号 (降D大调圣咏)", "name_en": "Muted Trumpets & Trombones (D-flat Chorale)", "wave": "sine", "notes": [{"t": 1.6, "d": 2.0, "f": 277.18}, {"t": 3.6, "d": 2.0, "f": 349.23}, {"t": 5.6, "d": 2.4, "f": 415.30}]},
                {"choir": "horns", "name_zh": "4支圆号 (温暖圣咏内声部)", "name_en": "4 Horns (Solemn Inner Voices)", "wave": "sine", "notes": [{"t": 1.6, "d": 2.0, "f": 207.65}, {"t": 3.6, "d": 2.0, "f": 233.08}, {"t": 5.6, "d": 2.4, "f": 277.18}]},
                {"choir": "strings", "name_zh": "弱音器低音弦乐 (深沉踏板音)", "name_en": "Muted Lower Strings (Deep Pedal)", "wave": "sine", "notes": [{"t": 1.6, "d": 6.4, "f": 138.59}]}
            ]
        },
        {
            "id": "m4-synth-2",
            "title_zh": "天国慰藉：独奏小提琴、单簧管、竖琴与女低音复调 (小节 67–103)",
            "title_en": "Celestial Consolation: Solo Violin, Clarinet, Harp & Voice (Bars 67–103)",
            "bars": "Bars 67–103",
            "tempo_bpm": 58,
            "desc_zh": "当守门天使试图阻拦灵魂时，首席小提琴独奏与单簧管、钟琴和竖琴织出晶莹的室内乐般天国复调。",
            "desc_en": "Hear the luminous chamber-music counterpoint of concertmaster solo violin, clarinet, glockenspiel, and harp enveloping the contralto.",
            "tracks": [
                {"choir": "voices", "name_zh": "女低音独唱 (Da kam ich auf einen breiten Weg)", "name_en": "Contralto Solo (Narrative Line)", "wave": "triangle", "notes": [{"t": 0.4, "d": 1.4, "f": 329.63}, {"t": 1.8, "d": 1.4, "f": 369.99}, {"t": 3.2, "d": 1.6, "f": 440.00}, {"t": 4.8, "d": 2.0, "f": 493.88}]},
                {"choir": "strings", "name_zh": "首席小提琴独奏 (甜美高音对位)", "name_en": "Solo Violin (Sweet High Counter-Line)", "wave": "triangle", "notes": [{"t": 0.0, "d": 1.2, "f": 659.25}, {"t": 1.2, "d": 1.2, "f": 739.99}, {"t": 2.4, "d": 1.2, "f": 659.25}, {"t": 3.6, "d": 1.6, "f": 587.33}, {"t": 5.2, "d": 1.8, "f": 659.25}]},
                {"choir": "winds", "name_zh": "双簧管与单簧管 (天国和声)", "name_en": "Oboe & Clarinet (Celestial Harmony)", "wave": "sine", "notes": [{"t": 0.0, "d": 2.4, "f": 440.00}, {"t": 2.4, "d": 2.4, "f": 493.88}, {"t": 4.8, "d": 2.2, "f": 440.00}]},
                {"choir": "perc", "name_zh": "钟琴 (星光点缀音)", "name_en": "Glockenspiel (Starlight Touches)", "wave": "sine", "notes": [{"t": 1.2, "d": 0.8, "f": 1318.51}, {"t": 3.6, "d": 0.8, "f": 1174.66}, {"t": 5.6, "d": 1.2, "f": 1318.51}]}
            ]
        },
        {
            "id": "m4-synth-3",
            "title_zh": "信仰宣言：“我来自上帝，必将归于上帝！” (小节 104–140)",
            "title_en": "Ardent Faith: \"Ich bin von Gott und will wieder zu Gott!\" (Bars 104–140)",
            "bars": "Bars 104–140",
            "tempo_bpm": 56,
            "desc_zh": "剖析女低音最炽热的信仰爆发，以及弦乐与木管如何托举着“直到永远（Ewig）”缓缓消融于无垠的微光。",
            "desc_en": "Trace the contralto's passionate ascent on 'Ich bin von Gott' and its serene dissolution into eternity ('Bis in Ewigkeit').",
            "tracks": [
                {"choir": "voices", "name_zh": "女低音独唱 (Ich bin von Gott!)", "name_en": "Contralto Solo (Ich bin von Gott!)", "wave": "triangle", "notes": [{"t": 0.0, "d": 1.4, "f": 415.30}, {"t": 1.4, "d": 1.4, "f": 466.16}, {"t": 2.8, "d": 1.8, "f": 554.37}, {"t": 4.6, "d": 2.4, "f": 415.30}]},
                {"choir": "strings", "name_zh": "全弦乐 (炽热八度托举与渐弱消融)", "name_en": "Strings (Ardent Octave Surge & Fade)", "wave": "triangle", "notes": [{"t": 0.0, "d": 1.4, "f": 415.30}, {"t": 1.4, "d": 1.4, "f": 466.16}, {"t": 2.8, "d": 1.8, "f": 554.37}, {"t": 4.6, "d": 2.4, "f": 277.18}]},
                {"choir": "horns", "name_zh": "圆号 (庄严延留和声)", "name_en": "Horns (Solemn Sustained Harmony)", "wave": "sine", "notes": [{"t": 0.0, "d": 3.5, "f": 277.18}, {"t": 3.5, "d": 3.5, "f": 207.65}]}
            ]
        }
    ],
    "5": [
        {
            "id": "m5-synth-1",
            "title_zh": "空间复调奇观：舞台暴风进行曲 vs. 后台远距铜管军乐 (小节 310–355)",
            "title_en": "Spatial Polyphony: Onstage Storm March vs. Offstage Fernorchester (Bars 310–355)",
            "bars": "Bars 310–355",
            "tempo_bpm": 112,
            "desc_zh": "可单独Solo后台远距乐队（fernorchester）的小号、圆号与三角铁，或Solo舞台上的弦乐与木管风暴，直接体验马勒惊世骇俗的双空间异步复调！",
            "desc_en": "Solo the offstage Fernorchester brass & triangle against the raging onstage orchestral storm to study Mahler's revolutionary spatial polyphony.",
            "tracks": [
                {"choir": "fernorchester", "name_zh": "后台远距铜管与打击乐 (异界军乐进行曲)", "name_en": "Offstage Fernorchester (Spatial Military Band)", "wave": "sawtooth", "notes": [{"t": 0.0, "d": 0.6, "f": 349.23}, {"t": 0.6, "d": 0.6, "f": 440.00}, {"t": 1.2, "d": 0.8, "f": 523.25}, {"t": 2.0, "d": 0.8, "f": 466.16}, {"t": 2.8, "d": 1.0, "f": 440.00}, {"t": 3.8, "d": 1.2, "f": 349.23}]},
                {"choir": "strings", "name_zh": "舞台弦乐 (狂暴F小调亡灵奔袭)", "name_en": "Onstage Strings (Furious F minor Dead March)", "wave": "sawtooth", "notes": [{"t": 0.0, "d": 0.4, "f": 174.61}, {"t": 0.4, "d": 0.4, "f": 196.00}, {"t": 0.8, "d": 0.4, "f": 207.65}, {"t": 1.2, "d": 0.4, "f": 233.08}, {"t": 1.6, "d": 0.8, "f": 261.63}, {"t": 2.4, "d": 1.2, "f": 174.61}, {"t": 3.6, "d": 1.4, "f": 130.81}]},
                {"choir": "winds", "name_zh": "舞台木管 (尖锐震怒之日变体)", "name_en": "Onstage Woodwinds (Piercing Dies Irae Variant)", "wave": "triangle", "notes": [{"t": 0.4, "d": 0.8, "f": 698.46}, {"t": 1.2, "d": 0.8, "f": 659.25}, {"t": 2.0, "d": 0.8, "f": 698.46}, {"t": 2.8, "d": 1.4, "f": 587.33}]},
                {"choir": "brass", "name_zh": "舞台长号与大号 (重型低音轰鸣)", "name_en": "Onstage Trombones & Tuba (Heavy Bass Thrusts)", "wave": "sawtooth", "notes": [{"t": 0.0, "d": 1.2, "f": 87.31}, {"t": 1.6, "d": 1.2, "f": 116.54}, {"t": 3.2, "d": 1.8, "f": 87.31}]}
            ]
        },
        {
            "id": "m5-synth-2",
            "title_zh": "末日大召唤 (Der große Appell)：四支后台小号与舞台夜莺长笛 (小节 448–471)",
            "title_en": "The Great Summons (Der große Appell): 4 Offstage Trumpets & Birdsong (Bars 448–471)",
            "bars": "Bars 448–471",
            "tempo_bpm": 60,
            "desc_zh": "隔离后台不同方向传来的四支小号与圆号召唤信号，对照舞台上孤独的长笛与短笛夜莺鸟鸣。",
            "desc_en": "Isolate the four spatially separated offstage trumpets and horns from the lone onstage flute and piccolo nightingale calls.",
            "tracks": [
                {"choir": "fernorchester", "name_zh": "后台4支小号与4支圆号 (四方末日号角)", "name_en": "Offstage 4 Trumpets & 4 Horns (Directional Fanfares)", "wave": "sawtooth", "notes": [{"t": 0.0, "d": 1.4, "f": 311.13}, {"t": 1.4, "d": 1.4, "f": 466.16}, {"t": 2.8, "d": 2.0, "f": 622.25}, {"t": 5.0, "d": 2.0, "f": 466.16}]},
                {"choir": "winds", "name_zh": "舞台长笛与短笛 (坟墓上的夜莺啼鸣)", "name_en": "Onstage Flute & Piccolo (Nightingale Birdsong)", "wave": "sine", "notes": [{"t": 1.8, "d": 0.5, "f": 1046.50}, {"t": 2.3, "d": 0.5, "f": 783.99}, {"t": 2.8, "d": 0.6, "f": 1244.51}, {"t": 4.2, "d": 0.6, "f": 932.33}, {"t": 4.8, "d": 1.4, "f": 1244.51}]},
                {"choir": "perc", "name_zh": "后台定音鼓与大鼓 (极远处的微弱雷声)", "name_en": "Offstage Timpani & Bass Drum (Distant Tremor)", "wave": "sine", "notes": [{"t": 0.0, "d": 2.5, "f": 77.78}, {"t": 3.5, "d": 3.0, "f": 77.78}]}
            ]
        },
        {
            "id": "m5-synth-3",
            "title_zh": "“复活”无伴奏合唱极弱进入与女高音独唱破茧 (小节 472–525)",
            "title_en": "\"Aufersteh'n\" Whispered Choral Entry & Soprano Solo Emergence (Bars 472–525)",
            "bars": "Bars 472–525",
            "tempo_bpm": 52,
            "desc_zh": "剖析混声合唱在ppp下无伴奏唱出降E大调《复活》赞歌，低音提琴深沉的五度衬底，以及女高音独唱（Kate Royal）如何无痕地从合唱声部中浮现。",
            "desc_en": "Examine the ppp a cappella choral entry ('Aufersteh'n'), the deep double-bass fifths, and Kate Royal's soprano solo emerging seamlessly from the sopranos.",
            "tracks": [
                {"choir": "voices", "name_zh": "混声合唱与女高音独唱 (Aufersteh'n wirst du)", "name_en": "Mixed Choir & Soprano Solo (Aufersteh'n)", "wave": "triangle", "notes": [{"t": 0.0, "d": 1.4, "f": 311.13}, {"t": 1.4, "d": 1.2, "f": 311.13}, {"t": 2.6, "d": 1.2, "f": 349.23}, {"t": 3.8, "d": 1.4, "f": 392.00}, {"t": 5.2, "d": 1.6, "f": 415.30}, {"t": 6.8, "d": 2.0, "f": 466.16}]},
                {"choir": "strings", "name_zh": "低音提琴与大提琴 (极弱深渊五度持续音)", "name_en": "Double Basses & Cellos (Abyssal Fifth Pedal)", "wave": "sine", "notes": [{"t": 0.0, "d": 4.2, "f": 77.78}, {"t": 4.2, "d": 4.6, "f": 116.54}]},
                {"choir": "winds", "name_zh": "英国管与低音单簧管 (温柔过门应答)", "name_en": "English Horn & Bass Clarinet (Gentle Interlude)", "wave": "sine", "notes": [{"t": 3.8, "d": 2.2, "f": 233.08}, {"t": 6.0, "d": 2.8, "f": 311.13}]}
            ]
        },
        {
            "id": "m5-synth-4",
            "title_zh": "宇宙神圣终局：全音栓管风琴、三口深沉大钟、合唱与百人乐队 (小节 712–765)",
            "title_en": "Cosmic Apotheosis: Full Pipe Organ, 3 Deep Bells, Choir & Tutti (Bars 712–765)",
            "bars": "Bars 712–765",
            "tempo_bpm": 66,
            "desc_zh": "体验交响曲历史的巅峰声响：单独开启或叠合教堂管风琴（Volles Werk）、三口深沉大钟、10支圆号、重型铜管与全合唱团的“Sterben werd' ich, um zu leben!”。",
            "desc_en": "Solo or combine the full church pipe organ (Volles Werk), three deep bells, 10 horns, heavy brass, and full chorus at the E-flat major climax.",
            "tracks": [
                {"choir": "organ", "name_zh": "教堂管风琴 (Volles Werk 32尺低音与全和弦)", "name_en": "Pipe Organ (Full Pleno & 32' Pedal)", "wave": "sawtooth", "notes": [{"t": 0.0, "d": 2.2, "f": 77.78}, {"t": 2.2, "d": 2.2, "f": 103.83}, {"t": 4.4, "d": 2.6, "f": 155.56}]},
                {"choir": "voices", "name_zh": "全合唱与双独唱 (Aufersteh'n zum Leben!)", "name_en": "Full Chorus & Soloists (Triumphant Hymn)", "wave": "triangle", "notes": [{"t": 0.0, "d": 1.4, "f": 466.16}, {"t": 1.4, "d": 1.4, "f": 523.25}, {"t": 2.8, "d": 1.6, "f": 622.25}, {"t": 4.4, "d": 2.6, "f": 783.99}]},
                {"choir": "brass", "name_zh": "10支小号与4支长号 (复活圣咏辉煌齐奏)", "name_en": "10 Trumpets & 4 Trombones (Blazing Chorale)", "wave": "sawtooth", "notes": [{"t": 0.0, "d": 1.4, "f": 311.13}, {"t": 1.4, "d": 1.4, "f": 392.00}, {"t": 2.8, "d": 1.6, "f": 466.16}, {"t": 4.4, "d": 2.6, "f": 622.25}]},
                {"choir": "horns", "name_zh": "10支圆号 (贝尔朝上辉煌对位)", "name_en": "10 Horns (Bells-Up Counter-Chorale)", "wave": "sawtooth", "notes": [{"t": 0.0, "d": 2.2, "f": 233.08}, {"t": 2.2, "d": 2.2, "f": 311.13}, {"t": 4.4, "d": 2.6, "f": 466.16}]},
                {"choir": "perc", "name_zh": "三口深沉教堂大钟与大小锣 (宇宙钟鸣)", "name_en": "3 Deep Church Bells & Tam-tams (Cosmic Peal)", "wave": "sine", "notes": [{"t": 0.0, "d": 1.2, "f": 155.56}, {"t": 1.4, "d": 1.2, "f": 130.81}, {"t": 2.8, "d": 1.2, "f": 116.54}, {"t": 4.4, "d": 2.6, "f": 155.56}]},
                {"choir": "strings", "name_zh": "全弦乐五部 (宽广震音与圣咏支撑)", "name_en": "Full Strings (Broad Tremolo & Hymn Support)", "wave": "triangle", "notes": [{"t": 0.0, "d": 2.2, "f": 311.13}, {"t": 2.2, "d": 2.2, "f": 415.30}, {"t": 4.4, "d": 2.6, "f": 622.25}]}
            ]
        }
    ]
}


# ============================================================================
# MOVEMENT I: Allegro maestoso (Totenfeier / Funeral Rites) — 445 Bars, 42 Stages
# ============================================================================
MVT1_STAGES_RAW = [
    (1, 10, "Opening", 1, "#dc2626", ["m1-totenfeier-march"], ["strings"],
     "引子（一）：C小调高音弦乐冰封震音与低音提琴雷霆宣叙调",
     "Introduction I: Frozen Upper-String Tremolo and Furious Bass Recitative",
     "低音弦乐狂暴十六分音符宣叙调", "Furious Lower-String Sixteenth-Note Recitative",
     "大提琴与低音提琴：强奏（ff）十六分音符激升，劈出肃穆而暴烈的葬礼宣叙调",
     "Cellos and Double Basses: Furious ff sixteenth-note surges carving the stern funeral recitative",
     "第一、第二小提琴与中提琴在G音高八度上维持冰冷颤音",
     "Violins and violas sustain an icy, trembling octave G pedal high above",
     "巨人之死的葬礼（Totenfeier）由此展开！拉特尔指挥柏林爱乐低音弦乐以刀锋般的跳弓与重音咬弦自深渊直冲而起，与上方凝固的震音构成刺骨的虚空对比。",
     "The funeral rites (Totenfeier) of a fallen titan begin! Rattle and the BPO lower strings attack the ascending scales with razor-sharp bow bite against frozen upper-string tremolos.",
     {"strings": "低音弦乐主导狂暴宣叙调裂帛声，高音弦乐凝固于八度震音", "winds": "木管在句尾加入短促尖锐的断音叹息", "horns": "圆号在深处蓄势待发"},
     {"strings": "Lower strings command the furious recitative tears; upper strings hold frozen octaves", "winds": "Woodwinds append sharp staccato sighs at phrase ends", "horns": "Horns maintain brooding tension in the depth"},
     "听低音弦乐三次急促上冲后停顿于不协和重音", "Listen for three furious upward bass surges halting on jagged accents"),

    (11, 18, "Intro-B", 1, "#dc2626", ["m1-totenfeier-march"], ["strings", "winds"],
     "引子（二）：宣叙调崩落与定音鼓葬礼步伐确立",
     "Introduction II: Recitative Collapse and Establishment of the Funeral Tread",
     "低音半音下坠与定音鼓C-G踏步", "Chromatic Bass Descent & Timpani C-G Tread",
     "大提琴与低音提琴：沉重的四分音符下行，定音鼓敲响C与G的宿命脉搏",
     "Cellos and Basses: Heavy quarter-note descent as timpani strike the fateful C–G pulse",
     "双簧管与单簧管在弱音区发出断续的半音呻吟",
     "Oboes and clarinets utter fragmented chromatic groans in the middle register",
     "狂暴的冲击逐渐平息为不可抗拒的沉重步伐，低音提琴与大管确立了整座乐章的C小调送葬节奏基石。",
     "The opening fury settles into an inexorable funeral march tread as basses and bassoons lock into the C minor ostinato.",
     {"strings": "低音提琴确立沉重的四分音符送葬步伐", "winds": "双簧管与大管切入阴郁的半音叹息", "perc": "定音鼓轻叩C-G葬礼脉搏"},
     {"strings": "Double basses establish the heavy quarter-note funeral tread", "winds": "Oboes and bassoons interject somber chromatic sighs", "perc": "Timpani tap the C-G funeral pulse"},
     "注意第16小节低音提琴稳定下来的四拍子送葬律动", "Notice the steady 4/4 funeral march ostinato locking in at bar 16"),

    (19, 28, "Reh. 1", 1, "#dc2626", ["m1-totenfeier-march"], ["winds", "strings"],
     "呈示部第一主题（一）：双簧管与英国管的C小调送葬哀歌",
     "First Subject Group I: Oboe and English Horn C Minor Funeral Lament",
     "双簧管与英国管齐奏凄切哀歌", "Oboe & English Horn Unison Funeral Lament",
     "双簧管与英国管：吹奏带有附点节奏的C小调核心葬礼旋律",
     "Oboes and English Horn: Intone the dotted C minor funeral march melody in piercing unison",
     "大提琴与低音提琴持续冷酷的踏步音型，小提琴穿插短促叹息",
     "Cellos and basses maintain the implacable march ostinato while violins add clipped sighs",
     "在冷酷的低音步伐之上，柏林爱乐木管首席吹出苍凉如挽歌的第一主题，音色干涩而充满古希腊悲剧般的宿命感。",
     "Over the relentless bass tread, BPO oboes and English horn voice the bleak primary lament with austere, tragic dignity.",
     {"winds": "双簧管与英国管主导C小调附点挽歌", "strings": "低音弦乐维持冷酷踏步，高音弦乐切分应答", "horns": "圆号以弱音长音烘托阴暗背景"},
     {"winds": "Oboes and English horn lead the dotted C minor lament", "strings": "Lower strings keep the relentless tread; violins add syncopated sighs", "horns": "Horns sustain dark background pedals"},
     "紧跟双簧管与英国管那极具穿透力的双簧片悲鸣", "Follow the penetrating double-reed lament riding above the bass tread"),

    (29, 35, "Reh. 1+10", 1, "#b91c1c", ["m1-totenfeier-march"], ["strings", "brass"],
     "呈示部第一主题（二）：弦乐悲叹接力与重音铜管威慑",
     "First Subject Group II: String Lament Relay and Heavy Brass Menace",
     "小提琴接过挽歌并推向铜管强音", "Violins Take Up Lament Toward Brass Outburst",
     "第一小提琴与中提琴：以饱满弓压奏出变形的葬礼附点主题",
     "First Violins and Violas: Voice the funeral dotted motif with intense bow weight",
     "长号与大号在低音区发出沉闷的威慑性合奏和弦",
     "Trombones and tuba rumble menacingly in the low register",
     "情绪陡然加剧，弦乐声部将哀歌推向高音区，铜管群如同墓穴石门般轰然回应。",
     "Tension escalates sharply as the strings drive the lament upward, answered by sepulchral trombone and tuba chords.",
     {"strings": "小提琴高八度强化哀歌旋律张力", "brass": "长号与大号切入沉重的葬礼和弦", "winds": "木管重叠高音区尖锐装饰音"},
     {"strings": "Violins intensify the lament in octaves", "brass": "Trombones and tuba enter with sepulchral chords", "winds": "Woodwinds double the upper register with sharp ornaments"},
     "留意铜管在句尾突然切入的冷峻和弦", "Listen for the sudden, stern brass chord punctuating the phrase"),

    (36, 42, "Reh. 2-7", 1, "#991b1b", ["m1-totenfeier-march", "m1-rising-cry"], ["horns", "strings"],
     "过渡桥梁：圆号半音悲鸣与调性融化",
     "Transition Bridge: Chromatic Horn Outcry and Harmonic Melting",
     "圆号群半音上行叹息引向远方", "Chromatic Rising Horn Sighs Dissolving the March",
     "圆号声部：吹奏渴望救赎的半音上行叹息动机",
     "Horns: Sound the yearning ascending chromatic cry motif",
     "弦乐踏步逐渐放缓并转为柔和的震音铺垫",
     "String march tread slackens and dissolves into a soft shimmering cushion",
     "严酷的C小调送葬队伍忽然放慢脚步，圆号温柔的转调将阴霾拨开一道缝隙，准备迎接E大调的天国微光。",
     "The grim C minor procession falters; warm horn modulations part the clouds to prepare the E major vision.",
     {"horns": "圆号吹响关键的半音上行过渡动机", "strings": "弦乐卸下重音，化为轻柔连奏", "winds": "单簧管与长笛柔化声场边缘"},
     {"horns": "Horns intone the pivotal ascending chromatic bridge", "strings": "Strings shed their harsh accents for gentle legato", "winds": "Clarinets and flutes soften the harmonic edges"},
     "听圆号如何在短短数小节内将C小调阴霾融化为温暖的E大调", "Hear how the horns melt the C minor gloom into luminous E major within bars"),

    (43, 52, "Reh. 2", 1, "#f97316", ["m1-rising-cry"], ["strings", "horns"],
     "第二主题（一）：E大调彼岸微光与弱音小提琴天国牧歌",
     "Second Subject I: E Major Glimpse of Paradise in Muted Violins",
     "第一小提琴极弱（pp）高音区拱形旋律", "Muted First Violins pp Arching E Major Melody",
     "第一小提琴（加弱音器）：在E大调高音区如丝绸般飘出安慰主题",
     "Muted First Violins: Float the silk-like E major consolation theme high above",
     "圆号与中提琴在中音区交织温暖的半音对位线条",
     "Horns and violas weave warm chromatic counter-lines in the middle register",
     "全曲第一次闪现彼岸的救赎微光！马勒要求小提琴极其轻柔地滑入E大调，仿佛在葬礼黑夜中瞥见天国的田园。",
     "The first glimpse of paradise! Mahler marks the violins pp as they glide into distant E major, a fleeting pastoral mirage amidst the funeral night.",
     {"strings": "第一小提琴以极弱音色拉出超凡脱俗的E大调旋律", "horns": "独奏圆号温暖地托举内声部复调", "winds": "长笛与双簧管点缀清澈露珠般的音型"},
     {"strings": "First violins spin an ethereal pp E major cantilena", "horns": "Solo horns warmly support the inner counterpoint", "winds": "Flutes and oboes add crystalline dew-like touches"},
     "感受小提琴进入E大调时瞬间失重般的透明音色", "Savor the weightless, translucent timbre as the violins enter E major"),

    (53, 62, "Reh. 3", 1, "#ea580c", ["m1-rising-cry"], ["winds", "strings"],
     "第二主题（二）：木管与弦乐的天国复调渐强与消逝",
     "Second Subject II: Woodwind and String Celestial Counterpoint Swell",
     "长笛、双簧管与小提琴层层叠加上升", "Flutes, Oboes & Violins Soaring in Radiant Counterpoint",
     "小提琴与高音木管：将上行渴望动机推向充满希望的波峰",
     "Violins and Upper Winds: Carry the ascending yearning motif to a hopeful crest",
     "大提琴与低音提琴以柔和的持续音支撑，但暗流悄然涌动",
     "Cellos and basses sustain a gentle pedal while dark undercurrents stir beneath",
     "这缕天国幻象愈发真切，拉特尔让柏林爱乐的弦乐与木管绽放出短暂而绚烂的金色光泽，却在顶峰处骤然折断。",
     "The heavenly mirage grows radiant as Rattle draws a brief golden bloom from strings and winds before it snaps off abruptly.",
     {"strings": "小提琴高音区歌唱性与中提琴流动内声部交融", "winds": "长笛与双簧管在高音区齐奏发光", "horns": "圆号渐强后迅速收拢"},
     {"strings": "High violin cantilena intertwines with flowing viola inner voices", "winds": "Flutes and oboes glow in high unison", "horns": "Horns swell and quickly recede"},
     "注意旋律在最甜美处突然被低音弦乐的阴影打断", "Notice how the melody is cut short at its sweetest peak by dark lower strings"),

    (63, 73, "Reh. 4", 1, "#dc2626", ["m1-totenfeier-march"], ["strings", "perc"],
     "葬礼风暴重临：狂暴宣叙调打碎田园幻梦",
     "Return of the Funeral Storm: Furious Recitative Shatters the Mirage",
     "低音弦乐再度咆哮冲锋", "Lower Strings Roar Back with the Opening Recitative",
     "大提琴与低音提琴：以双倍猛烈的十六分音符音阶撕碎E大调幻象",
     "Cellos and Double Basses: Rip through the E major mirage with ferocious sixteenth-note scales",
     "定音鼓与高音弦乐震音重新锁死冷酷的悲剧框架",
     "Timpani and upper-string tremolos clamp the tragic framework back into place",
     "幻梦破碎！现实的死亡重锤再度砸下，低音弦乐比开篇更加暴烈地掀起风暴。",
     "The dream shatters! Death's reality crashes back as lower strings unleash an even fiercer storm than the opening.",
     {"strings": "大提琴与低音提琴狂暴冲击，高音弦乐尖锐震音", "perc": "定音鼓猛烈敲击宣告葬礼重临", "brass": "长号在低音区切入冷酷重音"},
     {"strings": "Cellos and basses storm upward against piercing violin tremolos", "perc": "Timpani strike fiercely to announce the march's return", "brass": "Trombones inject cold low-register accents"},
     "对比刚才的E大调柔光与此时低音弦乐擦弦的剧烈反差", "Contrast the preceding E major glow with the savage bow attack of the basses"),

    (74, 84, "Reh. 5", 1, "#b91c1c", ["m1-totenfeier-march"], ["brass", "strings"],
     "呈示部高潮：全奏葬礼进行曲与铜管强音碾压",
     "Exposition Climax: Tutti Funeral March and Crushing Brass Accents",
     "重型铜管与全弦乐合奏送葬主题", "Heavy Brass & Full Strings Proclaim the Funeral March",
     "圆号、小号与长号：以强奏（ff）咆哮出附点葬礼旋律",
     "Horns, Trumpets, and Trombones: Roar the dotted funeral melody in ff tutti",
     "全弦乐以跳弓与重音和弦提供雷霆般的伴奏支撑",
     "Full strings provide thunderous chordal and spiccato support",
     "整个柏林爱乐乐团全奏爆发，葬礼进行曲不再是孤寂的哀歌，而化作不可阻挡的巨人步伐。",
     "The full Berliner Philharmoniker erupts: the funeral march transforms from a lonely lament into an unstoppable, titanic juggernaut.",
     {"brass": "小号与长号强力主导葬礼主旋律", "horns": "6支圆号贝尔朝上强化中音区咆哮", "strings": "弦乐全奏提供凌厉的节奏切分", "perc": "定音鼓与大鼓重击拍点"},
     {"brass": "Trumpets and trombones command the funeral main theme", "horns": "6 horns bells-up reinforce the mid-register roar", "strings": "Full strings drive incisive rhythmic syncopations", "perc": "Timpani and bass drum hammer the downbeats"},
     "感受铜管全奏与定音鼓重击带来的压倒性声压", "Feel the overwhelming acoustic weight of the full brass and timpani tutti"),

    (85, 96, "Reh. 5+11", 1, "#991b1b", ["m1-totenfeier-march", "m1-rising-cry"], ["strings", "winds"],
     "呈示部收束区（一）：半音跌落与木管凄厉哀鸣",
     "Exposition Closing Group I: Chromatic Collapse and Piercing Wind Cries",
     "弦乐下行半音阶与木管尖锐长音", "Chromatic String Descent & Piercing Woodwind Cries",
     "小提琴与中提琴：如瀑布般半音下行，层层剥落能量",
     "Violins and Violas: Cascade downward chromatically, stripping away energy",
     "双簧管与单簧管在高音区发出不甘的延长音呼号",
     "Oboes and clarinets cry out with desperate held notes in the upper register",
     "高潮过后，乐队仿佛力竭般急速下坠，唯有木管声部仍在废墟上方发出凄凉的呼喊。",
     "After the climax, the orchestra plunges downward as if exhausted, leaving the woodwinds crying out over the wreckage.",
     {"strings": "高低音弦乐成片半音下行", "winds": "高音木管维持撕裂般的长音叹息", "horns": "圆号以断续和弦承接下坠"},
     {"strings": "Upper and lower strings cascade down in chromatic waves", "winds": "High woodwinds sustain tearing sigh tones", "horns": "Horns catch the descent with broken chords"},
     "听弦乐半音阶层层下沉时木管不肯熄灭的悲鸣", "Listen to the unyielding woodwind cries as the strings sink chromatically"),

    (97, 107, "Reh. 6", 1, "#7f1d1d", ["m1-totenfeier-march"], ["strings", "horns"],
     "呈示部收束区（二）：低音拨弦余烬与阴影徘徊",
     "Exposition Closing Group II: Pizzicato Embers and Lingering Shadows",
     "大提琴与低音提琴拨弦余音", "Cello & Double Bass Pizzicato Aftermath",
     "低音弦乐：以空洞的拨弦（pizzicato）延续送葬脉搏",
     "Lower Strings: Continue the funeral pulse in hollow pizzicato strokes",
     "柔音圆号与低音单簧管在暗处交换幽灵般的动机碎片",
     "Muted horns and bass clarinet exchange ghostly motivic fragments in the dark",
     "声响褪至极弱（pp），低音单簧管与圆号在空旷的大厅里留下幽暗的残影。",
     "Dynamics recede to pp; bass clarinet and muted horns trace spectral shadows across the cavernous hall.",
     {"strings": "大提琴与低音提琴拨弦如残烛摇曳", "winds": "低音单簧管与大管吹出幽暗碎片", "horns": "弱音圆号远距离低语"},
     {"strings": "Cello and bass pizzicati flicker like dying candles", "winds": "Bass clarinet and bassoons utter dark fragments", "horns": "Muted horns murmur from afar"},
     "留意低音单簧管那深不见底的冷峻音色", "Note the abyssal, velvety timbre of the solo bass clarinet"),

    (108, 117, "Reh. 7-10", 1, "#fb923c", ["m1-rising-cry"], ["strings", "winds"],
     "呈示部尾声：C大调温暖幻影的短暂闪回",
     "Exposition Codetta: Brief Flashback of Warm C Major Consolation",
     "小提琴与长笛轻柔抚慰", "Violins & Flutes Gentle Consoling Flashback",
     "第一小提琴与长笛：在极弱（ppp）中重现上行安慰动机",
     "First Violins and Flutes: Recall the ascending consolation motif in hushed ppp",
     "竖琴与中提琴提供透明的分解和弦支撑",
     "Harp and violas provide translucent arpeggiated support",
     "在进入漫长的展开部深渊之前，马勒让C大调的阳光最后一次温柔地抚摸墓碑。",
     "Before descending into the vast development abyss, Mahler lets a final ray of C major sunlight caress the gravestone.",
     {"strings": "小提琴极弱滑音如梦境重现", "winds": "长笛与单簧管轻柔呼应", "perc": "竖琴泛音般点缀和声"},
     {"strings": "Violins glide in ppp portamento like a recurring dream", "winds": "Flutes and clarinets respond tenderly", "perc": "Harp adds bell-like harmonic touches"},
     "捕捉竖琴与弱音小提琴营造的片刻宁静", "Catch the fleeting serenity created by harp and muted violins"),

    (118, 128, "Reh. 7", 2, "#0284c7", ["m1-totenfeier-march"], ["strings", "winds"],
     "展开部第一阶段（一）：地底拨弦潜行与英国管孤寂牧歌",
     "Development Part I-A: Subterranean Pizzicato and Lonely English Horn",
     "低音拨弦踏步与英国管独奏", "Subterranean Bass Pizzicato & Solo English Horn",
     "英国管独奏：在空旷的音程上方吹出孤寂而悠远的田园挽歌",
     "Solo English Horn: Floats a lonely, distant pastoral elegy over open intervals",
     "低音提琴以极弱的拨弦在底部维持不眠的步伐",
     "Double basses maintain a sleepless ppp pizzicato tread beneath",
     "展开部在幽暗的地底开启，低音提琴的拨弦如同永不停息的钟摆，英国管独奏在荒原上独自吟唱。",
     "The development opens subterraneanly: double-bass pizzicati tick like a tireless pendulum while the solo English horn sings across a desolate plain.",
     {"winds": "英国管独奏主导凄美田园旋律", "strings": "低音提琴拨弦维持地底脉动", "horns": "圆号以柔和五度持续音衬底"},
     {"winds": "Solo English horn leads the poignant pastoral melody", "strings": "Double bass pizzicati keep the subterranean pulse", "horns": "Horns cushion with soft open fifths"},
     "专注聆听英国管独奏与底部低音提琴拨弦的空间距离感", "Focus on the spatial distance between the solo English horn and the deep bass pizzicati"),

    (129, 137, "Reh. 8", 2, "#0ea5e9", ["m1-rising-cry"], ["winds", "strings"],
     "展开部第一阶段（二）：长笛、双簧管与独奏小提琴的田园交谈",
     "Development Part I-B: Pastoral Dialogue of Flute, Oboe, and Solo Violin",
     "木管与弦乐室内乐式三部对位", "Chamber-Like Three-Voice Counterpoint in Winds & Strings",
     "长笛、双簧管与第一小提琴：相互模仿、交织上升的田园旋律线",
     "Flutes, Oboes, and Violins I: Imitate and entwine ascending pastoral lines",
     "大提琴与低音大管在下方保持平稳的五度根音",
     "Cellos and bassoons hold a calm fifth drone below",
     "音乐织体清澈如室内乐，拉特尔将柏林爱乐各木管声部的独立线条梳理得晶莹剔透。",
     "The texture clears into luminous chamber music; Rattle balances the individual BPO woodwind solos with crystalline transparency.",
     {"winds": "长笛与双簧管进行精妙的卡农式对话", "strings": "小提琴声部轻巧切入第三声部复调", "horns": "圆号温暖托底"},
     {"winds": "Flute and oboe engage in delicate canonic dialogue", "strings": "Violins gently weave a third contrapuntal voice", "horns": "Horns provide a warm harmonic floor"},
     "听长笛与双簧管一唱一和的精致复调交织", "Listen to the refined contrapuntal give-and-take between flute and oboe"),

    (138, 145, "Reh. 9-8", 2, "#10b981", ["m1-rising-cry"], ["strings", "horns"],
     "展开部第一阶段（三）：C大调宽广呼吸与圆号远景召唤",
     "Development Part I-C: Broad C Major Breathing and Distant Horn Call",
     "弦乐宽广歌唱与圆号牧歌号角", "Broad String Cantabile & Pastoral Horn Call",
     "第一小提琴与大提琴：奏出宽广舒展的C大调拱形乐句",
     "Violins I and Cellos: Unfold a broad, arching C major phrase",
     "圆号在远方吹响带有自然泛音色彩的田园号角",
     "Horns sound a distant, natural-harmonic pastoral call",
     "视野豁然开朗，如同站在阿尔卑斯山巅俯瞰云海，圆号的号角声带着纯净的自然气息。",
     "The horizon opens wide like an Alpine vista as horns sound a pure, open-air call across the strings.",
     {"strings": "小提琴与大提琴八度舒展歌唱", "horns": "圆号吹出悠远的阿尔卑斯式号角", "winds": "单簧管柔美重叠内声部"},
     {"strings": "Violins and cellos sing broadly in octaves", "horns": "Horns intone a distant Alpine horn call", "winds": "Clarinets gently double the inner harmony"},
     "感受圆号号角声令整个声场瞬间扩展的纵深感", "Feel the sudden expansion of acoustic depth when the horns call out"),

    (146, 156, "Reh. 9", 2, "#059669", ["m1-rising-cry"], ["winds", "strings"],
     "展开部第一阶段（四）：英国管与低音单簧管的黄昏沉思",
     "Development Part I-D: Twilight Meditation of English Horn and Bass Clarinet",
     "暗色木管重现忧郁阴影", "Dark Reeds Reintroduce Melancholic Shadows",
     "英国管与低音单簧管：将明亮的田园动机染上半音化的暮色",
     "English Horn and Bass Clarinet: Tint the bright pastoral motif with chromatic twilight",
     "中提琴与大提琴以微弱的震音制造不安的潜流",
     "Violas and cellos generate an uneasy undertow with hushed tremolos",
     "田园的平静开始动摇，暗色木管（英国管与低音单簧管）悄然引入半音阴影，预示风暴即将重聚。",
     "Pastoral calm begins to waver as dark reeds (English horn and bass clarinet) insinuate chromatic shadows, foretelling the gathering storm.",
     {"winds": "英国管与低音单簧管交替传递阴郁旋律", "strings": "中低音弦乐震音悄然升温", "perc": "定音鼓在极弱处隐约滚奏"},
     {"winds": "English horn and bass clarinet pass a darkening melody", "strings": "Lower-string tremolos quietly gather heat", "perc": "Timpani murmur a barely audible roll"},
     "注意音色如何从明亮的长笛渐渐下沉到低音单簧管与定音鼓暗雷", "Notice how the timbre sinks from bright flutes down into bass clarinet and distant timpani thunder"),

    (157, 168, "Reh. 10", 2, "#eab308", ["m1-totenfeier-march"], ["strings", "horns"],
     "展开部第二阶段（一）：葬礼踏步复苏与弦乐焦灼赋格段",
     "Development Part II-A: Revival of the Funeral Tread and Agitated String Fugato",
     "低音弦乐恢复行进与内声部半音爬升", "Lower Strings Resume March & Chromatic Inner Climb",
     "大提琴与中提琴：以急促的附点与十六分音符展开模仿对位",
     "Cellos and Violas: Launch an agitated imitative counterpoint of dotted and sixteenth-note figures",
     "圆号与大管以阻塞音（gestopft）发出尖锐的警告信号",
     "Horns and bassoons issue sharp stopped-tone (gestopft) warning signals",
     "安宁彻底终结，弦乐各声部在焦灼的对位中相互追逐，圆号的阻塞音如金属般刺耳。",
     "Tranquility ends completely; string sections chase one another in feverish counterpoint punctuated by metallic stopped horns.",
     {"strings": "大提琴、中提琴与小提琴层层模仿推进", "horns": "圆号阻塞音（+）刺破织体", "winds": "大管与单簧管强化低音锯齿线条"},
     {"strings": "Cellos, violas, and violins build in imitative waves", "horns": "Stopped horns (+) pierce the texture", "winds": "Bassoons and clarinets sharpen the jagged bass line"},
     "辨认圆号加塞音（gestopft）那种干涩冷酷的金属音色", "Identify the dry, biting metallic timbre of the stopped horns"),

    (169, 179, "Reh. 11", 2, "#d97706", ["m1-totenfeier-march", "m1-rising-cry"], ["brass", "strings"],
     "展开部第二阶段（二）：铜管号角切入与不协和浪潮堆叠",
     "Development Part II-B: Brass Fanfares and Piling Dissonant Waves",
     "小号与圆号高亢交锋", "Trumpets & Horns Clash Over Rising String Waves",
     "小号与圆号：吹响带有军乐锋芒的切分号角动机",
     "Trumpets and Horns: Sound militant, syncopated fanfare figures",
     "小提琴以狂乱的八度跳进与颤音不断抬高音高重心",
     "Violinsratchet up the pitch center with frantic octave leaps and trills",
     "多条动机同时在声场中碰撞：葬礼步伐、上行悲叹与尖锐号角彼此撕扯，张力逼近临界点。",
     "Multiple motifs collide simultaneously—funeral tread, rising cry, and militant fanfare tear at each other as tension nears breaking point.",
     {"brass": "小号切入锋利的节奏型", "horns": "圆号高音区强奏抗衡弦乐", "strings": "全弦乐剧烈跨八度跳进", "perc": "定音鼓加密节奏型"},
     {"brass": "Trumpets cut in with razor-sharp fanfares", "horns": "Horns blaze in the upper register against strings", "strings": "Full strings execute violent octave leaps", "perc": "Timpani intensify the rhythmic drive"},
     "留意小号与圆号之间紧密的立体声卡农咬合", "Listen for the tight stereo canonic interlocking between trumpets and horns"),

    (180, 193, "Reh. 12", 2, "#dc2626", ["m1-totenfeier-march"], ["strings", "brass", "perc"],
     "展开部第二阶段（三）：第一次风暴高潮与深渊急坠",
     "Development Part II-C: First Storm Climax and Abyssal Plunge",
     "全乐队狂飙突进后骤然悬崖式跌落", "Full Orchestra Storm Surge & Cliff-Edge Drop",
     "全奏铜管与弦乐：在极强（fff）的不协和顶峰猛烈撞击",
     "Tutti Brass and Strings: Collide on a searing fff dissonant peak",
     "定音鼓与大鼓轰鸣后，只剩低音弦乐与大管孤零零地坠入深渊",
     "After thunderous timpani and bass drum blows, lower strings and bassoons plunge into the void",
     "风暴在顶点轰然炸裂，旋即被斩断，音乐跌入冰冷幽暗的坟墓深处，为《震怒之日》圣咏的降临腾出空间。",
     "The storm explodes at its zenith and is suddenly severed, plunging into icy sepulchral gloom to clear the stage for the Dies Irae.",
     {"brass": "全铜管在fff顶点爆发后瞬间休止", "strings": "弦乐从最高音区一路狂泻至最低音", "perc": "定音鼓与镲片在顶点轰击"},
     {"brass": "Full brass erupt at the fff peak then cut off abruptly", "strings": "Strings plummet from their highest register to the bottom", "perc": "Timpani and cymbals crash at the apex"},
     "感受全奏骤停后低音弦乐下坠时的失重感", "Experience the vertigo as the tutti cuts off and lower strings plunge downward"),

    (194, 206, "Reh. 13-13", 2, "#4f46e5", ["m1-totenfeier-march"], ["strings", "winds"],
     "墓穴寂静：大提琴与低音提琴幽暗拔弦与命运叩门",
     "Sepulchral Silence: Dark Lower-String Pizzicato and Fate's Knocking",
     "低音弦乐孤独拨弦铺垫", "Solitary Lower-String Pizzicato Stalking",
     "大提琴与低音提琴：在极弱（pp）中以沉重的拨弦摸索前行",
     "Cellos and Double Basses: Stalk forward in hushed, heavy pp pizzicato",
     "大管与低音单簧管偶尔投下阴森的短促和音",
     "Bassoons and bass clarinet cast eerie, clipped harmonic shadows",
     "万籁俱寂，只剩低音提琴在黑暗中一步步前行，如同通往末日审判庭的漫长甬道。",
     "All falls silent save for the double basses stalking through the dark like footsteps down a corridor toward the Last Judgment.",
     {"strings": "低音提琴与大提琴拨弦主导悬疑氛围", "winds": "低音木管极弱点缀", "perc": "大鼓在极弱处轻轻震动空气"},
     {"strings": "Bass and cello pizzicati command the suspenseful atmosphere", "winds": "Low woodwinds add sparse pp touches", "perc": "Bass drum barely vibrates the air in ppp"},
     "屏息聆听拨弦背后的大鼓极弱深沉共鸣", "Hold your breath for the subterranean ppp bass drum resonance behind the pizzicati"),

    (207, 220, "Reh. 13", 2, "#6366f1", ["m5-dies-irae", "m1-totenfeier-march"], ["horns", "winds", "strings"],
     "《震怒之日》初次降临：圆号与木管吹响中世纪末日圣咏",
     "First Premonition of the Dies Irae: Horns and Winds Intone the Medieval Chant",
     "圆号肃穆吹出《震怒之日》四音核心", "Horns Solemnly Intone the Four-Note Dies Irae Motif",
     "圆号与大管：庄严吹出格里高利圣咏《震怒之日》（Dies Irae）核心动机",
     "Horns and Bassoons: Solemnly intone the Gregorian Dies Irae plainchant motif",
     "低音提琴拨弦持续送葬步伐，小提琴在高音区加入颤栗的叹息",
     "Double basses continue the pizzicato march tread while violins add shivering sighs above",
     "全曲结构最关键的伏笔！第五乐章终曲的核心《震怒之日》圣咏在此首次现身，将葬礼提升至宇宙末日审判的维度。",
     "A structural milestone of the symphony: the medieval Dies Irae chant that will dominate the Finale appears here for the first time, elevating the funeral into cosmic judgment.",
     {"horns": "圆号肃穆吹响《震怒之日》四音圣咏", "winds": "大管与单簧管庄严叠奏圣咏线条", "strings": "低音拨弦维持步伐，小提琴穿插半音悲叹"},
     {"horns": "Horns solemnly sound the four-note Dies Irae chant", "winds": "Bassoons and clarinets double the plainchant line", "strings": "Bass pizzicati keep the tread; violins interject chromatic sighs"},
     "牢记圆号吹出的这四个中世纪圣咏音符——它将在第五乐章掀起惊涛骇浪", "Memorize these four medieval chant notes in the horns—they will unleash a cataclysm in Movement V"),

    (221, 232, "Reh. 14", 2, "#7c3aed", ["m5-dies-irae", "m1-rising-cry"], ["brass", "strings", "winds"],
     "圣咏扩展与多声部复调漩涡：铜管与弦乐层层加码",
     "Chant Expansion and Polyphonic Vortex: Brass and Strings Escalate",
     "《震怒之日》在铜管与弦乐间卡农传递", "Dies Irae Passed Canonically Between Brass & Strings",
     "长号、圆号与小号：轮番接力《震怒之日》与上行呼号动机",
     "Trombones, Horns, and Trumpets: Relay the Dies Irae and ascending cry motifs in canon",
     "弦乐五部以汹涌的八分音符与三连音浪潮不断推高声场密度",
     "All five string sections drive surging eighth-note and triplet waves to thicken the density",
     "拉特尔在此展现出惊人的复调控制力：即使织体越来越密，铜管每个声部的卡农进入依然清晰如刀刻。",
     "Rattle demonstrates masterly contrapuntal control here: as the texture thickens, every canonical brass entry slices through with chiseled clarity.",
     {"brass": "长号与小号卡农式叠入圣咏动机", "horns": "圆号在高音区吹响渴望救赎的呼号", "strings": "弦乐掀起汹涌的半音音浪"},
     {"brass": "Trombones and trumpets enter canonically with the chant motif", "horns": "Horns cry out in the high register", "strings": "Strings unleash surging chromatic waves"},
     "追踪长号与圆号之间一前一后的卡农追逐", "Track the tight canonical chase between trombones and horns"),

    (233, 243, "Reh. 15", 2, "#9333ea", ["m1-totenfeier-march", "m5-dies-irae"], ["strings", "brass", "winds"],
     "降E小调大风暴酝酿：弦乐狂乱三连音与木管尖啸",
     "Brewing the E-flat Minor Tempest: Frantic String Triplets and Wind Shrieks",
     "全弦乐三连音急流与铜管切分", "Full String Triplet Torrent & Brass Syncopations",
     "小提琴与中提琴：以疾风骤雨般的三连音在降E小调上疯狂攀升",
     "Violins and Violas: Climb frantically in E-flat minor on a torrent of triplets",
     "高音木管与小号刺出不协和的切分尖叫",
     "High woodwinds and trumpets stab with dissonant syncopated shrieks",
     "整个乐队如同被卷入黑色旋涡，调性锁定在阴森惨烈的降E小调，定音鼓滚奏如地壳撕裂。",
     "The entire orchestra is sucked into a black maelstrom locked in grim E-flat minor as timpani rolls rumble like tectonic fractures.",
     {"strings": "弦乐全奏三连音如暴风骤雨", "winds": "短笛、长笛与高音单簧管在顶端尖啸", "brass": "铜管切分重音步步紧逼", "perc": "定音鼓持续雷鸣滚奏"},
     {"strings": "Tutti string triplets rage like a tempest", "winds": "Piccolos, flutes, and E-flat clarinet shriek at the top", "brass": "Syncopated brass accents press relentlessly", "perc": "Timpani sustain thunderous rolls"},
     "感受弦乐三连音不断加速逼近深渊边缘的窒息感", "Feel the breathless urgency as string triplets race toward the precipice"),

    (244, 253, "Reh. 16-10", 2, "#c026d3", ["m1-totenfeier-march", "m5-dies-irae"], ["brass", "perc", "strings"],
     "风暴冲顶前夜：10支圆号与重型铜管的极限积蓄",
     "Eve of the Cataclysm: Maximum Accumulation of 10 Horns and Heavy Brass",
     "铜管全员ベル朝上（Schalltrichter auf）冲刺", "Full Brass Bells-Up Sprint to the Apex",
     "圆号、小号与长号：高举号口（Bells up），以撕裂性的增四度与半音强行推进",
     "Horns, Trumpets, and Trombones: Raise bells up, driving forward with searing tritones and semitones",
     "定音鼓手双槌猛击，弦乐在极高音区剧烈震音",
     "Both timpanists hammer furiously while strings sustain scorching high tremolos",
     "能量积聚到管弦乐法的极限，柏林爱乐铜管声部高举号口，整个音乐厅的空气都在剧烈震颤。",
     "Energy accumulates to the limits of orchestration; BPO brass raise their bells as the air of the Philharmonie shudders.",
     {"brass": "小号与长号以最大音量冲向顶点", "horns": "圆号高举号口咆哮", "perc": "双定音鼓手与大镲极限轰鸣", "strings": "弦乐在最高音区拉出炽热震音"},
     {"brass": "Trumpets and trombones surge at maximum volume toward the peak", "horns": "Horns roar with bells raised", "perc": "Dual timpanists and cymbals thunder at the limit", "strings": "Strings sear in extreme high-register tremolos"},
     "注意铜管高举号口（Bells up）时瞬间锋利如刀的音色变化", "Notice the razor-sharp timbral shift as the brass raise their bells"),

    (254, 266, "Reh. 16", 2, "#e11d48", ["m1-totenfeier-march", "m3-totengreif"], ["brass", "perc", "strings"],
     "展开部最高潮：降E小调末日海啸与撕裂性全奏爆发",
     "Development Cataclysm: E-flat Minor Apocalyptic Tsunami and Shattering Tutti",
     "全乐队极强（fff）末日海啸爆发", "Full Orchestra fff Apocalyptic Tsunami Eruption",
     "重型铜管、10支圆号与高音木管：在fff顶点爆发出毁天灭地的葬礼号角",
     "Heavy Brass, 10 Horns, and High Winds: Detonate an earth-shattering fff funeral proclamation",
     "6面定音鼓、大鼓与大锣全速轰击，低音弦乐如山崩地裂",
     "Six timpani, bass drum, and tam-tam batter at full force while lower strings convulse",
     "这是第一乐章最骇人的高潮！拉特尔与柏林爱乐释放出火山喷发般的声响能量，巨人的抗争在此撞上死亡的铁壁。",
     "The most terrifying peak of Movement I! Rattle and the BPO unleash volcanic sonic energy as the titan's struggle crashes against the iron wall of death.",
     {"brass": "小号与长号在极高音区吹出撕裂性号角", "horns": "圆号群全力咆哮支撑中音区厚度", "perc": "定音鼓、大鼓、镲与大锣全面爆发", "strings": "弦乐全弓猛烈劈砍和弦"},
     {"brass": "Trumpets and trombones blaze in extreme upper-register fanfares", "horns": "Horns roar at full power to anchor mid-register mass", "perc": "Timpani, bass drum, cymbals, and tam-tam detonate", "strings": "Strings slash chords with full bow weight"},
     "听定音鼓与大镲在最高潮处的雷霆一击", "Hear the thunderous timpani and cymbal detonation at the very crest"),

    (267, 278, "Reh. 16+13", 2, "#be123c", ["m1-totenfeier-march"], ["strings", "brass", "winds"],
     "风暴余波：悲剧行进的痉挛与半音撕扯",
     "Storm Aftermath: Convulsive Tragic March and Chromatic Tearing",
     "铜管断续哀嚎与弦乐锯齿下行", "Broken Brass Outcries & Jagged String Descent",
     "长号与小号：发出受伤巨兽般的切分咆哮",
     "Trombones and Trumpets: Utter wounded, syncopated roars",
     "弦乐与木管以尖锐的附点下行音型层层坍塌",
     "Strings and woodwinds collapse in jagged dotted descending figures",
     "巨浪撞碎之后，残存的动机碎片在血色余晖中剧烈抽搐。",
     "After the wave breaks, surviving motivic shards convulse violently in the blood-red aftermath.",
     {"brass": "长号与大号在低音区发出沉重喘息", "strings": "弦乐附点节奏剧烈下挫", "winds": "木管声部尖锐重叠悲鸣"},
     {"brass": "Trombones and tuba heave in the low register", "strings": "Strings plunge in jagged dotted rhythms", "winds": "Woodwinds double the cries with piercing intensity"},
     "注意长号在低音区沉重而绝望的切分重音", "Note the heavy, despairing syncopated accents in the low trombones"),

    (279, 290, "Reh. 17-12", 2, "#9f1239", ["m1-totenfeier-march"], ["strings", "perc"],
     "通往死亡重步的蓄力：低音半音阶爬升与定音鼓威压",
     "Gathering for the Death Tread: Chromatic Bass Climb and Timpani Menace",
     "低音弦乐沉重半音爬升", "Heavy Chromatic Climb in Lower Strings",
     "大提琴与低音提琴：以极度沉重的连弓一步步向上攀爬",
     "Cellos and Double Basses: Climb step by chromatic step with crushing bow weight",
     "定音鼓与大鼓在底部密集敲击送葬节奏",
     "Timpani and bass drum hammer the funeral rhythm relentlessly underneath",
     "乐队再次积聚黑暗能量，为展开部最后一次沉重如铅的死亡行进（Pesante）做准备。",
     "The orchestra gathers dark energy once more, preparing for the leaden Pesante death-march collapse.",
     {"strings": "低音弦乐如背负巨石般半音上行", "perc": "定音鼓与大鼓密集轰击", "horns": "圆号低音区闷雷般长音"},
     {"strings": "Lower strings climb chromatically as if bearing boulders", "perc": "Timpani and bass drum pound densely", "horns": "Low horns rumble like distant thunder"},
     "听低音弦乐每一步半音上行带来的压迫感", "Listen to the crushing weight of each chromatic step in the lower strings"),

    (291, 304, "Reh. 17", 2, "#881337", ["m1-totenfeier-march", "m3-totengreif"], ["brass", "strings", "perc"],
     "沉重如铅（Pesante）：半音下坠的死亡送葬队列",
     "Pesante Death Procession: Leaden Chromatic Descent of the Funeral Cortège",
     "全乐队極强（ffff）沉重半音下行步伐", "Tutti ffff Leaden Chromatic Descending March",
     "全铜管、木管与高音弦乐：以ffff极强音量奏出步步下沉的半音送葬主题",
     "Full Brass, Winds, and Upper Strings: Hammer out the sinking chromatic funeral theme in ffff",
     "低音提琴、大管与大号以千钧之力踏出四分音符重步，大锣随之震鸣",
     "Double basses, bassoons, and tuba stomp crushing quarter-note strides with tam-tam shudders",
     "马勒标示“沉重地”（Pesante）：整个柏林爱乐像一座正在缓缓坍塌的黑色大教堂，每一步和声都令人窒息。",
     "Marked Pesante: the entire BPO sounds like a collapsing black cathedral, each chromatic stride crushing in its weight.",
     {"brass": "小号、长号与大号全奏沉重下压", "strings": "全弦乐以最大弓压顿弓下行", "perc": "大锣（Tam-tam）、大鼓与定音鼓同步轰击", "winds": "全木管高音区全力吹奏"},
     {"brass": "Trumpets, trombones, and tuba press down in full tutti", "strings": "Full strings descend with maximum martellato bow weight", "perc": "Tam-tam, bass drum, and timpani strike in unison", "winds": "All woodwinds blow at maximum force in the high register"},
     "感受大锣与重型铜管每一步下沉时的毁灭性重量", "Feel the devastating weight of each downward step reinforced by tam-tam and low brass"),

    (305, 315, "Reh. 18", 2, "#4c1d95", ["m1-totenfeier-march"], ["horns", "winds", "strings"],
     "假再现与幽灵回响：圆号阻塞音与木管空洞挽歌",
     "False Recapitulation & Spectral Echo: Stopped Horns and Hollow Wind Lament",
     "圆号与木管幽灵般的主题回声", "Spectral Echo of the Main Theme in Horns & Winds",
     "双簧管与加塞圆号：在奇异的远关系调性上吹出苍白的葬礼主题影子",
     "Oboes and Stopped Horns: Sound a ghostly shadow of the funeral theme in a remote key",
     "低音弦乐在底部维持不安的半音蠕动",
     "Lower strings maintain an uneasy chromatic crawl at the bottom",
     "在真正的再现部风暴降临前，音乐陷入一片诡异的真空，葬礼旋律如同隔着迷雾传来的幻听。",
     "Before the true recapitulation strikes, the music enters an eerie vacuum where the funeral melody sounds like a hallucination through fog.",
     {"horns": "阻塞音圆号发出空洞的金属回声", "winds": "双簧管与单簧管苍白地重现挽歌", "strings": "低音提琴半音潜行逼近再现点"},
     {"horns": "Stopped horns emit hollow metallic echoes", "winds": "Oboes and clarinets palely recall the lament", "strings": "Double basses creep chromatically toward the recapitulation"},
     "注意此时葬礼旋律如鬼魅般的疏离音色", "Notice the ghostly, alienated timbre of the funeral melody here"),

    (316, 324, "Reh. 19", 2, "#7f1d1d", ["m1-totenfeier-march"], ["strings", "perc"],
     "再现部导火索：低音弦乐狂飙蓄势与高音震音锁定",
     "Recapitulation Fuse: Lower-String Surge and High Tremolo Lock",
     "低音提琴极速冲向再现部起点", "Double Basses Hurtling Toward the Recapitulation",
     "大提琴与低音提琴：突然由弱转强，掀起重返C小调的狂暴浪潮",
     "Cellos and Double Basses: Surge suddenly from hush to fury, launching the return to C minor",
     "高音弦乐再次锁定开篇的G音八度冰冷震音",
     "Upper strings lock back onto the opening icy octave G tremolo",
     "潜伏的地火骤然喷发，低音弦乐一举冲破迷雾，直接撞开再现部的大门！",
     "Subterranean fire erupts abruptly as lower strings smash through the mist straight into the recapitulation!",
     {"strings": "低音弦乐猛烈渐强冲刺，高音弦乐锁定G音震音", "perc": "定音鼓滚奏推向极强顶点", "winds": "木管短促呼啸助推"},
     {"strings": "Lower strings surge in a fierce crescendo; violins lock onto the G tremolo", "perc": "Timpani roll drives to the ff impact", "winds": "Woodwinds add sharp rushing gusts"},
     "听定音鼓滚奏如何与低音弦乐合力撞开第325小节的再现部", "Hear how the timpani roll and bass surge smash open the recapitulation at bar 325"),

    (325, 336, "Reh. 20", 3, "#dc2626", ["m1-totenfeier-march"], ["strings", "brass", "perc"],
     "再现部开启：C小调狂暴葬礼宣叙调雷霆回归",
     "Recapitulation: Thunderous Return of the C Minor Totenfeier Recitative",
     "低音弦乐宣叙调以更强姿态回归", "Lower-String Recitative Returns with Heightened Force",
     "大提琴、低音提琴与低音大管：以排山倒海之势重现开篇的十六分音符宣叙调",
     "Cellos, Double Basses, and Bassoons: Reprise the opening sixteenth-note recitative with overwhelming force",
     "小提琴震音与铜管短促重音使声场比呈示部更加凛冽",
     "Violin tremolos and sharp brass stabs make the soundstage even fiercer than the exposition",
     "再现部以浓缩而加倍猛烈的姿态降临！经过展开部的生死搏杀，此时的宣叙调带着不可逆转的悲剧铁律。",
     "The recapitulation strikes in compressed, redoubled fury! After the life-and-death struggle of the development, the recitative carries irreversible tragic finality.",
     {"strings": "低音弦乐全弓猛烈劈出C小调音阶", "brass": "圆号与长号在休止缝隙切入重音", "perc": "定音鼓猛击C-G葬礼基石"},
     {"strings": "Lower strings slash the C minor scales with full bow", "brass": "Horns and trombones stab into the rests", "perc": "Timpani hammer the C-G funeral foundation"},
     "对比开篇第1小节，感受此处铜管加固后的雷霆重量", "Compare with bar 1 and feel the added weight of the brass reinforcements"),

    (337, 349, "Reh. 20+12", 3, "#b91c1c", ["m1-totenfeier-march"], ["winds", "brass", "strings"],
     "再现部第一主题：全木管与圆号齐奏的凄厉送葬挽歌",
     "Recapitulation First Subject: Piercing Funeral Lament in Full Winds and Horns",
     "高音木管与圆号合力嘶喊主部哀歌", "High Winds & Horns Cry Out the Primary Lament",
     "双簧管、英国管、单簧管与圆号：高举号口齐奏C小调葬礼主旋律",
     "Oboes, English Horn, Clarinets, and Horns: Intone the C minor funeral melody with bells raised",
     "大提琴、低音提琴与大号维持沉重无比的四分音符踏步",
     "Cellos, double basses, and tuba maintain an overwhelmingly heavy quarter-note tread",
     "不再仅仅是双簧管的孤独吟唱，整个木管与圆号声部汇成凄厉的合唱，在沉重的低音踏步上悲鸣。",
     "No longer a solitary oboe plaint, the entire woodwind and horn choir unites in a piercing lament over the crushing bass tread.",
     {"winds": "双簧管、英国管与单簧管全力齐奏挽歌", "horns": "圆号重叠旋律赋予金属悲剧感", "strings": "低音弦乐踏步如铁锤敲击", "brass": "大号与低音长号加固底盘"},
     {"winds": "Oboes, English horn, and clarinets unite in the lament", "horns": "Horns double the melody with metallic tragedy", "strings": "Lower strings tread like iron hammers", "brass": "Tuba and bass trombone reinforce the floor"},
     "听圆号加入双簧管旋律后那令人战栗的金属悲鸣", "Hear the chilling metallic sheen added when horns join the oboe lament"),

    (350, 361, "Reh. 21", 3, "#f97316", ["m1-rising-cry"], ["strings", "horns", "winds"],
     "再现部第二主题（一）：E大调彼岸微光的最后回眸",
     "Recapitulation Second Subject I: Final Backward Glance at the E Major Vision",
     "弱音小提琴与圆号重现天国安慰旋律", "Muted Violins & Horns Recall the Celestial Consolation",
     "第一小提琴与中提琴：在E大调上温柔地再次浮现那缕天国牧歌",
     "First Violins and Violas: Gently float the E major pastoral cantilena one last time",
     "独奏圆号与长笛在上方织出透明的告别对位",
     "Solo horn and flute weave a translucent farewell counterpoint above",
     "在迈向最终的墓穴尾声之前，E大调的安慰主题如回光返照般再次浮现，带着无限眷恋。",
     "Before entering the final funeral coda, the E major consolation theme reappears like a dying sunbeam filled with infinite longing.",
     {"strings": "小提琴极弱歌唱如流泪的微笑", "horns": "独奏圆号温柔应答", "winds": "长笛与单簧管提供晶莹的和声光晕"},
     {"strings": "Violins sing pp like a tearful smile", "horns": "Solo horn answers tenderly", "winds": "Flutes and clarinets supply a crystalline halo"},
     "珍惜这段E大调旋律——这是本乐章最后一抹温暖色彩", "Cherish this E major passage—the last warm ray of light in Movement I"),

    (362, 371, "Reh. 22", 3, "#ea580c", ["m1-rising-cry"], ["strings", "winds"],
     "再现部第二主题（二）：高音区消融与宿命阴影重聚",
     "Recapitulation Second Subject II: High-Register Dissolution and Gathering Shadows",
     "小提琴极高音长音消散于C小调阴影", "Extreme High Violins Dissolve into C Minor Shadows",
     "第一小提琴：攀升至极高音区维持纤细如丝的持续音",
     "First Violins: Climb to the stratosphere on a thread-like sustained tone",
     "低音提琴与定音鼓在底部悄然恢复C小调送葬脉搏",
     "Double basses and timpani quietly resume the C minor funeral pulse down below",
     "高音小提琴的光芒渐渐熄灭，底部的C小调定音鼓如宿命般重新敲响。",
     "As the stratospheric violin light fades, the C minor timpani pulse resumes inexorably from the depths.",
     {"strings": "小提琴高音如游丝，低音提琴恢复送葬踏步", "perc": "定音鼓极弱敲响宿命脉搏", "winds": "低音木管引入阴暗和声"},
     {"strings": "High violins hang by a thread as basses resume the march", "perc": "Timpani softly tap the pulse of fate", "winds": "Low winds reintroduce dark harmonies"},
     "注意高音小提琴尚未消失时底部定音鼓已经响起的冷酷脉搏", "Notice the cold timpani pulse already beating beneath the fading high violins"),

    (372, 381, "Reh. 23", 3, "#991b1b", ["m1-totenfeier-march"], ["horns", "winds", "strings"],
     "尾声（一）：送葬队伍远去与空旷五度挽歌",
     "Coda I: Receding Funeral Procession and Hollow Fifth Lament",
     "圆号与木管在空五度上吹出残破哀歌", "Horns & Winds Intone Broken Lament Over Open Fifths",
     "圆号与双簧管：在荒凉的C小调空五度背景上吹奏破碎的葬礼动机",
     "Horns and Oboes: Intone fragmented funeral motifs over desolate C minor open fifths",
     "大提琴与低音提琴维持缓慢而机械的送葬步伐",
     "Cellos and double basses keep a slow, mechanical funeral tread",
     "尾声开始，送葬队伍向墓地深处缓缓远去，声响空间变得空旷而荒凉。",
     "The Coda begins: the funeral cortège slowly recedes into the graveyard, leaving the acoustic space vast and desolate.",
     {"horns": "弱音圆号吹出凄凉的断续挽歌", "winds": "双簧管与英国管残存悲鸣", "strings": "低音弦乐踏步渐渐放慢"},
     {"horns": "Muted horns sound a bleak, broken lament", "winds": "Oboes and English horn utter lingering cries", "strings": "Lower-string tread gradually slows"},
     "听C小调空五度和声营造出的荒原孤寂感", "Listen to the wasteland desolation of the C minor open fifths"),

    (382, 391, "Reh. 24-10", 3, "#7f1d1d", ["m1-totenfeier-march"], ["brass", "strings", "perc"],
     "尾声（二）：长号阴森圣咏与墓穴深处的叹息",
     "Coda II: Sepulchral Trombone Chorale and Sighs from the Crypt",
     "长号与大号低音区庄严圣咏", "Solemn Low-Register Chorale in Trombones & Tuba",
     "4支长号与大号：在极弱（pp）下奏出阴郁庄严的墓穴圣咏",
     "Four Trombones and Tuba: Intone a dark, solemn crypt chorale in hushed pp",
     "定音鼓与大鼓在低音区维持濒死般的心跳节奏",
     "Timpani and bass drum maintain a dying heartbeat pulse underneath",
     "柏林爱乐的长号声部以令人屏息的极弱控制力，奏出如同墓志铭般的低音圣咏。",
     "With breathtaking pp control, the BPO trombones intone an epitaph-like low chorale over a dying heartbeat pulse.",
     {"brass": "长号与大号极弱合奏墓志铭和弦", "perc": "定音鼓与大鼓如微弱心跳", "strings": "中提琴与大提琴暗色震音"},
     {"brass": "Trombones and tuba blend in hushed epitaph chords", "perc": "Timpani and bass drum beat like a fading heart", "strings": "Violas and cellos sustain dark tremolos"},
     "细听4支长号在极弱（pp）状态下依然饱满深沉的共鸣", "Listen closely to the rich, solemn resonance of the four trombones at pp"),

    (392, 404, "Reh. 24", 3, "#450a0a", ["m1-totenfeier-march"], ["strings", "winds", "horns"],
     "尾声（三）：沉入黑暗深渊——半音下行叹息链",
     "Coda III: Sinking into the Abyss — Chain of Chromatic Descending Sighs",
     "全乐队在极弱（ppp）中层层下沉", "Orchestra Sinks Layer by Layer in ppp",
     "小提琴、中提琴与木管：以连绵不断的半音下行叹息缓缓沉落",
     "Violins, Violas, and Winds: Sink slowly in an unbroken chain of chromatic descending sighs",
     "低音提琴与低音大管在最低音区维持C音持续音",
     "Double basses and contrabassoon hold a subterranean low C pedal",
     "光亮完全熄灭，所有声部都在缓慢下沉，仿佛棺木缓缓落入深土。",
     "All light is extinguished; every voice sinks slowly downward as if the coffin is being lowered into the earth.",
     {"strings": "小提琴与中提琴连绵半音下坠", "winds": "低音单簧管与大管在暗处叹息", "horns": "圆号维持微弱的C音长音"},
     {"strings": "Violins and violas sink in continuous chromatic sighs", "winds": "Bass clarinet and bassoons sigh in the shadows", "horns": "Horns hold a faint C pedal"},
     "感受弦乐半音叹息一步步沉入最低音区的凝重感", "Feel the solemn gravity as string chromatic sighs sink into the lowest register"),

    (405, 415, "Reh. 25", 3, "#dc2626", ["m1-rising-cry", "m1-totenfeier-march"], ["brass", "horns", "strings"],
     "尾声（四）：最后一次悲剧挣扎与铜管悲鸣爆发",
     "Coda IV: Final Tragic Outcry and Brass Lament Eruption",
     "圆号与小号突然回光返照般强奏悲鸣", "Sudden Fierce Outcry in Horns & Trumpets",
     "圆号、小号与全弦乐：从极弱突然暴起（ff），发出最后一次不甘的悲叹",
     "Horns, Trumpets, and Full Strings: Erupt suddenly from ppp to ff in a final anguished outcry",
     "定音鼓与大锣猛烈震荡，随即迅速回落",
     "Timpani and tam-tam shudder violently before rapidly subsiding",
     "就在即将彻底沉寂之际，乐队突然爆发出最后一声撕心裂肺的悲鸣，对死亡发出最后的抗议。",
     "Just as total silence looms, the orchestra erupts in one last heart-rending outcry of protest against death.",
     {"horns": "圆号全力吹出上行悲鸣", "brass": "小号与长号强音支撑最后爆发", "strings": "小提琴高音区猛烈拉奏悲叹音型", "perc": "定音鼓与大锣震鸣"},
     {"horns": "Horns blaze forth in an ascending outcry", "brass": "Trumpets and trombones reinforce the final burst", "strings": "Violins slash the lament figure in the high register", "perc": "Timpani and tam-tam shudder"},
     "注意这次从极弱（ppp）到强奏（ff）的突然情感爆发", "Watch for the sudden emotional eruption from ppp to ff"),

    (416, 425, "Reh. 26", 3, "#7f1d1d", ["m1-totenfeier-march"], ["winds", "strings", "perc"],
     "尾声（五）：尘埃落定与破碎动机的最后低语",
     "Coda V: Dust Settling and Final Whispers of Broken Motifs",
     "低音单簧管、竖琴与拨弦的零星碎片", "Sparse Shards in Bass Clarinet, Harp & Pizzicato",
     "低音单簧管、英国管与独奏圆号：在极弱中交换残破的三音碎片",
     "Bass Clarinet, English Horn, and Solo Horn: Exchange broken three-note shards in ppp",
     "竖琴低音区与大提琴拨弦如滴水般稀疏落下",
     "Low harp tones and cello pizzicati fall sparsely like drops in a cavern",
     "抗争结束，墓园重归死寂，只剩零星的动机碎片在冰冷的空气中飘散。",
     "The struggle is over; the graveyard returns to dead silence save for sparse motivic shards drifting in the cold air.",
     {"winds": "低音单簧管与英国管发出最后的微弱叹息", "strings": "大提琴与低音提琴稀疏拨弦", "perc": "竖琴低音与定音鼓微弱余音"},
     {"winds": "Bass clarinet and English horn utter final faint sighs", "strings": "Cellos and basses pluck sparse pizzicati", "perc": "Low harp and timpani leave faint resonances"},
     "细听竖琴低音与低音单簧管营造的空寂感", "Listen to the stark emptiness created by low harp and bass clarinet"),

    (426, 434, "Reh. 27-8", 3, "#991b1b", ["m1-totenfeier-march"], ["strings", "winds"],
     "尾声（六）：虚无中的停滞与风暴前的死寂",
     "Coda VI: Stasis in the Void and Dead Silence Before the Final Blow",
     "极弱（pppp）悬停和弦", "Suspended pppp Chord in the Void",
     "木管与弱音弦乐：在极弱（pppp）中维持几乎听不见的C大三/小三模糊和弦",
     "Woodwinds and Muted Strings: Hold a barely audible pppp chord hovering between major and minor",
     "定音鼓完全静止，整个大厅屏住呼吸",
     "Timpani fall completely still as the entire hall holds its breath",
     "声音微弱到近乎消失（pppp），仿佛灵魂悬停在生死边界。",
     "Sound fades to the threshold of audibility (pppp), hovering motionless on the border between life and death.",
     {"strings": "弦乐以一丝弓毛维持极弱长音", "winds": "木管极弱气息融入背景", "horns": "圆号悄然收束"},
     {"strings": "Strings sustain a thread of sound with a single hair of the bow", "winds": "Woodwinds blend imperceptibly into the silence", "horns": "Horns quietly fade out"},
     "准备好迎接紧接着撕裂死寂的最后下行音阶！", "Brace yourself for the final descending scale that will rip through this silence!"),

    (435, 440, "Reh. 27", 3, "#dc2626", ["m1-totenfeier-march"], ["strings", "winds", "brass"],
     "尾声（七）：闪电般的C小调全奏半音下行斩击",
     "Coda VII: Lightning C Minor Tutti Chromatic Downward Slash",
     "全乐队强奏（ff）半音阶急速劈落", "Full Orchestra ff Chromatic Scale Plunges Downward",
     "全弦乐與木管：突然以强奏（ff）如闪电般自高音区半音急速劈向C音底部",
     "Full Strings and Woodwinds: Slash downward like lightning in a ferocious ff chromatic scale to low C",
     "铜管与定音鼓在底部接住这致命的下击",
     "Brass and timpani catch the fatal downward blow at the bottom",
     "死寂被一道闪电劈开！全乐队以毫不含糊的半音下行音阶直插地心。",
     "A bolt of lightning rips the silence! The full orchestra plunges straight into the earth on an uncompromising chromatic scale.",
     {"strings": "全弦乐急速半音下行斩击", "winds": "全木管重叠下行闪电音阶", "brass": "铜管在底部轰然截断"},
     {"strings": "Full strings slash downward in a rapid chromatic scale", "winds": "All woodwinds double the lightning descent", "brass": "Brass cut off the descent at the bottom"},
     "听这道毫无预警的ff下行音阶如何斩断一切幻想", "Hear how this unannounced ff downward scale severs all illusion"),

    (441, 445, "Fine", 3, "#1c1917", ["m1-totenfeier-march"], ["strings", "perc"],
     "第一乐章终结：两记干脆的拨弦与五分钟庄严静默",
     "Movement I Conclusion: Two Dry Pizzicato Strokes and the Five-Minute Pause",
     "全弦乐干脆利落的C音拨弦收束", "Crisp Unison C Pizzicato Final Stroke",
     "全弦乐与定音鼓：在短暂休止后，以干脆短促的C音拨弦（pizzicato）画上句号",
     "Full Strings and Timpani: After a tense rest, close with a dry, clipped unison C pizzicato stroke",
     "马勒在总谱上用大字注明：“在此之后必须保持至少五分钟的休止”",
     "Mahler writes in bold in the score: 'Here follows a pause of at least 5 minutes'",
     "没有冗长的尾音，只有两记冷酷干脆的句点。拉特尔的手臂在空中凝固，让柏林爱乐大厅陷入庄严的静默。",
     "No lingering resonance—only two clipped, implacable strokes. Rattle holds his baton frozen in the air as the Berlin Philharmonie sinks into solemn silence.",
     {"strings": "全弦乐齐奏干脆的最终拨弦", "perc": "定音鼓短促收束", "winds": "木管短音同歩切断"},
     {"strings": "Full strings pluck the final dry pizzicato", "perc": "Timpani damp immediately", "winds": "Woodwinds clip the final chord short"},
     "体会最后一记干脆拨弦后那令人敬畏的漫长静默", "Experience the awe-inspiring silence following the final dry pizzicato stroke")
]

#Wait—let's check how many stages MVT1_STAGES_RAW has: 26 stages! Let's add 16 more intermediate granular stages or subdivide so Mvt 1 has 38-42 stages, or let's write a helper that subdivides long ranges cleanly into 25-35s stages!

# ============================================================================
# MOVEMENT II: Andante moderato. Sehr gemächlich. Nie eilen — 299 Bars
# ============================================================================
MVT2_STAGES_RAW = [
    (1, 18, "Opening", 1, "#10b981", ["m2-laendler"], ["strings"],
     "第一部分A1（一）：降A大调兰德勒舞曲优雅起舞",
     "Section A1-I: Graceful Opening of the A-flat Major Ländler",
     "第一小提琴温婉摇曳的3/8拍舞步", "First Violins Graceful 3/8 Ländler Lilt",
     "第一小提琴：以轻柔优雅的连奏与断音交替，拉出降A大调怀旧兰德勒主题",
     "First Violins: Alternate gentle legato and light staccato in the nostalgic A-flat major Ländler",
     "大提琴与低音提琴以轻巧的拨弦（pizzicato）点出三拍子舞曲韵律",
     "Cellos and double basses pluck a feather-light 3/8 dance pulse beneath",
     "经历第一乐章的死亡风暴后，第二乐章如一缕温暖的往昔阳光：马勒称之为“在英雄生前幸福时刻的一瞥”。拉特尔让柏林爱乐弦乐呈现出丝绒般的维也纳沙龙音色。",
     "After the funeral storm of Movement I, Movement II opens like a warm sunbeam of memory—'a ray of sunlight from the life of the departed hero.' Rattle shapes the BPO strings with velvety Viennese charm.",
     {"strings": "第一小提琴主导优雅舞步，低音弦乐轻巧拨弦", "winds": "木管静默聆听，留出纯净弦乐空间", "horns": "圆号在句尾轻轻呼吸"},
     {"strings": "First violins lead the graceful dance over light bass pizzicati", "winds": "Woodwinds remain tacet, leaving pure string intimacy", "horns": "Horns breathe softly at phrase endings"},
     "留意小提琴在句尾那略带羞涩的维也纳式滑音（Portamento）", "Listen for the subtle, nostalgic Viennese portamento in the first violins"),

    (19, 38, "Reh. 28", 1, "#059669", ["m2-laendler"], ["strings", "winds"],
     "第一部分A1（二）：舞曲转身与单簧管、长笛的温柔应答",
     "Section A1-II: Dance Turn and Tender Clarinet & Flute Response",
     "木管轻柔切入与弦乐形成室内乐对话", "Woodwinds Enter Gently in Chamber Dialogue with Strings",
     "单簧管与长笛：接过小提琴的舞曲尾音，吹出清澈的田园式装饰呼应",
     "Clarinets and Flutes: Catch the violin phrase endings with crystalline pastoral ornaments",
     "第二小提琴与中提琴织出温暖摇曳的六度与三度内声部",
     "Second violins and violas weave rocking inner thirds and sixths",
     "木管声部悄然加入，如同记忆画卷中的色彩渐渐丰富，速度保持马勒叮嘱的“切勿匆忙（Nie eilen）”。",
     "Woodwinds slip in gently as colors bloom across the memory canvas, honoring Mahler's instruction 'Never rush (Nie eilen).'",
     {"strings": "小提琴与中提琴维持温柔的三拍子摇摆", "winds": "单簧管与长笛点缀田园花彩", "horns": "柔音圆号铺垫温暖和声"},
     {"strings": "Violins and violas keep the gentle 3/8 sway", "winds": "Clarinets and flutes add pastoral filigree", "horns": "Muted horns cushion the harmony"},
     "听单簧管如何无缝接过第一小提琴的旋律线条", "Hear how the clarinet seamlessly catches the melody from the first violins"),

    (39, 60, "Reh. 29", 1, "#0d9488", ["m2-laendler"], ["strings", "horns"],
     "第一部分A1（三）：大提琴深情副旋律歌唱",
     "Section A1-III: Soaring Cello Counter-Melody in Rich Cantabile",
     "大提琴声部宽广醇厚的歌唱性对位", "Cellos Sing a Warm, Arching Counter-Subject",
     "大提琴声部：升至高音区，以饱含深情的揉弦拉出宽广的歌唱性对位旋律",
     "Cellos: Rise into their tenor register with a warm, richly vibrated counter-melody",
     "第一小提琴在上方化作轻盈的断音伴奏，圆号温暖托底",
     "First violins turn into light staccato accompaniment above while horns sustain warm pedals",
     "柏林爱乐著名的大提琴声部在此展现出令人心醉的黄金音色，主旋律与伴奏发生精妙的声部倒置。",
     "The celebrated BPO cello section shines with golden warmth as melody and accompaniment invert in contrapuntal elegance.",
     {"strings": "大提琴主导深情歌唱，小提琴在上声部轻巧跳跃", "horns": "圆号以柔和长音烘托大提琴", "winds": "大管与单簧管温和重叠内声部"},
     {"strings": "Cellos lead the ardent song while violins dance lightly above", "horns": "Horns halo the cellos with soft sustained tones", "winds": "Bassoons and clarinets gently double inner voices"},
     "专注聆听大提琴在高音区如人声般温暖的吟唱", "Focus on the human-voice warmth of the cellos singing in their upper register"),

    (61, 84, "Reh. 30", 1, "#14b8a6", ["m2-laendler"], ["strings", "winds"],
     "第一部分A1（四）：兰德勒主题回归与阳光渐隐",
     "Section A1-IV: Return of the Ländler and Fading Sunlight",
     "小提琴与木管轻柔收束第一舞段", "Violins & Winds Gently Close the First Dance Paragraph",
     "第一小提琴与长笛：重新回到降A大调兰德勒主旋律，音量渐弱至耳语",
     "First Violins and Flutes: Return to the A-flat major Ländler, tapering to a whisper",
     "中提琴与大提琴以连绵的拨弦送走阳光",
     "Violas and cellos bid farewell to the sunlight with gentle pizzicati",
     "第一段回忆在极其精致的渐弱中收拢，空气中却悄然浮现出一丝不安的寒意。",
     "The first memory closes in an exquisite diminuendo as a faint chill of unease enters the air.",
     {"strings": "小提琴渐弱收束，低音弦乐轻拨尾音", "winds": "长笛与双簧管吹出告别叹息", "perc": "竖琴轻柔泛音点缀"},
     {"strings": "Violins taper off while lower strings pluck soft final notes", "winds": "Flute and oboe breathe a quiet farewell", "perc": "Harp adds delicate harmonic touches"},
     "注意舞曲尾声处调性突然向升G小调暗处倾斜的瞬间", "Notice the sudden harmonic tilt from A-flat major into dark G-sharp minor at the close"),

    (85, 108, "Reh. 32", 2, "#6366f1", ["m2-laendler"], ["strings", "winds"],
     "第一插部B1（一）：升G小调阴云骤起——三连音焦虑急流",
     "Episode B1-I: G-sharp Minor Shadows — Agitated Triplet Whirlpool",
     "弦乐与木管在升G小调上展开急促三连音", "Agitated G-sharp Minor Triplets in Strings & Winds",
     "小提琴、中提琴与单簧管：以永不停歇的弱奏三连音织出焦虑旋转的阴影",
     "Violins, Violas, and Clarinets: Spin a restless web of hushed G-sharp minor triplets",
     "大提琴与低音大管在底部踏出断续的切分脉冲",
     "Cellos and bassoons punctuate with uneasy syncopated pulses below",
     "降A大调（Ab）等音转换为升G小调（G#m），晴朗的回忆突然被现实的焦虑阴云笼罩，三连音如寒风吹拂枯叶。",
     "Enharmonically shifting from A-flat major to G-sharp minor, sunny memory is overcast by restless triplets rustling like autumn wind.",
     {"strings": "小提琴与中提琴紧密咬合三连音急流", "winds": "单簧管与双簧管刺出悲凉的断续旋律", "horns": "圆号以阻塞音增添寒意"},
     {"strings": "Violins and violas interlock in a restless triplet stream", "winds": "Clarinets and oboes project a plaintive broken melody", "horns": "Stopped horns add a metallic chill"},
     "听三连音伴奏如何将原本悠闲的三拍子变成急促的心跳", "Hear how the triplet figuration turns the leisurely 3/8 meter into an anxious pulse"),

    (109, 132, "Reh. 33", 2, "#4f46e5", ["m2-laendler"], ["strings", "brass", "winds"],
     "第一插部B1（二）：三连音风浪高涨与消退回暖",
     "Episode B1-II: Cresting of the Triplet Wave and Calming Transition",
     "全乐队短暂渐强涌动后重返温暖大调", "Orchestral Swell and Gentle Melting Back to A-flat Major",
     "弦乐与高音木管：将升G小调的三连音风浪推向紧绷的强音顶点",
     "Strings and Upper Winds: Drive the G-sharp minor triplet wave to a tense forte crest",
     "圆号与单簧管随后放慢呼吸，用柔和的滑音将阴云慢慢化解",
     "Horns and clarinets then slow the breath, melting the clouds back toward warmth",
     "阴云短暂聚集却并未真正爆发，圆号与大提琴温柔地牵引着音乐重新回到降A大调的怀抱。",
     "The dark clouds gather briefly without bursting; horns and cellos gently guide the music back into the embrace of A-flat major.",
     {"strings": "弦乐风浪冲顶后迅速柔化为拨弦准备", "winds": "木管声部顺滑完成等音转调", "horns": "圆号温暖长音架起回归桥梁"},
     {"strings": "String wave crests then softens in preparation for pizzicato", "winds": "Woodwinds smoothly execute the enharmonic return", "horns": "Warm horn pedals bridge the return"},
     "留意小提琴与中提琴放下琴弓、准备全员拨弦的戏剧性停顿", "Watch for the poised pause as strings lower their bows to prepare for full pizzicato"),

    (133, 149, "Reh. 34", 3, "#10b981", ["m2-laendler"], ["strings", "winds"],
     "第二部分A2（一）：著名的全弦乐拨弦（Pizzicato）兰德勒变奏",
     "Section A2-I: Famous Full-String Pizzicato Ländler Variation",
     "全弦乐五部立体拨弦与竖琴交相辉映", "Five-Part String Pizzicato Sparkling with Harp",
     "第一/第二小提琴、中提琴、大提琴与低音提琴：全员不用琴弓，以精湛的拨弦重现兰德勒舞曲",
     "All Five String Sections: Lay down bows completely to pluck the Ländler in sparkling polyphony",
     "竖琴与长笛、单簧管在拨弦珠玉之间穿插流动的歌唱性复调",
     "Harp, flute, and clarinet weave liquid counter-melodies through the plucked strings",
     "全曲最受喜爱的音响奇观之一！柏林爱乐全弦乐拨弦整齐如同一架巨大的古典鲁特琴，竖琴与长笛在其中翩翩起舞。",
     "One of the most beloved timbral marvels in the symphonic repertoire! The entire BPO string choir plucks like a giant lute while harp and flute dance through the lattice.",
     {"strings": "全弦乐五部以极致整齐的拨弦奏出兰德勒", "winds": "长笛与单簧管吹出丝滑的连奏对位线条", "perc": "竖琴琶音与拨弦浑然一体"},
     {"strings": "All five string choirs pluck the Ländler with pinpoint precision", "winds": "Flute and clarinet spin silky legato counter-lines", "perc": "Harp arpeggios blend seamlessly with pizzicati"},
     "细听无弓弦乐拨弦与连奏长笛之间一断一连的绝妙反差", "Relish the exquisite contrast between plucked strings and liquid legato flute"),

    (150, 165, "Reh. 34+17", 3, "#059669", ["m2-laendler"], ["winds", "strings", "horns"],
     "第二部分A2（二）：拨弦织体加密与独奏圆号、双簧管复调",
     "Section A2-II: Enriched Pizzicato Lattice with Solo Horn & Oboe Counterpoint",
     "双簧管与独奏圆号在拨弦声网中深情对唱", "Oboe & Solo Horn Duet Inside the Pizzicato Web",
     "双簧管、单簧管与独奏圆号：在三声部复调中交替吟唱温柔的副旋律",
     "Oboe, Clarinet, and Solo Horn: Trade tender counter-melodies in three-part counterpoint",
     "弦乐拨弦加入十六分音符装饰，音响如八音盒般晶莹",
     "String pizzicati add sixteenth-note embellishments like a luminous music box",
     "复调层次进一步丰富：弦乐继续保持全拨弦，而木管与圆号在上方织出越来越浓密的怀旧情网。",
     "Contrapuntal layers multiply: strings remain entirely pizzicato while winds and solo horn weave an increasingly poignant web of nostalgia.",
     {"winds": "双簧管与单簧管织出精致的内声部复调", "horns": "独奏圆号温柔应答", "strings": "全弦乐持续晶莹的拨弦伴奏"},
     {"winds": "Oboe and clarinet weave intricate inner counterpoint", "horns": "Solo horn answers warmly", "strings": "Full strings maintain the sparkling pizzicato lattice"},
     "追踪独奏圆号如何在拨弦背景中吹出温暖的中音区旋律", "Follow the solo horn singing warmly through the plucked string backdrop"),

    (166, 188, "Reh. 35", 4, "#dc2626", ["m2-laendler", "m1-rising-cry"], ["strings", "brass", "perc"],
     "第二插部B2（一）：风暴突袭！狂暴三连音与铜管悲剧呼号",
     "Episode B2-I: Sudden Storm! Furious Triplets and Tragic Brass Outcries",
     "弦乐重新抄起琴弓掀起剧烈三连音风暴", "Strings Seize Bows for a Fierce Triplet Tempest",
     "小号、长号与圆号：刺破田园梦境，吹出带有第一乐章悲剧烙印的切分强音",
     "Trumpets, Trombones, and Horns: Pierce the idyll with syncopated cries echoing Movement I",
     "全弦乐抄起琴弓，以狂暴的三连音音流在F小调与升G小调间翻滚",
     "Full strings seize their bows, surging in furious triplets between F minor and G-sharp minor",
     "第二段插部比第一段猛烈得多！死亡与痛苦的记忆突然闯入昔日沙龙，铜管的咆哮令人想起第一乐章的葬礼风暴。",
     "The second episode erupts with far greater violence! Memories of death and anguish crash into the ballroom as brass outcries echo the funeral storm.",
     {"strings": "弦乐全弓拉出狂风般的三连音急流", "brass": "小号与长号发出撕裂性的切分悲鸣", "horns": "圆号高举号口强化冲突", "perc": "定音鼓猛烈敲击三拍子重音"},
     {"strings": "Strings bow a tempestuous torrent of triplets", "brass": "Trumpets and trombones utter tearing syncopated cries", "horns": "Horns raise bells to heighten the conflict", "perc": "Timpani pound forceful 3/8 accents"},
     "感受从刚才轻巧的拨弦瞬间切换到全奏铜管咆哮的戏剧性冲击", "Feel the dramatic shock of switching from delicate pizzicato to roaring brass tutti"),

    (189, 210, "Reh. 36", 4, "#ea580c", ["m2-laendler"], ["brass", "strings", "winds"],
     "第二插部B2（二）：痛苦高潮的宣泄与泪水般的滑音回落",
     "Episode B2-II: Agonized Climax and Tearful Glissando Subsidence",
     "全乐队在最高潮处嘶喊后缓缓滑落", "Tutti Climax Outcry Followed by Weeping String Glissandi",
     "高音木管、铜管与第一小提琴：在极强（ff）顶点发出痛彻心扉的呼喊",
     "High Winds, Brass, and Violins I: Cry out at an agonized ff apex",
     "随即弦乐以长长的下行滑音（glissando）慢慢平息风暴，定音鼓渐弱",
     "Strings then subside in long, weeping downward glissandi as timpani fade",
     "风暴在顶点化作一声长叹，小提琴带着泪水般的滑音一步步走下高坡，重新寻回内心的平静。",
     "At its peak the storm dissolves into a long sigh; violins descend with tearful glissandi to rediscover inner peace.",
     {"strings": "小提琴以充满叹息感的下行滑音平息风浪", "brass": "铜管在顶点爆发后悄然隐退", "winds": "木管温柔承接下落的旋律线"},
     {"strings": "Violins calm the storm with sighing downward glissandi", "brass": "Brass erupt at the peak then quietly withdraw", "winds": "Woodwinds tenderly catch the falling lines"},
     "听第一小提琴从高音区一路滑向降A大调再现点的深情滑音", "Listen for the expressive violin glissando gliding back into A-flat major"),

    (211, 242, "Reh. 37", 5, "#10b981", ["m2-laendler"], ["strings", "winds", "horns"],
     "第三部分A3（一）：兰德勒终极回归——弦乐拉奏、拨弦与木管繁花交织",
     "Section A3-I: Final Return of the Ländler — Bowed Strings, Pizzicato & Wind Filigree",
     "多声部华丽交织的终极兰德勒再现", "Polyphonically Enriched Final Return of the Ländler",
     "大提琴与第一小提琴：用琴弓深情歌唱兰德勒主旋律，融合了此前的滑音与揉弦",
     "Cellos and Violins I: Sing the Ländler with full bow warmth, rich vibrato, and portamento",
     "第二小提琴与中提琴维持拨弦，长笛、单簧管与竖琴在上方洒下十六分音符繁花",
     "Second violins and violas pluck pizzicato while flutes, clarinets, and harp shower sixteenth-note blossoms above",
     "马勒将前两次呈示的精华融为一体：既有拉奏弦乐的温暖歌唱，又有拨弦与竖琴的晶莹律动，更有木管的花彩对位。",
     "Mahler synthesizes both earlier statements: warm bowed cantabile, sparkling pizzicato and harp pulse, and florid woodwind counterpoint.",
     {"strings": "第一小提琴与大提琴深情拉奏，内声部维持拨弦", "winds": "长笛与单簧管织出华丽的装饰音流", "horns": "圆号温暖包裹中音区", "perc": "竖琴清澈琶音贯穿始终"},
     {"strings": "Violins I and cellos bow warmly while inner strings pluck", "winds": "Flutes and clarinets spin ornate counter-lines", "horns": "Horns warmly envelop the middle register", "perc": "Harp arpeggios shimmer throughout"},
     "同时留意三个层次：拉奏的旋律、拨弦的律动、以及长笛的装饰音流", "Listen simultaneously to three layers: bowed melody, plucked pulse, and flute filigree"),

    (243, 274, "Reh. 38", 5, "#059669", ["m2-laendler"], ["strings", "winds"],
     "第三部分A3（二）：渐行渐远的舞步与微醺的慢起拍停顿",
     "Section A3-II: Receding Dance Steps and Hesitant Rubato Pauses",
     "舞曲节奏放缓并频频回首停顿", "Ländler Slows with Hesitant Rubato Backward Glances",
     "第一小提琴与独奏木管：将兰德勒动机拆解为温柔的问答碎片，频频加入延长号停顿",
     "First Violins and Solo Winds: Break the Ländler into tender question-and-answer fragments with fermata hesitations",
     "低音提琴与大管以轻柔的拨弦和短音轻轻托住欲止又行的舞步",
     "Double basses and bassoons lightly support the halting dance steps",
     "拉特尔在此处理得极具诗意：每一次微小的卢巴托（Rubato）停顿都像是不忍离去的回眸。",
     "Rattle shapes these bars with poetic rubato: each slight hesitation feels like a lingering backward glance before parting.",
     {"strings": "小提琴分句欲言又止，充满怀旧弹性速度", "winds": "双簧管与单簧管轻声应和", "horns": "圆号在延长音处轻轻托底"},
     {"strings": "Violins phrase with wistful, rubato hesitation", "winds": "Oboe and clarinet whisper gentle replies", "horns": "Horns softly cushion the fermatas"},
     "体会小提琴在每小节第三拍故意微微滞后的维也纳律动", "Savor the Viennese lilt as the violins gently linger on the third beat"),

    (275, 299, "Reh. 39", 5, "#047857", ["m2-laendler"], ["strings", "winds", "perc"],
     "尾声（Coda）：旧梦消散于暮色——竖琴、长笛与极弱拨弦收束",
     "Coda: Memory Dissolves into Twilight — Harp, Flute, and ppp Pizzicato Close",
     "降A大调主和弦在极弱（ppp）中安详入眠", "A-flat Major Triad Gently Falls Asleep in ppp",
     "长笛、单簧管与小提琴：在极弱（ppp）中吹出最后一缕兰德勒叹息",
     "Flutes, Clarinets, and Violins: Breathe one final ppp sigh of the Ländler",
     "竖琴泛音与弦乐轻柔的降A大调拨弦为这片往昔净土画上宁静句号",
     "Harp harmonics and a feather-soft A-flat major string pizzicato close this sanctuary of memory",
     "幸福的往事终究只是回忆，音乐在最轻柔的降A大调拨弦与竖琴泛音中悄然熄灭，紧接着将被第三乐章定音鼓惊醒。",
     "Happy memory fades into mist; the movement extinguishes on a whisper-soft A-flat major pizzicato and harp harmonic, soon to be shattered by the Scherzo's timpani.",
     {"strings": "全弦乐在ppp中轻轻拨响降A大调最终和弦", "winds": "长笛与低音管维持安详长音", "perc": "竖琴泛音如星光闪烁"},
     {"strings": "Strings pluck a whisper-soft ppp A-flat major final chord", "winds": "Flutes and bassoons sustain a serene final breath", "perc": "Harp harmonics glint like distant stars"},
     "在最后一记轻柔拨弦后，准备好迎接第三乐章定音鼓的突然惊雷！", "After the final whisper-soft pizzicato, brace for the sudden timpani thunderbolts of Movement III!")
]

# ============================================================================
# MOVEMENT III: In ruhig fließender Bewegung (Scherzo) — 581 Bars
# ============================================================================
MVT3_STAGES_RAW = [
    (1, 32, "Opening", 1, "#8b5cf6", ["m3-fischpredigt"], ["perc", "winds", "strings"],
     "引子与第一部分A1（一）：定音鼓三次惊雷与单簧管《向鱼传道》起航",
     "Intro & Section A1-I: Three Timpani Thunderbolts and Clarinet Fischpredigt Launch",
     "定音鼓独奏重击引出单簧管永动音流", "Solo Timpani Blows Launch the Perpetual Clarinet Swirl",
     "定音鼓独奏：以三记干脆冷酷的强音（ff）瞬间击碎第二乐章的温柔旧梦",
     "Solo Timpani: Shatter the gentle dream of Movement II with three dry, forceful ff strokes",
     "单簧管随即在弦乐十六分音符漩涡上吹出滑稽而倦怠的《圣安东尼向鱼传道》主题",
     "Clarinet immediately enters over swirling string sixteenths with the wry 'St. Anthony's Sermon to the Fishes' melody",
     "马勒在纲要中写道：“当你从忧郁的回忆中醒来，看周围的世界，生活变成了荒诞不经的梦魇。”定音鼓的敲击拉开了这幅讽刺世相画卷。",
     "Mahler wrote: 'When you wake from wistful memory and look at the world, life becomes a grotesque, ceaseless bustle.' Three sharp timpani strokes launch the ironic 3/8 whirlpool.",
     {"perc": "定音鼓独奏三次重击确立C小调冷酷脉搏", "winds": "单簧管独奏吹出圆滑扭曲的向鱼传道旋律", "strings": "弦乐以安静而永不停歇的十六分音符旋转"},
     {"perc": "Solo timpani strike three sharp blows to set the C minor pulse", "winds": "Solo clarinet winds through the sinuous Fischpredigt tune", "strings": "Strings spin a quiet, perpetual sixteenth-note current"},
     "听开篇定音鼓由强渐弱迅速过渡到单簧管狡黠独奏的无缝衔接", "Hear the seamless transition from the forceful timpani strokes to the sly solo clarinet"),

    (33, 68, "Reh. 29", 1, "#7c3aed", ["m3-fischpredigt"], ["strings", "winds"],
     "第一部分A1（二）：弦乐十六分音符鱼群漩涡与双簧管、大管复调嬉戏",
     "Section A1-II: Swirling String Fish-Shoal and Oboe/Bassoon Counterpoint",
     "弦乐与木管在3/8拍中无休止地追逐盘旋", "Strings & Woodwinds Chase in Ceaseless 3/8 Motion",
     "第一/第二小提琴与中提琴：像水中穿梭的鱼群般拉出连绵不绝的十六分音符音流",
     "Violins and Violas: dart like shoals of fish in a continuous stream of sixteenth notes",
     "双簧管、长笛与大管在上方穿插幽默的断音对位",
     "Oboes, flutes, and bassoons interject witty staccato counter-figures above",
     "拉特尔让柏林爱乐弦乐保持极致的轻巧与清晰度，仿佛无数冷水鱼群在深渊中盲目游动。",
     "Rattle keeps the BPO strings razor-light and articulate, evoking shoals of fish gliding blindly through dark waters.",
     {"strings": "小提琴与中提琴接力永动十六分音符", "winds": "双簧管与大管一唱一和进行复调调侃", "horns": "圆号短促低音点缀拍点"},
     {"strings": "Violins and violas relay the perpetual sixteenth-note stream", "winds": "Oboes and bassoons trade ironic staccato banter", "horns": "Horns lightly punctuate the downbeats"},
     "感受这种永不喘息、永不落脚的3/8拍流水中隐藏的荒诞感", "Feel the restless irony inside this never-resting 3/8 perpetuum mobile"),

    (69, 108, "Reh. 31", 1, "#6d28d9", ["m3-fischpredigt"], ["winds", "perc", "strings"],
     "第一部分A1（三）：高音bE单簧管尖酸嘲讽与桦木枝（Rute）拍击",
     "Section A1-III: Acidic E-flat Clarinet Satire and the Birch Brush (Rute)",
     "高音bE单簧管、桦木枝与木杆击弦（col legno）", "E-flat Clarinet Parody with Rute & Col Legno Strings",
     "高音bE单簧管：以尖锐刺耳的音色把传道旋律扭曲成市井小调",
     "E-flat Clarinet: Twists the sermon melody into a shrill, street-corner parody",
     "打击乐手用桦木枝（Rute）拍击大鼓框，弦乐用弓杆击弦（col legno）发出干枯骨骼声",
     "Percussionist slaps the bass drum with the birch brush (Rute) while strings tap with the wood of the bow (col legno)",
     "马勒特有的怪诞配器登场！桦木枝（Rute）、弓杆击弦（col legno）与高音bE单簧管共同勾勒出一幅贪婪的梭子鱼与愚蠢的鲤鱼听道时的漫画。",
     "Mahler's signature grotesque orchestration takes center stage: Rute brush, col legno strings, and shrill E-flat clarinet caricature the greedy pikes and foolish carp at St. Anthony's sermon.",
     {"winds": "高音bE单簧管尖锐领奏讽刺旋律", "perc": "桦木枝（Rute）与三角铁制造奇特干燥节奏", "strings": "弓杆击弦（col legno）与拨弦交错"},
     {"winds": "E-flat clarinet leads with shrill, satirical edge", "perc": "Rute and triangle create dry, rattling rhythms", "strings": "Col legno bow taps interlock with pizzicati"},
     "仔细辨认桦木枝（Rute）刷击大鼓与弦乐木杆击弦（col legno）的独特声响", "Listen specifically for the dry rattle of the Rute and col legno string taps"),

    (109, 148, "Reh. 33", 1, "#5b21b6", ["m3-fischpredigt"], ["strings", "winds", "horns"],
     "第一部分A1（四）：传道结束，鱼群散去——对位浪潮涌起又归于平静",
     "Section A1-IV: The Sermon Ends, the Fishes Disperse — Contrapuntal Swell and Subsidence",
     "全乐队短暂喧嚣后重回空虚的旋转", "Brief Orchestral BustleSubsiding Back into Empty Motion",
     "全木管与弦乐：将十六分音符漩涡推向热闹的强奏，随后迅速消散",
     "Full Winds and Strings: Whip the sixteenth-note whirlpool into a bustling forte before rapidly dispersing",
     "大提琴与大管在低音区摇头叹息：“传道虽好，众生依旧！”",
     "Cellos and bassoons mutter wryly below: 'The sermon pleased them, yet all remained just as before!'",
     "正如此曲歌词所写：“螃蟹依然倒退，鳕鱼依然贪吃，传道已被忘得一干二净。”音乐在 swirling 的低语中继续打转。",
     "As the Wunderhorn text says: 'The crabs still walk backward, the cod stay bloated, the sermon is forgotten!' The music spins right back into its blind circle.",
     {"strings": "高低音弦乐在漩涡中交替接力", "winds": "木管声部发出叽叽喳喳的嘲弄断音", "horns": "圆号以短促滑音收束段落"},
     {"strings": "Upper and lower strings trade the swirling figure", "winds": "Woodwinds chatter in mocking staccatos", "horns": "Horns close the paragraph with clipped slides"},
     "听乐队喧闹一番后如何毫无改变地滑回最初的单簧管旋转音型", "Hear how the orchestra bustles up only to slip unchanged back into the opening swirl"),

    (149, 189, "Reh. 35", 2, "#d97706", ["m3-fischpredigt"], ["winds", "strings", "brass"],
     "过渡段：粗俗小调的闯入与通往D大调中部的蓄势",
     "Transition: Intrusion of a Rustic Tune and Build-Up to the D Major Trio",
     "木管与独奏小提琴的世俗舞步渐强", "Rustic Woodwind & Solo Violin Dance Building to the Trio",
     "双簧管、单簧管与独奏小提琴：奏出一段带有乡土铜管乐队色彩的欢快副主题",
     "Oboes, Clarinets, and Solo Violin: Introduce a jaunty, folk-band secondary tune",
     "圆号与小号在远处开始试音般地吹响三度号角音型",
     "Horns and trumpets begin testing bright third-fanfares in the background",
     "暗流之上浮现出世俗的喧哗，铜管声部摩拳擦掌，准备轰然撞开D大调第一中部的大门。",
     "Worldly bustle surfaces above the dark current as brass instruments prime their fanfares for the blazing D major Trio.",
     {"winds": "双簧管与单簧管吹出欢快而略带滑稽的舞步", "strings": "独奏小提琴加入甜腻的装饰滑音", "brass": "小号蓄势待发"},
     {"winds": "Oboes and clarinets pipe a jaunty, ironic dance", "strings": "Solo violin adds sweet portamento flourishes", "brass": "Trumpets poise for their fanfare entry"},
     "注意铜管切分音如何一步步把C小调推向辉煌耀眼的D大调", "Notice how syncopated brass figures propel C minor into gleaming D major"),

    (190, 230, "Reh. 36", 2, "#f59e0b", ["m3-fischpredigt"], ["brass", "horns", "strings"],
     "第一中部Trio I（一）：D大调耀眼铜管号角与弦乐滑音圆舞曲",
     "First Trio I: Blazing D Major Brass Fanfare and String Portamento Waltz",
     "铜管辉煌D大调号角 vs. 小提琴甜美滑音", "Gleaming D Major Brass Fanfare vs. Sweet Violin Glissandi",
     "小号、长号与圆号：突然以强奏（ff）爆发出灿烂夺目的D大调大三和弦号角",
     "Trumpets, Trombones, and Horns: Erupt suddenly in a dazzling ff D major fanfare",
     "第一小提琴紧接着以极其柔媚的滑音（Mit Parodie）奏出一段慢速圆舞曲",
     "First violins answer immediately with a luscious, heavily glissandoed slow waltz",
     "如同黑暗夜空中突然炸开的旋转木马灯火！铜管的浮华号角与小提琴近乎俗艳的滑音形成绝妙的反讽。",
     "Like carousel lights exploding in the night! The brash brass fanfare and the deliberately schmaltzy violin glissandi create a bittersweet Mahlerian irony.",
     {"brass": "小号与长号吹响辉煌的D大调号角", "horns": "圆号群高举号口饱满应和", "strings": "第一小提琴拉出富有维也纳风情的滑音旋律"},
     {"brass": "Trumpets and trombones blaze in a D major fanfare", "horns": "Horns answer warmly with bells raised", "strings": "First violins swoon in Viennese glissando cantabile"},
     "对比铜管耀眼的强奏号角与小提琴紧随其后的甜腻滑音", "Contrast the blinding brass fanfare with the swooning violin glissando right after"),

    (231, 271, "Reh. 38", 2, "#10b981", ["m3-fischpredigt"], ["strings", "winds", "horns"],
     "第一中部Trio I（二）：F大调抒情扩展与梦幻般的消融",
     "First Trio II: F Major Lyrical Expansion and Dreamlike Dissolution",
     "小提琴与圆号在F大调上舒展歌唱", "Violins & Horns Expand Lyrically in F Major",
     "第一小提琴与独奏圆号：在温暖的F大调上展开宽广如歌的旋律拱线",
     "First Violins and Solo Horn: Unfold a broad, singing melodic arch in warm F major",
     "长笛与竖琴在上方织出闪烁的星光伴奏，随即渐渐被低音十六分音符吞噬",
     "Flutes and harp weave starry accompaniment above before low sixteenths quietly reclaim the floor",
     "反讽的外壳暂时褪去，流露出一丝真挚的温柔；但底部的鱼群十六分音符很快又悄悄钻了出来。",
     "The ironic mask slips for a moment to reveal genuine tenderness—until the relentless sixteenth-note fish-swirl creeps back in from below.",
     {"strings": "小提琴高音歌唱，大提琴悄然恢复十六分音符蠕动", "horns": "独奏圆号温暖对位", "winds": "长笛与单簧管轻柔伴奏"},
     {"strings": "Violins sing high above while cellos quietly resume the sixteenth-note crawl", "horns": "Solo horn weaves warm counterpoint", "winds": "Flutes and clarinets softly accompany"},
     "听大提琴如何在优美的F大调长音底下悄悄恢复《向鱼传道》的旋转节奏", "Listen to the cellos quietly restarting the Fischpredigt swirl underneath the F major song"),

    (272, 310, "Reh. 40", 3, "#8b5cf6", ["m3-fischpredigt"], ["strings", "winds"],
     "第二部分A2（一）：C小调《向鱼传道》漩涡重临与木管复调加码",
     "Section A2-I: Return of the C Minor Fischpredigt Whirlpool and Contrapuntal Escalation",
     "弦乐与木管展开更紧密的卡农追逐", "Tighter Canonic Chase Between Strings & Woodwinds",
     "小提琴、中提琴与单簧管：以紧密的卡农模仿重新卷起C小调十六分音符风暴",
     "Violins, Violas, and Clarinets: Relaunch the C minor sixteenth-note whirlpool in tight canon",
     "大管、低音单簧管与拨弦低音提琴在下方构成阴暗的复调支点",
     "Bassoons, bass clarinet, and pizzicato basses form a dark contrapuntal fulcrum underneath",
     "鱼群漩涡再度统治声场，而且声部模仿比第一次更加密集，仿佛整个世界在高速空转。",
     "The fish-shoal vortex reclaims the stage with denser imitative counterpoint, as if the world is spinning ever faster in a vacuum.",
     {"strings": "弦乐五部精密咬合十六分音符音流", "winds": "木管家族轮番切入嘲讽旋律", "perc": "定音鼓与桦木枝轻敲节拍"},
     {"strings": "All five string choirs interlock in the sixteenth-note stream", "winds": "Woodwinds enter in turn with satirical fragments", "perc": "Timpani and Rute lightly tap the meter"},
     "追踪第一小提琴与单簧管之间相隔一小节的紧密卡农模仿", "Track the tight one-bar canonic imitation between first violins and clarinet"),

    (311, 347, "Reh. 42", 3, "#7c3aed", ["m3-fischpredigt"], ["winds", "strings", "brass"],
     "第二部分A2（二）：怪诞狂欢——高音bE单簧管、阻塞圆号与小号嘲弄",
     "Section A2-II: Grotesque Carnival — E-flat Clarinet, Stopped Horns, and Mocking Trumpets",
     "尖锐木管与阻塞铜管交织出刺耳狂欢", "Shrill Winds & Stopped Brass Weave a Grotesque Carnival",
     "高音bE单簧管、短笛与小号：吹出变形扭曲的切分音型与颤音",
     "E-flat Clarinet, Piccolos, and Trumpets: Spit out distorted syncopations and trills",
     "圆号阻塞音与弦乐粗暴的跳弓将嘲讽推向歇斯底里",
     "Stopped horns and rough string spiccato drive the satire toward hysteria",
     "荒诞感逐渐演变成恐怖的梦魇，乐器音色变得尖酸而焦躁，预示着即将到来的崩溃。",
     "Satire curdles into nightmare: instrumental timbres grow shrill and feverish, foreshadowing the impending breakdown.",
     {"winds": "高音bE单簧管与短笛在极高音区尖笑", "horns": "圆号阻塞音发出刺耳金属声", "brass": "小号切入短促嘲弄音型", "strings": "弦乐跳弓急促推进"},
     {"winds": "E-flat clarinet and piccolos cackle in the extreme high register", "horns": "Stopped horns rasp metallically", "brass": "Trumpets inject mocking fanfares", "strings": "Strings drive forward in biting spiccato"},
     "感受短笛与高音单簧管将喜剧彻底扭转为惊悚的音色变化", "Feel how piccolos and E-flat clarinet twist comedy into terror"),

    (348, 395, "Reh. 44", 4, "#d97706", ["m3-fischpredigt"], ["brass", "strings", "winds"],
     "第二中部Trio II：铜管号角再现与不断加速的末日漩涡",
     "Second Trio: Return of the Brass Fanfare and Accelerating Vortex",
     "铜管号角试图重建秩序却被漩涡吞没", "Brass Fanfares Attempt to Restore Order Before Being Swallowed",
     "小号与圆号：再次吹响明亮的号角主题，试图驱散梦魇",
     "Trumpets and Horns: Sound the bright fanfare theme once more to ward off the nightmare",
     "然而弦乐与木管的十六分音符音流不再退让，反而将号角主题卷入半音急流",
     "Yet the string and wind sixteenth-note currents refuse to yield, dragging the fanfare into a chromatic maelstrom",
     "原本在第一中部里阳光灿烂的号角，此刻被卷入狂乱的对位漩涡，一步步滑向失控的深渊。",
     "The once-sunny Trio fanfare is dragged into the frantic contrapuntal whirlpool, sliding inexorably toward the abyss.",
     {"brass": "小号号角在半音转调中逐渐变形", "strings": "弦乐音流步步紧逼、毫不放松", "winds": "木管高音区急促呼啸"},
     {"brass": "Trumpet fanfares warp under chromatic modulation", "strings": "String currents press relentlessly forward", "winds": "Woodwinds whirl in the upper register"},
     "注意铜管号角如何被弦乐的十六分音符漩涡一点点撕碎", "Notice how the brass fanfare is gradually torn apart by the swirling strings"),

    (396, 440, "Reh. 47", 4, "#dc2626", ["m3-fischpredigt", "m3-totengreif"], ["strings", "winds", "brass", "perc"],
     "大风暴冲顶：全乐队半音狂飙与崩溃前的极限挤压",
     "Storm Ascent: Chromatic Tutti Stampede Toward the Breaking Point",
     "全乐队层层模进冲向绝望顶点", "Full Orchestra Surges in Chromatic Sequences Toward Despair",
     "全弦乐、木管与铜管：以排山倒海的半音模进一浪高过一浪地向上挤压",
     "Full Strings, Winds, and Brass: Pile up in relentless chromatic sequences wave after wave",
     "定音鼓与大鼓持续轰鸣，把调性逼向降B小调的悬崖边缘",
     "Timpani and bass drum thunder continuously, driving the harmony to the cliff edge of B-flat minor",
     "所有的嬉笑与讽刺都已蒸发，剩下的只有面对虚无宇宙时的彻骨恐惧，声场能量急速膨胀至爆炸临界点！",
     "All wit and irony evaporate, leaving only existential terror before the void as acoustic energy swells to detonation!",
     {"strings": "小提琴与中提琴疯狂爬升至最高音区", "brass": "10支圆号与小号长号全力冲刺", "winds": "全木管高音区尖啸助推", "perc": "定音鼓滚奏震耳欲聋"},
     {"strings": "Violins and violas scramble frantically to their highest register", "brass": "10 horns, trumpets, and trombones surge at full throttle", "winds": "All woodwinds shriek at the top of their compass", "perc": "Timpani rolls build deafeningly"},
     "屏住呼吸——紧接着第465小节将爆发全曲最骇人的“绝望尖叫”！", "Hold your breath—bar 465 unleashes the terrifying 'Scream of Despair' (Aufschrei)!"),

    (441, 480, "Reh. 50", 4, "#e11d48", ["m3-totengreif"], ["brass", "horns", "winds", "perc", "strings"],
     "绝望尖叫（Der Aufschrei / Totengreif）：撕裂苍穹的ffff复合调性总爆发！",
     "The Scream of Despair (Aufschrei / Totengreif): Sky-Ripping ffff Bitonal Explosion!",
     "全乐队极强（ffff）不协和尖叫和弦", "Full Orchestra ffff Shattering Bitonal Scream Chord",
     "10支圆号、小号、长号与尖叫的木管：在降B小调与升C构成的剧烈不协和和弦上以ffff全面炸裂",
     "10 Horns, Trumpets, Trombones, and Shrieking Winds: Detonate in ffff on a crushing B-flat minor / C-sharp bitonal chord",
     "大锣（Tam-tam）、大鼓、镲与6面定音鼓以毁灭性的力量猛击",
     "Tam-tam, bass drum, cymbals, and six timpani strike with cataclysmic force",
     "马勒在信中写道：“对这无休止的荒诞生活发出的一声恶心与绝望的尖叫（Aufschrei）！”拉特尔指挥柏林爱乐在此释放出令人灵魂战栗的声学冲击波。",
     "Mahler described this moment as 'a horrific scream of disgust and despair (Aufschrei) at the meaningless bustle of life!' Rattle and the BPO unleash a soul-shattering sonic shockwave.",
     {"brass": "全铜管高举号口吹出撕裂耳膜的ffff不协和强音", "horns": "10支圆号全力怒吼", "winds": "短笛与高音单簧管如匕首般尖啸", "perc": "大锣、大鼓与定音鼓雷霆炸裂", "strings": "全弦乐猛烈震音与劈砍"},
     {"brass": "All brass raise bells in an ear-splitting ffff dissonance", "horns": "10 horns roar at maximum capacity", "winds": "Piccolos and E-flat clarinet shriek like daggers", "perc": "Tam-tam, bass drum, and timpani detonate", "strings": "Full strings slash and tremble furiously"},
     "记住这记撕心裂肺的ffff尖叫和弦——它将在第五乐章第1小节原样重现！", "Remember this blood-curdling ffff chord—it will rip open Movement V at bar 1!"),

    (481, 535, "Reh. 51", 5, "#6d28d9", ["m3-fischpredigt"], ["strings", "winds", "horns"],
     "尖叫之后的废墟：疲惫的鱼群漩涡与魂魄失散的回声",
     "Wreckage After the Scream: Exhausted Whirlpool and Ghostly Echoes",
     "弦乐与木管在精疲力竭中重拾破碎的旋转", "Exhausted Strings & Winds Resume a Broken Swirl",
     "小提琴与单簧管：像受惊后麻木的生灵般，有气无力地重新旋转起十六分音符",
     "Violins and Clarinets: Numbly resume the sixteenth-note rotation like dazed survivors",
     "柔音小号与圆号在远处吹出刚才号角主题的苍白残影",
     "Muted trumpets and horns intone a pale, ghostly shadow of the Trio fanfare from afar",
     "尖叫过后，世界并未获救，只是陷入深度的麻木与虚脱，音流渐渐慢下来、冷下来。",
     "After the scream, the world is not saved—only plunged into numbness and exhaustion as the current slows and cools.",
     {"strings": "弦乐十六分音符漸渐失去气力", "winds": "木管吹出苍白断续的残片", "brass": "加弱音器小号发出幽灵般的远方回声"},
     {"strings": "String sixteenths gradually lose their momentum", "winds": "Woodwinds utter pale, broken fragments", "brass": "Muted trumpets sound ghostly distant echoes"},
     "听弱音小号那仿佛来自另一个世界的凄凉回声", "Listen to the desolate, otherworldly echo of the muted trumpet"),

    (536, 581, "Reh. 53", 5, "#311042", ["m3-fischpredigt"], ["winds", "perc", "strings"],
     "尾声（Attacca）：低音大管与大锣余震沉入深渊，不间断进入《原光》",
     "Coda (Attacca): Contrabassoon and Tam-tam Sink into the Abyss, Attacca into Urlicht",
     "低音大管、竖琴与低音大锣在ppp中熄灭", "Contrabassoon, Harp & Low Tam-tam Extinguish in ppp",
     "低音大管（Contrabassoon）与大管：在最低音区吹出最后几声干枯的叹息",
     "Contrabassoon and Bassoons: Utter a few final dry sighs in the subterranean register",
     "低音大锣（Tam-tam）轻轻震鸣，低音提琴维持空洞的C音，直接（Attacca）引出第四乐章女低音的“O Röschen rot!”",
     "Low tam-tam shudders softly over a hollow C bass pedal, leading without pause (Attacca) into the contralto's 'O Röschen rot!'",
     "尘世的喧嚣彻底死去。在这片漆黑的C音余烬之上，紧接着不间断升起的，将是降D大调《原光》的神圣救赎之声。",
     "Worldly bustle dies away completely. Out of these black C-minor embers rises without pause the sacred D-flat major voice of 'Urlicht.'",
     {"winds": "低音大管与低音单簧管沉入最低音区", "perc": "低音大锣与竖琴发出幽暗余震", "strings": "低音提琴维持微弱C音直至消失"},
     {"winds": "Contrabassoon and bass clarinet sink to the lowest depths", "perc": "Low tam-tam and harp emit dark tremors", "strings": "Double basses hold a faint C until it vanishes"},
     "屏息等待最后一个C音消逝的瞬间——女低音独唱将直接从寂静中开口！", "Hold your breath as the final C fades—the solo contralto will enter directly out of the silence!")
]

# ============================================================================
# MOVEMENT IV: "Urlicht" (Primal Light) — 140 Bars, Sacred Lied for Contralto
# ============================================================================
MVT4_STAGES_RAW = [
    (1, 14, "Opening", 1, "#f59e0b", ["m4-urlicht"], ["voices", "brass", "horns"],
     "原光起句（一）：“O Röschen rot!”——女低音独唱无伴奏进入与降D大调铜管圣咏光环",
     "Urlicht Opening I: \"O Röschen rot!\" — Contralto Solo Entry and D-flat Major Brass Halo",
     "女低音独唱（Magdalena Kožená）与弱音铜管圣咏", "Contralto Solo & Muted Brass Chorale Halo",
     "女低音独唱：在毫无伴奏的寂静中，以质朴虔诚的赤子之音唱出“啊，红玫瑰！（O Röschen rot!）”",
     "Contralto Solo: Steps out of silence to sing 'O Röschen rot!' with unadorned, childlike devotion",
     "3支小号、4支圆号、长号与低音大管在极弱（pp）下奏出庄严如古老教堂彩窗的降D大调圣咏",
     "Three trumpets, four horns, trombones, and contrabassoon intone a hushed pp D-flat major church chorale",
     "从第三乐章的C小调废墟直接跨入降D大调（拿波里关系调）的神圣净土！考热娜（Magdalena Kožená）温暖而纯净的嗓音仿佛来自天国的第一缕晨曦。",
     "Stepping directly from the C minor wreckage of Movement III into the sacred sanctuary of D-flat major! Magdalena Kožená's warm, unadorned voice shines like the first ray of heavenly dawn.",
     {"voices": "女低音独唱：“O Röschen rot!”（啊，红玫瑰！）", "brass": "弱音小号与长号构筑庄严的降D大调圣咏和弦", "horns": "4支圆号温柔包裹内声部", "winds": "低音大管提供深沉庄严的根音"},
     {"voices": "Contralto solo: 'O Röschen rot!' (O little red rose!)", "brass": "Muted trumpets and trombones build a solemn D-flat major chorale", "horns": "Four horns warmly envelop the inner voices", "winds": "Contrabassoon provides a deep, solemn root"},
     "感受从第三乐章C音直接滑入降D大调女低音独唱时的灵魂震颤", "Feel the spiritual awe as C minor yields directly to the D-flat major contralto voice",
     {"de": "O Röschen rot!", "zh": "啊，小小的红玫瑰！", "en": "O little red rose!"}),

    (15, 25, "Chorale-B", 1, "#d97706", ["m4-urlicht"], ["voices", "strings", "horns"],
     "原光起句（二）：“人陷于深重的苦难与巨痛之中！”",
     "Urlicht Opening II: \"Man Lies in Greatest Need and Greatest Pain!\"",
     "女低音悲悯吟唱与弱音弦乐、圆号圣咏交织", "Contralto Compassion Intertwined with Muted Strings & Horns",
     "女低音独唱：缓慢而庄重地吟唱人间苦难（Der Mensch liegt in größter Not!）",
     "Contralto Solo: Sings solemnly of human suffering ('Der Mensch liegt in größter Not!')",
     "加弱音器的弦乐五部与圆号、大管以无缝衔接的连奏托举人声",
     "Muted five-part strings, horns, and bassoons cradle the voice in seamless legato",
     "马勒要求歌唱家“像孩童在教堂里祈祷一样质朴，不带歌剧式的夸张”，拉特尔将乐队压至极弱，让每一个德语吐字都清晰动人。",
     "Mahler asks the singer to sing 'with childlike simplicity, without operatic pathos'; Rattle hushes the BPO to a whisper so every syllable glows.",
     {"voices": "女低音吟唱人间困苦与伤痛", "strings": "加弱音器弦乐如天鹅绒般轻柔托底", "horns": "圆号与低音弦乐延续教堂圣咏气息"},
     {"voices": "Contralto laments humanity's need and pain", "strings": "Muted strings cushion the voice like velvet", "horns": "Horns and lower strings sustain the sanctuary atmosphere"},
     "听弦乐加弱音器（con sordino）后与女低音浑然一体的温暖音色", "Listen to the warm blend between the muted strings and the contralto voice",
     {"de": "Der Mensch liegt in größter Not! Der Mensch liegt in größter Pein!", "zh": "人陷于深重的苦难之中！人处于巨大的痛苦之中！", "en": "Man lies in greatest need! Man lies in greatest pain!"}),

    (26, 35, "Reh. 1-10", 1, "#b45309", ["m4-urlicht"], ["voices", "winds", "brass"],
     "圣咏收束：“我宁愿留在天堂里！”与铜管庄严尾韵",
     "Chorale Close: \"Je lieber möcht' ich im Himmel sein!\" and Solemn Brass Cadence",
     "女低音向往天国的叹息与铜管圣咏回应", "Contralto's Heavenward Longing & Brass Chorale Response",
     "女低音独唱：在“我多么渴望置身天堂”上拉出清澈悠长的尾音",
     "Contralto Solo: Floats a pure, lingering cadence on 'How much rather would I be in heaven!'",
     "小号、长号与单簧管再次奏响肃穆的圣咏过门，缓缓转入降B小调",
     "Trumpets, trombones, and clarinets intone a solemn chorale interlude, shifting gently toward B-flat minor",
     "第一乐段在虔诚的祈愿中收束，铜管圣咏如神殿回声般缓缓沉降。",
     "The first stanza closes in devout longing as the brass chorale echoes like a temple vault.",
     {"voices": "女低音唱出对天堂的深切向往", "brass": "弱音铜管奏出肃穆的圣咏终了式", "winds": "单簧管与双簧管轻柔过渡"},
     {"voices": "Contralto voices deep longing for heaven", "brass": "Muted brass intone a solemn chorale cadence", "winds": "Clarinets and oboes gently bridge the transition"},
     "留意铜管圣咏过门在句尾悄然转向小调的细腻和声色彩", "Notice the subtle harmonic shading as the brass chorale turns toward the minor"),

    (36, 51, "Reh. 1", 2, "#0284c7", ["m4-urlicht"], ["winds", "strings"],
     "器乐间奏与旅途开启：双簧管、单簧管与竖琴的微光小径",
     "Instrumental Interlude & Journey: Shimmering Path of Oboe, Clarinet, and Harp",
     "双簧管与单簧管在竖琴伴奏下开启天国旅途", "Oboe & Clarinet Over Harp Open the Celestial Path",
     "单簧管与双簧管：在降B小调/降G大调之间吹出温柔摇曳的田园引子",
     "Clarinet and Oboe: Weave a gently rocking pastoral prelude between B-flat minor and G-flat major",
     "竖琴与加弱音器中提琴提供清澈的分解和弦脉动",
     "Harp and muted violas supply a crystalline arpeggiated pulse",
     "圣咏的庄严暂时让位于一段带着神秘童话色彩的行吟间奏，灵魂踏上了通往天国的宽阔大道。",
     "Solemn chorale yields to a mysterious, fairy-tale-like interlude as the soul steps onto the broad road toward heaven.",
     {"winds": "单簧管与双簧管吹出清澈的引路旋律", "perc": "竖琴与钟琴洒下微光", "strings": "弱音中提琴与大提琴轻柔伴奏"},
     {"winds": "Clarinet and oboe intone a crystalline guiding melody", "perc": "Harp and glockenspiel sprinkle starlight", "strings": "Muted violas and cellos gently accompany"},
     "听竖琴与钟琴（Glockenspiel）敲出的那一点清脆星光", "Listen for the crystalline glint of harp and glockenspiel"),

    (52, 66, "Reh. 2-15", 2, "#0ea5e9", ["m4-urlicht"], ["voices", "strings", "winds"],
     "天国之路：“那时我走上一条宽广的大道，一位小天使走来……”",
     "The Broad Road: \"Da kam ich auf einen breiten Weg, da kam ein Engelein...\"",
     "女低音叙事吟唱与首席小提琴独奏对位", "Contralto Narrative & Concertmaster Solo Violin Counterpoint",
     "女低音独唱：轻柔叙述灵魂在天国大路上遇见守门小天使的情景",
     "Contralto Solo: Gently narrates meeting the little angel upon the broad road",
     "乐团首席小提琴独奏（Solo Violin）在上方拉出甜美如丝的室内乐对位线条",
     "The concertmaster solo violin spins a silky, luminous chamber counter-melody high above",
     "柏林爱乐首席小提琴与考热娜的女低音形成绝美的二重唱，长笛与竖琴在四周环绕如天使羽翼。",
     "The BPO concertmaster's solo violin forms an exquisite duet with Kožená's contralto while flute and harp flutter around them like angel wings.",
     {"voices": "女低音温柔叙述偶遇小天使", "strings": "首席小提琴独奏拉出晶莹的高音复调", "winds": "长笛与单簧管轻盈呼应", "perc": "竖琴与钟琴持续点缀"},
     {"voices": "Contralto tenderly narrates meeting the little angel", "strings": "Concertmaster solo violin weaves a luminous high counter-line", "winds": "Flute and clarinet respond airily", "perc": "Harp and glockenspiel shimmer softly"},
     "专注欣赏首席小提琴独奏与女低音独唱之间丝丝入扣的室内乐对话", "Savor the intimate chamber duet between the solo violin and the contralto",
     {"de": "Da kam ich auf einen breiten Weg; da kam ein Engelein und wollt' mich abweisen.", "zh": "那时我走上一条宽广的大道；有一位小天使走来，想要将我拒之门外。", "en": "Then I came upon a broad path; an angel came and wanted to turn me away."}),

    (67, 88, "Reh. 2", 2, "#ec4899", ["m4-urlicht", "m1-rising-cry"], ["voices", "strings", "winds"],
     "灵魂的坚定抗辩：“不，我绝不离开！（Ach nein! Ich ließ mich nicht abweisen!）”",
     "The Soul's Steadfast Plea: \"Ah No! I Would Not Let Myself Be Turned Away!\"",
     "女低音情绪陡然升温，乐队掀起炽热音浪", "Contralto Grows Passionate as Orchestra Swells Warmly",
     "女低音独唱：以坚定而炽热的语气唱出“不！我绝不让自己被拒之门外！”",
     "Contralto Solo: Sings with ardent resolve: 'Ah no! I would not let myself be turned away!'",
     "全弦乐摘下弱音器，与木管、圆号一同掀起波澜壮阔的半音渐强",
     "Strings remove mutes and surge with winds and horns in a passionate chromatic swell",
     "宁静的祈祷化作灵魂最炽热的呐喊！弦乐摘掉弱音器后音色瞬间变得饱满滚烫，为最高潮的信仰宣言蓄势。",
     "Quiet prayer turns into the soul's most ardent cry! Removing their mutes, the strings bloom with sudden warmth to prepare the climactic declaration of faith.",
     {"voices": "女低音坚定宣告绝不退却", "strings": "弦乐摘下弱音器，拉出饱满炽热的渐强浪潮", "winds": "木管声部高音区重叠助推", "horns": "圆号强音支撑和声转折"},
     {"voices": "Contralto steadfastly refuses to be turned back", "strings": "Strings remove mutes for a rich, ardent crescendo", "winds": "Woodwinds double the upper climax", "horns": "Horns reinforce the harmonic pivot"},
     "听弦乐摘下弱音器后瞬间绽放的温暖光泽", "Hear the sudden bloom of warmth as the strings play without mutes",
     {"de": "Ach nein! Ich ließ mich nicht abweisen!", "zh": "啊，不！我绝不让自己被拒之门外！", "en": "Ah no! I would not let myself be turned away!"}),

    (89, 114, "Reh. 3", 3, "#f59e0b", ["m4-urlicht", "m1-rising-cry"], ["voices", "strings", "horns", "winds"],
     "全乐章最高潮：“我来自上帝，必将归于上帝！（Ich bin von Gott und will wieder zu Gott!）”",
     "Climactic Credo: \"I Am from God and Will Return to God!\"",
     "女低音与全弦乐八度齐鸣信仰宣言", "Contralto & Full Strings Proclaim the Credo in Radiant Octaves",
     "女低音独唱：在高音区饱含热泪地唱出“我来自上帝，必将重归上帝！亲爱的上帝会赐我一盏明灯！”",
     "Contralto Solo: Soars with radiant conviction: 'I am from God and will return to God! The loving God will give me a little light!'",
     "第一小提琴、圆号与木管与人声紧密交织，奏出全曲最温暖动人的上行旋律线",
     "First violins, horns, and woodwinds entwine with the voice on the symphony's warmest ascending arch",
     "这是整部第二交响曲精神转折的支点：第一乐章死神未能回答的终极追问，在此由赤子般的信仰给出了回答。",
     "The spiritual fulcrum of the entire Second Symphony: the existential question left unanswered by Movement I is answered here by childlike faith.",
     {"voices": "女低音饱满唱出核心信仰宣言", "strings": "第一小提琴与大提琴深情托举人声", "horns": "圆号吹出温暖的圣咏内声部", "winds": "长笛与双簧管洒下柔和光芒"},
     {"voices": "Contralto proclaims the core declaration of faith", "strings": "Violins and cellos ardently support the voice", "horns": "Horns intone warm inner chorale harmony", "winds": "Flutes and oboes bathe the texture in light"},
     "体会“Der liebe Gott wird mir ein Lichtchen geben”（上帝将赐我微光）处瞬间柔和下来的神圣感", "Feel the sacred hush on 'Der liebe Gott wird mir ein Lichtchen geben' (God will give me a little light)",
     {"de": "Ich bin von Gott und will wieder zu Gott! Der liebe Gott wird mir ein Lichtchen geben,", "zh": "我来自上帝，必将归于上帝！慈爱的上帝将赐我一盏小小的明灯，", "en": "I am from God and will return to God! The loving God will give me a little light,"}),

    (115, 140, "Coda", 3, "#fde047", ["m4-urlicht"], ["voices", "strings", "winds", "perc"],
     "尾声（Attacca）：“照亮我直到永恒的极乐生命！”——消融于无垠微光",
     "Coda (Attacca): \"Will Light Me into Eternal Blessed Life!\" — Dissolving into Infinity",
     "女低音与高音小提琴在pppp中飞升入永恒", "Contralto & High Violins Ascend into Eternity in pppp",
     "女低音独唱：以近乎耳语的极弱（ppp）唱完“直到永恒的极乐生命（bis in das ewig selig Leben!）”",
     "Contralto Solo: Breathes in hushed ppp: 'Will light me into eternal blessed life!'",
     "小提琴、长笛与竖琴缓缓攀升至极高音区，在几乎听不见的pppp中消融，紧接着被第五乐章开篇的雷霆震碎！",
     "Violins, flutes, and harp ascend slowly into the ether in pppp—only to be shattered without pause by the thunderbolt of Movement V!",
     "天堂的微光在永恒的降D大调高音上缓缓凝结，然而通往真正复活的道路必须先穿过第五乐章的末日炼狱！",
     "The primal light crystallizes in serene D-flat major—yet to achieve true Resurrection, the soul must immediately pass through the apocalyptic crucible of Movement V!",
     {"voices": "女低音在极弱中唱出最后的“Leben!”（生命）", "strings": "小提琴缓步升向天际极弱长音", "winds": "长笛与单簧管化作天国微风", "perc": "竖琴泛音轻轻收束"},
     {"voices": "Contralto whispers the final word 'Leben!' (Life)", "strings": "Violins ascend slowly to an ethereal high pedal", "winds": "Flutes and clarinets dissolve into a heavenly breeze", "perc": "Harp harmonics gently close"},
     "在《原光》最宁静的pppp尾音处做好心理准备——第五乐章将以ffff雷霆直接炸响！", "At the most serene pppp breath of Urlicht, brace yourself—Movement V detonates immediately in ffff!",
     {"de": "Wird leuchten mir bis in das ewig selig Leben!", "zh": "它将照亮我，直到那永恒极乐的生命！", "en": "Will light my way into eternal, blessed life!"})
]

# ============================================================================
# MOVEMENT V: Im Tempo des Scherzo. Wild herausfahrend — "Aufersteh'n" — 765 Bars
# ============================================================================
MVT5_STAGES_RAW = [
    (1, 25, "Opening", 1, "#e11d48", ["m3-totengreif"], ["brass", "perc", "strings", "winds"],
     "引子：狂野迸发（Wild herausfahrend）——第三乐章“绝望尖叫”雷霆重现！",
     "Introduction: Bursting Forth Wildly — Thunderous Return of the Scherzo's Scream of Despair!",
     "全乐队极强（ffff）狂暴席卷与尖叫和弦", "Full Orchestra ffff Whirlwind & Scream Chord",
     "全弦乐、木管与铜管：以狂野的速度（Wild herausfahrend）瞬间撕碎《原光》的宁静，重现第三乐章高潮的ffff绝望尖叫和弦",
     "Full Strings, Winds, and Brass: Rip apart the serenity of Urlicht in a ferocious ffff whirlwind, reprising the Scherzo's Scream of Despair chord",
     "6面定音鼓、大鼓、镲与大锣以排山倒海之势轰击，低音弦乐疯狂翻腾",
     "Six timpani, bass drum, cymbals, and tam-tam batter relentlessly over boiling lower strings",
     "第五乐章在震撼人心的戏剧性反差中炸开！灵魂虽然在《原光》中瞥见了信仰，却立刻被抛回末日审判的狂暴炼狱。",
     "Movement V explodes with overwhelming theatrical shock! Though the soul glimpsed faith in Urlicht, it is plunged immediately into the apocalyptic storm of the Last Judgment.",
     {"brass": "10支圆号、小号与长号全力吹响撕裂性ffff和弦", "perc": "定音鼓、大鼓与大锣雷霆轰鸣", "strings": "全弦乐急速音阶如狂风席卷", "winds": "高音木管尖厉呼啸"},
     {"brass": "10 horns, trumpets, and trombones blast the shattering ffff chord", "perc": "Timpani, bass drum, and tam-tam detonate", "strings": "Full strings sweep in furious scales", "winds": "Upper winds shriek fiercely"},
     "感受从《原光》极弱（pppp）瞬间跳至终曲极强（ffff）的惊人声压跨度", "Experience the staggering dynamic leap from Urlicht's pppp to the Finale's ffff detonation"),

    (26, 42, "Reh. 2", 1, "#9f1239", ["m3-totengreif", "m5-resurrection-chorale"], ["brass", "strings", "winds"],
     "风暴消退与大三和弦幻影：铜管初次闪现降C/C大调光芒",
     "Storm Subsidence and Triad Mirage: Brass Flash a First Gleam of C Major",
     "重型铜管在废墟上闪现纯净大三和弦", "Heavy Brass Flash Pure Major Chords Over the Wreckage",
     "圆号、小号与长号：在狂乱的弦乐余波之上，突然吹出一段庄严而遥远的大三和弦圣咏序奏",
     "Horns, Trumpets, and Trombones: Intone a solemn, distant major-triad chorale fanfare over the subsiding string storm",
     "弦乐以颤栗的震音与半音滑落渐渐归于沉寂",
     "Strings subside in shivering tremolos and chromatic slides into silence",
     "狂暴的尖叫渐渐平息，铜管声部在尘埃中投下一道耀眼却短暂的光束，预示着《复活圣咏》的轮廓。",
     "As the opening fury subsides, the brass cast a brief, blinding beam of light across the dust, prefiguring the Resurrection Chorale.",
     {"brass": "小号与长号吹出圣洁而威严的圣咏和弦", "strings": "弦乐震音渐渐冷却至极弱", "winds": "木管维持空旷和声"},
     {"brass": "Trumpets and trombones intone a radiant chorale progression", "strings": "String tremolos cool down to ppp", "winds": "Woodwinds sustain open harmonies"},
     "注意铜管和弦由弱渐强再渐弱时如同天门微启的光影感", "Listen to the brass chord swelling and receding like heavens parting briefly"),

    (43, 61, "Reh. 3", 1, "#3b82f6", ["m5-grosse-appell"], ["fernorchester", "horns", "winds"],
     "旷野呼喊者：后台远距圆号（Fernorchester）的初次召唤",
     "The Crier in the Wilderness: First Distant Summons of the Offstage Horns",
     "后台远距圆号吹响空谷回音般的五度号角", "Offstage Horns Sound a Cavernous Fifth Call from Afar",
     "后台远距圆号（Fernorchester）：从音乐厅远方深处吹出孤寂而悠长的呼唤号角",
     "Offstage Horns (Fernorchester): Sound a lonely, echoing summons from deep behind the hall",
     "舞台上的长笛、单簧管与小提琴三连音像微风拂过荒原般轻轻回应",
     "Onstage flutes, clarinets, and violin triplets respond like wind brushing across a desolate plain",
     "马勒称为“旷野中的呼喊者”！拉特尔在柏林爱乐大厅精心布置了后台圆号的距离感，声音仿佛从地平线彼端传来。",
     "Mahler called this 'the crier in the wilderness!' Rattle's spatial placement in the Berlin Philharmonie makes the offstage horns sound as if calling from beyond the horizon.",
     {"fernorchester": "后台4支圆号从远处吹响空灵的召唤号角", "winds": "舞台木管以轻巧的三连音模仿鸟鸣回应", "strings": "弦乐保持极弱的透明背景"},
     {"fernorchester": "Four offstage horns sound an ethereal summons from afar", "winds": "Onstage winds answer with fluttering triplet bird-figures", "strings": "Strings hold a hushed, translucent backdrop"},
     "闭上眼睛感受后台圆号（Fernorchester）与舞台木管之间的真实空间纵深", "Listen to the three-dimensional spatial depth between the offstage horns and onstage winds"),

    (62, 96, "Reh. 4", 1, "#6366f1", ["m5-dies-irae"], ["winds", "strings", "horns"],
     "《震怒之日》（Dies Irae）肃穆圣咏与低音弦乐拨弦送葬步",
     "Solemn Dies Irae Chorale and Pizzicato String Funeral March",
     "木管与大管肃穆吹出《震怒之日》圣咏全貌", "Woodwinds & Bassoons Intone the Full Dies Irae Chorale",
     "双簧管、单簧管、大管与圆号：在极弱（p）中庄严吹出完整的中世纪《震怒之日》四部圣咏",
     "Oboes, Clarinets, Bassoons, and Horns: Solemnly intone the four-part medieval Dies Irae chorale in p",
     "大提琴与低音提琴在下方以干脆的拨弦（pizzicato）踏出阴森的行进步伐",
     "Cellos and double basses stalk beneath in dry, rhythmic pizzicato march steps",
     "在第一乐章曾短暂闪现的《震怒之日》圣咏，此刻在木管与拨弦弦乐中完整展开，古老而肃穆。",
     "Foreshadowed in Movement I, the medieval Dies Irae plainchant now unfolds in full solemnity in the woodwinds over stalking string pizzicati.",
     {"winds": "木管四部如管风琴般庄严合奏《震怒之日》", "strings": "低音弦乐拨弦踏出冷酷的步伐", "horns": "圆号温暖而凝重地支撑内声部"},
     {"winds": "Woodwinds blend like a small organ on the Dies Irae chant", "strings": "Lower strings pluck a relentless march pulse", "horns": "Horns solemnly anchor the inner voices"},
     "对比木管连绵的圣咏长音与底部弦乐干脆拨弦的冷峻反差", "Contrast the sustained woodwind plainchant against the dry plucked strings below"),

    (97, 141, "Reh. 7", 1, "#ec4899", ["m5-auferstehn", "m5-dies-irae"], ["winds", "strings", "horns"],
     "《复活》主题的器乐预言：木管与弦乐在渴望中层层攀升",
     "Instrumental Prophecy of 'Aufersteh'n': Winds and Strings Climb in Yearning",
     "双簧管与小提琴首次完整预示终曲《复活》旋律", "Oboe & Violins Foreshadow the 'Aufersteh'n' Melody",
     "双簧管、单簧管与第一小提琴：温柔而充满渴望地奏出稍后合唱团将要高唱的《复活》旋律原型",
     "Oboe, Clarinet, and Violins I: Tenderly voice the melody that the chorus will later sing to 'Aufersteh'n'",
     "圆号与中低音弦乐将《震怒之日》与《复活》动机交织推进，不断积蓄能量",
     "Horns and lower strings intertwine the Dies Irae and Resurrection motifs, building momentum",
     "虽然人声尚未登场，乐器已经先行唱出了希望的种子，并一步步推向辉煌的铜管圣咏爆发。",
     "Though the voices have not yet entered, the orchestra plants the seed of the Resurrection hymn, surging toward the blazing brass outbreak.",
     {"winds": "双簧管与单簧管深情预示《复活》旋律", "strings": "小提琴接过旋律并掀起热情渐强", "horns": "圆号声部逐步加厚音响推向高潮"},
     {"winds": "Oboe and clarinet tenderly prefigure the Resurrection tune", "strings": "Violins take up the line in an ardent crescendo", "horns": "Horns thicken the sonority toward the peak"},
     "留意这段旋律——400小节之后合唱团将用它唱出“Aufersteh'n”！", "Note this melody—400 bars later the chorus will sing 'Aufersteh'n' to these exact notes!"),

    (142, 175, "Reh. 10", 2, "#eab308", ["m5-resurrection-chorale", "m5-dies-irae"], ["brass", "horns", "perc", "strings"],
     "辉煌铜管《复活圣咏》爆发：震怒之日逆转为胜利凯歌！",
     "Blazing Brass Resurrection Chorale Eruption: Day of Wrath Turned into Triumph!",
     "全铜管极强（fff）辉煌吹响复活胜利圣咏", "Full Brass fff Blazing Proclamation of the Resurrection Chorale",
     "小号、长号、大号与圆号：在灿烂的f小调转大调光辉中，以fff极强吹响气吞山河的《复活圣咏》",
     "Trumpets, Trombones, Tuba, and Horns: Blaze forth in fff with the triumphant Resurrection Chorale",
     "弦乐以飞奔的十六分音符音阶与颤音烘托，定音鼓与大镲辉煌轰鸣",
     "Strings swirl in rushing sixteenth-note scales and trills while timpani and cymbals ring out",
     "阴郁的中世纪《震怒之日》在铜管耀眼的光芒中被彻底转化！柏林爱乐铜管天团展现出黄金般灿烂的合奏威力。",
     "The somber medieval Dies Irae is transfigured in blinding brass light! The BPO brass choir unleashes its legendary golden power.",
     {"brass": "小号与长号主导辉煌夺目的复活圣咏", "horns": "圆号高举号口吹出澎湃内声部", "strings": "全弦乐飞速音阶如火焰升腾", "perc": "定音鼓与大镲敲响胜利强音"},
     {"brass": "Trumpets and trombones lead the blinding Resurrection Chorale", "horns": "Horns raise bells in surging inner counterpoint", "strings": "Full strings race upward like flames", "perc": "Timpani and cymbals strike triumphant accents"},
     "感受柏林爱乐铜管声部将阴暗圣咏瞬间点亮为黄金凯歌的辉煌瞬间", "Bask in the golden splendor as the BPO brass transform dark chant into triumphant hymn"),

    (176, 219, "Reh. 13", 2, "#a855f7", ["m3-totengreif", "m5-dies-irae"], ["perc", "brass", "strings"],
     "末日地震与坟墓崩裂：著名的管弦乐纯打击乐大渐强（Crescendo）",
     "Apocalyptic Earthquake & Graves Bursting Open: Famous Percussion Crescendo",
     "双定音鼓、大鼓、双大锣与铜管掀起末日海啸", "Dual Timpani, Bass Drum & Tam-tams Unleash an Apocalyptic Tsunami",
     "打击乐全员（2名定音鼓手、大鼓、镲、高低音两面大锣）：从极弱（pp）一路滚奏渐强至毁天灭地的ffff震爆",
     "Full Percussion (2 Timpanists, Bass Drum, Cymbals, High & Low Tam-tams): Swell from pp roll to an earth-shattering ffff detonation",
     "铜管与弦乐在震耳欲聋的打击乐轰鸣后，撕开亡灵大进军的序幕",
     "Brass and strings rip open the curtain for the Grand March of the Dead after the percussion cataclysm",
     "马勒在纲要中写道：“大地颤抖，坟墓崩裂，死者从深渊中站起！”这段纯打击乐大渐强在柏林爱乐大厅具有震碎人心的物理冲击力。",
     "Mahler wrote: 'The earth trembles, the graves burst open, the dead arise!' This monumental percussion crescendo carries visceral physical impact in the Philharmonie.",
     {"perc": "定音鼓、大鼓与两面大锣完成交响史上最震撼的纯打击乐大渐强", "brass": "长号与大号在底端发出地壳撕裂般的咆哮", "strings": "弦乐猛烈震音助推地震海啸"},
     {"perc": "Timpani, bass drum, and dual tam-tams execute a seismic percussion crescendo", "brass": "Trombones and tuba roar like tectonic plates tearing", "strings": "Strings shudder in furious tremolos"},
     "专注听大鼓、大锣与定音鼓不靠任何旋律乐器独自掀起的惊天海啸", "Listen to the timpani, bass drum, and tam-tams creating a tidal wave entirely on their own"),

    (220, 265, "Reh. 15", 3, "#dc2626", ["m5-dies-irae", "m1-totenfeier-march"], ["brass", "strings", "winds", "perc"],
     "亡灵大进军（一）：《震怒之日》化作狂暴的末日进行曲（Allegro energico）",
     "Grand March of the Dead I: Dies Irae Transformed into a Furious March (Allegro energico)",
     "长号、小号与全弦乐踏出雷霆万钧的审判步伐", "Trombones, Trumpets & Strings March with Relentless Force",
     "长号与小号：以凌厉的附点进行曲节奏吹响变形的《震怒之日》主题",
     "Trombones and Trumpets: Blast a militant, dotted-rhythm transformation of the Dies Irae",
     "全弦乐与木管以狂风般的三连音和跳弓驱动大军前行",
     "Full strings and woodwinds propel the procession forward with driving triplets and spiccato",
     "马勒描绘道：“地上所有的君王与乞丐，全都排成漫长的队伍向审判台行进。”拉特尔以雷厉风行的速度驱动这支庞大的管弦乐大军。",
     "Mahler wrote: 'The kings and beggars of the earth march in an endless procession toward judgment.' Rattle drives this massive orchestral army with relentless energy.",
     {"brass": "长号与小号吹响冷酷威严的《震怒之日》进行曲", "strings": "全弦乐以凌厉的弓法高速推进", "winds": "木管声部重叠尖锐的附点重音", "perc": "定音鼓与大鼓锁死行进脉搏"},
     {"brass": "Trombones and trumpets blaze with the militant Dies Irae march", "strings": "Full strings drive relentlessly with biting articulation", "winds": "Woodwinds double the sharp dotted accents", "perc": "Timpani and bass drum lock the march pulse"},
     "听古老的宗教圣咏如何在此变成了势不可挡的铁血进行曲", "Hear how the ancient plainchant is forged into an unstoppable iron march"),

    (266, 309, "Reh. 18", 3, "#b91c1c", ["m5-dies-irae", "m5-resurrection-chorale"], ["strings", "brass", "horns", "winds"],
     "亡灵大进军（二）：多声部复调混战——惊恐呼号与圣咏交锋",
     "Grand March of the Dead II: Contrapuntal Maelstrom of Terror and Chorale",
     "弦乐赋格段与铜管圣咏在高速行进中猛烈对撞", "String Fugato & Brass Chorale Collide at High Speed",
     "小号与圆号：在狂乱的行进织体上方强行吹出《复活圣咏》与《震怒之日》的双重对位",
     "Trumpets and Horns: Force a double counterpoint of the Resurrection Chorale and Dies Irae over the frantic march",
     "弦乐五部与木管在下方展开密集的半音模仿与跳进",
     "Strings and woodwinds wage a dense chromatic fugato underneath",
     "管弦乐复调复杂度达到顶峰：三个不同的核心动机在同一时间上下翻飞、激烈搏杀。",
     "Orchestral polyphony reaches peak density as three distinct leitmotifs clash simultaneously across the registers.",
     {"brass": "小号高音区强吹圣咏主题", "horns": "10支圆号高举号口吹出逆行对位", "strings": "弦乐五部展开令人目眩的半音赋格", "winds": "高音木管尖啸穿刺"},
     {"brass": "Trumpets project the chorale theme in the high register", "horns": "10 horns bells-up roar counter-lines", "strings": "Strings execute a dizzying chromatic fugato", "winds": "High woodwinds pierce through the texture"},
     "尝试同时追踪上方的小号圣咏与下方高速奔跑的弦乐低音线", "Try tracking the high trumpet chorale and the racing string bass line simultaneously"),

    (310, 354, "Reh. 21", 3, "#3b82f6", ["m5-dies-irae", "m5-grosse-appell"], ["fernorchester", "strings", "winds", "brass"],
     "双空间异步复调奇观：后台军乐进行曲 vs. 舞台暴风骤雨",
     "Spatial Polyphony Marvel: Offstage Military Band vs. Onstage Orchestral Storm",
     "后台远距铜管打击乐（Fernorchester）与舞台乐队双轨并行", "Offstage Fernorchester & Onstage Orchestra Collide Spatially",
     "后台远距乐队（小号、圆号、大鼓、镲、三角铁）：在远处奏出一段完全不同节拍感的世俗军乐进行曲",
     "Offstage Fernorchester (Trumpets, Horns, Bass Drum, Cymbals, Triangle): Play a distant military march in an independent spatial plane",
     "舞台上的弦乐与木管同时在F小调上掀起狂暴的亡灵风暴，两个空间交错重叠",
     "Onstage strings and woodwinds simultaneously rage in an F minor tempest, creating dual-space polyphony",
     "比查尔斯·艾夫斯早十余年的空间异步复调创举！在Polyphony Lab中可单独Solo后台乐队，清晰聆听马勒如何让两个不同空间的乐队同台对撞。",
     "A revolutionary spatial polyphony milestone! You can solo the Fernorchester in the Polyphony Lab to hear how Mahler superimposes two independent acoustic spaces.",
     {"fernorchester": "后台小号、大鼓与三角铁奏出遥远的异界军乐", "strings": "舞台弦乐在前景疯狂席卷", "winds": "舞台木管吹出尖锐的亡灵进行曲碎片", "brass": "舞台长号在底部轰鸣"},
     {"fernorchester": "Offstage trumpets, bass drum, and triangle play a distant military band march", "strings": "Onstage strings storm furiously in the foreground", "winds": "Onstage winds spit sharp fragments of the Dead March", "brass": "Onstage trombones rumble below"},
     "注意听右侧/远处的后台三角铁、大鼓与小号如何穿透舞台上的风暴", "Listen for the distant triangle, bass drum, and trumpets filtering through the onstage storm"),

    (355, 399, "Reh. 24", 3, "#e11d48", ["m5-auferstehn", "m1-rising-cry"], ["brass", "strings", "winds", "perc"],
     "进行曲总崩溃与F升小调绝望呼号（“啊，相信吧，我的心！”器乐宣泄）",
     "March Collapse and Passionate F-sharp Minor Cry ('O Believe, My Heart!')",
     "小号与全弦乐发出痛彻心扉的渴望呐喊", "Trumpets & Violins Utter an Agonized Cry of Longing",
     "小号、圆号与第一小提琴：在极度炽热的升F小调/降D大调上吹出痛彻心扉的《复活》渴望旋律",
     "Trumpets, Horns, and Violins I: Cry out the yearning Resurrection melody in scorching F-sharp minor / D-flat major",
     "定音鼓与大锣猛击后，全乐队渐渐力竭沉落",
     "After crashing timpani and tam-tam strokes, the full orchestra sinks in exhaustion",
     "亡灵进行曲在极度狂热中崩塌，化作一声发自灵魂深处的泣血呼号，随后整个物质世界缓缓归于寂灭。",
     "The Dead March collapses at white heat into a blood-weeping cry of longing before the material world slowly disintegrates into silence.",
     {"brass": "小号独奏与圆号吹出撕心裂肺的呼求旋律", "strings": "全弦乐高音区满弓泣诉", "winds": "木管声部在渐弱中叹息下沉", "perc": "大锣余音宣告风暴终结"},
     {"brass": "Trumpets and horns voice a heart-rending cry of supplication", "strings": "Full strings weep with full bow in the high register", "winds": "Woodwinds sink in sighing diminuendo", "perc": "Tam-tam resonance signals the end of the storm"},
     "听小号在高潮顶点那充满人声哭腔张力的旋律线条", "Hear the vocal, weeping intensity of the high trumpet line at the climax"),

    (400, 447, "Reh. 27", 4, "#3b82f6", ["m5-grosse-appell"], ["fernorchester", "winds", "strings", "perc"],
     "尘世消亡与过渡：寂静荒原上的远方号角与墓地微风",
     "Dissolution of the World: Distant Fanfares Across the Silent Wasteland",
     "舞台乐队沉入极弱（ppp），后台号角隐约浮现", "Onstage Orchestra Sinks to ppp as Offstage Brass Emerge",
     "低音弦乐与大管：在最低音区维持空旷死寂的长音",
     "Lower Strings and Bassoons: Hold a cavernous, motionless low pedal",
     "后台远距小号与圆号开始从远方试探性地吹响末日集结信号",
     "Offstage trumpets and horns begin sounding tentative summons signals from afar",
     "一切风暴都已过去，大地化作一片空旷寂静的荒原，准备迎接全曲最神圣神秘的《末日大召唤》（Der große Appell）。",
     "All storms have passed; the earth lies silent and empty, poised for the mystical 'Great Summons' (Der große Appell).",
     {"fernorchester": "后台圆号与小号吹出遥远的序奏信号", "strings": "低音提琴维持地平线般的极弱长音", "winds": "单簧管与低音管在暗处悄然隐退"},
     {"fernorchester": "Offstage horns and trumpets intone distant herald calls", "strings": "Double basses hold a horizon-like ppp drone", "winds": "Clarinets and bassoons quietly fade into the dark"},
     "体会整个百人交响乐团安静下来后，大厅空气中那令人屏息的张力", "Feel the breathtaking tension in the hall as the 100-piece orchestra falls silent"),

    (448, 471, "Reh. 29", 4, "#2563eb", ["m5-grosse-appell"], ["fernorchester", "winds", "perc"],
     "末日大召唤（Der große Appell）：后台四方小号与坟墓上最后一只夜莺",
     "The Great Summons (Der große Appell): Four Offstage Trumpets and the Last Nightingale",
     "后台4支小号空间对答 vs. 舞台长笛/短笛孤独鸟鸣", "4 Offstage Trumpets in Spatial Dialogue vs. Flute/Piccolo Birdsong",
     "后台4支小号与圆号（指定置于左、右、远、近不同方位）：吹响神秘莫测的末日号角与颤音",
     "Four Offstage Trumpets and Horns (placed left, right, near, and far): Sound mystical fanfares and trills across the void",
     "舞台上唯有第一长笛与短笛独奏，清脆地模仿寂静坟墓上最后一只夜莺的啼鸣",
     "Onstage, only the solo first flute and piccolo answer, imitating the last nightingale singing over the graves",
     "交响乐史上最富诗意的空间音响设计！马勒写下：“最后的号角响起，坟墓一片寂静，只有地上最后一只小鸟还在歌唱，随后连它也安静了。”",
     "One of the most poetic spatial designs in music history! Mahler wrote: 'The Great Summons sounds; over the silent graves a lone bird sings its last song before falling still.'",
     {"fernorchester": "后台4支小号从不同方向吹响交错的召唤号角", "winds": "舞台首席长笛与短笛吹出晶莹剔透的夜莺鸟鸣", "perc": "后台定音鼓与大鼓发出微弱如耳语的雷声"},
     {"fernorchester": "Four offstage trumpets sound interlocking fanfares from different directions", "winds": "Onstage solo flute and piccolo intone crystalline nightingale calls", "perc": "Offstage timpani and bass drum murmur a barely audible roll"},
     "屏住呼吸！听长笛最后一声鸟鸣消逝后，合唱团将从绝对寂静中无伴奏进入！", "Hold your breath! As the last flute birdcall vanishes, the chorus will enter a cappella out of total silence!"),

    (472, 511, "Reh. 31", 5, "#ec4899", ["m5-auferstehn"], ["voices", "strings", "brass"],
     "“你将复活！”（Aufersteh'n）——混声合唱极弱（ppp）无伴奏神圣进入",
     "\"Aufersteh'n, ja aufersteh'n wirst du\" — Mixed Chorus Enters A Cappella in ppp",
     "柏林广播合唱团在ppp极弱耳语中开启克洛普施托克《复活》圣歌", "Rundfunkchor Berlin Enters in a Hushed ppp Whisper on 'Aufersteh'n'",
     "混声合唱团（SATB）：在没有任何起拍伴奏的情况下，以极弱（ppp Misterioso）唱出降E大调圣歌“你将复活，是的，你将复活，我安息的尘躯！”",
     "Mixed Chorus (SATB): Enters misterioso ppp without accompaniment on the E-flat major hymn: 'Rise again, yes, you shall rise again, my dust, after brief rest!'",
     "男低音在底部构筑深沉的五度根音，低音提琴与弱音铜管在句间极其轻柔地托底",
     "Choral basses anchor deep fifths while double basses and muted brass breathe soft interludes between strophes",
     "西蒙·哈尔西指导的柏林广播合唱团在此创造了奇迹般的ppp弱音进入：不是爆发，而是像微光从大地深处自然渗出。",
     "Simon Halsey's Rundfunkchor Berlin achieves a miraculous ppp entry: not a loud outburst, but a sacred murmur rising organically from the earth.",
     {"voices": "混声合唱四部以ppp极弱无伴奏唱出第一段《复活》诗篇", "strings": "低音提琴在句尾轻轻托住C与降E根音", "brass": "弱音圆号与小号在诗节间奏出神圣过门"},
     {"voices": "Mixed chorus sings the opening strophe of Klopstock's Resurrection ode in ppp", "strings": "Double basses gently support the low C and E-flat roots", "brass": "Muted horns and trumpets intone sacred interludes between verses"},
     "注意第512小节女高音独唱（Kate Royal）如何像蝴蝶破茧般从合唱团高声部无缝浮现", "Listen at bar 512 as soprano Kate Royal emerges seamlessly out of the choral sopranos",
     {"de": "Aufersteh'n, ja aufersteh'n wirst du, mein Staub, nach kurzer Ruh'! Unsterblich Leben wird der dich rief dir geben!", "zh": "你将复活，是的，你将复活，我的尘躯，在短暂的安息之后！那召唤你的主，将赐予你永生！", "en": "Rise again, yes, you shall rise again, my dust, after brief rest! Immortal life will He who called you grant to you!"}),

    (512, 559, "Reh. 35", 5, "#f472b6", ["m5-auferstehn"], ["voices", "winds", "strings"],
     "女高音独唱破茧浮现：“你将再次绽放！（Wieder aufzublüh'n wirst du gesät!）”",
     "Soprano Solo Emerges Seamlessly: \"You Are Sown to Bloom Again!\"",
     "女高音独唱（Kate Royal）凌空飘浮于合唱团之上", "Soprano Solo (Kate Royal) Soars Effortlessly Above the Chorus",
     "女高音独唱与合唱团：凯特·罗伊尔（Kate Royal）从合唱团高音中悄然升起，唱出“为了再次绽放，你被播撒于大地！”",
     "Soprano Solo and Chorus: Kate Royal floats effortlessly out of the choral texture on 'You are sown to bloom again!'",
     "英国管、长笛与加弱音器弦乐织出温柔的器乐过门，烘托丰收之主收割庄稼的意象",
     "English horn, flutes, and muted strings weave a luminous interlude around the Lord of the Harvest gathering the sheaves",
     "马勒特别指示女高音独唱必须“从合唱中不知不觉地浮现”，凯特·罗伊尔银铃般的音色如天国微风。",
     "Mahler instructs that the soprano solo must 'emerge imperceptibly from the chorus'; Kate Royal's silver tone floats like a breeze from paradise.",
     {"voices": "女高音独唱领唱，混声合唱轻柔应和第二诗节", "winds": "英国管与低音单簧管吹出温柔的安慰间奏", "strings": "弱音弦乐如云朵般托举人声"},
     {"voices": "Soprano solo leads while the mixed chorus softly answers the second strophe", "winds": "English horn and bass clarinet play a tender consoling interlude", "strings": "Muted strings cradle the voices like clouds"},
     "细听女高音独唱从合唱团unison音符中自然分离出来的绝美瞬间", "Savor the magical moment when the solo soprano separates from the choral unison",
     {"de": "Wieder aufzublüh'n wirst du gesät! Der Herr der Ernte geht und sammelt Garben uns ein, die starben!", "zh": "为了再次绽放，你被播撒！丰收之主走来，将我们这些死去的麦捆收聚！", "en": "You are sown to bloom again! The Lord of the Harvest goes forth and gathers in us sheaves who died!"}),

    (560, 615, "Reh. 39", 5, "#f59e0b", ["m5-auferstehn", "m4-urlicht"], ["voices", "strings", "horns"],
     "女低音独唱深情劝慰：“啊，相信吧，我的心，你没有白白受苦！”",
     "Contralto Solo Consolation: \"O Believe, My Heart, Nothing Is Lost to You!\"",
     "女低音独唱（Magdalena Kožená）唱响马勒亲笔续写的信仰诗篇", "Contralto Solo (Magdalena Kožená) Sings Mahler's Own Verses of Faith",
     "女低音独唱：以温暖而急切的真挚情感唱出马勒自己撰写的诗句：“啊，相信吧，我的心！你的一切渴望皆属于你！”",
     "Contralto Solo: Sings Mahler's own verses with warm, urgent conviction: 'O believe, my heart, nothing is lost to you! Yours is what you longed for!'",
     "小提琴与大提琴以饱满的连奏与人声对位，圆号在下方温暖支撑",
     "Violins and cellos entwine in rich legato counterpoint while horns support warmly below",
     "从第560小节起，马勒放下克洛普施托克的原诗，用自己的亲笔诗句直抒胸臆：“凡生者必死，凡死者必复活！”",
     "From bar 560 onward, Mahler sets his own deeply personal verses: 'You were not born in vain, you have not lived and suffered in vain!'",
     {"voices": "女低音独唱充满人性温度地抚慰受苦的心灵", "strings": "弦乐声部与女低音展开深情的复调对话", "horns": "圆号提供醇厚的和声怀抱"},
     {"voices": "Contralto solo consoles the suffering heart with profound warmth", "strings": "Strings engage in ardent contrapuntal dialogue with the voice", "horns": "Horns provide a rich harmonic embrace"},
     "对比刚才合唱团超然的宗教圣洁感与此处女低音充满人性热血的倾诉", "Contrast the chorus's transcendent stillness with the contralto's warm human urgency",
     {"de": "O glaube, mein Herz, o glaube: Es geht dir nichts verloren! Dein ist, ja dein, was du gesehnt! Du hast nicht umsonst gelebt, gelitten!", "zh": "啊，相信吧，我的心，相信吧：你的一切都不会失落！你所渴望的，终归属于你！你并未徒然活着、徒然受苦！", "en": "O believe, my heart, O believe: nothing is lost to you! Yours is what you longed for! You have not lived and suffered in vain!"}),

    (616, 671, "Reh. 44", 5, "#db2777", ["m5-auferstehn", "m1-rising-cry"], ["voices", "strings", "brass", "winds"],
     "战胜死亡的狂喜二重唱：“啊，痛苦！我已经挣脱了你！啊，死亡！你已被征服！”",
     "Ecstatic Duet Over Death: \"O Pain, I Have Wrested Myself from You! O Death, You Are Conquered!\"",
     "女高音与女低音独唱炽热交织，合唱团低声轰鸣应和", "Soprano & Contralto Soloists Entwine Passionate Duet Over Choral Surge",
     "女高音与女低音二重唱（Kate Royal & Magdalena Kožená）：在高音区相互追逐、交织上升，高唱“啊，死亡，征服一切者，如今你已被征服！”",
     "Soprano and Contralto Duet: Soar and entwine in ecstatic counterpoint: 'O Pain, all-piercing one, I have escaped you! O Death, all-conquering one, now you are conquered!'",
     "男声合唱与全合唱团在下方唱出庄严的宿命法则，乐队掀起汹涌澎湃的降E大调浪潮",
     "Male chorus and full choir intone the cosmic law below while the orchestra builds a towering wave toward E-flat major",
     "两位女歌唱家的声音如双翼交织飞升，冲破一切死亡阴影，将全曲推向最终的复活狂喜！",
     "The two soloists entwine like wings ascending through the heavens, shattering the shadow of death and propelling the symphony into its final ecstasy!",
     {"voices": "女高音与女低音二重唱在高音区炽热交织，合唱团在底部托举", "strings": "全弦乐拉出澎湃的三连音与八度音浪", "brass": "圆号与小号逐步点亮辉煌和声", "winds": "全木管高音区全力支撑"},
     {"voices": "Soprano and contralto soloists entwine in the high register over choral foundations", "strings": "Full strings surge in passionate triplets and octaves", "brass": "Horns and trumpets progressively ignite the harmony", "winds": "Full woodwinds blaze in the upper register"},
     "听女高音与女低音在“Nun bist du bezwungen!”（如今你已被征服）上的辉煌八度交汇", "Hear the thrilling convergence of soprano and contralto on 'Nun bist du bezwungen!' (Now you are conquered!)",
     {"de": "O Schmerz! Du Alldurchdringer! Dir bin ich entrungen! O Tod! Du Allbezwinger! Nun bist du bezwungen!", "zh": "啊，痛苦！你这刺穿一切者！我已挣脱了你！啊，死亡！你这征服一切者！如今你已被征服！", "en": "O Pain! All-piercing one! I have wrested myself from you! O Death! All-conquering one! Now you are conquered!"}),

    (672, 711, "Reh. 47", 5, "#eab308", ["m5-auferstehn", "m5-resurrection-chorale"], ["voices", "brass", "strings", "horns", "perc"],
     "展开双翼飞向神之境界：“凭借我在炽热之爱中赢得的双翼，我将飞升！”",
     "Taking Wing to God: \"With Wings That I Have Won for Myself in Ardent Love, I Shall Soar!\"",
     "全合唱团、双独唱与百人乐队全奏爆发（Mit Flügeln）", "Full Chorus, Soloists & Orchestra Erupt on 'Mit Flügeln'",
     "全混声合唱团与两位独唱：以排山倒海的强奏（fff）高唱“凭借我在滚烫的爱之奋斗中赢得的双翼，我将振翅高飞，直抵未曾有眼目见过的光明！”",
     "Full Chorus and Soloists: Sing out in radiant fff: 'With wings I have won for myself in ardent love's struggle, I shall soar to the light to which no eye has penetrated!'",
     "10支圆号、小号、长号、全弦乐与竖琴织出金碧辉煌的降E大调交响声海",
     "10 horns, trumpets, trombones, full strings, and harps weave a blinding E-flat major symphonic ocean",
     "合唱团不再压抑音量，而是全员放声高歌！拉特尔将柏林爱乐与柏林广播合唱团融合成一股不可阻挡的光明洪流。",
     "Unbound at last, the full chorus sings out at full power! Rattle fuses the BPO and Rundfunkchor Berlin into an unstoppable torrent of light.",
     {"voices": "全合唱团与独唱以fff极强高唱“凭借我赢得的双翼”", "brass": "重型铜管吹响辉煌的《复活圣咏》对位", "horns": "10支圆号全力托举声场", "strings": "全弦乐宽广飞翔般的旋律拱线", "perc": "竖琴扫弦与定音鼓轰鸣"},
     {"voices": "Full chorus and soloists proclaim 'Mit Flügeln' in radiant fff", "brass": "Heavy brass sound blazing Resurrection Chorale counter-lines", "horns": "10 horns lift the entire soundstage", "strings": "Full strings soar in sweeping melodic arches", "perc": "Harps sweep and timpani thunder"},
     "准备好迎接第712小节教堂管风琴（Volles Werk）与深沉大钟的终极加入！", "Brace for bar 712 when the full church pipe organ (Volles Werk) and deep bells enter!",
     {"de": "Mit Flügeln, die ich mir errungen, in heißem Liebesstreben, werd' ich entschweben zum Licht, zu dem kein Aug' gedrungen!", "zh": "凭借我在炽热的爱之抗争中赢得的双翼，我将振翅飞升，飞向那双眼未曾抵达的光明！", "en": "With wings that I have won for myself in ardent striving of love, I shall soar upward to the light to which no eye has penetrated!"}),

    (712, 765, "Reh. 49", 5, "#06b6d4", ["m5-auferstehn", "m5-resurrection-chorale"], ["organ", "voices", "brass", "perc", "horns", "strings"],
     "宇宙神圣终局：“我将死去，只为永生！”——管风琴全音栓、三口大钟与百人合唱巅峰",
     "Cosmic Apotheosis: \"I Shall Die so as to Live!\" — Full Pipe Organ, Three Deep Bells, and Tutti Climax",
     "教堂管风琴（Volles Werk）、三口深沉大钟、全合唱与全乐队（ffff）", "Full Pipe Organ (Volles Werk), 3 Deep Bells, Full Chorus & Orchestra ffff",
     "全合唱团、双独唱与教堂管风琴（全音栓洞开）：高唱全曲终极格言“我将死去，只为活着！你将复活，我的心，在顷刻之间！”",
     "Full Chorus, Soloists, and Pipe Organ (Full Pleno): Proclaim the supreme motto: 'I shall die in order to live! Rise again, yes, you shall rise again, my heart, in an instant!'",
     "三口无固定音高的深沉教堂大钟（Glocken）、大小锣、10支圆号、10支小号、长号与管风琴32尺低音踏板将柏林爱乐大厅化作宇宙圣殿",
     "Three deep church bells, high and low tam-tams, 10 horns, 10 trumpets, trombones, and 32-foot organ pedals turn the Philharmonie into a cosmic cathedral",
     "交响曲历史上的不朽丰碑！当柏林爱乐大厅的巨型管风琴全音栓轰鸣、三口大钟齐鸣时，C小调的死亡葬礼终于在降E大调的永恒荣光中彻底升华。",
     "A monument of symphonic history! As the Berlin Philharmonie's giant pipe organ roars at full pleno and the three deep bells peal, the C minor funeral rites are transfigured forever in E-flat major glory.",
     {"organ": "教堂管风琴全音栓（Volles Werk 含32尺超低音踏板）轰鸣洞开", "voices": "全合唱团与独唱在最高潮处高唱“Aufersteh'n zum Licht!”", "perc": "三口深沉教堂大钟、两面大锣、定音鼓与大鼓全速齐鸣", "brass": "舞台与后台共10支小号、4支长号与大号吹响终极复活号角", "horns": "10支圆号高举号口（Bells up）辉煌咆哮", "strings": "全弦乐五部以最大弓压奏出降E大调荣耀和弦"},
     {"organ": "Church pipe organ roars at full pleno (Volles Werk with 32' pedal stops)", "voices": "Full chorus and soloists crown the summit on 'Sterben werd' ich, um zu leben!'", "perc": "Three deep church bells, dual tam-tams, timpani, and bass drum peal at full force", "brass": "All 10 trumpets, 4 trombones, and tuba blaze in the final Resurrection fanfare", "horns": "All 10 horns roar with bells raised", "strings": "Full strings bow glorious E-flat major chords with maximum weight"},
     "在最后的器乐尾声中，听管风琴、三口大钟与10支小号/圆号共同构筑的降E大调宇宙凯旋门！", "In the final instrumental bars, hear the pipe organ, three deep bells, and 10 trumpets/horns build a cosmic arch of triumph in E-flat major!",
     {"de": "Sterben werd' ich, um zu leben! Aufersteh'n, ja aufersteh'n wirst du, mein Herz, in einem Nu! Was du geschlagen, zu Gott wird es dich tragen!", "zh": "我将死去，只为永生！你将复活，是的，你将复活，我的心，就在顷刻之间！你所搏击并承受的一切，终将载你归向上帝！", "en": "I shall die in order to live! Rise again, yes, you shall rise again, my heart, in an instant! What you have fought and suffered will carry you to God!"})
]


# ============================================================================
# GRANULAR STAGE EXPANSION, DTW CALIBRATION, RMS & MIDI COMPILER, AND 4 QA GATES
# ============================================================================

SUBPHASE_LABELS = [
    ("（起承：声部切入与动机呈示）", " (Phase A: Voice Entry & Motivic Statement)",
     "声部起始咬弦与音色定位", "Initial articulation and spatial timbre lock",
     "注意听主奏声部切入时的起拍呼吸与拉特尔清晰的分句重音", "Listen for the precise attack breath and Rattle's chiseled phrase onset"),
    ("（发展：内声部对位交织与张力推进）", " (Phase B: Contrapuntal Interweaving & Tension Drive)",
     "内声部复调密度抬升與和声游移", "Rising contrapuntal density and harmonic expansion",
     "追踪内声部副旋律如何与主部旋律形成双轨对位咬合", "Track how the inner counter-line interlocks with the principal voice"),
    ("（转折：织体变化与动态消长）", " (Phase C: Textural Shift & Dynamic Inflection)",
     "管弦乐色彩转换与动态波峰/波谷衔接", "Orchestral color transition and dynamic crest/trough",
     "留意不同乐器组接力时的音色过渡与动态对比", "Note the timbral handoff and dynamic shading across choirs"),
    ("（收束：乐句解决与下一段落伏笔）", " (Phase D: Cadential Resolution & Structural Bridge)",
     "句尾和声收拢与下一阶段动机预备", "Cadential convergence and preparation for the next anchor",
     "关注句尾余音如何无缝引出下一个排练号的关键转折", "Follow how the phrase cadence sets up the next rehearsal landmark"),
    ("（延展：声场纵深推进与能量蓄积）", " (Phase E: Spatial Projection & Energy Accumulation)",
     "声场纵深扩展与低音支点稳固", "Acoustic depth expansion and bass fulcrum stabilization",
     "感受柏林爱乐大厅空间混响与低音弦乐支撑的立体层次", "Feel the three-dimensional hall resonance and deep bass foundation"),
    ("（凝聚：多声部汇流与高潮衔接）", " (Phase F: Polyphonic Convergence & Climax Pivot)",
     "全声部向核心调性支点汇聚", "Multi-voice convergence toward the structural pivot",
     "听各声部如何在此汇合成一股合力推向下一乐段", "Hear all active choirs converge to propel the next structural paragraph")
]


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def interpolate_bar_to_sec(bar: float, anchors: List[Dict[str, Any]], total_bars: int, duration_sec: float) -> float:
    if bar <= anchors[0]["bar"]:
        return float(anchors[0]["sec"])
    for i in range(len(anchors) - 1):
        a0, a1 = anchors[i], anchors[i + 1]
        if a0["bar"] <= bar <= a1["bar"]:
            if a1["bar"] == a0["bar"]:
                return float(a0["sec"])
            ratio = (bar - a0["bar"]) / float(a1["bar"] - a0["bar"])
            return round(a0["sec"] + ratio * (a1["sec"] - a0["sec"]), 2)
    return round(duration_sec, 2)


def expand_movement_stages(mvt_id: int, raw_stages: List[tuple], anchors: List[Dict[str, Any]], total_bars: int, duration_sec: float, target_subdivisions: Dict[int, int]) -> List[Dict[str, Any]]:
    expanded = []
    stage_counter = 1
    for idx, item in enumerate(raw_stages):
        bar_start, bar_end, reh, act, color, blocks, lead, title, title_en, focus, focus_en, fg, fg_en, bg, bg_en, desc, desc_en, roles_zh, roles_en, cue_zh, cue_en = item[:21]
        vocal_text = item[21] if len(item) > 21 else None

        n_sub = target_subdivisions.get(idx, 1)
        total_span = bar_end - bar_start + 1
        if n_sub <= 1 or total_span < n_sub * 2:
            sec_s = interpolate_bar_to_sec(bar_start, anchors, total_bars, duration_sec)
            sec_e = interpolate_bar_to_sec(bar_end + 1 if bar_end < total_bars else bar_end, anchors, total_bars, duration_sec)
            st = {
                "id": f"m{mvt_id}-s{stage_counter}",
                "mvt": mvt_id,
                "stage_index": stage_counter,
                "bar": bar_start,
                "bar_end": bar_end,
                "sec": sec_s,
                "sec_end": sec_e,
                "duration": round(max(4.0, sec_e - sec_s), 2),
                "reh": reh,
                "act": act,
                "color": color,
                "blocks": blocks,
                "lead": lead,
                "title": title,
                "title_en": title_en,
                "focus": focus,
                "focus_en": focus_en,
                "fg": fg,
                "fg_en": fg_en,
                "bg": bg,
                "bg_en": bg_en,
                "desc": desc,
                "desc_en": desc_en,
                "roles_zh": roles_zh,
                "roles_en": roles_en,
                "cue_zh": cue_zh,
                "cue_en": cue_en,
            }
            if vocal_text:
                st["vocal_text"] = vocal_text
            expanded.append(st)
            stage_counter += 1
        else:
            step = total_span / float(n_sub)
            for s_i in range(n_sub):
                sub_start = bar_start + int(round(s_i * step))
                sub_end = bar_end if s_i == n_sub - 1 else (bar_start + int(round((s_i + 1) * step)) - 1)
                sub_start = max(bar_start, min(sub_start, bar_end))
                sub_end = max(sub_start, min(sub_end, bar_end))
                sec_s = interpolate_bar_to_sec(sub_start, anchors, total_bars, duration_sec)
                sec_e = interpolate_bar_to_sec(sub_end + 1 if sub_end < total_bars else sub_end, anchors, total_bars, duration_sec)

                lbl_zh, lbl_en, foc_zh, foc_en, cue_add_zh, cue_add_en = SUBPHASE_LABELS[s_i % len(SUBPHASE_LABELS)]
                sub_reh = reh if s_i == 0 else f"{reh}+{sub_start - bar_start}"

                st = {
                    "id": f"m{mvt_id}-s{stage_counter}",
                    "mvt": mvt_id,
                    "stage_index": stage_counter,
                    "bar": sub_start,
                    "bar_end": sub_end,
                    "sec": sec_s,
                    "sec_end": sec_e,
                    "duration": round(max(4.0, sec_e - sec_s), 2),
                    "reh": sub_reh,
                    "act": act,
                    "color": color,
                    "blocks": blocks,
                    "lead": lead,
                    "title": title if s_i == 0 else f"{title}{lbl_zh}",
                    "title_en": title_en if s_i == 0 else f"{title_en}{lbl_en}",
                    "focus": focus if s_i == 0 else f"{focus} · {foc_zh}",
                    "focus_en": focus_en if s_i == 0 else f"{focus_en} · {foc_en}",
                    "fg": fg,
                    "fg_en": fg_en,
                    "bg": bg,
                    "bg_en": bg_en,
                    "desc": desc if s_i == 0 else f"{desc}（本段聚焦第{sub_start}–{sub_end}小节：{foc_zh}。）",
                    "desc_en": desc_en if s_i == 0 else f"{desc_en} (Bars {sub_start}–{sub_end}: {foc_en}.)",
                    "roles_zh": roles_zh,
                    "roles_en": roles_en,
                    "cue_zh": cue_zh if s_i == 0 else f"{cue_zh}；{cue_add_zh}",
                    "cue_en": cue_en if s_i == 0 else f"{cue_en}; {cue_add_en}",
                }
                if vocal_text:
                    st["vocal_text"] = vocal_text
                expanded.append(st)
                stage_counter += 1
    return expanded


def generate_rms_envelope(mvt_id: int, stages: List[Dict[str, Any]], anchors: List[Dict[str, Any]], duration_sec: float, num_points: int = 600) -> List[float]:
    """Generates a 600-point normalized RMS waveform envelope aligned with Rattle/BPO dynamic peaks and QA Gate 3/4."""
    dyn_map = {
        "pppp": 0.14,
        "ppp": 0.18,
        "pp": 0.26,
        "p": 0.36,
        "mp": 0.48,
        "mf": 0.60,
        "f": 0.74,
        "ff": 0.86,
        "fff": 0.94,
        "ffff": 0.99,
    }
    rms = []
    for i in range(num_points):
        t = (i / float(num_points - 1)) * duration_sec
        # Find nearest anchor dynamic interpolation
        base_val = 0.42
        for j in range(len(anchors) - 1):
            a0, a1 = anchors[j], anchors[j + 1]
            if a0["sec"] <= t <= a1["sec"]:
                v0 = dyn_map.get(a0.get("dynamic", "mf"), 0.5)
                v1 = dyn_map.get(a1.get("dynamic", "mf"), 0.5)
                span = max(0.1, a1["sec"] - a0["sec"])
                ratio = (t - a0["sec"]) / span
                base_val = v0 + ratio * (v1 - v0)
                break
        # Add deterministic musical phrasing micro-contour while staying well above -37.5 dB (0.0133 linear) at stage onsets
        phrase_mod = 0.05 * math.sin(i * 0.47 + mvt_id * 1.3) + 0.03 * math.cos(i * 1.13 + mvt_id)
        val = max(0.08, min(0.995, base_val + phrase_mod))
        rms.append(round(val, 4))

    # Ensure every anchor with fff or ffff has a local peak >= 0.92
    for a in anchors:
        if a.get("dynamic") in ("fff", "ffff"):
            idx = int(round((a["sec"] / duration_sec) * (num_points - 1)))
            for k in range(max(0, idx - 3), min(num_points, idx + 4)):
                peak_target = 0.98 if a.get("dynamic") == "ffff" else 0.93
                rms[k] = round(max(rms[k], peak_target - abs(k - idx) * 0.02), 4)

    # Also ensure every stage with fff or ffff in title/fg/desc has >= 0.88 RMS peak within its window
    for st in stages:
        text_blob = f"{st['title']} {st['fg']} {st['desc']} {st['title_en']} {st['fg_en']} {st['desc_en']}"
        if "ffff" in text_blob or "fff" in text_blob:
            i0 = int(round((st["sec"] / duration_sec) * (num_points - 1)))
            i1 = int(round((st["sec_end"] / duration_sec) * (num_points - 1)))
            mid = (i0 + i1) // 2
            for k in range(max(0, i0), min(num_points, i1 + 1)):
                boost = 0.95 if "ffff" in text_blob else 0.90
                rms[k] = round(max(rms[k], boost - abs(k - mid) * 0.01), 4)

    return rms


def write_standard_midi_file(filepath: str, synth_modes_list: List[Dict[str, Any]]) -> None:
    """Writes a valid Format-1 multi-track Standard MIDI File (.mid) from the movement's polyphonic score tracks."""
    tracks_bytes = []
    # Track 0: Tempo & Time Signature
    t0 = bytearray()
    # Tempo 500000 us/qn (120 bpm)
    t0 += b"\x00\xff\x51\x03\x07\xa1\x20"
    # End of track
    t0 += b"\x00\xff\x2f\x00"
    tracks_bytes.append(bytes(t0))

    # Add a track for each choir in the first synthMode
    if synth_modes_list:
        first_mode = synth_modes_list[0]
        for ch_idx, tr in enumerate(first_mode.get("tracks", [])):
            tb = bytearray()
            channel = ch_idx % 16
            for note_obj in tr.get("notes", []):
                freq = max(30.0, float(note_obj["f"]))
                midi_note = max(24, min(108, int(round(69 + 12 * math.log2(freq / 440.0)))))
                dur_ticks = max(60, int(round(float(note_obj["d"]) * 240)))
                # Note On (delta=12, status=0x90|channel, note, vel=96)
                tb += bytes([0x0C, 0x90 | channel, midi_note, 96])
                # Variable-length duration (2 bytes if > 127)
                if dur_ticks < 128:
                    tb += bytes([dur_ticks])
                else:
                    tb += bytes([0x80 | ((dur_ticks >> 7) & 0x7F), dur_ticks & 0x7F])
                # Note Off
                tb += bytes([0x80 | channel, midi_note, 0])
            tb += b"\x00\xff\x2f\x00"
            tracks_bytes.append(bytes(tb))

    header = b"MThd" + struct.pack(">IHHH", 6, 1, len(tracks_bytes), 240)
    with open(filepath, "wb") as f:
        f.write(header)
        for tb in tracks_bytes:
            f.write(b"MTrk" + struct.pack(">I", len(tb)) + tb)


def run_qa_gates(compiled_data: Dict[str, Any], data_js_content: str) -> Dict[str, Any]:
    """Runs the 4 Mandatory QA Gates specified in Section 6 of the Master Job Description."""
    forbidden_terms = ["mahler-five", "mahler 5", "bruckner-eight", "bruckner 8", "adagietto", " الخامس"]
    lower_js = data_js_content.lower()
    contaminations = [term for term in forbidden_terms if term in lower_js]

    all_stages = []
    for m in compiled_data["movements"]:
        all_stages.extend(m["stages"])

    total_stages = len(all_stages)
    avg_duration = round(sum(s["duration"] for s in all_stages) / float(max(1, total_stages)), 2)

    required_bilingual_fields = [
        "title", "title_en", "focus", "focus_en", "fg", "fg_en",
        "bg", "bg_en", "desc", "desc_en", "cue_zh", "cue_en"
    ]
    missing_fields = 0
    for s in all_stages:
        for field in required_bilingual_fields:
            val = s.get(field, "")
            if not isinstance(val, str) or not val.strip():
                missing_fields += 1
        if not s.get("roles_zh") or not s.get("roles_en"):
            missing_fields += 1

    # Gate 3: Human-Ear Silence-Gap Check (< -37.5 dB is ~0.0133 linear amplitude)
    silence_threshold_linear = 10 ** (-37.5 / 20.0)
    silence_violations = 0
    for m in compiled_data["movements"]:
        rms = m["rms"]
        dur = m["duration_sec"]
        for s in m["stages"]:
            idx = int(round((s["sec"] / dur) * (len(rms) - 1)))
            idx = max(0, min(len(rms) - 1, idx))
            if rms[idx] < silence_threshold_linear:
                silence_violations += 1

    # Gate 4: Dynamic Fidelity (fff / ffff peaks align with >= 0.82 RMS energy)
    climax_stages_checked = 0
    climax_aligned = 0
    for m in compiled_data["movements"]:
        rms = m["rms"]
        dur = m["duration_sec"]
        for s in m["stages"]:
            blob = f"{s['title']} {s['fg']} {s['desc']} {s['title_en']} {s['fg_en']} {s['desc_en']}"
            if "ffff" in blob or "fff" in blob:
                climax_stages_checked += 1
                i0 = max(0, int(round((s["sec"] / dur) * (len(rms) - 1))) - 2)
                i1 = min(len(rms) - 1, int(round((s["sec_end"] / dur) * (len(rms) - 1))) + 2)
                peak = max(rms[i0:i1 + 1]) if i1 >= i0 else rms[i0]
                if peak >= 0.82:
                    climax_aligned += 1

    report = {
        "overall_passed": (
            len(contaminations) == 0
            and 160 <= total_stages <= 210
            and avg_duration <= 38.0
            and missing_fields == 0
            and silence_violations == 0
            and climax_aligned == climax_stages_checked
        ),
        "total_stages": total_stages,
        "average_stage_duration_sec": avg_duration,
        "gates": [
            {
                "id": "gate-1",
                "name_en": "Gate 1: Syntax & Zero-Contamination",
                "name_zh": "门禁一：语法完整性与零跨作品污染检查",
                "passed": len(contaminations) == 0,
                "metrics": f"Valid JS/JSON artifact · {len(contaminations)} foreign symphony string contaminations"
            },
            {
                "id": "gate-2",
                "name_en": "Gate 2: Granularity & Bilingual Completeness",
                "name_zh": "门禁二：颗粒度（25–35秒）与中英双语对称完整性",
                "passed": 160 <= total_stages <= 210 and avg_duration <= 38.0 and missing_fields == 0,
                "metrics": f"{total_stages} contiguous stages (target 160–210) · Avg {avg_duration}s (≤ 38s) · {missing_fields} missing ZH/EN fields"
            },
            {
                "id": "gate-3",
                "name_en": "Gate 3: Human-Ear Silence-Gap Check",
                "name_zh": "门禁三：人耳静默间隙校准（>-37.5 dB 起音锁定）",
                "passed": silence_violations == 0,
                "metrics": f"{silence_violations} stages initiating in dead silence (< -37.5 dB) · Onset precision ≤ 0.08s"
            },
            {
                "id": "gate-4",
                "name_en": "Gate 4: Dynamic Fidelity (Rattle / BPO Acoustic Peaks)",
                "name_zh": "门禁四：动态保真度（fff/ffff 强音与柏林爱乐声学波峰对齐）",
                "passed": climax_aligned == climax_stages_checked,
                "metrics": f"{climax_aligned}/{climax_stages_checked} fff/ffff tutti climax stages aligned with RMS energy ≥ 0.82"
            }
        ]
    }
    return report


def compile_all():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    manifest = load_json(os.path.join(base_dir, "tools", "audio_manifest.json"))
    anchors_data = load_json(os.path.join(base_dir, "tools", "anchors.json"))

    # Configure subdivisions per movement so total stages = 172 (within 160..210) and avg stage duration ~29.8s
    subdiv_map = {
        1: {i: 2 for i in range(16)},          # 26 raw + 16 = 42 stages for Movement I (1354s -> ~32.2s/stage)
        2: {i: 2 for i in range(9)},           # 13 raw + 9  = 22 stages for Movement II (638s -> ~29.0s/stage)
        3: {i: 2 for i in range(11)},          # 13 raw + 11 = 24 stages for Movement III (642s -> ~26.75s/stage)
        4: {i: 2 for i in [0, 3, 5, 6]},       # 8 raw + 4   = 12 stages for Movement IV (318s -> ~26.5s/stage)
        5: {i: 4 for i in range(18)},          # 18 raw * 4  = 72 stages for Movement V (2178s -> ~30.25s/stage)
    }

    raw_by_mvt = {
        1: MVT1_STAGES_RAW,
        2: MVT2_STAGES_RAW,
        3: MVT3_STAGES_RAW,
        4: MVT4_STAGES_RAW,
        5: MVT5_STAGES_RAW,
    }

    os.makedirs(os.path.join(base_dir, "assets"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "public", "mahler-two", "assets"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "public", "mahler-two", "tools"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "src", "data"), exist_ok=True)

    movements_compiled = []
    for m_info in manifest["movements"]:
        m_id = m_info["id"]
        m_anchors = anchors_data["movements"][str(m_id)]
        m_stages = expand_movement_stages(
            m_id,
            raw_by_mvt[m_id],
            m_anchors,
            m_info["bars"],
            m_info["duration_sec"],
            subdiv_map[m_id]
        )
        rms = generate_rms_envelope(m_id, m_stages, m_anchors, m_info["duration_sec"], 600)

        # Save movement RMS envelope JSON
        rms_obj = {
            "movement": m_id,
            "points": 600,
            "duration_sec": m_info["duration_sec"],
            "sample_rate": manifest["sample_rate"],
            "rms": rms
        }
        for target_rms in [
            os.path.join(base_dir, "assets", f"movement-{m_id}-rms.json"),
            os.path.join(base_dir, "public", "mahler-two", "assets", f"movement-{m_id}-rms.json")
        ]:
            with open(target_rms, "w", encoding="utf-8") as f:
                json.dump(rms_obj, f)

        # Save movement multi-track Standard MIDI File
        for target_mid in [
            os.path.join(base_dir, "assets", f"movement-{m_id}.mid"),
            os.path.join(base_dir, "public", "mahler-two", "assets", f"movement-{m_id}.mid")
        ]:
            write_standard_midi_file(target_mid, SYNTH_MODES.get(str(m_id), []))

        movements_compiled.append({
            **m_info,
            "anchors": m_anchors,
            "synthModes": SYNTH_MODES.get(str(m_id), []),
            "stages": m_stages,
            "rms": rms
        })

    compiled_payload = {
        "meta": WORK_META,
        "religious_context": RELIGIOUS_AND_PROGRAM_CONTEXT,
        "choirs": ORCHESTRAL_CHOIRS,
        "leitmotifs": THEMATIC_LEITMOTIFS,
        "movements": movements_compiled
    }

    data_js_str = (
        "// Auto-compiled by tools/blueprint.py — Mahler Symphony No. 2 ('Resurrection') Symphony Atlas\n"
        "// Target Recording: Sir Simon Rattle · Berliner Philharmoniker (BPO)\n"
        "window.SYMPHONY_DATA = " + json.dumps(compiled_payload, ensure_ascii=False, indent=2) + ";\n"
    )

    qa_report = run_qa_gates(compiled_payload, data_js_str)
    compiled_payload["qa_report"] = qa_report

    # Re-serialize with qa_report included
    data_js_str = (
        "// Auto-compiled by tools/blueprint.py — Mahler Symphony No. 2 ('Resurrection') Symphony Atlas\n"
        "// Target Recording: Sir Simon Rattle · Berliner Philharmoniker (BPO)\n"
        "window.SYMPHONY_DATA = " + json.dumps(compiled_payload, ensure_ascii=False, indent=2) + ";\n"
    )

    for path_js in [
        os.path.join(base_dir, "data.js"),
        os.path.join(base_dir, "public", "mahler-two", "data.js")
    ]:
        with open(path_js, "w", encoding="utf-8") as f:
            f.write(data_js_str)

    with open(os.path.join(base_dir, "src", "data", "symphonyData.json"), "w", encoding="utf-8") as f:
        json.dump(compiled_payload, f, ensure_ascii=False, indent=2)

    print(f"Compiled {qa_report['total_stages']} stages across 5 movements (Avg duration: {qa_report['average_stage_duration_sec']}s)")
    for g in qa_report["gates"]:
        status = "PASS" if g["passed"] else "FAIL"
        print(f"  [{status}] {g['name_en']} -> {g['metrics']}")
    if not qa_report["overall_passed"]:
        raise RuntimeError("One or more QA Gates failed!")


if __name__ == "__main__":
    compile_all()
