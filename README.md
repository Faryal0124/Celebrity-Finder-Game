# 🌟 Celebrity Finder Game

An interactive Python GUI game built with **Tkinter** that demonstrates the famous **Celebrity Problem** in Data Structures & Algorithms. The project compares two approaches — **Brute Force** and **Optimized DCC (Candidate Elimination)** — while letting users play and guess the celebrity in a fun way.

---

## 🎯 Problem Statement

In a group of people, a **celebrity** is defined as someone who:

- Knows nobody in the group
- Is known by everyone else

The challenge is to identify the celebrity using minimum number of “knows” queries and compare different algorithmic approaches.

---

## 🎯 Objectives

- Implement the Celebrity Problem using two algorithms
- Compare **Brute Force vs DCC (optimized) approach**
- Build an interactive GUI using Python Tkinter
- Provide a game-like experience for better understanding
- Analyze performance based on number of questions asked

---

## ⚙️ Features

- 🎮 Interactive GUI game (Tkinter)
- 👥 Randomly generated party scenarios
- 💡 Hint system (limited hints with score penalty)
- 🧠 Two algorithm comparison:
  - Brute Force (O(N²))
  - DCC Candidate Elimination (O(N))
- 🏆 Score system based on performance
- ⏱ Time tracking
- 🔄 Multiple rounds (4, 6, 8 players)

---

## 🧠 Algorithms Used

### 1. Brute Force
Checks every person against all others.

- Time Complexity: **O(N²)**
- Simple but inefficient

---

### 2. DCC (Optimized Approach)
Eliminates non-celebrities step-by-step to find a candidate.

- Time Complexity: **O(N)**
- Efficient and optimized

---

## 🛠️ Tech Stack

- Python 🐍
- Tkinter (GUI)
- Random module
- Time module

---

