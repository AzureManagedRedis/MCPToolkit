#!/usr/bin/env python3

import os
from dotenv import load_dotenv
import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

load_dotenv()

# Destination data
destinations = [
  {
    "store_name": "destinations",
    "prompt": "A breathtaking wilderness paradise featuring towering granite cliffs, cascading waterfalls, and ancient giant sequoias. Home to iconic landmarks like El Capitan and Half Dome, this majestic and adventurous destination offers world-class hiking, rock climbing, and photography opportunities amidst pristine alpine lakes and meadows. Experience four distinct seasons with snowy winters and warm summers, making spring, summer, and fall the best times to visit this family-friendly nature adventure.",
    "response": "Yosemite National Park, California",
    "metadata": {
      "categories": ["nature", "adventure", "photography", "hiking"],
      "weather": "Four distinct seasons, snowy winters, warm summers",
      "family_friendly": "true",
      "vibe": "Majestic and adventurous",
      "best_season": ["spring", "summer", "fall"]
    },
    "distance_threshold": 0.3
  },
  {
    "store_name": "destinations",
    "prompt": "A vibrant cultural melting pot known for its world-class museums, Broadway theaters, iconic skyline, and diverse neighborhoods. From Central Park to Times Square, this fast-paced and energetic metropolis offers endless dining, shopping, entertainment, and nightlife options in the city that never sleeps. Experience four seasons with hot summers and cold winters, with spring and fall being the best times to visit this family-friendly cultural hub.",
    "response": "New York City, New York",
    "metadata": {
      "categories": ["culture", "entertainment", "food", "shopping", "nightlife"],
      "weather": "Four seasons, hot summers, cold winters",
      "family_friendly": "true",
      "vibe": "Fast-paced and energetic",
      "best_season": ["spring", "fall"]
    },
    "distance_threshold": 0.3
  },
  {
    "store_name": "destinations",
    "prompt": "A mystical landscape of towering red sandstone formations, ancient Native American ruins, and spiritual vortex sites. This peaceful and mystical destination is known for its stunning sunsets, world-class spas, art galleries, and outdoor adventures including hiking, jeep tours, and stargazing in the high desert. Enjoy desert climate with mild winters and hot summers, with spring, fall, and winter being the best seasons for this family-friendly spiritual and wellness retreat focused on nature, art, and adventure.",
    "response": "Sedona, Arizona",
    "metadata": {
      "categories": ["nature", "spiritual", "adventure", "art", "wellness"],
      "weather": "Desert climate, mild winters, hot summers",
      "family_friendly": "true",
      "vibe": "Peaceful and mystical",
      "best_season": ["spring", "fall", "winter"]
    },
    "distance_threshold": 0.3
  },
  {
    "store_name": "destinations",
    "prompt": "A tropical paradise featuring pristine beaches, volcanic landscapes, lush rainforests, and rich Polynesian culture. This relaxed and tropical destination offers world-class surfing, snorkeling, hiking to waterfalls, luaus, and the chance to witness active volcanoes on the Big Island. With warm and humid tropical weather year-round, this family-friendly destination is perfect for beaches, culture, adventure, and relaxation anytime of the year.",
    "response": "Hawaii",
    "metadata": {
      "categories": ["beaches", "tropical", "culture", "adventure", "relaxation"],
      "weather": "Tropical year-round, warm and humid",
      "family_friendly": "true",
      "vibe": "Relaxed and tropical",
      "best_season": ["year-round"]
    },
    "distance_threshold": 0.3
  },
  {
    "store_name": "destinations",
    "prompt": "A city rich in American history featuring cobblestone streets, colonial architecture, and iconic sites like the Freedom Trail, USS Constitution, and Boston Tea Party Ships. This historic and intellectual destination is known for its world-class seafood, prestigious universities, and passionate sports culture. Experience four distinct seasons with cold winters and warm summers, with spring, summer, and fall being the best times to visit this family-friendly hub of history, culture, food, education, and sports.",
    "response": "Boston, Massachusetts",
    "metadata": {
      "categories": ["history", "culture", "food", "education", "sports"],
      "weather": "Four distinct seasons, cold winters, warm summers",
      "family_friendly": "true",
      "vibe": "Historic and intellectual",
      "best_season": ["spring", "summer", "fall"]
    },
    "distance_threshold": 0.3
  },
  {
    "store_name": "destinations",
    "prompt": "A vibrant coastal city known for its year-round perfect Mediterranean climate and laid-back sunny atmosphere. This family-friendly destination features stunning beaches, world-famous zoo, Balboa Park, craft beer scene, and laid-back California lifestyle. Offers excellent surfing, hiking, outdoor activities, and proximity to both Mexico and Los Angeles. With mild weather year-round, this is perfect for beaches, nature, food, and outdoor family adventures anytime of the year.",
    "response": "San Diego, California",
    "metadata": {
      "categories": ["beaches", "nature", "food", "family", "outdoor"],
      "weather": "Mediterranean climate, mild year-round",
      "family_friendly": "true",
      "vibe": "Laid-back and sunny",
      "best_season": ["year-round"]
    },
    "distance_threshold": 0.3
  },
  {
    "store_name": "destinations",
    "prompt": "A dazzling entertainment capital in the desert featuring world-class shows, casinos, luxury resorts, and fine dining. This glamorous and exciting adult-oriented destination offers spectacular nightlife, gaming, and entertainment beyond the Strip, plus proximity to natural wonders like Red Rock Canyon and serves as a gateway to the Grand Canyon. Experience desert climate with very hot summers and mild winters, with spring, fall, and winter being the best seasons for this entertainment and nightlife paradise.",
    "response": "Las Vegas, Nevada",
    "metadata": {
      "categories": ["entertainment", "nightlife", "food", "shows", "gaming"],
      "weather": "Desert climate, very hot summers, mild winters",
      "family_friendly": "false",
      "vibe": "Glamorous and exciting",
      "best_season": ["spring", "fall", "winter"]
    },
    "distance_threshold": 0.3
  },
  {
    "store_name": "destinations",
    "prompt": "A stunning alpine wonderland featuring pristine lakes, snow-capped peaks, and year-round outdoor recreation. This outdoor adventure paradise is famous for world-class skiing in winter and hiking, mountain biking, and water sports in summer, all surrounded by breathtaking Sierra Nevada scenery. Experience alpine climate with snowy winters and warm summers, making winter and summer the best seasons for this family-friendly destination focused on nature, adventure, skiing, lakes, and mountains.",
    "response": "Lake Tahoe, California/Nevada",
    "metadata": {
      "categories": ["nature", "adventure", "skiing", "lakes", "mountains"],
      "weather": "Alpine climate, snowy winters, warm summers",
      "family_friendly": "true",
      "vibe": "Outdoor adventure paradise",
      "best_season": ["winter", "summer"]
    },
    "distance_threshold": 0.3
  },
  {
    "store_name": "destinations",
    "prompt": "A vibrant music city known as the birthplace of jazz, featuring colorful Creole architecture, world-famous cuisine including gumbo and beignets, lively street performances, and an infectious party atmosphere especially during Mardi Gras. This festive and soulful destination celebrates culture, music, food, nightlife, and festivals in a subtropical climate with hot humid summers and mild winters. Winter and spring are the best seasons to visit this family-friendly cultural hub.",
    "response": "New Orleans, Louisiana",
    "metadata": {
      "categories": ["culture", "music", "food", "nightlife", "festivals"],
      "weather": "Subtropical, hot humid summers, mild winters",
      "family_friendly": "true",
      "vibe": "Festive and soulful",
      "best_season": ["winter", "spring"]
    },
    "distance_threshold": 0.3
  },
  {
    "store_name": "destinations",
    "prompt": "One of the world's most awe-inspiring natural wonders featuring dramatic layered rock formations carved by the Colorado River over millions of years. This majestic and humbling destination offers breathtaking viewpoints, hiking trails ranging from easy rim walks to challenging backcountry adventures, and unforgettable sunrise and sunset vistas. Experience desert climate that varies by elevation and season, with spring and fall being the best times to visit this family-friendly destination perfect for nature, hiking, photography, geology, and adventure.",
    "response": "Grand Canyon National Park, Arizona",
    "metadata": {
      "categories": ["nature", "hiking", "photography", "geology", "adventure"],
      "weather": "Desert climate, varies by elevation and season",
      "family_friendly": "true",
      "vibe": "Majestic and humbling",
      "best_season": ["spring", "fall"]
    },
    "distance_threshold": 0.3
  }
]

async def store_destination(session: ClientSession, destination):
    """Store a destination in the semantic cache and search for it."""
    try:
        # Store the destination
        store_tool_name = "knowledge_store_put"
        store_args = {
            "store_name": "destinations",
            "prompt": destination["prompt"],
            "response": destination["response"],
            "metadata": destination["metadata"]
        }
        
        print(f"\nStoring destination: {destination['response']}...")
        store_result = await session.call_tool(store_tool_name, arguments=store_args)
        print(f"✅ Tool result: {store_result.structuredContent['result']}")
        if store_result.content:
            print(store_result.content[0].text)
        else:
            print("No content")

    except Exception as e:
        print(f"Error processing destination {destination['response']}: {e}")


async def main():
    """Test the MCP server using SSE transport"""
    
    # Server configuration
    SSE_URL = os.environ.get("MCP_SERVER_SSE_URL")
    API_KEY = os.environ.get("MCP_API_KEY")
    
    print("=" * 60)
    print("MCP SDK SSE Client Test")
    print("=" * 60)
    print(f"Connecting to: {SSE_URL}\n")
    
    try:
        # Connect to SSE server with API key header
        async with sse_client(
            url=SSE_URL,
            headers={"X-API-Key": API_KEY}
        ) as (read_stream, write_stream):
            print("✅ SSE connection established")
            
            # Create a client session
            async with ClientSession(read_stream, write_stream) as session:
                print("✅ Client session created")
                
                # Initialize the connection
                print("\n📤 Sending initialize request...")
                await session.initialize()
                print("✅ Session initialized")
                
                # List available tools
                print("\n📤 Requesting tools list...")
                tools_response = await session.list_tools()
                print(f"✅ Found {len(tools_response.tools)} tools:")
                for tool in tools_response.tools[:5]:  # Show first 5
                    print(f"   - {tool.name}: {tool.description}")
                if len(tools_response.tools) > 5:
                    print(f"   ... and {len(tools_response.tools) - 5} more")
                                
                # Example: Call info tool
                print("\n📤 Testing Redis info tool...")
                try:
                    result = await session.call_tool("info", arguments={"section": "default"})
                    print(f"✅ info result: {(result.structuredContent or {}).get('result')}")  # Show first 200 chars
                    if result.content:
                        print(f"   {result.content[0].text[:200]}...")  # Show first 200 chars
                except Exception as e:
                    print(f"❌ info failed: {e}")

                # Store and search destinations
                print("\n" + "="*60)
                print("Processing destinations...")
                print("="*60)
            
                for destination in destinations:
                    await store_destination(session, destination)
            
                print("\n" + "="*60)
                print("All destinations have been processed.")
                print("="*60)
                
                
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    asyncio.run(main())
