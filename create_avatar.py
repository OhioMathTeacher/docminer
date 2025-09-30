#!/usr/bin/env python3
"""
Create avatar trio image for Research Buddy welcome screen
"""

def create_emoji_avatar():
    """Create a simple text-based avatar representation"""
    with open("avatar_trio.txt", "w") as f:
        f.write("👨‍💻🤖👩‍🎓")
    print("Created simple avatar representation")

if __name__ == "__main__":
    create_emoji_avatar()