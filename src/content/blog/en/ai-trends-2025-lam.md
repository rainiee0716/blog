---
title: '2025 AI Trends: From Conversation to Action (LAMs) — When AI Learned to Click the Mouse'
description: 'Large Language Models (LLMs) have solved the problem of "understanding human language." The focus in 2025 is on Large Action Models (LAMs), through which AI will truly connect to the UI of the digital world and complete tedious operations for us.'
pubDate: '2026-01-29'
heroImage: '../../../assets/blog-placeholder-1.jpg'
---

If 2023-2024 was the golden age of **LLM (Large Language Model)**, when they learned to write poetry, write code, and pass the Turing test, then 2025 is undoubtedly the inaugural year of **LAM (Large Action Model)**.

AI is no longer content to be a "keyboard warrior" typing in chat boxes. It's starting to grow "hands," attempting to take over our mouse and keyboard, to click apps, fill out forms, and operate user interfaces (UI) designed for humans.

## What is LAM? Why Do We Need It?

### The Limitations of LLM
Imagine you want to book a flight to Tokyo for next week.
*   **What LLM can do**: Give you a comparison of airlines, tell you about Tokyo's weather that season, and even write your leave request.
*   **What LLM cannot do**: Actually open Ctrip or Expedia for you, select flights, enter your passport number, and click the "Pay" button.

Because LLM outputs **Text**, while many real-world tasks require **Action**.

### The Definition of LAM
LAM is a specially trained model that understands not only natural language but also **GUI (Graphical User Interface)**. Through understanding screenshots, DOM trees, and API calls, it can translate user intent into a series of specific operational steps.

> **The Revelation of Rabbit R1**: Although the 2024 Rabbit R1 hardware launch was controversial, the LAM concept it proposed was directionally correct. It attempted to teach AI how to operate software like Spotify and Uber as humans do, rather than depending on whether these software providers have open APIs.

## Technical Principles: How Does AI "See" and "Click"?

There are two main technical routes to implementing LAM, and in 2026, these two routes are converging.

### 1. API-Based Function Calling
This is the current transitional solution. Like OpenAI's Assistant API, you define a series of tools (such as `get_weather`, `book_flight`), and the model outputs calling instructions in JSON format.
*   **Advantages**: Accurate and stable.
*   **Disadvantages**: Limited by whether service providers have open APIs. If an app doesn't have an API, AI is helpless.

### 2. Vision-Based UI Action (Visual UI Action)
This is the ultimate form of LAM. AI "sees" the screen like humans do (through Computer Vision technology).
1.  **Perception (See)**: The model analyzes the current screenshot, identifying where buttons are, where input fields are, and where dropdown menus are.
2.  **Planning (Plan)**: Based on the user instruction "order me a latte," it plans the path -> open delivery app -> click search -> enter latte -> select -> checkout.
3.  **Execution (Act)**: Simulate mouse movement and keyboard input.

The development of **Multi-Modal** technology has made this route a reality. GPT-4V and Gemini 1.5 Pro have demonstrated amazing screen understanding capabilities.

## Application Scenario Explosion in 2025-2026

### 1. Software Operation Automation (RPA 2.0)
Traditional RPA (Robotic Process Automation) requires programmers to rigidly record scripts, and once the UI changes even slightly (such as a button moving 5 pixels), the script breaks.
LAM-driven RPA is **semantic-level**. It looks for the "submit button," not "coordinates (800, 600)." Even if the interface undergoes a major redesign, as long as the logic hasn't changed, AI can still find the button. This will completely restructure enterprise internal processes for expense reimbursement, approval, and data entry.

### 2. Super Personal Assistant
Phone OS will have system-level LAM built in.
*   Siri / Android Assistant will no longer be useless. You can say: "Edit that photo you just sent me, post it to my social media, with the caption 'Even while working overtime, I love life.'"
*   AI will automatically open the album -> invoke editing functions -> open WeChat -> edit Moments -> send. The entire process flows smoothly.

## Challenges Faced: Security and Trust

Giving AI "action rights" is ten thousand times more dangerous than giving it "speaking rights."

*   **Risk of Misoperation**: If AI misunderstands and interprets "transfer 100 yuan" as "transfer 10,000 yuan," or sends an email to the wrong person, the consequences are unimaginable.
*   **Human-in-the-loop**: In 2026 design specifications, all sensitive operations (payment, deletion, sending) must have a "human confirmation" step. AI can only be responsible for filling in; the finger that clicks "confirm" must be human.

## Conclusion

From LLM to LAM is AI's leap from **Info-Provider** to **Service-Provider**. We are about to enter an era of "speak but don't act." In this era, the most valuable skill is no longer operating complex software, but clearly expressing your intent.
