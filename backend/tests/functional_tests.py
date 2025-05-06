import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import datetime

# Adjust this path to point to your module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import from your module
from backend.ibm_course_recommender import (
    handle_user_message, process_course_completion, start_quest,
    start_learning_path, check_chapter_completion, join_leaderboard,
    check_quests, check_learning_path_completion, leaderboard,
    show_leaderboard, get_course_average_rating, rate_course,
    check_skill_badges, initialize_course_ratings
)

class FunctionalTests(unittest.TestCase):
    def setUp(self):
        # Create a fresh user state before each test
        self.user_state = {
            "user_id": "test_user_id",
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
        }
        # Ensure course ratings are initialized
        initialize_course_ratings()
        
    def tearDown(self):
        # Clean up the leaderboard after each test
        global leaderboard
        leaderboard = [entry for entry in leaderboard if entry["user_id"] != "test_user_id"]
        
    def test_course_completion_workflow(self):
        """Test the complete workflow of completing a course"""
        # 1. Complete a course
        result, course_to_rate = process_course_completion(self.user_state, "Python for Everybody")
        
        # Verify results
        self.assertIsNotNone(course_to_rate)  # Should return a course to rate
        self.assertEqual(course_to_rate, "Python for Everybody")
        self.assertIn("Python for Everybody", self.user_state["completed_courses"])
        self.assertEqual(self.user_state["xp"], 50)  # Check XP was awarded
        
        # 2. Rate the course
        rating_result = rate_course(self.user_state, "Python for Everybody", "5")
        
        # 3. Check that rating increased XP
        self.assertEqual(self.user_state["xp"], 60)  # 50 + 10 for rating
        
        # 4. Verify quest progress if this course was part of any quests
        quest_messages = check_quests(self.user_state)
        
        # 5. Check if badge was earned
        badges_before = len(self.user_state["badges"])
        check_skill_badges(self.user_state)
        
        # If this single course completes a badge, we'll see it
        if len(self.user_state["badges"]) > badges_before:
            self.assertGreater(len(self.user_state["badges"]), badges_before)
        
    def test_starting_quest(self):
        """Test starting a quest"""
        result = start_quest(self.user_state, "Data Science Starter")
        
        # Verify the quest was started
        self.assertTrue(self.user_state["active_quests"]["Data Science Starter"]["started"])
        self.assertFalse(self.user_state["active_quests"]["Data Science Starter"]["completed"])
        
    def test_completing_quest(self):
        """Test the workflow of completing a quest"""
        # 1. Start a quest
        start_quest(self.user_state, "Data Science Starter")
        
        # 2. Complete the required courses
        process_course_completion(self.user_state, "Python for Everybody")
        process_course_completion(self.user_state, "Intro to Data Science")
        
        # 3. Check if quest is completed
        quest_messages = check_quests(self.user_state)
        
        # Verify quest completion
        self.assertTrue(self.user_state["active_quests"]["Data Science Starter"]["completed"])
        self.assertIn("Data Science Starter Badge", self.user_state["badges"])
        self.assertEqual(self.user_state["xp"], 100 + 100)  # 2 courses (50 each) + 100 for quest
        
    def test_learning_path_workflow(self):
        """Test the workflow of a learning path"""
        # 1. Start a learning path
        result = start_learning_path(self.user_state, "Data Science Fundamentals")
        
        # 2. Complete courses in the first chapter
        process_course_completion(self.user_state, "Python for Everybody")
        process_course_completion(self.user_state, "Intro to Data Science")
        
        # 3. Check chapter completion
        messages = check_chapter_completion(self.user_state)
        
        # 4. Verify chapter completion and progress to next chapter
        path_progress = self.user_state["learning_paths_progress"]["Data Science Fundamentals"]
        self.assertIn(0, path_progress["chapters_completed"])
        self.assertEqual(path_progress["current_chapter"], 1)
        
        # 5. Complete final chapter and check learning path completion
        process_course_completion(self.user_state, "Machine Learning Basics")
        check_chapter_completion(self.user_state)
        
        # Check learning path completion and rewards
        completion_messages = check_learning_path_completion(self.user_state)
        
        # Should be completed
        self.assertTrue(path_progress["completed"])
        self.assertIn("Data Science Explorer Badge", self.user_state["badges"])
        
    def test_leaderboard_functionality(self):
        """Test joining and viewing the leaderboard"""
        # Give the user some XP first
        self.user_state["xp"] = 500
        
        # 1. Join the leaderboard
        result = join_leaderboard(self.user_state, "TestUser")
        
        # 2. Verify the user is on the leaderboard
        self.assertEqual(self.user_state["leaderboard_nickname"], "TestUser")
        
        # 3. View the leaderboard
        leaderboard_view = show_leaderboard(top_n=5, user_state=self.user_state)
        
        # 4. Verify the user is visible on the leaderboard
        self.assertIn("TestUser", leaderboard_view)
        
    def test_level_progression(self):
        """Test level progression when earning XP"""
        from backend.ibm_course_recommender import check_level_up
        
        # Initially at level 0x1
        self.assertEqual(self.user_state["level"], "0x1 [Initiate]")
        
        # Add XP to reach level 0x2
        self.user_state["xp"] = 250
        
        # Check level
        level_up_message = check_level_up(self.user_state)
        
        # Verify level up
        self.assertEqual(self.user_state["level"], "0x2 [Explorer]")
        self.assertNotEqual(level_up_message, "")
        
        # Add more XP to reach level 0x4
        self.user_state["xp"] = 1200
        
        # Check level again
        level_up_message = check_level_up(self.user_state)
        
        # Verify new level
        self.assertEqual(self.user_state["level"], "0x4 [Vanguard]")
        
    def test_command_parsing(self):
        """Test the command parsing functionality"""
        # Test well-formed command
        result = handle_user_message("show xp", self.user_state)
        self.assertIsNotNone(result)
        self.assertIn("XP", result)
        
        # Test course completion command
        result = handle_user_message("completed course Python for Everybody", self.user_state)
        self.assertIn("Python for Everybody", self.user_state["completed_courses"])
        
        # Test quest command
        result = handle_user_message("show quests", self.user_state)
        self.assertIn("Available Quests", result)
        
        # Test learning path command
        result = handle_user_message("list learning paths", self.user_state)
        self.assertIn("Learning Paths", result)
        
    def test_recommendations(self):
        """Test the recommendation functionality"""
        # Test data science recommendation with a more direct phrase
        # Test data science recommendation with a more direct phrase
        result = handle_user_message("I'm interested in data science courses", self.user_state)
        self.assertIn("Data Science", result)
        
        # Test cybersecurity recommendation
        result = handle_user_message("I want to learn cybersecurity", self.user_state)
        self.assertIn("Cyber Security", result)
        
    def test_multi_step_interactions(self):
        """Test multi-step interactions with the system"""
        # Start a command that requires multiple steps
        result = handle_user_message("join leaderboard", self.user_state)
        
        # Verify pending action is set
        self.assertEqual(self.user_state["pending_action"], "join_leaderboard")
        
        # Complete the command in the next step
        result = handle_user_message("TestUser123", self.user_state)
        
        # Verify action is completed
        self.assertIsNone(self.user_state["pending_action"])
        self.assertEqual(self.user_state["leaderboard_nickname"], "TestUser123")

if __name__ == "__main__":
    unittest.main()