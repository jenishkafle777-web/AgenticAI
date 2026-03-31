# Product Requirements Document (PRD)
## Executive Voice & Leadership Communication

## 1) Product Concept & Objective

### Goal
Bridge the gap between **knowing** leadership concepts and **speaking** with executive presence.

The app functions as a daily coach that helps users transform casual communication into high-stakes, persuasive leadership communication through **10–15 minute micro-learning modules**.

---

## 2) Core Functional Requirements

### A. The "Executive Briefing" (Book Summaries)

- **Session Length:** Strict **12-minute cap** per briefing.
- **Delivery Format:**
  - Audio-first with professional-quality narration.
  - Companion **Skim-Read** text version.
- **Content Curation:**
  - Source leadership and communication classics such as:
    - *Crucial Conversations*
    - *Influence*
    - *How to Win Friends and Influence People*
  - Distill content specifically for actionable dialogue in meetings.
- **Required Output:**
  - Every briefing ends with **The Power Phrase Takeaway**:
    - 3 specific phrases the user can apply in a meeting the same day.

#### Acceptance Criteria
1. User can complete a full briefing in 12 minutes or less.
2. Audio and synchronized skim-read text are both available.
3. Every briefing includes exactly 3 actionable “Power Phrases.”

---

### B. The "Leadership Lexicon" (Vocabulary Builder)

- **Objective:** Replace weak fillers and low-impact corporate jargon with persuasive, executive-level alternatives.
- **Daily Drill:**
  - Duration: **2 minutes**.
  - User receives a scenario (e.g., “Giving bad news”).
  - User selects the most leader-like response from multiple options.

#### Acceptance Criteria
1. User receives one daily 2-minute vocabulary challenge.
2. Challenge includes scenario + multiple response options.
3. Feedback identifies the strongest “executive” phrasing and explains why.

---

### C. Micro-Lessons: "The 10-Minute Lead"

- **Lesson Duration:** 10 minutes.
- **Topic Tracks:**
  1. **Logic & Rhetoric** — building arguments that stick.
  2. **Business Thinking** — reframing problems as opportunities.
  3. **Emotional Intelligence** — reading the room and adjusting tone.
- **Active Learning Requirement:**
  - Every lesson must include a **Speech Prompt** to practice live speaking behavior.
  - Example: “Practice a 3-second slight pause before answering this simulated question.”

#### Acceptance Criteria
1. Each micro-lesson maps to one of the three topic tracks.
2. Every lesson contains at least one speech prompt.
3. Speech prompts are measurable (time-based or behavior-based).

---

## 3) Key UX Features

### A. Style Toggle: Casual vs Executive
- User can toggle between **Casual English** and **Executive English** to compare phrasing for boardroom contexts.

### B. Progression System: Leader Level
- App tracks a cumulative **Leader Level**.
- Leader Level increases as users complete modules in:
  - Finance
  - Logic
  - Communication

### C. Audio-Text Synchronization
- Highlighted text follows audio playback in real time.
- Supports pronunciation + spelling acquisition for complex vocabulary.

#### Acceptance Criteria
1. Toggle shows side-by-side or switchable rephrasing output.
2. Leader Level updates immediately on module completion.
3. Highlighted text remains synchronized with narrated content.

---

## 4) Suggested MVP Scope (Optional Implementation Guidance)

1. Launch with:
   - 10 Executive Briefings
   - 30 Leadership Lexicon drills
   - 15 Micro-Lessons
2. Include baseline Leader Level logic with visible progression.
3. Ship audio-text sync for Executive Briefing first, then expand to lessons.

---

## 5) Success Metrics

- **Engagement:** Daily active usage of 10+ minutes.
- **Completion:** % of users finishing full 12-minute briefings.
- **Practice Quality:** % of speech prompts completed.
- **Language Upgrade:** Improvement in executive phrase selection over time.
- **Retention:** 7-day and 30-day return rates.
