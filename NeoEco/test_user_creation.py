#!/usr/bin/env python
"""
Test script to manually create a user using the custom User model
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NeoEco.settings')
django.setup()

from ChallengeSetter.models import User

def create_test_user():
    try:
        # Create a test user
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            eco_rank='Silver',
            xp=100,
            level=2,
            avatar_choice='eco_warrior'
        )
        
        print(f"✅ User created successfully!")
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Eco Rank: {user.eco_rank}")
        print(f"XP: {user.xp}")
        print(f"Level: {user.level}")
        print(f"Avatar: {user.avatar_choice}")
        print(f"Date Joined: {user.date_joined}")
        print(f"User ID: {user.id}")
        
        return user
        
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        return None

def list_all_users():
    """List all users in the database"""
    try:
        users = User.objects.all()
        print(f"\n📋 Total users in database: {users.count()}")
        
        for user in users:
            print(f"  - {user.username} ({user.email}) - Level {user.level} {user.eco_rank}")
            
    except Exception as e:
        print(f"❌ Error listing users: {e}")

if __name__ == "__main__":
    print("🧪 Testing custom User model...")
    print("=" * 40)
    
    # Create a test user
    user = create_test_user()
    
    if user:
        print("\n" + "=" * 40)
        # List all users
        list_all_users()
        
        print("\n🎉 User creation test completed successfully!")
    else:
        print("\n❌ User creation test failed!")
