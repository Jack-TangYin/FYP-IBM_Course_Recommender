import gradio as gr
import time
import uuid
from datetime import date
import random
import re
from typing import Tuple, Optional


#########################################
# 1. DATA DEFINITIONS & GLOBALS
#########################################

TEN_LEVELS = [
    {"hex_code": "0x1", "title": "Initiate",   "xp_needed":    0},
    {"hex_code": "0x2", "title": "Explorer",   "xp_needed":  200},
    {"hex_code": "0x3", "title": "Challenger", "xp_needed":  500},
    {"hex_code": "0x4", "title": "Vanguard",   "xp_needed": 1000},
    {"hex_code": "0x5", "title": "Innovator",  "xp_needed": 1500},
    {"hex_code": "0x6", "title": "Visionary",  "xp_needed": 2000},
    {"hex_code": "0x7", "title": "Mastermind", "xp_needed": 3000},
    {"hex_code": "0x8", "title": "Renegade",   "xp_needed": 4500},
    {"hex_code": "0x9", "title": "Ascendant",  "xp_needed": 6000},
    {"hex_code": "0xA", "title": "Legendary",  "xp_needed": 8000},
]

SKILL_BADGE_REQUIREMENTS = {
    "Python Beginner": {
        "courses_needed": ["Python for Everybody", "Intro to Data Science"],
        "min_xp": 50
    },
    "Cybersecurity Fundamentals": {
        "courses_needed": ["Intro to Cybersecurity", "CIA Triad", "Basic Terminologies"],
        "min_xp": 100
    },
    "Web Developer Fundamentals": {
        "courses_needed": ["Introduction to HTML", "Introduction to CSS", "Introduction to JavaScript"],
        "min_xp": 75
    },
    "Business Management Essentials": {
        "courses_needed": ["Introduction to Business", "Introduction to Management", "Introduction to Business Strategy"],
        "min_xp": 60
    }
}

QUESTS = {
    "Data Science Starter": {
        "courses_required": ["Python for Everybody", "Intro to Data Science"],
        "reward_xp": 100,
        "reward_badge": "Data Science Starter Badge",
    },
    "Cybersecurity Beginner": {
        "courses_required": ["Intro to Cybersecurity", "CIA Triad", "Common Types of Attacks"],
        "reward_xp": 120,
        "reward_badge": "Cybersecurity Beginner Badge",
    },
    "Web Developer Starter": {
        "courses_required": ["Introduction to HTML", "Introduction to CSS"],
        "reward_xp": 90,
        "reward_badge": "Web Developer Starter Badge",
    },
    # New quests based on learning paths
    "Network Security Novice": {
        "courses_required": ["Networking Fundamentals", "IP Addressing & Subnetting", "Network Security Essentials"],
        "reward_xp": 150,
        "reward_badge": "Network Security Novice Badge",
    },
    "Cryptography Explorer": {
        "courses_required": ["Introduction to Cryptography", "Symmetric Encryption", "Hash Functions & Data Integrity"],
        "reward_xp": 130,
        "reward_badge": "Cryptography Explorer Badge",
    },
    "Web Hacking Initiate": {
        "courses_required": ["Introduction to Web Applications", "Information Gathering & Reconnaissance", "Common Web Vulnerabilities"],
        "reward_xp": 160,
        "reward_badge": "Web Hacking Initiate Badge",
    },
    "Incident Response Trainee": {
        "courses_required": ["Introduction to Incident Response", "First Responder Actions", "Basics of Log Analysis"],
        "reward_xp": 140,
        "reward_badge": "Incident Response Trainee Badge",
    },
    "Machine Learning Apprentice": {
        "courses_required": ["Python for Everybody", "Intro to Data Science", "Machine Learning Basics"],
        "reward_xp": 170,
        "reward_badge": "Machine Learning Apprentice Badge",
    },
    "Full-Stack Web Developer": {
        "courses_required": ["Introduction to HTML", "Introduction to CSS", "Introduction to JavaScript"],
        "reward_xp": 160,
        "reward_badge": "Full-Stack Developer Badge",
    },
    "Business Management Foundation": {
        "courses_required": ["Introduction to Business", "Introduction to Management", "Introduction to Business Strategy"],
        "reward_xp": 130,
        "reward_badge": "Business Management Foundation Badge",
    }
}

DAILY_CHALLENGES = [
    {
        "question": "What does AI stand for?",
        "answer": "artificial intelligence",
        "reward_xp": 10
    },
    {
        "question": "Name a popular cloud platform by IBM?",
        "answer": "ibm cloud",
        "reward_xp": 15
    },
    {
        "question": "True or False: Python is primarily a snake, not a programming language?",
        "answer": "false",
        "reward_xp": 5
    }
]

LEARNING_PATHS = {
    "Cyber Security 101": {
        "description": "A comprehensive introduction to the world of cybersecurity.",
        "difficulty": "Advanced",
        "estimated_hours": 28,
        "chapters": [
            {
                "title": "Begin Your Cybersecurity Journey",
                "description": "Learn the fundamental concepts and terminology of cybersecurity.",
                "courses": ["Intro to Cybersecurity", "CIA Triad", "Basic Terminologies"]
            },
            {
                "title": "Threats and Attacks",
                "description": "Explore common cyber threats and attack methodologies.",
                "courses": ["Common Types of Attacks", "Offensive Security Intro", "Defensive Security Intro"]
            },
            {
                "title": "Linux Fundamentals",
                "description": "Linux is widely used among many servers. Learn how to use the Linux operating system.",
                "courses": ["Linux Fundamentals - Part 1", "Linux Fundamentals - Part 2", "Linux Fundamentals - Part 3"]
            },
            {
                "title": "Networking",
                "description": "Learn how devices communicate, explore key protocols, and understand how data moves securely across networks.",
                "courses": ["Networking Fundamentals", "IP Addressing & Subnetting", "Core Networking Protocols", "Network Security Essentials", "Network Analysis with Wireshark & Nmap"]
            },
            {
                "title": "Cryptography",
                "description": "Understand how data is protected using encryption, hashing, and secure communication techniques.",
                "courses": ["Introduction to Cryptography", "Symmetric Encryption", "Asymmetric Encryption & PKI", "Hash Functions & Data Integrity", "Cryptographic Attacks & Weaknesses"]
            },
            {
                "title": "Web Hacking",
                "description": "Learn how to find, exploit, and secure vulnerabilities in web applications.",
                "courses": ["Introduction to Web Applications", "Information Gathering & Reconnaissance", "Common Web Vulnerabilities", "Authentication & Session Attacks", "Exploitation & Post-Exploitation"]
            },
            {
                "title": "Vulnerability Management & Exploitation Basics",
                "description": "Discover how to find, assess, and exploit security weaknesses, and learn the basics of patching and mitigation.",
                "courses": ["Introduction to Vulnerabilities and CVEs", "Common Vulnerability Scanning Tools", "Basics of Exploit Development", "Patch Management & Remediation Strategies"]
            },
            {
                "title": "Incident Response and Digital Forensics",
                "description": "Learn how to detect, contain, and investigate cybersecurity incidents through basic response strategies and digital forensics.",
                "courses": ["Introduction to Incident Response", "First Responder Actions", "Basics of Log Analysis", "Digital Forensics Fundamentals"]
            },
        ],
        "completion_reward_xp": 350,
        "completion_reward_badge": "Cybersecurity Foundations Badge"
    },
    "Data Science Fundamentals": {
        "description": "Master the essentials of data science from basics to machine learning.",
        "difficulty": "Beginner",
        "estimated_hours": 5,
        "chapters": [
            {
                "title": "Foundations of Data Analysis",
                "description": "Learn the core concepts of data analysis and statistics.",
                "courses": ["Python for Everybody", "Intro to Data Science"]
            },
            {
                "title": "Machine Learning Essentials",
                "description": "Understand the principles of machine learning algorithms.",
                "courses": ["Machine Learning Basics"]
            }
        ],
        "completion_reward_xp": 100,
        "completion_reward_badge": "Data Science Explorer Badge"
    },
    "Web Fundamentals": {
        "description": "A beginner's guide to understanding how websites work and how the web connects us all.",
        "difficulty": "Beginner",
        "estimated_hours": 10,
        "chapters": [
            {
                "title": "Introduction to the Web",
                "description": "Learn how the web works, including browsers, servers, and how they communicate.",
                "courses": ["What is the Web?", "How Browsers and Servers Communicate", "Basic Web Terminologies"]
            },
            {
                "title": "HTML Fundamentals",
                "description": "Understand the structure of web pages and start building with HTML.",
                "courses": ["Introduction to HTML", "HTML Tags and Elements", "Building Your First Web Page"]
            },
            {
                "title": "CSS Fundamentals",
                "description": "Learn how to style web pages with CSS to create visually appealing designs.",
                "courses": ["Introduction to CSS", "Selectors and Properties", "Basic Page Styling"]
            },
            {
                "title": "JavaScript Basics",
                "description": "Discover how JavaScript brings interactivity and logic to websites.",
                "courses": ["Introduction to JavaScript", "Variables, Functions, and Events", "Making Websites Interactive"]
            },
            {
                "title": "Web Hosting and Deployment",
                "description": "Learn how to put your website online and understand domain names and hosting services.",
                "courses": ["What is Web Hosting?", "How to Buy a Domain", "Deploying a Website"]
            }
        ],
        "completion_reward_xp": 200,
        "completion_reward_badge": "Web Fundamentals Badge"
    },
        "Management 101": {
        "description": "An essential introduction to core business management principles and practices.",
        "difficulty": "Intermediate",
        "estimated_hours": 14,
        "chapters": [
            {
                "title": "Foundations of Business",
                "description": "Learn the basics of how businesses operate, their structures, and key functional areas.",
                "courses": ["Introduction to Business", "Business Structures and Types", "Key Business Functions"]
            },
            {
                "title": "Principles of Management",
                "description": "Understand core management functions, leadership styles, and effective organizational planning.",
                "courses": ["Introduction to Management", "Leadership and Decision-Making", "Planning and Organizational Structure"]
            },
            {
                "title": "Business Strategy and Growth",
                "description": "Explore how businesses develop strategies, adapt to markets, and drive sustainable growth.",
                "courses": ["Introduction to Business Strategy", "Market Analysis Basics", "Growth and Innovation Strategies"]
            }
        ],
        "completion_reward_xp": 150,
        "completion_reward_badge": "Business Management Foundations Badge"
    },

}

COURSE_LINKS = {
    # Cyber Security 101 - Chapter 1: Begin Your Cybersecurity Journey
    "Intro to Cybersecurity": "https://example.com/intro-cybersecurity",
    "CIA Triad": "https://example.com/cia-triad",
    "Basic Terminologies": "https://example.com/basic-terminologies",
    
    # Cyber Security 101 - Chapter 2: Threats and Attacks
    "Common Types of Attacks": "https://example.com/common-attacks",
    "Offensive Security Intro": "https://example.com/offensive-security",
    "Defensive Security Intro": "https://example.com/defensive-security",
    
    # Cyber Security 101 - Chapter 3: Linux Fundamentals
    "Linux Fundamentals - Part 1": "https://example.com/linux-fundamentals-1",
    "Linux Fundamentals - Part 2": "https://example.com/linux-fundamentals-2",
    "Linux Fundamentals - Part 3": "https://example.com/linux-fundamentals-3",
    
    # Cyber Security 101 - Chapter 4: Networking
    "Networking Fundamentals": "https://example.com/networking-fundamentals",
    "IP Addressing & Subnetting": "https://example.com/ip-addressing",
    "Core Networking Protocols": "https://example.com/networking-protocols",
    "Network Security Essentials": "https://example.com/network-security",
    "Network Analysis with Wireshark & Nmap": "https://example.com/network-analysis",
    
    # Cyber Security 101 - Chapter 5: Cryptography
    "Introduction to Cryptography": "https://example.com/intro-cryptography",
    "Symmetric Encryption": "https://example.com/symmetric-encryption",
    "Asymmetric Encryption & PKI": "https://example.com/asymmetric-encryption",
    "Hash Functions & Data Integrity": "https://example.com/hash-functions",
    "Cryptographic Attacks & Weaknesses": "https://example.com/crypto-attacks",
    
    # Cyber Security 101 - Chapter 6: Web Hacking
    "Introduction to Web Applications": "https://example.com/intro-web-apps",
    "Information Gathering & Reconnaissance": "https://example.com/info-gathering",
    "Common Web Vulnerabilities": "https://example.com/web-vulnerabilities",
    "Authentication & Session Attacks": "https://example.com/auth-attacks",
    "Exploitation & Post-Exploitation": "https://example.com/exploitation",
    
    # Cyber Security 101 - Chapter 7: Vulnerability Management & Exploitation Basics
    "Introduction to Vulnerabilities and CVEs": "https://example.com/intro-vulnerabilities",
    "Common Vulnerability Scanning Tools": "https://example.com/vulnerability-scanning",
    "Basics of Exploit Development": "https://example.com/exploit-development",
    "Patch Management & Remediation Strategies": "https://example.com/patch-management",
    
    # Cyber Security 101 - Chapter 8: Incident Response and Digital Forensics
    "Introduction to Incident Response": "https://example.com/intro-incident-response",
    "First Responder Actions": "https://example.com/first-responder",
    "Basics of Log Analysis": "https://example.com/log-analysis",
    "Digital Forensics Fundamentals": "https://example.com/digital-forensics",
    
    # Data Science Fundamentals
    "Python for Everybody": "https://example.com/python-for-everybody",
    "Intro to Data Science": "https://example.com/intro-to-data-science",
    "Machine Learning Basics": "https://example.com/machine-learning-basics",
    
    # Web Fundamentals
    "What is the Web?": "https://example.com/what-is-web",
    "How Browsers and Servers Communicate": "https://example.com/browser-server",
    "Basic Web Terminologies": "https://example.com/web-terms",
    "Introduction to HTML": "https://example.com/intro-html",
    "HTML Tags and Elements": "https://example.com/html-tags",
    "Building Your First Web Page": "https://example.com/first-webpage",
    "Introduction to CSS": "https://example.com/intro-css",
    "Selectors and Properties": "https://example.com/css-selectors",
    "Basic Page Styling": "https://example.com/page-styling",
    "Introduction to JavaScript": "https://example.com/intro-javascript",
    "Variables, Functions, and Events": "https://example.com/js-basics",
    "Making Websites Interactive": "https://example.com/interactive-websites",
    "What is Web Hosting?": "https://example.com/web-hosting",
    "How to Buy a Domain": "https://example.com/buying-domains",
    "Deploying a Website": "https://example.com/website-deployment",
    
    # Business Management Fundamentals
    "Introduction to Business": "https://example.com/intro-business",
    "Business Structures and Types": "https://example.com/business-structures",
    "Key Business Functions": "https://example.com/business-functions",
    "Introduction to Management": "https://example.com/intro-management",
    "Leadership and Decision-Making": "https://example.com/leadership",
    "Planning and Organizational Structure": "https://example.com/organizational-planning",
    "Introduction to Business Strategy": "https://example.com/business-strategy",
    "Market Analysis Basics": "https://example.com/market-analysis",
    "Growth and Innovation Strategies": "https://example.com/growth-strategies"
}

import random

def initialize_course_ratings():
    """
    Prepopulate the course_ratings dictionary with realistic dummy data
    for all courses across all categories. Each course will have:
    - Between 5-30 ratings
    - Average rating between 3-5 stars (generally positive)
    """
    global course_ratings
    course_ratings = {}
    
    # Extract all courses from COURSE_LINKS
    all_courses = list(COURSE_LINKS.keys())
    
    # Initialize ratings for each course
    for course in all_courses:
        # Determine number of ratings (between 5 and 30)
        num_ratings = random.randint(5, 30)
        
        # For "trending" or popular courses, boost the number of ratings
        popular_courses = [
            "Intro to Cybersecurity", 
            "Python for Everybody", 
            "Introduction to HTML",
            "Introduction to Business",
            "Machine Learning Basics",
            "Network Security Essentials",
            "Common Web Vulnerabilities"
        ]
        if course in popular_courses:
            num_ratings = random.randint(25, 50)  # More ratings for popular courses
        
        # Generate average rating (between 3.2 and 5.0)
        # Weight toward higher ratings using beta distribution
        avg_rating = 3.2 + (1.8 * random.betavariate(5, 2))
        
        # Calculate total rating
        total_rating = round(avg_rating * num_ratings)
        
        # Store in the dictionary
        course_ratings[course] = {
            "total_rating": total_rating,
            "num_ratings": num_ratings
        }
    
    # Add more positive ratings for foundational courses
    foundational_courses = [
        "CIA Triad", 
        "Introduction to JavaScript",
        "Introduction to Management",
        "Linux Fundamentals - Part 1"
    ]
    for course in foundational_courses:
        if course in course_ratings:
            num_ratings = random.randint(30, 45)
            avg_rating = 4.5 + (0.5 * random.betavariate(8, 2))  # Higher avg (4.5-5.0)
            course_ratings[course] = {
                "total_rating": round(avg_rating * num_ratings),
                "num_ratings": num_ratings
            }
    
    # Add slightly lower ratings for more challenging courses
    challenging_courses = [
        "Cryptographic Attacks & Weaknesses",
        "Basics of Exploit Development",
        "Hash Functions & Data Integrity",
        "Exploitation & Post-Exploitation"
    ]
    for course in challenging_courses:
        if course in course_ratings:
            course_ratings[course]["total_rating"] = round(3.5 * course_ratings[course]["num_ratings"])
    
    return course_ratings

leaderboard = []

# Initialize empty course ratings dictionary
course_ratings = {}

# Initialize with dummy data
initialize_course_ratings()

#########################################
# 2. LEVEL & PROGRESSION LOGIC
#########################################

def determine_custom_level(xp: int) -> str:
    qualifying = [lvl for lvl in TEN_LEVELS if xp >= lvl["xp_needed"]]
    if not qualifying:
        return "0x1 [Initiate]"
    highest = qualifying[-1]
    return f"{highest['hex_code']} [{highest['title']}]"

def check_level_up(user_state):
    old_level = user_state["level"]
    new_level = determine_custom_level(user_state["xp"])
    user_state["level"] = new_level
    if new_level != old_level:
        return f"\n\n👏 Congratulations! You've advanced to **{new_level}**! 🚀\n\n "
    return ""

#########################################
# 3. STREAK TRACKING
#########################################

def update_streak(user_state):
    today = date.today()
    last_active_str = user_state.get("last_active_date")
    
    if last_active_str is None:
        user_state["current_streak"] = 1
        user_state["longest_streak"] = 1
        user_state["last_active_date"] = today.isoformat()
        return
    
    last_active = date.fromisoformat(last_active_str)
    if today == last_active:
        return

    diff = (today - last_active).days
    if diff == 1:
        user_state["current_streak"] += 1
        user_state["longest_streak"] = max(
            user_state["longest_streak"], user_state["current_streak"]
        )
    else:
        user_state["current_streak"] = 1
    
    user_state["last_active_date"] = today.isoformat()

#########################################
# 4. SKILL BADGES & QUEST CHECKS
#########################################

def check_skill_badges(user_state):
    newly_awarded = []
    for badge_name, req in SKILL_BADGE_REQUIREMENTS.items():
        if badge_name in user_state["badges"]:
            continue
        if all(course in user_state["completed_courses"] for course in req["courses_needed"]) \
           and user_state["xp"] >= req["min_xp"]:
            user_state["badges"].append(badge_name)
            newly_awarded.append(badge_name)
    return newly_awarded

def check_quests(user_state):
    messages = []
    for quest_name, quest_data in QUESTS.items():
        if quest_name not in user_state["active_quests"]:
            continue
        if user_state["active_quests"][quest_name]["completed"]:
            continue

        required_courses = quest_data["courses_required"]
        if all(c in user_state["completed_courses"] for c in required_courses):
            user_state["active_quests"][quest_name]["completed"] = True
            user_state["xp"] += quest_data["reward_xp"]
            user_state["badges"].append(quest_data["reward_badge"])
            msg = (
                f"\n\n\n\n🎉 You have completed the **'{quest_name}'** Quest!"
                f"You earned **{quest_data['reward_xp']} XP** + **{quest_data['reward_badge']}**!\n\n\n\n"
            )
            messages.append(msg)   
    return messages

#########################################
# 5. LEADERBOARD
#########################################

def show_leaderboard(top_n=5, user_state=None):
    """
    Display leaderboard in a formatted table without the Badges column.
    If empty, provides instructions on how to join.
    
    Args:
        top_n: Number of top entries to display
        user_state: Optional user state to check if user is on leaderboard
    
    Returns:
        Formatted string with leaderboard data
    """
    if not leaderboard:
        return (
            "The leaderboard is currently empty! Be the first to add your name and start the competition.\n\n"
            "### 💪 Ready to join the leaderboard?\n"
            "Use: `join leaderboard`\n\n"
            "Once you join, your XP and level will be displayed for others to see!"
        )
    
    sorted_lb = sorted(leaderboard, key=lambda x: x["xp"], reverse=True)
    top_entries = sorted_lb[:top_n]
    
    # Add a header above the table
    response_parts = ["## 🏆 Leaderboard 🏆", 
                      "Top performers in our learning community:\n"]
    
    # Create table headers without the Badges column
    table_lines = [
        "|| Name | XP | Level | Streak |",
        "|:--:|:----:|:--:|:-----:|:------:|"
    ]
    
    # Add entries to table with additional info (if available)
    for rank, entry in enumerate(top_entries, start=1):
        # Find additional data for this user if possible
        streak = entry.get("current_streak", "-")
        
        # Add row with available data
        table_lines.append(
            f"| {rank} | **{entry['nickname']}** | {entry['xp']} | {entry['level']} | {streak} |"
        )
    
    response_parts.extend(table_lines)
    
    # Add encouraging message at the bottom
    footer = "\n\n**🤩 Want to see your name here?** Use: `join leaderboard`"
    
    # If user_state is provided and valid, check if user is on leaderboard
    if user_state and not isinstance(user_state, gr.State):
        if user_state.get("leaderboard_nickname"):
            # Find user's position
            user_pos = next((i for i, entry in enumerate(sorted_lb) 
                            if entry["user_id"] == user_state["user_id"]), None)
            
            if user_pos is not None:
                footer = f"\n\n**Your current rank:** {user_pos + 1} of {len(sorted_lb)}"
                
                # If user is not in the top_n displayed
                if user_pos >= top_n:
                    user_entry = sorted_lb[user_pos]
                    footer += f"\n**Your stats:** {user_entry['nickname']} - {user_entry['xp']} XP (Level: {user_entry['level']})"
    
    response_parts.append(footer)
    
    return "\n".join(response_parts)

def find_user_in_leaderboard(user_id):
    for entry in leaderboard:
        if entry["user_id"] == user_id:
            return entry
    return None

def update_leaderboard(user_state):
    if not user_state.get("leaderboard_nickname"):
        return
    user_entry = find_user_in_leaderboard(user_state["user_id"])
    if user_entry:
        user_entry["xp"] = user_state["xp"]
        user_entry["level"] = user_state["level"]
        # Add streak information
        user_entry["current_streak"] = user_state.get("current_streak", 0)
    else:
        leaderboard.append({
            "user_id": user_state["user_id"],
            "nickname": user_state["leaderboard_nickname"],
            "xp": user_state["xp"],
            "level": user_state["level"],
            # Add streak information
            "current_streak": user_state.get("current_streak", 0)
        })

def join_leaderboard(user_state, nickname):
    if user_state.get("leaderboard_nickname"):
        return f"You are already on the leaderboard as **'{user_state['leaderboard_nickname']}'**."
    for entry in leaderboard:
        if entry["nickname"] == nickname:
            return "Nickname is taken. Please choose another."
    user_state["leaderboard_nickname"] = nickname
    leaderboard.append({
        "user_id": user_state["user_id"],
        "nickname": nickname,
        "xp": user_state["xp"],
        "level": user_state["level"],
        "current_streak": user_state.get("current_streak", 0)
    })
    
    # Show success message and then the updated leaderboard
    join_success = f"🙌 You have successfully joined the leaderboard as **'{nickname}'**! "
    updated_leaderboard = show_leaderboard(top_n=5, user_state=user_state)
    
    return f"{join_success}\n\n{updated_leaderboard}"

def leave_leaderboard(user_state):
    nickname = user_state.get("leaderboard_nickname")
    if not nickname:
        return (
            "You are **not** on the leaderboard yet.\n"
            "### 💪 Ready to join the leaderboard?\n"
            "Use: `join leaderboard`\n\n"
            "Once you join, your XP and level will be displayed for others to see!"
        )
    global leaderboard
    leaderboard = [e for e in leaderboard if e["user_id"] != user_state["user_id"]]
    user_state["leaderboard_nickname"] = None
    return f"You have been **removed from** the leaderboard. (Nickname was: **{nickname}**)"

#########################################
# 6. DAILY CHALLENGES (UPDATED)
#########################################

def present_daily_challenge(user_state):
    """
    Assign a new challenge to user_state["current_challenge"] if they haven't done today's.
    Return the question, instructing them to simply type their guess.
    """
    today = date.today().isoformat()
    if user_state["daily_challenge_date"] == today and user_state["daily_challenge_done"]:
        return "You've already completed today's challenge!"
    
    if user_state["daily_challenge_date"] != today:
        user_state["daily_challenge_done"] = False
    
    user_state["daily_challenge_date"] = today
    challenge = random.choice(DAILY_CHALLENGES)
    user_state["current_challenge"] = challenge
    return (
        f"🧩 Today's Challenge: **{challenge['question']}**\n"
        "Just type your guess as a message, and I'll check if it's correct!"
    )

def check_daily_challenge_answer(user_state, user_message):
    """
    Check if user_message matches the current_challenge's answer. If correct, reward XP.
    If not correct, let them try again.
    """
    if not user_state["current_challenge"]:
        return None  # Means there's no active challenge to answer.
    if user_state["daily_challenge_done"]:
        return "✅ You've already completed today's challenge."
    
    challenge = user_state["current_challenge"]
    correct_answer = challenge["answer"].lower().strip()
    user_answer = user_message.lower().strip()
    
    # If correct
    if user_answer == correct_answer:
        user_state["daily_challenge_done"] = True
        reward = challenge["reward_xp"]
        user_state["xp"] += reward
        # Reset current_challenge so it won't re-check
        user_state["current_challenge"] = None
        return f"✅ Correct! You earned **{reward} XP** for today's challenge!"
    else:
        return "🤔 That doesn't seem right. Try again!"

#########################################
# 7. QUESTS
#########################################
def start_quest(user_state, quest_name):
    # 1) Case-insensitive lookup for the quest
    quest_name_lower = quest_name.lower()
    quest_matched = None
    for q_key in QUESTS.keys():
        if q_key.lower() == quest_name_lower:
            quest_matched = q_key
            break

    if not quest_matched:
        # Enhanced error message with available and in-progress quests
        response = [f"❌ No quest named **'{quest_name}'** found."]
        
        # Add available quests - collect just the names first
        available_quests = []
        for q_name in QUESTS.keys():
            quest_status = user_state["active_quests"].get(q_name)
            if not quest_status:
                available_quests.append(q_name)
            
        if available_quests:
            response.append("\n💪 Available quests you can start:")
            
            # Limit to top 5 quests and format them with bullet points
            top_quests = available_quests[:5]
            formatted_quests = [f"- {quest}" for quest in top_quests]
            response.extend(formatted_quests)
            
            # Add message about remaining quests if there are more than 5
            if len(available_quests) > 5:
                more_count = len(available_quests) - 5
                response.append(f"*...and **{more_count}** more quests. Use `show quests` to see all.*")
        
        # Add in-progress quests - collect just the names first
        in_progress_quests = []
        for q_name, status in user_state["active_quests"].items():
            if status and not status.get("completed", False):
                in_progress_quests.append(q_name)
                
        if in_progress_quests:
            response.append("\n⏳ Quests you're currently working on:")
            
            # Limit to top 5 in-progress quests and format them with bullet points
            top_in_progress = in_progress_quests[:5]
            formatted_in_progress = [f"- {quest}" for quest in top_in_progress]
            response.extend(formatted_in_progress)
            
            # Add message about remaining quests if there are more than 5
            if len(in_progress_quests) > 5:
                more_count = len(in_progress_quests) - 5
                response.append(f"*...and **{more_count}** more quests in progress. Use `show quest progress` to see all.*")
            
        return "\n".join(response)

    # Retrieve the quest status if it exists
    existing_status = user_state["active_quests"].get(quest_matched)

    # 2) Already Completed
    if existing_status and existing_status.get("completed") is True:
        available = list_available_quests(user_state)
        return (
            f"✅ You have already completed the quest **'{quest_matched}'**!\n\n"
            f"Would you like to start a new one?\nHere are some available quests:\n{available}"
        )

    # 3) In Progress
    if existing_status and existing_status.get("completed") is False:
        # Let's show the user which courses remain
        quest_data = QUESTS[quest_matched]
        required_courses = quest_data["courses_required"]
        
        # Build a list of courses that the user has NOT yet completed
        # (We assume user_state["completed_courses"] tracks fully completed courses.)
        incomplete_courses = [
            course for course in required_courses
            if course not in user_state["completed_courses"]
        ]
        
        if incomplete_courses:
            # Bullet-point the incomplete courses with links
            bullet_lines = []
            for course in incomplete_courses:
                link = COURSE_LINKS.get(course, "https://example.com/courses")
                bullet_lines.append(f"- [{course}]({link})")
            
            courses_str = "\n".join(bullet_lines)
            
            return (
                f"⏳ You're already in the middle of this quest: **'{quest_matched}'**.\n\n"
                "Keep going to complete it!\n\n"
                f"You still need to finish:\n{courses_str}\n\n"
                "✊ You can do it! Once you've completed all the required courses, "
                "you'll earn your rewards."
            )
        else:
            # Edge case: The user might have completed all the courses 
            # but the quest hasn't been marked "completed" yet for some reason.
            # Typically your check_quests() function handles awarding XP 
            # once they've done all courses. You can handle it here or prompt them.
            return (
                f"⏳ You're already in the middle of **'{quest_matched}'**, and you've finished all "
                "required courses. Use `show quest progress` to see your progress. "
                "You might be moments away from completing it!"
            )

    # 4) Not Started => normal start flow
    user_state["active_quests"][quest_matched] = {
        "started": True,
        "completed": False,
    }

    quest_data = QUESTS[quest_matched]
    required_courses = quest_data["courses_required"]
    reward_xp = quest_data["reward_xp"]
    reward_badge = quest_data["reward_badge"]

    bullet_lines = []
    for course in required_courses:
        link = COURSE_LINKS.get(course, "https://example.com/courses")
        bullet_lines.append(f"- [{course}]({link})")

    courses_str = "\n".join(bullet_lines)

    response_msg = (
        f"🚀 You have started the **'{quest_matched}'** quest!\n\n"
        f"**Required Courses:**\n{courses_str}\n\n"
        f"**Reward XP:** {reward_xp} XP\n"
        f"**Reward Badge:** {reward_badge}\n\n"
        "Complete all required courses to finish this quest and claim your rewards.\n"
        "🌟 Best of luck on your journey!\n\n"
        "***Tip:** Use `show quest progress` to **track your progress** on this quest anytime.*"
    )

    return response_msg

def list_quests(user_state):
    """
    Returns a friendly overview of quests:
    1) Available (not started) quests with a welcoming intro line, limited to top 5
    2) In-progress quests in their own section.
    3) Completed quests in a separate section.
    """

    available_quests = []
    in_progress_quests = []
    completed_quests = []

    # Separate quests by whether the user has started them or not
    for quest_name, data in QUESTS.items():
        quest_status = user_state["active_quests"].get(quest_name)

        if not quest_status:
            # Not started
            available_quests.append(f"- **{quest_name}** - Not Started")
        else:
            # The user has started this quest; is it in progress or completed?
            if quest_status.get("completed"):
                completed_quests.append(f"- ✅ **{quest_name}** - Completed")
            else:
                in_progress_quests.append(f"- **{quest_name}** - In Progress")

    # Build the response step by step
    response_parts = []

    # 1) Available quests section - MODIFIED to limit to top 5
    if available_quests:
        response_parts.append(
            "## Available Quests"
        )
        response_parts.append(
            "💪 Here are all the available quests:\n"
        )
        
        # Limit to top 5 quests
        top_quests = available_quests[:5]
        response_parts.append("\n".join(top_quests))
        
        # Add message about remaining quests if there are more than 5
        if len(available_quests) > 5:
            more_count = len(available_quests) - 5
            response_parts.append(f"*...and **{more_count}** more quests. Use `show quest details` to see all.*")
        
        response_parts.append("\n### 💡 Want to find out more about each quest?")
        response_parts.append("Use: `show quest details`")
        
        # Extract just the quest name without the "- Not Started" part
        # first_available_quest = available_quests[0].split(" - ")[0][2:]  # Remove "- " prefix and " - Not Started" suffix
        raw_quest_with_bold = available_quests[0].split(" - ")[0][2:]  # Gets "**Quest Name**"
        first_available_quest = raw_quest_with_bold.strip('*')  # Removes the asterisks
        response_parts.append("\n### ⚔️ Ready to start a quest?")
        response_parts.append("Use: `start quest <Quest Name>`")
        response_parts.append(f"For example: `start quest {first_available_quest}`")

    # 2) In-progress quests section
    if in_progress_quests:
        # Add a blank line if there's already something above
        if available_quests:
            response_parts.append("\n---\n")
        response_parts.append("## Current Progress")
        response_parts.append("⏳ Here's your current progress so far: \n")
        response_parts.append("\n".join(in_progress_quests))
        
        response_parts.append("\n### 🔍 Want to see detailed quest progress? ")
        response_parts.append("Use: `show quest progress`")

    # 3) Completed quests section
    if completed_quests:
        # Add a blank line if there's already something above
        if available_quests or in_progress_quests:
            response_parts.append("\n---\n")
        response_parts.append("## Completed Progress")
        response_parts.append("🥳 Here are your completed quests:\n")
        response_parts.append("\n".join(completed_quests))

    # Edge case: if none of the three lists have anything
    if not (available_quests or in_progress_quests or completed_quests):
        return "❌ There are currently no quests available."
    
    
    # Return the assembled response
    return "\n".join(response_parts)

def list_available_quests(user_state) -> str:
    """
    Return a bullet-pointed list of quests that the user has NOT completed.
    If the user has started a quest but not completed it, we skip it,
    so only truly 'new' quests appear. Also limits to showing only 5 quests.
    """
    all_available = []
    for quest_name, quest_data in QUESTS.items():
        quest_status = user_state["active_quests"].get(quest_name)
        if not quest_status:  
            # Quest is not started at all
            all_available.append(quest_name)
        else:
            # If there's a status, check if it's completed
            if quest_status.get("completed") is False:
                # It's in progress; skip it, because it's not "available"
                pass
            elif quest_status.get("completed") is True:
                # It's completed, skip it
                pass
    
    # Format and limit to top 5
    if not all_available:
        return "❌ No more quests available at this time."
    
    # Get top 5 quests
    top_quests = all_available[:5]
    lines = [f"- {quest}" for quest in top_quests]
    
    # Add note about remaining quests if more than 5
    if len(all_available) > 5:
        more_count = len(all_available) - 5
        lines.append(f"*...and **{more_count}** more quests. Use `show quests` to see all.*")
    
    return "\n".join(lines)

def show_quest_details(user_state, quest_name=None):
    """
    Shows detailed information about a specific quest or all quests if no name provided.
    Displays name, description, required courses, rewards, and completion status.
    
    Args:
        user_state: The user's state dictionary
        quest_name: Optional specific quest name to show details for
        
    Returns:
        A formatted string with detailed information about quest(s)
    """
    # If no specific quest requested, list all quests with details
    if not quest_name:
        response_parts = ["## Quest Details\n"]
        
        for quest_name, quest_data in QUESTS.items():
            # Check if user has started or completed this quest
            quest_status = user_state["active_quests"].get(quest_name)
            status_text = "Not Started"
            if quest_status:
                if quest_status.get("completed", False): # pragma: no cover
                    status_text = "✅ Completed" # pragma: no cover
                else:
                    status_text = "⏳ In Progress" # pragma: no cover
            
            # Add section for this quest
            response_parts.append(f"### {quest_name} ({status_text})\n")
            
            # Add required courses with links
            response_parts.append("**Required Courses:**")
            for course in quest_data["courses_required"]:
                link = COURSE_LINKS.get(course, "https://example.com/courses")
                # Check if user has completed this course
                completed = course in user_state["completed_courses"]
                status_icon = "✅ " if completed else ""
                response_parts.append(f"- {status_icon}[{course}]({link})")
            
            # Add rewards info
            response_parts.append(f"\n**Reward XP:** {quest_data['reward_xp']} XP")
            response_parts.append(f"**Reward Badge:** {quest_data['reward_badge']}")
            
            # Add dynamic note based on quest status
            if status_text == "Not Started":
                response_parts.append(f"***Note**: Use `start quest {quest_name}` to start this quest*\n")
            elif status_text == "⏳ In Progress": # pragma: no cover
                response_parts.append(f"***Note**: Use `show quest progress` to track your current progress*\n") # pragma: no cover
            else:  # Completed
                response_parts.append(f"***Note**: Use `show quests` to see all available quests*\n") # pragma: no cover
            
        return "\n".join(response_parts)
    
    # Case-insensitive lookup for a specific quest name
    quest_name_lower = quest_name.lower()
    quest_matched = None
    for q_key in QUESTS.keys():
        if q_key.lower() == quest_name_lower:
            quest_matched = q_key
            break
            
    if not quest_matched:
        return f"❌ No quest named **'{quest_name}'** found. Use `show quests` to see **available quests**."
        
    # Get the quest data
    quest_data = QUESTS[quest_matched]
    
    # Check if user has started or completed this quest
    quest_status = user_state["active_quests"].get(quest_matched)
    status_text = "Not Started"
    
    if quest_status:
        if quest_status.get("completed", False):
            status_text = "✅ Completed"
        else:
            status_text = "⏳ In Progress"
    
    # Build comprehensive details for this quest
    response_parts = [f"# {quest_matched} - Quest Details\n"]
    response_parts.append(f"**Status:** {status_text}")
    
    # Count completed courses
    courses_completed = 0
    for course in quest_data["courses_required"]:
        if course in user_state["completed_courses"]:
            courses_completed += 1
    
    total_courses = len(quest_data["courses_required"])
    progress_percent = (courses_completed / total_courses) * 100 if total_courses > 0 else 0
    
    # Add progress bar
    # progress_bar_length = 20
    # filled_length = int(progress_bar_length * (progress_percent / 100))
    # bar = '█' * filled_length + '▒' * (progress_bar_length - filled_length)
    progress_bar_length = 16
    filled_length = int(progress_bar_length * (progress_percent / 100))
    bar = '🟩' * filled_length + '⬜' * (progress_bar_length - filled_length)
    
    
    # Add progress information
    if status_text != "Not Started":
        response_parts.append(f"**Progress:** {courses_completed}/{total_courses} courses completed ({progress_percent:.1f}%)")
        response_parts.append(f"`{bar}`")
    
    # Add reward information
    response_parts.append(f"\n**Reward XP:** {quest_data['reward_xp']} XP")
    response_parts.append(f"**Reward Badge:** {quest_data['reward_badge']}\n")
    
    # List required courses with completion status
    response_parts.append("## Required Courses\n")
    for course in quest_data["courses_required"]:
        link = COURSE_LINKS.get(course, "https://example.com/courses")
        completed = course in user_state["completed_courses"]
        status_icon = "✅ " if completed else "⏳ "
        response_parts.append(f"- {status_icon}[{course}]({link})")
    
    # Add call to action based on status
    if status_text == "Not Started":
        response_parts.append(f"\n## 🚀 Ready to begin?")
        response_parts.append(f"Use the command: `start quest {quest_matched}`")
    elif status_text == "⏳ In Progress":
        remaining_courses = [course for course in quest_data["courses_required"] 
                            if course not in user_state["completed_courses"]]
        if remaining_courses:
            response_parts.append(f"\n## ⏩ Continue your progress!")
            response_parts.append(f"Complete the remaining courses to finish this quest.")
    else:  # Completed
        response_parts.append(f"\n## 🎉 Quest Completed!")
        response_parts.append(f"You've already completed this quest and earned the rewards.")
        response_parts.append(f"Use `show quests` to find **more quests** to complete.")
    
    return "\n".join(response_parts)

def show_quest_progress(user_state):
    """
    Displays detailed progress for all quests that the user has started.
    Shows completed courses and courses still needed for each in-progress quest.
    
    Args:
        user_state: The user's state dictionary
        
    Returns:
        A formatted string with detailed quest progress information
    """
    # Get all active quests (both in-progress and completed)
    active_quests = user_state["active_quests"]
    
    # If no active quests, return a message
    if not active_quests:
        return (
            "❌ You haven't started any quests yet.\n"
            "Type `show quests` to see available quests."
        )
    
    # Check if there are any in-progress quests (not completed)
    in_progress_quests = {
        quest_name: status for quest_name, status in active_quests.items() 
        if status.get("started") and not status.get("completed", False)
    }
    
    # If no in-progress quests, only completed ones
    if not in_progress_quests:
        return (
            "❌ You have no quests in progress. All your started quests are completed.\n"
            "Type `show quests` to see available quests."
        )
    
    # Build the response showing progress for each in-progress quest
    response_parts = ["## 📈 Your Quest Progress"]

    for quest_name, status in in_progress_quests.items():
        # Get quest data
        quest_data = QUESTS.get(quest_name)
        if not quest_data:
            continue  # Skip if quest data not found (shouldn't happen)
        
        # Add quest header with name
        response_parts.append(f"### {quest_name}")
        
        # Get required courses for this quest
        required_courses = quest_data["courses_required"]
        
        # Track completed and remaining courses
        completed_courses = []
        remaining_courses = []
        
        for course in required_courses:
            if course in user_state["completed_courses"]:
                completed_courses.append(course)
            else:
                remaining_courses.append(course)
        
        # Calculate progress percentage
        progress_percent = (len(completed_courses) / len(required_courses)) * 100 if required_courses else 0
        
        # Add progress bar
        # progress_bar_length = 20
        # filled_length = int(progress_bar_length * (progress_percent / 100))
        # bar = '█' * filled_length + '▒' * (progress_bar_length - filled_length)
        progress_bar_length = 16
        filled_length = int(progress_bar_length * (progress_percent / 100))
        bar = '🟩' * filled_length + '⬜' * (progress_bar_length - filled_length)
        
        # Add progress information
        response_parts.append(f"**Progress:** {len(completed_courses)}/{len(required_courses)} courses completed ({progress_percent:.1f}%)")
        response_parts.append(f"`{bar}`")
        
        # Add reward info
        response_parts.append(f"\n**Rewards upon completion:**")
        response_parts.append(f"- {quest_data['reward_xp']} XP")
        response_parts.append(f"- {quest_data['reward_badge']}")
        
        # Add completed courses section
        if completed_courses:
            response_parts.append("\n**Completed Courses:**")
            for course in completed_courses:
                link = COURSE_LINKS.get(course, "https://example.com/courses")
                response_parts.append(f"- ✅ [{course}]({link})")
        
        # Add remaining courses section
        if remaining_courses:
            response_parts.append("\n**Courses Remaining:**")
            for course in remaining_courses:
                link = COURSE_LINKS.get(course, "https://example.com/courses")
                response_parts.append(f"- ⏳ [{course}]({link})")
        
        # Add a separator between quests
        response_parts.append("\n---\n")
    
    # Add a helpful tip at the end
    response_parts.append("💰 Complete the remaining courses to finish your quests and earn rewards!")
    
    return "\n".join(response_parts)

#########################################
# SHOW COURSES
#########################################
def show_courses(user_state):
    """
    Displays courses in a tabular format organized by category.
    Shows only uncompleted courses in the available courses list.
    Limits initial display to improve responsiveness.
    Includes ratings for each course when available.
    """
    # Get the course categories
    course_categories = get_course_categories()
    
    # Create a flat list of all available courses with their categories
    all_available_courses = []
    for category_name, courses in course_categories.items():
        for course in courses:
            all_available_courses.append((course, category_name))
    
    # Find valid completed courses (with correct casing and categories)
    valid_completed_courses = []
    for completed in user_state["completed_courses"]:
        # Check if this completed course is in our available courses (case-insensitive)
        matched_course = next(
            ((course, category) for course, category in all_available_courses if course.lower() == completed.lower()),
            None
        )
        if matched_course:
            valid_completed_courses.append(matched_course)
    
    # Create a list of completed course names (lowercase for easier comparison)
    completed_course_names_lower = [course.lower() for course, _ in valid_completed_courses]
    
    response_parts = ["## 🚀 Available Courses\n"]
    
    # Flag to track if all courses in a category are completed
    empty_categories = []
    
    # Build the response by category - showing only uncompleted courses
    # Limit courses per category
    max_courses_per_category = 3
    
    for category, courses in course_categories.items():
        # Filter out completed courses
        uncompleted_courses = [course for course in courses 
                              if course.lower() not in completed_course_names_lower]
        
        # Only add the category if it has uncompleted courses
        if uncompleted_courses:
            response_parts.append(f"### {category.upper()}")
            
            # Only show the top courses from each category
            top_courses = uncompleted_courses[:max_courses_per_category]
            
            for course in top_courses:
                link = COURSE_LINKS.get(course, "https://example.com/courses")
                
                # Add rating if available - CHANGED "ratings" to "reviews"
                course_rating_info = course_ratings.get(course)
                if course_rating_info and course_rating_info["num_ratings"] > 0:
                    avg_rating = course_rating_info["total_rating"] / course_rating_info["num_ratings"]
                    rating_display = "⭐" * round(avg_rating)
                    response_parts.append(f"- [{course}]({link}) - {rating_display} ({course_rating_info['num_ratings']} reviews)")
                else:
                    response_parts.append(f"- [{course}]({link}) - No reviews yet")
            
            # Add note if there are more courses in this category
            if len(uncompleted_courses) > max_courses_per_category:
                more_count = len(uncompleted_courses) - max_courses_per_category
                response_parts.append(f"*...and **{more_count}** more courses. Use `show {category} courses` to see all.*")
            
            # Add a blank line between categories
            response_parts.append("")
        else:
            empty_categories.append(category)
    
    # If there are categories where all courses are completed, mention them
    if empty_categories:
        if len(empty_categories) == len(course_categories):
            # Special case: All courses completed
            response_parts = ["## Congratulations! 🎉\n\nYou've completed all available courses!\n"]
        else:
            response_parts.append(f"***Note**: You've completed all courses in: {', '.join(empty_categories)}*\n")
    
    # Calculate progress statistics
    total_courses = len(all_available_courses)
    completed_count = len(valid_completed_courses)
    
    progress_percentage = (completed_count / total_courses) * 100 if total_courses > 0 else 0
    
    # Add the progress summary with a cleaner format
    response_parts.append(f"## 📈 Your Progress: {completed_count}/{total_courses} courses")
    
    # Add a visual progress bar using markdown symbols
    progress_bar_length = 16
    filled_length = int(progress_bar_length * (progress_percentage / 100))
    bar = '🟩' * filled_length + '⬜' * (progress_bar_length - filled_length)
    
    response_parts.append(f"`{bar}` ({progress_percentage:.1f}%)")
    
    # Add a dedicated section listing recent completed courses WITH TABLE FORMAT
    # Limit to 5 most recent completed courses
    if valid_completed_courses:
        response_parts.append("\n## Recent Completed Courses\n")
        
        # Add table header with Rating column - CHANGED "Rating" header
        response_parts.append("| Course | Category | Rating |")
        response_parts.append("|--------|----------|--------|")
        
        # Sort completed courses by category for better organization
        sorted_completed = sorted(valid_completed_courses, key=lambda x: x[1])
        # Show only the most recent completions (assume last in the list are most recent)
        show_count = min(5, len(sorted_completed))
        recent_completions = sorted_completed[-show_count:]
        
        for course, category in recent_completions:
            link = COURSE_LINKS.get(course, "https://example.com/courses")
            # Check if the course has a rating
            course_rating_info = course_ratings.get(course)
            if course_rating_info and course_rating_info["num_ratings"] > 0:
                avg_rating = course_rating_info["total_rating"] / course_rating_info["num_ratings"]
                rating_display = "⭐" * round(avg_rating)
                response_parts.append(f"| ✅ [{course}]({link}) | {category} | {rating_display} |")
            else:
                response_parts.append(f"| ✅ [{course}]({link}) | {category} | Not rated |") # pragma: no cover
        
        # If there are more completed courses not shown
        if len(sorted_completed) > show_count:
            more_count = len(sorted_completed) - show_count
            response_parts.append(f"\n*...and **{more_count}** more completed courses. Use `show completed courses` to see all.*")
    
    return "\n".join(response_parts)

def show_category_courses(user_state, category_name):
    """
    Shows all courses in a specific category.
    Includes ratings for each course when available.
    """
    # Get the course categories
    course_categories = get_course_categories()
    
    # Find the matching category (case-insensitive)
    matched_category = None
    for cat in course_categories.keys():
        if cat.lower() == category_name.lower():
            matched_category = cat
            break
    
    if not matched_category:
        return f"❌ Category **'{category_name}'** not found. Available categories: {', '.join(course_categories.keys())}"
    
    # Get courses in this category
    category_courses = course_categories[matched_category]
    
    # Find which courses are completed
    completed_courses = [c.lower() for c in user_state["completed_courses"]]
    
    response_parts = [f"## {matched_category.upper()} Courses\n"]
    
    # Add uncompleted courses first
    uncompleted = []
    completed = []
    
    for course in category_courses:
        if course.lower() in completed_courses:
            completed.append(course)
        else:
            uncompleted.append(course)
    
    if uncompleted:
        response_parts.append("### Available Courses")
        
        # Show available courses with average ratings
        for course in uncompleted:
            link = COURSE_LINKS.get(course, "https://example.com/courses")
            
            # Add rating if available - CHANGED "ratings" to "reviews"
            course_rating_info = course_ratings.get(course)
            if course_rating_info and course_rating_info["num_ratings"] > 0:
                avg_rating = course_rating_info["total_rating"] / course_rating_info["num_ratings"]
                rating_display = "⭐" * round(avg_rating)
                response_parts.append(f"- [{course}]({link}) - {rating_display} ({course_rating_info['num_ratings']} reviews)")
            else:
                response_parts.append(f"- [{course}]({link}) - No reviews yet") # pragma: no cover
        
        response_parts.append("")
    
    if completed:
        response_parts.append("### Completed Courses")
        # Add table header with Rating column
        response_parts.append("| Course | Rating |")
        response_parts.append("|--------|--------|")
        
        for course in completed:
            link = COURSE_LINKS.get(course, "https://example.com/courses")
            
            # Add rating if available
            course_rating_info = course_ratings.get(course)
            if course_rating_info and course_rating_info["num_ratings"] > 0:
                avg_rating = course_rating_info["total_rating"] / course_rating_info["num_ratings"]
                rating_display = "⭐" * round(avg_rating)
                response_parts.append(f"| ✅ [{course}]({link}) | {rating_display} |")
            else:
                response_parts.append(f"| ✅ [{course}]({link}) | Not rated |") # pragma: no cover
    
    return "\n".join(response_parts)

def show_completed_courses(user_state):
    """
    Shows all completed courses in a table format.
    """
    # Create a flat list of all available courses with their categories
    all_available_courses = []
    for category_name, courses in get_course_categories().items():
        for course in courses:
            all_available_courses.append((course, category_name))
    
    # Find valid completed courses (with correct casing and categories)
    valid_completed_courses = []
    for completed in user_state["completed_courses"]:
        # Check if this completed course is in our available courses (case-insensitive)
        matched_course = next(
            ((course, category) for course, category in all_available_courses if course.lower() == completed.lower()),
            None
        )
        if matched_course:
            valid_completed_courses.append(matched_course)
    
    if not valid_completed_courses:
        return "❌ You haven't completed any courses yet. Use `show courses` to see **available courses**."
    
    response_parts = ["# Your Completed Courses\n"]
    
    # Add table header
    response_parts.append("| Course | Category | Rating |")
    response_parts.append("|--------|----------|--------|")
    
    # Sort by category for better organization
    sorted_completed = sorted(valid_completed_courses, key=lambda x: x[1])
    
    for course, category in sorted_completed:
        # Check if the course has a rating
        course_rating_info = course_ratings.get(course)
        if course_rating_info and course_rating_info["num_ratings"] > 0:
            avg_rating = course_rating_info["total_rating"] / course_rating_info["num_ratings"]
            rating_display = "⭐" * round(avg_rating)
        else:
            rating_display = "Not rated" # pragma: no cover
        
        link = COURSE_LINKS.get(course, "https://example.com/courses")
        response_parts.append(f"| ✅ [{course}]({link}) | {category} | {rating_display} |")
    
    return "\n".join(response_parts)

#########################################
# 8. COURSE RECOMMENDATION LOGIC
#########################################

def get_recommendation(user_message: str) -> str:
    """
    Provides personalized course recommendations based on the user's interests,
    suggesting relevant learning paths and courses from the existing catalog.
    Also includes helpful command suggestions for users to explore further.
    """
    user_message_lower = user_message.lower()
    
    # Data Science / Machine Learning interests
    if "data science" in user_message_lower or "machine learning" in user_message_lower or "ai" in user_message_lower:
        return (
            f"I see you're interested in Data Science! 🔢\n\n"
            f"I'd recommend our 🛤️ **'Data Science Fundamentals'** learning path which includes:\n"
            f"- **'Python for Everybody'** - A perfect starting point for data analysis\n"
            f"- **'Intro to Data Science'** - Learn essential data concepts\n"
            f"- **'Machine Learning Basics'** - Explore AI fundamentals\n\n"
            f"You might also enjoy our 🎯 **'Machine Learning Apprentice'** quest which rewards you with XP and a special badge upon completion!\n\n"
            f"**Helpful commands:**\n"
            f"- Use `show learning path details Data Science Fundamentals` for the **full curriculum**\n"
            f"- Use `start learning path Data Science Fundamentals` to begin **right away**\n"
            f"- Use `show quests` to see **related data science quests**\n\n"
            f"Would you like to start one of these courses or see more options?"
        )
    
    # Cybersecurity interests
    elif "cybersecurity" in user_message_lower or "security" in user_message_lower or "hacking" in user_message_lower or "network security" in user_message_lower:
        return (
            f"Great choice! Cybersecurity is an exciting field! 🔐\n\n"
            f"I recommend our **'Cyber Security 101'** learning path which includes:\n"
            f"- **'Intro to Cybersecurity'** - Learn fundamental concepts\n"
            f"- **'CIA Triad'** - Understand the core principles of information security\n"
            f"- **'Network Security Essentials'** - Protect systems from threats\n\n"
            f"We also have specialized paths like **'Cryptography Explorer'** and **'Web Hacking Initiate'** quests that can earn you badges and XP!\n\n"
            f"**Helpful commands:**\n"
            f"- Use `show learning path details Cyber Security 101` to see **all chapters**\n"
            f"- Use `start learning path Cyber Security 101` to begin your **security journey**\n"
            f"- Use `show cybersecurity courses` for **all security-related courses**\n\n"
            f"Would you like to explore any of these options, or would you prefer something more advanced?"
        )
    
    # Web Development interests
    elif "web" in user_message_lower or "html" in user_message_lower or "css" in user_message_lower or "javascript" in user_message_lower or "web development" in user_message_lower:
        return (
            f"Web development is a fantastic choice! 💻\n\n"
            f"Our **'Web Fundamentals'** learning path is perfect for you with courses like:\n"
            f"- **'Introduction to HTML'** - Build the structure of websites\n"
            f"- **'Introduction to CSS'** - Create beautiful designs\n"
            f"- **'Introduction to JavaScript'** - Add interactivity to your sites\n\n"
            f"The **'Web Developer Starter'** quest is also great for beginners and rewards you with a special badge!\n\n"
            f"**Helpful commands:**\n"
            f"- Use `show learning path details Web Fundamentals` to explore the **full curriculum**\n" 
            f"- Use `start learning path Web Fundamentals` to begin coding **right away**\n"
            f"- Use `start quest Web Developer Starter` to earn your **first web development badge**\n\n"
            f"Ready to start building awesome websites? Which of these interests you most?"
        )
    
    # Business/Management interests
    elif "business" in user_message_lower or "management" in user_message_lower or "leadership" in user_message_lower or "strategy" in user_message_lower:
        return (
            f"Business and management skills are always valuable! 📊\n\n"
            f"I recommend our **'Management 101'** learning path which covers:\n"
            f"- **'Introduction to Business'** - Understand core business concepts\n"
            f"- **'Introduction to Management'** - Learn effective leadership skills\n"
            f"- **'Introduction to Business Strategy'** - Develop strategic thinking\n\n"
            f"The **'Business Management Foundation'** quest can help you earn extra XP and a professional badge!\n\n"
            f"**Helpful commands:**\n"
            f"- Use `show learning path details Management 101` to see the **full curriculum**\n"
            f"- Use `start learning path Management 101` to begin your **management journey**\n"
            f"- Use `show business management courses` for **all related courses**\n\n"
            f"Would you like to focus on a specific aspect of business management?"
        )
    
    # Linux/Operating Systems
    elif "linux" in user_message_lower or "operating system" in user_message_lower or "os" in user_message_lower:
        return (
            f"Linux skills are highly sought after! 🐧\n\n"
            f"Check out these courses from our **'Cyber Security 101'** path:\n"
            f"- **'Linux Fundamentals - Part 1'** - Learn basic commands\n"
            f"- **'Linux Fundamentals - Part 2'** - Explore system management\n"
            f"- **'Linux Fundamentals - Part 3'** - Master advanced techniques\n\n"
            f"These skills will give you a solid foundation for many tech careers!\n\n"
            f"**Helpful commands:**\n"
            f"- Use `show learning path details Cyber Security 101` to see the **full curriculum**\n"
            f"- Use `start learning path Cyber Security 101` to begin **learning Linux**\n"
            f"- Use `completed course 'Linux Fundamentals - Part 1'` after finishing a course\n\n"
            f"Would you like to start with Linux basics or do you have some experience already?"
        )
    
    # Networking
    elif "network" in user_message_lower or "cisco" in user_message_lower or "routing" in user_message_lower:
        return (
            f"Networking is a critical field in IT! 🌐\n\n"
            f"From our **'Cyber Security 101'** path, I recommend:\n"
            f"- **'Networking Fundamentals'** - Understand how networks function\n"
            f"- **'IP Addressing & Subnetting'** - Master IP management\n"
            f"- **'Core Networking Protocols'** - Learn how devices communicate\n\n"
            f"The **'Network Security Novice'** quest would be perfect for building your skills!\n\n"
            f"**Helpful commands:**\n"
            f"- Use `show learning path details Cyber Security 101` to explore **networking modules**\n"
            f"- Use `start quest Network Security Novice` to begin the **networking quest**\n"
            f"- Use `show trending courses` to see **popular networking courses**\n\n"
            f"Would you like to focus on basic networking or network security aspects?"
        )
    
    # Career change/beginners
    elif "career change" in user_message_lower or "beginner" in user_message_lower or "starting out" in user_message_lower or "new to" in user_message_lower:
        return (
            f"Exciting to see you starting a new journey in tech! 🤖\n\n"
            f"For beginners, I recommend:\n"
            f"- **'Web Fundamentals'** learning path - Friendly introduction to web technologies\n"
            f"- **'Cyber Security 101'** - Start with 'Basic Terminologies' course\n"
            f"- **'Python for Everybody'** - Great first programming language\n\n"
            f"All these paths are marked as beginner-friendly and will help you build confidence!\n\n"
            f"**Helpful commands:**\n"
            f"- Use `list learning paths` to see **all available learning journeys**\n"
            f"- Use `show profile` to **track your progress** as you learn\n"
            f"- Use `daily challenge` for a quick way to **earn XP every day**\n\n"
            f"Do any of these areas spark your interest? I can recommend specific starting points."
        )
    
    # Catch-all for other or unclear interests
    else:
        return (
            f"I'd love to help you find the perfect courses! 😊\n\n"
            f"We have several popular learning paths 🛤️:\n"
            f"- **'Cyber Security 101'** - Explore the world of digital security\n"
            f"- **'Data Science Fundamentals'** - Learn to analyze data and build models\n"
            f"- **'Web Fundamentals'** - Create websites and web applications\n"
            f"- **'Management 101'** - Develop essential business leadership skills\n\n"
            f"**Helpful commands:**\n"
            f"- Use `list learning paths` to see **all learning paths with details**\n"
            f"- Use `show courses` to browse **all available courses**\n"
            f"- Use `show trending courses` to see **what's popular right now**\n"
            f"- Use `help all` for a list of **all available commands** for **every feature**\n\n"
            f"What topics are you most interested in exploring today?"
        )

#########################################
# 9. COURSE RATING FUNCTIONALITY
#########################################

def process_course_completion(user_state, course_name) -> Tuple[str, Optional[str]]:
    """
    Process a user's claim of completing a course, verifying the course exists first.
    Returns a tuple with response message and course name if rating is needed.
    """
    # Clean up the course name by removing any extra quotes
    clean_course_name = course_name.strip("'\"")
    
    # Create a flat list of all available courses from all categories
    all_available_courses = []
    for category, courses in get_course_categories().items():
        for course in courses:
            all_available_courses.append((course, category))
    
    # Check if the course exists (case-insensitive)
    matched_course = next(
        ((c, cat) for c, cat in all_available_courses if c.lower() == clean_course_name.lower()), 
        None
    )
    
    # If the course doesn't exist in our system
    if not matched_course:
        # Generate a list of uncompleted courses, similar to show_courses
        # Find valid completed courses first
        valid_completed_courses = []
        for completed in user_state["completed_courses"]:
            # Check if this completed course is in our available courses (case-insensitive)
            completed_match = next(
                ((course, category) for course, category in all_available_courses if course.lower() == completed.lower()),
                None
            )
            if completed_match:
                valid_completed_courses.append(completed_match)
    
        # Create a list of completed course names (lowercase for easier comparison)
        completed_course_names_lower = [course.lower() for course, _ in valid_completed_courses]
    
        response_parts = [f"Unfortunately, **'{clean_course_name}'** does not exist in our course catalog. **No** XP has been awarded.\n"]
        response_parts.append("Here are some popular courses you might want to complete:\n")
    
        # Build the response by category - showing only the top 3 uncompleted courses from each category with reviews
        for category, courses in get_course_categories().items():
            # Filter out completed courses
            uncompleted_courses = [course for course in courses 
                                if course.lower() not in completed_course_names_lower]
        
            # Only add the category if it has uncompleted courses
            if uncompleted_courses:
                response_parts.append(f"**{category}**")
            
                # Only show the top 3 courses from each category
                top_courses = uncompleted_courses[:3]
            
                for course in top_courses:
                    link = COURSE_LINKS.get(course, "https://example.com/courses")
                    # Add rating if available
                    course_rating_info = course_ratings.get(course)
                    if course_rating_info and course_rating_info["num_ratings"] > 0:
                        avg_rating = course_rating_info["total_rating"] / course_rating_info["num_ratings"]
                        rating_display = "⭐" * round(avg_rating)
                        response_parts.append(f"- [{course}]({link}) - {rating_display} ({course_rating_info['num_ratings']} reviews)")
                    else:
                        response_parts.append(f"- [{course}]({link}) - No reviews yet") # pragma: no cover
            
                # Add a note if there are more courses in this category
                if len(uncompleted_courses) > 3:
                    more_count = len(uncompleted_courses) - 3
                    response_parts.append(f"*...and **{more_count}** more courses. Use `show courses` to see all.*")
            
                # Add a blank line between categories
                response_parts.append("")
    
        return "\n".join(response_parts), None
    
    # Extract just the course name from the matched tuple
    matched_course_name, _ = matched_course
    
    # Check if the user has already completed this course
    existing_course = next(
        (c for c in user_state["completed_courses"] if c.lower() == matched_course_name.lower()), 
        None
    )
    
    if not existing_course:
        # Add the matched course name (with correct capitalization) to completed courses
        user_state["completed_courses"].append(matched_course_name)
        base_xp = 50
        user_state["xp"] += base_xp
        
        # Add flag to check learning path progress
        user_state["pending_notifications"]["learning_path_check_needed"] = True
        
        return (
            f"🎓 Congratulations on completing **'{matched_course_name}'**! You earned **{base_xp} XP**.",
            matched_course_name  # Return the course name for immediate rating
        )
    else:
        return (
            f"✔️ You've already completed **'{existing_course}'**. **No** additional XP awarded.\n\n",
            None
        )

def get_course_categories():
    """
    Returns a dictionary of course categories and their courses,
    aligned with the LEARNING_PATHS structure.
    """
    return {
        "Cybersecurity": [
            # Chapter 1
            "Intro to Cybersecurity",
            "CIA Triad",
            "Basic Terminologies",
            # Chapter 2
            "Common Types of Attacks",
            "Offensive Security Intro",
            "Defensive Security Intro",
            # Chapter 3
            "Linux Fundamentals - Part 1",
            "Linux Fundamentals - Part 2",
            "Linux Fundamentals - Part 3",
            # Chapter 4
            "Networking Fundamentals",
            "IP Addressing & Subnetting",
            "Core Networking Protocols",
            "Network Security Essentials",
            "Network Analysis with Wireshark & Nmap",
            # Chapter 5
            "Introduction to Cryptography",
            "Symmetric Encryption",
            "Asymmetric Encryption & PKI",
            "Hash Functions & Data Integrity",
            "Cryptographic Attacks & Weaknesses",
            # Chapter 6
            "Introduction to Web Applications",
            "Information Gathering & Reconnaissance",
            "Common Web Vulnerabilities",
            "Authentication & Session Attacks",
            "Exploitation & Post-Exploitation",
            # Chapter 7
            "Introduction to Vulnerabilities and CVEs",
            "Common Vulnerability Scanning Tools",
            "Basics of Exploit Development",
            "Patch Management & Remediation Strategies",
            # Chapter 8
            "Introduction to Incident Response",
            "First Responder Actions",
            "Basics of Log Analysis",
            "Digital Forensics Fundamentals"
        ],
        "Data Science": [
            "Python for Everybody",
            "Intro to Data Science",
            "Machine Learning Basics"
        ],
        "Web Development": [
            "What is the Web?",
            "How Browsers and Servers Communicate",
            "Basic Web Terminologies",
            "Introduction to HTML",
            "HTML Tags and Elements",
            "Building Your First Web Page",
            "Introduction to CSS",
            "Selectors and Properties",
            "Basic Page Styling",
            "Introduction to JavaScript",
            "Variables, Functions, and Events",
            "Making Websites Interactive",
            "What is Web Hosting?",
            "How to Buy a Domain",
            "Deploying a Website"
        ],
        "Business Management": [
            "Introduction to Business",
            "Business Structures and Types",
            "Key Business Functions",
            "Introduction to Management",
            "Leadership and Decision-Making",
            "Planning and Organizational Structure",
            "Introduction to Business Strategy",
            "Market Analysis Basics",
            "Growth and Innovation Strategies"
        ]
    }

def format_course_list():
    """
    Creates a formatted string of all available courses by category.
    """
    course_categories = get_course_categories()
    lines = []
    
    for category, courses in course_categories.items():
        lines.append(f"**{category}**")
        for course in courses:
            link = COURSE_LINKS.get(course, "https://example.com/courses")
            lines.append(f"- [{course}]({link})")
        lines.append("")  # Add blank line between categories
    
    return "\n".join(lines)

def rate_course(user_state, course_name, rating_str):
    try:
        rating = int(rating_str)
        if not 1 <= rating <= 5:
            return f"Please provide a rating between 1 and 5 for '{course_name}'."
        
        # Check if this course is in the completed courses
        matched_course = next(
            (c for c in user_state["completed_courses"] if c.lower() == course_name.lower()),
            None
        )
        if not matched_course:
            return f"❌ You haven't completed '{course_name}' yet."
        
        # Update course ratings
        if matched_course not in course_ratings:
            course_ratings[matched_course] = {"total_rating": 0, "num_ratings": 0} # pragma: no cover
        
        course_ratings[matched_course]["total_rating"] += rating
        course_ratings[matched_course]["num_ratings"] += 1

        feedback_xp = 10
        user_state["xp"] += feedback_xp

        return (
            f"🙌 Thank you for rating **'{matched_course}'** **{rating}/5** stars!"
            f"\nYou earned ✨ **{feedback_xp} XP** for providing feedback.\n\n"
            f"\n---\n"
        )
    except ValueError:
        return "Please provide a numeric rating between 1 and 5."

def get_course_average_rating(course_name):
    matched_course = next(
        (c for c in course_ratings if c.lower() == course_name.lower()),
        None
    )
    if not matched_course or course_ratings[matched_course]["num_ratings"] == 0:
        return "No ratings yet"
    
    total = course_ratings[matched_course]["total_rating"]
    count = course_ratings[matched_course]["num_ratings"]
    avg = total / count
    return f"{avg:.1f}/5 ({count} ratings)"

#########################################
# 10. LEARNING PATHS IMPLEMENTATION
#########################################

def initialize_learning_paths_in_user_state(user_state):
    """
    Initialize the learning_paths_progress entry in user_state if it doesn't exist.
    """
    if "learning_paths_progress" not in user_state:
        user_state["learning_paths_progress"] = {}
    return user_state

def start_learning_path(user_state, path_name):
    """
    Start a learning path for the user if it exists.
    Returns a message indicating success or failure.
    """
    # Initialize if needed
    user_state = initialize_learning_paths_in_user_state(user_state)
    
    # 1) Case-insensitive lookup for the learning path
    path_name_lower = path_name.lower()
    path_matched = None
    for p_key in LEARNING_PATHS.keys():
        if p_key.lower() == path_name_lower:
            path_matched = p_key
            break

    if not path_matched:
        # Enhanced error message with available and in-progress paths
        response = [f"❌ No learning path named **'{path_name}'** found."]
        
        # Add available paths - store as dictionaries for table formatting
        available_paths = []
        for p_name in LEARNING_PATHS.keys():
            path_status = user_state["learning_paths_progress"].get(p_name)
            if not path_status:
                p_data = LEARNING_PATHS[p_name]
                available_paths.append({
                    "name": p_name,
                    "difficulty": p_data["difficulty"],
                    "hours": p_data["estimated_hours"]
                })
            
        if available_paths:
            response.append("\n#### 🚀 Available learning paths you can start:")
            
            # Format paths as a table
            table_parts = []
            table_parts.append("| Learning Path | Difficulty Level | Estimated Time |")
            table_parts.append("|--------------|------------------|----------------|")
            
            for path in available_paths:
                table_parts.append(f"| {path['name']} | {path['difficulty']} | {path['hours']} hours |")
            
            response.extend(table_parts)
            
            # Add tip about how to start a learning path
            response.append("\n***Tip:** To **begin a learning path**, use `start learning path <Learning Path Name>`*")
            response.append("For example: `start learning path " + (available_paths[0]["name"] if available_paths else "Data Science Fundamentals") + "`")
        
        # Add in-progress paths as bullet points
        in_progress_paths = []
        for p_name, status in user_state["learning_paths_progress"].items():
            if status and not status.get("completed", False):
                # Calculate progress for more meaningful information
                chapters_completed = len(status.get("chapters_completed", []))
                total_chapters = len(LEARNING_PATHS[p_name]["chapters"])
                progress_percent = (chapters_completed / total_chapters) * 100 if total_chapters > 0 else 0
                
                # Add as formatted bullet point with progress
                in_progress_paths.append(f"- **{p_name}** - {chapters_completed}/{total_chapters} chapters completed ({progress_percent:.1f}%)")
                
        if in_progress_paths:
            response.append("\n#### ⏳ Learning paths you're currently working on:")
            response.extend(in_progress_paths)
            
            # Add tip about how to start a learning path
            response.append("\n*💡 **Tip:** To **track your current progress**, use `show learning path progress`*")
            
        return "\n".join(response)

    # Retrieve the path status if it exists
    existing_status = user_state["learning_paths_progress"].get(path_matched)

    # 2) Already Completed
    if existing_status and existing_status.get("completed") is True:
        available = list_available_learning_paths(user_state)
        return (
            f"You have already completed the learning path **'{path_matched}'**!\n\n"
            f"Would you like to start a new one?\nHere are some available learning paths:\n{available}"
        )

    # 3) In Progress
    if existing_status and existing_status.get("completed") is False:
        # Let's show the user which chapter they're on and their progress
        path_data = LEARNING_PATHS[path_matched]
        current_chapter_idx = existing_status.get("current_chapter", 0)
        
        if current_chapter_idx < len(path_data["chapters"]):
            current_chapter = path_data["chapters"][current_chapter_idx]
            
            # Build a list of courses in the current chapter that the user has NOT yet completed
            incomplete_courses = [
                course for course in current_chapter["courses"]
                if course not in user_state["completed_courses"]
            ]
            
            chapters_completed = existing_status.get("chapters_completed", [])
            total_chapters = len(path_data["chapters"])
            completion_percentage = (len(chapters_completed) / total_chapters) * 100
            
            if incomplete_courses:
                # Bullet-point the incomplete courses with links
                bullet_lines = []
                for course in incomplete_courses:
                    link = COURSE_LINKS.get(course, "https://example.com/courses")
                    bullet_lines.append(f"- [{course}]({link})")
                
                courses_str = "\n".join(bullet_lines)
                
                return (
                    f"⏳ You're already in the middle of the learning path: '{path_matched}'.\n\n"
                    f"**Current Chapter:** {current_chapter['title']}\n"
                    f"**Progress:** {len(chapters_completed)}/{total_chapters} chapters completed ({completion_percentage:.1f}%)\n\n"
                    f"You still need to finish these courses in the current chapter:\n{courses_str}\n\n"
                    "💪 Keep going to complete this chapter!"
                )
            else:
                # All courses in the current chapter are completed
                return (
                    f"⏳ You're already in the middle of the learning path: '{path_matched}'.\n\n"
                    f"**Current Chapter:** {current_chapter['title']}\n"
                    f"**Progress:** {len(chapters_completed)}/{total_chapters} chapters completed ({completion_percentage:.1f}%)\n\n"
                    "You've completed all the courses in the current chapter! "
                    "Use `check chapter completion` to update your progress."
                )
        else:
            # Edge case: All chapters might be completed but the path hasn't been marked completed
            return (
                f"⏳ You're already in the middle of **'{path_matched}'**, and you've completed all chapters. "
                "Use `check learning path progress` to **update your status**."
            )

    # 4) Not Started => normal start flow
    user_state["learning_paths_progress"][path_matched] = {
        "started": True,
        "current_chapter": 0,
        "chapters_completed": [],
        "completed": False
    }

    path_data = LEARNING_PATHS[path_matched]
    first_chapter = path_data["chapters"][0]
    
    bullet_lines = []
    for course in first_chapter["courses"]:
        link = COURSE_LINKS.get(course, "https://example.com/courses")
        bullet_lines.append(f"- [{course}]({link})")

    courses_str = "\n".join(bullet_lines)

    response_msg = (
        f"You have started the Learning Path: **'{path_matched}'**!\n\n"
        f"**Description:** {path_data['description']}\n"
        f"**Difficulty:** {path_data['difficulty']}\n"
        f"**Estimated Hours:** {path_data['estimated_hours']}\n"
        f"**Total Chapters:** {len(path_data['chapters'])}\n\n"
        f"**First Chapter: {first_chapter['title']}**\n"
        f"{first_chapter['description']}\n\n"
        f"**Required Courses:**\n{courses_str}\n\n"
        f"**Complete Reward:** {path_data['completion_reward_xp']} XP + {path_data['completion_reward_badge']}\n\n"
        "Complete all required courses in each chapter to progress through this learning path!"
    )

    return response_msg

def list_learning_paths(user_state):
    """
    Returns a friendly overview of all learning paths with refined formatting:
    1) Available paths in a table
    2) In-progress paths in a separate table with progress details
    3) Completed paths as a simple checkmarked list
    """
    # Initialize if needed
    user_state = initialize_learning_paths_in_user_state(user_state)
    
    available_paths = []
    in_progress_paths = []
    completed_paths = []

    # Separate paths by whether the user has started them or not
    for path_name, path_data in LEARNING_PATHS.items():
        path_status = user_state["learning_paths_progress"].get(path_name)

        if not path_status:
            # Not started - store relevant data for the table
            available_paths.append({
                "name": path_name,
                "difficulty": path_data["difficulty"],
                "hours": path_data["estimated_hours"]
            })
        else:
            # The user has started this path; is it in progress or completed?
            if path_status.get("completed"):
                completed_paths.append(path_name)
            else:
                # Calculate progress
                chapters_completed = len(path_status.get("chapters_completed", []))
                total_chapters = len(path_data["chapters"])
                progress_percent = (chapters_completed / total_chapters) * 100 if total_chapters > 0 else 0
                
                in_progress_paths.append({
                    "name": path_name,
                    "chapters_completed": chapters_completed,
                    "total_chapters": total_chapters,
                    "progress": f"{progress_percent:.1f}%"
                })

    # Build the response
    response_parts = []

    # 1) Available paths section - Table format
    if available_paths:
        response_parts.append("## 🚀 Available Learning Paths\nHere are learning paths you can start anytime:\n")
        
        # Create a markdown table - REMOVED Description column
        response_parts.append("| Learning Path | Difficulty Level | Estimated Time |")
        response_parts.append("|--------------|------------|----------------|")
        
        for path in available_paths:
            response_parts.append(f"| {path['name']} | {path['difficulty']} | {path['hours']} hours |")

    # 2) In-progress paths section - Simplified table focused on progress
    if in_progress_paths:
        # Add a blank line if there's already something above
        if response_parts:
            response_parts.append("\n")
        response_parts.append("## ⏳ In-Progress Learning Paths\nContinue your learning journey:\n")
        
        # Create a simplified markdown table focused on progress
        response_parts.append("| Course Name | Chapters Completed | Progress |")
        response_parts.append("|------------|-------------------|----------|")
        
        for path in in_progress_paths:
            response_parts.append(f"| {path['name']} | {path['chapters_completed']}/{path['total_chapters']} | {path['progress']} |")

    # 3) Completed paths section - Simple checkmarked list
    if completed_paths:
        # Add a blank line if there's already something above
        if response_parts:
            response_parts.append("\n")
        response_parts.append("## 🥳 Completed Learning Paths\nYou've mastered these paths:\n")
        
        # Create a simple checkmarked list
        for path_name in completed_paths:
            response_parts.append(f"✅ **{path_name}**")

    # Edge case: if none of the three lists have anything
    if not (available_paths or in_progress_paths or completed_paths):
        return "❌ There are currently **no** learning paths available."
    
    # ADD THE NEW SECTION - Information about detailed path view right after the tables
    response_parts.append("\n### 🔎 Want to find out more about each learning path?")
    response_parts.append("Use: `show learning path details`")
    
    # Add command suggestions at the end
    if available_paths:
        response_parts.append("\n### 🚀 Ready to start a new learning path?")
        response_parts.append("Use: `start learning path <Learning Path Name>`")
        response_parts.append("For example: `start learning path " + available_paths[0]["name"] + "`")
    
    if in_progress_paths:
        response_parts.append("\n### 📄 Want to see detailed progress?")
        response_parts.append("Use: `show learning path progress`")

    # Return the assembled response
    return "\n".join(response_parts)

def list_available_learning_paths(user_state):
    """
    Return a bullet-pointed list of learning paths that the user has NOT started.
    """
    # Initialize if needed
    user_state = initialize_learning_paths_in_user_state(user_state)
    
    lines = []
    for path_name, path_data in LEARNING_PATHS.items():
        path_status = user_state["learning_paths_progress"].get(path_name)
        if not path_status:  
            # Path is not started at all - REMOVED description
            lines.append(
                f"- **{path_name}** ({path_data['difficulty']} - {path_data['estimated_hours']} hours)"
            )
    
    if not lines:
        return "❌ No more learning paths available at this time."
    
    return "\n".join(lines)

def show_learning_path_details(user_state, path_name=None):
    """
    Shows detailed information about a specific learning path or all paths if no name provided.
    Displays name, description, difficulty level, estimated time, and chapter/course structure.
    
    Args:
        user_state: The user's state dictionary
        path_name: Optional specific path name to show details for
        
    Returns:
        A formatted string with detailed information about learning path(s)
    """
    # Initialize if needed
    user_state = initialize_learning_paths_in_user_state(user_state)
    
    # If no specific path requested, list all paths with details
    if not path_name:
        response_parts = ["## Learning Path Details\n"]
        
        for path_name, path_data in LEARNING_PATHS.items():
            # Check if user has started or completed this path
            path_status = user_state["learning_paths_progress"].get(path_name)
            status_text = "Not Started"
            if path_status:
                if path_status.get("completed", False):
                    status_text = "✅ Completed" # pragma: no cover
                else:
                    # Calculate progress
                    chapters_completed = len(path_status.get("chapters_completed", []))
                    total_chapters = len(path_data["chapters"])
                    progress_percent = (chapters_completed / total_chapters) * 100 if total_chapters > 0 else 0
                    status_text = f"⏳ In Progress ({progress_percent:.1f}%)"
            
            # Add section for this path
            response_parts.append(f"### {path_name} ({status_text})\n")
            response_parts.append(f"**Description:** {path_data['description']}")
            response_parts.append(f"**Difficulty Level:** {path_data['difficulty']}")
            response_parts.append(f"**Estimated Time:** {path_data['estimated_hours']} hours")
            response_parts.append(f"**Total Chapters:** {len(path_data['chapters'])}")
            
            # Add rewards info
            response_parts.append(f"**Completion Rewards:** {path_data['completion_reward_xp']} XP + {path_data['completion_reward_badge']}\n")
            
            # Preview first chapter only to avoid too much detail in the overview
            first_chapter = path_data['chapters'][0]
            response_parts.append(f"**First Chapter:** {first_chapter['title']}")
            response_parts.append(f"*{first_chapter['description']}*\n")
            
            # Add a more subtle note about how to get more details
            response_parts.append(f"***Note**: Use `show learning path details {path_name}` for **full chapter** and **course listing***")
            response_parts.append(f"\n")
            
        return "\n".join(response_parts)
    
    # Case-insensitive lookup for a specific path name
    path_name_lower = path_name.lower()
    path_matched = None
    for p_key in LEARNING_PATHS.keys():
        if p_key.lower() == path_name_lower:
            path_matched = p_key
            break
            
    if not path_matched:
        return f"❌ No learning path named **'{path_name}'** found. Use `list learning paths` to see **available paths**."
        
    # Get the path data
    path_data = LEARNING_PATHS[path_matched]
    
    # Check if user has started or completed this path
    path_status = user_state["learning_paths_progress"].get(path_matched)
    status_text = "Not Started"
    current_chapter = 0
    
    if path_status:
        if path_status.get("completed", False):
            status_text = "✅ Completed" # pragma: no cover
        else:
            # Calculate progress
            current_chapter = path_status.get("current_chapter", 0)
            chapters_completed = len(path_status.get("chapters_completed", []))
            total_chapters = len(path_data["chapters"])
            progress_percent = (chapters_completed / total_chapters) * 100 if total_chapters > 0 else 0
            status_text = f"⏳ In Progress ({progress_percent:.1f}%)"
    
    # Build comprehensive details for this path
    response_parts = [f"# {path_matched} - Learning Path Details\n"]
    response_parts.append(f"**Status:** {status_text}")
    response_parts.append(f"**Description:** {path_data['description']}")
    response_parts.append(f"**Difficulty Level:** {path_data['difficulty']}")
    response_parts.append(f"**Estimated Time:** {path_data['estimated_hours']} hours")
    response_parts.append(f"**Total Chapters:** {len(path_data['chapters'])}")
    response_parts.append(f"**Completion Rewards:** {path_data['completion_reward_xp']} XP + '{path_data['completion_reward_badge']}' badge\n")
    
    # Show all chapters with their courses
    response_parts.append("## Chapter Breakdown\n")
    
    for idx, chapter in enumerate(path_data['chapters']):
        # Determine chapter status
        chapter_status = ""
        if path_status:
            if idx in path_status.get("chapters_completed", []):
                chapter_status = " ✅"
            elif idx == current_chapter and not path_status.get("completed", False):
                chapter_status = " ⏳ (Current)"
        
        response_parts.append(f"### Chapter {idx + 1}: {chapter['title']}{chapter_status}")
        response_parts.append(f"*{chapter['description']}*\n")
        
        # List courses in this chapter
        response_parts.append("**Courses:**")
        for course in chapter['courses']:
            link = COURSE_LINKS.get(course, "https://example.com/courses")
            # Check if user has completed this course
            completed = course in user_state["completed_courses"]
            status_icon = "✅ " if completed else ""
            response_parts.append(f"- {status_icon}[{course}]({link})")
        
        response_parts.append("")  # Empty line between chapters
    
    # Add call to action based on status
    if status_text == "Not Started":
        response_parts.append("\n## 🚀 Ready to begin?")
        response_parts.append(f"Use the command: `start learning path {path_matched}`")
    elif "In Progress" in status_text:
        response_parts.append(f"\n**⏩ Continue your progress!** Use `show learning path progress` to see **what's next**.")
    
    return "\n".join(response_parts)

def show_learning_path_progress(user_state, path_name=None):
    """
    Shows detailed progress for a specific learning path,
    or a summary of all in-progress paths if path_name is None.
    Enhanced with visual progress bars and more detailed statistics.
    """
    # Initialize if needed
    user_state = initialize_learning_paths_in_user_state(user_state)
    
    # If no path_name provided, show summary of all in-progress paths
    if not path_name:
        in_progress = []
        completed_paths = []
        
        # First collect all paths data
        for path_name, status in user_state["learning_paths_progress"].items():
            path_data = LEARNING_PATHS.get(path_name)
            if not path_data:
                continue # pragma: no cover
                
            if status.get("completed", False):
                completed_paths.append(path_name)
            elif status:  # In progress
                chapters_completed = len(status.get("chapters_completed", []))
                total_chapters = len(path_data["chapters"])
                progress_percent = (chapters_completed / total_chapters) * 100 if total_chapters > 0 else 0
                
                # Add progress bar
                # progress_bar_length = 20
                # filled_length = int(progress_bar_length * (progress_percent / 100))
                # bar = '█' * filled_length + '▒' * (progress_bar_length - filled_length)
                progress_bar_length = 16
                filled_length = int(progress_bar_length * (progress_percent / 100))
                bar = '🟩' * filled_length + '⬜' * (progress_bar_length - filled_length)
                
                # Calculate courses completed
                completed_courses = 0
                total_courses = 0
                for chapter in path_data["chapters"]:
                    total_courses += len(chapter["courses"])
                    for course in chapter["courses"]:
                        if course in user_state["completed_courses"]:
                            completed_courses += 1
                
                # Calculate time invested and remaining (based on estimated hours)
                total_time = path_data["estimated_hours"]
                time_invested = (completed_courses / total_courses) * total_time if total_courses > 0 else 0
                time_remaining = total_time - time_invested
                
                # Store all this information for sorting and display
                in_progress.append({
                    "name": path_name,
                    "chapters_completed": chapters_completed,
                    "total_chapters": total_chapters,
                    "progress_percent": progress_percent,
                    "progress_bar": bar,
                    "difficulty": path_data["difficulty"],
                    "completed_courses": completed_courses,
                    "total_courses": total_courses,
                    "time_invested": time_invested,
                    "time_remaining": time_remaining,
                    "reward_xp": path_data["completion_reward_xp"],
                    "reward_badge": path_data["completion_reward_badge"]
                })
        
        # Sort in-progress paths by progress percentage (descending)
        in_progress.sort(key=lambda x: x["progress_percent"], reverse=True)
        
        if not in_progress and not completed_paths:
            return "You haven't started any learning paths yet. Use `list learning paths` to see **available options**."
        
        response_parts = ["# Your Learning Path Progress\n"]
        
        # Show in-progress paths with enhanced visualization
        if in_progress:
            response_parts.append("## ⏳ In-Progress Learning Paths\n")
            
            for path in in_progress:
                response_parts.append(f"### {path['name']} ({path['difficulty']})")
                response_parts.append(f"**Progress:** {path['chapters_completed']}/{path['total_chapters']} chapters completed ({path['progress_percent']:.1f}%)")
                response_parts.append(f"`{path['progress_bar']}`")
                response_parts.append(f"**Courses Completed:** {path['completed_courses']}/{path['total_courses']}")
                response_parts.append(f"**Time Investment:** ~{path['time_invested']:.1f} hours invested, ~{path['time_remaining']:.1f} hours remaining")
                
                # Add call-to-action
                response_parts.append(f"\n*To see detailed chapter progress: `show learning path progress {path['name']}`*")
                response_parts.append("---\n")
        
        # Show completed paths as a simple list
        if completed_paths:
            response_parts.append("## 🥳 Completed Learning Paths")
            for path in completed_paths:
                path_data = LEARNING_PATHS.get(path)
                if path_data:
                    response_parts.append(f"✅ **{path}** - Earned: {path_data['completion_reward_xp']} XP + '{path_data['completion_reward_badge']}' badge")
            response_parts.append("")
        
        # Add tips
        if in_progress:
            response_parts.append("\n💡 **Tips:**")
            response_parts.append("- Complete all courses in a chapter to advance to the next chapter")
            response_parts.append("- Use `check chapter completion` to update your **progress after completing courses**")
            response_parts.append("- Use `show learning path details <path name>` to see the **full curriculum**")
        
        return "\n".join(response_parts)
    
    # Case-insensitive lookup for the learning path
    path_name_lower = path_name.lower()
    path_matched = None
    for p_key in LEARNING_PATHS.keys():
        if p_key.lower() == path_name_lower:
            path_matched = p_key
            break
            
    if not path_matched:
        return f"❌ No learning path named **'{path_name}'** found. Use `list learning paths` to see **available paths**."
        
    path_status = user_state["learning_paths_progress"].get(path_matched)
    if not path_status:
        return f"You haven't started the **'{path_matched}'** learning path yet. Use `start learning path {path_matched}` to **begin**."
        
    path_data = LEARNING_PATHS[path_matched]
    
    # If the path is completed
    if path_status.get("completed", False):
        # Calculate total stats for the completed path
        total_courses = sum(len(chapter["courses"]) for chapter in path_data["chapters"])
        total_chapters = len(path_data["chapters"])
        
        return (
            f"# {path_matched} - COMPLETED 🏆\n\n"
            f"## Congratulations!\n"
            f"You've successfully completed this learning path with:\n"
            f"- **{total_chapters}** chapters mastered\n"
            f"- **{total_courses}** courses completed\n"
            f"- **{path_data['estimated_hours']}** hours of learning\n\n"
            f"## Rewards Earned\n"
            f"- **{path_data['completion_reward_xp']}** XP\n"
            f"- **'{path_data['completion_reward_badge']}'**\n\n"
            f"*Feel free to explore other learning paths with `list learning paths`.*"
        )
    
    # If the path is in progress
    current_chapter_idx = path_status.get("current_chapter", 0)
    chapters_completed = path_status.get("chapters_completed", [])
    total_chapters = len(path_data["chapters"])
    progress_percent = (len(chapters_completed) / total_chapters) * 100 if total_chapters > 0 else 0
    
    # Create progress bar for overall path progress
    # progress_bar_length = 20
    # filled_length = int(progress_bar_length * (progress_percent / 100))
    # overall_bar = '█' * filled_length + '▒' * (progress_bar_length - filled_length)
    progress_bar_length = 16
    filled_length = int(progress_bar_length * (progress_percent / 100))
    overall_bar = '🟩' * filled_length + '⬜' * (progress_bar_length - filled_length)
    
    # Count completed courses across the entire path
    completed_courses = 0
    total_courses = 0
    
    for chapter in path_data["chapters"]:
        chapter_courses = chapter["courses"]
        total_courses += len(chapter_courses)
        for course in chapter_courses:
            if course in user_state["completed_courses"]:
                completed_courses += 1
    
    course_percent = (completed_courses / total_courses) * 100 if total_courses > 0 else 0
    
    # Create progress bar for course completion
    # course_filled_length = int(progress_bar_length * (course_percent / 100))
    # course_bar = '█' * course_filled_length + '▒' * (progress_bar_length - course_filled_length)
    course_filled_length = int(progress_bar_length * (course_percent / 100))
    course_bar = '🟩' * course_filled_length + '⬜' * (progress_bar_length - course_filled_length)
    
    # Calculate estimated time metrics
    total_time = path_data["estimated_hours"]
    time_invested = (course_percent / 100) * total_time
    time_remaining = total_time - time_invested
    
    # If current chapter exists
    if current_chapter_idx < total_chapters:
        current_chapter = path_data["chapters"][current_chapter_idx]
        
        # Calculate current chapter progress
        chapter_courses = current_chapter["courses"]
        chapter_completed_courses = sum(1 for course in chapter_courses if course in user_state["completed_courses"])
        chapter_total_courses = len(chapter_courses)
        chapter_percent = (chapter_completed_courses / chapter_total_courses) * 100 if chapter_total_courses > 0 else 0
        
        # Create progress bar for current chapter
        # chapter_filled_length = int(progress_bar_length * (chapter_percent / 100))
        # chapter_bar = '█' * chapter_filled_length + '▒' * (progress_bar_length - chapter_filled_length)
        chapter_filled_length = int(progress_bar_length * (chapter_percent / 100))
        chapter_bar = '🟩' * chapter_filled_length + '⬜' * (progress_bar_length - chapter_filled_length)
        
        response_parts = [
            f"# {path_matched} - Learning Path Progress\n",
            f"## Overall Progress\n",
            f"**Path Completion:** {len(chapters_completed)}/{total_chapters} chapters ({progress_percent:.1f}%)",
            f"`{overall_bar}`",
            f"**Course Completion:** {completed_courses}/{total_courses} courses ({course_percent:.1f}%)",
            f"`{course_bar}`",
            f"**Time Stats:** ~{time_invested:.1f} hours invested, ~{time_remaining:.1f} hours remaining\n",
            f"## Current Chapter: {current_chapter['title']}\n",
            f"**Description:** {current_chapter['description']}",
            f"**Chapter Progress:** {chapter_completed_courses}/{chapter_total_courses} courses ({chapter_percent:.1f}%)",
            f"`{chapter_bar}`\n",
            "**Required Courses:**\n"
        ]
        
        # Check which courses are completed in the current chapter
        for course in current_chapter["courses"]:
            completed = course in user_state["completed_courses"]
            link = COURSE_LINKS.get(course, "https://example.com/courses")
            status_icon = "✅" if completed else "⏳"
            response_parts.append(f"- {status_icon} [{course}]({link})")
        
        # Create a visual chapter map
        response_parts.append("\n## Learning Path Map\n")
        
        for idx, chapter in enumerate(path_data["chapters"]):
            if idx in chapters_completed:
                status = "✅ COMPLETED"
            elif idx == current_chapter_idx:
                status = "⏳ IN PROGRESS"
            elif idx < current_chapter_idx:
                # This shouldn't happen normally, but just in case
                status = "⚠️ PENDING COMPLETION" # pragma: no cover
            else:
                status = "🔒 LOCKED"
            
            response_parts.append(f"**Chapter {idx+1}:** {chapter['title']} - {status}")
        
        # Add reward and tips section
        response_parts.append(f"\n## Completion Reward")
        response_parts.append(f"- {path_data['completion_reward_xp']} XP")
        response_parts.append(f"- '{path_data['completion_reward_badge']}' badge\n")
        
        response_parts.append("## 💡 **Tips**")
        response_parts.append("- Complete all courses in the current chapter to unlock the next one")
        response_parts.append("- Use `check chapter completion` to update your **progress after completing courses**")
        response_parts.append("- Use `show learning path details` to see the **full curriculum**")
        
        return "\n".join(response_parts)
    else:
        # This shouldn't happen if check_chapter_completion is working properly
        return f"You've completed **all chapters** in **'{path_matched}'**. Use `check learning path progress` to update your **status**." # pragma: no cover

def check_chapter_completion(user_state, path_name=None):
    """
    Checks if the current chapter in a learning path is completed
    and advances to the next chapter if it is.
    If path_name is None, checks all in-progress learning paths.
    Returns a list of messages for any chapter completions.
    """
    # Initialize if needed
    user_state = initialize_learning_paths_in_user_state(user_state)
    
    messages = []
    
    # Determine which paths to check
    paths_to_check = []
    if path_name:
        # Case-insensitive lookup for the learning path
        path_name_lower = path_name.lower()
        path_matched = None
        for p_key in LEARNING_PATHS.keys():
            if p_key.lower() == path_name_lower:
                path_matched = p_key
                break
                
        if path_matched and path_matched in user_state["learning_paths_progress"]:
            paths_to_check.append(path_matched)
        else:
            return [f"❌ No learning path named **'{path_name}'** found in your active paths."]
    else:
        # Check all in-progress paths
        for p_name, status in user_state["learning_paths_progress"].items():
            if status and not status.get("completed", False):
                paths_to_check.append(p_name)
    
    # Check each path
    for path_name in paths_to_check:
        path_status = user_state["learning_paths_progress"][path_name]
        
        # Skip if the path is already completed
        if path_status.get("completed", False):
            continue # pragma: no cover
            
        path_data = LEARNING_PATHS[path_name]
        current_chapter_idx = path_status.get("current_chapter", 0)
        
        # Make sure we're still within the path's chapters
        if current_chapter_idx >= len(path_data["chapters"]):
            continue
            
        current_chapter = path_data["chapters"][current_chapter_idx]
        
        # Check if all courses in the current chapter are completed
        all_completed = all(course in user_state["completed_courses"] for course in current_chapter["courses"])
        
        if all_completed:
            # Mark this chapter as completed if not already
            chapters_completed = path_status.get("chapters_completed", [])
            if current_chapter_idx not in chapters_completed:
                chapters_completed.append(current_chapter_idx)
                path_status["chapters_completed"] = chapters_completed
                
                # Award XP for chapter completion
                chapter_reward_xp = 50  # Base XP for completing a chapter
                user_state["xp"] += chapter_reward_xp
                
                # Create chapter completion message
                completion_message = (
                    f"🎉 You've completed Chapter **{current_chapter_idx + 1}**: **'{current_chapter['title']}'**"
                    f"in the **'{path_name}'** learning path!\n"
                    f"You earned **{chapter_reward_xp} XP** for completing this chapter!"
                )
                messages.append(completion_message)
                
            # Move to the next chapter
            next_chapter_idx = current_chapter_idx + 1
            
            # If there are more chapters, advance to the next one
            if next_chapter_idx < len(path_data["chapters"]):
                path_status["current_chapter"] = next_chapter_idx
                next_chapter = path_data["chapters"][next_chapter_idx]
                
                # Create course links for the next chapter
                course_links = []
                # Only show up to 3 courses in the message to avoid very long messages for chapters with many courses
                show_courses = next_chapter["courses"][:3]
                more_courses = len(next_chapter["courses"]) > 3
                
                for course in show_courses:
                    link = COURSE_LINKS.get(course, "https://example.com/courses")
                    completed = "✅ " if course in user_state["completed_courses"] else ""
                    course_links.append(f"- {completed}[{course}]({link})")
                
                # Add note if there are more courses not shown
                if more_courses:
                    course_links.append(f"- ...and {len(next_chapter['courses']) - 3} more courses")
                
                # Create a separate message for the next chapter
                next_chapter_message = (
                    f"🚩 Next chapter unlocked: **'{next_chapter['title']}'**\n"
                    f"{next_chapter['description']}\n\n"
                    f"**Required Courses:** (showing {len(show_courses)} of {len(next_chapter['courses'])})\n"
                    f"{chr(10).join(course_links)}\n\n"
                    f"Use `show learning path progress` to see **all required courses**."
                )
                messages.append(next_chapter_message)
    
    # If no messages were generated, provide a status update
    if not messages:
        available_courses = []
        for path_name in paths_to_check:
            path_status = user_state["learning_paths_progress"][path_name]
            path_data = LEARNING_PATHS[path_name]
            current_chapter_idx = path_status.get("current_chapter", 0)
            
            if current_chapter_idx < len(path_data["chapters"]):
                current_chapter = path_data["chapters"][current_chapter_idx]
                incomplete_courses = [
                    course for course in current_chapter["courses"]
                    if course not in user_state["completed_courses"]
                ]
                
                # Only show up to 5 incomplete courses to avoid very long messages
                show_incomplete = incomplete_courses[:5]
                more_incomplete = len(incomplete_courses) > 5
                
                if incomplete_courses:
                    if len(paths_to_check) > 1:
                        available_courses.append(f"**{path_name}** - Chapter {current_chapter_idx + 1}: '{current_chapter['title']}'")
                        for course in show_incomplete:
                            link = COURSE_LINKS.get(course, "https://example.com/courses")
                            available_courses.append(f"  - [{course}]({link})")
                        if more_incomplete:
                            available_courses.append(f"  - ...and {len(incomplete_courses) - 5} more courses")
                    else:
                        for course in show_incomplete:
                            link = COURSE_LINKS.get(course, "https://example.com/courses")
                            available_courses.append(f"- [{course}]({link})")
                        if more_incomplete:
                            available_courses.append(f"- ...and {len(incomplete_courses) - 5} more courses")
        
        if available_courses:
            header = "You still need to complete these courses to finish the current chapter:" if len(paths_to_check) == 1 else "Your current learning path progress:"
            messages.append(f"{header}\n{chr(10).join(available_courses)}")
        else:
            messages.append("No chapters to update. All your learning paths are either completed or up to date.")
    
    return messages

def check_learning_path_completion(user_state):
    """
    Checks if any learning paths are completed and awards rewards.
    Returns a list of completion messages.
    """
    # Initialize if needed
    user_state = initialize_learning_paths_in_user_state(user_state)
    
    messages = []
    
    for path_name, path_status in user_state["learning_paths_progress"].items():
        # Skip if the path is already marked as completed
        if path_status.get("completed", True):
            continue
            
        path_data = LEARNING_PATHS.get(path_name)
        if not path_data:
            continue # pragma: no cover
            
        # A path is completed if all chapters are in the chapters_completed list
        chapters_completed = path_status.get("chapters_completed", [])
        total_chapters = len(path_data["chapters"])
        
        if len(chapters_completed) == total_chapters:
            # Mark the path as completed
            path_status["completed"] = True
            
            # Award XP and badge
            reward_xp = path_data["completion_reward_xp"]
            reward_badge = path_data["completion_reward_badge"]
            
            user_state["xp"] += reward_xp
            
            # Add the badge if not already earned
            if reward_badge not in user_state["badges"]:
                user_state["badges"].append(reward_badge)
            
            messages.append(
                f"🎊 Congratulations! You've completed the entire **'{path_name}'** learning path!\n"
                f"You've earned:\n"
                f"- **{reward_xp} XP**\n"
                f"- **'{reward_badge}'**\n\n"
                f"This achievement shows your dedication to mastering **{path_name}**. Well done! 🫡"
            )
    
    return messages

def detect_learning_path_commands(user_message, user_state):
    """
    Detects and handles learning path related commands in the user message.
    Returns the appropriate response or None if no learning path command is detected.
    """
    # Initialize learning_paths_progress if needed
    user_state = initialize_learning_paths_in_user_state(user_state)
    
    user_message_lower = user_message.lower().strip()
    
    # Keywords for command detection
    start_synonyms = ["start", "begin", "kick off", "go ahead with", "undertake", "embark on"]
    list_synonyms = ["list", "show", "display", "view", "see", "what are"]
    check_synonyms = ["check", "update", "verify", "look at"]
    progress_synonyms = ["progress", "status", "advancement", "development"]
    details_synonyms = ["details", "information", "description", "info", "courses", "explain", "tell me more about"]
    path_synonyms = ["learning path", "learning paths", "path", "paths", "learning journey", "journey"]
    
    # FIX: Check for the PROGRESS command FIRST before more general commands
    # 3. Show Learning Path Progress command
    if ((any_keyword_in_text(user_message_lower, list_synonyms + check_synonyms) and
         any_keyword_in_text(user_message_lower, progress_synonyms) and
         any_keyword_in_text(user_message_lower, path_synonyms)) or
        # Special case for "show learning path progress"
        "show learning path progress" in user_message_lower):
        
        # Check if a specific path was mentioned
        path_name = None
        for p_name in LEARNING_PATHS.keys():
            if p_name.lower() in user_message_lower:
                path_name = p_name # pragma: no cover
                break # pragma: no cover
        
        return show_learning_path_progress(user_state, path_name)
    
    # NEW COMMAND: Show Learning Path Details
    if (any_keyword_in_text(user_message_lower, list_synonyms + ["get"]) and
        any_keyword_in_text(user_message_lower, details_synonyms) and
        any_keyword_in_text(user_message_lower, path_synonyms)):
        
        # Check if a specific path was mentioned
        path_name = None
        for p_name in LEARNING_PATHS.keys():
            if p_name.lower() in user_message_lower:
                path_name = p_name
                break
                
        # Extract path name after any of the relevant keywords if we didn't find a match
        if not path_name:
            paths_keywords = path_synonyms + details_synonyms
            for keyword in paths_keywords:
                if keyword in user_message_lower:
                    remainder = extract_after_keyword(user_message, [keyword])
                    if remainder.strip():
                        # Check if this remainder matches any path
                        for p_name in LEARNING_PATHS.keys():
                            if p_name.lower() in remainder.lower():
                                path_name = p_name # pragma: no cover
                                break # pragma: no cover
                    if path_name:
                        break # pragma: no cover
        
        return show_learning_path_details(user_state, path_name)
    
    # 1. Start Learning Path command
    if (any_keyword_in_text(user_message_lower, start_synonyms) and 
        any_keyword_in_text(user_message_lower, path_synonyms)):
        
        path_name = extract_after_keyword(user_message, path_synonyms)
        
        # If no path name was provided, set pending action for next input
        if not path_name.strip():
            user_state["pending_action"] = "start_learning_path"
            
            # Get available paths for the user as dictionaries for table formatting
            available_paths = []
            for p_name, p_data in LEARNING_PATHS.items():
                if p_name not in user_state["learning_paths_progress"]:
                    available_paths.append({
                        "name": p_name,
                        "difficulty": p_data["difficulty"],
                        "hours": p_data["estimated_hours"]
                    })
            
            if available_paths:
                # Format paths as a table instead of a list
                table_parts = []
                table_parts.append("| Learning Path | Difficulty Level | Estimated Time |")
                table_parts.append("|--------------|------------------|----------------|")
                
                for path in available_paths:
                    table_parts.append(f"| **{path['name']}** | {path['difficulty']} | {path['hours']} hours |")
                
                paths_table = "\n".join(table_parts)
                
                return (
                    f"Which learning path 🛤️ would you like to start? Here are the available options:\n\n"
                    f"{paths_table}\n\n"
                    f"Just type the name of the learning path you'd like to begin!"
                )
            else:
                # If user has started all paths but not completed them
                in_progress = []
                for p_name, status in user_state["learning_paths_progress"].items():
                    if not status.get("completed", False):
                        # Calculate progress for more meaningful information
                        chapters_completed = len(status.get("chapters_completed", []))
                        total_chapters = len(LEARNING_PATHS[p_name]["chapters"])
                        progress_percent = (chapters_completed / total_chapters) * 100 if total_chapters > 0 else 0
                        
                        # Add as formatted bullet point with progress
                        in_progress.append(f"- **{p_name}** - {chapters_completed}/{total_chapters} chapters completed ({progress_percent:.1f}%)")
                
                if in_progress:
                    paths_list = "\n".join(in_progress)
                    return (
                        f"You've already started all available learning paths. Here are your in-progress paths:\n\n"
                        f"{paths_list}\n\n"
                        f"Would you like to continue with any of these? Just type the path name!"
                    )
                else:
                    return (
                        "You've either completed or started all available learning paths. "
                        "**Check your progress** with `show learning path progress`."
                    )
        
        return start_learning_path(user_state, path_name.strip())
    
    # Handle pending action for starting a learning path
    if user_state.get("pending_action") == "start_learning_path":
        path_name = user_message.strip()
        user_state["pending_action"] = None
        return start_learning_path(user_state, path_name)
    
    # 2. List Learning Paths command - MOVED AFTER the progress command to avoid conflicts
    if (any_keyword_in_text(user_message_lower, list_synonyms) and 
        any_keyword_in_text(user_message_lower, path_synonyms)):
        return list_learning_paths(user_state)
    
    # 4. Check Chapter Completion command
    if (any_keyword_in_text(user_message_lower, check_synonyms) and
        any_keyword_in_text(user_message_lower, ["chapter", "learning path progress"])):
        
        # Check if a specific path was mentioned
        path_name = None
        for p_name in LEARNING_PATHS.keys():
            if p_name.lower() in user_message_lower:
                path_name = p_name # pragma: no cover
                break # pragma: no cover
        
        messages = check_chapter_completion(user_state, path_name)
        
        # Check if any paths were completed
        completion_messages = check_learning_path_completion(user_state)
        messages.extend(completion_messages)
        
        return "\n\n".join(messages)
    
    # No learning path command detected
    return None
        
#########################################
# 11. HELPER FUNCTIONS FOR KEYWORD MATCHES
#########################################

def any_keyword_in_text(text: str, keywords: list[str]) -> bool:
    return any(kw in text for kw in keywords)

def extract_after_keyword(message: str, keywords) -> str:
    msg_lower = message.lower()
    last_index = -1
    chosen_len = 0
    for kw in keywords:
        idx = msg_lower.rfind(kw)
        if idx > last_index:
            last_index = idx
            chosen_len = len(kw)
    if last_index == -1:
        return ""
    
    # Extract everything after the keyword and trim whitespace and punctuation
    remainder = message[last_index + chosen_len:].strip(" .:-")
    
    # Remove surrounding quotes if present (handles both single and double quotes)
    import re
    quote_pattern = r'^([\'"])(.*)\1$'
    match = re.match(quote_pattern, remainder)
    if match:
        remainder = match.group(2)  # Extract just the content inside the quotes
    
    return remainder

# Add this function to your code in the command handler section

def get_trending_courses():
    """
    Returns 5 random trending courses with higher ratings, ensuring that
    at least 4 different categories are represented.
    """
    import random
    
    # Get course categories
    course_categories = get_course_categories()
    categories = list(course_categories.keys())
    
    # For trending courses, we'll prefer courses with higher ratings and more reviews
    # First, create a list of eligible courses with their metadata
    eligible_courses = []
    
    for category, courses in course_categories.items():
        for course in courses:
            # Get rating info if available
            course_rating_info = course_ratings.get(course)
            
            # Only include courses that have ratings
            if course_rating_info and course_rating_info["num_ratings"] > 0:
                avg_rating = course_rating_info["total_rating"] / course_rating_info["num_ratings"]
                num_ratings = course_rating_info["num_ratings"]
                
                # Create a "trending score" - higher for courses with more ratings and better scores
                trending_score = avg_rating * (1 + (num_ratings / 10))
                
                eligible_courses.append({
                    "name": course,
                    "category": category,
                    "rating": avg_rating,
                    "num_ratings": num_ratings,
                    "trending_score": trending_score,
                    "link": COURSE_LINKS.get(course, "https://example.com/courses")
                })
    
    # Sort by trending score (highest first)
    eligible_courses.sort(key=lambda x: x["trending_score"], reverse=True)
    
    # Take top 20 courses to sample from
    top_courses = eligible_courses[:20] if len(eligible_courses) > 20 else eligible_courses
    
    # First, ensure we have at least one course from each category (up to 4 categories)
    selected_courses = []
    selected_categories = set()
    
    # Try to get one course from each category first
    for category in categories[:4]:  # Limit to 4 categories
        # Find courses in this category from our top courses
        category_courses = [course for course in top_courses 
                           if course["category"] == category and course["name"] not in [c["name"] for c in selected_courses]]
        
        if category_courses:
            # Choose a random course from this category
            selected_course = random.choice(category_courses)
            selected_courses.append(selected_course)
            selected_categories.add(category)
    
    # If we haven't reached 5 courses yet, add more random ones from any category
    remaining_slots = 5 - len(selected_courses)
    if remaining_slots > 0:
        # Filter out courses we've already selected
        remaining_courses = [course for course in top_courses 
                            if course["name"] not in [c["name"] for c in selected_courses]]
        
        # Choose random courses to fill remaining slots
        if remaining_courses:
            additional_courses = random.sample(remaining_courses, 
                                             min(remaining_slots, len(remaining_courses)))
            selected_courses.extend(additional_courses)
    
    # If we somehow still don't have 5 courses (unlikely but possible if data is limited)
    while len(selected_courses) < 5 and eligible_courses:
        # Just add any eligible course that we haven't already selected
        remaining_all = [course for course in eligible_courses # pragma: no cover
                        if course["name"] not in [c["name"] for c in selected_courses]] 
        
        if not remaining_all: # pragma: no cover
            break # pragma: no cover
            
        selected_courses.append(random.choice(remaining_all)) # pragma: no cover
    
    # Format the response
    response_parts = ["## 🔥 Trending Courses Right Now\n"]
    
    for i, course in enumerate(selected_courses, 1):
        # Create star display
        stars = "⭐" * round(course["rating"])
        
        # Add course to response - CHANGED "ratings" to "reviews"
        response_parts.append(
            f"{i}. **{course['name']}** ({course['category']}) - {stars} ({course['num_ratings']} reviews)\n"
            f"   [Visit Course]({course['link']})"
        )
    
    # Add a note about the selection
    response_parts.append("\n*Courses selected based on user reviews and popularity*")
    response_parts.append("\nIf you need to see **all available courses**, use: `show courses`")
    
    return "\n".join(response_parts)

#########################################
# 12. COMMAND HANDLER
#########################################
def show_user_profile(user_state):
    """
    Displays all user profile information in one comprehensive view,
    including level, XP, badges, streaks, and learning progress.
    """
    # Calculate progress level percentage
    current_level_idx = 0
    next_level_idx = 0
    current_xp = user_state["xp"]
    
    # Find current and next level indices
    for i, level in enumerate(TEN_LEVELS):
        if current_xp >= level["xp_needed"]:
            current_level_idx = i
            next_level_idx = min(i + 1, len(TEN_LEVELS) - 1)
    
    # Calculate progress to next level
    current_level = TEN_LEVELS[current_level_idx]
    next_level = TEN_LEVELS[next_level_idx]
    
    # If at max level
    if current_level_idx == next_level_idx:
        level_progress = 100
        xp_to_next = 0
    else:
        xp_in_current_level = current_xp - current_level["xp_needed"]
        xp_needed_for_next = next_level["xp_needed"] - current_level["xp_needed"]
        level_progress = (xp_in_current_level / xp_needed_for_next) * 100 if xp_needed_for_next > 0 else 100
        xp_to_next = next_level["xp_needed"] - current_xp
    
    # Create progress bar for level
    progress_bar_length = 16
    filled_length = int(progress_bar_length * (level_progress / 100))
    level_bar = '🟩' * filled_length + '⬜' * (progress_bar_length - filled_length)
    
    # Build the response
    response_parts = ["# Your Profile Overview\n"]
    
    # Level and XP section
    response_parts.append("## 📊 Level & Experience")
    response_parts.append(f"**Current Level:** {user_state['level']}")
    response_parts.append(f"**Total XP:** {current_xp} XP")
    
    # Only show progress to next level if not at max level
    if current_level_idx < len(TEN_LEVELS) - 1:
        response_parts.append(f"**Progress to {next_level['hex_code']} [{next_level['title']}]:** {level_progress:.1f}%")
        response_parts.append(f"`{level_bar}`")
        response_parts.append(f"**XP needed for next level:** {xp_to_next} XP\n")
    else:
        response_parts.append("**Status:** Maximum level achieved! 🏆\n")
    
    # Streak information
    response_parts.append("## 🔥 Activity Streak")
    response_parts.append(f"**Current Streak:** {user_state.get('current_streak', 0)} days")
    response_parts.append(f"**Longest Streak:** {user_state.get('longest_streak', 0)} days\n")
    
    # Badges section
    response_parts.append("## 🎖️ Earned Badges")
    if user_state["badges"]:
        # Show badges in a cleaner format - maximum 5 per line
        badge_chunks = [user_state["badges"][i:i+5] for i in range(0, len(user_state["badges"]), 5)]
        for chunk in badge_chunks:
            response_parts.append("• " + " • ".join(chunk))
    else:
        response_parts.append("You haven't earned any badges yet. Complete courses and quests to earn badges!")
    
    # Course completion stats
    total_courses = 0
    for category, courses in get_course_categories().items():
        total_courses += len(courses)
    
    completed_courses_count = len(user_state["completed_courses"])
    completion_percent = (completed_courses_count / total_courses) * 100 if total_courses > 0 else 0
    
    response_parts.append("\n## 📈 Learning Progress")
    response_parts.append(f"**Completed Courses:** {completed_courses_count}/{total_courses} ({completion_percent:.1f}%)")
    
    # Count active and completed quests
    active_quests = sum(1 for q, status in user_state["active_quests"].items() if not status.get("completed", False))
    completed_quests = sum(1 for q, status in user_state["active_quests"].items() if status.get("completed", True))
    
    response_parts.append(f"**Active Quests:** {active_quests}")
    response_parts.append(f"**Completed Quests:** {completed_quests}")
    
    # Count learning paths
    active_paths = sum(1 for p, status in user_state.get("learning_paths_progress", {}).items() 
                     if not status.get("completed", False))
    completed_paths = sum(1 for p, status in user_state.get("learning_paths_progress", {}).items() 
                        if status.get("completed", True))
    
    response_parts.append(f"**Active Learning Paths:** {active_paths}")
    response_parts.append(f"**Completed Learning Paths:** {completed_paths}")
    
    # Add leaderboard info if the user is on the leaderboard
    if user_state.get("leaderboard_nickname"):
        response_parts.append("\n## 🏆 Leaderboard Status")
        
        # Find user's position on the leaderboard
        sorted_lb = sorted(leaderboard, key=lambda x: x["xp"], reverse=True)
        user_pos = next((i for i, entry in enumerate(sorted_lb) 
                        if entry["user_id"] == user_state["user_id"]), None)
        
        if user_pos is not None:
            response_parts.append(f"**Nickname:** {user_state['leaderboard_nickname']}")
            response_parts.append(f"**Rank:** {user_pos + 1} of {len(sorted_lb)}")
    
    # Add tip at the end
    response_parts.append("\n*💡 **Tip:** Continue completing courses, quests, and daily challenges to earn XP and level up!*")
    
    return "\n".join(response_parts)

def handle_user_message(user_message: str, user_state: dict):
    user_message_lower = user_message.lower().strip()
    
    # Check for any pending actions first
    if user_state["pending_action"] == "join_leaderboard":
        # Temporarily reset pending_action
        user_state["pending_action"] = None
        
        nickname = user_message.strip()
        result = join_leaderboard(user_state, nickname)
        
        # If the nickname is taken, or any other error that asks user to try again,
        # we can look for that exact text or do partial checks.
        if "Nickname is taken. Please choose another." in result:
            # Re-enable the pending action so user can re-try a new nickname
            user_state["pending_action"] = "join_leaderboard"
        
        return result
    
    # Handle "start_quest" pending action
    elif user_state["pending_action"] == "start_quest":
        # Temporarily reset pending_action
        user_state["pending_action"] = None
        
        quest_name = user_message.strip()
        return start_quest(user_state, quest_name)
    
    # Handle "complete_course" pending action
    elif user_state["pending_action"] == "complete_course":
        # Temporarily reset pending_action
        user_state["pending_action"] = None
        
        course_name = user_message.strip()
        return process_course_completion(user_state, course_name)
    
    # Handle "start_learning_path" pending action
    elif user_state["pending_action"] == "start_learning_path":
        # Temporarily reset pending_action
        user_state["pending_action"] = None
        
        path_name = user_message.strip()
        return start_learning_path(user_state, path_name)

    # ------------------------------------------------------------------
    # 1) If user HAS an active daily challenge, attempt to answer it
    #    - We only skip this if the user is clearly doing another command
    # ------------------------------------------------------------------
    if user_state["current_challenge"] is not None and not user_state["daily_challenge_done"]:
        # We do a quick pass: does the user message match any "recognized" commands (like "show xp")?
        # If so, we let them do that command.
        # Otherwise, we treat it as an attempt to answer the daily challenge.
        recognized_response = detect_command(user_message, user_state)
        if recognized_response is not None:
            # Means the user typed a recognized command
            return recognized_response
        else:
            # Attempt the challenge
            ans = check_daily_challenge_answer(user_state, user_message)
            # If ans is None => no challenge active or error. 
            # But we do have an active challenge, so None means bug. 
            if ans is None:
                return "🚫 Unexpected error. Please try again."
            return ans
    else:
        # If there's no active challenge, we proceed normally
        recognized_response = detect_command(user_message, user_state)
        if recognized_response is not None:
            return recognized_response
        else:
            return get_recommendation(user_message)

def detect_command(user_message: str, user_state: dict) -> str | None | Tuple[str, Optional[str]]:
    """
    Check known commands or synonyms. Return the command's response if matched,
    else return None so handle_user_message() can do fallback or daily-challenge attempt.
    """
    user_message_lower = user_message.lower().strip()
    
    HELP_RESPONSES = {
        "📚 courses": (
            "### Course Commands:\n"
            "- `show courses` - List all available courses\n"
            "- `show trending courses` - List some trending courses\n"
            "- `completed course [name]` - Mark a course as completed\n"
        ),
        
        "🛣️ learning paths": (
            "### Learning Paths Commands:\n"
            "- `list learning paths` - See all available paths\n"
            "- `start learning path [name]` - Begin a learning path\n"
            "- `show learning path progress` - Check your current progress\n"
            "- `show learning path details` - View detailed curriculum\n"
            "- `check chapter completion` - Update chapter progress"
        ),
        
        "🎯 quests": (
            "### Quest Commands:\n"
            "- `show quests` - List all available quests\n"
            "- `show quest details` - View detailed info of each quest\n"
            "- `start quest [name]` - Begin a new quest\n"
            "- `show quest progress` - Check your current quest progress"
        ),
        
        "🧩 challenges": (
            "### Daily Challenge Commands:\n"
            "- `daily challenge` - Get today's challenge\n"
            "- Simply type your answer to respond to a challenge"
        ),
        
        "📈 progress": (
            "### Progress Tracking Commands:\n"
            "- `show xp` - View your current experience points\n"
            "- `show level` - Check your current level\n"
            "- `show badges` - See all earned badges\n"
            "- `show profile` - Displays all user profile information."
        ),
        
        "🏆 leaderboard": (
            "### Leaderboard Commands:\n"
            "- `show leaderboard` - View top performers\n"
            "- `join leaderboard [nickname]` - Add yourself to rankings\n"
            "- `leave leaderboard` - Remove yourself from rankings"
        )
    }
    
    # Check specifically for "help all" command
    if user_message_lower == "help all":
        # Compile all help responses into one comprehensive guide
        response_parts = [
            "# IBM Course Recommender - Command Guide\n",
            "Here's a comprehensive list of all available commands organized by feature:\n"
        ]
        
        # Add each feature's commands with spacing between sections
        for feature, commands in HELP_RESPONSES.items():
            response_parts.append(f"\n\n## {feature.title()}\n{commands}")
            response_parts.append("\n---\n")
        
        # Add final tips
        response_parts.append("### 💡 Tips")
        response_parts.append("- Commands are case-insensitive")
        response_parts.append("- Daily challenges refresh every day for bonus XP")
        response_parts.append("- For personalized recommendations, just chat about your interests!")
        
        return "\n".join(response_parts)
    
    # Check for specific feature help
    help_keywords = ["help", "how to", "show commands for", "tell me about"]
    if any(kw in user_message_lower for kw in help_keywords):
        # Check for each feature keyword in a way that doesn't require emojis
        # Define a mapping between common user terms and the emoji keys in HELP_RESPONSES
        feature_keyword_map = {
            "course": "📚 courses",
            "courses": "📚 courses",
            "path": "🛣️ learning paths",
            "paths": "🛣️ learning paths", 
            "learning path": "🛣️ learning paths",
            "learning paths": "🛣️ learning paths",
            "quest": "🎯 quests",
            "quests": "🎯 quests",
            "challenge": "🧩 challenges",
            "challenges": "🧩 challenges",
            "daily challenge": "🧩 challenges",
            "progress": "📈 progress",
            "xp": "📈 progress",
            "level": "📈 progress",
            "badge": "📈 progress",
            "leaderboard": "🏆 leaderboard",
            "ranking": "🏆 leaderboard"
        }
        
        # Check if any feature keyword is in the user message
        matched_feature = None
        for keyword, help_key in feature_keyword_map.items():
            if keyword in user_message_lower:
                matched_feature = help_key
                break
                
        if matched_feature:
            return HELP_RESPONSES[matched_feature]
        else:
            # If no specific feature matched, return general help
            return (
                "👋 Welcome to **IBM Course Recommender** - start your personalized learning journey now!\n\n"
                "**Available Features:**\n"
                "- 📚 **Courses** - Gain knowledge from different fields\n"
                "- 🛣️ **Learning Paths** - Structured educational journeys\n"
                "- 🎯 **Quests** - Complete tasks to earn rewards\n"
                "- 🧩 **Daily Challenges** - Test your knowledge daily\n"
                "- 📈 **Progress Tracking** - Monitor your advancement\n"
                "- 🏆 **Leaderboard** - Compare with other learners\n\n"
                
                "**💡 Tips:**\n"  # Fixed missing newline and added colon
                "Type `help all` to see **all command for every feature**\n"
                "Type `help [feature]` to learn more about **any feature** (e.g., `help quests`)"
            )


    # 1) Show "Trending"/"Popular" Courses
    synonyms_for_show = ["show", "display", "provide", "tell me", "share", "can i see"]
    synonyms_for_trending = ["trending", "popular", "hot", "top-rated"]
    synonyms_for_courses = ["course", "courses", "class", "classes", "program", "programs"]

    if (any_keyword_in_text(user_message_lower, synonyms_for_show)
        and any_keyword_in_text(user_message_lower, synonyms_for_trending)
        and any_keyword_in_text(user_message_lower, synonyms_for_courses)):
        return get_trending_courses()
        
        
    # Course display commands - UPDATED SECTION
    if (any_keyword_in_text(user_message_lower, ["show", "display", "list"]) and
        "courses" in user_message_lower):
        
        # Check if it's for completed courses
        if "completed" in user_message_lower:
            return show_completed_courses(user_state)
        
        # Check if it's for a specific category
        categories = ["cybersecurity", "data science", "web development", "business management"]
        
        for category in categories:
            if category in user_message_lower:
                return show_category_courses(user_state, category)
        
        # If no specific category, show all courses
        return show_courses(user_state)

    # 2) Course Completion
    completion_synonyms = ["completed", "finished", "done with"]
    course_synonyms = ["course", "program", "programme", "class"]

    if (any_keyword_in_text(user_message_lower, completion_synonyms) and
    any_keyword_in_text(user_message_lower, course_synonyms)):
    
        course_name = extract_after_keyword(user_message, course_synonyms)
    
        if not course_name.strip():
            # No course name was provided, set pending action for next input
            user_state["pending_action"] = "complete_course"
        
            # Create a simplified response without listing all courses
            response = (
            "It seems like you forgot to include the course name, no worries!\n\n"
            "Please type the name of the course you've completed.\n\n"
            "If you need to see available courses, use: `show courses`"
            )
        
            return response
    
        # If course name was provided, process it normally
        return process_course_completion(user_state, course_name)
    
    # Handle pending actions for multi-turn interactions
    if user_state.get("pending_action") == "complete_course":
        # User's next message should be the course name
        course_name = user_message.strip()
        # Reset pending action
        user_state["pending_action"] = None
        # Process the course completion
        return process_course_completion(user_state, course_name)
            
    # 3) Show XP
    show_synonyms = ["show", "display", "tell me", "my"]
    if any_keyword_in_text(user_message_lower, show_synonyms) and "xp" in user_message_lower:
        return f"You current XP ✨: **{user_state['xp']}**"

    # 4) Show Badges
    badge_synonyms = ["badge", "badges"]   
    if (any_keyword_in_text(user_message_lower, show_synonyms)
        and any_keyword_in_text(user_message_lower, badge_synonyms)):
        if user_state["badges"]:
            return "You have the following badges 🎖️:\n- " + "\n- ".join(user_state["badges"])
        else:
            return "You haven't earned any badges yet."

    # 5) Show Level
    level_synonyms = ["level", "rank"]
    if (any_keyword_in_text(user_message_lower, show_synonyms)
        and any_keyword_in_text(user_message_lower, level_synonyms)):
        return f"Your current level 🔝: **{user_state['level']}**."

    # 6) Daily Challenge synonyms
    #    If user wants to start a daily challenge (no active one).
    if "daily" in user_message_lower and "challenge" in user_message_lower:
        return present_daily_challenge(user_state)

    # 7) Start Quest synonyms
    start_synonyms = ["start", "begin", "kick off", "go ahead with"]
    quest_synonyms = ["quest", "quests"]

    # Check if user wants to start a quest
    if (any_keyword_in_text(user_message_lower, start_synonyms)
        and any_keyword_in_text(user_message_lower, quest_synonyms)):
        
        quest_name = extract_after_keyword(user_message, quest_synonyms)
        
        # If no quest name was provided, set pending action for next input
        if not quest_name.strip():
            # Get ONLY truly available quests (not started, not completed)
            available_quests = []
            in_progress_quests = []
            
            for q_name in QUESTS.keys():
                # Check if the quest is in active_quests
                quest_status = user_state["active_quests"].get(q_name)
                
                # Completely new quests
                if quest_status is None:
                    available_quests.append(q_name)
                # In-progress quests (started but not completed)
                elif quest_status.get("completed") is False:
                    in_progress_quests.append(q_name)
            
            # Set the pending action to capture the next input as quest name
            user_state["pending_action"] = "start_quest"
            
            # If there are new quests available
            if available_quests:
                # Limit to top 5 quests and format them with bullet points
                top_quests = available_quests[:5]
                formatted_quests = [f"- {quest}" for quest in top_quests]
                quest_list = "\n".join(formatted_quests)
                
                # Add message about remaining quests if there are more than 5
                remaining_msg = ""
                if len(available_quests) > 5:
                    more_count = len(available_quests) - 5
                    remaining_msg = f"\n*...and {more_count} more quests. Use `show quests` to see **all**.*"
                
                return (
                    f"It seems like you forgot to include the quest name, no worries! Here are some quests you can start:\n\n"
                    f"{quest_list}{remaining_msg}\n\n"
                    f"Just type the quest name you'd like to begin!"
                )
            # If there are no new quests but there are in-progress quests
            elif in_progress_quests:
                # Limit to top 5 in-progress quests and format them with bullet points
                top_quests = in_progress_quests[:5]
                formatted_quests = [f"- {quest}" for quest in top_quests]
                quest_list = "\n".join(formatted_quests)
                
                # Add message about remaining quests if there are more than 5
                remaining_msg = ""
                if len(in_progress_quests) > 5:
                    more_count = len(in_progress_quests) - 5
                    remaining_msg = f"\n*...and **{more_count}** more quests in progress. Use `show quest progress` to see **all**.*"
                
                return (
                    f"You don't have any new quests available at the moment, but here are some quests you're currently working on:\n\n"
                    f"{quest_list}{remaining_msg}\n\n"
                    f"Would you like to continue with any of these? Just type the quest name!"
                )
            # If there are no new or in-progress quests
            else:
                return (
                    "It looks like you've completed **all available quests**! Check back later for new quests, "
                    "or type `list quests` to see all your **completed quests**."
                )
        
        return start_quest(user_state, quest_name.strip())
    
    # Handle pending actions for multi-turn interactions
    if user_state.get("pending_action") == "start_quest":
        # User's message should be the quest name
        quest_name = user_message.strip() # pragma: no cover
        # Reset pending action
        user_state["pending_action"] = None # pragma: no cover
        # Process the quest name
        return start_quest(user_state, quest_name) # pragma: no cover

    # 8) Quest Commands - check specific quest commands first
    synonyms_for_list = ["show", "list", "provide", "display", "tell me", "what are", "can you show me", "could you display", "can i see"]
    quest_synonyms = ["quest", "quests"]
    progress_synonyms = ["progress", "status", "advancement", "details", "info"]
    details_synonyms = ["details", "information", "description", "info", "explain", "tell me more about"]
    
    # NEW: Check for "show quest details" command
    if (any_keyword_in_text(user_message_lower, synonyms_for_list) and
        any_keyword_in_text(user_message_lower, quest_synonyms) and
        any_keyword_in_text(user_message_lower, details_synonyms)):
        
        # Check if a specific quest was mentioned
        quest_name = None
        for q_name in QUESTS.keys():
            if q_name.lower() in user_message_lower:
                quest_name = q_name # pragma: no cover
                break # pragma: no cover
                
        # Extract quest name after any of the relevant keywords if we didn't find a match
        if not quest_name:
            quests_keywords = quest_synonyms + details_synonyms
            for keyword in quests_keywords:
                if keyword in user_message_lower:
                    remainder = extract_after_keyword(user_message, [keyword])
                    if remainder.strip():
                        # Check if this remainder matches any quest
                        for q_name in QUESTS.keys():
                            if q_name.lower() in remainder.lower():
                                quest_name = q_name # pragma: no cover
                                break # pragma: no cover
                    if quest_name:
                        break # pragma: no cover
        
        return show_quest_details(user_state, quest_name)
    
    # First check for the more specific "show quest progress" command
    if (any_keyword_in_text(user_message_lower, synonyms_for_list) and
        any_keyword_in_text(user_message_lower, quest_synonyms) and
        any_keyword_in_text(user_message_lower, progress_synonyms)):
        return show_quest_progress(user_state)
    
    # Then check for the more general "show quests" command
    if (any_keyword_in_text(user_message_lower, synonyms_for_list) and
        any_keyword_in_text(user_message_lower, quest_synonyms)):
        return list_quests(user_state)
    
    # 10) Show leaderboard synonyms
    synonyms_for_leaderboard = ["leaderboard", "rankings", "scoreboard"]
    if (any_keyword_in_text(user_message_lower, synonyms_for_show) and
        any_keyword_in_text(user_message_lower, synonyms_for_leaderboard)):
        return show_leaderboard(top_n=5, user_state=user_state)
    
    # 11) Leave Leaderboard synonyms
    synonyms_for_leave = ["leave", "quit", "exit from", "withdraw from"]
    if (any_keyword_in_text(user_message_lower, synonyms_for_leave) and
        any_keyword_in_text(user_message_lower, synonyms_for_leaderboard)):
        return leave_leaderboard(user_state)
    
    # 12) "Join leaderboard" logic: Check if the user wants to "join the leaderboard" in any phrasing
    synonyms_for_join = ["join", "be part of", "get on", "see my name on", "participate in", "add me to", "include me in", "be included in"]
    if (any_keyword_in_text(user_message_lower, synonyms_for_join) and
        any_keyword_in_text(user_message_lower, synonyms_for_leaderboard)):
         # Now we check if the user also provided a nickname in the same message
        # e.g. "include me in the scoreboard JohnDoe"
        
        # We can try a simple approach: see if there's any text after the last leaderboard synonym
        # or after the last join synonym. We can do something like:
        
        remainder = extract_after_keyword(user_message, synonyms_for_leaderboard + synonyms_for_join)
        nickname = remainder.strip()
        
        if nickname:
            # The user typed something that might be their nickname
            # e.g. "add me to the scoreboard MyNickname" 
            return join_leaderboard(user_state, nickname)
        else:
            # No nickname found => prompt for it
            user_state["pending_action"] = "join_leaderboard"
            return "🤩 Absolutely! Can I please have your nickname?"
            
    # Check for Learning Path commands
    learning_path_response = detect_learning_path_commands(user_message, user_state)
    if learning_path_response is not None:
        return learning_path_response
    
    if user_message_lower.startswith("course rating"):
        parts = user_message_lower.split("rating", 1)
        if len(parts) < 2 or not parts[1].strip():
            return "Usage: 'Course rating <course name>'." # pragma: no cover
        course_name = parts[1].strip()
        avg_rating = get_course_average_rating(course_name)
        return f"'{course_name}' has an average rating of {avg_rating}."
    
    # Add the profile command detection after existing show XP, badges, level commands
    profile_synonyms = ["profile", "stats", "status", "info", "information", "summary", "overview"]
    if (any_keyword_in_text(user_message_lower, show_synonyms) and
        any_keyword_in_text(user_message_lower, profile_synonyms)):
        return show_user_profile(user_state)

    # If none of those matched, return None
    return None

#########################################
# 13. MAIN CHATBOT & GRADIO UI
#########################################

def add_message(history, message):
    for path in message["files"]:
        history.append({"role": "user", "content": {"path": path}})
    if message["text"] is not None:
        history.append({"role": "user", "content": message["text"]})
    return history, gr.MultimodalTextbox(value=None, interactive=False)


def type_text_in_word_chunks(
    full_text: str,
    chunk_size: int = 3,
    chunk_delay: float = 0.5,
    pre_delay: float = 0.0,
    post_delay: float = 0.0
):
    """
    Yields partial segments of `full_text`, revealing it in chunks of N words 
    (default 5 words). Uses a regex split that preserves whitespace/newlines, 
    so bullet points and line breaks remain intact.

    :param full_text:   The complete text you want to display in chunks.
    :param chunk_size:  Number of "real words" per chunk (excluding pure whitespace).
    :param chunk_delay: Delay (in seconds) between revealing each chunk.
    :param pre_delay:   A "thinking pause" before revealing text.
    :param post_delay:  A pause after all text is revealed.
    """
    # Pre-typing pause
    if pre_delay > 0:
        time.sleep(pre_delay) # pragma: no cover

    # Split into tokens, capturing whitespace/newline tokens separately.
    # Example: ["Here", " ", "are", " ", ..., "\n", "-", " ", "Data", ...]
    tokens = re.split(r'(\s+)', full_text)

    displayed_text = ""
    chunk_accumulator = []
    word_count = 0

    for token in tokens:
        # We always append the token to the accumulator (so whitespace is included).
        chunk_accumulator.append(token)

        # Increase word_count only if token is NOT pure whitespace
        # (i.e., it's an actual word, bullet, punctuation, etc.)
        if not re.match(r'^\s*$', token):
            word_count += 1

        # If we've hit the chunk_size of actual "words," yield the chunk
        if word_count >= chunk_size:
            # Join everything in chunk_accumulator into displayed_text
            displayed_text += "".join(chunk_accumulator)
            # We yield the newly extended displayed_text so it updates on-screen
            yield displayed_text

            # Reset counters for the next chunk
            chunk_accumulator = []
            word_count = 0

            # Sleep briefly to simulate the delay between each chunk
            time.sleep(chunk_delay)

    # If there are leftover tokens after the final full chunk
    if chunk_accumulator:
        displayed_text += "".join(chunk_accumulator)
        yield displayed_text

    # Post-typing pause
    if post_delay > 0:
        time.sleep(post_delay) # pragma: no cover

def process_pending_notifications(history, user_state):
    """Process all pending notifications for quests, badges, level-ups, and learning paths."""
    # Skip if there are no pending notifications
    if "pending_notifications" not in user_state:
        yield history, user_state, gr.update(visible=False), None
        return
    
    # Process quest completions
    if user_state["pending_notifications"].get("quest_check_needed", False):
        quest_msgs = check_quests(user_state)
        # Stream quest messages
        for qm in quest_msgs:
            history.append({"role": "assistant", "content": ""})
            for partial_text in type_text_in_word_chunks(qm, chunk_size=3, chunk_delay=0.15, pre_delay=0.75):
                history[-1]["content"] = partial_text
                yield history, user_state, gr.update(visible=False), None

    # Process badge awards
    if user_state["pending_notifications"].get("badges_check_needed", False):
        newly_awarded_skill_badges = check_skill_badges(user_state)
        for badge in newly_awarded_skill_badges:
            badge_text = (
                f"You've earned a new skill badge: **'{badge}'**!"
            )
            history.append({"role": "assistant", "content": ""})
            for partial_text in type_text_in_word_chunks(badge_text, chunk_size=3, chunk_delay=0.15, pre_delay=0.75):
                history[-1]["content"] = partial_text
                yield history, user_state, gr.update(visible=False), None

    # Process level-up
    if user_state["pending_notifications"].get("level_check_needed", False):
        levelup_msg = check_level_up(user_state)
        if levelup_msg:
            history.append({"role": "assistant", "content": ""})
            for partial_text in type_text_in_word_chunks(levelup_msg, chunk_size=3, chunk_delay=0.15, pre_delay=0.75):
                history[-1]["content"] = partial_text
                yield history, user_state, gr.update(visible=False), None
    
    # Process learning path updates
    if user_state["pending_notifications"].get("learning_path_check_needed", False):
        # Check chapter completion
        chapter_messages = check_chapter_completion(user_state)
        for cm in chapter_messages:
            history.append({"role": "assistant", "content": ""})
            for partial_text in type_text_in_word_chunks(cm, chunk_size=3, chunk_delay=0.15, pre_delay=0.75):
                history[-1]["content"] = partial_text
                yield history, user_state, gr.update(visible=False), None
        
        # Check learning path completion
        path_messages = check_learning_path_completion(user_state)
        for pm in path_messages:
            history.append({"role": "assistant", "content": ""})
            for partial_text in type_text_in_word_chunks(pm, chunk_size=3, chunk_delay=0.15, pre_delay=0.75):
                history[-1]["content"] = partial_text
                yield history, user_state, gr.update(visible=False), None
    
    # Update leaderboard
    update_leaderboard(user_state)
    
    # Clear pending notifications after processing
    user_state["pending_notifications"] = {
        "quest_check_needed": False,
        "badges_check_needed": False,
        "level_check_needed": False,
        "learning_path_check_needed": False
    }

def bot(history: list, user_state: dict):
    # 1) Update streak, parse user command, etc...
    update_streak(user_state)
    user_message = str(history[-1]["content"]).strip()
    response = handle_user_message(user_message, user_state)
    
    # Check if response is a tuple (indicating rating is needed)
    course_to_rate = None
    if isinstance(response, tuple) and len(response) == 2:
        immediate_response, course_to_rate = response
    else:
        immediate_response = response

    # Set up pending notifications based on course completion
    user_state["pending_notifications"] = {
        "quest_check_needed": True if course_to_rate else False,
        "badges_check_needed": True if course_to_rate else False,
        "level_check_needed": True if course_to_rate else False,
        "learning_path_check_needed": True if course_to_rate else False
    }

    # 2) Generate the "typing" response for the immediate command
    if immediate_response:
        # First, append an empty message for the assistant
        history.append({"role": "assistant", "content": ""})
        # Now type it out character by character
        for partial_text in type_text_in_word_chunks(immediate_response, chunk_size=3, chunk_delay=0.15, pre_delay=0.75):
            history[-1]["content"] = partial_text
            yield history, user_state, gr.update(visible=False), None

    # After displaying the course completion message, show the rating component if needed
    if course_to_rate:
        # Add an explicit message to draw attention to the rating component
        rating_prompt = f"\n---\n⭐ Please rate **'{course_to_rate}'** using the star rating options **below the chat input**! ⭐\n\n"
        history.append({"role": "assistant", "content": ""})
        for partial_text in type_text_in_word_chunks(rating_prompt, chunk_size=3, chunk_delay=0.15, pre_delay=0.5):
            history[-1]["content"] = partial_text
            yield history, user_state, gr.update(visible=True, label=f"How would you rate **'{course_to_rate}'**?", value=None), course_to_rate
        
        # Important: we return here and don't process the other notifications
        # The handle_rating function will process the pending notifications when rating is submitted
        return

    # Process pending notifications if we're not waiting for a rating
    if "pending_notifications" in user_state:
        notification_generator = process_pending_notifications(history, user_state)
        for hist, state, rating_vis, rating_course in notification_generator:
            yield hist, state, rating_vis, rating_course
    
    yield history, user_state, gr.update(visible=False), None

def handle_rating(rating_value, course_name, history, user_state):
    if course_name and rating_value is not None:
        # Convert stars to number
        rating_number = rating_value.count("⭐")
        
        # Use the existing rate_course function
        rating_result = rate_course(user_state, course_name, str(rating_number))
        history.append({"role": "assistant", "content": ""})
        for partial_text in type_text_in_word_chunks(rating_result, chunk_size=3, chunk_delay=0.15, pre_delay=0.75):
            history[-1]["content"] = partial_text
            yield history, user_state, gr.update(visible=False), None
        
        # Now that rating is complete, process any pending notifications using the refactored function
        if "pending_notifications" in user_state:
            notification_generator = process_pending_notifications(history, user_state)
            for hist, state, rating_vis, rating_course in notification_generator:
                yield hist, state, rating_vis, rating_course
    else: 
        yield history, user_state, gr.update(visible=False), None


theme = gr.themes.Base(
    primary_hue=gr.themes.Color(c100="#d0e2ff", c200="#a6c8ff", c300="#78a9ff", c400="rgba(40.996987409599356, 114.88735362155961, 243.10887145996094, 1)", c50="#edf5ff", c500="#0f62fe", c600="#2563eb", c700="#0043ce", c800="#002d9c", c900="#001141", c950="rgba(0, 0, 0, 1)"),
    secondary_hue=gr.themes.Color(c100="#ffd6e8", c200="#ffafd2", c300="#ff7eb6", c400="#fb7185", c50="#ee5396", c500="#f43f5e", c600="#e11d48", c700="#be123c", c800="#9f1239", c900="#881337", c950="#771d3a"),
    neutral_hue=gr.themes.Color(c100="#dde1e6", c200="#f2f4f8", c300="#c6c6c6", c400="#c1c7cd", c50="#fafafa", c500="#71717a", c600="#52525b", c700="#3f3f46", c800="#27272a", c900="#18181b", c950="#0f0f11"),
    text_size="sm",
    font=[gr.themes.GoogleFont('IBM Plex Sans'), 'ui-sans-serif', 'system-ui', 'sans-serif'],
    font_mono=[gr.themes.GoogleFont('IBM Plex Mono'), 'ui-monospace', 'Consolas', 'monospace'],
).set(
    body_background_fill='*neutral_200',
    body_text_color='*primary_950',
    body_text_color_dark='*primary_950',
    # body_text_size='*text_xxs',
    body_text_color_subdued='*neutral_300',
    body_text_weight='500', 
    embed_radius='*radius_md',
    background_fill_secondary='white',
    prose_text_size='*text_md',
    code_background_fill='*primary_100',
    # prose_text_weight='100',  
    block_label_background_fill='*primary_500',
    block_label_background_fill_dark='*primary_500',
    block_label_text_color='*neutral_300',
    block_label_text_color_dark='white',
    block_title_text_color='*primary_950',
    block_title_text_size='*text_lg',
    block_title_text_weight='500',
    checkbox_background_color='white',
    chatbot_text_size='*text_md',
    checkbox_label_background_fill='*primary_50',
    checkbox_label_background_fill_hover='*primary_500',
    checkbox_label_text_weight='500',
    button_large_text_weight='500',
    button_secondary_background_fill='*primary_500',
    button_secondary_background_fill_dark='*neutral_700',
    button_secondary_background_fill_hover='*primary_700',
    button_secondary_background_fill_hover_dark='*primary_950',
    button_secondary_text_color='white'
)


# 6. Modified Gradio UI setup
with gr.Blocks(theme=theme) as demo:
    user_state = gr.State({
        "user_id": str(uuid.uuid4()),
        "xp": 0,
        "level": "0x1 [Initiate]",
        "badges": [],
        "leaderboard_nickname": None,
        "last_active_date": None,
        "current_streak": 0,
        "longest_streak": 0,
        "completed_courses": [],
        "daily_challenge_date": None,
        "daily_challenge_done": False,
        "current_challenge": None,
        "active_quests": {},
        "pending_action": None,
        "pending_notifications": {
            "quest_check_needed": False,
            "badges_check_needed": False,
            "level_check_needed": False,
            "learning_path_check_needed": False
        },
        "learning_paths_progress": {}
    })

    chatbot = gr.Chatbot(
        value=[
            {
                "role": "assistant",
                "content": (
                    "👋 Welcome to **IBM Course Recommender** - start your personalized learning journey now!\n\n"
                    "**Available Features:**\n"
                    "- 📚 **Courses** - Gain knowledge from different fields\n"
                    "- 🛣️ **Learning Paths** - Structured educational journeys\n"
                    "- 🎯 **Quests** - Complete tasks to earn rewards\n"
                    "- 🧩 **Daily Challenges** - Test your knowledge daily\n"
                    "- 📈 **Progress Tracking** - Monitor your advancement\n"
                    "- 🏆 **Leaderboard** - Compare with other learners\n\n"
                    "Type `help all` to see all commands for every feature\n"
                    "Type `help [feature]` to learn more about any feature (e.g., `help quests`)"
                )
            }
        ],
        elem_id="Chatbot",
        type="messages",
        render_markdown=True  # Add this parameter
        
    )

    chat_input = gr.MultimodalTextbox(
        interactive=True,
        file_count="multiple",
        placeholder="Enter message or upload file...",
        show_label=False,
    )
    
    # Add state to track which course is being rated
    current_rating_course = gr.State(None)
    
    # Add star rating component (hidden by default)
    rating_component = gr.Radio(
        choices=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
        label="Rate this course",
        # value="⭐⭐⭐⭐⭐",  # Default to 5 stars
        visible=False
    )

    chat_msg = chat_input.submit(
        fn=add_message,
        inputs=[chatbot, chat_input],
        outputs=[chatbot, chat_input]
    )

    bot_msg = chat_msg.then(
        fn=bot,
        inputs=[chatbot, user_state],
        outputs=[chatbot, user_state, rating_component, current_rating_course]
    )
    
    # Add change event for the rating component
    rating_component.change(
        fn=handle_rating,
        inputs=[rating_component, current_rating_course, chatbot, user_state],
        outputs=[chatbot, user_state, rating_component, current_rating_course]
    )

    bot_msg.then(
        fn=lambda: gr.MultimodalTextbox(interactive=True),
        inputs=None,
        outputs=[chat_input]
    )

demo.launch()        
        