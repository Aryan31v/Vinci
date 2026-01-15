#!/usr/bin/env python3
"""
🎭 The Simulator Launcher
-------------------------
A simple menu to pick a social scenario and start the roleplay.
"""

import sys
import os

def main():
    print("\n🎭 THE SOCIAL SIMULATOR")
    print("-----------------------")
    print("Select a Difficulty Level:")
    print("1. 🛒 The Shopkeeper (Transactional)")
    print("2. 🚶 The Random Guy (Neutral)")
    print("3. 🎒 The Classmate (Peer)")
    print("4. 🤝 The Best Friend (Intimacy)")
    print("5. 👩 The Random Girl (High Anxiety)")
    print("6. ❤️ The Girlfriend (Relationship)")
    print("-----------------------")
    
    try:
        choice = input("Select [1-6]: ").strip()
    except KeyboardInterrupt:
        print("\n🚫 Simulation Cancelled.")
        return

    personas = {
        "1": "The Shopkeeper",
        "2": "The Random Guy",
        "3": "The Classmate",
        "4": "The Best Friend",
        "5": "The Random Girl",
        "6": "The Girlfriend"
    }
    
    if choice in personas:
        persona = personas[choice]
        print(f"\n🚀 Loading Simulation: **{persona}**...")
        print(f"👉 To start, simply say: 'Hi' or set the scene.")
        print(f"   (Type your response in the chat below)")
        
        # In a real CLI app, we would loop here. 
        # But since the LLM handles the chat, we just output the instruction for the User/LLM to see.
        print(f"\n[SYSTEM] Please activate {persona} mode.")
    else:
        print("❌ Invalid selection.")

if __name__ == "__main__":
    main()

