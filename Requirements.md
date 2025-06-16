# A2A Poetic Agents Simulation

## Overview

This project simulates a system where two AI agents can communicate by exchanging poetry written in the style of the poet Frederick Turner. The communication itself is a simulation of Google's Agent-to-Agent (A2A) protocol, currently implemented using file-based message passing (JSON files).
The two agents are Alpha and Beta.

The primary goal of this foundational codebase is to establish the core components, agent logic stubs, and interaction workflow. A key objective is for the agents to engage in creative interpretation of received poetry, allowing them to generate distinct and original responses rather than mere echoes, fostering a more dynamic and engaging poetic dialogue. This can be expanded upon in the future with real Large Language Model (LLM) integration for poetry generation and the official Google A2A SDK for communication.

## Poetry

It is extremely important that you ONLY give me your response poems for both Alpha and Beta and no other text. Do not comment on the stanzas offered by Alpha and Beta, neither to be encouraging or otherwise. Do not create the first lines of each stanza to explicitly comment on the received poem by the other agent - instead, the first line of the poem should be normal and fit within the meter specified by Frederick Turner's work. Do not repeat a stanza back to the originating agent. 


## Meter

All poetry dialogues between Alpha and Beta will conform to a randomly selected meter starting from Alpha's first poem until Beta's final poem. The types of meters are selected from this list:

📜 Common Poetic Forms and Their Meters
Form Name	Typical Meter	Notes
Sonnet (Shakespearean)	Iambic pentameter	14 lines, ABAB CDCD EFEF GG rhyme scheme
Sonnet (Petrarchan)	Iambic pentameter	14 lines, octave (ABBAABBA) + sestet (varied rhyme)
Villanelle	Iambic pentameter or tetrameter	19 lines, 5 tercets + a quatrain, with repeated refrains
Ballad	Iambic tetrameter and trimeter	Quatrains with alternating lines of 4 and 3 beats; ABCB or ABAB rhyme
Limerick	Anapestic trimeter and dimeter	5 lines, AABBA rhyme, usually humorous
Haiku	No fixed meter (syllabic: 5–7–5)	3 lines, often nature-themed
Blank Verse	Iambic pentameter	Unrhymed but metrically regular
Free Verse	No fixed meter	May include rhythmic patterns, but not regular or consistent
Sestina	Typically iambic pentameter	6 stanzas of 6 lines + 1 triplet; end-word repetition pattern
Ode	Often iambic or varied	Formal tone, often uses irregular or Pindaric meter
Elegy	Often iambic pentameter	Mournful, reflective; often follows classical or pastoral tradition
Heroic Couplet	Iambic pentameter	Rhyming pairs of lines, used in epics or didactic verse
Terza Rima	Iambic pentameter	Tercets with interlocking rhyme (ABA BCB CDC...)
Clerihew	Irregular meter	Humorous, biographical 4-line poems with AABB rhyme

## Rhyme

All poetry dialogues between Alpha and Beta will conform to a randomly selected rhyme scheme starting from Alpha's first poem until Beta's final poem. Some poetry will not have a rhyme scheme, but will instead follow a meter. Listed are some rhyming schemes, including thoese schemes that follow naturally from a chosen meter:

### Common Rhyme Schemes

Rhyme Scheme	Name / Notes	Example Snippet
AABB	Couplets — successive rhyming lines. Often used in ballads, children's verse, or satire	Roses are red / A
Violets are blue / A
Sugar is sweet / B
And so are you / B
ABAB	Alternate rhyme — used in sonnets and many lyrical poems	The sun is high / A
The sky is blue / B
Birds sing and fly / A
And so do you / B
ABBA	Enclosed rhyme — used in Petrarchan sonnets	Love hides its face / A
Behind the veil / B
Of truth and tale / B
It leaves no trace / A
ABCABC	Interlaced rhyme — more complex; used in sestinas or experimental forms	Less common, usually part of larger repeating schemes
AABBA	Limerick form — humorous 5-line poems	There once was a man from Peru / A
Who dreamt he was eating his shoe / A
He woke in the night / B
With a terrible fright / B
And found that it all had come true / A
AAAA	Monorhyme — same end rhyme on every line	Used in Arabic, Persian poetry; also children's verse
ABCB	Ballad stanza — 2nd and 4th lines rhyme only	There came a ghost to Margret’s door / A
With many a grievous groan / B
And aye he tirled at the pin / C
But answer made she none / B
ABCCBA	Chiasmus or mirror rhyme — symmetrical form	Rare and typically symbolic or philosophical

### Fixed Forms and Their Rhyme Patterns
Form	Rhyme Scheme
Shakespearean Sonnet	ABAB CDCD EFEF GG
Petrarchan Sonnet	ABBAABBA CDECDE (or CDCDCD)
Villanelle	ABA ABA ABA ABA ABA ABAA (repeated refrains)
Terza Rima	ABA BCB CDC DED...
Rondeau	AABBA AABR AABBAR (R = refrain)
Sestina	No rhyme; uses word repetition at line ends instead
Pantoum	Uses repeated lines from earlier stanzas rather than rhyme


 
