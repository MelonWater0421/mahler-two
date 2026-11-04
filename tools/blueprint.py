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
    "subtitle_zh": "全景声部与复调导览 · 柏林爱乐乐团与西蒙·拉特尔录音自动估计定位版",
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
        "total_duration_sec": 5081.27,
        "total_bars": 2229,
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

# Polyphony Anatomy Lab: concert-pitch reductions from Junji Miki's public
# score digitization. Embedded events make compilation offline/reproducible.
# This is NOT a certified transcription of the Kaplan/IGMG critical edition.
# Raw events: (onset ticks, duration ticks, concert MIDI note, velocity, GM program).
# t/d are seconds; start/dur are quarter-note beats used by app.js and the SMF.
SYNTH_SOURCE = {
    "author": "Junji Miki",
    "catalog_url": "https://gustavmahler.com/midi.html",
    "score_url": "https://ks15.imslp.org/files/imglnks/usimg/e/e2/IMSLP415748-PMLP49406-GMahler_Symphony_No.2_fe_UE_reprint_RSL1.pdf",
    "score_edition": "1897 first edition, Universal Edition reprint (IMSLP415748)",
    "validation_en": "Source MIDI reductions; opening pitches spot-checked against the first edition. Exhaustive Kaplan/IGMG critical-edition verification remains outstanding.",
    "validation_zh": "基于有署名的数字谱缩编；开篇音高已与初版总谱抽查。尚未完成 Kaplan/IGMG 校勘版的逐音核对。",
}


def _score_track(choir, name_zh, name_en, events, ppq, bpm, source_tracks, percussion=False):
    colors = {"strings": "#d97706", "winds": "#0d9488", "horns": "#eab308", "brass": "#dc2626", "choir": "#db2777", "perc": "#7c3aed", "organ": "#2563eb"}
    waves = {"strings": "triangle", "winds": "sine", "horns": "triangle", "brass": "sawtooth", "choir": "triangle", "perc": "sine", "organ": "sine"}
    notes = []
    pitch_names = ("C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B")
    for onset, length, pitch, velocity, program in events:
        start, duration = onset / ppq, length / ppq
        notes.append({"start": start, "dur": duration, "midi": pitch,
                      "t": start * 60 / bpm, "d": duration * 60 / bpm,
                      "f": 440.0 * 2.0 ** ((pitch - 69) / 12.0),
                      "label": pitch_names[pitch % 12] + str(pitch // 12 - 1),
                      "velocity": velocity, "program": program})
    return {"choir": choir, "name_zh": name_zh, "name_en": name_en, "name": name_zh,
            "sub_zh": "有来源的数字谱缩编", "sub_en": "Sourced score reduction", "sub": "Sourced score reduction",
            "color": colors[choir], "wave": waves[choir], "gain": 0.12,
            "program": notes[0]["program"] if notes else 48, "percussion": percussion,
            "source_tracks": source_tracks, "notes": notes}


def _score_scene(movement, index, title_zh, title_en, desc_zh, desc_en, bpm,
                 source_q, end_q, source_grid_bar, source_grid_bar_end, ppq, meter, tracks, source_hash, source_url):
    return {"id": f"m{movement}-synth-{index}", "title_zh": title_zh, "title_en": title_en,
            "name_zh": title_zh, "name_en": title_en, "name": title_zh,
            "desc_zh": desc_zh, "desc_en": desc_en, "desc": desc_zh,
            "bars": f"Source MIDI grid {source_grid_bar}–{source_grid_bar_end}",
            "tempo_bpm": bpm, "bpm": bpm, "totalBeats": end_q - source_q,
            "duration_sec": (end_q - source_q) * 60 / bpm, "meter": meter,
            "source_q": source_q, "source_q_end": end_q,
            "source_grid_bar": source_grid_bar, "source_grid_bar_end": source_grid_bar_end,
            "source_ppq": ppq, "source_sha256": source_hash, "source_url": source_url,
            "provenance": "Junji Miki digitization · concert pitch A4=440 · fixed teaching tempo · critical-edition audit pending",
            "provenance_zh": "Junji Miki 数字谱 · 实音 A4=440 · 固定教学速度 · 校勘版逐音审核待完成",
            "provenance_en": "Junji Miki digitization · concert pitch A4=440 · fixed teaching tempo · critical-edition audit pending",
            "midi": f"assets/movement-{movement}.mid", "tracks": tracks}


SYNTH_MODES = {
    "1": [
        _score_scene(1, 1, '葬礼主题：低音行进与木管哀歌', 'Funeral theme: bass tread and wind lament',
            '小提琴与双簧管的高音线条在大提琴持续行进上交织；英国管与圆号保留各自独立的进入。',
            'Violin and oboe lines interweave over the cello tread; English horn and horn retain their independent entries.',
            84, 100, 132, 25, 32, 96, [4, 4], [
                _score_track('strings', '第一小提琴', 'Violins I',
                    [[0, 154, 79, 47, 48], [192, 115, 86, 47, 48], [336, 31, 84, 47, 48], [384, 154, 79, 47, 48], [576, 115, 86, 47, 48], [720, 31, 84, 47, 48], [768, 77, 79, 47, 48], [1248, 154, 79, 47, 48], [1440, 38, 77, 47, 48], [1488, 38, 75, 47, 48], [1536, 154, 74, 47, 48], [1728, 115, 77, 47, 48], [1872, 38, 75, 47, 48], [1920, 230, 74, 47, 48], [2208, 77, 80, 95, 48], [2304, 77, 79, 95, 48], [2400, 58, 74, 95, 48], [2472, 19, 75, 95, 48], [2496, 77, 77, 95, 48], [2592, 77, 80, 95, 48], [2688, 38, 79, 95, 48], [2784, 154, 87, 95, 48], [2976, 77, 86, 95, 48]],
                    96, 84, [21], False),
                _score_track('strings', '大提琴', 'Cellos',
                    [[0, 31, 55, 95, 48], [72, 16, 50, 47, 48], [96, 31, 43, 47, 48], [224, 21, 53, 47, 48], [256, 21, 55, 47, 48], [288, 21, 56, 47, 48], [320, 21, 53, 47, 48], [352, 21, 62, 47, 48], [384, 31, 55, 95, 48], [456, 16, 50, 47, 48], [480, 31, 43, 47, 48], [608, 21, 53, 47, 48], [640, 21, 55, 47, 48], [672, 21, 56, 47, 48], [704, 21, 53, 47, 48], [736, 21, 62, 47, 48], [768, 26, 55, 47, 48], [800, 26, 51, 47, 48], [832, 26, 60, 47, 48], [864, 26, 53, 47, 48], [896, 26, 50, 47, 48], [928, 26, 58, 47, 48], [960, 26, 51, 47, 48], [992, 26, 48, 47, 48], [1024, 26, 56, 47, 48], [1056, 26, 50, 47, 48], [1088, 26, 43, 47, 48], [1120, 26, 55, 47, 48], [1152, 26, 56, 47, 48], [1184, 26, 53, 47, 48], [1216, 26, 62, 47, 48], [1248, 26, 55, 47, 48], [1280, 26, 51, 47, 48], [1312, 26, 60, 47, 48], [1344, 26, 53, 47, 48], [1376, 26, 50, 47, 48], [1408, 26, 58, 47, 48], [1440, 26, 51, 47, 48], [1472, 26, 48, 47, 48], [1504, 26, 56, 47, 48], [1536, 38, 55, 47, 48], [1608, 19, 50, 47, 48], [1632, 38, 43, 47, 48], [1776, 19, 50, 47, 48], [1800, 19, 51, 47, 48], [1824, 19, 53, 47, 48], [1848, 19, 51, 47, 48], [1872, 19, 53, 47, 48], [1896, 19, 50, 47, 48], [1920, 38, 55, 47, 48], [1992, 19, 50, 47, 48], [2016, 38, 43, 47, 48], [2160, 19, 42, 47, 48], [2184, 19, 43, 47, 48], [2208, 19, 44, 47, 48], [2232, 19, 43, 47, 48], [2256, 19, 41, 47, 48], [2280, 19, 38, 47, 48], [2304, 38, 48, 95, 48], [2376, 19, 43, 47, 48], [2400, 38, 48, 47, 48], [2472, 19, 43, 47, 48], [2496, 38, 48, 47, 48], [2640, 31, 43, 47, 48], [2688, 77, 48, 47, 48], [2832, 38, 43, 47, 48], [2880, 77, 48, 47, 48], [3024, 38, 43, 47, 48]],
                    96, 84, [24], False),
                _score_track('winds', '双簧管', 'Oboe',
                    [[0, 77, 79, 47, 68], [720, 31, 67, 79, 68], [720, 31, 79, 79, 68], [768, 77, 72, 79, 68], [768, 77, 84, 79, 68], [864, 31, 70, 79, 68], [864, 31, 82, 79, 68], [936, 16, 68, 79, 68], [936, 16, 80, 79, 68], [960, 115, 67, 79, 68], [960, 115, 79, 79, 68], [1104, 31, 65, 79, 68], [1104, 31, 77, 79, 68], [1152, 38, 63, 79, 68], [1152, 38, 75, 79, 68], [1224, 19, 62, 79, 68], [1224, 19, 74, 79, 68], [1248, 115, 60, 79, 68], [1248, 115, 72, 79, 68], [1392, 31, 62, 47, 68], [1392, 31, 74, 47, 68], [1440, 21, 63, 47, 68], [1440, 21, 75, 47, 68], [1472, 21, 62, 47, 68], [1472, 21, 74, 47, 68], [1504, 21, 60, 47, 68], [1504, 21, 72, 47, 68], [1536, 154, 67, 31, 68], [1536, 154, 79, 31, 68], [1728, 115, 62, 31, 68], [1728, 115, 74, 31, 68], [1872, 31, 62, 31, 68], [1872, 31, 74, 31, 68], [1920, 230, 67, 31, 68], [1920, 230, 79, 31, 68], [2208, 38, 77, 31, 68], [2256, 38, 75, 31, 68], [2304, 77, 74, 79, 68], [2400, 38, 67, 79, 68], [2472, 19, 67, 79, 68], [2496, 77, 74, 79, 68], [2592, 58, 77, 79, 68], [2664, 19, 75, 79, 68], [2688, 31, 74, 79, 68], [2880, 154, 68, 95, 68]],
                    96, 84, [3], False),
                _score_track('winds', '英国管', 'English horn',
                    [[0, 77, 67, 47, 69], [768, 922, 67, 47, 69], [1728, 115, 62, 31, 69], [1872, 38, 62, 31, 69], [1920, 230, 67, 31, 69], [2208, 38, 65, 31, 69], [2256, 38, 63, 31, 69], [2304, 77, 62, 79, 69], [2400, 38, 55, 79, 69], [2472, 19, 55, 79, 69], [2496, 77, 62, 79, 69], [2592, 58, 65, 79, 69], [2664, 19, 63, 79, 69], [2688, 31, 62, 79, 69], [2880, 154, 68, 95, 69]],
                    96, 84, [4], False),
                _score_track('horns', '第一圆号组', 'Horns I',
                    [[0, 154, 67, 95, 60], [192, 154, 68, 95, 60], [192, 154, 72, 95, 60], [384, 154, 67, 95, 60], [576, 154, 68, 95, 60], [576, 154, 72, 95, 60], [768, 691, 55, 47, 60], [768, 691, 67, 47, 60], [1536, 691, 68, 95, 60], [1536, 691, 72, 95, 60], [2304, 230, 65, 95, 60], [2304, 230, 71, 95, 60], [2592, 77, 65, 95, 60], [2592, 77, 72, 95, 60], [2688, 154, 65, 95, 60], [2688, 154, 71, 95, 60], [2880, 154, 59, 95, 60], [2880, 154, 68, 95, 60]],
                    96, 84, [11], False),
            ], '39a8ba95cd0ec86158c249480e7a8018d6a88e868960ab6ae56eb90893f239a4', 'https://gustavmahler.com/site/midi/symphony2/1st-movement-Allegro-maestoso-Totenfeier.midi'),
        _score_scene(1, 2, 'E大调第二主题：弦乐、长笛与圆号', 'E major second subject: strings, flute and horn',
            '第一小提琴的歌唱线条与大提琴低音分开，长笛和两组圆号可分别静音，听清主题与内声部。',
            'Separate the violin cantilena from the cello bass, then mute flute and the two horn groups to hear the theme against its inner parts.',
            76, 192, 224, 48, 55, 96, [4, 4], [
                _score_track('strings', '第一小提琴', 'Violins I',
                    [[0, 154, 71, 31, 48], [192, 77, 76, 31, 48], [288, 77, 78, 31, 48], [384, 77, 80, 31, 48], [480, 77, 81, 31, 48], [576, 77, 83, 31, 48], [672, 48, 85, 31, 48], [720, 38, 87, 31, 48], [768, 77, 90, 31, 48], [864, 154, 88, 31, 48], [1056, 48, 87, 31, 48], [1104, 38, 88, 31, 48], [1152, 48, 90, 31, 48], [1200, 38, 88, 31, 48], [1248, 48, 87, 31, 48], [1296, 38, 88, 31, 48], [1344, 48, 87, 31, 48], [1392, 38, 85, 31, 48], [1440, 48, 84, 31, 48], [1488, 38, 85, 31, 48], [1536, 96, 83, 31, 48], [1632, 154, 82, 31, 48], [1824, 48, 80, 31, 48], [1872, 38, 82, 31, 48], [1920, 96, 80, 31, 48], [2016, 154, 78, 31, 48], [2208, 48, 88, 31, 48], [2256, 38, 87, 31, 48], [2304, 96, 87, 31, 48], [2400, 154, 85, 31, 48], [2592, 48, 84, 31, 48], [2640, 38, 85, 31, 48], [2688, 48, 84, 31, 48], [2736, 77, 85, 31, 48], [2832, 77, 87, 31, 48], [2928, 48, 88, 31, 48], [2976, 48, 92, 31, 48], [3024, 38, 90, 31, 48]],
                    96, 76, [21], False),
                _score_track('strings', '大提琴', 'Cellos',
                    [[0, 26, 47, 31, 48], [32, 26, 46, 31, 48], [64, 26, 47, 31, 48], [96, 26, 49, 31, 48], [128, 26, 47, 31, 48], [160, 26, 46, 31, 48], [192, 77, 47, 31, 48], [384, 26, 47, 31, 48], [416, 26, 46, 31, 48], [448, 26, 47, 31, 48], [480, 26, 49, 31, 48], [512, 26, 47, 31, 48], [544, 26, 46, 31, 48], [576, 77, 47, 31, 48], [768, 26, 47, 31, 48], [800, 26, 46, 31, 48], [832, 26, 47, 31, 48], [864, 26, 49, 31, 48], [896, 26, 47, 31, 48], [928, 26, 46, 31, 48], [960, 77, 47, 31, 48], [1152, 154, 47, 31, 48], [1344, 77, 48, 31, 48], [1440, 77, 49, 31, 48], [1536, 21, 42, 15, 48], [1568, 21, 41, 15, 48], [1600, 21, 42, 15, 48], [1632, 21, 44, 15, 48], [1664, 21, 42, 15, 48], [1696, 21, 41, 15, 48], [1728, 77, 42, 15, 48], [1920, 21, 42, 15, 48], [1952, 21, 41, 15, 48], [1984, 21, 42, 15, 48], [2016, 21, 44, 15, 48], [2048, 21, 42, 15, 48], [2080, 21, 41, 15, 48], [2112, 77, 42, 15, 48], [2304, 21, 42, 15, 48], [2336, 21, 41, 15, 48], [2368, 21, 42, 15, 48], [2400, 21, 44, 15, 48], [2432, 21, 42, 15, 48], [2464, 21, 41, 15, 48], [2496, 77, 42, 15, 48], [2688, 21, 42, 15, 48], [2720, 21, 41, 15, 48], [2752, 21, 42, 15, 48], [2784, 21, 44, 15, 48], [2816, 21, 42, 15, 48], [2848, 21, 41, 15, 48], [2880, 77, 42, 15, 48]],
                    96, 76, [24], False),
                _score_track('winds', '长笛', 'Flute',
                    [[0, 1306, 71, 47, 73], [0, 1306, 83, 47, 73], [1344, 192, 68, 47, 73], [1344, 192, 80, 47, 73], [1536, 576, 66, 47, 73], [1536, 576, 78, 47, 73]],
                    96, 76, [2], False),
                _score_track('horns', '第一圆号组', 'Horns I',
                    [[0, 288, 64, 15, 60], [0, 288, 68, 15, 60], [288, 96, 59, 15, 60], [288, 96, 66, 15, 60], [384, 96, 56, 15, 60], [384, 96, 64, 15, 60], [480, 96, 59, 15, 60], [480, 96, 66, 15, 60], [576, 96, 64, 15, 60], [576, 96, 68, 15, 60], [672, 96, 59, 15, 60], [672, 96, 66, 15, 60], [768, 288, 56, 15, 60], [768, 288, 64, 15, 60], [1056, 96, 59, 15, 60], [1056, 96, 66, 15, 60], [1152, 96, 64, 15, 60], [1152, 96, 68, 15, 60], [1248, 48, 68, 15, 60], [1248, 48, 71, 15, 60], [1296, 48, 66, 15, 60], [1296, 48, 69, 15, 60], [1344, 154, 64, 15, 60], [1344, 154, 68, 15, 60], [1536, 1459, 64, 15, 60], [1536, 1459, 66, 15, 60]],
                    96, 76, [11], False),
                _score_track('horns', '第二圆号组', 'Horns II',
                    [[384, 288, 64, 31, 60], [384, 288, 68, 31, 60], [672, 96, 59, 31, 60], [672, 96, 66, 31, 60], [768, 96, 56, 31, 60], [768, 96, 64, 31, 60], [864, 96, 59, 31, 60], [864, 96, 66, 31, 60], [960, 96, 64, 31, 60], [960, 96, 68, 31, 60], [1056, 48, 68, 31, 60], [1056, 48, 71, 31, 60], [1104, 48, 66, 31, 60], [1104, 48, 69, 31, 60], [1152, 96, 64, 31, 60], [1152, 96, 68, 31, 60], [1248, 230, 56, 31, 60], [1248, 230, 64, 31, 60], [1536, 288, 61, 47, 60], [1824, 96, 59, 47, 60], [1920, 288, 58, 47, 60], [1920, 288, 61, 47, 60], [2208, 77, 56, 63, 60], [2208, 77, 59, 63, 60], [2304, 154, 54, 47, 60], [2304, 154, 58, 47, 60], [2496, 192, 55, 47, 60], [2496, 192, 59, 47, 60], [2688, 96, 55, 47, 60], [2688, 96, 58, 47, 60], [2784, 96, 56, 47, 60], [2784, 96, 59, 47, 60], [2880, 96, 57, 47, 60], [2880, 96, 60, 47, 60], [2976, 96, 58, 47, 60], [2976, 96, 61, 47, 60]],
                    96, 76, [12], False),
            ], '39a8ba95cd0ec86158c249480e7a8018d6a88e868960ab6ae56eb90893f239a4', 'https://gustavmahler.com/site/midi/symphony2/1st-movement-Allegro-maestoso-Totenfeier.midi'),
        _score_scene(1, 3, '展开部：木管、圆号与大提琴的层次', 'Development: winds and horn over cello motion',
            '大提琴连续运动、长笛旋律、圆号回应和竖琴分解和弦来自同一段原始数字谱，避免用平行移调制造伪对位。',
            'Cello motion, flute melody, horn responses and harp arpeggios come from the same source passage; the layers are not generated by parallel transposition.',
            96, 832, 864, 208, 215, 96, [4, 4], [
                _score_track('strings', '第一小提琴', 'Violins I',
                    [[0, 230, 77, 111, 44], [0, 230, 81, 111, 44], [0, 230, 84, 111, 44], [288, 77, 72, 111, 44], [288, 77, 79, 111, 44], [288, 77, 84, 111, 44], [384, 230, 77, 111, 44], [384, 230, 81, 111, 44], [384, 230, 84, 111, 44], [672, 77, 72, 111, 44], [672, 77, 79, 111, 44], [672, 77, 84, 111, 44], [768, 230, 77, 111, 44], [768, 230, 81, 111, 44], [768, 230, 84, 111, 44], [1056, 77, 72, 111, 44], [1056, 77, 81, 111, 44], [1056, 77, 84, 111, 44], [1152, 228, 81, 111, 44], [1152, 228, 84, 111, 44], [1440, 76, 77, 111, 44], [1440, 76, 81, 111, 44], [1536, 38, 77, 111, 48], [1536, 38, 79, 111, 48]],
                    96, 96, [21], False),
                _score_track('strings', '大提琴', 'Cellos',
                    [[0, 12, 60, 15, 48], [12, 12, 62, 15, 48], [24, 12, 60, 15, 48], [36, 12, 62, 15, 48], [48, 12, 60, 15, 48], [60, 12, 62, 15, 48], [72, 12, 60, 15, 48], [84, 12, 62, 15, 48], [96, 12, 60, 15, 48], [108, 12, 62, 15, 48], [120, 12, 60, 15, 48], [132, 12, 62, 15, 48], [144, 12, 60, 15, 48], [156, 12, 62, 15, 48], [168, 12, 60, 15, 48], [180, 12, 62, 15, 48], [192, 12, 60, 15, 48], [204, 12, 62, 15, 48], [216, 12, 60, 15, 48], [228, 12, 62, 15, 48], [240, 12, 60, 15, 48], [252, 12, 62, 15, 48], [264, 12, 60, 15, 48], [276, 12, 62, 15, 48], [288, 12, 60, 15, 48], [300, 12, 62, 15, 48], [312, 12, 60, 15, 48], [324, 12, 62, 15, 48], [336, 12, 60, 15, 48], [348, 12, 62, 15, 48], [360, 12, 60, 15, 48], [372, 12, 62, 15, 48], [384, 12, 60, 15, 48], [396, 12, 62, 15, 48], [408, 12, 60, 15, 48], [420, 12, 62, 15, 48], [432, 12, 60, 15, 48], [444, 12, 62, 15, 48], [456, 12, 60, 15, 48], [468, 12, 62, 15, 48], [480, 12, 60, 15, 48], [492, 12, 62, 15, 48], [504, 12, 60, 15, 48], [516, 12, 62, 15, 48], [528, 12, 60, 15, 48], [540, 12, 62, 15, 48], [552, 12, 60, 15, 48], [564, 12, 62, 15, 48], [576, 12, 60, 15, 48], [588, 12, 62, 15, 48], [600, 12, 60, 15, 48], [612, 12, 62, 15, 48], [624, 12, 60, 15, 48], [636, 12, 62, 15, 48], [648, 12, 60, 15, 48], [660, 12, 62, 15, 48], [672, 12, 60, 15, 48], [684, 12, 62, 15, 48], [696, 12, 60, 15, 48], [708, 12, 62, 15, 48], [720, 12, 60, 15, 48], [732, 12, 62, 15, 48], [744, 12, 60, 15, 48], [756, 12, 62, 15, 48], [768, 12, 60, 15, 48], [780, 12, 62, 15, 48], [792, 12, 60, 15, 48], [804, 12, 62, 15, 48], [816, 12, 60, 15, 48], [828, 12, 62, 15, 48], [840, 12, 60, 15, 48], [852, 12, 62, 15, 48], [864, 12, 60, 15, 48], [876, 12, 62, 15, 48], [888, 12, 60, 15, 48], [900, 12, 62, 15, 48], [912, 12, 60, 15, 48], [924, 12, 62, 15, 48], [936, 12, 60, 15, 48], [948, 12, 62, 15, 48], [960, 12, 60, 15, 48], [972, 12, 62, 15, 48], [984, 12, 60, 15, 48], [996, 12, 62, 15, 48], [1008, 12, 60, 15, 48], [1020, 12, 62, 15, 48], [1032, 12, 60, 15, 48], [1044, 12, 62, 15, 48], [1056, 12, 60, 15, 48], [1068, 12, 62, 15, 48], [1080, 12, 60, 15, 48], [1092, 12, 62, 15, 48], [1104, 12, 60, 15, 48], [1116, 12, 62, 15, 48], [1128, 12, 60, 15, 48], [1140, 12, 62, 15, 48], [1152, 12, 60, 15, 48], [1164, 12, 62, 15, 48], [1176, 12, 60, 15, 48], [1188, 12, 62, 15, 48], [1200, 12, 60, 15, 48], [1212, 12, 62, 15, 48], [1224, 12, 60, 15, 48], [1236, 12, 62, 15, 48], [1248, 12, 60, 15, 48], [1260, 12, 62, 15, 48], [1272, 12, 60, 15, 48], [1284, 12, 62, 15, 48], [1296, 12, 60, 15, 48], [1308, 12, 62, 15, 48], [1320, 12, 60, 15, 48], [1332, 12, 62, 15, 48], [1344, 12, 60, 15, 48], [1356, 12, 62, 15, 48], [1368, 12, 60, 15, 48], [1380, 12, 62, 15, 48], [1392, 12, 60, 15, 48], [1404, 12, 62, 15, 48], [1416, 12, 60, 15, 48], [1428, 12, 62, 15, 48], [1440, 12, 60, 15, 48], [1452, 12, 62, 15, 48], [1464, 12, 60, 15, 48], [1476, 12, 62, 15, 48], [1488, 12, 60, 15, 48], [1500, 12, 62, 15, 48], [1512, 12, 60, 15, 48], [1524, 12, 62, 15, 48], [1536, 12, 60, 15, 48], [1548, 12, 62, 15, 48], [1560, 12, 60, 15, 48], [1572, 12, 62, 15, 48], [1584, 12, 60, 15, 48], [1596, 12, 62, 15, 48], [1608, 12, 60, 15, 48], [1620, 12, 62, 15, 48], [1632, 12, 60, 15, 48], [1644, 12, 62, 15, 48], [1656, 12, 60, 15, 48], [1668, 12, 62, 15, 48], [1680, 12, 60, 15, 48], [1692, 12, 62, 15, 48], [1704, 12, 60, 15, 48], [1716, 12, 62, 15, 48], [1728, 12, 60, 15, 48], [1740, 12, 62, 15, 48], [1752, 12, 60, 15, 48], [1764, 12, 62, 15, 48], [1776, 12, 60, 15, 48], [1788, 12, 62, 15, 48], [1800, 12, 60, 15, 48], [1812, 12, 62, 15, 48], [1824, 12, 60, 15, 48], [1836, 12, 62, 15, 48], [1848, 12, 60, 15, 48], [1860, 12, 62, 15, 48], [1872, 12, 60, 15, 48], [1884, 12, 62, 15, 48], [1896, 12, 60, 15, 48], [1908, 12, 62, 15, 48], [1920, 12, 60, 15, 48], [1932, 12, 62, 15, 48], [1944, 12, 60, 15, 48], [1956, 12, 62, 15, 48], [1968, 12, 60, 15, 48], [1980, 12, 62, 15, 48], [1992, 12, 60, 15, 48], [2004, 12, 62, 15, 48], [2016, 12, 60, 15, 48], [2028, 12, 62, 15, 48], [2040, 12, 60, 15, 48], [2052, 12, 62, 15, 48], [2064, 12, 60, 15, 48], [2076, 12, 62, 15, 48], [2088, 12, 60, 15, 48], [2100, 12, 62, 15, 48], [2112, 12, 60, 15, 48], [2124, 12, 62, 15, 48], [2136, 12, 60, 15, 48], [2148, 12, 62, 15, 48], [2160, 12, 60, 15, 48], [2172, 12, 62, 15, 48], [2184, 12, 60, 15, 48], [2196, 12, 62, 15, 48], [2208, 12, 60, 15, 48], [2220, 12, 62, 15, 48], [2232, 12, 60, 15, 48], [2244, 12, 62, 15, 48], [2256, 12, 60, 15, 48], [2268, 12, 62, 15, 48], [2280, 12, 60, 15, 48], [2292, 12, 62, 15, 48], [2304, 12, 60, 15, 48], [2316, 12, 62, 15, 48], [2328, 12, 60, 15, 48], [2340, 12, 62, 15, 48], [2352, 12, 60, 15, 48], [2364, 12, 62, 15, 48], [2376, 12, 60, 15, 48], [2388, 12, 62, 15, 48], [2400, 12, 60, 15, 48], [2412, 12, 62, 15, 48], [2424, 12, 60, 15, 48], [2436, 12, 62, 15, 48], [2448, 12, 60, 15, 48], [2460, 12, 62, 15, 48], [2472, 12, 60, 15, 48], [2484, 12, 62, 15, 48], [2496, 12, 60, 15, 48], [2508, 12, 62, 15, 48], [2520, 12, 60, 15, 48], [2532, 12, 62, 15, 48], [2544, 12, 60, 15, 48], [2556, 12, 62, 15, 48], [2568, 12, 60, 15, 48], [2580, 12, 62, 15, 48], [2592, 12, 60, 15, 48], [2604, 12, 62, 15, 48], [2616, 12, 60, 15, 48], [2628, 12, 62, 15, 48], [2640, 12, 60, 15, 48], [2652, 12, 62, 15, 48], [2664, 12, 60, 15, 48], [2676, 12, 62, 15, 48], [2688, 12, 60, 15, 48], [2700, 12, 62, 15, 48], [2712, 12, 60, 15, 48], [2724, 12, 62, 15, 48], [2736, 12, 60, 15, 48], [2748, 12, 62, 15, 48], [2760, 12, 60, 15, 48], [2772, 12, 62, 15, 48], [2784, 12, 60, 15, 48], [2796, 12, 62, 15, 48], [2808, 12, 60, 15, 48], [2820, 12, 62, 15, 48], [2832, 12, 60, 15, 48], [2844, 12, 62, 15, 48], [2856, 12, 60, 15, 48], [2868, 12, 62, 15, 48], [2880, 12, 60, 15, 48], [2892, 12, 62, 15, 48], [2904, 12, 60, 15, 48], [2916, 12, 62, 15, 48], [2928, 12, 60, 15, 48], [2940, 12, 62, 15, 48], [2952, 12, 60, 15, 48], [2964, 12, 62, 15, 48], [2976, 12, 60, 15, 48], [2988, 12, 62, 15, 48], [3000, 12, 60, 15, 48], [3012, 12, 62, 15, 48], [3024, 12, 60, 15, 48], [3036, 12, 62, 15, 48], [3048, 12, 60, 15, 48], [3060, 12, 62, 15, 48]],
                    96, 96, [24], False),
                _score_track('winds', '长笛', 'Flute',
                    [[0, 192, 72, 47, 73], [192, 96, 77, 47, 73], [288, 96, 79, 47, 73], [384, 96, 81, 47, 73], [480, 96, 82, 47, 73], [576, 96, 84, 47, 73], [672, 48, 86, 47, 73], [720, 38, 88, 47, 73], [768, 96, 91, 47, 73], [864, 154, 89, 47, 73], [1056, 38, 88, 47, 73], [1104, 38, 89, 47, 73], [1152, 48, 91, 47, 73], [1200, 38, 89, 47, 73], [1248, 48, 88, 47, 73], [1296, 38, 89, 47, 73], [1344, 48, 88, 47, 73], [1392, 38, 86, 47, 73], [1440, 48, 85, 47, 73], [1488, 38, 86, 47, 73], [1536, 96, 84, 47, 73], [1632, 154, 83, 47, 73], [1824, 48, 81, 47, 73], [1872, 38, 83, 47, 73], [1920, 96, 81, 47, 73], [2016, 154, 79, 47, 73], [2208, 48, 89, 47, 73], [2256, 38, 88, 47, 73], [2304, 96, 88, 47, 73], [2400, 154, 86, 47, 73], [2496, 288, 71, 47, 73], [2592, 48, 85, 47, 73], [2640, 48, 86, 47, 73], [2688, 48, 85, 47, 73], [2736, 96, 86, 47, 73], [2784, 96, 72, 47, 73], [2832, 96, 88, 47, 73], [2880, 96, 73, 47, 73], [2928, 48, 89, 47, 73], [2976, 77, 74, 47, 73], [2976, 48, 93, 47, 73], [3024, 48, 91, 47, 73]],
                    96, 96, [2], False),
                _score_track('horns', '第二圆号组', 'Horns II',
                    [[0, 1248, 60, 31, 60], [1248, 96, 61, 31, 60], [1344, 96, 62, 31, 60], [1440, 48, 64, 31, 60], [1488, 48, 65, 31, 60], [1536, 1536, 67, 31, 60]],
                    96, 96, [12], False),
                _score_track('strings', '竖琴', 'Harp',
                    [[0, 38, 65, 47, 46], [48, 38, 64, 47, 46], [96, 38, 62, 47, 46], [144, 38, 60, 47, 46], [192, 38, 58, 47, 46], [240, 38, 57, 47, 46], [288, 38, 55, 47, 46], [336, 38, 60, 47, 46], [384, 38, 65, 47, 46], [432, 38, 64, 47, 46], [480, 38, 62, 47, 46], [528, 38, 60, 47, 46], [576, 38, 58, 47, 46], [624, 38, 57, 47, 46], [672, 38, 55, 47, 46], [720, 38, 60, 47, 46], [768, 38, 65, 47, 46], [816, 38, 64, 47, 46], [864, 38, 62, 47, 46], [912, 38, 60, 47, 46], [960, 38, 65, 47, 46], [1008, 38, 64, 47, 46], [1056, 38, 62, 47, 46], [1104, 38, 60, 47, 46], [1152, 77, 65, 47, 46], [1248, 77, 61, 47, 46], [1344, 77, 62, 47, 46], [1440, 38, 64, 47, 46], [1488, 38, 65, 47, 46], [1536, 77, 67, 47, 46], [1632, 77, 74, 47, 46], [1728, 77, 77, 47, 46], [1824, 77, 72, 47, 46], [1920, 77, 71, 47, 46], [2016, 77, 74, 47, 46], [2112, 77, 77, 47, 46], [2208, 77, 69, 47, 46], [2304, 77, 67, 47, 46], [2400, 77, 71, 47, 46], [2496, 77, 77, 47, 46], [2592, 77, 71, 47, 46], [2688, 77, 77, 47, 46], [2784, 77, 72, 47, 46], [2880, 77, 73, 47, 46], [2976, 77, 74, 47, 46]],
                    96, 96, [18], False),
            ], '39a8ba95cd0ec86158c249480e7a8018d6a88e868960ab6ae56eb90893f239a4', 'https://gustavmahler.com/site/midi/symphony2/1st-movement-Allegro-maestoso-Totenfeier.midi'),
    ],
    "2": [
        _score_scene(2, 1, '兰德勒：小提琴与大提琴的对话', 'Ländler: violin and cello dialogue',
            '旋律与大提琴线条独立呈现；低音提琴保留舞步，长笛和圆号只在原始数字谱记有音符处发声。',
            'The melody and cello line remain separate. Double bass keeps the dance step; flute and horn enter only where the source contains notes.',
            68, 33, 60, 22, 39, 120, [3, 8], [
                _score_track('strings', '第一小提琴', 'Violins I',
                    [[540, 30, 65, 52, 48], [570, 30, 63, 52, 48], [600, 30, 62, 52, 48], [630, 30, 63, 52, 48], [660, 60, 64, 52, 48], [720, 30, 70, 52, 48], [750, 30, 68, 52, 48], [780, 30, 73, 52, 48], [810, 30, 68, 52, 48], [840, 47, 65, 52, 48], [900, 30, 65, 52, 48], [930, 30, 63, 52, 48], [960, 30, 68, 52, 48], [990, 30, 63, 52, 48], [1020, 60, 60, 52, 48], [1080, 60, 58, 52, 48], [1140, 60, 63, 52, 48], [1200, 60, 59, 52, 48], [1260, 60, 60, 52, 48], [1320, 60, 63, 52, 48], [1380, 47, 60, 52, 48], [1440, 3, 65, 52, 48], [1443, 3, 67, 52, 48], [1447, 22, 65, 52, 48], [1470, 30, 64, 52, 48], [1500, 30, 65, 52, 48], [1530, 30, 67, 52, 48], [1560, 30, 68, 52, 48], [1590, 23, 70, 52, 48], [1620, 30, 72, 52, 48], [1650, 30, 80, 52, 48], [1680, 47, 75, 52, 48], [1740, 30, 68, 52, 48], [1770, 30, 70, 52, 48], [1800, 30, 72, 52, 48], [1830, 30, 75, 52, 48], [1860, 30, 77, 52, 48], [1890, 30, 75, 52, 48], [1920, 30, 73, 52, 48], [1950, 30, 63, 52, 48], [1980, 72, 68, 52, 48], [2070, 30, 75, 52, 48], [2100, 30, 74, 52, 48], [2130, 30, 75, 52, 48], [2160, 252, 63, 52, 48], [2430, 30, 75, 52, 48], [2460, 30, 74, 52, 48], [2490, 30, 75, 52, 48], [2520, 23, 63, 52, 48], [2580, 60, 63, 52, 48], [2640, 60, 70, 52, 48], [2700, 227, 63, 52, 48]],
                    120, 68, [21], False),
                _score_track('strings', '大提琴', 'Cellos',
                    [[0, 30, 60, 52, 48], [30, 30, 58, 52, 48], [60, 30, 57, 52, 48], [90, 30, 58, 52, 48], [120, 30, 55, 52, 48], [150, 30, 51, 52, 48], [180, 30, 61, 52, 48], [210, 30, 60, 52, 48], [240, 30, 59, 52, 48], [270, 23, 60, 52, 48], [300, 60, 60, 52, 48], [360, 180, 55, 48, 48], [540, 30, 65, 52, 48], [570, 30, 63, 52, 48], [600, 30, 62, 52, 48], [630, 30, 63, 52, 48], [660, 60, 64, 52, 48], [720, 276, 56, 48, 48], [1020, 60, 60, 52, 48], [1080, 30, 58, 52, 48], [1110, 23, 63, 52, 48], [1140, 3, 63, 52, 48], [1143, 3, 65, 52, 48], [1147, 52, 63, 52, 48], [1200, 30, 59, 52, 48], [1230, 23, 63, 52, 48], [1260, 30, 60, 52, 48], [1290, 23, 63, 52, 48], [1320, 3, 63, 52, 48], [1323, 3, 65, 52, 48], [1327, 52, 63, 52, 48], [1380, 30, 60, 52, 48], [1410, 23, 63, 52, 48], [1440, 180, 65, 48, 48], [1620, 120, 60, 48, 48], [1740, 60, 62, 48, 48], [1800, 276, 63, 48, 48], [2100, 60, 70, 48, 48], [2160, 120, 60, 48, 48], [2280, 60, 61, 48, 48], [2340, 96, 63, 48, 48], [2460, 60, 70, 48, 48], [2520, 120, 60, 48, 48], [2640, 60, 61, 48, 48], [2700, 180, 63, 48, 48], [2880, 38, 60, 48, 48]],
                    120, 68, [24], False),
                _score_track('strings', '低音提琴', 'Double basses',
                    [[0, 47, 43, 52, 45], [60, 47, 39, 52, 45], [120, 47, 46, 52, 45], [180, 47, 44, 52, 45], [240, 47, 39, 52, 45], [300, 47, 44, 52, 45], [360, 47, 46, 52, 45], [420, 47, 39, 52, 45], [480, 47, 49, 52, 45], [540, 47, 36, 52, 45], [540, 47, 48, 52, 45], [600, 47, 39, 52, 45], [600, 47, 51, 52, 45], [660, 47, 44, 52, 45], [660, 47, 56, 52, 45], [720, 47, 37, 52, 45], [720, 47, 49, 52, 45], [780, 47, 41, 52, 45], [780, 47, 53, 52, 45], [840, 47, 37, 52, 45], [840, 47, 49, 52, 45], [900, 47, 39, 52, 45], [900, 47, 51, 52, 45], [960, 47, 36, 52, 45], [960, 47, 48, 52, 45], [1020, 47, 32, 52, 45], [1020, 47, 44, 52, 45], [1080, 47, 43, 52, 45], [1140, 47, 39, 52, 45], [1200, 47, 43, 52, 45], [1260, 47, 44, 52, 45], [1320, 47, 39, 52, 45], [1380, 47, 44, 52, 45], [1440, 47, 37, 52, 45], [1440, 47, 49, 52, 45], [1500, 47, 41, 52, 45], [1500, 47, 53, 52, 45], [1560, 47, 38, 52, 45], [1560, 47, 50, 52, 45], [1620, 47, 39, 52, 45], [1620, 47, 51, 52, 45], [1680, 47, 56, 52, 45], [1740, 47, 40, 52, 45], [1740, 47, 52, 52, 45], [1800, 47, 39, 52, 45], [1800, 47, 51, 52, 45], [1860, 47, 39, 52, 45], [1920, 47, 51, 52, 45], [1980, 47, 32, 52, 45], [1980, 47, 44, 52, 45], [2040, 47, 51, 52, 45], [2100, 47, 63, 52, 45], [2160, 47, 44, 52, 45], [2220, 47, 51, 52, 45], [2280, 47, 63, 52, 45], [2340, 47, 32, 52, 45], [2340, 47, 44, 52, 45], [2400, 47, 51, 52, 45], [2460, 47, 63, 52, 45], [2520, 47, 44, 52, 45], [2580, 47, 51, 52, 45], [2640, 47, 63, 52, 45], [2700, 47, 32, 52, 45], [2700, 47, 44, 52, 45], [2760, 47, 51, 52, 45], [2820, 47, 63, 52, 45], [2940, 47, 51, 52, 45], [3000, 47, 63, 52, 45], [3120, 47, 51, 52, 45], [3180, 47, 63, 52, 45]],
                    120, 68, [25], False),
                _score_track('winds', '长笛', 'Flute',
                    [[1800, 276, 63, 52, 73], [2100, 60, 70, 52, 73], [2160, 276, 63, 52, 73], [2460, 60, 70, 52, 73], [2520, 276, 63, 52, 73], [2820, 60, 70, 52, 73], [2880, 276, 63, 52, 73]],
                    120, 68, [2], False),
                _score_track('horns', '第一圆号组', 'Horns I',
                    [[3060, 180, 63, 52, 60]],
                    120, 68, [11], False),
            ], '6657af3fca1c9d129566d4f149ee99db8f1dad25790d33a30085618dc962c612', 'https://gustavmahler.com/site/midi/symphony2/2nd-movement-Andante-moderato.midi'),
        _score_scene(2, 2, '三连音插段：交错弦乐与圆号', 'Triplet episode: interlocking strings and horn',
            '将两组小提琴和大提琴分开，可听见短音型的接力；单簧管与圆号保留不同的时值与休止。',
            'Separate the two violin sections and cello to follow the relay of short figures; clarinet and horn retain different durations and rests.',
            68, 60, 97.5, 40, 64, 120, [3, 8], [
                _score_track('strings', '第一小提琴', 'Violins I',
                    [[120, 12, 87, 48, 48], [140, 12, 86, 48, 48], [160, 12, 87, 48, 48], [180, 12, 88, 48, 48], [200, 12, 87, 48, 48], [220, 12, 85, 48, 48], [240, 12, 83, 48, 48], [260, 12, 82, 48, 48], [280, 12, 80, 48, 48], [300, 12, 79, 48, 48], [320, 12, 80, 48, 48], [340, 12, 82, 48, 48], [360, 20, 80, 48, 48], [380, 12, 75, 48, 48], [400, 12, 75, 48, 48], [420, 12, 75, 48, 48], [440, 12, 75, 48, 48], [460, 12, 75, 48, 48], [480, 12, 75, 48, 48], [500, 12, 75, 48, 48], [520, 12, 75, 48, 48], [540, 12, 76, 48, 48], [560, 12, 75, 48, 48], [580, 12, 76, 48, 48], [600, 12, 80, 48, 48], [620, 12, 79, 48, 48], [640, 12, 80, 48, 48], [660, 12, 83, 48, 48], [680, 12, 82, 48, 48], [700, 12, 80, 48, 48], [720, 20, 82, 48, 48], [740, 12, 75, 48, 48], [760, 12, 75, 48, 48], [780, 12, 75, 48, 48], [800, 12, 75, 48, 48], [820, 12, 75, 48, 48], [840, 12, 75, 48, 48], [860, 12, 75, 48, 48], [880, 12, 75, 48, 48], [900, 12, 80, 48, 48], [920, 12, 79, 48, 48], [940, 12, 80, 48, 48], [960, 12, 83, 48, 48], [980, 12, 82, 48, 48], [1000, 12, 83, 48, 48], [1020, 12, 87, 48, 48], [1040, 12, 86, 48, 48], [1060, 12, 87, 48, 48], [1080, 12, 79, 48, 48], [1100, 12, 78, 48, 48], [1120, 12, 79, 48, 48], [1140, 12, 82, 48, 48], [1160, 12, 81, 48, 48], [1180, 12, 82, 48, 48], [1200, 12, 87, 48, 48], [1220, 12, 86, 48, 48], [1240, 12, 87, 48, 48], [1260, 12, 76, 48, 48], [1280, 12, 75, 48, 48], [1300, 12, 76, 48, 48], [1320, 12, 80, 48, 48], [1340, 12, 83, 48, 48], [1360, 12, 82, 48, 48], [1380, 12, 80, 48, 48], [1400, 12, 78, 48, 48], [1420, 12, 76, 48, 48], [1440, 12, 75, 48, 48], [1460, 12, 74, 48, 48], [1480, 12, 73, 48, 48], [1500, 12, 71, 48, 48], [1520, 12, 70, 48, 48], [1540, 12, 68, 48, 48], [1560, 12, 67, 48, 48], [1580, 12, 66, 48, 48], [1600, 12, 64, 48, 48], [1620, 20, 63, 48, 48], [2100, 12, 79, 48, 48], [2120, 12, 80, 48, 48], [2140, 12, 82, 48, 48], [2160, 12, 81, 48, 48], [2180, 12, 80, 48, 48], [2200, 12, 78, 48, 48], [2220, 12, 76, 48, 48], [2240, 12, 75, 48, 48], [2260, 12, 73, 48, 48], [2280, 12, 72, 48, 48], [2300, 12, 73, 48, 48], [2320, 12, 75, 48, 48], [2340, 12, 73, 48, 48], [2360, 12, 75, 48, 48], [2380, 12, 76, 48, 48], [2400, 12, 68, 48, 48], [2420, 12, 72, 48, 48], [2440, 12, 73, 48, 48], [2460, 12, 64, 48, 48], [2480, 12, 67, 48, 48], [2500, 12, 68, 48, 48], [2520, 12, 71, 48, 48], [2540, 12, 75, 48, 48], [2560, 12, 76, 48, 48], [2580, 12, 68, 48, 48], [2600, 12, 70, 48, 48], [2620, 12, 71, 48, 48], [2640, 12, 64, 48, 48], [2660, 12, 67, 48, 48], [2680, 12, 68, 48, 48], [2700, 12, 71, 48, 48], [2720, 12, 74, 48, 48], [2740, 12, 75, 48, 48], [2760, 12, 66, 48, 48], [2780, 12, 70, 48, 48], [2800, 12, 71, 48, 48], [2820, 12, 63, 48, 48], [2840, 12, 65, 48, 48], [2860, 12, 66, 48, 48], [2880, 12, 60, 48, 48], [2900, 12, 63, 48, 48], [2920, 12, 64, 48, 48], [2940, 12, 66, 48, 48], [2960, 12, 63, 48, 48], [2980, 12, 60, 48, 48], [3000, 12, 61, 48, 48], [3020, 12, 64, 48, 48], [3040, 12, 66, 48, 48], [3060, 12, 68, 48, 48], [3080, 12, 65, 48, 48], [3100, 12, 62, 48, 48], [3120, 12, 63, 48, 48], [3140, 12, 66, 48, 48], [3160, 12, 68, 48, 48], [3180, 12, 69, 48, 48], [3200, 12, 66, 48, 48], [3220, 12, 63, 48, 48], [3240, 12, 64, 48, 48], [3260, 12, 68, 48, 48], [3280, 12, 70, 48, 48], [3300, 12, 71, 48, 48], [3320, 12, 68, 48, 48], [3340, 12, 65, 48, 48], [3360, 12, 71, 48, 48], [3380, 12, 68, 48, 48], [3400, 12, 64, 48, 48], [3420, 12, 71, 48, 48], [3440, 12, 68, 48, 48], [3460, 12, 63, 48, 48], [3480, 12, 71, 48, 48], [3500, 12, 68, 48, 48], [3520, 12, 62, 48, 48], [3540, 12, 72, 48, 48], [3560, 12, 69, 48, 48], [3580, 12, 66, 48, 48], [3600, 12, 72, 48, 48], [3620, 12, 69, 48, 48], [3640, 12, 65, 48, 48], [3660, 12, 72, 48, 48], [3680, 12, 69, 48, 48], [3700, 12, 64, 48, 48], [3720, 12, 73, 48, 48], [3740, 12, 72, 48, 48], [3760, 12, 73, 48, 48], [3840, 12, 73, 48, 48], [3860, 12, 72, 48, 48], [3880, 12, 73, 48, 48], [3960, 12, 63, 48, 48], [3980, 12, 63, 48, 48], [4000, 12, 63, 48, 48], [4020, 12, 63, 48, 48], [4040, 12, 63, 48, 48], [4060, 12, 63, 48, 48], [4080, 12, 63, 48, 48], [4100, 12, 63, 48, 48], [4120, 12, 63, 48, 48], [4140, 12, 63, 48, 48], [4160, 12, 63, 48, 48], [4180, 12, 63, 48, 48], [4200, 12, 63, 48, 48], [4220, 12, 63, 48, 48], [4240, 12, 63, 48, 48], [4260, 12, 63, 48, 48], [4280, 12, 63, 48, 48], [4300, 12, 63, 48, 48], [4320, 12, 63, 48, 48], [4340, 12, 63, 48, 48], [4360, 12, 63, 48, 48], [4380, 12, 63, 48, 48], [4400, 12, 63, 48, 48], [4420, 12, 63, 48, 48], [4440, 12, 63, 48, 48], [4460, 12, 63, 48, 48], [4480, 12, 63, 48, 48]],
                    120, 68, [21], False),
                _score_track('strings', '第二小提琴', 'Violins II',
                    [[840, 12, 73, 48, 48], [860, 12, 71, 48, 48], [880, 12, 70, 48, 48], [900, 12, 71, 48, 48], [920, 12, 70, 48, 48], [940, 12, 71, 48, 48], [960, 12, 75, 48, 48], [980, 12, 78, 48, 48], [1000, 12, 76, 48, 48], [1020, 12, 75, 48, 48], [1040, 12, 73, 48, 48], [1060, 12, 71, 48, 48], [1080, 12, 70, 48, 48], [1100, 12, 69, 48, 48], [1120, 12, 70, 48, 48], [1140, 12, 73, 48, 48], [1160, 12, 76, 48, 48], [1180, 12, 75, 48, 48], [1200, 12, 73, 48, 48], [1220, 12, 71, 48, 48], [1240, 12, 70, 48, 48], [1260, 12, 68, 48, 48], [1280, 12, 67, 48, 48], [1300, 12, 68, 48, 48], [1320, 12, 71, 48, 48], [1340, 12, 74, 48, 48], [1360, 12, 73, 48, 48], [1380, 12, 71, 48, 48], [1400, 12, 70, 48, 48], [1420, 12, 68, 48, 48], [1440, 12, 67, 48, 48], [1460, 12, 66, 48, 48], [1480, 12, 64, 48, 48], [1500, 12, 63, 48, 48], [1520, 12, 61, 48, 48], [1540, 12, 59, 48, 48], [1560, 12, 58, 48, 48], [1580, 12, 61, 48, 48], [1600, 12, 64, 48, 48], [1620, 12, 63, 48, 48], [1640, 12, 63, 48, 48], [1660, 12, 63, 48, 48], [1680, 12, 63, 48, 48], [1700, 12, 63, 48, 48], [1720, 12, 63, 48, 48], [1740, 12, 63, 48, 48], [1760, 12, 63, 48, 48], [1780, 12, 63, 48, 48], [1800, 12, 64, 48, 48], [1820, 12, 63, 48, 48], [1840, 12, 64, 48, 48], [1860, 12, 68, 48, 48], [1880, 12, 67, 48, 48], [1900, 12, 68, 48, 48], [1920, 12, 71, 48, 48], [1940, 12, 70, 48, 48], [1960, 12, 68, 48, 48], [1980, 12, 74, 48, 48], [2000, 12, 75, 48, 48], [2020, 12, 76, 48, 48], [2040, 12, 75, 48, 48], [2060, 12, 73, 48, 48], [2080, 12, 71, 48, 48], [2100, 12, 70, 48, 48], [2120, 12, 71, 48, 48], [2140, 12, 73, 48, 48], [2160, 12, 72, 48, 48], [2180, 12, 71, 48, 48], [2200, 12, 69, 48, 48], [2220, 12, 68, 48, 48], [2240, 12, 66, 48, 48], [2260, 12, 64, 48, 48], [2280, 12, 63, 48, 48], [2300, 12, 64, 48, 48], [2320, 12, 66, 48, 48], [2340, 12, 68, 48, 48], [2360, 12, 67, 48, 48], [2380, 12, 68, 48, 48], [2400, 12, 64, 48, 48], [2420, 12, 63, 48, 48], [2440, 12, 64, 48, 48], [2460, 12, 61, 48, 48], [2480, 12, 60, 48, 48], [2500, 12, 61, 48, 48], [2520, 12, 68, 48, 48], [2540, 12, 67, 48, 48], [2560, 12, 68, 48, 48], [2580, 12, 64, 48, 48], [2600, 12, 63, 48, 48], [2620, 12, 64, 48, 48], [2640, 12, 59, 48, 48], [2660, 12, 58, 48, 48], [2680, 12, 59, 48, 48], [2700, 12, 66, 48, 48], [2720, 12, 65, 48, 48], [2740, 12, 66, 48, 48], [2760, 12, 63, 48, 48], [2780, 12, 62, 48, 48], [2800, 12, 63, 48, 48], [2820, 12, 59, 48, 48], [2840, 12, 58, 48, 48], [2860, 12, 59, 48, 48], [2880, 12, 60, 48, 48], [2900, 12, 60, 48, 48], [2920, 12, 60, 48, 48], [2940, 12, 60, 48, 48], [2960, 12, 59, 48, 48], [2980, 12, 60, 48, 48], [3000, 12, 61, 48, 48], [3020, 12, 61, 48, 48], [3040, 12, 61, 48, 48], [3060, 12, 62, 48, 48], [3080, 12, 61, 48, 48], [3100, 12, 62, 48, 48], [3120, 12, 63, 48, 48], [3140, 12, 63, 48, 48], [3160, 12, 63, 48, 48], [3180, 12, 63, 48, 48], [3200, 12, 62, 48, 48], [3220, 12, 63, 48, 48], [3240, 12, 64, 48, 48], [3260, 12, 63, 48, 48], [3280, 12, 64, 48, 48], [3300, 12, 65, 48, 48], [3320, 12, 68, 48, 48], [3340, 12, 71, 48, 48], [3360, 12, 64, 48, 48], [3380, 12, 68, 48, 48], [3400, 12, 71, 48, 48], [3420, 12, 63, 48, 48], [3440, 12, 68, 48, 48], [3460, 12, 71, 48, 48], [3480, 12, 62, 48, 48], [3500, 12, 68, 48, 48], [3520, 12, 71, 48, 48], [3540, 12, 66, 48, 48], [3560, 12, 69, 48, 48], [3580, 12, 72, 48, 48], [3600, 12, 65, 48, 48], [3620, 12, 69, 48, 48], [3640, 12, 72, 48, 48], [3660, 12, 64, 48, 48], [3680, 12, 69, 48, 48], [3700, 12, 72, 48, 48], [3720, 12, 68, 48, 48], [3740, 12, 67, 48, 48], [3760, 12, 68, 48, 48], [3780, 12, 64, 48, 48], [3800, 12, 63, 48, 48], [3820, 12, 64, 48, 48], [3900, 12, 63, 48, 48], [3920, 12, 62, 48, 48], [3940, 12, 63, 48, 48]],
                    120, 68, [22], False),
                _score_track('strings', '大提琴', 'Cellos',
                    [[300, 12, 63, 48, 48], [320, 12, 62, 48, 48], [340, 12, 63, 48, 48], [360, 12, 64, 48, 48], [380, 12, 63, 48, 48], [400, 12, 61, 48, 48], [420, 12, 59, 48, 48], [440, 12, 58, 48, 48], [460, 12, 56, 48, 48], [480, 12, 55, 48, 48], [500, 12, 56, 48, 48], [520, 12, 58, 48, 48], [540, 12, 59, 48, 48], [560, 12, 58, 48, 48], [580, 12, 56, 48, 48], [600, 12, 54, 48, 48], [620, 12, 52, 48, 48], [640, 12, 51, 48, 48], [660, 12, 56, 48, 48], [680, 12, 58, 48, 48], [700, 12, 59, 48, 48], [720, 12, 61, 48, 48], [740, 12, 63, 48, 48], [760, 12, 64, 48, 48], [780, 12, 63, 48, 48], [800, 12, 61, 48, 48], [820, 12, 59, 48, 48], [840, 12, 58, 48, 48], [860, 12, 59, 48, 48], [880, 12, 61, 48, 48], [900, 20, 59, 48, 48], [1560, 12, 58, 48, 48], [1580, 12, 57, 48, 48], [1600, 12, 56, 48, 48], [1620, 12, 51, 47, 48], [1620, 12, 55, 48, 48], [1640, 12, 51, 47, 48], [1640, 12, 53, 48, 48], [1660, 12, 51, 47, 48], [1660, 12, 55, 48, 48], [1680, 12, 51, 48, 48], [1700, 12, 51, 47, 48], [1700, 12, 53, 48, 48], [1720, 12, 51, 47, 48], [1720, 12, 55, 48, 48], [1740, 12, 51, 47, 48], [1740, 12, 58, 48, 48], [1760, 12, 51, 47, 48], [1760, 12, 56, 48, 48], [1780, 12, 51, 47, 48], [1780, 12, 55, 48, 48], [1800, 12, 51, 47, 48], [1800, 12, 56, 48, 48], [1820, 12, 51, 47, 48], [1820, 12, 55, 48, 48], [1840, 12, 51, 47, 48], [1840, 12, 56, 48, 48], [1860, 12, 51, 47, 48], [1860, 12, 59, 48, 48], [1880, 12, 51, 47, 48], [1880, 12, 58, 48, 48], [1900, 12, 51, 47, 48], [1900, 12, 59, 48, 48], [1920, 12, 51, 47, 48], [1920, 12, 62, 48, 48], [1940, 12, 51, 47, 48], [1940, 12, 61, 48, 48], [1960, 12, 51, 47, 48], [1960, 12, 62, 48, 48], [1980, 12, 51, 47, 48], [1980, 12, 56, 48, 48], [2000, 12, 51, 47, 48], [2000, 12, 58, 48, 48], [2020, 12, 51, 47, 48], [2020, 12, 59, 48, 48], [2040, 12, 51, 47, 48], [2040, 12, 58, 48, 48], [2060, 12, 51, 47, 48], [2060, 12, 56, 48, 48], [2080, 12, 51, 47, 48], [2080, 12, 54, 48, 48], [2100, 12, 51, 47, 48], [2100, 12, 52, 48, 48], [2120, 12, 51, 48, 48], [2140, 12, 49, 47, 48], [2140, 12, 51, 48, 48], [2160, 12, 51, 47, 48], [2160, 12, 54, 48, 48], [2180, 12, 51, 47, 48], [2180, 12, 57, 48, 48], [2200, 12, 51, 47, 48], [2200, 12, 61, 48, 48], [2220, 12, 51, 47, 48], [2220, 12, 64, 48, 48], [2240, 12, 51, 47, 48], [2240, 12, 66, 48, 48], [2260, 12, 51, 47, 48], [2260, 12, 67, 48, 48], [2280, 12, 51, 47, 48], [2280, 12, 66, 48, 48], [2300, 12, 51, 47, 48], [2300, 12, 64, 48, 48], [2320, 12, 51, 47, 48], [2320, 12, 63, 48, 48], [2340, 12, 51, 47, 48], [2340, 12, 61, 48, 48], [2360, 12, 51, 47, 48], [2360, 12, 61, 48, 48], [2380, 12, 51, 47, 48], [2380, 12, 61, 48, 48], [2400, 12, 51, 47, 48], [2400, 12, 56, 48, 48], [2420, 12, 51, 47, 48], [2420, 12, 56, 48, 48], [2440, 12, 51, 47, 48], [2440, 12, 56, 48, 48], [2460, 12, 51, 47, 48], [2460, 12, 52, 48, 48], [2480, 12, 51, 47, 48], [2480, 12, 52, 48, 48], [2500, 12, 51, 47, 48], [2500, 12, 52, 48, 48], [2520, 12, 51, 47, 48], [2520, 12, 59, 48, 48], [2540, 12, 51, 47, 48], [2540, 12, 59, 48, 48], [2560, 12, 51, 47, 48], [2560, 12, 59, 48, 48], [2580, 12, 51, 47, 48], [2580, 12, 56, 48, 48], [2600, 12, 51, 47, 48], [2600, 12, 56, 48, 48], [2620, 12, 51, 47, 48], [2620, 12, 56, 48, 48], [2640, 12, 51, 47, 48], [2640, 12, 52, 48, 48], [2660, 12, 51, 47, 48], [2660, 12, 52, 48, 48], [2680, 12, 51, 47, 48], [2680, 12, 52, 48, 48], [2700, 12, 51, 47, 48], [2700, 12, 59, 48, 48], [2720, 12, 51, 47, 48], [2720, 12, 59, 48, 48], [2740, 12, 51, 47, 48], [2740, 12, 59, 48, 48], [2760, 12, 51, 47, 48], [2760, 12, 54, 48, 48], [2780, 12, 51, 47, 48], [2780, 12, 54, 48, 48], [2800, 12, 51, 47, 48], [2800, 12, 54, 48, 48], [2820, 12, 51, 47, 48], [2840, 12, 51, 47, 48], [2860, 12, 51, 47, 48], [2880, 12, 51, 47, 48], [2880, 12, 57, 48, 48], [2900, 12, 51, 47, 48], [2900, 12, 54, 48, 48], [2920, 12, 51, 47, 48], [2920, 12, 52, 48, 48], [2940, 12, 51, 47, 48], [2960, 12, 51, 47, 48], [2960, 12, 54, 48, 48], [2980, 12, 51, 47, 48], [2980, 12, 57, 48, 48], [3000, 12, 51, 47, 48], [3000, 12, 59, 48, 48], [3020, 12, 51, 47, 48], [3020, 12, 56, 48, 48], [3040, 12, 51, 47, 48], [3040, 12, 54, 48, 48], [3060, 12, 51, 47, 48], [3060, 12, 53, 48, 48], [3080, 12, 51, 47, 48], [3080, 12, 56, 48, 48], [3100, 12, 51, 47, 48], [3100, 12, 58, 48, 48], [3120, 12, 51, 47, 48], [3120, 12, 59, 48, 48], [3140, 12, 51, 47, 48], [3140, 12, 54, 48, 48], [3160, 12, 51, 47, 48], [3160, 12, 52, 48, 48], [3180, 12, 51, 47, 48], [3180, 12, 54, 48, 48], [3200, 12, 51, 47, 48], [3200, 12, 57, 48, 48], [3220, 12, 51, 47, 48], [3220, 12, 60, 48, 48], [3240, 12, 51, 47, 48], [3240, 12, 61, 48, 48], [3260, 12, 51, 47, 48], [3260, 12, 56, 48, 48], [3280, 12, 51, 47, 48], [3280, 12, 52, 48, 48], [3300, 12, 51, 47, 48], [3300, 12, 56, 48, 48], [3320, 12, 51, 47, 48], [3320, 12, 55, 48, 48], [3340, 12, 51, 47, 48], [3340, 12, 56, 48, 48], [3360, 12, 51, 47, 48], [3360, 12, 55, 48, 48], [3380, 12, 51, 47, 48], [3380, 12, 54, 48, 48], [3400, 12, 51, 47, 48], [3400, 12, 55, 48, 48], [3420, 12, 51, 47, 48], [3420, 12, 54, 48, 48], [3440, 12, 51, 47, 48], [3440, 12, 53, 48, 48], [3460, 12, 51, 47, 48], [3460, 12, 54, 48, 48], [3480, 12, 51, 47, 48], [3480, 12, 53, 48, 48], [3500, 12, 51, 47, 48], [3500, 12, 52, 48, 48], [3520, 12, 51, 47, 48], [3520, 12, 53, 48, 48], [3540, 12, 51, 47, 48], [3540, 12, 58, 48, 48], [3560, 12, 51, 47, 48], [3560, 12, 57, 48, 48], [3580, 12, 51, 47, 48], [3580, 12, 58, 48, 48], [3600, 12, 51, 47, 48], [3600, 12, 57, 48, 48], [3620, 12, 51, 47, 48], [3620, 12, 56, 48, 48], [3640, 12, 51, 47, 48], [3640, 12, 57, 48, 48], [3660, 12, 51, 47, 48], [3660, 12, 56, 48, 48], [3680, 12, 51, 47, 48], [3680, 12, 55, 48, 48], [3700, 12, 51, 47, 48], [3700, 12, 56, 48, 48], [3720, 12, 51, 47, 48], [3720, 12, 59, 48, 48], [3740, 12, 51, 47, 48], [3740, 12, 58, 48, 48], [3760, 12, 51, 47, 48], [3760, 12, 59, 48, 48], [3780, 12, 51, 47, 48], [3780, 12, 58, 48, 48], [3800, 12, 51, 47, 48], [3800, 12, 57, 48, 48], [3820, 12, 51, 47, 48], [3820, 12, 58, 48, 48], [3840, 12, 51, 47, 48], [3840, 12, 57, 48, 48], [3860, 12, 51, 47, 48], [3860, 12, 56, 48, 48], [3880, 12, 51, 47, 48], [3880, 12, 57, 48, 48], [3900, 12, 51, 47, 48], [3900, 12, 55, 48, 48], [3920, 12, 51, 47, 48], [3920, 12, 54, 48, 48], [3940, 12, 51, 47, 48], [3940, 12, 55, 48, 48], [3960, 12, 51, 47, 48], [3960, 12, 54, 48, 48], [3980, 12, 51, 47, 48], [3980, 12, 53, 48, 48], [4000, 12, 51, 47, 48], [4000, 12, 54, 48, 48], [4020, 12, 51, 47, 48], [4020, 12, 55, 48, 48], [4040, 12, 51, 47, 48], [4040, 12, 54, 48, 48], [4060, 12, 51, 47, 48], [4060, 12, 55, 48, 48], [4080, 12, 51, 47, 48], [4080, 12, 56, 48, 48], [4100, 12, 51, 47, 48], [4100, 12, 55, 48, 48], [4120, 12, 51, 47, 48], [4120, 12, 56, 48, 48], [4140, 12, 51, 47, 48], [4140, 12, 55, 48, 48], [4160, 12, 51, 47, 48], [4160, 12, 54, 48, 48], [4180, 12, 51, 47, 48], [4180, 12, 55, 48, 48], [4200, 12, 51, 47, 48], [4200, 12, 56, 48, 48], [4220, 12, 51, 47, 48], [4220, 12, 55, 48, 48], [4240, 12, 51, 47, 48], [4240, 12, 56, 48, 48], [4260, 12, 51, 47, 48], [4260, 12, 57, 48, 48], [4280, 12, 51, 47, 48], [4280, 12, 56, 48, 48], [4300, 12, 51, 47, 48], [4300, 12, 57, 48, 48], [4320, 12, 51, 47, 48], [4320, 12, 56, 48, 48], [4340, 12, 51, 47, 48], [4340, 12, 55, 48, 48], [4360, 12, 51, 47, 48], [4360, 12, 56, 48, 48], [4380, 12, 51, 47, 48], [4380, 12, 57, 48, 48], [4400, 12, 51, 47, 48], [4400, 12, 56, 48, 48], [4420, 12, 51, 47, 48], [4420, 12, 57, 48, 48], [4440, 12, 51, 47, 48], [4440, 12, 58, 48, 48], [4460, 12, 51, 47, 48], [4460, 12, 57, 48, 48], [4480, 12, 51, 47, 48], [4480, 12, 58, 48, 48]],
                    120, 68, [24], False),
                _score_track('winds', '单簧管', 'Clarinet',
                    [[1260, 60, 83, 54, 71], [1320, 30, 87, 54, 71], [1350, 30, 86, 54, 71], [1380, 30, 87, 54, 71], [1410, 30, 83, 54, 71], [1440, 30, 82, 54, 71], [1470, 30, 87, 54, 71], [1500, 96, 75, 54, 71]],
                    120, 68, [6], False),
                _score_track('horns', '第一圆号组', 'Horns I',
                    [[0, 20, 63, 52, 60], [30, 20, 63, 48, 60], [60, 20, 63, 48, 60], [90, 20, 63, 48, 60], [120, 20, 63, 48, 60], [150, 20, 63, 48, 60], [180, 20, 63, 48, 60], [210, 20, 63, 48, 60], [240, 20, 63, 48, 60], [270, 20, 63, 48, 60], [300, 20, 63, 48, 60], [330, 20, 63, 48, 60], [360, 20, 63, 48, 60], [390, 20, 63, 48, 60], [420, 20, 63, 48, 60], [450, 20, 63, 48, 60], [480, 20, 63, 48, 60], [510, 20, 63, 48, 60], [540, 20, 63, 48, 60], [570, 20, 63, 48, 60], [600, 20, 63, 48, 60], [630, 20, 63, 48, 60], [660, 20, 63, 48, 60], [690, 20, 63, 48, 60], [720, 20, 63, 48, 60], [750, 20, 63, 48, 60], [780, 20, 63, 48, 60], [810, 20, 63, 48, 60], [840, 20, 63, 48, 60], [870, 20, 63, 48, 60], [900, 20, 63, 48, 60], [930, 20, 63, 48, 60], [960, 20, 63, 48, 60], [990, 20, 63, 48, 60], [1020, 20, 63, 48, 60], [1050, 20, 63, 48, 60], [1080, 20, 63, 48, 60], [1110, 20, 63, 48, 60], [1140, 20, 63, 48, 60], [1170, 20, 63, 48, 60], [1200, 20, 63, 48, 60], [1230, 20, 63, 48, 60], [1260, 20, 63, 48, 60], [1290, 20, 63, 48, 60], [1320, 20, 63, 48, 60], [1350, 20, 63, 48, 60], [1380, 20, 63, 48, 60], [1410, 20, 63, 48, 60], [1440, 20, 63, 48, 60], [1470, 20, 63, 48, 60], [1500, 20, 63, 48, 60], [1530, 20, 63, 48, 60], [1560, 20, 63, 48, 60], [1590, 20, 63, 48, 60]],
                    120, 68, [11], False),
            ], '6657af3fca1c9d129566d4f149ee99db8f1dad25790d33a30085618dc962c612', 'https://gustavmahler.com/site/midi/symphony2/2nd-movement-Andante-moderato.midi'),
        _score_scene(2, 3, '晚段舞曲：长笛、单簧管与弦乐', 'Late dance: flute, clarinet and strings',
            '长笛与单簧管的流动线条并不齐奏，大提琴与小提琴的断奏及长音均保留源数据中的进入次序。',
            'Flute and clarinet flow independently; violin and cello retain the source ordering of detached notes and sustained tones.',
            70, 354, 393, 236, 261, 120, [3, 8], [
                _score_track('strings', '第一小提琴', 'Violins I',
                    [[360, 23, 62, 56, 45], [390, 23, 68, 56, 45], [420, 47, 68, 56, 45], [480, 47, 68, 56, 45], [540, 23, 67, 56, 45], [570, 23, 70, 56, 45], [600, 47, 70, 56, 45], [660, 47, 70, 56, 45], [720, 47, 68, 56, 45], [720, 47, 72, 56, 45], [780, 47, 68, 56, 45], [780, 47, 72, 56, 45], [840, 47, 68, 56, 45], [840, 47, 72, 56, 45], [900, 23, 67, 56, 45], [900, 23, 70, 56, 45], [930, 23, 65, 56, 45], [930, 23, 68, 56, 45], [960, 23, 63, 56, 45], [960, 23, 67, 56, 45], [990, 23, 62, 56, 45], [990, 23, 65, 56, 45], [1020, 47, 60, 56, 45], [1020, 47, 63, 56, 45], [1140, 23, 74, 56, 45], [1170, 23, 72, 56, 45], [1200, 23, 70, 56, 45], [1230, 23, 68, 56, 45], [1260, 23, 67, 56, 45], [1290, 23, 66, 56, 45], [1320, 23, 65, 56, 45], [1350, 23, 63, 56, 45], [1740, 60, 63, 56, 48], [1740, 60, 75, 56, 48], [1800, 180, 72, 56, 48], [1800, 180, 84, 56, 48], [1980, 30, 77, 56, 48], [1980, 30, 89, 56, 48], [2010, 30, 75, 56, 48], [2010, 30, 87, 56, 48], [2040, 30, 74, 56, 48], [2040, 30, 86, 56, 48], [2070, 30, 75, 56, 48], [2070, 30, 87, 56, 48], [2100, 30, 72, 56, 48], [2100, 30, 84, 56, 48], [2130, 23, 68, 56, 48], [2130, 23, 80, 56, 48], [2160, 120, 63, 56, 48], [2160, 120, 75, 56, 48], [2280, 60, 65, 56, 48], [2280, 60, 77, 56, 48], [2340, 96, 63, 56, 48], [2340, 96, 75, 56, 48], [2460, 60, 63, 56, 48], [2460, 60, 75, 56, 48], [2520, 120, 72, 56, 48], [2520, 120, 84, 56, 48], [2640, 30, 70, 56, 48], [2640, 30, 82, 56, 48], [2670, 30, 68, 56, 48], [2670, 23, 80, 56, 48], [2700, 23, 67, 56, 48], [2700, 23, 79, 56, 48], [2730, 23, 68, 56, 48], [2730, 23, 80, 56, 48], [2760, 23, 70, 56, 48], [2760, 23, 82, 56, 48], [2790, 23, 72, 56, 48], [2790, 23, 84, 56, 48], [2820, 23, 74, 56, 48], [2820, 23, 86, 56, 48], [2850, 23, 75, 56, 48], [2850, 23, 87, 56, 48], [2880, 5, 86, 52, 48], [2885, 5, 87, 52, 48], [2890, 5, 86, 52, 48], [2895, 5, 87, 52, 48], [2900, 5, 86, 52, 48], [2905, 5, 87, 52, 48], [2910, 10, 86, 52, 48], [2915, 5, 87, 52, 48], [2920, 5, 86, 52, 48], [2925, 5, 87, 52, 48], [2930, 5, 86, 52, 48], [2935, 5, 87, 52, 48], [2940, 10, 86, 52, 48], [2945, 5, 87, 52, 48], [2950, 5, 86, 52, 48], [2955, 5, 87, 52, 48], [2960, 5, 86, 52, 48], [2965, 5, 87, 52, 48], [2970, 10, 86, 52, 48], [2975, 5, 87, 52, 48], [2980, 5, 86, 52, 48], [2985, 5, 87, 52, 48], [2990, 5, 86, 52, 48], [2995, 5, 87, 52, 48], [3000, 10, 86, 52, 48], [3005, 5, 87, 52, 48], [3010, 5, 86, 52, 48], [3015, 5, 87, 52, 48], [3020, 5, 86, 52, 48], [3025, 5, 87, 52, 48], [3030, 10, 86, 52, 48], [3035, 5, 87, 52, 48], [3040, 5, 86, 52, 48], [3045, 7, 84, 52, 48], [3045, 5, 87, 52, 48], [3052, 7, 86, 52, 48], [3060, 90, 77, 56, 48], [3060, 90, 89, 56, 48], [3150, 23, 75, 56, 48], [3150, 23, 87, 56, 48], [3180, 23, 74, 56, 48], [3180, 23, 86, 56, 48], [3210, 23, 73, 56, 48], [3210, 23, 85, 56, 48], [3240, 120, 72, 56, 48], [3240, 120, 84, 56, 48], [3360, 30, 71, 56, 48], [3360, 30, 83, 56, 48], [3390, 30, 72, 56, 48], [3390, 30, 84, 56, 48], [3420, 30, 73, 56, 48], [3420, 30, 85, 56, 48], [3450, 30, 72, 56, 48], [3450, 30, 84, 56, 48], [3480, 30, 71, 56, 48], [3480, 30, 83, 56, 48], [3510, 30, 72, 56, 48], [3510, 30, 84, 56, 48], [3540, 30, 73, 56, 48], [3540, 30, 85, 56, 48], [3570, 23, 72, 56, 48], [3570, 23, 84, 56, 48], [3600, 90, 77, 56, 48], [3600, 90, 89, 56, 48], [3690, 30, 76, 56, 48], [3690, 30, 88, 56, 48], [3720, 30, 77, 56, 48], [3720, 30, 89, 56, 48], [3750, 30, 79, 56, 48], [3750, 30, 91, 56, 48], [3780, 120, 72, 56, 48], [3780, 120, 84, 56, 48], [3900, 47, 71, 56, 48], [3900, 47, 83, 56, 48], [3960, 90, 70, 56, 48], [3960, 90, 82, 56, 48], [4050, 30, 71, 56, 48], [4050, 30, 83, 56, 48], [4080, 23, 70, 56, 48], [4080, 23, 82, 56, 48], [4110, 23, 72, 56, 48], [4110, 23, 84, 56, 48], [4140, 60, 70, 56, 48], [4140, 60, 82, 56, 48], [4200, 30, 67, 56, 48], [4200, 30, 79, 56, 48], [4230, 30, 70, 56, 48], [4230, 30, 82, 56, 48], [4260, 30, 77, 56, 48], [4260, 30, 89, 56, 48], [4290, 23, 75, 56, 48], [4290, 23, 87, 56, 48], [4320, 60, 74, 56, 48], [4320, 60, 86, 56, 48], [4380, 30, 70, 56, 48], [4380, 30, 82, 56, 48], [4410, 30, 74, 56, 48], [4410, 30, 86, 56, 48], [4440, 30, 79, 56, 48], [4440, 30, 91, 56, 48], [4470, 23, 77, 56, 48], [4470, 23, 89, 56, 48], [4500, 30, 77, 56, 48], [4500, 30, 89, 56, 48], [4530, 23, 75, 56, 48], [4530, 23, 87, 56, 48], [4560, 23, 74, 56, 48], [4560, 23, 86, 56, 48], [4590, 23, 75, 56, 48], [4590, 23, 87, 56, 48], [4620, 30, 77, 56, 48], [4620, 30, 89, 56, 48], [4650, 23, 73, 56, 48], [4650, 23, 85, 56, 48]],
                    120, 70, [21], False),
                _score_track('strings', '大提琴', 'Cellos',
                    [[0, 47, 50, 56, 45], [0, 47, 53, 56, 45], [60, 47, 46, 56, 45], [60, 23, 50, 56, 45], [90, 23, 51, 56, 45], [120, 47, 50, 56, 45], [120, 23, 53, 56, 45], [150, 23, 55, 56, 45], [180, 47, 51, 56, 45], [240, 47, 46, 56, 45], [240, 47, 63, 56, 45], [300, 47, 51, 56, 45], [360, 47, 53, 56, 45], [360, 47, 58, 56, 45], [420, 47, 46, 56, 45], [480, 47, 58, 56, 45], [540, 47, 51, 56, 45], [540, 47, 58, 56, 45], [600, 47, 51, 56, 45], [600, 47, 55, 56, 45], [660, 47, 51, 56, 45], [660, 47, 58, 56, 45], [720, 23, 48, 56, 45], [720, 23, 56, 56, 45], [750, 23, 51, 56, 45], [750, 23, 58, 56, 45], [780, 23, 56, 56, 45], [780, 23, 60, 56, 45], [810, 23, 58, 56, 45], [810, 23, 62, 56, 45], [840, 23, 60, 56, 45], [840, 23, 63, 56, 45], [870, 23, 62, 56, 45], [870, 23, 65, 56, 45], [900, 47, 63, 56, 45], [900, 47, 67, 56, 45], [960, 47, 55, 56, 45], [960, 47, 58, 56, 45], [1020, 23, 63, 56, 45], [1020, 23, 67, 56, 45], [1050, 23, 62, 56, 45], [1050, 23, 65, 56, 45], [1080, 23, 60, 56, 45], [1080, 23, 63, 56, 45], [1110, 23, 58, 56, 45], [1110, 23, 62, 56, 45], [1140, 47, 56, 56, 45], [1140, 47, 60, 56, 45], [1200, 47, 46, 56, 45], [1200, 47, 56, 56, 45], [1260, 23, 58, 56, 45], [1290, 23, 57, 56, 45], [1320, 23, 56, 56, 45], [1350, 23, 55, 56, 45], [1590, 23, 51, 79, 45], [1620, 23, 50, 79, 45], [1650, 23, 49, 79, 45], [1680, 23, 48, 79, 45], [1710, 23, 47, 79, 45], [1740, 23, 46, 79, 45], [1770, 23, 39, 79, 45], [1800, 47, 44, 79, 45], [1980, 47, 44, 56, 45], [2040, 47, 51, 56, 45], [2100, 47, 39, 56, 45], [2100, 47, 51, 56, 45], [2160, 47, 44, 56, 45], [2160, 47, 56, 56, 45], [2340, 47, 44, 56, 45], [2400, 47, 51, 56, 45], [2460, 47, 39, 56, 45], [2520, 47, 44, 56, 45], [2580, 47, 48, 56, 45], [2640, 47, 44, 56, 45], [2700, 47, 46, 56, 45], [2880, 47, 53, 56, 45], [2940, 47, 46, 56, 45], [3000, 47, 58, 56, 45], [3060, 47, 51, 56, 45], [3180, 38, 51, 52, 45], [3240, 60, 44, 52, 48], [3240, 60, 51, 52, 48], [3300, 20, 44, 52, 48], [3300, 20, 51, 52, 48], [3330, 20, 44, 52, 48], [3330, 20, 51, 52, 48], [3360, 20, 44, 52, 48], [3360, 20, 51, 52, 48], [3390, 20, 44, 52, 48], [3390, 20, 51, 52, 48], [3420, 20, 44, 52, 48], [3420, 20, 51, 52, 48], [3450, 20, 44, 52, 48], [3450, 20, 51, 52, 48], [3480, 38, 44, 52, 48], [3480, 38, 51, 52, 48], [3540, 60, 36, 52, 48], [3540, 60, 48, 52, 48], [3600, 47, 41, 52, 48], [3600, 47, 48, 52, 48], [3660, 20, 41, 52, 48], [3660, 20, 48, 52, 48], [3690, 20, 41, 52, 48], [3690, 20, 48, 52, 48], [3720, 20, 41, 52, 48], [3720, 20, 48, 52, 48], [3750, 20, 41, 52, 48], [3750, 20, 48, 52, 48], [3780, 20, 41, 52, 48], [3780, 20, 48, 52, 48], [3810, 20, 41, 52, 48], [3810, 20, 48, 52, 48], [3840, 38, 41, 52, 48], [3840, 38, 48, 52, 48], [3900, 38, 44, 52, 48], [3900, 60, 55, 52, 48], [3960, 30, 53, 52, 48], [3990, 23, 58, 52, 48], [4020, 3, 58, 52, 48], [4023, 3, 60, 52, 48], [4027, 52, 58, 52, 48], [4080, 26, 53, 52, 48], [4110, 23, 58, 52, 48], [4140, 30, 55, 52, 48], [4170, 23, 63, 52, 48], [4200, 3, 63, 52, 48], [4203, 3, 65, 52, 48], [4207, 52, 63, 52, 48], [4260, 26, 58, 52, 48], [4290, 23, 55, 52, 48], [4320, 30, 56, 52, 48], [4350, 23, 68, 52, 48], [4380, 30, 68, 52, 48], [4410, 30, 65, 52, 48], [4440, 30, 62, 52, 48], [4470, 23, 65, 52, 48], [4500, 3, 63, 52, 48], [4503, 3, 65, 52, 48], [4507, 22, 63, 52, 48], [4530, 30, 62, 52, 48], [4560, 30, 63, 52, 48], [4590, 30, 67, 52, 48], [4620, 30, 68, 52, 48], [4650, 23, 65, 52, 48]],
                    120, 70, [24], False),
                _score_track('winds', '长笛', 'Flute',
                    [[1740, 20, 63, 56, 73], [1800, 60, 63, 56, 73], [1860, 20, 60, 56, 73], [1890, 20, 61, 56, 73], [1920, 20, 63, 56, 73], [1950, 20, 65, 56, 73], [1980, 60, 60, 56, 73], [1980, 60, 63, 56, 73], [2040, 23, 63, 56, 73], [2040, 23, 68, 56, 73], [2100, 23, 63, 56, 73], [2100, 23, 68, 56, 73], [2160, 60, 63, 56, 73], [2160, 60, 68, 56, 73], [2220, 20, 60, 56, 73], [2220, 20, 63, 56, 73], [2250, 20, 63, 56, 73], [2250, 20, 67, 56, 73], [2280, 20, 63, 56, 73], [2280, 20, 68, 56, 73], [2310, 20, 67, 56, 73], [2310, 20, 70, 56, 73], [2340, 60, 63, 56, 73], [2340, 60, 68, 56, 73], [2400, 23, 68, 56, 73], [2400, 23, 72, 56, 73], [2460, 23, 68, 56, 73], [2460, 23, 72, 56, 73], [2520, 30, 68, 56, 73], [2520, 30, 72, 56, 73], [2550, 20, 72, 56, 73], [2550, 20, 75, 56, 73], [2580, 3, 72, 56, 73], [2580, 3, 75, 56, 73], [2583, 3, 73, 56, 73], [2583, 3, 77, 56, 73], [2587, 52, 72, 56, 73], [2587, 52, 75, 56, 73], [2640, 20, 70, 56, 73], [2640, 20, 73, 56, 73], [2670, 20, 68, 56, 73], [2670, 20, 72, 56, 73], [2700, 60, 70, 56, 73], [2700, 52, 75, 56, 73], [2760, 23, 67, 56, 73], [2760, 23, 70, 56, 73], [2820, 23, 67, 56, 73], [2820, 23, 70, 56, 73], [2880, 30, 62, 56, 73], [2880, 30, 68, 56, 73], [2910, 20, 68, 56, 73], [2910, 20, 72, 56, 73], [2940, 3, 68, 56, 73], [2940, 3, 72, 56, 73], [2943, 3, 70, 56, 73], [2943, 3, 74, 56, 73], [2947, 52, 68, 56, 73], [2947, 52, 72, 56, 73], [3000, 20, 67, 56, 73], [3000, 20, 70, 56, 73], [3030, 20, 65, 56, 73], [3030, 20, 68, 56, 73], [3060, 60, 67, 56, 73], [3060, 60, 75, 56, 73], [3120, 23, 63, 56, 73], [3180, 23, 63, 56, 73], [3900, 52, 67, 52, 73], [3960, 26, 65, 52, 73], [3990, 23, 70, 52, 73], [4020, 52, 70, 52, 73], [4080, 26, 65, 52, 73], [4110, 23, 70, 52, 73], [4140, 30, 67, 52, 73], [4170, 23, 75, 52, 73], [4200, 60, 75, 52, 73], [4260, 30, 70, 52, 73], [4290, 23, 67, 52, 73], [4320, 30, 68, 52, 73], [4350, 23, 80, 52, 73], [4380, 30, 80, 52, 73], [4410, 30, 77, 52, 73], [4440, 30, 74, 52, 73], [4470, 30, 77, 52, 73], [4500, 120, 75, 52, 73], [4620, 47, 70, 56, 73], [4620, 47, 73, 56, 73]],
                    120, 70, [2], False),
                _score_track('winds', '单簧管', 'Clarinet',
                    [[1740, 20, 51, 56, 71], [1740, 20, 63, 56, 71], [1800, 60, 60, 56, 71], [1800, 60, 63, 56, 71], [1860, 20, 56, 56, 71], [1860, 20, 60, 56, 71], [1890, 20, 56, 56, 71], [1890, 20, 58, 56, 71], [1890, 20, 61, 56, 71], [1920, 20, 56, 56, 71], [1920, 20, 60, 56, 71], [1920, 20, 63, 56, 71], [1950, 20, 56, 56, 71], [1950, 20, 61, 56, 71], [1950, 20, 65, 56, 71], [1980, 60, 56, 56, 71], [1980, 60, 60, 56, 71], [1980, 60, 63, 56, 71], [2040, 23, 60, 56, 71], [2040, 23, 63, 56, 71], [2040, 23, 68, 56, 71], [2100, 23, 60, 56, 71], [2100, 23, 63, 56, 71], [2100, 23, 68, 56, 71], [2160, 60, 60, 56, 71], [2160, 60, 63, 56, 71], [2160, 60, 68, 56, 71], [2220, 20, 56, 56, 71], [2220, 20, 60, 56, 71], [2220, 20, 63, 56, 71], [2250, 20, 58, 56, 71], [2250, 20, 63, 56, 71], [2250, 20, 67, 56, 71], [2280, 20, 60, 56, 71], [2280, 20, 63, 56, 71], [2280, 20, 68, 56, 71], [2310, 20, 63, 56, 71], [2310, 20, 67, 56, 71], [2310, 20, 70, 56, 71], [2340, 60, 60, 56, 71], [2340, 60, 63, 56, 71], [2340, 60, 68, 56, 71], [2400, 23, 63, 56, 71], [2400, 23, 68, 56, 71], [2400, 23, 72, 56, 71], [2460, 23, 63, 56, 71], [2460, 23, 68, 56, 71], [2460, 23, 72, 56, 71], [2520, 30, 68, 56, 71], [2520, 30, 72, 56, 71], [2550, 20, 72, 56, 71], [2550, 20, 75, 56, 71], [2580, 3, 72, 56, 71], [2580, 3, 75, 56, 71], [2583, 3, 73, 56, 71], [2583, 3, 77, 56, 71], [2587, 52, 72, 56, 71], [2587, 52, 75, 56, 71], [2640, 20, 70, 56, 71], [2640, 20, 73, 56, 71], [2670, 20, 68, 56, 71], [2670, 20, 72, 56, 71], [2700, 60, 70, 56, 71], [2700, 60, 75, 56, 71], [2760, 23, 67, 56, 71], [2760, 23, 70, 56, 71], [2820, 23, 67, 56, 71], [2820, 23, 70, 56, 71], [2880, 30, 62, 56, 71], [2880, 30, 68, 56, 71], [2910, 20, 68, 56, 71], [2910, 20, 72, 56, 71], [2940, 3, 68, 56, 71], [2940, 3, 72, 56, 71], [2943, 3, 70, 56, 71], [2943, 3, 74, 56, 71], [2947, 52, 68, 56, 71], [2947, 52, 72, 56, 71], [3000, 20, 67, 56, 71], [3000, 20, 70, 56, 71], [3030, 20, 65, 56, 71], [3030, 20, 68, 56, 71], [3060, 60, 67, 56, 71], [3060, 60, 75, 56, 71], [3120, 23, 63, 56, 71], [3180, 23, 63, 56, 71], [3240, 60, 60, 52, 71], [3240, 60, 63, 52, 71], [3300, 20, 56, 52, 71], [3300, 20, 60, 52, 71], [3330, 20, 56, 52, 71], [3330, 20, 58, 52, 71], [3330, 20, 61, 52, 71], [3360, 20, 56, 52, 71], [3360, 20, 60, 52, 71], [3360, 20, 63, 52, 71], [3390, 20, 56, 52, 71], [3390, 20, 61, 52, 71], [3390, 20, 65, 52, 71], [3420, 20, 56, 52, 71], [3420, 20, 60, 52, 71], [3420, 20, 63, 52, 71], [3450, 20, 56, 52, 71], [3450, 20, 58, 52, 71], [3450, 20, 61, 52, 71], [3480, 38, 56, 52, 71], [3480, 38, 60, 52, 71], [3540, 60, 55, 52, 71], [3540, 60, 58, 52, 71], [3600, 60, 56, 52, 71], [3600, 60, 60, 52, 71], [3660, 20, 53, 52, 71], [3660, 20, 56, 52, 71], [3690, 20, 53, 52, 71], [3690, 20, 55, 52, 71], [3690, 20, 58, 52, 71], [3720, 20, 53, 52, 71], [3720, 20, 56, 52, 71], [3720, 20, 60, 52, 71], [3750, 20, 53, 52, 71], [3750, 20, 58, 52, 71], [3750, 20, 61, 52, 71], [3780, 20, 53, 52, 71], [3780, 20, 56, 52, 71], [3780, 20, 60, 52, 71], [3810, 20, 53, 52, 71], [3810, 20, 55, 52, 71], [3810, 20, 58, 52, 71], [3840, 38, 53, 52, 71], [3840, 38, 56, 52, 71], [3900, 38, 51, 52, 71], [3900, 38, 55, 52, 71], [4500, 120, 75, 56, 71], [4620, 60, 73, 56, 71]],
                    120, 70, [6], False),
                _score_track('horns', '第一圆号组', 'Horns I',
                    [[2520, 23, 63, 56, 60], [2580, 23, 63, 56, 60], [2640, 23, 63, 56, 60], [2700, 143, 63, 56, 60], [2880, 23, 62, 56, 60], [2940, 23, 62, 56, 60], [3000, 23, 62, 56, 60], [3060, 227, 63, 56, 60], [4140, 540, 70, 56, 60], [4620, 47, 68, 56, 60]],
                    120, 70, [11], False),
            ], '6657af3fca1c9d129566d4f149ee99db8f1dad25790d33a30085618dc962c612', 'https://gustavmahler.com/site/midi/symphony2/2nd-movement-Andante-moderato.midi'),
    ],
    "3": [
        _score_scene(3, 1, '鱼群旋转：单簧管与弦乐的永动', 'Circling fishes: clarinet and string motion',
            '单簧管旋律、弦乐音流、大管低音和打击乐各有独立节奏。无固定音高的打击乐以通用 MIDI 音色近似呈现。',
            'Clarinet, string motion, bassoon and percussion each retain their own rhythm. Unpitched percussion uses an approximate General MIDI sound.',
            108, 48, 87, 32, 57, 96, [3, 8], [
                _score_track('winds', '单簧管', 'Clarinet',
                    [[240, 3, 56, 31, 71], [243, 13, 55, 31, 71], [288, 3, 56, 31, 71], [291, 74, 55, 31, 71], [384, 3, 56, 31, 71], [387, 13, 55, 31, 71], [432, 3, 56, 31, 71], [435, 74, 55, 31, 71], [528, 3, 56, 31, 71], [531, 13, 55, 31, 71], [576, 3, 56, 31, 71], [579, 74, 55, 31, 71], [672, 3, 56, 31, 71], [675, 13, 55, 31, 71], [720, 3, 56, 31, 71], [723, 74, 55, 31, 71], [816, 3, 56, 31, 71], [819, 13, 55, 31, 71], [864, 547, 58, 31, 71], [1944, 24, 67, 47, 71], [1968, 31, 67, 47, 71], [1968, 24, 72, 47, 71], [1992, 24, 74, 47, 71], [2016, 72, 67, 47, 71], [2016, 24, 76, 47, 71], [2040, 24, 74, 47, 71], [2064, 24, 72, 47, 71], [2088, 24, 67, 47, 71], [2112, 31, 67, 47, 71], [2112, 24, 72, 47, 71], [2136, 24, 74, 47, 71], [2160, 77, 67, 47, 71], [2160, 77, 76, 47, 71], [2520, 24, 67, 47, 71], [2544, 31, 67, 47, 71], [2544, 24, 72, 47, 71], [2568, 24, 74, 47, 71], [2592, 72, 67, 47, 71], [2592, 24, 76, 47, 71], [2616, 24, 74, 47, 71], [2640, 24, 72, 47, 71], [2664, 24, 67, 47, 71], [2688, 31, 67, 47, 71], [2688, 24, 72, 47, 71], [2712, 24, 74, 47, 71], [2736, 77, 67, 47, 71], [2736, 77, 76, 47, 71]],
                    96, 108, [6], False),
                _score_track('strings', '第一小提琴', 'Violins I',
                    [[240, 24, 60, 47, 48], [264, 24, 55, 47, 48], [288, 24, 60, 47, 48], [312, 24, 62, 47, 48], [336, 24, 63, 47, 48], [360, 24, 65, 47, 48], [384, 24, 67, 47, 48], [408, 24, 68, 47, 48], [432, 24, 67, 47, 48], [456, 24, 63, 47, 48], [480, 24, 60, 47, 48], [504, 24, 62, 47, 48], [528, 24, 63, 47, 48], [552, 24, 65, 47, 48], [576, 3, 68, 47, 48], [579, 21, 67, 47, 48], [600, 24, 66, 47, 48], [624, 24, 67, 47, 48], [648, 24, 71, 47, 48], [672, 24, 72, 47, 48], [696, 24, 74, 47, 48], [720, 24, 75, 47, 48], [744, 24, 79, 47, 48], [768, 24, 77, 47, 48], [792, 24, 75, 47, 48], [816, 24, 74, 47, 48], [840, 24, 72, 47, 48], [864, 24, 70, 47, 48], [888, 24, 72, 47, 48], [912, 24, 70, 47, 48], [936, 24, 72, 47, 48], [960, 24, 68, 47, 48], [984, 24, 70, 47, 48], [1008, 24, 67, 47, 48], [1032, 24, 70, 47, 48], [1056, 24, 75, 47, 48], [1080, 24, 79, 47, 48], [1104, 24, 77, 47, 48], [1128, 24, 75, 47, 48], [1152, 24, 70, 47, 48], [1176, 24, 72, 47, 48], [1200, 24, 70, 47, 48], [1224, 24, 72, 47, 48], [1248, 24, 68, 47, 48], [1272, 24, 70, 47, 48], [1296, 24, 67, 47, 48], [1320, 24, 70, 47, 48], [1344, 24, 75, 47, 48], [1368, 24, 82, 47, 48], [1392, 24, 80, 47, 48], [1416, 24, 79, 47, 48], [1440, 24, 77, 47, 48], [1464, 24, 76, 47, 48], [1488, 24, 77, 47, 48], [1512, 24, 80, 47, 48], [1536, 24, 79, 47, 48], [1560, 24, 77, 47, 48], [1584, 24, 75, 47, 48], [1608, 24, 74, 47, 48], [1632, 24, 75, 47, 48], [1656, 24, 79, 47, 48], [1680, 24, 77, 47, 48], [1704, 24, 75, 47, 48], [1728, 24, 73, 47, 48], [1752, 24, 75, 47, 48], [1776, 24, 73, 47, 48], [1800, 24, 72, 47, 48], [1824, 24, 70, 47, 48], [1848, 24, 68, 47, 48], [1872, 24, 67, 47, 48], [1896, 24, 64, 47, 48], [1920, 16, 60, 47, 48], [2232, 24, 67, 31, 48], [2256, 24, 76, 31, 48], [2280, 24, 77, 31, 48], [2304, 24, 76, 31, 48], [2328, 16, 74, 31, 48], [2352, 24, 74, 31, 48], [2376, 16, 73, 31, 48], [2400, 24, 74, 31, 48], [2424, 24, 76, 31, 48], [2448, 24, 74, 31, 48], [2472, 16, 72, 31, 48], [2496, 16, 72, 31, 48], [2808, 24, 67, 31, 48], [2832, 24, 76, 31, 48], [2856, 24, 80, 31, 48], [2880, 24, 79, 31, 48], [2904, 16, 77, 31, 48], [2928, 24, 77, 31, 48], [2952, 19, 76, 31, 48], [2976, 24, 77, 31, 48], [3000, 24, 79, 31, 48], [3024, 24, 77, 31, 48], [3048, 16, 76, 31, 48], [3072, 16, 76, 31, 48], [3360, 38, 55, 47, 45], [3408, 38, 64, 47, 45], [3504, 38, 56, 47, 45], [3552, 38, 65, 47, 45], [3648, 38, 55, 47, 45], [3696, 38, 64, 47, 45]],
                    96, 108, [21], False),
                _score_track('strings', '大提琴', 'Cellos',
                    [[0, 38, 48, 47, 45], [48, 38, 51, 47, 45], [96, 38, 50, 47, 45], [144, 38, 48, 47, 45], [192, 38, 51, 47, 45], [240, 38, 50, 47, 45], [288, 38, 48, 47, 45], [336, 38, 51, 47, 45], [384, 38, 50, 47, 45], [432, 38, 48, 47, 45], [480, 38, 51, 47, 45], [528, 38, 50, 47, 45], [576, 38, 48, 47, 45], [624, 38, 51, 47, 45], [672, 38, 50, 47, 45], [720, 38, 48, 47, 45], [768, 38, 51, 47, 45], [816, 38, 55, 47, 45], [864, 38, 50, 47, 45], [912, 38, 53, 47, 45], [960, 38, 58, 47, 45], [1008, 38, 51, 47, 45], [1056, 38, 55, 47, 45], [1104, 38, 58, 47, 45], [1152, 38, 50, 47, 45], [1200, 38, 53, 47, 45], [1248, 38, 58, 47, 45], [1296, 38, 51, 47, 45], [1344, 38, 55, 47, 45], [1392, 38, 58, 47, 45], [1440, 38, 53, 47, 45], [1488, 38, 56, 47, 45], [1536, 38, 61, 47, 45], [1584, 38, 56, 47, 45], [1632, 38, 60, 47, 45], [1680, 38, 63, 47, 45], [1728, 38, 58, 47, 45], [1824, 38, 56, 47, 45], [1872, 38, 55, 47, 45], [1968, 48, 55, 31, 48], [2016, 38, 48, 31, 48], [2064, 38, 55, 47, 45], [2112, 38, 43, 47, 45], [2160, 38, 48, 47, 45], [2208, 38, 55, 47, 45], [2256, 38, 43, 47, 45], [2304, 38, 47, 47, 45], [2352, 38, 56, 47, 45], [2400, 38, 43, 47, 45], [2448, 38, 48, 47, 45], [2496, 38, 55, 47, 45], [2544, 38, 43, 47, 45], [2592, 38, 48, 47, 45], [2640, 38, 55, 47, 45], [2688, 38, 43, 47, 45], [2736, 38, 48, 47, 45], [2784, 38, 55, 47, 45], [2832, 38, 43, 47, 45], [2880, 38, 49, 47, 45], [2928, 38, 56, 47, 45], [2976, 38, 49, 47, 45], [3024, 38, 48, 47, 45], [3072, 38, 55, 47, 45], [3168, 38, 48, 47, 45], [3216, 38, 56, 47, 45], [3264, 38, 65, 47, 45], [3456, 38, 47, 47, 45], [3600, 38, 48, 47, 45]],
                    96, 108, [24], False),
                _score_track('winds', '大管', 'Bassoon',
                    [[240, 31, 43, 31, 70], [288, 31, 48, 31, 70], [336, 31, 51, 31, 70], [384, 31, 43, 31, 70], [384, 31, 50, 31, 70], [432, 31, 48, 31, 70], [480, 31, 51, 31, 70], [528, 31, 43, 31, 70], [528, 31, 50, 31, 70], [576, 31, 48, 31, 70], [624, 31, 51, 31, 70], [672, 31, 43, 31, 70], [672, 31, 50, 31, 70], [720, 31, 48, 31, 70]],
                    96, 108, [8], False),
                _score_track('perc', '打击乐节奏（通用 MIDI 近似）', 'Percussion pulse (GM approximation)',
                    [[48, 38, 49, 47, 0], [96, 38, 49, 47, 0], [192, 38, 49, 47, 0], [240, 38, 49, 47, 0]],
                    96, 108, [10], True),
            ], 'f7064199806a8ea50eef77d79e47a0240fe32f50be93fa344f39296ec633e09e', 'https://gustavmahler.com/site/midi/symphony2/3rd-movement-Scherzo-In-ruhig-fliessenttaca.midi'),
        _score_scene(3, 2, 'D大调中部：小号、圆号与弦乐', 'D major middle section: trumpet, horn and strings',
            '小号旋律与圆号内声部单独成轨，弦乐和大管保留各自的伴奏运动，不把所有乐器压成同一旋律。',
            'Trumpet melody and horn inner parts have separate tracks; strings and bassoon keep their own motion rather than sharing a single tune.',
            100, 319.5, 354, 213, 235, 96, [3, 8], [
                _score_track('brass', '第一小号组', 'Trumpets I',
                    [[0, 77, 66, 111, 56], [0, 77, 74, 111, 56], [96, 31, 69, 111, 56], [144, 58, 66, 111, 56], [144, 58, 74, 111, 56], [216, 16, 69, 111, 56], [216, 16, 76, 111, 56], [240, 31, 74, 111, 56], [240, 31, 78, 111, 56], [288, 38, 66, 111, 56], [288, 38, 74, 111, 56], [336, 38, 66, 111, 56], [336, 38, 74, 111, 56], [384, 38, 69, 111, 56], [432, 77, 66, 111, 56], [432, 77, 74, 111, 56], [528, 31, 69, 111, 56], [576, 403, 62, 95, 56], [576, 403, 74, 95, 56], [1296, 31, 81, 111, 56], [1344, 16, 81, 111, 56], [1368, 16, 81, 111, 56], [1392, 16, 81, 111, 56], [1416, 16, 81, 111, 56], [1440, 31, 81, 111, 56], [1488, 16, 81, 111, 56], [1512, 16, 81, 111, 56], [1536, 16, 81, 111, 56], [1560, 16, 81, 111, 56], [1584, 221, 81, 111, 56], [2976, 31, 61, 111, 56], [3024, 58, 66, 111, 56], [3096, 16, 69, 111, 56], [3120, 31, 73, 111, 56], [3168, 31, 78, 111, 56], [3216, 31, 78, 111, 56], [3264, 31, 78, 111, 56]],
                    96, 100, [13], False),
                _score_track('horns', '第一圆号组', 'Horns I',
                    [[0, 77, 54, 111, 60], [0, 77, 62, 111, 60], [96, 31, 57, 111, 60], [144, 58, 54, 111, 60], [144, 58, 62, 111, 60], [216, 16, 57, 111, 60], [216, 16, 64, 111, 60], [240, 31, 62, 111, 60], [240, 31, 66, 111, 60], [288, 38, 54, 111, 60], [288, 38, 62, 111, 60], [336, 38, 54, 111, 60], [336, 38, 62, 111, 60], [384, 38, 57, 111, 60], [432, 77, 54, 111, 60], [432, 77, 62, 111, 60], [528, 31, 57, 111, 60], [576, 58, 62, 111, 60], [648, 16, 66, 111, 60], [672, 31, 69, 111, 60], [720, 31, 74, 111, 60], [768, 31, 74, 111, 60], [816, 31, 74, 111, 60], [864, 48, 74, 111, 60], [912, 16, 76, 111, 60], [936, 16, 73, 111, 60], [960, 16, 74, 111, 60], [984, 16, 71, 111, 60], [1008, 77, 69, 111, 60], [1584, 115, 62, 111, 60], [1584, 115, 66, 111, 60], [1584, 115, 69, 111, 60], [1728, 115, 62, 111, 60], [1728, 115, 66, 111, 60], [1728, 115, 71, 111, 60], [1872, 115, 61, 111, 60], [1872, 115, 64, 111, 60], [1872, 115, 69, 111, 60], [2016, 115, 62, 111, 60], [2016, 115, 66, 111, 60], [2016, 115, 71, 111, 60], [2160, 115, 64, 111, 60], [2160, 115, 67, 111, 60], [2160, 115, 71, 111, 60], [2304, 115, 66, 111, 60], [2304, 115, 69, 111, 60], [2448, 115, 64, 111, 60], [2448, 115, 67, 111, 60], [2448, 115, 71, 111, 60], [2592, 115, 64, 111, 60], [2592, 115, 68, 111, 60]],
                    96, 100, [11], False),
                _score_track('strings', '第一小提琴', 'Violins I',
                    [[0, 19, 74, 100, 48], [24, 19, 69, 100, 48], [48, 19, 66, 100, 48], [72, 19, 69, 100, 48], [96, 19, 74, 100, 48], [120, 19, 76, 100, 48], [144, 19, 78, 100, 48], [168, 19, 79, 100, 48], [192, 19, 81, 100, 48], [216, 19, 79, 100, 48], [240, 19, 78, 100, 48], [264, 19, 76, 100, 48], [288, 19, 74, 100, 48], [312, 19, 69, 100, 48], [336, 19, 66, 100, 48], [360, 19, 69, 100, 48], [384, 19, 74, 100, 48], [408, 19, 76, 100, 48], [432, 19, 78, 100, 48], [456, 19, 79, 100, 48], [480, 19, 78, 100, 48], [504, 19, 76, 100, 48], [528, 19, 74, 100, 48], [552, 19, 76, 100, 48], [576, 24, 78, 100, 48], [600, 19, 81, 100, 48], [624, 19, 78, 100, 48], [648, 19, 74, 100, 48], [672, 19, 76, 100, 48], [696, 19, 73, 100, 48], [720, 24, 74, 100, 48], [744, 19, 78, 100, 48], [768, 19, 74, 100, 48], [792, 19, 71, 100, 48], [816, 19, 73, 100, 48], [840, 19, 69, 100, 48], [864, 24, 71, 100, 48], [888, 19, 69, 100, 48], [912, 19, 71, 100, 48], [936, 19, 73, 100, 48], [960, 19, 74, 100, 48], [984, 19, 78, 100, 48], [1008, 19, 73, 95, 48], [1008, 19, 81, 95, 48], [1032, 19, 83, 95, 48], [1056, 19, 81, 95, 48], [1080, 19, 79, 95, 48], [1104, 19, 78, 95, 48], [1128, 19, 79, 95, 48], [1152, 19, 73, 95, 48], [1152, 19, 81, 95, 48], [1176, 19, 83, 95, 48], [1200, 19, 81, 95, 48], [1224, 19, 79, 95, 48], [1248, 19, 78, 95, 48], [1272, 19, 76, 95, 48], [1296, 19, 78, 95, 48], [1320, 19, 79, 95, 48], [1344, 19, 78, 95, 48], [1368, 19, 76, 95, 48], [1392, 19, 74, 95, 48], [1416, 19, 76, 95, 48], [1440, 19, 78, 95, 48], [1464, 19, 79, 95, 48], [1488, 19, 78, 95, 48], [1512, 19, 76, 95, 48], [1536, 19, 74, 95, 48], [1560, 19, 76, 95, 48], [1584, 115, 69, 111, 48], [1584, 115, 81, 111, 48], [1728, 31, 71, 111, 48], [1728, 31, 83, 111, 48], [1800, 16, 85, 111, 48], [1824, 31, 86, 111, 48], [1872, 115, 73, 111, 48], [1872, 115, 85, 111, 48], [2016, 31, 74, 111, 48], [2016, 31, 86, 111, 48], [2088, 16, 88, 111, 48], [2112, 31, 90, 111, 48], [2160, 115, 76, 111, 48], [2160, 115, 88, 111, 48], [2304, 115, 73, 111, 48], [2304, 115, 85, 111, 48], [2448, 115, 76, 111, 48], [2448, 115, 88, 111, 48], [2592, 163, 73, 111, 48], [2592, 163, 85, 111, 48], [2760, 19, 86, 111, 48], [2784, 19, 85, 111, 48], [2808, 19, 83, 111, 48], [2832, 19, 81, 111, 48], [2856, 19, 80, 111, 48], [2880, 19, 78, 111, 48], [2904, 19, 73, 111, 48], [2928, 19, 78, 111, 48], [2952, 19, 80, 111, 48], [2976, 19, 81, 111, 48], [3000, 19, 83, 111, 48], [3024, 19, 85, 111, 48], [3048, 19, 86, 111, 48], [3072, 19, 85, 111, 48], [3096, 19, 83, 111, 48], [3120, 19, 81, 111, 48], [3144, 19, 80, 111, 48], [3168, 19, 78, 111, 48], [3192, 19, 73, 111, 48], [3216, 19, 78, 111, 48], [3240, 19, 80, 111, 48], [3264, 19, 81, 111, 48], [3288, 19, 83, 111, 48]],
                    96, 100, [21], False),
                _score_track('strings', '大提琴', 'Cellos',
                    [[0, 31, 50, 100, 48], [48, 31, 50, 100, 48], [96, 31, 54, 100, 48], [144, 31, 50, 100, 48], [192, 16, 50, 100, 48], [216, 16, 45, 100, 48], [240, 16, 47, 100, 48], [264, 16, 49, 100, 48], [288, 19, 50, 100, 48], [312, 19, 49, 100, 48], [336, 19, 50, 100, 48], [360, 19, 52, 100, 48], [384, 19, 54, 100, 48], [408, 19, 57, 100, 48], [432, 31, 50, 100, 48], [480, 16, 50, 100, 48], [504, 19, 57, 100, 48], [528, 19, 59, 100, 48], [552, 19, 61, 100, 48], [576, 24, 62, 100, 48], [600, 19, 61, 100, 48], [624, 19, 62, 100, 48], [648, 19, 59, 100, 48], [672, 19, 61, 100, 48], [696, 19, 57, 100, 48], [720, 24, 59, 100, 48], [744, 19, 57, 100, 48], [768, 19, 59, 100, 48], [792, 19, 55, 100, 48], [816, 19, 57, 100, 48], [840, 19, 54, 100, 48], [864, 24, 55, 100, 48], [888, 19, 54, 100, 48], [912, 19, 55, 100, 48], [936, 19, 52, 100, 48], [960, 19, 54, 100, 48], [984, 19, 50, 100, 48], [1008, 19, 49, 95, 48], [1032, 19, 45, 95, 48], [1056, 19, 49, 95, 48], [1080, 19, 54, 95, 48], [1104, 19, 57, 95, 48], [1128, 19, 54, 95, 48], [1152, 19, 49, 95, 48], [1176, 19, 45, 95, 48], [1200, 19, 49, 95, 48], [1224, 19, 54, 95, 48], [1248, 19, 57, 95, 48], [1272, 19, 54, 95, 48], [1296, 19, 50, 95, 48], [1320, 19, 45, 95, 48], [1344, 19, 50, 95, 48], [1368, 19, 52, 95, 48], [1392, 19, 54, 95, 48], [1416, 19, 52, 95, 48], [1440, 19, 50, 95, 48], [1464, 19, 45, 95, 48], [1488, 19, 50, 95, 48], [1512, 19, 52, 95, 48], [1536, 19, 54, 95, 48], [1560, 19, 57, 95, 48], [1584, 19, 62, 111, 48], [1608, 19, 61, 111, 48], [1632, 19, 62, 111, 48], [1656, 19, 59, 111, 48], [1680, 19, 61, 111, 48], [1704, 19, 57, 111, 48], [1728, 19, 59, 111, 48], [1752, 19, 57, 111, 48], [1776, 19, 59, 111, 48], [1800, 19, 55, 111, 48], [1824, 19, 57, 111, 48], [1848, 19, 54, 111, 48], [1872, 19, 59, 111, 48], [1896, 19, 57, 111, 48], [1920, 19, 59, 111, 48], [1944, 19, 55, 111, 48], [1968, 19, 57, 111, 48], [1992, 19, 54, 111, 48], [2016, 19, 55, 111, 48], [2040, 19, 54, 111, 48], [2064, 19, 55, 111, 48], [2088, 19, 52, 111, 48], [2112, 19, 54, 111, 48], [2136, 19, 50, 111, 48], [2160, 19, 52, 111, 48], [2184, 19, 54, 111, 48], [2208, 19, 55, 111, 48], [2232, 19, 52, 111, 48], [2256, 19, 54, 111, 48], [2280, 19, 55, 111, 48], [2304, 19, 57, 111, 48], [2328, 19, 59, 111, 48], [2352, 19, 57, 111, 48], [2376, 19, 55, 111, 48], [2400, 19, 57, 111, 48], [2424, 19, 54, 111, 48], [2448, 19, 55, 111, 48], [2472, 19, 57, 111, 48], [2496, 19, 59, 111, 48], [2520, 19, 55, 111, 48], [2544, 19, 57, 111, 48], [2568, 19, 59, 111, 48], [2592, 19, 61, 111, 48], [2616, 19, 62, 111, 48], [2640, 19, 61, 111, 48], [2664, 19, 59, 111, 48], [2688, 19, 57, 111, 48], [2712, 19, 56, 111, 48], [2736, 19, 54, 111, 48], [2760, 19, 49, 111, 48], [2784, 19, 54, 111, 48], [2808, 19, 56, 111, 48], [2832, 19, 57, 111, 48], [2856, 19, 59, 111, 48], [2880, 19, 61, 111, 48], [2904, 19, 62, 111, 48], [2928, 19, 61, 111, 48], [2952, 19, 59, 111, 48], [2976, 19, 57, 111, 48], [3000, 19, 56, 111, 48], [3024, 19, 54, 111, 48], [3048, 19, 49, 111, 48], [3072, 19, 54, 111, 48], [3096, 19, 56, 111, 48], [3120, 19, 57, 111, 48], [3144, 19, 59, 111, 48], [3168, 19, 61, 111, 48], [3192, 19, 62, 111, 48], [3216, 19, 61, 111, 48], [3240, 19, 59, 111, 48], [3264, 19, 57, 111, 48], [3288, 19, 56, 111, 48]],
                    96, 100, [24], False),
                _score_track('winds', '大管', 'Bassoon',
                    [[0, 31, 50, 79, 70], [48, 31, 50, 79, 70], [96, 31, 54, 79, 70], [144, 31, 50, 79, 70], [192, 16, 50, 79, 70], [216, 16, 45, 79, 70], [240, 16, 47, 79, 70], [264, 16, 49, 79, 70], [288, 16, 50, 79, 70], [312, 16, 49, 79, 70], [336, 16, 50, 79, 70], [360, 16, 52, 79, 70], [384, 16, 54, 79, 70], [408, 16, 57, 79, 70], [432, 31, 50, 79, 70], [480, 16, 50, 79, 70], [504, 16, 45, 79, 70], [504, 16, 57, 79, 70], [528, 16, 47, 79, 70], [528, 16, 59, 79, 70], [552, 16, 49, 79, 70], [552, 16, 61, 79, 70], [576, 16, 50, 79, 70], [576, 16, 62, 79, 70], [600, 16, 49, 79, 70], [600, 16, 61, 79, 70], [624, 16, 50, 79, 70], [624, 16, 62, 79, 70], [648, 16, 47, 79, 70], [648, 16, 59, 79, 70], [672, 16, 49, 79, 70], [672, 16, 61, 79, 70], [696, 16, 45, 79, 70], [696, 16, 57, 79, 70], [720, 16, 47, 79, 70], [720, 16, 59, 79, 70], [744, 16, 45, 79, 70], [744, 16, 57, 79, 70], [768, 16, 47, 79, 70], [768, 16, 59, 79, 70], [792, 16, 43, 79, 70], [792, 16, 55, 79, 70], [816, 16, 45, 79, 70], [816, 16, 57, 79, 70], [840, 16, 42, 79, 70], [840, 16, 54, 79, 70], [864, 16, 43, 79, 70], [864, 16, 55, 79, 70], [888, 16, 42, 79, 70], [888, 16, 54, 79, 70], [912, 16, 43, 79, 70], [912, 16, 55, 79, 70], [936, 16, 40, 79, 70], [936, 16, 52, 79, 70], [960, 16, 42, 79, 70], [960, 16, 54, 79, 70], [984, 16, 38, 79, 70], [984, 16, 50, 79, 70], [1008, 16, 37, 79, 70], [1008, 16, 49, 79, 70], [1032, 16, 33, 79, 70], [1032, 16, 45, 79, 70], [1056, 16, 37, 79, 70], [1056, 16, 49, 79, 70], [1080, 16, 42, 79, 70], [1080, 16, 54, 79, 70], [1104, 16, 45, 79, 70], [1104, 16, 57, 79, 70], [1128, 16, 42, 79, 70], [1128, 16, 54, 79, 70], [1152, 16, 37, 79, 70], [1152, 16, 49, 79, 70], [1176, 16, 33, 79, 70], [1176, 16, 45, 79, 70], [1200, 16, 37, 79, 70], [1200, 16, 49, 79, 70], [1224, 16, 42, 79, 70], [1224, 16, 54, 79, 70], [1248, 16, 45, 79, 70], [1248, 16, 57, 79, 70], [1272, 16, 42, 79, 70], [1272, 16, 54, 79, 70], [1296, 16, 50, 79, 70], [1320, 16, 45, 79, 70], [1344, 16, 50, 79, 70], [1368, 16, 52, 79, 70], [1392, 16, 54, 79, 70], [1416, 16, 52, 79, 70], [1440, 16, 50, 79, 70], [1464, 16, 45, 79, 70], [1488, 16, 50, 79, 70], [1512, 16, 52, 79, 70], [1536, 16, 54, 79, 70], [1560, 16, 52, 79, 70], [1584, 16, 50, 79, 70], [2736, 16, 42, 79, 70], [2736, 16, 54, 79, 70], [2760, 16, 37, 79, 70], [2760, 16, 49, 79, 70], [2784, 16, 42, 79, 70], [2784, 16, 54, 79, 70], [2808, 16, 44, 79, 70], [2808, 16, 56, 79, 70], [2832, 16, 45, 79, 70], [2832, 16, 57, 79, 70], [2856, 16, 47, 79, 70], [2856, 16, 59, 79, 70], [2880, 16, 49, 79, 70], [2880, 16, 61, 79, 70], [2904, 16, 50, 79, 70], [2904, 16, 62, 79, 70], [2928, 16, 49, 79, 70], [2928, 16, 61, 79, 70], [2952, 16, 47, 79, 70], [2952, 16, 59, 79, 70], [2976, 16, 45, 79, 70], [2976, 16, 57, 79, 70], [3000, 16, 44, 79, 70], [3000, 16, 56, 79, 70], [3024, 16, 42, 79, 70], [3024, 16, 54, 79, 70], [3048, 16, 37, 79, 70], [3048, 16, 49, 79, 70], [3072, 16, 42, 79, 70], [3072, 16, 54, 79, 70], [3096, 16, 44, 79, 70], [3096, 16, 56, 79, 70], [3120, 16, 45, 79, 70], [3120, 16, 57, 79, 70], [3144, 16, 47, 79, 70], [3144, 16, 59, 79, 70], [3168, 16, 49, 79, 70], [3168, 16, 61, 79, 70], [3192, 16, 50, 79, 70], [3192, 16, 62, 79, 70], [3216, 16, 49, 79, 70], [3216, 16, 61, 79, 70], [3240, 16, 47, 79, 70], [3240, 16, 59, 79, 70], [3264, 16, 45, 79, 70], [3264, 16, 57, 79, 70], [3288, 16, 44, 79, 70], [3288, 16, 56, 79, 70]],
                    96, 100, [8], False),
            ], 'f7064199806a8ea50eef77d79e47a0240fe32f50be93fa344f39296ec633e09e', 'https://gustavmahler.com/site/midi/symphony2/3rd-movement-Scherzo-In-ruhig-fliessenttaca.midi'),
        _score_scene(3, 3, '危机段：铜管、木管与弦乐的冲突', 'Crisis passage: brass, winds and strings',
            '快速木管、尖锐铜管与弦乐运动同时展开；这是一段有来源的缩编，未声称包含整支乐队的全部声部。',
            'Fast winds, incisive brass and string motion unfold simultaneously. This sourced reduction does not claim to include every orchestral part.',
            104, 687, 723, 458, 481, 96, [3, 8], [
                _score_track('brass', '第一小号组', 'Trumpets I',
                    [[0, 38, 72, 95, 56], [144, 16, 72, 111, 56], [168, 16, 75, 111, 56], [192, 16, 79, 111, 56], [216, 16, 75, 111, 56], [240, 16, 72, 111, 56], [264, 16, 67, 111, 56], [288, 77, 72, 111, 56], [432, 16, 72, 111, 56], [456, 16, 75, 111, 56], [480, 16, 79, 111, 56], [504, 16, 75, 111, 56], [528, 16, 72, 111, 56], [552, 16, 67, 111, 56], [576, 8, 72, 111, 56], [584, 8, 73, 111, 56], [592, 8, 72, 111, 56], [600, 8, 73, 111, 56], [608, 8, 72, 111, 56], [616, 8, 73, 111, 56], [624, 8, 72, 111, 56], [632, 8, 73, 111, 56], [640, 8, 72, 111, 56], [648, 8, 73, 111, 56], [656, 8, 72, 111, 56], [664, 8, 73, 111, 56], [672, 8, 72, 111, 56], [680, 8, 73, 111, 56], [688, 8, 72, 111, 56], [696, 8, 73, 111, 56], [704, 8, 72, 111, 56], [712, 8, 73, 111, 56], [720, 8, 72, 111, 56], [728, 8, 73, 111, 56], [736, 8, 72, 111, 56], [744, 8, 73, 111, 56], [752, 8, 72, 111, 56], [760, 8, 73, 111, 56], [768, 8, 72, 111, 56], [776, 8, 73, 111, 56], [784, 8, 72, 111, 56], [792, 8, 73, 111, 56], [800, 8, 72, 111, 56], [808, 8, 73, 111, 56], [816, 8, 72, 111, 56], [824, 8, 73, 111, 56], [832, 8, 72, 111, 56], [840, 8, 73, 111, 56], [848, 8, 72, 111, 56], [856, 8, 73, 111, 56], [864, 8, 72, 111, 56], [872, 8, 73, 111, 56], [880, 8, 72, 111, 56], [888, 8, 73, 111, 56], [896, 8, 72, 111, 56], [904, 8, 73, 111, 56], [912, 8, 72, 111, 56], [920, 8, 73, 111, 56], [928, 8, 72, 111, 56], [936, 8, 73, 111, 56], [944, 8, 72, 111, 56], [952, 8, 73, 111, 56], [960, 8, 72, 111, 56], [968, 8, 73, 111, 56], [976, 8, 72, 111, 56], [984, 8, 73, 111, 56], [992, 8, 72, 111, 56], [1000, 8, 73, 111, 56], [1008, 8, 72, 111, 56], [1016, 8, 73, 111, 56], [1024, 8, 72, 111, 56], [1032, 8, 73, 111, 56], [1040, 8, 72, 111, 56], [1048, 8, 73, 111, 56], [1056, 8, 72, 111, 56], [1064, 8, 73, 111, 56], [1072, 8, 72, 111, 56], [1080, 8, 73, 111, 56], [1088, 8, 72, 111, 56], [1152, 1190, 70, 127, 56], [1152, 1190, 73, 127, 56], [1152, 1190, 77, 127, 56], [1152, 1267, 82, 127, 56], [2448, 130, 80, 111, 56], [2592, 130, 79, 111, 56], [2736, 130, 77, 111, 56], [2880, 130, 79, 111, 56], [3024, 130, 77, 111, 56], [3168, 130, 75, 111, 56], [3312, 130, 73, 111, 56]],
                    96, 104, [13], False),
                _score_track('horns', '第一圆号组', 'Horns I',
                    [[0, 31, 72, 111, 60], [48, 16, 71, 111, 60], [72, 16, 72, 111, 60], [96, 16, 74, 111, 60], [120, 16, 76, 111, 60], [144, 77, 72, 111, 60], [288, 31, 72, 111, 60], [336, 16, 71, 111, 60], [360, 16, 72, 111, 60], [384, 16, 74, 111, 60], [408, 16, 76, 111, 60], [432, 77, 72, 111, 60], [576, 38, 72, 111, 60], [624, 19, 72, 111, 60], [648, 19, 67, 111, 60], [672, 19, 60, 111, 60], [696, 19, 67, 111, 60], [720, 38, 72, 111, 60], [768, 19, 72, 111, 60], [792, 19, 67, 111, 60], [816, 19, 60, 111, 60], [840, 19, 67, 111, 60], [864, 38, 72, 111, 60], [912, 19, 72, 111, 60], [936, 19, 67, 111, 60], [960, 19, 60, 111, 60], [984, 19, 67, 111, 60], [1008, 38, 72, 111, 60], [1056, 19, 72, 111, 60], [1080, 19, 67, 111, 60], [1104, 19, 60, 111, 60], [1152, 1411, 53, 127, 60], [1152, 1411, 58, 127, 60], [1152, 1411, 61, 127, 60], [1152, 1411, 65, 127, 60], [2592, 130, 58, 111, 60], [2592, 130, 67, 111, 60], [2736, 130, 61, 111, 60], [2736, 130, 68, 111, 60], [2880, 130, 58, 111, 60], [2880, 130, 67, 111, 60], [3024, 130, 61, 111, 60], [3024, 130, 68, 111, 60], [3168, 130, 63, 111, 60], [3168, 130, 70, 111, 60], [3312, 130, 65, 111, 60], [3312, 130, 71, 111, 60]],
                    96, 104, [11], False),
                _score_track('winds', '长笛', 'Flute',
                    [[0, 31, 84, 127, 73], [48, 16, 83, 127, 73], [72, 16, 84, 127, 73], [96, 16, 86, 127, 73], [120, 16, 88, 127, 73], [144, 77, 84, 127, 73], [288, 31, 84, 127, 73], [336, 16, 83, 127, 73], [360, 16, 84, 127, 73], [384, 16, 86, 127, 73], [408, 16, 88, 127, 73], [432, 77, 84, 127, 73], [1056, 10, 83, 127, 73], [1066, 9, 84, 127, 73], [1075, 10, 85, 127, 73], [1085, 9, 86, 127, 73], [1094, 10, 87, 127, 73], [1104, 8, 88, 127, 73], [1112, 8, 89, 127, 73], [1120, 8, 90, 127, 73], [1128, 8, 91, 127, 73], [1136, 8, 92, 127, 73], [1144, 6, 93, 127, 73], [1152, 547, 89, 127, 73], [1152, 547, 94, 127, 73], [1728, 18, 89, 79, 73], [1728, 18, 94, 79, 73], [1746, 18, 85, 79, 73], [1746, 18, 89, 79, 73], [1764, 18, 82, 79, 73], [1764, 18, 85, 79, 73], [1782, 18, 77, 79, 73], [1782, 18, 82, 79, 73], [1800, 18, 73, 79, 73], [1800, 18, 77, 79, 73], [1818, 18, 77, 79, 73], [1818, 18, 82, 79, 73], [1836, 18, 82, 79, 73], [1836, 18, 85, 79, 73], [1854, 15, 85, 79, 73], [1854, 15, 89, 79, 73], [1872, 18, 85, 79, 73], [1872, 18, 89, 79, 73], [1890, 18, 82, 79, 73], [1890, 18, 85, 79, 73], [1908, 18, 77, 79, 73], [1908, 18, 82, 79, 73], [1926, 18, 73, 79, 73], [1926, 18, 77, 79, 73], [1944, 18, 70, 79, 73], [1944, 18, 73, 79, 73], [1962, 18, 73, 79, 73], [1962, 18, 77, 79, 73], [1980, 18, 77, 79, 73], [1980, 18, 82, 79, 73], [1998, 15, 82, 79, 73], [1998, 15, 85, 79, 73], [2016, 18, 82, 79, 73], [2016, 18, 85, 79, 73], [2034, 18, 77, 79, 73], [2034, 18, 82, 79, 73], [2052, 18, 73, 79, 73], [2052, 18, 77, 79, 73], [2070, 18, 70, 79, 73], [2070, 18, 73, 79, 73], [2088, 18, 65, 79, 73], [2088, 18, 70, 79, 73], [2106, 18, 70, 79, 73], [2106, 18, 73, 79, 73], [2124, 18, 73, 79, 73], [2124, 18, 77, 79, 73], [2142, 15, 77, 79, 73], [2142, 15, 82, 79, 73], [2160, 18, 77, 79, 73], [2160, 18, 82, 79, 73], [2178, 18, 73, 79, 73], [2178, 18, 77, 79, 73], [2196, 18, 70, 79, 73], [2196, 18, 73, 79, 73], [2214, 18, 65, 79, 73], [2214, 18, 70, 79, 73], [2232, 12, 70, 79, 73], [2244, 12, 73, 79, 73], [2256, 12, 77, 79, 73], [2268, 12, 82, 79, 73], [2280, 12, 85, 79, 73], [2292, 10, 89, 79, 73], [2304, 115, 94, 95, 73], [2448, 115, 92, 95, 73], [2592, 115, 91, 95, 73], [2736, 115, 89, 95, 73], [2880, 115, 91, 95, 73], [3024, 115, 89, 95, 73], [3168, 115, 87, 95, 73], [3312, 115, 85, 95, 73]],
                    96, 104, [2], False),
                _score_track('strings', '第一小提琴', 'Violins I',
                    [[0, 19, 72, 111, 48], [0, 19, 84, 111, 48], [24, 19, 84, 111, 48], [48, 19, 84, 111, 48], [72, 19, 79, 111, 48], [96, 19, 72, 111, 48], [120, 19, 79, 111, 48], [144, 19, 84, 111, 48], [168, 19, 86, 111, 48], [192, 19, 87, 111, 48], [216, 19, 89, 111, 48], [240, 19, 87, 111, 48], [264, 19, 86, 111, 48], [288, 19, 84, 111, 48], [312, 19, 84, 111, 48], [336, 19, 84, 111, 48], [360, 19, 79, 111, 48], [384, 19, 72, 111, 48], [408, 19, 79, 111, 48], [432, 19, 84, 111, 48], [456, 19, 86, 111, 48], [480, 19, 87, 111, 48], [504, 19, 89, 111, 48], [528, 19, 87, 111, 48], [552, 19, 86, 111, 48], [576, 19, 84, 111, 44], [600, 19, 86, 111, 44], [624, 19, 84, 111, 44], [648, 19, 83, 111, 44], [672, 19, 84, 111, 44], [696, 19, 86, 111, 44], [720, 19, 84, 111, 44], [744, 19, 86, 111, 44], [768, 19, 84, 111, 44], [792, 19, 83, 111, 44], [816, 19, 84, 111, 44], [840, 19, 86, 111, 44], [864, 19, 84, 111, 44], [888, 19, 86, 111, 44], [912, 19, 84, 111, 44], [936, 19, 83, 111, 44], [960, 19, 84, 111, 44], [984, 19, 86, 111, 44], [1008, 19, 84, 127, 48], [1056, 10, 83, 127, 48], [1066, 9, 84, 127, 48], [1075, 10, 85, 127, 48], [1085, 9, 86, 127, 48], [1094, 10, 87, 127, 48], [1104, 8, 88, 127, 48], [1112, 8, 89, 127, 48], [1120, 8, 90, 127, 48], [1128, 8, 91, 127, 48], [1136, 8, 92, 127, 48], [1144, 6, 93, 127, 48], [1152, 547, 89, 127, 44], [1152, 547, 94, 127, 44], [1728, 18, 89, 79, 48], [1728, 18, 94, 79, 48], [1746, 18, 85, 79, 48], [1746, 18, 89, 79, 48], [1764, 18, 82, 79, 48], [1764, 18, 85, 79, 48], [1782, 18, 77, 79, 48], [1782, 18, 82, 79, 48], [1800, 18, 73, 79, 48], [1800, 18, 77, 79, 48], [1818, 18, 77, 79, 48], [1818, 18, 82, 79, 48], [1836, 18, 82, 79, 48], [1836, 18, 85, 79, 48], [1854, 15, 85, 79, 48], [1854, 15, 89, 79, 48], [1872, 18, 85, 79, 48], [1872, 18, 89, 79, 48], [1890, 18, 82, 79, 48], [1890, 18, 85, 79, 48], [1908, 18, 77, 79, 48], [1908, 18, 82, 79, 48], [1926, 18, 73, 79, 48], [1926, 18, 77, 79, 48], [1944, 18, 70, 79, 48], [1944, 18, 73, 79, 48], [1962, 18, 73, 79, 48], [1962, 18, 77, 79, 48], [1980, 18, 77, 79, 48], [1980, 18, 82, 79, 48], [1998, 15, 82, 79, 48], [1998, 15, 85, 79, 48], [2016, 18, 82, 79, 48], [2016, 18, 85, 79, 48], [2034, 18, 77, 79, 48], [2034, 18, 82, 79, 48], [2052, 18, 73, 79, 48], [2052, 18, 77, 79, 48], [2070, 18, 70, 79, 48], [2070, 18, 73, 79, 48], [2088, 18, 65, 79, 48], [2088, 18, 70, 79, 48], [2106, 18, 70, 79, 48], [2106, 18, 73, 79, 48], [2124, 18, 73, 79, 48], [2124, 18, 77, 79, 48], [2142, 15, 77, 79, 48], [2142, 15, 82, 79, 48], [2160, 18, 77, 79, 48], [2160, 18, 82, 79, 48], [2178, 18, 73, 79, 48], [2178, 18, 77, 79, 48], [2196, 18, 70, 79, 48], [2196, 18, 73, 79, 48], [2214, 18, 65, 79, 48], [2214, 18, 70, 79, 48], [2232, 18, 65, 79, 48], [2250, 18, 70, 79, 48], [2268, 18, 73, 79, 48], [2286, 15, 77, 79, 48], [2304, 130, 94, 111, 44], [2448, 144, 92, 111, 44], [2592, 144, 91, 111, 44], [2736, 144, 89, 111, 44], [2880, 144, 91, 111, 44], [3024, 144, 89, 111, 44], [3168, 144, 87, 100, 44], [3312, 130, 85, 100, 44]],
                    96, 104, [21], False),
                _score_track('strings', '大提琴', 'Cellos',
                    [[0, 115, 46, 111, 44], [144, 115, 45, 111, 44], [288, 115, 44, 111, 44], [432, 115, 43, 111, 44], [576, 96, 42, 127, 48], [672, 38, 43, 127, 48], [720, 96, 42, 127, 48], [816, 38, 43, 127, 48], [864, 19, 42, 127, 48], [912, 19, 41, 127, 48], [960, 19, 40, 127, 48], [1008, 19, 39, 127, 48], [1056, 19, 38, 127, 48], [1104, 19, 37, 127, 48], [1152, 576, 36, 127, 44], [1152, 576, 48, 127, 44], [1728, 38, 36, 47, 48], [1728, 38, 48, 47, 48], [3384, 16, 43, 100, 48], [3408, 16, 45, 100, 48], [3432, 16, 47, 100, 48]],
                    96, 104, [24], False),
            ], 'f7064199806a8ea50eef77d79e47a0240fe32f50be93fa344f39296ec633e09e', 'https://gustavmahler.com/site/midi/symphony2/3rd-movement-Scherzo-In-ruhig-fliessenttaca.midi'),
    ],
    "4": [
        _score_scene(4, 1, '原光：女低音与铜管圣咏', 'Urlicht: alto and brass chorale',
            '女低音以降D、降D、降E、F开口，弱音弦乐伴随；随后铜管圣咏接续。保留独唱与伴奏的真实休止。',
            'The alto opens D-flat, D-flat, E-flat, F with muted strings, followed by the brass chorale. The solo and accompaniment retain their actual rests.',
            54, 4, 60, 1, 15, 480, [4, 4], [
                _score_track('choir', '女低音', 'Alto',
                    [[1440, 430, 61, 47, 52], [1920, 865, 61, 47, 52], [2880, 865, 63, 47, 52], [3840, 1535, 65, 47, 52], [26400, 480, 68, 47, 52]],
                    480, 54, [30], False),
                _score_track('brass', '第一小号组', 'Trumpets I',
                    [[5760, 480, 61, 47, 56], [5760, 480, 65, 47, 56], [6240, 480, 63, 47, 56], [6240, 480, 66, 47, 56], [6720, 770, 65, 47, 56], [6720, 770, 68, 47, 56], [7680, 480, 63, 47, 56], [7680, 480, 68, 47, 56], [8160, 480, 65, 47, 56], [8160, 480, 70, 47, 56], [8640, 770, 66, 47, 56], [8640, 770, 72, 47, 56], [9600, 960, 68, 47, 56], [9600, 960, 73, 47, 56], [10560, 770, 68, 47, 56], [10560, 770, 72, 47, 56], [11520, 480, 68, 47, 56], [11520, 1920, 70, 47, 56], [12000, 480, 66, 47, 56], [12480, 480, 65, 47, 56], [12960, 480, 63, 47, 56], [13440, 1535, 65, 47, 56], [13440, 1535, 68, 47, 56], [15840, 770, 63, 47, 56], [15840, 770, 68, 47, 56], [16800, 770, 63, 47, 56], [16800, 770, 66, 47, 56], [17760, 1345, 61, 47, 56], [17760, 1345, 65, 47, 56], [19200, 770, 61, 47, 56], [19200, 770, 66, 47, 56], [20160, 1440, 61, 47, 56], [20160, 2880, 63, 47, 56], [21600, 1440, 60, 47, 56], [23040, 385, 61, 47, 56], [23520, 1535, 61, 47, 56]],
                    480, 54, [13], False),
                _score_track('horns', '第一圆号组', 'Horns I',
                    [[5760, 1535, 56, 31, 60], [7680, 770, 63, 31, 60], [8640, 770, 56, 31, 60], [9600, 770, 61, 31, 60], [10560, 770, 53, 31, 60], [11520, 1535, 54, 31, 60], [13440, 1535, 49, 31, 60], [13440, 1535, 61, 31, 60], [15840, 770, 48, 31, 60], [15840, 770, 60, 31, 60], [16800, 770, 51, 31, 60], [16800, 770, 58, 31, 60], [17760, 1345, 46, 31, 60], [17760, 1345, 58, 31, 60], [19200, 770, 42, 31, 60], [19200, 770, 58, 31, 60], [20160, 2880, 44, 31, 60], [20160, 2975, 56, 31, 60], [23040, 385, 49, 31, 60], [23520, 1535, 49, 31, 60], [23520, 1535, 56, 31, 60]],
                    480, 54, [11], False),
                _score_track('strings', '第一小提琴', 'Violins I',
                    [[1920, 865, 61, 15, 48], [2880, 865, 63, 15, 48], [3840, 1535, 65, 15, 48]],
                    480, 54, [21], False),
                _score_track('strings', '大提琴', 'Cellos',
                    [[1920, 865, 49, 15, 48], [2880, 865, 44, 15, 48], [2880, 865, 51, 15, 48], [3840, 1535, 44, 15, 48], [3840, 1535, 49, 15, 48]],
                    480, 54, [24], False),
            ], 'c052b61bb24f76fd87664b1a00d6869d2eb975075948f631c7acf37dbaf68d42', 'https://gustavmahler.com/site/midi/symphony2/4th-movement-Ulrich-Sehr-feierlich-aber.midi'),
        _score_scene(4, 2, '原光中段：女低音、双簧管与弦乐', 'Urlicht middle passage: alto, oboe and strings',
            '双簧管在独唱停歇处继续歌唱，小提琴与大提琴分别承接高音和低音线条。',
            'The oboe continues singing during the soloist’s rests, while violin and cello carry distinct upper and lower lines.',
            58, 103, 140, 28, 36, 480, [4, 4], [
                _score_track('choir', '女低音', 'Alto',
                    [[0, 480, 65, 47, 52], [480, 480, 66, 47, 52], [960, 960, 68, 47, 52], [1920, 480, 68, 47, 52], [2400, 480, 70, 47, 52], [2880, 480, 72, 47, 52], [3360, 480, 72, 47, 52], [3840, 960, 73, 47, 52], [4800, 480, 72, 47, 52], [5280, 1150, 70, 47, 52]],
                    480, 58, [30], False),
                _score_track('winds', '双簧管', 'Oboe',
                    [[0, 480, 65, 31, 68], [480, 480, 66, 31, 68], [960, 770, 68, 31, 68], [1920, 480, 68, 31, 68], [2400, 480, 70, 31, 68], [2880, 770, 72, 31, 68], [3840, 960, 73, 31, 68], [4800, 480, 72, 31, 68], [5280, 1440, 70, 31, 68], [6720, 480, 75, 31, 68], [7200, 385, 73, 31, 68], [7680, 960, 73, 31, 68], [8640, 480, 72, 31, 68], [9120, 480, 70, 31, 68], [9600, 480, 68, 31, 68], [10080, 385, 77, 31, 68], [10560, 1150, 75, 31, 68], [12000, 240, 77, 31, 68], [12240, 240, 75, 31, 68], [12480, 240, 74, 31, 68], [12720, 240, 75, 31, 68], [12960, 960, 78, 31, 68], [13920, 385, 77, 31, 68], [14400, 2305, 73, 31, 68]],
                    480, 58, [3], False),
                _score_track('strings', '第一小提琴', 'Violins I',
                    [[0, 480, 68, 15, 48], [480, 480, 66, 15, 48], [960, 770, 65, 15, 48], [1920, 480, 66, 15, 48], [2400, 480, 65, 15, 48], [2880, 770, 63, 15, 48], [3840, 960, 65, 15, 48], [4800, 960, 68, 15, 48], [5760, 480, 66, 15, 48], [6240, 480, 65, 15, 48], [6720, 3840, 66, 15, 48], [7680, 1920, 70, 15, 48], [9600, 960, 68, 15, 48], [10560, 2400, 68, 15, 48], [10560, 3550, 72, 15, 48], [12960, 960, 78, 15, 48], [13920, 385, 77, 15, 48], [14400, 2305, 73, 15, 48]],
                    480, 58, [21], False),
                _score_track('strings', '大提琴', 'Cellos',
                    [[0, 3840, 44, 15, 48], [0, 1920, 53, 15, 48], [1920, 1920, 54, 15, 48], [3840, 960, 46, 15, 48], [3840, 1440, 53, 15, 48], [4800, 480, 41, 15, 48], [5280, 1440, 42, 15, 48], [5280, 385, 54, 15, 48], [6720, 960, 39, 15, 48], [7680, 9025, 44, 15, 48], [10560, 6145, 37, 15, 48]],
                    480, 58, [24], False),
            ], 'c052b61bb24f76fd87664b1a00d6869d2eb975075948f631c7acf37dbaf68d42', 'https://gustavmahler.com/site/midi/symphony2/4th-movement-Ulrich-Sehr-feierlich-aber.midi'),
        _score_scene(4, 3, '永恒的光：独唱与室内乐式尾声', 'Eternal light: solo voice and chamber coda',
            '女低音、单簧管、独奏小提琴、大提琴和竖琴分别保留原始音高与节奏；固定教学速度不模拟末尾自由延长。',
            'Alto, clarinet, solo violin, cello and harp retain their source pitches and rhythms. The fixed teaching tempo does not reproduce the final expressive stretching.',
            56, 240, 268, 62, 69, 480, [4, 4], [
                _score_track('choir', '女低音', 'Alto',
                    [[0, 480, 72, 63, 52], [480, 480, 70, 63, 52], [960, 480, 68, 63, 52], [1440, 480, 66, 63, 52], [1920, 480, 65, 63, 52], [2400, 480, 63, 63, 52], [2880, 480, 65, 63, 52], [3360, 480, 66, 63, 52], [3840, 770, 68, 63, 52], [4800, 480, 68, 63, 52], [5280, 480, 70, 63, 52], [5760, 960, 72, 63, 52], [6720, 1440, 75, 63, 52], [8160, 385, 73, 63, 52]],
                    480, 56, [30], False),
                _score_track('winds', '单簧管', 'Clarinet',
                    [[2880, 480, 61, 31, 71], [2880, 480, 65, 31, 71], [3360, 480, 63, 31, 71], [3360, 480, 66, 31, 71], [3840, 770, 65, 31, 71], [3840, 770, 68, 31, 71], [4800, 480, 60, 31, 71], [4800, 1535, 66, 31, 71], [4800, 480, 68, 31, 71], [5280, 480, 61, 31, 71], [5280, 480, 70, 31, 71], [5760, 770, 63, 31, 71], [5760, 770, 72, 31, 71]],
                    480, 56, [6], False),
                _score_track('strings', '第一小提琴', 'Violins I',
                    [[0, 480, 72, 15, 40], [480, 385, 70, 15, 40], [960, 480, 72, 15, 40], [1440, 480, 70, 15, 40], [1920, 480, 68, 15, 40], [2400, 385, 66, 15, 40], [5760, 40, 72, 8, 40], [5800, 40, 73, 8, 40], [5840, 40, 72, 8, 40], [5880, 40, 73, 8, 40], [5920, 40, 72, 8, 40], [5960, 40, 73, 8, 40], [6000, 40, 72, 8, 40], [6040, 40, 73, 8, 40], [6080, 40, 72, 8, 40], [6120, 40, 73, 8, 40], [6160, 40, 72, 8, 40], [6200, 40, 73, 8, 40], [6240, 40, 72, 8, 40], [6280, 40, 73, 8, 40], [6320, 40, 72, 8, 40], [6360, 40, 73, 8, 40], [6400, 40, 72, 8, 40], [6440, 40, 73, 8, 40], [6480, 40, 72, 8, 40], [6520, 40, 73, 8, 40], [6560, 40, 72, 8, 40], [6600, 40, 70, 8, 40], [6640, 40, 72, 8, 40], [6720, 1440, 78, 15, 40], [8160, 455, 77, 15, 40], [8640, 480, 73, 15, 40], [9120, 960, 68, 15, 40], [10080, 385, 66, 15, 40], [10560, 1920, 66, 15, 40], [12480, 960, 65, 15, 40]],
                    480, 56, [21], False),
                _score_track('strings', '大提琴', 'Cellos',
                    [[0, 2495, 42, 15, 48], [0, 2495, 49, 15, 48], [6720, 2400, 49, 15, 48], [6720, 5760, 56, 15, 48], [9120, 3360, 44, 15, 48], [12480, 960, 37, 15, 48], [12480, 960, 44, 15, 48]],
                    480, 56, [24], False),
                _score_track('strings', '竖琴', 'Harp',
                    [[4000, 130, 32, 47, 46], [4160, 130, 44, 47, 46], [4320, 130, 49, 47, 46], [4480, 130, 56, 47, 46], [4640, 130, 61, 47, 46], [4800, 190, 68, 47, 46], [5920, 130, 32, 47, 46], [6080, 130, 44, 47, 46], [6240, 130, 51, 47, 46], [6400, 130, 54, 47, 46], [6560, 130, 60, 47, 46], [6720, 190, 63, 47, 46], [9120, 385, 56, 47, 46], [9600, 385, 58, 47, 46], [10080, 385, 60, 47, 46], [10880, 255, 37, 47, 46], [11200, 255, 44, 47, 46], [11520, 255, 49, 47, 46], [11840, 255, 56, 47, 46], [12160, 255, 61, 47, 46], [12480, 385, 65, 47, 46]],
                    480, 56, [18], False),
            ], 'c052b61bb24f76fd87664b1a00d6869d2eb975075948f631c7acf37dbaf68d42', 'https://gustavmahler.com/site/midi/symphony2/4th-movement-Ulrich-Sehr-feierlich-aber.midi'),
    ],
    "5": [
        _score_scene(5, 1, '终曲预示：木管、铜管与低音弦乐', 'Finale premonition: winds, brass and low strings',
            '双簧管、小号、圆号、大提琴与定音鼓从同一时间区间抽取，各声部的休止和交错进入得以保留。',
            'Oboe, trumpet, horn, cello and timpani are drawn from the same interval, preserving rests and staggered entries.',
            96, 459, 503, 131, 141, 480, [2, 2], [
                _score_track('winds', '双簧管', 'Oboe',
                    [[0, 480, 73, 95, 68], [0, 155, 80, 95, 68], [480, 385, 72, 95, 68], [1440, 1630, 73, 95, 68], [3120, 190, 72, 95, 68], [3360, 190, 71, 95, 68], [3600, 190, 72, 95, 68], [3840, 480, 73, 95, 68], [4320, 155, 72, 95, 68], [4680, 80, 73, 95, 68], [4800, 480, 73, 95, 68], [5280, 155, 72, 95, 68], [5640, 80, 73, 95, 68], [5760, 480, 73, 95, 68], [6240, 155, 72, 95, 68], [6480, 155, 82, 47, 68], [6600, 80, 73, 95, 68], [6720, 480, 73, 95, 68], [6720, 2880, 82, 47, 68], [7200, 385, 72, 95, 68], [8400, 155, 73, 95, 68], [8640, 480, 73, 95, 68], [9120, 385, 72, 95, 68], [9600, 310, 80, 47, 68], [10560, 1150, 61, 95, 68]],
                    480, 96, [3], False),
                _score_track('brass', '第一小号组', 'Trumpets I',
                    [[0, 480, 73, 111, 56], [480, 385, 72, 111, 56], [1440, 1630, 73, 111, 56], [3120, 190, 72, 111, 56], [3360, 190, 71, 111, 56], [3600, 190, 72, 111, 56], [3840, 480, 73, 111, 56], [4320, 155, 72, 111, 56], [4680, 80, 73, 111, 56], [4800, 480, 73, 111, 56], [5280, 155, 72, 111, 56], [5640, 80, 73, 111, 56], [5760, 480, 73, 111, 56], [6240, 155, 72, 111, 56], [6600, 80, 73, 111, 56], [6720, 480, 73, 111, 56], [7200, 385, 72, 111, 56], [8400, 155, 73, 111, 56], [8640, 480, 73, 111, 56], [9120, 385, 72, 111, 56]],
                    480, 96, [13], False),
                _score_track('horns', '第一圆号组', 'Horns I',
                    [[10320, 155, 61, 95, 60], [10560, 1440, 61, 95, 60], [12000, 385, 60, 95, 60]],
                    480, 96, [11], False),
                _score_track('strings', '大提琴', 'Cellos',
                    [[960, 385, 56, 100, 45], [3840, 385, 53, 100, 45], [7680, 1535, 65, 95, 44], [7680, 1535, 68, 95, 44], [10320, 155, 54, 95, 48], [10560, 1440, 54, 95, 48], [12000, 480, 53, 95, 48]],
                    480, 96, [24], False),
                _score_track('perc', '第二定音鼓', 'Timpani II',
                    [[7680, 385, 44, 95, 47], [11520, 40, 44, 47, 47], [11560, 40, 44, 47, 47], [11600, 40, 44, 47, 47], [11640, 40, 44, 47, 47], [11680, 40, 44, 47, 47], [11720, 40, 44, 47, 47], [11760, 40, 44, 47, 47], [11800, 40, 44, 47, 47], [11840, 40, 44, 47, 47], [11880, 40, 44, 47, 47], [11920, 40, 44, 47, 47], [11960, 40, 44, 47, 47], [12000, 40, 44, 47, 47], [12040, 40, 44, 47, 47], [12080, 40, 44, 47, 47], [12120, 40, 44, 47, 47], [12160, 40, 44, 47, 47], [12200, 40, 44, 47, 47], [12240, 40, 44, 47, 47], [12280, 40, 44, 47, 47], [12320, 40, 44, 47, 47], [12360, 40, 44, 47, 47], [12400, 40, 44, 47, 47], [12440, 40, 44, 47, 47], [12480, 40, 44, 47, 47], [12520, 40, 44, 47, 47], [12560, 40, 44, 47, 47], [12600, 40, 44, 47, 47], [12640, 40, 44, 47, 47], [12680, 40, 44, 47, 47], [12720, 40, 44, 47, 47], [12760, 40, 44, 47, 47], [12800, 40, 44, 47, 47], [12840, 40, 44, 47, 47], [12880, 40, 44, 47, 47], [12920, 40, 44, 47, 47], [12960, 40, 44, 47, 47], [13000, 40, 44, 47, 47], [13040, 40, 44, 47, 47], [13080, 40, 44, 47, 47], [13120, 40, 44, 47, 47], [13160, 40, 44, 47, 47], [13200, 40, 44, 47, 47], [13240, 40, 44, 47, 47], [13280, 40, 44, 47, 47], [13320, 40, 44, 47, 47], [13360, 40, 44, 47, 47], [13400, 40, 44, 47, 47], [13440, 40, 44, 47, 47], [13480, 40, 44, 47, 47], [13520, 40, 44, 47, 47], [13560, 40, 44, 47, 47], [13600, 40, 44, 47, 47], [13640, 40, 44, 47, 47], [13680, 40, 44, 47, 47], [13720, 40, 44, 47, 47], [13760, 40, 44, 47, 47], [13800, 40, 44, 47, 47], [13840, 40, 44, 47, 47], [13880, 40, 44, 47, 47], [13920, 40, 44, 47, 47], [13960, 40, 44, 47, 47], [14000, 40, 44, 47, 47], [14040, 40, 44, 47, 47], [14080, 40, 44, 47, 47], [14120, 40, 44, 47, 47], [14160, 40, 44, 47, 47], [14200, 40, 44, 47, 47], [14240, 40, 44, 47, 47], [14280, 40, 44, 47, 47], [14320, 40, 44, 47, 47], [14360, 40, 44, 47, 47], [14400, 40, 44, 47, 47], [14440, 40, 44, 47, 47], [14480, 40, 44, 47, 47], [14520, 40, 44, 47, 47], [14560, 40, 44, 47, 47], [14600, 40, 44, 47, 47], [14640, 40, 44, 47, 47], [14680, 40, 44, 47, 47], [14720, 40, 44, 47, 47], [14760, 40, 44, 47, 47], [14800, 40, 44, 47, 47], [14840, 40, 44, 47, 47], [14880, 40, 44, 47, 47], [14920, 40, 44, 47, 47], [14960, 40, 44, 47, 47], [15000, 40, 44, 47, 47], [15040, 40, 44, 47, 47], [15080, 40, 44, 47, 47], [15120, 40, 44, 47, 47], [15160, 40, 44, 47, 47], [15200, 40, 44, 47, 47], [15240, 40, 44, 47, 47], [15280, 40, 44, 47, 47], [15320, 40, 44, 47, 47], [15360, 40, 44, 47, 47], [15400, 40, 44, 47, 47], [15440, 40, 44, 47, 47], [15480, 40, 44, 47, 47], [15520, 40, 44, 47, 47], [15560, 40, 44, 47, 47], [15600, 40, 44, 47, 47], [15640, 40, 44, 47, 47], [15680, 40, 44, 47, 47], [15720, 40, 44, 47, 47], [15760, 40, 44, 47, 47], [15800, 40, 44, 47, 47], [15840, 40, 44, 47, 47], [15880, 40, 44, 47, 47], [15920, 40, 44, 47, 47], [15960, 40, 44, 47, 47], [16000, 40, 44, 47, 47], [16040, 40, 44, 47, 47], [16080, 40, 44, 47, 47], [16120, 40, 44, 47, 47], [16160, 40, 44, 47, 47], [16200, 40, 44, 47, 47], [16240, 40, 44, 47, 47], [16280, 40, 44, 47, 47], [16320, 40, 44, 47, 47], [16360, 40, 44, 47, 47], [16400, 40, 44, 47, 47], [16440, 40, 44, 47, 47], [16480, 40, 44, 47, 47], [16520, 40, 44, 47, 47], [16560, 40, 44, 47, 47], [16600, 40, 44, 47, 47], [16640, 40, 44, 47, 47], [16680, 40, 44, 47, 47], [16720, 40, 44, 47, 47], [16760, 40, 44, 47, 47], [16800, 40, 44, 47, 47], [16840, 40, 44, 47, 47], [16880, 40, 44, 47, 47], [16920, 40, 44, 47, 47], [16960, 40, 44, 47, 47], [17000, 40, 44, 47, 47], [17040, 40, 44, 47, 47], [17080, 40, 44, 47, 47], [17120, 40, 44, 47, 47], [17160, 40, 44, 47, 47], [17200, 40, 44, 47, 47], [17240, 40, 44, 47, 47], [17280, 40, 44, 47, 47], [17320, 40, 44, 47, 47], [17360, 40, 44, 47, 47], [17400, 40, 44, 47, 47], [17440, 40, 44, 47, 47], [17480, 40, 44, 47, 47], [17520, 40, 44, 47, 47], [17560, 40, 44, 47, 47], [17600, 40, 44, 47, 47], [17640, 40, 44, 47, 47], [17680, 40, 44, 47, 47], [17720, 40, 44, 47, 47], [17760, 40, 44, 47, 47], [17800, 40, 44, 47, 47], [17840, 40, 44, 47, 47], [17880, 40, 44, 47, 47], [17920, 40, 44, 47, 47], [17960, 40, 44, 47, 47], [18000, 40, 44, 47, 47], [18040, 40, 44, 47, 47], [18080, 40, 44, 47, 47], [18120, 40, 44, 47, 47], [18160, 40, 44, 47, 47], [18200, 40, 44, 47, 47], [18240, 40, 44, 47, 47], [18280, 40, 44, 47, 47], [18320, 40, 44, 47, 47], [18360, 40, 44, 47, 47], [18400, 40, 44, 47, 47], [18440, 40, 44, 47, 47], [18480, 40, 44, 47, 47], [18520, 40, 44, 47, 47], [18560, 40, 44, 47, 47], [18600, 40, 44, 47, 47], [18640, 40, 44, 47, 47], [18680, 40, 44, 47, 47], [18720, 40, 44, 47, 47], [18760, 40, 44, 47, 47], [18800, 40, 44, 47, 47], [18840, 40, 44, 47, 47], [18880, 40, 44, 47, 47], [18920, 40, 44, 47, 47], [18960, 40, 44, 47, 47], [19000, 40, 44, 47, 47], [19040, 40, 44, 47, 47], [19080, 40, 44, 47, 47], [19120, 40, 44, 47, 47], [19160, 40, 44, 47, 47], [19200, 40, 44, 47, 47], [19240, 40, 44, 47, 47], [19280, 40, 44, 47, 47], [19320, 40, 44, 47, 47], [19360, 40, 44, 47, 47], [19400, 40, 44, 47, 47], [19440, 40, 44, 47, 47], [19480, 40, 44, 47, 47], [19520, 40, 44, 47, 47], [19560, 40, 44, 47, 47], [19600, 40, 44, 47, 47], [19640, 40, 44, 47, 47], [19680, 40, 44, 47, 47], [19720, 40, 44, 47, 47], [19760, 40, 44, 47, 47], [19800, 40, 44, 47, 47], [19840, 40, 44, 47, 47], [19880, 40, 44, 47, 47], [19920, 40, 44, 47, 47], [19960, 40, 44, 47, 47], [20000, 40, 44, 47, 47], [20040, 40, 44, 47, 47], [20080, 40, 44, 47, 47], [20120, 40, 44, 47, 47], [20160, 40, 44, 47, 47], [20200, 40, 44, 47, 47], [20240, 40, 44, 47, 47], [20280, 40, 44, 47, 47], [20320, 40, 44, 47, 47], [20360, 40, 44, 47, 47], [20400, 40, 44, 47, 47], [20440, 40, 44, 47, 47], [20480, 40, 44, 47, 47], [20520, 40, 44, 47, 47], [20560, 40, 44, 47, 47], [20600, 40, 44, 47, 47], [20640, 40, 44, 47, 47], [20680, 40, 44, 47, 47], [20720, 40, 44, 47, 47], [20760, 40, 44, 47, 47], [20800, 40, 44, 47, 47], [20840, 40, 44, 47, 47], [20880, 40, 44, 47, 47], [20920, 40, 44, 47, 47], [20960, 40, 44, 47, 47], [21000, 40, 44, 47, 47], [21040, 40, 44, 47, 47], [21080, 40, 44, 47, 47]],
                    480, 96, [28], False),
            ], '35a59329ab8f1f86ec2602bb5293b9fbddc694e512aafa00e310cb8da237f302', 'https://gustavmahler.com/site/midi/symphony2/5th-movement-Im-Tempo-Des-Scherzo-Wild-H.midi'),
        _score_scene(5, 2, '大召唤：长笛与远方号角', 'Great Summons: flute and distant brass',
            '保留长笛与三条铜管线索之间的大量留白；不为满足织体密度而添加原谱没有的持续伴奏。',
            'Preserve the space between flute and three brass strands; no continuous accompaniment is added to thicken this sparse texture.',
            60, 1715, 1759, 448, 458, 480, [4, 4], [
                _score_track('winds', '长笛', 'Flute',
                    [[11520, 385, 85, 31, 73], [12000, 260, 85, 31, 73], [12320, 260, 85, 31, 73], [12640, 260, 85, 31, 73], [12960, 40, 85, 31, 73], [13000, 40, 86, 31, 73], [13040, 40, 85, 31, 73], [13080, 40, 86, 31, 73], [13120, 40, 85, 31, 73], [13160, 40, 86, 31, 73], [13200, 40, 85, 31, 73], [13240, 40, 86, 31, 73], [13280, 40, 85, 31, 73], [13320, 40, 86, 31, 73], [13360, 40, 85, 31, 73], [13400, 40, 86, 31, 73], [13440, 40, 85, 31, 73], [13480, 40, 86, 31, 73], [13520, 40, 85, 31, 73], [13560, 40, 86, 31, 73], [13600, 40, 85, 31, 73], [13640, 40, 86, 31, 73], [13680, 40, 85, 31, 73], [13720, 40, 86, 31, 73], [13760, 40, 85, 31, 73], [13800, 40, 86, 31, 73], [13840, 40, 85, 31, 73], [13880, 40, 86, 31, 73], [13920, 40, 85, 31, 73], [13960, 40, 86, 31, 73], [14000, 40, 85, 31, 73], [14040, 40, 86, 31, 73], [14080, 40, 85, 31, 73], [14120, 40, 86, 31, 73], [14160, 40, 85, 31, 73], [14200, 40, 86, 31, 73], [14240, 40, 85, 31, 73], [14280, 40, 86, 31, 73], [14320, 40, 85, 31, 73]],
                    480, 60, [2], False),
                _score_track('horns', '第一圆号组', 'Horns I',
                    [[0, 770, 61, 47, 60], [1440, 385, 54, 31, 60], [1920, 770, 61, 31, 60], [3360, 130, 61, 47, 60], [3520, 130, 54, 47, 60], [3680, 130, 61, 47, 60], [3840, 770, 66, 47, 60], [4800, 1730, 68, 47, 60]],
                    480, 60, [11], False),
                _score_track('brass', '第一小号组', 'Trumpets I',
                    [[7680, 385, 73, 63, 56], [8160, 770, 76, 63, 56], [9600, 385, 73, 47, 56], [10080, 1150, 76, 47, 56], [12960, 385, 73, 63, 56], [13440, 130, 78, 63, 56], [13600, 130, 73, 63, 56], [13760, 130, 78, 63, 56], [13920, 130, 74, 63, 56], [14080, 130, 71, 63, 56], [14240, 130, 74, 63, 56], [14400, 130, 73, 63, 56], [14560, 130, 69, 63, 56], [14720, 130, 71, 63, 56], [14880, 130, 73, 63, 56], [15040, 130, 66, 63, 56], [15200, 130, 68, 63, 56], [15360, 130, 69, 63, 56], [15520, 130, 66, 63, 56], [15680, 130, 73, 63, 56], [15840, 130, 68, 63, 56], [16000, 130, 61, 63, 56], [16160, 130, 73, 63, 56], [16320, 130, 66, 63, 56], [16480, 130, 69, 63, 56], [16640, 130, 68, 63, 56], [16800, 15, 71, 63, 56], [16815, 115, 69, 63, 56], [16960, 130, 66, 63, 56], [16960, 130, 68, 63, 56], [17120, 130, 66, 63, 56], [17280, 575, 68, 63, 56], [17280, 190, 71, 63, 56], [17440, 130, 74, 63, 56], [17600, 130, 73, 63, 56], [17760, 670, 71, 63, 56], [18000, 190, 74, 63, 56], [18240, 575, 68, 63, 56], [18400, 125, 74, 63, 56], [18560, 125, 73, 63, 56], [18720, 1250, 71, 63, 56], [18960, 190, 74, 63, 56], [19200, 960, 68, 63, 56], [20160, 130, 68, 63, 56], [20320, 130, 61, 63, 56], [20480, 130, 68, 63, 56], [20640, 130, 68, 63, 56], [20800, 130, 61, 63, 56], [20960, 130, 68, 63, 56]],
                    480, 60, [13], False),
                _score_track('brass', '第二小号组', 'Trumpets II',
                    [[14400, 770, 69, 63, 56], [14880, 385, 73, 63, 56], [15360, 1535, 66, 63, 56], [15360, 130, 78, 63, 56], [15520, 130, 76, 63, 56], [15680, 130, 78, 63, 56], [15840, 130, 80, 63, 56], [16000, 130, 78, 63, 56], [16160, 130, 76, 63, 56], [16320, 610, 61, 63, 56], [16320, 130, 78, 63, 56], [16480, 130, 76, 63, 56], [16640, 130, 74, 63, 56], [16800, 130, 76, 63, 56], [16960, 130, 74, 63, 56], [17120, 130, 69, 63, 56], [17120, 130, 73, 63, 56], [17280, 610, 61, 63, 56], [17280, 130, 73, 63, 56], [17440, 130, 68, 63, 56], [17600, 130, 73, 63, 56], [17760, 385, 76, 63, 56], [17920, 130, 68, 63, 56], [18080, 130, 71, 63, 56], [18240, 610, 61, 63, 56], [18240, 130, 73, 63, 56], [18400, 130, 68, 63, 56], [18560, 130, 73, 63, 56], [18720, 385, 76, 63, 56], [18880, 130, 68, 63, 56], [19040, 130, 71, 63, 56], [19200, 960, 61, 63, 56], [19200, 130, 73, 63, 56], [19360, 130, 68, 63, 56], [19520, 130, 73, 63, 56], [19680, 130, 73, 63, 56], [19840, 130, 68, 63, 56], [20000, 130, 73, 63, 56], [20160, 960, 61, 63, 56], [20160, 960, 73, 63, 56]],
                    480, 60, [14], False),
            ], '35a59329ab8f1f86ec2602bb5293b9fbddc694e512aafa00e310cb8da237f302', 'https://gustavmahler.com/site/midi/symphony2/5th-movement-Im-Tempo-Des-Scherzo-Wild-H.midi'),
        _score_scene(5, 3, '复活：四部合唱与器乐应答', 'Resurrection: SATB chorus and instrumental response',
            '四部合唱分别成轨，起初仅合唱发声；弦乐与长号只在后续器乐应答处进入。完整保留第一段合唱与应答，故此场景较长。',
            'SATB has four independent tracks. Initially the chorus sings alone; strings and trombone enter only in the instrumental response. The first choral paragraph and response are kept together, making this scene longer.',
            66, 1829.5, 1910.5, 475, 495, 480, [4, 4], [
                _score_track('choir', '女高音', 'Soprano',
                    [[0, 770, 61, 15, 52], [960, 770, 63, 15, 52], [1920, 770, 61, 15, 52], [3360, 240, 58, 15, 52], [3600, 190, 61, 15, 52], [3840, 480, 66, 15, 52], [4320, 385, 65, 15, 52], [4800, 770, 63, 15, 52], [5760, 770, 61, 15, 52], [7200, 240, 58, 15, 52], [7440, 190, 61, 15, 52], [7680, 770, 68, 15, 52], [8640, 770, 66, 15, 52], [9600, 770, 68, 15, 52], [10560, 770, 70, 15, 52], [11520, 480, 68, 15, 52], [12000, 385, 66, 15, 52], [12480, 480, 65, 15, 52], [12960, 385, 63, 15, 52], [13440, 480, 61, 15, 52], [13920, 960, 59, 15, 52], [14880, 1825, 58, 15, 52], [17280, 385, 56, 15, 52], [17760, 770, 61, 15, 52], [18720, 770, 63, 15, 52], [19680, 770, 64, 15, 52], [20640, 770, 59, 15, 52], [22080, 480, 64, 15, 52], [22560, 480, 63, 15, 52], [23040, 385, 64, 15, 52], [23520, 960, 65, 15, 52], [24480, 385, 64, 15, 52], [24960, 385, 63, 15, 52], [25440, 770, 64, 15, 52], [26400, 385, 59, 15, 52], [26880, 385, 64, 15, 52], [27360, 960, 65, 15, 52], [28320, 385, 66, 15, 52], [28800, 385, 68, 15, 52], [29280, 960, 70, 15, 52], [30240, 385, 68, 15, 52], [30720, 385, 66, 15, 52], [31200, 1920, 75, 15, 52], [33120, 770, 77, 15, 52], [34080, 770, 78, 15, 52], [35040, 960, 78, 15, 52], [36000, 480, 77, 15, 52], [36480, 480, 75, 15, 52], [36960, 960, 73, 15, 52], [37920, 480, 71, 15, 52], [38400, 385, 68, 15, 52]],
                    480, 66, [29], False),
                _score_track('choir', '女低音', 'Alto',
                    [[0, 770, 61, 15, 52], [960, 770, 63, 15, 52], [1920, 770, 61, 15, 52], [3360, 240, 58, 15, 52], [3600, 190, 61, 15, 52], [3840, 480, 66, 15, 52], [4320, 385, 65, 15, 52], [4800, 770, 63, 15, 52], [5760, 770, 61, 15, 52], [7200, 240, 58, 15, 52], [7440, 190, 61, 15, 52], [7680, 770, 65, 15, 52], [8640, 770, 63, 15, 52], [9600, 770, 65, 15, 52], [10560, 770, 65, 15, 52], [11520, 770, 63, 15, 52], [12480, 480, 65, 15, 52], [12960, 385, 63, 15, 52], [13440, 480, 61, 15, 52], [13920, 960, 59, 15, 52], [14880, 1825, 58, 15, 52], [17280, 385, 56, 15, 52], [17760, 770, 61, 15, 52], [18720, 770, 63, 15, 52], [19680, 770, 64, 15, 52], [20640, 770, 59, 15, 52], [22080, 480, 64, 15, 52], [22560, 480, 63, 15, 52], [23040, 385, 64, 15, 52], [23520, 960, 65, 15, 52], [24480, 385, 64, 15, 52], [24960, 385, 63, 15, 52], [25440, 770, 64, 15, 52], [26400, 385, 59, 15, 52], [26880, 385, 64, 15, 52], [27360, 960, 65, 15, 52], [28320, 385, 66, 15, 52], [28800, 385, 68, 15, 52], [29280, 960, 70, 15, 52], [30240, 385, 68, 15, 52], [30720, 385, 66, 15, 52], [31200, 960, 70, 15, 52], [31200, 960, 73, 15, 52], [32160, 770, 68, 15, 52], [32160, 770, 71, 15, 52], [33120, 1535, 66, 15, 52], [33120, 1535, 70, 15, 52], [35040, 2880, 71, 15, 52], [35040, 1920, 75, 15, 52], [37920, 770, 61, 15, 52]],
                    480, 66, [30], False),
                _score_track('choir', '男高音', 'Tenor',
                    [[0, 770, 54, 15, 52], [0, 770, 58, 15, 52], [960, 770, 54, 15, 52], [960, 770, 58, 15, 52], [1920, 770, 54, 15, 52], [1920, 770, 58, 15, 52], [3360, 385, 53, 15, 52], [3360, 385, 58, 15, 52], [3840, 770, 58, 15, 52], [3840, 770, 61, 15, 52], [4800, 770, 58, 15, 52], [4800, 770, 63, 15, 52], [5760, 770, 58, 15, 52], [5760, 770, 61, 15, 52], [7200, 385, 53, 15, 52], [7680, 770, 61, 15, 52], [8640, 770, 58, 15, 52], [9600, 770, 61, 15, 52], [10560, 770, 61, 15, 52], [11520, 770, 58, 15, 52], [12480, 480, 56, 15, 52], [12480, 480, 61, 15, 52], [12960, 385, 54, 15, 52], [12960, 385, 58, 15, 52], [13440, 480, 53, 15, 52], [13440, 960, 56, 15, 52], [13920, 2785, 51, 15, 52], [14400, 385, 54, 15, 52], [14880, 960, 53, 15, 52], [15840, 865, 54, 15, 52], [17280, 385, 53, 15, 52], [17280, 385, 56, 15, 52], [17760, 770, 54, 15, 52], [17760, 770, 58, 15, 52], [18720, 770, 54, 15, 52], [18720, 770, 58, 15, 52], [19680, 770, 56, 15, 52], [19680, 770, 59, 15, 52], [20640, 770, 56, 15, 52], [20640, 770, 59, 15, 52], [22080, 1150, 56, 15, 52], [22080, 1150, 59, 15, 52], [23520, 1150, 57, 15, 52], [23520, 1150, 59, 15, 52], [24960, 385, 57, 15, 52], [24960, 385, 59, 15, 52], [25440, 770, 55, 15, 52], [25440, 770, 59, 15, 52], [26400, 385, 55, 15, 52], [26400, 385, 59, 15, 52], [27360, 1535, 59, 15, 52], [27360, 1535, 63, 15, 52], [29280, 1150, 61, 15, 52], [29280, 1150, 64, 15, 52], [30720, 385, 61, 15, 52], [30720, 385, 64, 15, 52], [31200, 1920, 63, 15, 52], [33120, 770, 65, 15, 52], [34080, 770, 63, 15, 52], [34080, 770, 66, 15, 52], [35040, 2880, 56, 15, 52], [35040, 2880, 66, 15, 52], [37920, 480, 61, 15, 52], [37920, 770, 65, 15, 52], [38400, 385, 59, 15, 52]],
                    480, 66, [31], False),
                _score_track('choir', '男低音', 'Bass',
                    [[0, 770, 42, 15, 52], [0, 770, 54, 15, 52], [960, 770, 39, 15, 52], [960, 770, 51, 15, 52], [1920, 770, 37, 15, 52], [1920, 770, 49, 15, 52], [3360, 240, 34, 15, 52], [3360, 240, 46, 15, 52], [3600, 190, 37, 15, 52], [3600, 190, 49, 15, 52], [3840, 480, 42, 15, 52], [3840, 480, 54, 15, 52], [4320, 385, 41, 15, 52], [4320, 385, 53, 15, 52], [4800, 770, 39, 15, 52], [4800, 770, 51, 15, 52], [5760, 770, 37, 15, 52], [5760, 770, 49, 15, 52], [7200, 385, 34, 15, 52], [7200, 385, 46, 15, 52], [7680, 770, 37, 15, 52], [7680, 770, 49, 15, 52], [8640, 770, 39, 15, 52], [8640, 770, 51, 15, 52], [9600, 770, 37, 15, 52], [9600, 770, 49, 15, 52], [10560, 770, 34, 15, 52], [10560, 770, 46, 15, 52], [11520, 770, 39, 15, 52], [11520, 770, 51, 15, 52], [12480, 480, 41, 15, 52], [12480, 480, 53, 15, 52], [12960, 385, 42, 15, 52], [12960, 385, 54, 15, 52], [13440, 1440, 44, 15, 52], [13440, 480, 53, 15, 52], [13920, 2785, 51, 15, 52], [14880, 960, 46, 15, 52], [15840, 865, 47, 15, 52], [17280, 385, 49, 15, 52], [17760, 770, 49, 15, 52], [18720, 770, 51, 15, 52], [19680, 770, 52, 15, 52], [20640, 770, 47, 15, 52], [22080, 480, 52, 15, 52], [22560, 480, 51, 15, 52], [23040, 385, 52, 15, 52], [23520, 960, 53, 15, 52], [24480, 385, 52, 15, 52], [24960, 385, 51, 15, 52], [25440, 770, 52, 15, 52], [26400, 385, 47, 15, 52], [27360, 1535, 44, 15, 52], [27360, 1535, 56, 15, 52], [29280, 960, 43, 15, 52], [29280, 960, 55, 15, 52], [30240, 385, 44, 15, 52], [30240, 385, 56, 15, 52], [30720, 385, 46, 15, 52], [30720, 385, 58, 15, 52], [31200, 1920, 47, 15, 52], [31200, 1440, 59, 15, 52], [33120, 1920, 48, 15, 52], [35040, 3455, 49, 15, 52]],
                    480, 66, [32], False),
                _score_track('strings', '弦乐应答', 'String response',
                    [[17760, 960, 37, 15, 48], [17760, 960, 49, 15, 48], [17760, 1535, 54, 15, 48], [17760, 1535, 58, 15, 48], [17760, 960, 61, 15, 48], [18720, 960, 39, 15, 48], [18720, 960, 51, 15, 48], [18720, 960, 63, 15, 48], [19680, 960, 40, 15, 48], [19680, 960, 52, 15, 48], [19680, 1535, 56, 15, 48], [19680, 1730, 59, 15, 48], [19680, 960, 64, 15, 48], [20640, 770, 35, 15, 48], [20640, 770, 47, 15, 48], [22080, 480, 52, 15, 48], [22080, 1440, 56, 15, 48], [22080, 4705, 59, 15, 48], [22080, 480, 64, 15, 48], [22560, 480, 51, 15, 48], [22560, 480, 63, 15, 48], [23040, 480, 52, 15, 48], [23040, 480, 64, 15, 48], [23520, 960, 53, 15, 48], [23520, 1920, 57, 15, 48], [23520, 960, 65, 15, 48], [24480, 480, 52, 15, 48], [24480, 480, 64, 15, 48], [24960, 480, 51, 15, 48], [24960, 480, 63, 15, 48], [25440, 960, 52, 15, 48], [25440, 1345, 55, 15, 48], [25440, 960, 64, 15, 48], [26400, 385, 47, 15, 48], [37920, 720, 73, 15, 48], [38640, 190, 85, 15, 48]],
                    480, 66, [21, 22, 23, 24, 25], False),
                _score_track('brass', '长号', 'Trombones',
                    [[19680, 1535, 52, 15, 57], [19680, 1535, 56, 15, 57], [19680, 1535, 59, 15, 57], [25440, 1345, 52, 15, 57], [25440, 1345, 55, 15, 57], [25440, 1345, 59, 15, 57], [27360, 1920, 59, 15, 57], [27360, 1920, 63, 15, 57], [29280, 1150, 61, 15, 57], [29280, 1150, 64, 15, 57]],
                    480, 66, [15], False),
            ], '35a59329ab8f1f86ec2602bb5293b9fbddc694e512aafa00e310cb8da237f302', 'https://gustavmahler.com/site/midi/symphony2/5th-movement-Im-Tempo-Des-Scherzo-Wild-H.midi'),
        _score_scene(5, 4, '复活颂歌：合唱、铜管与管风琴', 'Resurrection hymn: chorus, brass and organ',
            '合唱高低声部、铜管和声、弦乐与管风琴分轨。管风琴使用通用 MIDI 教堂风琴；未将该音色等同于柏林爱乐大厅的真实管风琴。',
            'Upper and lower chorus, brass harmony, strings and organ have separate tracks. General MIDI church organ approximates the instrument rather than reproducing the Philharmonie organ.',
            70, 2830.5, 2886.5, 729, 742, 480, [4, 4], [
                _score_track('choir', '合唱高声部', 'Upper chorus',
                    [[0, 1150, 72, 95, 52], [0, 960, 74, 95, 52], [960, 385, 75, 95, 52], [1440, 385, 72, 95, 52], [1440, 385, 77, 95, 52], [1920, 1150, 70, 95, 52], [1920, 1150, 73, 95, 52], [1920, 960, 79, 95, 52], [2880, 385, 77, 95, 52], [3360, 385, 70, 95, 52], [3360, 385, 73, 95, 52], [3360, 385, 76, 95, 52], [3840, 1215, 72, 111, 52], [3840, 640, 79, 111, 52], [3840, 640, 82, 111, 52], [4480, 575, 77, 111, 52], [4480, 575, 81, 111, 52], [5120, 575, 72, 111, 52], [5120, 575, 76, 111, 52], [5120, 575, 80, 111, 52], [5760, 770, 72, 111, 52], [5760, 770, 75, 111, 52], [5760, 770, 79, 111, 52], [6720, 770, 71, 111, 52], [6720, 770, 75, 111, 52], [6720, 770, 78, 111, 52], [7680, 1920, 70, 111, 52], [7680, 1920, 75, 111, 52], [7680, 1920, 77, 111, 52], [9600, 1535, 74, 127, 52], [9600, 960, 79, 127, 52], [9600, 1535, 82, 127, 52], [10560, 770, 77, 127, 52], [11520, 770, 75, 127, 52]],
                    480, 70, [29, 30], False),
                _score_track('choir', '合唱低声部', 'Lower chorus',
                    [[0, 1150, 58, 95, 52], [0, 1150, 68, 95, 52], [1440, 385, 58, 95, 52], [1440, 385, 68, 95, 52], [1920, 960, 52, 95, 52], [1920, 960, 67, 95, 52], [2880, 385, 53, 95, 52], [2880, 385, 65, 95, 52], [3360, 385, 55, 95, 52], [3360, 385, 64, 95, 52], [3840, 1215, 56, 111, 52], [3840, 1215, 60, 111, 52], [3840, 640, 67, 111, 52], [3840, 640, 70, 111, 52], [4480, 575, 65, 111, 52], [4480, 575, 69, 111, 52], [5120, 575, 56, 111, 52], [5120, 575, 60, 111, 52], [5120, 575, 64, 111, 52], [5120, 575, 68, 111, 52], [5760, 770, 57, 111, 52], [5760, 770, 60, 111, 52], [5760, 770, 63, 111, 52], [5760, 770, 67, 111, 52], [6720, 770, 57, 111, 52], [6720, 770, 59, 111, 52], [6720, 770, 63, 111, 52], [6720, 770, 66, 111, 52], [7680, 3455, 58, 111, 52], [7680, 1920, 63, 111, 52], [7680, 1920, 65, 111, 52], [9600, 1535, 68, 127, 52], [11520, 770, 51, 111, 52], [11520, 770, 63, 111, 52], [11520, 770, 67, 127, 52], [11520, 770, 75, 127, 52]],
                    480, 70, [31, 32], False),
                _score_track('brass', '铜管和声', 'Brass harmony',
                    [[0, 1535, 46, 47, 61], [0, 1535, 58, 47, 61], [0, 385, 62, 47, 61], [0, 1535, 68, 47, 61], [0, 1535, 72, 47, 61], [0, 770, 74, 79, 61], [960, 385, 75, 79, 61], [1440, 385, 77, 79, 61], [1920, 770, 40, 47, 61], [1920, 770, 52, 47, 61], [1920, 1535, 70, 47, 61], [1920, 1535, 73, 47, 61], [1920, 770, 79, 79, 61], [2880, 385, 41, 47, 61], [2880, 385, 53, 47, 61], [2880, 385, 77, 79, 61], [3360, 385, 43, 47, 61], [3360, 385, 55, 47, 61], [3360, 385, 76, 79, 61], [3840, 1535, 44, 47, 61], [3840, 1535, 56, 47, 61], [3840, 2690, 60, 79, 61], [3840, 575, 67, 79, 61], [3840, 575, 70, 79, 61], [3840, 2690, 72, 47, 61], [3840, 575, 79, 79, 61], [3840, 575, 82, 79, 61], [4480, 575, 65, 79, 61], [4480, 575, 69, 79, 61], [4480, 575, 77, 79, 61], [4480, 575, 81, 79, 61], [5120, 575, 64, 79, 61], [5120, 575, 68, 79, 61], [5120, 575, 76, 79, 61], [5120, 575, 80, 79, 61], [5760, 1535, 45, 47, 61], [5760, 1535, 57, 47, 61], [5760, 1535, 63, 79, 61], [5760, 770, 67, 79, 61], [5760, 1535, 75, 47, 61], [5760, 770, 79, 47, 61], [6720, 770, 59, 79, 61], [6720, 770, 66, 79, 61], [6720, 770, 71, 47, 61], [6720, 770, 78, 47, 61], [7680, 3455, 46, 79, 61], [7680, 3455, 58, 79, 61], [7680, 1535, 63, 79, 61], [7680, 770, 65, 79, 61], [7680, 1535, 70, 95, 61], [7680, 1535, 75, 95, 61], [7680, 770, 77, 95, 61], [8640, 385, 67, 79, 61], [8640, 385, 79, 95, 61], [9120, 385, 68, 79, 61], [9120, 385, 80, 95, 61], [9600, 1535, 56, 79, 61], [9600, 1535, 62, 79, 61], [9600, 770, 67, 79, 61], [9600, 1535, 68, 95, 61], [9600, 1535, 74, 95, 61], [9600, 770, 79, 95, 61], [10560, 770, 65, 79, 61], [10560, 770, 77, 95, 61], [11520, 385, 39, 79, 61], [11520, 385, 51, 79, 61], [11520, 385, 55, 79, 61], [11520, 385, 58, 79, 61], [11520, 385, 63, 79, 61], [11520, 385, 67, 95, 61], [11520, 385, 70, 95, 61], [11520, 385, 75, 95, 61], [19200, 1150, 70, 95, 61], [19200, 1150, 82, 95, 61], [20640, 385, 63, 95, 61], [20640, 385, 75, 95, 61], [21120, 385, 65, 95, 61], [21120, 385, 77, 95, 61], [21600, 385, 67, 95, 61], [21600, 385, 79, 95, 61], [22080, 385, 68, 95, 61], [22080, 385, 80, 95, 61], [22560, 385, 70, 95, 61], [22560, 385, 82, 95, 61], [23040, 960, 84, 95, 61], [24000, 2495, 82, 95, 61]],
                    480, 70, [13, 14, 15, 16, 17], False),
                _score_track('strings', '弦乐全奏', 'Tutti strings',
                    [[0, 1535, 46, 127, 48], [0, 1535, 58, 127, 48], [0, 770, 74, 127, 48], [0, 770, 80, 127, 48], [0, 1535, 84, 127, 48], [0, 1535, 86, 127, 48], [0, 770, 92, 127, 48], [960, 385, 75, 127, 48], [960, 385, 79, 127, 48], [960, 385, 91, 127, 48], [1440, 385, 77, 127, 48], [1440, 385, 89, 127, 48], [1920, 960, 40, 127, 48], [1920, 960, 52, 127, 48], [1920, 770, 79, 127, 48], [1920, 770, 82, 127, 48], [1920, 770, 85, 127, 48], [1920, 770, 94, 127, 48], [2880, 385, 41, 127, 48], [2880, 385, 53, 127, 48], [2880, 385, 77, 127, 48], [2880, 385, 80, 127, 48], [2880, 385, 85, 127, 48], [2880, 385, 92, 127, 48], [3360, 385, 43, 127, 48], [3360, 385, 55, 127, 48], [3360, 385, 76, 127, 48], [3360, 385, 79, 127, 48], [3360, 385, 85, 127, 48], [3360, 385, 91, 127, 48], [3840, 1535, 32, 127, 48], [3840, 1535, 44, 127, 48], [3840, 1535, 72, 127, 48], [3840, 1535, 84, 127, 48], [3840, 1535, 96, 127, 48], [5760, 1535, 33, 127, 48], [5760, 1535, 45, 127, 48], [5760, 385, 72, 127, 48], [5760, 385, 84, 127, 48], [5760, 385, 96, 127, 48], [6240, 770, 74, 127, 48], [6240, 770, 86, 127, 48], [6240, 770, 98, 127, 48], [7200, 2015, 75, 127, 48], [7200, 2015, 87, 127, 48], [7200, 2015, 99, 127, 48], [7680, 3455, 34, 127, 48], [7680, 3455, 46, 127, 48], [9600, 1535, 70, 127, 48], [9600, 1535, 82, 127, 48], [9600, 1535, 94, 127, 48], [11520, 3455, 39, 111, 48], [11520, 3455, 51, 111, 48], [11520, 1535, 75, 111, 48], [11520, 1535, 79, 111, 48], [11520, 1535, 82, 111, 48], [11520, 1535, 87, 111, 48], [13440, 1535, 77, 111, 48], [13440, 1535, 80, 111, 48], [13440, 1535, 84, 111, 48], [13440, 1535, 89, 111, 48], [15360, 3455, 39, 111, 48], [15360, 3455, 51, 111, 48], [15360, 1535, 75, 111, 48], [15360, 1535, 79, 111, 48], [15360, 1535, 82, 111, 48], [15360, 1535, 87, 111, 48], [17280, 1535, 72, 111, 48], [17280, 1535, 77, 111, 48], [17280, 1535, 80, 111, 48], [17280, 1535, 84, 111, 48], [17280, 1535, 89, 111, 48], [19200, 3455, 39, 95, 48], [19200, 3455, 51, 95, 48], [19200, 1535, 70, 111, 48], [19200, 1535, 75, 111, 48], [19200, 1535, 79, 111, 48], [19200, 1535, 82, 111, 48], [19200, 1535, 87, 111, 48], [21120, 1535, 68, 111, 48], [21120, 1535, 72, 111, 48], [21120, 1535, 77, 111, 48], [21120, 1535, 80, 111, 48], [21120, 1535, 84, 111, 48], [23040, 3455, 39, 79, 48], [23040, 3455, 51, 79, 48], [23040, 1535, 70, 111, 48], [23040, 1535, 75, 111, 48], [23040, 1535, 79, 111, 48], [23040, 1535, 82, 111, 48], [24960, 1535, 68, 111, 48], [24960, 1535, 72, 111, 48], [24960, 1535, 77, 111, 48], [24960, 1535, 80, 111, 48]],
                    480, 70, [21, 22, 23, 24, 25], False),
                _score_track('organ', '管风琴', 'Pipe organ',
                    [[11520, 14975, 39, 111, 19], [11520, 14975, 51, 111, 19], [11520, 1535, 63, 111, 19], [11520, 1535, 67, 111, 19], [11520, 1535, 70, 111, 19], [11520, 1535, 75, 111, 19], [13440, 1535, 65, 111, 19], [13440, 1535, 68, 111, 19], [13440, 1535, 72, 111, 19], [13440, 1535, 77, 111, 19], [15360, 1535, 63, 111, 19], [15360, 1535, 67, 111, 19], [15360, 1535, 70, 111, 19], [15360, 1535, 75, 111, 19], [17280, 1535, 65, 111, 19], [17280, 1535, 68, 111, 19], [17280, 1535, 72, 111, 19], [17280, 1535, 77, 111, 19], [19200, 1920, 63, 111, 19], [19200, 1920, 67, 111, 19], [19200, 1920, 70, 111, 19], [19200, 1920, 75, 111, 19], [21120, 1920, 65, 111, 19], [21120, 1920, 68, 111, 19], [21120, 1920, 72, 111, 19], [23040, 1920, 63, 111, 19], [23040, 1920, 67, 111, 19], [23040, 1920, 70, 111, 19], [24960, 1535, 60, 111, 19], [24960, 1535, 65, 111, 19], [24960, 1535, 68, 111, 19]],
                    480, 70, [20], False),
                _score_track('perc', '钟琴与钟（源补充声部）', 'Glockenspiel and bells (source auxiliary part)',
                    [[11520, 1150, 47, 111, 14], [12960, 1250, 53, 111, 14], [14400, 1345, 59, 111, 14], [15840, 1150, 47, 111, 14], [17280, 1150, 53, 111, 14], [18720, 1250, 59, 103, 14], [20160, 1345, 53, 95, 14], [21600, 2590, 59, 87, 14], [24480, 1250, 47, 79, 14], [25920, 960, 53, 71, 14]],
                    480, 70, [29], False),
            ], '35a59329ab8f1f86ec2602bb5293b9fbddc694e512aafa00e310cb8da237f302', 'https://gustavmahler.com/site/midi/symphony2/5th-movement-Im-Tempo-Des-Scherzo-Wild-H.midi'),
    ],
}

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

    (180,
     193,
     'Reh. 11+1',
     2,
     '#dc2626',
     ['m1-totenfeier-march'],
     ['strings', 'winds', 'brass'],
     '原速中的强弱交替：尖锐起音与快速消退',
     'Tempo I Contrasts: Accented Attacks and Rapid Recession',
     '排练号11之后的重音与强弱对照',
     'Accents and dynamic contrasts after Rehearsal 11',
     '弦乐、木管与铜管从重音和骤强中推进，随后迅速收拢',
     'Strings, winds and brass advance through accented attacks and forte surges before rapidly receding',
     '短暂强奏之后，弱奏织体重新显露；勿把整个段落听成持续的极强',
     'Soft textures reappear after the forceful attacks; the paragraph is not uniformly fortissimo',
     '公开总谱第22–24页在排练号11后标示Tempo I及fp、ff与弱奏对比。旧导览把本段标为排练号12并称为极强风暴；排练号12实际稍后出现。',
     'Published score pages 22–24 show Tempo I with fp, ff and soft contrasts after Rehearsal 11. This corrects '
     'the inherited Rehearsal 12 label and uniformly thunderous description.',
     {'strings': '重音推进后迅速消退', 'winds': '强奏应答与弱奏间隙形成对照', 'brass': '参与重音与强奏，随后收拢'},
     {'strings': 'Accented motion rapidly recedes',
      'winds': 'Forceful responses contrast with soft intervals',
      'brass': 'Brass join the accents and forte before withdrawing'},
     '比较重音后的消退与下一次强奏起音',
     'Compare the recession after each accent with the next forceful attack'),

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

    (254,
     266,
     'Reh. 16',
     2,
     '#0284c7',
     ['m1-rising-cry'],
     ['strings', 'winds'],
     '展开部慢板回望：弱奏低音弦乐与英国管独白',
     'Slow Development Recollection: Quiet Lower Strings and English Horn',
     '从低音弦乐弱奏到英国管的抒情呼吸',
     'Quiet lower strings opening into an English-horn cantilena',
     '大提琴与低音提琴以较少人数、弱力度开始；总谱标示“Sehr langsam beginnend”',
     'Reduced cello and bass forces begin softly under the instruction “Sehr langsam beginnend”',
     '英国管随后以弱奏歌唱，高音弦乐保持极弱的透明背景',
     'The English horn subsequently sings softly while upper strings remain hushed',
     '公开出版总谱第32页表明，此处是非常缓慢开始的弱奏段落。它并非旧导览所称的降E小调全奏风暴；定位保留其安静音响，不移往强音来满足能量门槛。',
     'The published score on page 32 shows a soft passage beginning very slowly. This replaces the inherited '
     'description of an E-flat-minor tutti storm; the quiet musical location is retained.',
     {'strings': '较少人数的大提琴与低音提琴弱奏，随后由极弱高音弦乐衬托', 'winds': '英国管在弱奏中展开抒情独白'},
     {'strings': 'Reduced cellos and basses begin softly; hushed upper strings later provide a backdrop',
      'winds': 'English horn unfolds a quiet cantilena'},
     '注意缓慢起句和低音弦乐人数减少后的透明音色',
     'Hear the very slow opening and the transparency of the reduced lower strings'),

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

    (291,
     304,
     'Reh. 18',
     2,
     '#881337',
     ['m1-totenfeier-march'],
     ['brass', 'strings'],
     '速度骤变：更为激动的弦乐与铜管高潮',
     'Sudden Acceleration: More Agitated Strings and Brass Climax',
     'a tempo subito，Molto più mosso',
     'a tempo subito, Molto più mosso',
     '弦乐与铜管在排练号18以极强（fff）推进',
     'Strings and brass drive forward in fff at Rehearsal 18',
     '疾速的推动和强烈重音构成紧张背景',
     'Urgent motion and forceful accents form the tense backdrop',
     '公开总谱第36页标示“a tempo subito. Molto più mosso”，并有fff弦乐与铜管。旧导览的排练号17和沉重慢行描述已更正；声学能量仍按实测值检查。',
     'Published score page 36 marks “a tempo subito. Molto più mosso” with fff strings and brass. This corrects '
     'the inherited Rehearsal 17 and heavy slow-march description; measured acoustic energy remains '
     'independently checked.',
     {'strings': '极强快速推进', 'brass': '极强重音与弦乐共同推动高潮'},
     {'strings': 'Very forceful, urgent motion',
      'brass': 'Very forceful accents drive the climax with the strings'},
     '听速度骤变后弦乐与铜管共同推进的力量',
     'Hear strings and brass propel the sudden increase in motion'),

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

    (142,
     175,
     'Reh. 10',
     2,
     '#6366f1',
     ['m5-resurrection-chorale', 'm5-dies-irae'],
     ['winds', 'brass', 'strings'],
     '重新宽广：低音铜管与低音大管的弱奏众赞歌',
     'Broadly Again: Quiet Low-Brass and Contrabassoon Chorale',
     '总休止后，低音众赞歌从弱奏逐渐展开',
     'A quiet low-register chorale after the general pause, gradually broadening',
     '低音大管以极弱、长号与大号以弱奏呈示宽广线条；总谱标示“Wieder sehr breit”',
     'Contrabassoon, trombones and tuba begin softly under “Wieder sehr breit”',
     '弦乐随后加入极弱拨弦；后续段落逐渐走向排练号11的强奏',
     'Hushed string pizzicati enter later; the following paragraph builds toward forte at Rehearsal 11',
     '公开出版总谱第148页在总休止之后标示弱奏低音众赞歌，而非原导览所称的极强铜管爆发。听各声部怎样从稀疏音响逐渐集结；后续力度变化不可等同于整个区间持续极强。',
     'Published score page 148 shows a quiet low-register chorale after a general pause, correcting the '
     'inherited description of a fortissimo brass eruption. Follow the gradual gathering of voices rather than '
     'treating the entire interval as a sustained climax.',
     {'winds': '低音大管以极弱支撑低音众赞歌', 'brass': '长号与大号从弱奏开始，逐渐拓展线条', 'strings': '弦乐稍后以极弱拨弦加入'},
     {'winds': 'Contrabassoon supports the low chorale very softly',
      'brass': 'Trombones and tuba begin quietly and gradually broaden the line',
      'strings': 'Strings later enter with hushed pizzicati'},
     '分辨总休止后的弱奏低音和后来逐渐增强的众赞歌',
     'Distinguish the quiet low-register restart after the general pause from the subsequent growth'),

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



# Existing player-facing text retained here so compilation needs no previous data.js.
PLAYER_COPY = {'metadata': {'work': 'Gustav Mahler · Symphony No. 2 in C minor ("Resurrection" / Auferstehung)',
              'shortWork': 'Mahler 2',
              'composer': 'Gustav Mahler (1860–1911)',
              'composer_zh': '古斯塔夫·马勒 (1860–1911)',
              'conductor': 'Sir Simon Rattle',
              'orchestra': 'Berliner Philharmoniker',
              'recordingLabel': 'Rattle · Berliner Philharmoniker (declared 2010 source; unverified)',
              'badge': 'EMI 2010',
              'edition': 'Published score references; Junji Miki MIDI digitization (critical edition '
                         'unverified)',
              'storageKey': 'mahler-two-atlas-v1',
              'slug': 'mahler-two',
              'totalStages': 191,
              'soloists': 'Kate Royal (Soprano) · Magdalena Kožená (Mezzo-Soprano)',
              'chorus': 'Rundfunkchor Berlin (Simon Halsey)',
              'venue': 'Philharmonie, Berlin',
              'sampleRate': 44100,
              'pageTitle_zh': 'Mahler 2 · 全景声部与复调导览 (Sir Simon Rattle · BPO)',
              'pageTitle_en': 'Mahler 2 · Full-Score Listening Guide (Sir Simon Rattle · BPO)',
              'heroSubtitle_zh': ' · 五乐章原声 · 动机积木 · 复调全景导览',
              'heroSubtitle_en': ' · 5-Movement Audio · Motif Anatomy · Full-Score Guide',
              'footerTitle_zh': 'Mahler 2 · Sir Simon Rattle / Berliner Philharmoniker (EMI 2010)',
              'footerTitle_en': 'Mahler 2 · Sir Simon Rattle / Berliner Philharmoniker (EMI 2010)',
              'timingRef_zh': '色度对齐的估计定位 · 小节轴待核对',
              'timingRef_en': 'Estimated chroma alignment · bar axis requires review',
              'stringsLabel_zh': '弦乐五部',
              'stringsLabel_en': 'Strings',
              'windsLabel_zh': '木管声部',
              'windsLabel_en': 'Woodwinds',
              'hornsLabel_zh': '圆号声部',
              'hornsLabel_en': 'Horns',
              'percLabel_zh': '打击与合唱',
              'percLabel_en': 'Perc & Chorus',
              'waveLabel_zh': '拉特尔 / 柏林爱乐 原声波形 · 点击或拖动定位',
              'waveLabel_en': 'Rattle / BPO Recording RMS · Click or drag to seek',
              'settingsIntro_zh': '内置五乐章音轨，来源标注为拉特尔与柏林爱乐的2010年录音。第一乐章比乐团官方目录时长短102秒，版本及剪辑情况尚待核实。可在此替换为已确认来源的本地音轨。',
              'settingsIntro_en': 'The five bundled tracks are attributed to Rattle and the BPO in '
                                  '2010. Movement I is 102 seconds shorter than the orchestra’s '
                                  'official catalog timing; its edition and editing history remain '
                                  'unverified. You may substitute verified local audio here.',
              'scoreNote_zh': '保留任务指定的小节轴；来源MIDI的节拍网格与部分小节、排练号不一致，不能视为批判版逐小节校订。',
              'scoreNote_en': 'The requested atlas bar axis is retained; source MIDI meter and some '
                              'rehearsal labels differ, so this is not a critical-edition bar-by-bar '
                              'audit.',
              'dtwNote_zh': '音频色度与来源MIDI进行自动对齐；声学采样间隔不等于总谱定位误差，未经人工逐小节校准。',
              'dtwNote_en': 'Automatic audio-chroma / source-MIDI alignment; analysis frame spacing '
                            'does not establish score-timing accuracy. Manual bar-by-bar calibration '
                            'remains outstanding.',
              'synthIntro_zh': '按声部聆听来源MIDI的完整短乐句，并在钢琴卷帘中静音或独奏。原声跳转采用自动估计定位；下载文件依次包含本乐章全部示例。',
              'synthIntro_en': 'Hear complete short phrases from the source MIDI; mute or solo voices '
                               'in the piano roll. Recording jumps use estimated alignment; the '
                               'download includes all scenes for this movement in sequence.',
              'glossaryTitle_zh': '马勒第二交响曲《复活》聆听小词典',
              'glossaryTitle_en': 'Mahler Symphony No. 2 Listening Glossary',
              'threadsTitle_zh': '《复活》全景交响线索',
              'threadsTitle_en': "Symphonic Threads of the 'Resurrection' Symphony",
              'finaleComplete_zh': '全曲结束。赞美诗与钟声响彻天际！点击下方按钮回到终曲《复活》辉煌高潮，再次重温宇宙新生的永恒时刻！',
              'finaleComplete_en': 'Symphony complete. Click below to return to the grand Resurrection '
                                   'climax and relive the apotheosis!',
              'finaleCta_zh': '重听终曲《复活》管风琴与全奏高潮',
              'finaleCta_en': 'Relisten to Finale Resurrection Apotheosis',
              'sourcesHeading1_zh': '总谱版本考据：卡普兰基金会 / 国际马勒学会批判版本 (Kaplan / IGMG Edition)',
              'sourcesHeading1_en': 'Score Edition: Kaplan Foundation / IGMG Critical Edition',
              'sourcesBody_zh': 'MIDI乐句取自Junji Miki的数字化版本，并抽查公开出版总谱。卡普兰/国际马勒学会批判版的逐音逐小节核对尚未完成。',
              'sourcesBody_en': 'MIDI phrases derive from Junji Miki’s digitization, with spot checks '
                                'against a public published score. Note-by-note and bar-by-bar '
                                'verification against the Kaplan/IGMG critical edition remains '
                                'incomplete.',
              'sourcesHeading2_zh': '演绎版本解析：西蒙·拉特尔爵士指挥柏林爱乐乐团 (EMI Classics 2010)',
              'sourcesHeading2_en': 'Performance: Sir Simon Rattle conducting the Berliner '
                                    'Philharmoniker (2010)',
              'sourcesInterp_zh': '音轨来源标注为2010年拉特尔与柏林爱乐录音，但文件只有编码器标签。乐团官方目录第一乐章为24分16秒，内置文件为22分34秒，相差102秒；现有定位只适用于内置文件，不能视为完整官方录音的认证。',
              'sourcesInterp_en': 'The files are attributed to the 2010 Rattle/BPO recording but '
                                  'contain only encoder tags. The orchestra’s official catalog lists '
                                  'Movement I at 24:16, versus the bundled 22:34, a 102-second '
                                  'discrepancy. Alignment applies to the bundled files; the complete '
                                  'official release is not authenticated.'},
 'overview': {'oneSentence': '在第一乐章英雄葬礼的巨大深渊之上，走过兰德勒回忆、世俗荒诞与原初神圣之光，最终在无伴奏弱音合唱与全宇宙的管风琴轰鸣中完成终极复活。',
              'parts': [{'part': 'I',
                         'movements': [1],
                         'label': '葬礼之祭 (Totenfeier)',
                         'label_en': 'Funeral Rites (Totenfeier)',
                         'listenFor': '第一乐章独占第一部分；严酷的C小调附点进行曲步伐与泰坦英雄遗体的安葬，结尾总谱指示必须静默五分钟。',
                         'listenFor_en': 'Movement 1 stands alone as Part I; stern C minor funeral '
                                         'march and the solemn burial of the titan, followed by '
                                         "Mahler's mandatory five-minute silence."},
                        {'part': 'II',
                         'movements': [2, 3],
                         'label': '回忆与世俗迷局',
                         'label_en': 'Retrospective Memory & Worldly Absurdity',
                         'listenFor': '降A大调兰德勒舞步的温柔旧梦，与圣安东尼向鱼传道的荒诞旋涡交织，直至绝望尖叫和弦（Aufschrei）。',
                         'listenFor_en': 'Gentle nostalgic recollections in the A-flat Ländler followed '
                                         'by the ceaseless Wunderhorn fish sermon, culminating in the '
                                         'shattering Scream of Despair.'},
                        {'part': 'III',
                         'movements': [4, 5],
                         'label': '原光与终极复活',
                         'label_en': 'Primal Light & Universal Resurrection',
                         'listenFor': '女低音独唱《原光》质朴虔诚的信仰，引出终曲末日审判的号角、无伴奏合唱《复活》与管风琴终极大合唱。',
                         'listenFor_en': 'Intimate spiritual longing in Urlicht yields to the vast '
                                         'apocalyptic fresco: offstage brass calls, whispered choral '
                                         'entry, and full pipe organ apotheosis.'}]},
 'threads': [{'id': 'dies-irae',
              'title': '末日天堑：《震怒之日》（Dies Irae）的四次化身',
              'title_en': "The Apocalyptic Sequence: Four Avatars of 'Dies Irae'",
              'summary': '中世纪天主教圣咏《震怒之日》在第一乐章作为展开部暗号吹响，在第五乐章化为长号的审判号角与死者进行曲的核心旋律。',
              'summary_en': "The medieval Dies Irae plainchant sounds in Movement I's development and "
                            'becomes the central judgment call and Dead March in Movement V.',
              'milestones': [{'movement': 1,
                              'label': '展开部初现 (Bar 207)',
                              'label_en': 'Development Embryo (Bar 207)'},
                             {'movement': 5,
                              'label': '木管与拨弦宣告 (Bar 62)',
                              'label_en': 'Woodwind Proclamation (Bar 62)'},
                             {'movement': 5,
                              'label': '死者大进行曲 (Bar 220)',
                              'label_en': 'Grand Dead March (Bar 220)'}]},
             {'id': 'resurrection-chorale',
              'title': "救赎升华：复活众赞歌（Aufersteh'n）的从暗到明",
              'title_en': 'Redemptive Apotheosis: The Resurrection Chorale Arc',
              'summary': '从第四乐章《原光》微弱质朴的赤子之光，到第五乐章无伴奏合唱的极弱耳语，最终引向管弦乐与管风琴爆裂而出的宇宙神圣光明。',
              'summary_en': 'From the humble spiritual dawn of Urlicht to the whispered pppp choral '
                            'entry and the shattering full pipe organ apotheosis.',
              'milestones': [{'movement': 4,
                              'label': '《原光》铜管众赞歌 (Bar 4)',
                              'label_en': 'Urlicht Brass Chorale (Bar 4)'},
                             {'movement': 5,
                              'label': '铜管初次预示复活 (Bar 142)',
                              'label_en': 'First Brass Resurrection (Bar 142)'},
                             {'movement': 5,
                              'label': '合唱《复活》极弱进入 (Bar 472)',
                              'label_en': "Choir Aufersteh'n pppp (Bar 472)"},
                             {'movement': 5,
                              'label': '管风琴与全钟辉煌巅峰 (Bar 732)',
                              'label_en': 'Organ & Bells Climax (Bar 732)'}]},
             {'id': 'spatial-fernorchester',
              'title': '三维声场：后台乐队（Fernorchester）的旷野呼唤',
              'title_en': 'Spatial Dimension: Offstage Brass & Percussion Calls',
              'summary': '马勒利用柏林爱乐大厅的空间纵深，在第五乐章部署后台小号、圆号与定音鼓，创造出天籁、末日号角与大审判的神秘远近对比。',
              'summary_en': 'Utilizing the multi-dimensional acoustics of the Philharmonie, Mahler '
                            'places offstage brass to evoke calls from beyond the physical world.',
              'milestones': [{'movement': 5,
                              'label': '旷野中的呼喊者 (Bar 43)',
                              'label_en': 'The Crier in the Wilderness (Bar 43)'},
                             {'movement': 5,
                              'label': '大点名 (Der Grosse Appell, Bar 448)',
                              'label_en': 'The Great Summons (Bar 448)'}]}],
 'glossary': [{'term': 'Totenfeier (葬礼)',
               'term_en': 'Totenfeier (Funeral Rites)',
               'definition': '第一乐章的原名，源自波兰诗人亚当·密茨凯维奇的史诗《先人祭》。马勒在此为第一交响曲中的英雄巨擘举行安魂葬礼。',
               'definition_en': "Original title of Movement I, inspired by Adam Mickiewicz's epic "
                                'drama; Mahler buries the heroic titan of his First Symphony.'},
              {'term': 'Urlicht (原光)',
               'term_en': 'Urlicht (Primal Light)',
               'definition': '第四乐章标题，源自德意志民歌集《少年魔角》。代表灵魂深处对纯真天国源头之光的绝对笃信。',
               'definition_en': 'Title of Movement IV from Des Knaben Wunderhorn, expressing childlike, '
                                'unshakeable faith in the primal divine source of light.'},
              {'term': 'Fernorchester (后台乐队)',
               'term_en': 'Fernorchester (Offstage Band)',
               'definition': '放置在观众席外或舞台后方的声乐与管乐群（4支小号、4支圆号、定音鼓与钹），用以创造超越尘世的三维空间音效。',
               'definition_en': 'Ensemble of trumpets, horns, and percussion placed outside the hall to '
                                'create supernatural spatial depth and otherworldly acoustic distance.'},
              {'term': 'Der Grosse Appell (大点名)',
               'term_en': 'Der Grosse Appell (The Great Summons)',
               'definition': '终曲中四支后台小号与圆号在不同方向相继吹响的四音号角声，宣告全宇宙所有的死者接受唤醒。',
               'definition_en': 'The apocalyptic spatial trumpet and horn fanfare in the Finale '
                                'sounding the awakening of all departed souls.'},
              {'term': 'Dies Irae (震怒之日)',
               'term_en': 'Dies Irae (Day of Wrath)',
               'definition': '13世纪天主教安魂弥撒的格里高利圣咏旋律，在此象征不可逆转的死亡命运与末世审判。',
               'definition_en': '13th-century Gregorian chant sequence from the Requiem Mass, '
                                'symbolizing mortality and apocalyptic judgment.'},
              {'term': 'Aufschrei / Totengreif (绝望尖叫和弦)',
               'term_en': 'The Scream of Despair (Aufschrei)',
               'definition': '第三乐章与第五乐章爆发的降B小调极不协和全奏崩塌和弦，如同面对虚无宇宙时发自灵魂深处的绝望悲鸣。',
               'definition_en': 'A catastrophic, dissonant B-flat minor tutti explosion capturing '
                                'existential dread before the abyss.'}],
 'movements': [{'id': 1,
                'roman': 'I',
                'part': 'I',
                'navLabel': 'I. 葬礼 (Totenfeier)',
                'title': '第一乐章：庄严的快板（葬礼 / Totenfeier）',
                'title_en': 'I. Allegro maestoso — Funeral Rites (Totenfeier)',
                'shortEn': 'Allegro maestoso',
                'radarGroups': [['strings', '🎻', '弦乐五部'],
                                ['winds', '🪈', '木管声部'],
                                ['horns', '📯', '圆号声部'],
                                ['brass', '🎺', '重型铜管与小号'],
                                ['perc', '🥁', '打击乐与合唱/管风琴']],
                'question': '当英雄逝去，死亡究竟是一场毁灭还是通往永生的入口？',
                'form': '扩展奏鸣曲式（葬礼进行曲）',
                'form_en': 'Expanded Sonata-Allegro Form (Funeral March)',
                'mission': '抓住C小调低音提琴狂暴的宣叙调与附点踏步，追踪E大调彼岸幻象与《震怒之日》圣咏的初现。',
                'mission_en': 'Track the furious lower-string recitative and dotted march pulse, '
                              'contrasting against the luminous E major consolation theme and the '
                              'embryonic Dies Irae motif.',
                'introduction': '马勒第二交响曲的第一乐章《葬礼》（Totenfeier）原本是一首独立的交响音诗。乐章开篇由大提琴与低音提琴撕裂寂静，掀起一段阴冷而激昂的宣叙调。整部乐章以极其庞大的奏鸣曲式构建，充满严苛的葬礼步伐、半音阶悲叹与对生命意义的叩问。依照马勒总谱指示，第一乐章结束后必须保持至少五分钟的庄严静默。',
                'introduction_en': 'Originally conceived as an independent symphonic poem '
                                   "('Totenfeier'), this opening funeral rite erupts with furious "
                                   'lower-string recitatives. Across an immense sonata landscape, '
                                   'Mahler juxtaposes stern C minor funeral marches against '
                                   'transcendent E major visions, culminating in a subterranean '
                                   'collapse that demands a mandatory five-minute silence.',
                'color': '#dc2626'},
               {'id': 2,
                'roman': 'II',
                'part': 'II',
                'navLabel': 'II. 兰德勒 (Ländler)',
                'title': '第二乐章：中庸的行板，非常从容，切勿匆忙',
                'title_en': 'II. Andante moderato. Very leisurely. Never rush',
                'shortEn': 'Andante moderato',
                'radarGroups': [['strings', '🎻', '弦乐五部'],
                                ['winds', '🪈', '木管声部'],
                                ['horns', '📯', '圆号声部'],
                                ['brass', '🎺', '重型铜管与小号'],
                                ['perc', '🥁', '打击乐与合唱/管风琴']],
                'question': '逝者生前那些纯洁、幸福的往昔回忆，能否抚平死亡的创伤？',
                'form': "五部回旋曲式 (A-B-A'-B'-A'') / 兰德勒舞曲",
                'form_en': "Five-Part Rondo (A-B-A'-B'-A'') / Austrian Ländler",
                'mission': '在温柔摇曳的3/8拍中倾听大提琴对位线条，并在主题回归时跟看全弦乐轻巧的拨弦变奏与木管花彩。',
                'mission_en': 'Follow the warm cello counter-melody under the gentle 3/8 Ländler, and '
                              'enjoy the shimmering pizzicato string variation and woodwind filigree on '
                              'its return.',
                'introduction': '马勒形容第二乐章是“逝者生命中一段幸福的回忆”。音乐从第一乐章的严酷深渊中抽离，转入降A大调纯真典雅的奥地利兰德勒（Ländler）舞步。大提琴倾诉深情的对位副旋律，而中段的升G小调暴风雨急流带来短暂的不安，最终在晶莹剔透的全弦乐拨弦与竖琴中消融。',
                'introduction_en': "Mahler described this movement as 'a memory from the youth of him "
                                   "whom we carried to the grave.' Transported to idyllic A-flat major, "
                                   'delicate muted violins glide through an Austrian Ländler, countered '
                                   'by lyrical cello song and contrasting minor-key storm episodes '
                                   'before dissolving in ethereal pizzicati.',
                'color': '#10b981'},
               {'id': 3,
                'roman': 'III',
                'part': 'II',
                'navLabel': 'III. 谐谑曲 (Scherzo)',
                'title': '第三乐章：在平静流动的律动中（圣安东尼向鱼传道）',
                'title_en': "III. In quietly flowing motion (St. Anthony's Sermon to the Fishes)",
                'shortEn': 'In ruhig fließender Bewegung',
                'radarGroups': [['strings', '🎻', '弦乐五部'],
                                ['winds', '🪈', '木管声部'],
                                ['horns', '📯', '圆号声部'],
                                ['brass', '🎺', '重型铜管与小号'],
                                ['perc', '🥁', '打击乐与合唱/管风琴']],
                'question': '当世界退化为一场庸碌无意义的荒诞狂欢，心灵该如何面对虚无？',
                'form': '交响谐谑曲与双三声中部 (Scherzo with Double Trio)',
                'form_en': 'Symphonic Scherzo with Double Trio & Aufschrei Coda',
                'mission': '倾听单簧管永不停歇的《向鱼传道》盘旋旋律，并在乐章高潮迎接撕心裂肺的绝望尖叫和弦（Aufschrei）。',
                'mission_en': 'Track the perpetual-motion 16th-note swirl of the fish sermon in '
                              'clarinets and strings, culminating in the shattering B-flat minor Scream '
                              'of Despair (Aufschrei).',
                'introduction': '第三乐章以两记干脆刺耳的定音鼓独奏敲击开场，随后流淌出源自《少年魔角》歌曲《圣安东尼向鱼传道》的无休止3/8拍旋律。鱼儿们听道时无比感动，道毕依然浑浑噩噩。马勒借此讽刺世俗生活的空虚与徒劳。全曲在第465小节爆发出一记震惊寰宇的“绝望尖叫和弦”（Totengreif '
                                '/ Aufschrei），为末日审判埋下伏笔。',
                'introduction_en': 'Launched by startling solo timpani blows, this Scherzo adapts the '
                                   "Wunderhorn song 'St. Anthony's Sermon to the Fishes'. Sinuous, "
                                   'ceaseless woodwind figurations satirize the absurdity and senseless '
                                   'bustle of daily life, suddenly interrupted by the cataclysmic '
                                   "B-flat minor 'Scream of Despair' (Aufschrei).",
                'color': '#8b5cf6'},
               {'id': 4,
                'roman': 'IV',
                'part': 'III',
                'navLabel': 'IV. 原光 (Urlicht)',
                'title': '第四乐章：“原光”（Urlicht）——极其庄严而质朴',
                'title_en': 'IV. "Urlicht" (Primal Light). Very solemn, but simple',
                'shortEn': 'Urlicht',
                'radarGroups': [['strings', '🎻', '弦乐五部'],
                                ['winds', '🪈', '木管声部'],
                                ['horns', '📯', '圆号声部'],
                                ['brass', '🎺', '重型铜管与小号'],
                                ['perc', '🥁', '打击乐与合唱/管风琴']],
                'question': '面对人间的苦难与诱惑，纯真的赤子信仰能否叩开天国之门？',
                'form': '连贯通作 lied 形式 (Through-Composed Sacred Lied)',
                'form_en': 'Through-Composed Sacred Lied for Contralto and Orchestra',
                'mission': '在静止的时光中聆听女中音独唱“红玫瑰”的圣洁吟咏，伴随弱音铜管众赞歌的温暖抚慰。',
                'mission_en': "Surrender to the timeless serenity of the solo Contralto intoning 'O "
                              "Röschen rot!', embraced by the muted brass chorale and celestial violin "
                              'cantilena.',
                'introduction': '第三乐章结束后毫无间歇（attacca）直接进入第四乐章《原光》（Urlicht）。女低音/女中音独唱在至简的寂静中唱出“哦红玫瑰！”（O '
                                'Röschen '
                                'rot!）。铜管群奏出路德宗众赞歌般的宁静和声，抚慰人间最深重的苦难。这首歌曲表达了纯朴孩童般的笃定信仰：“我来自上帝，必将回归上帝！”',
                'introduction_en': "Flowing without pause (attacca) from the Scherzo, 'Urlicht' "
                                   "('Primal Light') strips away symphonic complexity. A solo Contralto "
                                   'gently intones verses from Des Knaben Wunderhorn, accompanied by '
                                   'solemn brass chorales and ethereal violin counterpoint, asserting '
                                   "unwavering faith: 'I am from God and will return to God!'",
                'color': '#f59e0b'},
               {'id': 5,
                'roman': 'V',
                'part': 'III',
                'navLabel': "V. 复活终曲 (Aufersteh'n)",
                'title': '第五乐章：谐谑曲速度，狂野迸发——“复活”终曲',
                'title_en': 'V. In the tempo of the Scherzo. Bursting forth wildly — "Resurrection"',
                'shortEn': 'Im Tempo des Scherzos',
                'radarGroups': [['strings', '🎻', '弦乐五部'],
                                ['winds', '🪈', '木管声部'],
                                ['horns', '📯', '圆号声部'],
                                ['brass', '🎺', '重型铜管与小号'],
                                ['perc', '🥁', '打击乐与合唱/管风琴']],
                'question': '末日终结之后，谁将被审判？谁能获得永恒的复活？',
                'form': '宏大末世狂想音画与合唱康塔塔 (Apocalyptic Fresco & Choral Cantata)',
                'form_en': 'Monumental Apocalyptic Fresco & Choral Cantata',
                'mission': '辨识旷野呼喊的后台铜管（Fernorchester），等待极弱pppp无伴奏合唱《复活》的进入，直至管风琴与全钟齐鸣的巅峰辉煌。',
                'mission_en': 'Follow the three-dimensional spatial dialogue between onstage orchestra '
                              'and offstage brass (Der Grosse Appell), the whispered pppp choral entry, '
                              'and the overwhelming organ and bell apotheosis.',
                'introduction': '长达35分钟的浩瀚终曲是整部交响曲的精神顶峰。谐谑曲绝望尖叫再度撕裂苍穹，随后荒野号角与《震怒之日》圣咏宣告末日降临。坟墓裂开，死者苏醒踏着庄严步伐前进。当人类全部站在虚空之中，没有惩罚，没有审判——柏林广播合唱团以极弱（pppp）的神秘音响唱出克洛普施托克的诗句：“复活，是的，你必将复活！”在女高音与女中音独唱的交织中，管风琴、钟声与全管弦乐爆发出宇宙重生的灿烂光芒！',
                'introduction_en': "The monumental 35-minute Finale represents Mahler's ultimate "
                                   'metaphysical triumph. After apocalyptic fanfares, offstage brass '
                                   'calls (The Great Summons), and the March of the Dead, absolute '
                                   "silence falls. The choir enters whispered pppp: 'Aufersteh'n, ja "
                                   "aufersteh'n wirst du!' Joined by soprano and contralto soloists, "
                                   'the music builds to an ecstatic apotheosis crowned by deep bells '
                                   'and full pipe organ.',
                'color': '#e11d48'}]}

def adapt_compiled_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Expose the existing app.js / engine.js schema without changing either player."""
    import copy
    ui = copy.deepcopy(PLAYER_COPY)
    payload.update({key: ui[key] for key in ("metadata", "overview", "threads", "glossary")})
    payload["work"] = ui["metadata"]["work"]
    payload["language"] = "zh-CN"
    payload["meta"]["performance"]["recording_identity_verified"] = False
    payload["meta"]["performance"]["movement_1_official_catalog_duration_sec"] = 1456
    payload["meta"]["performance"]["movement_1_duration_discrepancy_sec"] = 102
    payload["metadata"]["totalStages"] = sum(len(m["stages"]) for m in payload["movements"])
    payload["meta"]["performance"]["total_duration_sec"] = round(sum(m["duration_sec"] for m in payload["movements"]), 2)
    payload["meta"]["performance"]["total_bars"] = sum(m["bars"] for m in payload["movements"])
    payload["sources"] = [
        {"title": "Berliner Philharmoniker Recordings — official tracklist", "url": "https://www.berliner-philharmoniker-recordings.com/simon-rattle-the-berlin-years-tracklist?___store=rec_en", "note": "第一乐章目录时长24:16，内置音轨22:34，相差102秒 / Movement I catalog 24:16 vs bundled 22:34: 102 s discrepancy"},
        {"title": "Junji Miki — Mahler MIDI digitizations", "url": "https://gustavmahler.com/midi.html", "note": "来源MIDI，非批判版认证 / Source MIDI; not critical-edition certification"},
        {"title": "Published full score — first-edition UE reprint", "url": "https://imslp.org/wiki/Symphony_No.2_(Mahler,_Gustav)", "note": "公开总谱抽查 / Public score spot checks"},
        {"title": "International Gustav Mahler Society", "url": "https://www.gustav-mahler.org/", "note": "批判版逐音校验尚未完成 / Critical-edition note audit remains incomplete"}
    ]
    for m, labels in zip(payload["movements"], ui["movements"]):
        m.update(labels)
        m.update({"duration": m["duration_sec"], "barCount": m["bars"],
                  "audio": m["file"], "originalTitle": m["title_de"],
                  "timing": "inherited", "audioMatched": False,
                  "waveform": list(m["rms"])})
        for stage in m["stages"]:
            stage.update({"start": stage["sec"], "foreground": stage["fg"],
                          "foreground_en": stage["fg_en"], "background": stage["bg"],
                          "background_en": stage["bg_en"], "timeStatus": "estimated",
                          "actName": f"第 {stage['act']} 幕", "actName_en": f"Act {stage['act']}"})
            stage["choirs"] = {key: {"active": True, "highlight": key in stage["lead"],
                                    "role": role, "role_en": stage["roles_en"].get(key, "")}
                               for key, role in stage["roles_zh"].items()}
            if (m["id"] == 1 and 254 <= stage["bar"] <= 266) or (m["id"] == 5 and 142 <= stage["bar"] <= 175):
                stage["source_evidence"] = {"edition": "First-edition UE reprint, IMSLP415748",
                    "printed_page": 32 if m["id"] == 1 else 148,
                    "note_en": "Quiet scoring confirmed visually; inherited climax description corrected.",
                    "note_zh": "目视核对弱奏配器，已更正原有的高潮误述。"}
            checked_page = {(1, 180): 22, (1, 254): 32, (1, 291): 36, (5, 142): 148}.get((m["id"], stage["bar"]))
            if checked_page is not None:
                stage["score"] = {"label": f"{stage['reh']} · 图谱小节 / Atlas bars {stage['bar']}–{stage['bar_end']}",
                    "bars": f"{stage['bar']}–{stage['bar_end']}", "reh": stage["reh"],
                    "page": checked_page, "edition": "First-edition UE reprint (spot check)",
                    "url": f"https://ks15.imslp.org/files/imglnks/usimg/e/e2/IMSLP415748-PMLP49406-GMahler_Symphony_No.2_fe_UE_reprint_RSL1.pdf#page={checked_page}"}
            stage["cues"] = [{"time": stage["sec"], "sec": stage["sec"],
                              "label": stage["cue_zh"], "label_en": stage["cue_en"]}]
            # A score link is supplied without inventing an unverified PDF page number.
            stage["score_reference"] = {"bars": f"{stage['bar']}–{stage['bar_end']}",
                                         "reh": stage["reh"], "status": "atlas-axis-unverified"}
        motifs = [motif for motif in THEMATIC_LEITMOTIFS if m["id"] in motif["movements"]]
        m["motifs"] = []
        for motif in motifs:
            indexes = [i for i, stage in enumerate(m["stages"]) if motif["id"] in stage["blocks"]]
            index = indexes[0] if indexes else 0
            m["motifs"].append({**motif, "name": motif["name_zh"], "earprint": motif["desc_zh"],
                                "earprint_en": motif["desc_en"], "stageIndex": index,
                                "audioStart": m["stages"][index]["sec"], "timeStatus": "estimated"})
        for scene in m["synthModes"]:
            # Source quarters survive fermata-expanded source MIDI measures better than bar labels.
            source_q = scene.get("source_q", scene.get("source_start_q"))
            source_anchors = [a for a in m["anchors"] if isinstance(a.get("source_q"), (int, float))]
            if source_q is not None and len(source_anchors) > 1:
                source_anchors = sorted(source_anchors, key=lambda a: a["source_q"])
                ruler = [{"bar": a["source_q"], "sec": a["sec"]} for a in source_anchors]
                scene["realJumpSec"] = interpolate_bar_to_sec(source_q, ruler, m["bars"], m["duration_sec"])
            else:
                scene["realJumpSec"] = interpolate_bar_to_sec(scene.get("start_bar", 1), m["anchors"], m["bars"], m["duration_sec"])
            scene["midi"] = f"assets/movement-{m['id']}.mid"
        populate_bar_events(m)
        if m["id"] == 5:
            m["codaStageId"] = next(stage["id"] for stage in m["stages"] if stage["bar"] >= 712)
    payload["synthModes"] = payload["movements"][3]["synthModes"]
    return payload


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
        bar_end = min(bar_end, total_bars)
        if bar_start > total_bars:
            continue
        vocal_text = item[21] if len(item) > 21 else None

        n_sub = target_subdivisions.get(idx, 1)
        total_span = bar_end - bar_start + 1
        if n_sub <= 1 or total_span < n_sub * 2:
            sec_s = interpolate_bar_to_sec(bar_start, anchors, total_bars, duration_sec)
            sec_e = interpolate_bar_to_sec(bar_end + 1, anchors, total_bars, duration_sec)
            st = {
                "id": f"m{mvt_id}-s{stage_counter}",
                "mvt": mvt_id,
                "stage_index": stage_counter,
                "bar": bar_start,
                "bar_end": bar_end,
                "sec": sec_s,
                "sec_end": sec_e,
                "duration": round(sec_e - sec_s, 2),
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
                sec_e = interpolate_bar_to_sec(sub_end + 1, anchors, total_bars, duration_sec)

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
                    "duration": round(sec_e - sec_s, 2),
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


_SOURCE_ACTIVITY_B85 = (
    'c-rl~UC%Z-avt_q26OzzW))dQ(r1aJAbVigK#ZISdoa5hO9PMIS<K8P2n+!M0>m&Zdj%*C>?nX?M1c%g7GyYpzp}`m+12j;i!{5c'
    '*d&|m?)!OP_(PZ@J`d}<itN6-Nj6y@fBRGT^soHwPrrEo&9`6w_;)^k|Lr&B-@Wc{e)c<GeEC0p`d2>vAHR72-+%MzyHCIT><6EJ'
    'x&8l(fATMW@h5-y$zT5DuYd8wAAa@aSD*gwyHD|w@vDFM{|V#2{_@A)eqQkY694m`{N6AA?2mu(r~h=L{Iwr^wKKvc<ClN$U;g|L'
    'e=3aMc>h~pe(}w3fAZU3ef_>L>AG+K`0xM5FaPX+`T5`fhqcMy_%HtEm!Ez6$q&E$?CUSyfBtRJ!Pot5$iLRG;w9^6Km7;4`X~RY'
    '<^ETnee+G%Y`Sjtj~d=rU+ov0pEPN_U;FC)w_ktugM$sOqyOmhuYcIE|NQU%!O#EBzyI04{r$iCy<h*{FMs;aK7sNOY?vQ^^UW7u'
    'z5k?Cf3hk3;otfMc5VH0RDO@H`~T<v`tzUs>s`rzvx$_0PdI2C+&TTz^n<Ur3u-xk_7iL8Z)^|wk3Roan+i{8*wCakx}<H-`qA1~'
    'zw?8y-hZym@e>}lJZUdpck_?_xbQaCkALvlj!##=;V=H=Pk#1q{^wu(^Z)%9zyJS~oA}w+Kl<c*J1yVQ{@w2lw4I0UzPX?O>Ho1k'
    'cE9?6|Dbg9i{JUtXYap|MzMcFwn6BN_rLYcng3@$`SYLrzBK*ceeu<oU%Xd3KA``*-<#2e?{D}&`#1lhW9~N?!wqZuNh<5tKL1ij'
    'NV;ole>W@f*T4Gl55D~Tlk#%zbbjg0#O0g0KT{a*f9&axw%xXk{>A%mKmYoF`0UGVviQy4bno1|@R!`X-~9gf-~A@+f2Q&;!aKxw'
    '=u0*3Re)CS-(h%%R775?fvc?42B|<dVUSeg-e`K4-wkpW5vB<@O0}Q$BuTaBi7ZQXnDqy=K6D+z9s?o{sbU5Iij1UZgV0Mo@roTp'
    '#%={5k#Sf7SY(`L?MJDP)6ONSk9+6*yYMb;Kj}$-7C>@WC{#cShT?Z|jsyXvB*-NW1(I>l2s5x3T;?a>AUJStiatF9NQwm)W{mAu'
    'o{(7K;N+Ki=O2)w!a-lTchc5KsraNw(AV$|pA`xEg1$ShB`>ev8y@7<eaHgE1Ev>PsCe-B0?R8NJiovSiihyZ-5|w72>lOhob9FF'
    'UfT(il>;GNF}GKGLXJuU!UfqM{O!e`s7Oi%;<u{EN(NruGF2iP+@Rzg#(kPF4Zz_|dUhqCbl}+&<`x%q?h;$CP*s5pnClx;8D6mv'
    'y9e*G1FP19YJt?<+hNuUqyR{vZ*l~(LLj9cSO$jSRz^iZ)~9QMONxN3*SlTf{Kv_PLFX#6yihYR84O*p=2!0@fuhg`)(b2u3IT7i'
    'UQuXc=>;|@3S}I<K$2om#?A{QD+Xn}yg)|9pp22_Cpd$WicyBdIVh_bWdz&+$2_=rb=lA;<KHD`CxAjxhP`_NDimd?D+GT`oU~wh'
    '#Ut4TE7}&b98`w3+!|GoiqMu@BY;(e)8!UN6<};St`qWzO^QMpIWDnTQJCBvHW~_3=&@ImS_H*oN-wZb@tE-imRCGxet{Jf@10w*'
    'Zl|wEO80JYa|R8#vsm%or59LH@g5d8=ji8-Pm1)wZ@<8-bdQhkQm-Ky*JF2!=%nLvf={3dJf^9d)8x3+gsQ`PTy@BwNM7OI^9ME`'
    'REH1ldGn-je~giI`U#dzvhw^fU_M~))Tks+_~g2;f5W6|Jn{9TaIv}(O<8q#cF%r}>z-xP<T<?Bv$`_?%J!VrKkTF4pz81u-`pFo'
    'Y#(_!#?aMjI0xnWbb9scXftP$a{PJ9xM8w#d}_XE(j_G-*dHrRy|82qT^H~0q(EO6oE1DEvtmNO;5;L@k9h?Jod#si=^&uOV5`i!'
    'o>+Ai94a~hb}JCQ7ai6sD!}mJU`T-l1%&>CJvD<sr<N2MP`4@+r|MV*0n<zzRS?>b?;es=7}_uG9+FiUf^M)3w+`~D-(ctv!jg0B'
    '$${cRNRL}UMF+wMEqKKR;tqY_s^Xxaz|G~3`bfor?fMErWURG82ckm~wJzwuQm<^XPni@I^h<P($|?^!NG!hI01XmSxCVkkg0384'
    'ib9o#j29@c@{rple0$X$JSdQKNr-0%sgRDXJB1w>Rw=o3Z10^=QRQ?j=h((|>0t*?3Z!E-cWlWWu&e-*_dCpPi#IXJOWlD40V<<*'
    'uWg(t1d0lx_8mXwBLR68Q~Q=j-D4QL7ZgVAHrfhI3ZpRWUcemBilk6Cj1Qz@qDskL?FlBSl<b9OeNTH>RseDHVV}m?8iFB+kI(uO'
    '2vkfw`=VD6s+i;*pM$)LNnY*&BtKdRDyI5w+e0jJQVGc`-F|D;$0M+cNnYn{7v@DARX{d-&)?*b6hSs^&p=tlY%}%*L?&k48k#^r'
    'g)A?yJ<c5lRm$@E?wAhXRmAebo&iBcY_IAFAQiE_rXzq=#F*xQs3P`@P9_zxUvx67h{L>-Y$6V|lg;u+FrZQnX}}CmIHO{iaH-9!'
    'l!<S&1;udtmB43>qzG<T|J<DR98gvew~PEaG%AS4&6{O^lVW*Xv&UnBHgd9}d0eHhInmHOuFvC&0gB~uJ0~tTSRkUpIpcGZS2$;$'
    '^lionijB_An_2Kk8PSDdbAECISYgqn^KCv8yN05&BH)@kBPOLp;Ma&*DG}X8Z~gtJC?r!7F?^^hP$d!5`7~sp*9jz{;-kk8?SNM$'
    '(en!(2#Swk_J-9bY&;AnCBzU`v=fIF9mDK3oBYx#DmD^6WF*B#;)jf^*l1^Tr%edCYrg-G$;OCwCb!s{xjaLI45}d7socZnQ5jLK'
    '72epqR|U~d<aRYTZ3l(N<UZ^qQPhztiYa^yb*zeFdyq#Ta?%Mos<xPMs`GBA5pq&)%%|PK_@-Sw$XS&o=N2mK>pSZcI-{oJbMHZa'
    '7B>kUsG{VK5zx(c2A3L8xe0D=bE|5i$E$|aZWqyHYViXxC?y>mNcSXCc*1%dJEtg~6`3Y8#q4K_icB6?_#nunm}DQK$A$n@P*!oW'
    '56}q+Oq@b!PPkj3uUJr23TebP8d2q`wa933*y{9(ONa4=B0E@6KspR8W-wAfI_xKAFjhd~W`B0k!KkPd>sNHD3l@PS6{f@5VT5EA'
    'reh>cCPb@F$GDgpa<L6l<FNL=ugtP`6S2L=`Sx@lw|@kdGLO2C9j1{K6rNpkHHDOWyQ=M75J+~R2Z~WoGDfGJ6`l_hvDA!Gp?Nk('
    'YE)7NeS-?Ej%+PWeqBro&A<l%R-D>SRzgPCJQVF1cy7xZJliJpC8@LH10`i_AJ}#>8X2hA?2m_FxU}=F_g?YY^Vm*j|LTK6a&V{L'
    '=wxz(o)nl{<FJ;{p;>V`)TPn_85NTW8>DqIX?-Sc$Lpdi?OJ4<_E{0x2A6#m*+PN|^RWml(mFQ;P*G+b>w7V(AnPjbka(@jI(QtC'
    'pmjOvrp2-7rmIy922xH=Va`0Dte~8h=7>*LP8g!9$Qj!<UsIBlo-=<~Z?dWYCqtC1bt`X5q6*)NFtX+pFzi+&J7AbY(J<h2)#Lkz'
    'guIEif?I@$gVlr6Rm)+DOIEoRVUV#^Zbceo(JH~|Kyk>DRc?juQJqYHvkAf3*4oM9w+go+EHGfgtw;+Dnh>15?y^LjnHhUSZ3U0u'
    '0~SmUuAWm(U}W;GXhyIZlnt{L=^7dh11{n<G#O?q4m-RFFdG7#ZlzUFXHi`NThW~ME^lZALvBUtH_}Ha8V1~hB}nv!+lsl3;eibX'
    '0<}|Lt0lt#bm!R<C>sW#JM3B#q9H*|(mTS4P6h)tNauI`LSxoMHZ*`)Q=V2Q6JDwW0Br2?uMO-I7#s$>^mN-G8VA%kz5NQD5xgOx'
    'vrDJu0RP&i15+?AbVlmbcKFgF3=<g_AWW=f9$J=RVp9MRCKfX{U)P78XbJ%6#$JZb>|``(tk@T}Hp{!3jSZb0`%1}KL#|ZlEZFHa'
    'b3M#p3Scl|f7x0KGnx{Bh#$ku3bQv|aA)9tqbQgLfaE?--^g?Uq$?}1aG`^Z43JLG^v!sXqp<+;N4nq1bOGcSZ0=fpswtZaKsUeP'
    'cRIYQWIz|*)|=+)yaQ7N=+YZ43Plr|3P8Y*&@*p}0D&)`rP)TE=m<sz#Mz+o@MY%ODKbrf7(RwVHcfz-K8C_*ngBh1428)w0eZey'
    'NVf{JX#x!Hew>~@ZBW^O;n90AR|CceY$wpyl%TPp^NyG*S-n0*ENs9xoA!#PU@8FFy?Gw=MJ5UWpPKZ})UfdZ?ZAIE=FRBQcz~Ct'
    'yz^^FMuWkp<JA0&os9;VW_R-9?qMYX9y_aTtF##S5R3wt(#M#?Jfi6WbqlFoI56IXfSEr|v%z$MuR9@Qvt&Xr2apGga9><`1rO!{'
    'GSUPW4FDbvOSFqC=~_ufgSiLD%XcK3CYXDJynbxxeN_hPA5uUpGO$YUnC7-xzWDcgb?`l$`A3j9Dfq*ye*^`Sg1Kfay@SaxU=A5e'
    'C>sWRc<_bni(jrF!4p0qBtwEH9tqR0R$tt11q|jvae)pM2EN<Gx#EC<!E<`ZK?8&Dwso#J-oW4^KjZ`hgYVDhFIi-8@cl8oy6j9S'
    'Y*_H)F7ahk(Fou(zQ9XH06*>nU-GgMAh?sk!WEM$1%eANF~KMhT)Oeup3ZP(Us$LR0B<$Sr|7bEENmD&C*s9AeN+;R4FTPgo-Fi`'
    'DS&|Csh-t%UAC`94TPD+)p^1xo7w_};PHdoPo@UKIgG-5YAoC0L1QQ!>uY_MW)To75W>j-e72|P%Z7Q-s0ksRU;Yyw4G4i+FP7CM'
    'lnr!2LTHZW*Y3%_?4=77!f}w+c^i!kGAINNj~HxF2sR#%yOfJVRA08+g#^LI<&m4!>(rMGcR_)9jx=EZ?!xE9mpynP!QoG`ywS13'
    'AlQH$x{bs3g5;SjoACmMkW$Y<H5>3{8(yRkGENj9{RvgEH!yV0ChbACFPrcp1)6NaD~L=A)Na2wS0gw!0H~wM<f>I=Gz?JdN;bQx'
    '$uK~$S}K(-c9DYmnatnLQ~{u_CJP)G0My}RfkOiTU4$y|WusgGKo`*peAx{b0MN~nuk3mY2B=%|c@eYKgF2R&*nWeuO-&kbh1%ah'
    '#mVY{h$rqAzHBm!2#AlHE>To!C8z^QBLk}h^&2q(S`AR=4|W7+@g@Rw6geS+iJ<cm>0RJ#MPIg91qRfeoz2l~FrfC}Y=Mpj1Il=d'
    'P6h+&e8cAGY%pNgFPD#*a5TwLa&VOeJboljM%+pR!vniIQjP7-2h*wpjSLLf>sXV#p@D&)l7gXuv3HmCEAQPVQcc;K6dtfGe6EPf'
    'VuJ%8Q2`F#IfhKxU=%3uVNSj}x(#LfP;kKh^a(vTcv^Ngn-bvQK1>%>CBWhAVr`psYd#neIHWi5(TKo=GZ*h+-F@-X?`J(S@G<f9'
    '0QEASLfHGNF{IeNMFANTn8RBXurYx-&D^RV+=ggm;E3yU<k_R$s!7HNj(n$PJ$zJs*%SdM*SUDFh61cu;A2^K`CJPRi~xKr&6YeR'
    'p`n3~rP|8FH<W!s!2!=*f`^~B>;eiBVmI<H31mo!lhxaVz=ni4S;kEW(U4#cMePIDg&#|X0d*l7p2h>24Fb_DGrNzx`t$k<fw(Y}'
    'Xo<&Vv>hv3d%}i@=|;)$+aF5M*kHav=g;e--`-%L?mw&j%CW(E=gSVEaKU_m-0Aa4Xi6YMf_VYm5ZI7lE<iVgXh?|EnGY_B$Nfu2'
    'f@rRkkGa`M5V>&#D9q4zF;oo1ZuhW46$b`@$mtb-w@@|?qXycG_!`w42V%VPvYU=sdx$+59;co@^AWP_BnlkNq34YIz6DeN&mbiG'
    'f4sozug69IE*AMmiADZhZ1KNvvBhWcyx}jA#q%zIdK;|7F=PKf6v*KG<M-Ne`$*z>?{1M34(+vh!r{FZ+(4?4ymtvK4*!yd758&?'
    '775TI7K9Vgwlq5Tc>jzl<i+9SzKYvpo6g8y>Jet4w1d<m?#xpN@4a3>luzNiCFm#3m{IC6&ck=__1lVSdZ)@NpoqMiUoAQjd6@IJ'
    'nqB1mf{!Bd@<8>`xc5puL^ws?mT-D;a>3hNy4U->Xp==07SGnU*4{;7@o;Sm>>$Cb7W^!tuz0+@6H(wfe_JQ-qOdyt)?o2Lp0If&'
    '>s?5&iilFe?SKTFU+EwbQdsI>5fUwRL=jS4>PRA_wA7JB$jt^*I-=SH4SUb~16Vgew{_)S!@k)F4jP_$ujEh(Ch=0q?dEYE!h+Ou'
    'Y-sHeM<U|fcC+8;(|F1|B+A2g#%UnsT^>7kfHTZu@9z&HuiMN5iHir4oQNV%-X;R6kBg^~P((4$pJwtRO0eJu5hYykNknN8xQAF%'
    '0nmaUMU>)#pG1@vBOqlF<;4idPDFVz0y2mw``ILiQlIO5S|wg8bC-`o0}zWhX>2)1@Zr5a?~kF{ACDLoadG#c4s;4cED&%wXgftA'
    '76>?R8gUkXSmfZS@iv}*W9|MnBwj)Co*a(EZXS79kX@dH3p`qi1eYJ__lg97#u*jnA%+E1d|2ojN(us4JlwmhjaZg19`D_^hISo`'
    '2YmOZiDI3;(2-RJxOm9Zk-TB?n3vPMT?W`b=v9m=C~h;Vpvt_~0`hTERgURUEE$i5qlU$mD!^lc*NC@L1zu-%4Q4C<TP_IHsI->r'
    'L1uB(2($7(csj7z>Ho!treZVb|KN`(-WteNs=((uo@#Vfse-T=3v*BzgvDr>NoAHdqB-%+M`nojVQFHfiU2}9QIpmdpPG5YS!F<O'
    'wQ6=M1X?^KB_OH@f&5Afst_oww0ISo^UkoyF6UBuW*S#2NQFRoycs3HsZ<x|oCQCs5Exe%l2i!nS6Z?Pfmfd*`>Bt7j4YOmuz!*4'
    'Pa?0rNucJW;Jnh}RR|GQT7n9TH_t)~sSx5S(B8h^Dm#9((h^k&F|M>E6+&Enx|Cy#U1+H=rU6PV4aVw`EhiMa5Yp<AE$0!tuy_G2'
    'w0IRl;+2-5LP)EpwwyEULP&X~g;fZ7_3W0jgk5N9Iwp`KL&xgbEr$oY5HihP!g6G=ONs;0Ttzt$*oBZ+4{q7+&+<9FdT`4g|1Lxa'
    '8cSdrUR1>B_D8pkNj;4(Dmb(#aa|PVX@F5nCqjq%bF42P6@e~x>xg+sH=h((+?41Zo)w7TZdNHJ_Nbr`pj!bg9Mwu3Qh_4)Zi%%d'
    'ph6MCvlhHU@vzCHsZVXks##PZS~GObAjKl&qn%3zE4Fx2E!!9`Cn_8fk7m*>Ehz!fA8n<p@FgV%s-O{R+0;2Cs-O{h+RizWO^J~z'
    'XteV?dV2V8@l!SD3}$(rU*vmbqSs~k3*4Zr;u=O*PZypdvI+%#xPC106sc7x=;^f<qf*evw#8fPXxQ`h>;r~RZIcg}Svie|+i~WP'
    '7WUPW_RPi%ckE2So~~yfEkZw9)N{3Q2NM-qoZDzdIQO|E>)Fv5_}s`m0BA|y6C_ztT>L0A7AYRXYT_+feRd(zYT_-KeRiQb-A!kz'
    'lF~;r5czg0xi)DpAz_7pMBS8i`(l(_KRc(m;L*&=ZJgRmo}V3yl;(DElaS#h%@0XFCjI2*d2sKN*=L6!!x3X^9s^b&$arX+#BYzJ'
    '5VWJ{_80G=M{Xvvt&EEqH%0{_$3?m=3+gI};uxqC`RQS^D6WFRXcie$Tyl!QSl`8~Cpdv3G5X#-eWn~0hA})+?iGm-y>Uu>RZT_}'
    '<MF!BUUrMCDnN{R2zfGnrV}f&I5g^`vCte9gX!38U8+qA!=!WbLTOe6CaSRn7XdJxf-vzyWrc!*&@83a(3(>#HTzp@xK|)%=py_r'
    ';6Z`K`|`o=SqWt-P|RUI8%#K?Xw39<Lda3knB%0KY4}lrVosArCWNd|@7&PBJd&to3WGuY3=N9&&L7M784wjx{7Fed-OONK0p9WI'
    '^e(8-yExf0Dlt4o;@xSRqy+4gYOklXha_s9da!C_Mt3A9Yc}0V<V~sYav*DwHsxOr&8Axkswov-&tK7^XiA0GV^_3rnNs2Hz}3QI'
    'N`-HZS}h``)cNL|)q-GJDzfg7)uLWXwVxicmXMbs@p{fW%Ckzmp0kdJq)sJX&RKW+<z-YyP?%pIx}plbp1YpIT#BSge70_{<~H+-'
    'eTx#<QiNX5WX~}yMdFudvKUq91KxKjDa`8`?I_PG@vAf15`I#IUXE#}?OC)*!T8mIZ3!=_3DrWL^~Zaacsa3c8XJ*8F`gD%a3y-A'
    '2tCbg1xma~k$5?{)rN*Zks|bRa=YkDQn{zJ>PuFkIvh_R;mE=UO?M_hP>9z<-6aqe;`NMo3G@o_Y<?~?R8YC+skK2Mm3Yqmdi8*?'
    '3Vn3VN_9j<mHUW;A`ACu+1>nwmaKBG$Gw9Vaw_q9+}qAbhY1C!+{ZqMZjVBh`<O3ud6oMFCtaQ0Mo@^C!(f|<&k<6I6r)brlf=a('
    'kfWuQqpEEJiwf|1LcE%Fw{L5K__Q=uC=nh->~o*67-oSU1?2VU_yP(F^4ULG*OcIo0`)nJD>P_=K8m<;8$W}BihYi2O{8L<^F-6w'
    'IaXY7?tWFoQE|cH{fcY*dKO%8{(<hSxNsavuhG#dF1YiXbB_Ngs5bN8Jouw#`?G`S1<orX0CZniGi*>)0KC5kkrWpoJbJdaPh^1x'
    'peJkQ68=%30Vb>R`JlUfFbg`sYGH119|aN6Eqfm<)T3oJgmu3yzN3Hw`nw)mR7ZgZoV{;{Vy}pR+<$0Iqc#dEVC=u)I*p|AfcdP^'
    'VlIj>cz3?=b6&C%Tv4D+Jb?NDSpY>#;OK`}!D1tdBzQUv`R$F%P9eebOwsnuE0W;HdC0;QiX`~?u98I{6nT)7_bDc*G|1We<X6t5'
    'LXA2A$>RT6BFSSxWx@TVF36F)h3Auh!|JTP#N88Nki&Khq$mG|`SJSq&5Hj&1K)vg$@t~p`<Fle!=I|t!293&@{4bN`;%gR{~y=u'
    'AYQV>#=7Me_k*t4*WDKKlO~P#YhS(p_Uq4n&^SF@+Ry*_-~EH1|DAvTvw!>hfAxF6{=HxR^q=j10)KtO{P>%1zWD0>C#Cw6P2ms!'
    'mO2f5=R)x@TqxpoH~;953vXln_y?bT=W_8E)8%5L^Gk0gF5k@knZkJgV^4py@4evu;YQyNH@JL^ejaXc?>PB%#IqkqJo#=U%Z}c9'
    'Z0yr_JbP;F^))$F=ci#Y0S|HKrqP8AJTRTNMvtjWrV8%7H}1f_HwRpKbHJ512i$mbT)J|+*^grysJ!#!;CE|Z4t{s(&A}JW9DMqG'
    '?|eC?{p!3q<{{QQe~x$OMtX;i8-I>dOyAy}<IbA{+{Amdcj(aA5mP_Y-mzo8mC?I)EHIsO#{$#2cPucSgNL75hW9QWb4>5&vA}dr'
    '9}7(9{xOkvP9QVy-_{RgBJcb_rakC9Ku#}1@B1-T(7Am~<ej_6OhfPRaq2?v@-bELlGDe`;G}o^Aae)ooIQ$VhGmI6yLvRzxv$3z'
    '&^dd|pV;2vV~**aJ{FkH@neDM{Xh2a>=DvCg1kE=9Uc5ZCV<W-1WvX$gFnawFgSwv`5-mAfxwZrYC2Sn4k3oWcL%vZ4vruf$iW5V'
    '0y#K;EKq~r#{xCDd@N9d+sE|=+voz~*MSg6UyvKcgI~xsdh`*wLC^g~{I$!-fH*mhG_t{cgpcTxt%kvu#5R{)0~x$Z8pz<{GB}#d'
    '>|RE<lhq?PI-*FUGiQ{3U#)s;49+RDzKnh<He3#<!D+=t>d{q2j7RSsR+hNId1Z+ky;u(Wz0=cv@@ly{mN+@M^dY*Q_`96b|JCff'
    'qvMO81b05bgA2^wk;@dZCzqJi=a=Z9gLh1NcRm3=`NyQzy=HKa>12anOd33M2A`NwJov*5;?Wmo6c2tdqj>OvN!R`_ds5LW?-xI}'
    'ARIkl{AnzndcpW*e(=#5=3;n1dBxc1(6v0c#mq3HUkqyk$GJ-kkGJaN5OXLV{a`LVV6J>${Q1cD<ox2tH~7j8W(uBq!(6K!{9^oK'
    '6q!27tX(?>SDA&n!CPj58XRU8sKH}q-L=74W}$BIkXfJx|ClC-^1XLV4?c7bUNJo^EWKe)n5hHI{5nS8mrI+%(eLFNJh;0|!Am!n'
    '3-rXrrAOcSwk)i)XZ|dAcATR>i$v$Tn~z727TCW$PHVoC7t0bic&jXNgICHDck)1a<ZVJvd`sqwrIRNKiMPfB&yfq{;3=~3m>7IT'
    '7O25Z#IO7>2JaC6#2w_Z|Hl)Dj|FUW`dGjQ$Bz|kaQ(oGkLQ!a2VQ<_pS(P9x;u7q?O4GEXAXYi$l({dPHr62n{#&Jn8OAKjz?}A'
    'mliT7=Z($+VdAjS4x3Y7jpi$4>YFk9N}2j)?03{X@yNJ9PCYRe*pnMZ-@TL9#Yw@$+hX$2PMs}eewq4Ll)J3~D5p*psn6oL^r$HF'
    '%-V@!kPbc*gLH6_7^H(g#2_6!9|q~*<1k1EhlW8qcrSF)lefYk9lR5YG+p~82&9~KUAZMJP=jZ}0yX$29H{YlYxGqZ<tLAYK|Z=J'
    'jQqie;dFd9xHHTQR!854DQ0kVxXCU$IzWv1TxOKPIpPUr@S1o+8Qdw>`3Gm@!QJ9D^5BaxkZ&_akG>kO@@Kvr6aEv&j)wQZ$-~so'
    '19?yVKAunp?~m)-F;_8oha4*IZsp)MG7=xUk=#)RXObtB(ZA%5FnXKZ6Go?#Tf*pqGW<%@8$9}@oU<#gewve?%5&!6zA`4hoKXgk'
    '7T=q*j@~SzcyMDG#e)lr9nmcvSh%q{9(`6i+2E$q$p+7qPB!?Xbh5!0rISsZP#WpU`Q*y+q>-K6O|D!`8rjLgq>-K6N*dY8nWT{o'
    '{v(}i@EEbrhcNXO8Kfr{5&vYS868HRPzLvr2b9r`<OyYPC%KqE-4pMU1%E*vyiQ&t58fz+Og1<y6QYmqDd#!riahaFxuGunR_NV>'
    '`E+z(X~t*w)P?0d`-Z!m@n_$b({Iu$hzlo|C!~|d%k0sc@CFZ<dLIwx#JT%RkDB_tjEa`NE+^pB!DZ65>O(L(wk$LbZY|3Wj!rFe'
    'b)!E^hZ>zf23M8|_HcU{+*vO54(=?MdIzVLNtUF}vuAK{S;CJ71`n49X_yv%FI}LEQ`W+TGt4QY^ZA<2jxl3P$~cS^Pp&e)O%Hj3'
    'pFC%-;e!j!co7rE;81hdz~EeS2Open?%;zbj>0Rjv-TVvbgr<2r_KfT?7(w{1w{q&w|Y@gfx@j`uc#(V=@J_h6)4{7B}E0wi(k*3'
    'Nv!a|ZV?2ggGU7hKIMs?!IJ_5`|A)hm5~)2m>N6V#cNv4d!6C~bAKW?eX~7)A~hu|_c>CBoC=#7!3EAol<y_lD=x&=Qur#*>o(#E'
    'IK;#0da0ij7Gh|RDwlXxWQg>j_fc^{!+y5QrS%0Q#RrW9dJtylthivQdv4TkkBUG;f_wE_mEeL#3w>|_h>8xWpK(t>uaJ;<wkqhb'
    'K~W*~(`}C;m4|dO(H?MCV92wH_DEA(jP7?x$g}yiy07|Td%r_MwrFQ<<6U2~f`S-U=qmcidEitM)RsczDg><#YCq8lQLBTRP1Jyi'
    '2gIw89E=I^>YH6`?{_gdwGiqf<5e6fLR0-NajXb(bg3^Yf?OYk?3|vvnB(sta_M*>anP4lOyK7FL|Jf(Ab_Q^04k=#Y$6}&Cg(ZP'
    '11g-3*r9Whz`X+Lh#Y#~Mo>5%fkUs_AO(_{Q#7Ag1F36<l|g1$vF0fwDwfQ+V!`m0krYeVY*9|PU~kg5hpakCEiYW_HsZ9J@R;e`'
    ';93GIwVcka@rb5~M->v<ls0TxD$Xl{yao1c-!=*=AYbkA&Z}=vqyX}Zh}51~h2$3zsXav%l8-AbNrmLo>P)<(x)-sfo))v2`joL#'
    '38~q{C<m2L@KZjjghH6|y-Fx>6JzX<2bGYRN1WuO5(;@V{PC7^USvd_AyI>fDkH*$j-)aoztE9YMl?HbD{10ILNrTiQc}W;geYCO'
    'G?c9Hf*`710vFC#(JPP`uH6qxT6h5w<F)@mNe(X{OY?mJWd#w_oz|!z;&^iwUlPO%ia0f48s^xnD2nb*Z*qzvi(+Xj*2^8pk~>})'
    'WEK-?pjhg70Z^O-l|40JY2*b>k+00=q9v0T9L0DS45e~N(G(ZKWJ_jw5mH(NL@TM~MMw!J4xJ^pyhuo6RnBi@Ryk>;%GJb>okA$p'
    '{fIRf6h<kvo9&&?AF7m&5S8;jX0I61=#*|YTjZc}I)YNJJ4gzn9F`qql~QiPH_!SP6+&5!?2bt)C#@w5FiETTF=qv_g_c}FOLlny'
    'vBi~KLqS38nnUAwVPaYm$P1WV^VVEbyn@*^FHO8Q*ev<u1<x+F4P7nWYVLVb7Q5WGIP5$R`G6fOo<W^?j&!d=n6wlX&4BexrY^ub'
    'WKs;Pk;pk4yhvD$M9vxBMZ&;m4~3GzT?7p22p`=cP-P6};xHn-${1mxBdCnc{^Nuom9d$7oDi%sMzTYU9uQT;*!VPzprm5PBWQBx'
    'aM2_z7Yuv1c9Dpdsa#O(;nMM<<R%vkd%yPNDA~vb!2XEFil-FhB4uAqyib^*Qr0+{Zjh5o*ym$8JmxxQ6?1U&UvK*~7a5yJ{B+#d'
    'KFkHc!O#7ax9@S0aiB%G+Gxqc1;S$7(0fF<DFqbFA)TEl<`h&ghy1h^uV5y4+DcF`6LyI{7BfxB1};#hE|tibqHp`w7X(wEL1e^5'
    'MX(q%EOAK@OlhI7dc0=^F}o|3#RXq{@ENYUSlsZ%4_}NP(tY}YlFVDs%wcwlePnodODDLJ)|=INpJ%7%&y)nEGsn00gp|&l+w|hI'
    'Gxlc+SygdtOq~`A@3lqM!+qlPH)>0&hoisk+oOxks){3hl)FbxRdM8x(nA7O#W78Lc-A&u#Sp3nj``uwI@jY>11EU+gU<B?)xZg#'
    '->A7NQYD<i^B-}pid6|G`k=cMRRgE^L3b&s22N?(pLWZQmOGGvvTES$-gt{7pomiqoZ+@VH>yCDaBCX$hAyFM;M^IXKL63#E0=R;'
    'i~53wpj^)JjeQ{Ha-I+4uW4h|6P<hIXIdB}G{X@`)fpW={?#6+O{y@u=L7o#wOJKLM<21b(W%0?G+}yKC8)BvG;q3ADZhP0)e*0('
    'o*rrPsv{nefZwPosE&BV34ZZ8)Z0X=A|4@xPl`lEK9gB#@dzipAg3umDl<a7X?)I4%8W;(;g|SXnem7~{0cugWyT{c@k@MAW;|jQ'
    'KjXKbDG8My`vArldfYTLl~)b13vldahMiseK^d_Nc6|OA>qw;V*u_4+A+f@vcWbkdju90b+i=JS{J8j}kl0y=b-=1LD=KzIVP~b;'
    'DI^{dl68YTjJ7BtgTmqwE_n?`g~cOw@*3<F76Ys_cQMF<B4fan@(xdmjAs6IgJ(rXv;VrmM@7aETm6@o(jh0s$B^1q&gTamD=R)8'
    'p=7Qp<eY+|*oIBsm<|pKjA9;kryUg-%|eVHx#p1bN{MDJ#>-nwE+{OTz1ZbXLXH#}DL?qh$+03Mw@JMg;Ha?3c;EA+u*m*V&$A*U'
    ')8mJUz$re8q1dBe06^i9)8dyN8K~GO7Guwv@d}R-9ySvc8zW9e>`N*sDaJ5K7k3_gXq$Kh8zY?>^JjQeV2trJF-+h|fib2h+Oq;<'
    'a((wJR)Zuug~S9Cz1@7Q3{Y%Le$w%k2^k?OBc{+#YW{2=rt3f2{ug*m_2up^bo)z0F~!bfr~*huG39l%0NNJR0*KkoV-M6WMa9Hy'
    ';V)H1(yEw!XI!D;tb&*==w%m;(y1V3?ozFEAW(74sY~5*?xsft#hg2R?alFC#mT{)zM!Dg#oBRQARF?e^3(;|IR&C4&k9LhtR2_c'
    'p^}d(PhvH;R+ki#T<UD}+Hc)ZuO%xkf$b)*HdKTVoI(@8Qhi4Ng(mRNT0n&+2we+w!SRYtz+EF(oS^6g$A-g$odF7@lmxktck=<e'
    '0u)&FCA7evXR}HQQRPXj&CcOJDI^spH7~0Wm1mWt!)Oe82ssrd<ko*)grL<4Q)|i~Le%Pnt6;O_RhYz3Yz7G`OlB;`7NrN<#z+Cl'
    'hZ?5OP0Y%u#G>6X$<v^)>wQ!}@^PuKb}}g}`Lw#!tilu)3Dt<53X^7O9_65tWT}~#p-+fWQ7KeUzc$5}fV_%R;2~O5mxZS)4T?-5'
    '_STBcC@M%&ObYozbJt^5a2m|dX2*HNQE_Q7MVq6O;?iK2=0+Pw;;f)Vbgwu%#U<j-is<q%k|HP}Q5yXkS0U#pqQVp9(RuTP^@>Ui'
    'V*@8_P*h@^U&BZsg(eQOulEto3QSDHQ{z_mCn`8`JcSWkP?CZZ*RB1zmuDSjV^(mAV>~PgIqg)E#KvuYc?ndWqF+YQql79?V$ha*'
    '7aN&SzHbS3{z4}LdRr2o|KK@zzRQ~PF|y|T2hM`?T_T%@iER93zM!A~-~USJe|hWiR&4zL^2=|(nrEE}mLvxDKgH}vv(D@xO>tcB'
    'cuheg>0&1N8Wa&kh>dZJjLcGnja^PzVoRbL$-t7%qA0Z<&!Qx?nlrf(WX*4q&m7R|;3qPW>cA5jN_Cj&^ioZJw1Uw@H6%9CQ>mu&'
    '&|oJ{6Viy?PgvgLV$c^PEyfa(L>gfY$s&!kgrKFaNNWg)RP3Tp0VNHE0!Va5Y0jEml+r|tst6*@i$`;7YZql+$XP_-+yW3)2F@=K'
    'NoC;TIp(EevPw07!3^VF&0Y|e7^qnZ@)Cn81*8*3Guem;%v5s(1Qmf<U7kF8R0KZG0jwejizcFqYD{|BD=Th?nzP1Y(Wg;v*O^ra'
    'gbPS8p@w9iLBK+>bK_{&xLzs@6#yJ&FwI*dQfR%32TZUC=$2f@vMX!m8mWh<pK<5yM(qzPMk9z{AY+Xq9&V6HF<_w>m&mLbjoS?q'
    'S7LHCVmFT%(?g(AbVpq1G#M#M9N-<I0j`e}D=POjv~}uy>N`+SF#@(>q^g`$f^bgsq7b&w&+Sx}=EECBg<(6tt-wiP*v@z>aJI0>'
    '$8o3-_N}SP5i}dF#xoA@EMB~6EKz_pn6V~nn>Jj60Pg_Q*llU@bnHQZ_x8eK)IA~q(-HrEf7Vn^D#0T^R{Ja}idC+Ga#v659{M+F'
    'blVwDGv|mHFA~w0fWIt(THONleM^w~T?*LmQow$f0`|KUupd7K?4SPAU;SVIKuCY>>)-n9{deEX|0ySay~@^`-kvpfW9OR>|6l#{'
    'e<WZ0|Ls>l`uel?Uwy!C!A6A3zW#6jy0-Q=K7aq!*E<DoDAJY=wl5^Yt)ZWeT)1A>G<jiS$3v>zOT*s_Q@yg~{0`HQY4@b<v63b`'
    '?@Y=0uyL)b&FuT3y1JaeAF8a&Cj6nwx-7&Ws;tjlJlAkV@A4Zf@0!u2JnkC1=5=Y1k9bB;s9jQIIXpTmxVcY#uH;t7Ew#_2{1Ua#'
    'v-}dZ%fdW+*<XE9y3EbJ!W&)joZR`~KV)~QpI>HoX`x?ccZs84W_Nj|UuJiir#tp7mD^3-(-Sba!`2_WgwEP$mbkF)pO|wQH3^IA'
    'VeN!Cf6U%t)~!Ox9!;%=c{IC)3a@PHZd<2j7M4x$Jh@@7wQlL1>w)iEl=yb1dZJ_&O{(3wUVF6Mzwp)v&EFhPx3Q0K@JJVn8nY>E'
    'bX+UQx?7s$$a%t^@Um{9?)VG~kK%ER^I5PO+YMJ?9|WN8SU8$s1+Y}cz6r3vwu##Alpg}$Z;wOWE7c8gYHCUU*DY|Z<+|zZo7!0O'
    '*XlmC)+en2Z=vL190bZ9=PuR!uQeN8wB1e30h?PX*!WYnHg^%!v|6okZPZ;&k!m8<3Bp_YRBCO4<$3A*OF=<Ebb^}C1Cffs?7e#n'
    '*v6*f$S|s5^GBqbUMK+AeBtRFpR`}{CIxGj&;4N@)*(|~uE{_53(O7WWO>I11ATk>urOiJTFsrQwMW9t#$Z_tNZ4yFWH`x!)@rgz'
    'li9u^)%22$gN({pYtc2P#?|(!>|5@FCKDr{HZ3LnBESNXRff>|xX`%$84aPC3a23gN@g-mQ0N<w<?@zV)Pyk9nFp6dWU?aD1bw?('
    'ZflbkkJNm$%xPCLknLjBCBZ3XP)R<v%QT(cTurRG?Be`@Ql5#Dc5Fu=^(Oge7p0PeYzJvBxX_x@PcwB}F1R|ogm-N$oC#5zD!Iyb'
    '7WQ-Xi9Pj!C<)AV9`+VlBUerm>P05a_N{5y<kcM(6$dA2{%^ryq%H`Bz?uZ$0?>?RsSd`P``Z$l`H3`YJ*L<u(ruD`iv%+?Za{64'
    'Z_5!zhk<yTlG;RQukQ!|6?uDyCw>A=zHiIU6_;^`o3!5o^GDA6V{kox7zYJv`m58hdS*~fh?U0ywVzuuE5@sXBOcF0j#{gkpd|ck'
    't|^|>9{63*z_dAQoj0#Llay@UQmI*p+PhKGcUz_*fACrWs>s{A{ZQ<+vL?|vL`Rk!eQ!-bTIFr39NS|RX=0gHX{>o=PF+b_>0|8*'
    '?Sr<Z-xfj5<#H@yYi!?=h1;^a<TJ`Laf{F&ZY-f!f+}lLstgEk*;Dc)q=hvURO~aYL8M}zbK6#~fFs4n^n=Y{Q2{|6CI-+kd6qof'
    '0<vTk6`EUAu9+&Ry9wCj;TBmilZ!B>`?8GOg3tsHEv_HGOKxt<?+^{j9oQ0e3n17kbq)&((A);?t(!GYHLF3M!ST#s#fJ08bbkw?'
    'LNvmE=v7)GZ;k9v&|(fiR#Bkk<yhiwfdo2T$k~>tr0=#!_g%)FdA8dUkDA5sE1t6AS_*HGh1iFqo+vxwyVInn4au^33oyjIhBwo4'
    '$?Ppy4S8;iRi^3fd(y(4*9Y)OQzO%}ADT!C4muW8)B(vVwCLc}%fk^JJlm&Xvb^3>M>>fnOW`dQ8dTd-b!+%+d9Uj%7cDur2nc8<'
    'CKXVf^E&YnDcaA(Q3WI~?kG+w&}hk{IM-;&v#yZ|$PZoXf4majc}H0MVK?<{vi#W=i#Q&?+6?FwLIl^qpb(AvyNIu2iL@;OaBhO-'
    'FX5~}V!Qbr!P04qSVQK{K{Zxxgf%FunCkcB8N?>mK(VvUW83J48Zg%Plk$|*IX+Y!sBCKI<U_}kNH>QvuWBgIQU@--5?U2UL|3|2'
    '@t`}TS}5l?>PnXJTU0dhRNK*UFoNp2u?AL+uY?ntZ_y>o87|rw;MHI{%bS%|8!t|}+?&+KBfRN(YB}pWlv!qS;W7G;*(p?ojB!5S'
    '&5o%ozq!UI^^5G7Z|P4^b!<C-uZNpTmM~p(XuQzIrSvWRIs%K<=YI0Uw<*>I$)OL+bJ6P9WKuG>*+==h*<9mu4r9joqR;y%B~!Z)'
    'nev)GBZ5+x{cFS{@MW}gr*{;uU~V@;Uiw+P)5@TVG}_|5vZW@fVHP#}XneaaRxO<TTvw}Qt|BT~!~I<;n6PV*ziiWZJ@jZ!BuXxN'
    'L9i}7TUR{EMK2PIAvemQMun3n$99oR{&}g3&e94tLa)`arbFzHjE~@6G^BE-bNK3(NJ@#&CCi*CxH__CRS?(1^<5OflIz~0QpJ_Y'
    '#qHEzV)*Rz=;5{}^KNA2M(?jJKW21vMvOkbg$_#8$V-cxu)YIW!vAP2Ci;*thKEA0s-pR2zj>O%5;bVoVxf%Q7I6|C)fh+dgDz6E'
    'vFeGeAK1DMo&=W{LR6@R1R93_Zq5-xs?mV*X`-JWuL>_KBSydGjY;bbt^skNTjNl-uE7#=NW$TyX7h^2O$aQ3hIT|uG&!X9iyyp%'
    '8cO2AwLaTkl0yw8b9!3xeVl15p@(*6%<)ZpR;C7ZS(z%F&bSa_jq!40BQS3`DKWYH7J62q#!Ok#XW8ss4WAOH21qjwC^{kZZiX{3'
    'Doo>tq$$YP2qO7jV^CP~ex|V+Cy^pFJjW8p7MUZ!x`$E4DbQS*Jj0k2(M7cwe~Se-*YFmv{EkNVMobi6eGEJ(OM^kA<ryJ*tg#?y'
    '0TrBAMB;p>GAO8vkFeN55C+v)3GtRuZxAay$=FA?+ZD=-%1AO6Qa`hwE<7nPr6=*>XSXgZH(dp4o)CjkQjV_?K`Gh6YeZB^c618M'
    'KmYB5S8#T@ZjUXXK|vY()p0roQb>k)nmAVr$!b~`Sa})Y4eY4AjPwR}QeGa1zSFZ|c6=c#ILiRoJ;$^(+d?u%_E!T0_1~oj9h8^@'
    'ygBH*Tr{C7$zl9}StoTw@`}%)+4Y?PgF-S5k@l7hQf#L9kim-03=bJmv6)+onI$|aF!QjK>Y@?WH3(%z<~U~Nm}qCi<rqiw0Rk20'
    '1ZxngI47F4+d;j8a;neztZzX9IWLZE&lFN{o)3H{JS!61e88Kv5e>Z+7hVGMN1l_>w&LRSO+Fwv8w?x_p8}Is)VR2!w<3<ami1$0'
    '#ss5)L%7}Jl23$)hTaOA?U(m(Z@8_v*dwM%f>w;dSm4gz>8A%>IAq|hh>Opu>B|w>DBuFjvdzp$(a>8#-9hl`GchK^ZbhC@{BYzT'
    'tZZ;_<S!09CY?-`v=#B@>}KSGk-+h6Q~crsKB1AeqRx`513OIKa9eT24<3(S1RD$lPM44G4&^5_8Eh+V5{0z=s_$`PV}iTO$1+zC'
    'jky(9UyETqf2L&Qt;lcGk&O(l9cSnJDRUjUlDDEi3b<Y5W-t<fgXuBCjD-f@3VO`)2H%Q2M$*3`24et#f7~1yd@JH(78@J@7l%$)'
    '^k_T)T%W04Z;j<-?5)UG2VXaOvMB%!_3~0@#B0D+HfT7QS39G6z!U(iw^{GD4ZTC-Zw0-iMiqEtZbg3c5?Yl7(*kh6xjJ!bab(P`'
    'xY<>`$h7X*_y7!xnYrT&EgF6+=;nl#E}BoKU@I<9|EK9)T{hnK=J^}rfmI)%vbQ2WKP|rUm?;EN29V%`@)NaM(bR1Py_|We)#OdZ'
    'R^*S?zhLSBvj3p|k*U~<*lK#JfQ<?0;P&-+q%xYWt@yCJpG?J8<o5jh%^I_*+U5{{()g-6ta`R0Ugv8ZHX9BdU}V5?qxk_FjkXoE'
    'Vo!M92wO3?tvI|4j(r@z{jUT--`E;@B&*qqF@l~T*hGK<1}7OoL=$aAHGw?D$?CVFdfBKfTje&d`_4Mj`&zjbv9YXFF<3nyL$9{P'
    'f|JUvP}71&>aBV!@)5LO^#-d3jJ~=n7?-SiE1G$!L9mGc+p!VaTUO%0iF7Nd^+$m^36)rIBHW66!c<k+<lB<Qk1)Z6D%^@=N5!OI'
    ')!^N+mC}dCLlbU=<zDUp-X!2__<eW!Sd)Mh#l=xjThXoV*Az1BR>Vt+;MsuS5&9U+Jun(#E9eTC46zmI3YZPCtq;S^t)Pn9igX7C'
    'LxFGCimRJYJS_#d74!h_4Y(D##h)S}27`bn95qkB@%0kO7+b-|^<JEFD3Of;>Y9>f8=4A^h63NG0-mgpif5*vz;nC<XG4LH%M&@z'
    'RlXHr4Fi*JMOwqq<lxgqqu%6OLCagz-qqs9DcG$@)!*udM1}^RFH(8?;^`@ft>7zQGz0|a8ke@_M-X5##8!kku+^Il2f@V)y|E&;'
    'kEpf-6QyN8Qb1ebZ?I^ft%zsr0rZA|fXyI0!h*@SBCKI#a!_ZRIgCvX)!C+7rCmG(Wk*p+5InueO-6!nG7-IE+xKPJWen<P9{gg7'
    '`5^y^PgMhi(0m=ek|o%ey+>g~b?<p>KIF^pqtGDqrlT+D@J5Dk*pE`T)pkV>#)H6TEB;3+$hZ(VE>sNH(ec@c5aM#@^8Q9d<3o5Q'
    'h4(~LG8Hg!NP6C(Y<w8JlwR#nt|~zNm)7i&3dRBTV|r5u(CDD9PV+t8D;3_jpx#h#>PRp;sOQw1w2;w(T>QWdud+QVT7UpPR9Q4F'
    'pzd66Rg_Ev5abV0luZK=`VYIj;HnlNj4$taiViR`kcT(wKqCWr`bfJ(q3olIIw1dK@99!mFfBmAf2cAtEnt3eAE1m)3lPDFDvPEC'
    'i0DI=CDQ^#`O@zCQcX5K5I^_(xl##L7ZAq}ec(hTm@c6BXeV~{R_=R8GILU-w;0a1-SVadDCV~*Q%%8C0Hqsy{;Lj=@j-nI-`pWK'
    '6+jt2NK-TwKzVt`Z*(LhL-jB0zp<!3ec3QjJqQ<2tQcSyyHstHaBc?;3=a%2(z?x1C7>apbNI6@l@99-1l5br_c*l$3uU)cFi>6g'
    '{7fYo0ICn3KWtbgirJ9BzTbaoU$L`inYI^=2Ylq-Uiw@qDH$3Xce=DP=c!%IhKK4mw=fG1zJj3o%%!#Jvhyl9sQz&mcVKJ`jRw_I'
    'ZnR+!E3P*ZR5!V$+0nrY28YH+?%d`)4%cznWPD(beg1*!QC7pnm2F^w0Y{iNdedAqCa?uXSvHmo1RR@Dpf1a5JI$d$C_Bdj2c87z'
    'OMU#iP+`C+c5O@=u&XG0%K``WW>X8cLob>LIJa(qc@k$b?8!!Cyi>2XMpLj#P>(iqcdKkN5vXTd!)B`lb!=;7(JCQYP`)ZlRte^}'
    'cF3|-f;ppA8P!TKAG1RSRte@hcF52wx1xp&Q<=BQt;mBcSS3Uo5E?02HPkfqHLFu7d#_Rrk!m0_l|`%E3L0d|Dj_zp5JZ-(5~8iI'
    '+8BU=t7I!|%2p9r9mHeRV?wlA&;;SF&|B?R@F)yc3nhEDC1E_8tpd<&*Kp+Y3T3lXs<%P|@R}%E9h6+sMl`j_s-fg|9@S>621}~^'
    'u7=|h1<{!dimT0`paQ@okYLbp-0-qjDPky2F)NfeF(h2;3MK~4o;yWVF%)MQ+QY#55}E6rM?tWOAW1OY6C#=jEbZ)wNG5{f{W3#j'
    '6G8EDnIMug5m*Y=5dkKG;;b@5pot){n<Bi4wqo8&Fws`<6j4P`l7BWCkHtuTK(oO>6MO3E?vfA<xfQ8bKSGmXASJwpX2Wa+pSm%i'
    'vojbZ$?Fd1j+Q+yk#0p;fzYH|k!H8E>{y8ivZP2qA%cmvV)~QhDuN8I$*(-(*Z^B0UB+pgJegnzax~Ufq$AyHAGT4T$uN)+J7~WK'
    '6?8V(Ry0Y1FF53!fgyXh<{Sht<W_`L^zw^n(h@7RZ0QJpE4m=)chRUdysbAP<bc=R@O{kJnNt^){TorV72N7Oz7S90J;+r!WOBE?'
    '2<wh$FW3}q#p&i=_9Pl*E9ODvU+6|MEs*<6&94Op5oOu5Y=u6Rp$Qi7M4v`1cBTTd4w#3g*W;B?;fSKG2zHsThi6f3Xlk}1O|(tJ'
    'i;rFM#)h15sU%Ngeo*P6khVf^^wk^LaVu#nr1O$h%|<OMmo6g68K#J6qOAy1L^9D<%v;GO!r~({L7+3yR`>%kjIvZNQUF`Q7dSKk'
    'I$4q}aNYpu04{LB09!#9xC+>ct9ID{=&;Vsb7(ZoR`9r>XmH5@=)AkYWdm$QxLKf(cLv*vbc+Uqp$mA6MuVY~g<+X2muPP=biopt'
    'ETF+K=w!9HhE@zZSvIbrY#1!wDwoh`7<5cs(v@Ru7&*zn=pyu-VN@BJ*(h64KMC%mI+tZkrzkknuoZc(=zNev0Su2Wb?J7NRN<i!'
    'wjz$asoxd_Z(wv8)@_Y5;(4A3!BlJoEn8pC&7l&vA|L$PkLx*EM(DuCM$mC@SQ7MYM#EvrTwvLQ>IU^N<A-E81R34z2DJ>uW&<Gr'
    'HA}{HT3wPe41x}FODGryOG<=sAvz(TA+h92XbC5%Hw=O#xWO7Fj8=<wVFsgMNvCkntPc%U3YI(z-O_!^)CSq`SW++C(==^DG(47k'
    '3}pMQ6LNjDw83N)Ea@30%z>s2X2WAi*g!`Pl(<fzA}z8r4weiKN;TSK)F`=M1&P3Q)HvXZLK9<2-(VX?huoV0K}Jn|RZ6l~sX>rI'
    'F*G@MxmF{{NY_c(su5&B>w6xp9zn*fa7vY1awLclLB^@Bfo#<X`P8{RD}szHkWZbHbO?LrP=<_i>w8)R87I)ilLl|qh;Zs#$%r7;'
    'h%yk!Qnf);5u&{RCj^@aQC@pR40(-9Mg##MqV==Q)Lc>_hy>BY0qB%u6C!$=W0Er=qR*3tN_GR0AO_zr(R<TEfurFNLp;IH6RtJm'
    'jeuzHWf$bR0)rtCsjiJWL=_=YZV+91XErG!`vYX+X!VF3&*EhDh;>PFY9gByG15s#c2<uVSKTb>3`B~Ue0#MbMyp4Z7tYTj9oYMs'
    'z2Ok$-IH5<=nE!6l-KX1qKXi6Zd#l*#|A?0^kHw>idKzYUd0nXnFzhSj*E7(0nqC%@@Z0J=S+$o@=_T)FaUb=7dSKkdU-<!*93On'
    'MCf%Iwu@&MtP;I%Z*&%Mtw%3!<$3O8$0kLuZzhcM9lK~!^dZhJM{&sj=m{=x*#PL}^|LKQN#*0L9zEsrPf>AT0QBrHaA*MZ94~O*'
    '0O+GV*%MeWIr>OzSe2uXdGSE);nwBV^vSP4(WG0!!w)HlWTI`9b^4O@5kPofr|-h82n|LOB{{3!ili4+m&pG3jN$!%*=`83XYA*>'
    'H5&>Vb}MWHyfgfWE!rCl1Govgfd<2DMOY|yEukW}B8~YvEfIZ7U_)Zi-Q=nDOCD&^@LRz%+DJ%-+$KJ`=ss#Wmz@O>ZN+}AeXM!*'
    '&LmrrW&kh=2H8JoBS$C(O}G_&tfh~hmYo6-VbJ~C5fMzZ71mSvMjfu&SIAbROC%cv1LGw!8e}W>D`;fNDz|0A?2wAf*S?6hBFqrM'
    'nP@B06agl}kZ_7X6Kw@A&rG;{j|%`pcJ=`qFZTL{77V`?VWiCn6}c6uekd>DY&ax6Hd?@S3Bu*mTA*9eJXYN%nnIIdwiR0Qe06zo'
    'n^hl&Y{;z$BVkx0GC6~7MRStW%uy8zhC$MI{~SN?K%>F7g6(|k)ahe_C|}ruMABCtXLgo~4hGwbFzd|GlZx4jH1=fnjaiv&6r_MJ'
    'F{4qof?r}LqipMK*I(EH$|l{4(C)QdD`#hftw=3zb@R%Hvp|t#py{oE=FOm?w}Kxv;|+==Bhhg|>t=$Xw<0`hrb4&k+4ZwQkrF;)'
    'M1yX{aPj&CT-~~4wCzi(zV5?YaG<lnwnFbf#os&&(HUtg(u-U$60*aC`|uerI|jnr3O)@{=j$w+2!cdz2f-OM7-lO%zk-+PMCOuM'
    '0b8MCe7{9F;Msu4mS?;L8!Vc9D|ih{Cf~k@-2`^Dn+>uRI(g}$*q^}38EPw1vwj{Xm9haL0OWudI5fakaD$UZK|tQ5$mH7T?-YB#'
    'Aq7KkMOc#>Mul!gIx}F^5*q=TkJ<S|Y8cU=TTxFzSJng#FBt(jx@%r;dD#eC(HtW4jTuAg)nsS<tw?WCV~<hUArTeG2`?-G__<0n'
    'U0cB)N2NDi$honcATvE%S<{btf+^UF@LW%?q_Vdn^#?q+sjLT8Y&tMH{4iC~bZiAbG3j`uHJLh$;66yJ=*y;PE5dAaUmQk8=Zvxy'
    '=_Mu@1!HR#^?->+*$Q45R9*4C5i$B>spH<gs3sVHD~83-#J^x<SK3yj8GAel9u=@LF$TO>Af#yMt>6V|5>01pI~gBi`^h~Cjy30J'
    'BW^`_z(0*W5u9<iqTM)oL<VDF<Qv1YRfddFC7Q0SxOmYYX!524V{{*+DVU0_2p^=Ws@RH0mT7X^+!NhwN-;JI{98?<nrQs3;J2$u'
    '#>bf5+tp;_Z$+5xx815hXIwNx^_NwEaWOf3n+i1UR`A<Yc;jNy+3IB#!MIxyPDA!Y0ngrhto*G=Pt;6wu#qw0_&s`mA<<}C!RNV0'
    'M(wAUlS~Vyej;0`ndrzy-iixr)d%ai=$$FqinP%6ND-I@OlQO37dwTfWGnasb$L^QX<;h-#C3ht8cf|*gpa1Rs@sZmIo0cW-#t{!'
    'rV$g53y%v;S=iBNn8ux{2kc}tO#Lp^BX%|#s{6%c?pkRP6=kzsxTp>pud4v#VoKA8`-YE3#58`$Jz#sIVLHCq^dg2wp_{aY9gK$Q'
    '_)@!Jr^>E0OvfkMecOiuHYVod!>oHp9;u1ONA)2&{e-g+7O|WJ2m#fz<UY1;ET;j2#th*hsT>Lj8Z)G)Brr5)#HS=QG-kZoDOR{Q'
    '9A@wC;lXg2eYl5L9A<wpW-W)R`V*If15tr_`E~S6Q#2KruRfU`XiBC6)zRe5nzE_D+?+nVq@$cf2pMxTKfI;`jEtG_H65Y=jft80'
    'jh*mD#(ed?bSysH+&njy;|x)O`RaS=fu^bg^X2!_y(Tslm@jt%?=?kJfjRN>Z@7i$O)Li`q6o9hBvPI2e^d{W?|=XMzx%uYKM^U!'
    'S^'
)

def populate_bar_events(movement: Dict[str, Any]) -> None:
    """Map genuine source-MIDI note overlap onto the atlas' explicitly estimated bar axis.

    The source grid includes renderer-specific fermata measures and differs from the
    task's bar counts. These events therefore describe source notes, not a critical-
    edition assertion about which score bar or recorded instrument is sounding.
    """
    import base64
    import bisect
    import zlib
    activity = globals().get("_SOURCE_ACTIVITY_CACHE")
    if activity is None:
        activity = json.loads(zlib.decompress(base64.b85decode(_SOURCE_ACTIVITY_B85)).decode("utf-8"))
        globals()["_SOURCE_ACTIVITY_CACHE"] = activity
    source = activity[str(movement["id"])]
    intervals, instruments = source["intervals"], source["instruments"]
    quarter_starts = [row[1] for row in intervals]
    anchors = [anchor for anchor in movement["anchors"] if isinstance(anchor.get("source_q"), (int, float))]
    if len(anchors) < 2:
        movement["barEvents"] = []
        return
    bar_starts = [anchor["bar"] for anchor in anchors]
    events = []
    for bar in range(1, movement["bars"] + 1):
        anchor_index = max(0, min(len(anchors) - 2, bisect.bisect_right(bar_starts, bar) - 1))
        left, right = anchors[anchor_index], anchors[anchor_index + 1]
        ratio = (bar - left["bar"]) / (right["bar"] - left["bar"])
        source_q = left["source_q"] + ratio * (right["source_q"] - left["source_q"])
        interval = intervals[max(0, min(len(intervals) - 1, bisect.bisect_right(quarter_starts, source_q) - 1))]
        groups = {family: [] for family in ("strings", "winds", "horns", "brass", "perc")}
        for instrument_id in interval[3]:
            instrument = instruments[str(instrument_id)]
            groups[instrument["family"]].append(instrument["label"])
        events.append({"bar": bar, "sec": interpolate_bar_to_sec(bar, movement["anchors"], movement["bars"], movement["duration_sec"]),
                       "source_q": round(source_q, 6), "sourceGridBar": interval[0],
                       "groups": groups, "timeStatus": "estimated",
                       "provenance": "Junji Miki source-MIDI note overlap; estimated atlas/source-grid correspondence"})
    movement["barEvents"] = events


def calibrate_stage_onsets(stages: List[Dict[str, Any]], measured: Dict[str, Any], duration_sec: float, listen_onsets: Dict[str, Any] = None) -> None:
    """Move a silent interpolated boundary forward by at most 0.5 s to measured sound.

    This is a bounded acoustic correction, not proof of the score's note/bar onset.
    Quiet passages without a nearby qualifying frame remain visible QA failures.
    Source-supported rest-to-first-attack overrides are separately authored and hash-bound.
    """
    levels, step = measured["rms_normalized"], measured["frame_sec"]
    threshold = 10 ** (-37.5 / 20)
    for index, stage in enumerate(stages):
        reference = stage["sec"]
        stage["interpolated_sec"] = reference
        stage["onset_adjustment_sec"] = 0.0
        frame = min(len(levels) - 1, max(0, int(math.floor(reference / step + 1e-9))))
        if levels[frame] >= threshold:
            continue
        limit = min(reference + 0.5, stages[index + 1]["sec"] - step if index + 1 < len(stages) else duration_sec - step)
        for candidate in range(int(math.ceil(reference / step - 1e-9)), min(len(levels), int(math.floor(limit / step + 1e-9)) + 1)):
            if levels[candidate] >= threshold:
                stage["sec"] = round(candidate * step, 4)
                stage["onset_adjustment_sec"] = round(stage["sec"] - reference, 4)
                break
    for index, stage in enumerate(stages):
        override = (listen_onsets or {}).get(str(stage["bar"]))
        if not override or override.get("audio_sha256") != measured["sha256"]:
            continue
        candidate = float(override["sec"])
        next_start = stages[index + 1]["sec"] if index + 1 < len(stages) else duration_sec
        frame = min(len(levels) - 1, max(0, int(math.floor(candidate / step + 1e-9))))
        if stage["interpolated_sec"] <= candidate < next_start and levels[frame] >= threshold:
            stage["sec"] = candidate
            stage["onset_adjustment_sec"] = round(candidate - stage["interpolated_sec"], 4)
            stage["onset_adjustment_kind"] = "source-supported-rest-to-first-attack"
            stage["source_marker_sec"] = override["source_marker_sec"]
            stage["listen_onset_evidence"] = override
    for index, stage in enumerate(stages):
        stage["sec_end"] = stages[index + 1]["sec"] if index + 1 < len(stages) else duration_sec
        stage["duration"] = round(stage["sec_end"] - stage["sec"], 4)


def analyze_recording_audio(mvt_id: int, duration_sec: float) -> Dict[str, Any]:
    """Measure the bundled MP3, without deriving or boosting energy from annotations.

    Local backend: a bounded, single-threaded audio-data readout, not a simulation.
    8 kHz mono PCM is sufficient for the RMS energy diagnostic (not pitch analysis).
    Frames are 80 ms; their timestamps are measurement bins, not score-alignment errors.
    """
    import array
    import hashlib
    import shutil
    import subprocess
    import sys

    cache = globals().setdefault("_AUDIO_ANALYSIS_CACHE", {})
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    audio_path = os.path.join(base_dir, "assets", f"movement-{mvt_id}.mp3")
    stat = os.stat(audio_path)
    cache_key = (audio_path, stat.st_size, stat.st_mtime_ns)
    if cache_key in cache:
        return cache[cache_key]
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("Measured acoustic QA requires ffmpeg on PATH; synthetic fallback is forbidden")
    result = subprocess.run(
        [ffmpeg, "-hide_banner", "-loglevel", "error", "-threads", "1", "-i", audio_path,
         "-vn", "-sn", "-dn", "-ac", "1", "-ar", "8000", "-f", "f32le", "pipe:1"],
        capture_output=True, check=True, timeout=180,
    )
    pcm = array.array("f")
    pcm.frombytes(result.stdout)
    if sys.byteorder != "little":
        pcm.byteswap()
    sample_rate, frame_samples = 8000, 640
    measured_duration = len(pcm) / sample_rate
    if abs(measured_duration - duration_sec) > 0.25:
        raise ValueError(f"Movement {mvt_id}: decoded duration {measured_duration:.3f}s differs from declared {duration_sec}s")
    absolute_rms = []
    for offset in range(0, len(pcm), frame_samples):
        frame = pcm[offset:offset + frame_samples]
        absolute_rms.append(math.sqrt(math.fsum(sample * sample for sample in frame) / len(frame)))
    peak_rms = max(absolute_rms, default=0.0)
    if peak_rms <= 0:
        raise ValueError(f"Movement {mvt_id}: decoded audio contains no measurable energy")
    with open(audio_path, "rb") as audio_file:
        checksum = hashlib.file_digest(audio_file, "sha256").hexdigest() if hasattr(hashlib, "file_digest") else hashlib.sha256(audio_file.read()).hexdigest()
    analysis = {
        "source": f"assets/movement-{mvt_id}.mp3",
        "sha256": checksum,
        "method": "ffmpeg mono 8000 Hz float PCM; non-overlapping 80 ms RMS frames",
        "backend": "local bounded audio-data readout; one ffmpeg decode thread",
        "sample_rate": sample_rate,
        "frame_sec": frame_samples / sample_rate,
        "duration_sec": measured_duration,
        "peak_frame_rms_absolute": peak_rms,
        "peak_frame_dbfs": 20 * math.log10(peak_rms),
        "silence_db_reference": "20 log10(frame RMS / maximum measured frame RMS in this movement)",
        "rms_absolute": [round(value, 9) for value in absolute_rms],
        "rms_normalized": [round(value / peak_rms, 7) for value in absolute_rms],
    }
    cache[cache_key] = analysis
    return analysis


def generate_rms_envelope(mvt_id: int, stages: List[Dict[str, Any]], anchors: List[Dict[str, Any]], duration_sec: float, num_points: int = 600) -> List[float]:
    """Peak-pool measured 80 ms RMS frames for display; annotations never set energy."""
    measured = analyze_recording_audio(mvt_id, duration_sec)["rms_normalized"]
    return [
        round(max(measured[int(i * len(measured) / num_points):max(int(i * len(measured) / num_points) + 1, int((i + 1) * len(measured) / num_points))]), 6)
        for i in range(num_points)
    ]


def write_standard_midi_file(filepath: str, synth_modes_list: List[Dict[str, Any]]) -> None:
    """Serialize every scene as a sequential Format-1 SMF anthology.

    Events are sorted in absolute ticks before converting to VLQ deltas, so
    chords, rests, staggered entries and overlapping notes retain their timing.
    Each source stem has its own named track; scene channels are reused only
    after that scene finishes. All tempo/meter changes live in conductor track 0.
    The download contains all scenes (the existing UI exposes one file/movement).
    """
    ppq = 480

    def vlq(value):
        if not 0 <= value <= 0x0FFFFFFF:
            raise ValueError(f"MIDI delta outside SMF range: {value}")
        result = [value & 0x7F]
        value >>= 7
        while value:
            result.insert(0, (value & 0x7F) | 0x80)
            value >>= 7
        return bytes(result)

    def meta(kind, text):
        payload = text.encode("utf-8")
        return b"\xff" + bytes([kind]) + vlq(len(payload)) + payload

    def chunk(events, end_tick):
        result = bytearray()
        previous = 0
        for tick, priority, event in sorted(events, key=lambda e: (e[0], e[1], e[2])):
            if tick < previous:
                raise ValueError("Unordered MIDI event")
            result.extend(vlq(tick - previous))
            result.extend(event)
            previous = tick
        result.extend(vlq(max(previous, end_tick) - previous))
        result.extend(b"\xff\x2f\x00")
        return b"MTrk" + struct.pack(">I", len(result)) + bytes(result)

    conductor = [(0, 0, meta(3, "Mahler 2 | polyphony score reductions")),
                 (0, 1, meta(1, "Concert pitch A4=440; sourced reductions; fixed teaching tempi"))]
    musical_tracks = []
    scene_tick = 0
    gap_ticks = ppq * 2
    for scene_index, mode in enumerate(synth_modes_list):
        bpm = float(mode["tempo_bpm"])
        if not math.isfinite(bpm) or bpm <= 0:
            raise ValueError("Scene tempo must be positive")
        tempo = round(60_000_000 / bpm)
        if not 1 <= tempo <= 0xFFFFFF:
            raise ValueError("Scene tempo cannot be represented in MIDI")
        conductor.append((scene_tick, 0, b"\xff\x51\x03" + tempo.to_bytes(3, "big")))
        numerator, denominator = mode.get("meter", [4, 4])
        exponent = int(math.log2(denominator))
        if 2 ** exponent != denominator:
            raise ValueError("MIDI time signature denominator must be a power of two")
        conductor.append((scene_tick, 1, b"\xff\x58\x04" + bytes([numerator, exponent, 24, 8])))
        conductor.append((scene_tick, 2, meta(6, f"Scene {scene_index + 1}: {mode['title_en']}")))
        conductor.append((scene_tick, 3, meta(1, f"Source quarters {mode.get('source_q')}–{mode.get('source_q_end')}; {mode.get('provenance', '')}")))
        span = round(float(mode["totalBeats"]) * ppq)
        scene_end = scene_tick + span
        channels = [ch for ch in range(16) if ch != 9]
        melodic_index = 0
        for track_index, track in enumerate(mode["tracks"]):
            percussion = track.get("percussion", False)
            if percussion:
                channel = 9
            else:
                if melodic_index >= len(channels):
                    raise ValueError("A scene exceeds the 15 melodic MIDI channels")
                channel = channels[melodic_index]
                melodic_index += 1
            name = f"{scene_index + 1}.{track_index + 1} {track['name_en']}"
            events = [(0, 0, meta(3, name)),
                      (scene_tick, 0, bytes([0xB0 | channel, 7, 100])),
                      (scene_tick, 0, bytes([0xB0 | channel, 10, min(112, 32 + track_index * 12)]))]
            if not percussion:
                events.append((scene_tick, 0, bytes([0xC0 | channel, int(track.get("program", 48))])))
            program_changes = {}
            for note in track["notes"]:
                start = float(note.get("start", float(note["t"]) * bpm / 60))
                duration = float(note.get("dur", float(note["d"]) * bpm / 60))
                pitch = int(note.get("midi", round(69 + 12 * math.log2(float(note["f"]) / 440))))
                if not (math.isfinite(start) and math.isfinite(duration) and start >= 0 and duration > 0 and 0 <= pitch <= 127):
                    raise ValueError("Invalid score note in MIDI export")
                on_tick = scene_tick + round(start * ppq)
                off_tick = scene_tick + round((start + duration) * ppq)
                off_tick = max(on_tick + 1, off_tick)
                if on_tick >= scene_end or off_tick > scene_end + 1:
                    raise ValueError("Note falls outside its scene")
                velocity = max(1, min(127, int(note.get("velocity", 88))))
                if not percussion:
                    program = int(note.get("program", track.get("program", 48)))
                    if not 0 <= program <= 127:
                        raise ValueError("Invalid General MIDI program")
                    if on_tick in program_changes and program_changes[on_tick] != program:
                        raise ValueError("Conflicting instrument programs in one stem")
                    program_changes[on_tick] = program
                # Note-offs precede a rearticulation at the same tick.
                events.append((off_tick, 10, bytes([0x80 | channel, pitch, 0])))
                events.append((on_tick, 30, bytes([0x90 | channel, pitch, velocity])))
            current_program = int(track.get("program", 48))
            for tick, program in sorted(program_changes.items()):
                if program != current_program:
                    events.append((tick, 20, bytes([0xC0 | channel, program])))
                    current_program = program
            events.append((scene_end, 40, bytes([0xB0 | channel, 64, 0])))
            events.append((scene_end, 40, bytes([0xB0 | channel, 123, 0])))
            musical_tracks.append((events, scene_end))
        scene_tick = scene_end + gap_ticks
    final_tick = max(0, scene_tick - gap_ticks)
    chunks = [chunk(conductor, final_tick)] + [chunk(events, end) for events, end in musical_tracks]
    header = b"MThd" + struct.pack(">IHHH", 6, 1, len(chunks), ppq)
    with open(filepath, "wb") as file:
        file.write(header + b"".join(chunks))


def check_javascript_syntax(source: str) -> Dict[str, Any]:
    """Parse generated JavaScript with an installed JavaScript engine."""
    import shutil
    import subprocess
    node = shutil.which("node") or shutil.which("nodejs")
    bundled_node = "/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node"
    if not node and os.path.isfile(bundled_node):
        node = bundled_node
    if node:
        command, engine = [node, "--check"], "Node.js"
    elif shutil.which("osascript"):
        script = ('ObjC.import("Foundation"); function run(argv) {'
                  'var bytes=$.NSFileHandle.fileHandleWithStandardInput.readDataToEndOfFile;'
                  'var source=ObjC.unwrap($.NSString.alloc.initWithDataEncoding(bytes,$.NSUTF8StringEncoding));'
                  'new Function(source); return "JavaScriptCore syntax OK";}')
        command, engine = ["osascript", "-l", "JavaScript", "-e", script], "JavaScriptCore"
    else:
        return {"passed": False, "engine": None, "error": "No JavaScript parser available"}
    try:
        result = subprocess.run(command, input=source, text=True, capture_output=True, timeout=30)
        return {"passed": result.returncode == 0, "engine": engine,
                "error": result.stderr.strip() if result.returncode else ""}
    except (OSError, subprocess.TimeoutExpired) as error:
        return {"passed": False, "engine": engine, "error": str(error)}


def run_qa_gates(compiled_data: Dict[str, Any], data_js_content: str) -> Dict[str, Any]:
    """Run structural checks and independent measured-audio gates; never manufacture a pass."""
    import re
    forbidden_terms = ["mahler-five", "mahler 5", "bruckner-eight", "bruckner 8", "adagietto", " الخامس"]
    lower_js = data_js_content.lower()
    contaminations = [term for term in forbidden_terms if term in lower_js]
    syntax = check_javascript_syntax(data_js_content)
    movements = compiled_data["movements"]
    all_stages = [stage for movement in movements for stage in movement["stages"]]
    total_stages = len(all_stages)
    average_duration = sum(stage["duration"] for stage in all_stages) / max(1, total_stages)
    required_bilingual_fields = ["title", "title_en", "focus", "focus_en", "fg", "fg_en",
                                 "bg", "bg_en", "desc", "desc_en", "cue_zh", "cue_en"]
    missing_fields, continuity_errors, polyphony_errors, anchor_errors = [], [], [], []
    silence_diagnostics, climax_diagnostics, movement_metrics = [], [], []
    silence_threshold = 10 ** (-37.5 / 20)
    for movement in movements:
        movement_id, stages = movement["id"], movement["stages"]
        anchors = movement.get("anchors", [])
        if not 20 <= len(anchors) <= 40:
            anchor_errors.append(f"m{movement_id}: {len(anchors)} anchors outside 20–40")
        if not anchors or anchors[0].get("bar") != 1 or anchors[-1].get("bar") != movement["bars"] + 1:
            anchor_errors.append(f"m{movement_id}: anchor endpoints must be bar 1 and bar_count + 1")
        if anchors and (not isinstance(anchors[-1].get("sec"), (int, float)) or abs(anchors[-1]["sec"] - movement["duration_sec"]) > 0.011):
            anchor_errors.append(f"m{movement_id}: final anchor must equal movement duration")
        previous_anchor = None
        for anchor_index, anchor in enumerate(anchors):
            if any(not isinstance(anchor.get(key), (int, float)) or not math.isfinite(anchor[key]) for key in ("bar", "sec")):
                anchor_errors.append(f"m{movement_id}.anchor{anchor_index}: nonfinite bar/time")
                continue
            if not 1 <= anchor["bar"] <= movement["bars"] + 1 or not 0 <= anchor["sec"] <= movement["duration_sec"]:
                anchor_errors.append(f"m{movement_id}.anchor{anchor_index}: out-of-bounds bar/time")
            if previous_anchor and (anchor["bar"] <= previous_anchor["bar"] or anchor["sec"] <= previous_anchor["sec"]):
                anchor_errors.append(f"m{movement_id}.anchor{anchor_index}: bar/time must increase strictly")
            previous_anchor = anchor
        if not stages or stages[0]["bar"] != 1 or stages[-1]["bar_end"] != movement["bars"]:
            continuity_errors.append(f"m{movement_id}: incomplete score-bar coverage")
        if stages and abs(stages[-1]["sec_end"] - movement["duration_sec"]) > 0.011:
            continuity_errors.append(f"m{movement_id}: final time does not equal movement duration")
        acoustic = movement["acoustic_analysis"]
        normalized, absolute = acoustic["rms_normalized"], acoustic["rms_absolute"]
        frame_sec = acoustic["frame_sec"]
        movement_silence, movement_climaxes = [], []
        for index, stage in enumerate(stages):
            stage_id = stage["id"]
            for field in required_bilingual_fields:
                if not isinstance(stage.get(field), str) or not stage[field].strip():
                    missing_fields.append(f"{stage_id}.{field}")
            for language in ("zh", "en"):
                roles = stage.get(f"roles_{language}")
                if not isinstance(roles, dict) or not roles or not all(isinstance(value, str) and value.strip() for value in roles.values()):
                    missing_fields.append(f"{stage_id}.roles_{language}")
            if set(stage.get("roles_zh", {})) != set(stage.get("roles_en", {})):
                missing_fields.append(f"{stage_id}.roles language keys differ")
            if stage["sec_end"] <= stage["sec"] or abs(stage["duration"] - (stage["sec_end"] - stage["sec"])) > 0.011:
                continuity_errors.append(f"{stage_id}: invalid duration")
            if index:
                previous = stages[index - 1]
                if previous["bar_end"] + 1 != stage["bar"] or abs(previous["sec_end"] - stage["sec"]) > 0.011:
                    continuity_errors.append(f"{stage_id}: non-contiguous bar/time boundary")
            frame_index = max(0, min(len(normalized) - 1, int(math.floor(stage["sec"] / frame_sec + 1e-9))))
            onset_level = normalized[frame_index]
            onset_db = 20 * math.log10(max(onset_level, 1e-12))
            diagnostic = {"stage": stage_id, "bar": stage["bar"], "sec": stage["sec"],
                          "measurement_frame_sec": round(frame_index * frame_sec, 4),
                          "onset_db_relative_movement_peak": round(onset_db, 4),
                          "onset_dbfs": round(20 * math.log10(max(absolute[frame_index], 1e-12)), 4),
                          "passed": onset_level >= silence_threshold}
            silence_diagnostics.append(diagnostic)
            if not diagnostic["passed"]:
                movement_silence.append(stage_id)
            blob = " ".join(str(stage.get(field, "")) for field in ("title", "title_en", "focus", "focus_en", "fg", "fg_en", "bg", "bg_en", "desc", "desc_en"))
            blob += " " + " ".join(stage.get("roles_zh", {}).values()) + " " + " ".join(stage.get("roles_en", {}).values())
            if re.search(r"(?<![a-z])f{3,4}(?![a-z])", blob, re.I):
                # No padding: only frames whose start falls inside this actual stage.
                start_frame = max(0, int(math.ceil(stage["sec"] / frame_sec - 1e-9)))
                end_frame = min(len(normalized), int(math.ceil(stage["sec_end"] / frame_sec - 1e-9)))
                peak_index = max(range(start_frame, max(start_frame + 1, end_frame)), key=lambda point: normalized[point])
                peak = normalized[peak_index]
                climax = {"stage": stage_id, "bar": stage["bar"], "start_sec": stage["sec"], "end_sec": stage["sec_end"],
                          "peak_normalized_rms": round(peak, 7), "peak_sec": round(peak_index * frame_sec, 4), "passed": peak >= 0.82}
                climax_diagnostics.append(climax)
                movement_climaxes.append(climax)
        scenes = movement.get("synthModes", [])
        if len(scenes) < (4 if movement_id == 5 else 3):
            polyphony_errors.append(f"m{movement_id}: insufficient scene count")
        scene_metrics = []
        for scene in scenes:
            scene_id, tracks = scene.get("id", "unknown"), scene.get("tracks", [])
            for field in ("title_zh", "title_en", "desc_zh", "desc_en"):
                if not isinstance(scene.get(field), str) or not scene[field].strip():
                    missing_fields.append(f"{scene_id}.{field}")
            families = {track.get("choir") for track in tracks}
            if not 4 <= len(tracks) <= 6 or not 3 <= len(families) <= 5:
                polyphony_errors.append(f"{scene_id}: requires 4–6 voices and 3–5 orchestral families")
            phrase_end = 0.0
            for track_index, track in enumerate(tracks):
                for language in ("zh", "en"):
                    if not isinstance(track.get(f"name_{language}"), str) or not track[f"name_{language}"].strip():
                        missing_fields.append(f"{scene_id}.track{track_index}.name_{language}")
                for note in track.get("notes", []):
                    if any(not isinstance(note.get(key), (float, int)) or not math.isfinite(note[key]) for key in ("t", "d", "f")) or note.get("d", 0) <= 0 or note.get("t", -1) < 0 or note.get("f", 0) <= 0:
                        polyphony_errors.append(f"{scene_id}: invalid note")
                        continue
                    pitch = 69 + 12 * math.log2(note["f"] / 440)
                    if abs(pitch - round(pitch)) * 100 > 0.01:
                        polyphony_errors.append(f"{scene_id}: pitch differs from A440 equal temperament by >0.01 cent")
                    phrase_end = max(phrase_end, note["t"] + note["d"])
            if phrase_end < 15 or scene.get("tempo_bpm", 0) <= 0:
                polyphony_errors.append(f"{scene_id}: phrase shorter than 15 s or invalid tempo")
            scene_metrics.append({"id": scene_id, "voices": len(tracks), "families": len(families),
                                  "duration_sec": round(phrase_end, 4), "notes": sum(len(track.get("notes", [])) for track in tracks)})
        movement_metrics.append({"movement": movement_id, "stages": len(stages), "anchors": len(movement["anchors"]),
                                 "decoded_duration_sec": acoustic["duration_sec"], "peak_frame_rms_absolute": acoustic["peak_frame_rms_absolute"],
                                 "silence_violations": len(movement_silence), "climax_checked": len(movement_climaxes),
                                 "climax_passed": sum(climax["passed"] for climax in movement_climaxes), "scenes": scene_metrics})
    silence_violations = [item for item in silence_diagnostics if not item["passed"]]
    climax_failures = [item for item in climax_diagnostics if not item["passed"]]
    gate1 = syntax["passed"] and not contaminations
    gate2 = 160 <= total_stages <= 210 and average_duration <= 38 and not missing_fields and not continuity_errors and not polyphony_errors and not anchor_errors
    gate3, gate4 = not silence_violations, bool(climax_diagnostics) and not climax_failures
    return {
        "overall_passed": gate1 and gate2 and gate3 and gate4,
        "total_stages": total_stages, "average_stage_duration_sec": round(average_duration, 6),
        "javascript_syntax": syntax, "contaminations": contaminations,
        "missing_bilingual_fields": missing_fields, "continuity_errors": continuity_errors,
        "polyphony_errors": polyphony_errors, "anchor_errors": anchor_errors, "movements": movement_metrics,
        "acoustic_reference": "Measured 80 ms RMS, normalized to maximum frame RMS independently per movement; absolute dBFS retained as diagnostic. No ground-truth score-timestamp error is asserted.",
        "stage_onsets": silence_diagnostics, "climax_windows": climax_diagnostics,
        "gates": [
            {"id": "gate-1", "name_en": "Gate 1: Syntax & Zero-Contamination", "name_zh": "门禁一：语法与零跨作品污染",
             "passed": gate1, "metrics": f"{syntax['engine']} syntax {'valid' if syntax['passed'] else 'INVALID'} · {len(contaminations)} foreign symphony contaminations"},
            {"id": "gate-2", "name_en": "Gate 2: Granularity & Bilingual Completeness", "name_zh": "门禁二：颗粒度与中英双语完整性",
             "passed": gate2, "metrics": f"{total_stages} stages · Avg {average_duration:.6f}s (≤38s) · {len(missing_fields)} missing ZH/EN fields · {len(continuity_errors)} continuity errors · {len(polyphony_errors)} polyphony errors · {len(anchor_errors)} anchor errors"},
            {"id": "gate-3", "name_en": "Gate 3: Measured Silence-Gap Check", "name_zh": "门禁三：实测静默间隙检查",
             "passed": gate3, "metrics": f"{len(silence_violations)} stage starts below -37.5 dB relative to movement peak RMS · 80 ms analysis frames"},
            {"id": "gate-4", "name_en": "Gate 4: Measured Dynamic Fidelity", "name_zh": "门禁四：实测动态保真度",
             "passed": gate4, "metrics": f"{len(climax_diagnostics) - len(climax_failures)}/{len(climax_diagnostics)} fff/ffff stage windows contain measured normalized RMS ≥0.82"},
        ],
    }


def compile_all():
    """Regenerate only contract-authorized artifacts; leave other workspace files untouched."""
    import copy
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    manifest = load_json(os.path.join(base_dir, "tools", "audio_manifest.json"))
    anchors_data = load_json(os.path.join(base_dir, "tools", "anchors.json"))
    subdiv_map = {
        1: {i: 2 for i in range(16)},
        2: {i: 2 for i in range(9)},
        3: {i: 2 for i in range(11)},
        4: {i: 2 for i in [0, 3, 5, 6]},
        5: {**{i: 4 for i in range(len(MVT5_STAGES_RAW))}, len(MVT5_STAGES_RAW) - 1: 5},
    }
    raw_by_mvt = {1: MVT1_STAGES_RAW, 2: MVT2_STAGES_RAW, 3: MVT3_STAGES_RAW, 4: MVT4_STAGES_RAW, 5: MVT5_STAGES_RAW}
    movements_compiled = []
    for manifest_info in manifest["movements"]:
        movement_info = dict(manifest_info)
        movement_id = movement_info["id"]
        if movement_id == 5:
            movement_info["bars"] = 764  # Task contract; manifest's 765 denotes the end boundary.
        anchors = anchors_data["movements"][str(movement_id)]
        stages = expand_movement_stages(movement_id, raw_by_mvt[movement_id], anchors,
                                        movement_info["bars"], movement_info["duration_sec"], subdiv_map[movement_id])
        measured = analyze_recording_audio(movement_id, movement_info["duration_sec"])
        calibrate_stage_onsets(stages, measured, movement_info["duration_sec"], anchors_data.get("stage_listen_onsets", {}).get(str(movement_id), {}))
        movement = {**movement_info, "anchors": anchors, "synthModes": copy.deepcopy(SYNTH_MODES.get(str(movement_id), [])),
                    "stages": stages, "rms": generate_rms_envelope(movement_id, stages, anchors, movement_info["duration_sec"]),
                    "acoustic_analysis": measured}
        movements_compiled.append(movement)
    payload = {"meta": copy.deepcopy(WORK_META), "religious_context": RELIGIOUS_AND_PROGRAM_CONTEXT,
               "choirs": ORCHESTRAL_CHOIRS, "leitmotifs": THEMATIC_LEITMOTIFS, "movements": movements_compiled}
    if "adapt_compiled_payload" in globals():
        adapted = adapt_compiled_payload(payload)
        if adapted is not None:
            payload = adapted
    header = ("// Auto-compiled by tools/blueprint.py — Mahler Symphony No. 2 ('Resurrection') Symphony Atlas\n"
              "// Target Recording: Sir Simon Rattle · Berliner Philharmoniker (BPO)\n")
    source = header + "window.SYMPHONY_DATA = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n"
    report = run_qa_gates(payload, source)
    payload["qa_report"] = report
    source = header + "window.SYMPHONY_DATA = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n"
    final_syntax = check_javascript_syntax(source)
    if not final_syntax["passed"]:
        raise RuntimeError(f"Final generated data.js failed syntax check: {final_syntax['error']}")
    for movement in payload["movements"]:
        write_standard_midi_file(os.path.join(base_dir, "assets", f"movement-{movement['id']}.mid"), movement["synthModes"])
    with open(os.path.join(base_dir, "data.js"), "w", encoding="utf-8") as artifact:
        artifact.write(source)
    print(f"Compiled {report['total_stages']} stages across 5 movements (Avg duration: {report['average_stage_duration_sec']}s)")
    for gate in report["gates"]:
        print(f"[{'PASS' if gate['passed'] else 'FAIL'}] {gate['name_en']} -> {gate['metrics']}")
    if not report["overall_passed"]:
        raise RuntimeError("One or more independently measured QA gates failed; see data.js qa_report for diagnostics")


if __name__ == "__main__":
    compile_all()
