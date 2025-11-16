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
    }
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
    }
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
    }
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
    }
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
    }
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
    }
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
    }
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
    }
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
    }
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
    }
  },
  {
    "store_name": "destinations",
    "prompt": "A world-renowned beach destination featuring 10 miles of pristine white sand beaches, crystal-clear emerald waters, and charming coastal communities. This laid-back and pristine paradise offers excellent fishing, water sports, beachcombing, and seafood dining in a subtropical climate with mild winters and warm summers. Perfect for families seeking beaches, nature, relaxation, and outdoor activities, with spring through fall being the best seasons to visit this Gulf Coast gem.",
    "response": "Destin, Florida",
    "metadata": {
      "categories": ["beaches", "nature", "relaxation", "family", "fishing"],
      "weather": "Subtropical, mild winters, warm summers",
      "family_friendly": "true",
      "vibe": "Laid-back and pristine",
      "best_season": ["spring", "summer", "fall"]
    }
  },
  {
    "store_name": "destinations",
    "prompt": "A stunning Pacific Coast destination featuring dramatic rocky coastlines, pristine beaches, world-class wineries, and charming coastal towns. This romantic and scenic paradise offers wine tasting, coastal drives, hiking, art galleries, and farm-to-table dining with a Mediterranean climate and mild weather year-round. Perfect for couples and families seeking beaches, nature, food, wine, and relaxation, this destination is beautiful to visit any time of year.",
    "response": "Monterey and Carmel, California",
    "metadata": {
      "categories": ["beaches", "nature", "food", "wine", "romantic"],
      "weather": "Mediterranean climate, mild year-round",
      "family_friendly": "true",
      "vibe": "Romantic and scenic",
      "best_season": ["year-round"]
    }
  },
  {
    "store_name": "destinations",
    "prompt": "A majestic mountain wilderness featuring towering peaks over 14,000 feet, pristine alpine lakes, abundant wildlife, and endless outdoor recreation opportunities. This rugged and inspiring destination offers world-class hiking, fishing, camping, wildlife viewing, and scenic drives through diverse ecosystems from grasslands to alpine tundra. Experience mountain climate with cold snowy winters and mild summers, making summer and early fall the best seasons for this family-friendly nature and adventure paradise.",
    "response": "Rocky Mountain National Park, Colorado",
    "metadata": {
      "categories": ["nature", "adventure", "hiking", "mountains", "wildlife"],
      "weather": "Mountain climate, cold winters, mild summers",
      "family_friendly": "true",
      "vibe": "Rugged and inspiring",
      "best_season": ["summer", "fall"]
    }
  },
  {
    "store_name": "destinations",
    "prompt": "An exclusive island paradise accessible only by ferry, featuring 25 miles of pristine beaches, upscale resorts, world-class golf courses, and charming New England coastal charm. This sophisticated and tranquil destination offers tennis, spa treatments, fine dining, boutique shopping, and maritime activities in a temperate coastal climate. Perfect for luxury-seeking families and couples looking for beaches, relaxation, and refined experiences, with late spring through early fall being the ideal seasons.",
    "response": "Nantucket, Massachusetts",
    "metadata": {
      "categories": ["beaches", "luxury", "relaxation", "golf", "maritime"],
      "weather": "Temperate coastal climate",
      "family_friendly": "true",
      "vibe": "Sophisticated and tranquil",
      "best_season": ["spring", "summer", "fall"]
    }
  },
  {
    "store_name": "destinations",
    "prompt": "A vibrant music city known as the live music capital of the world, featuring eclectic neighborhoods, food trucks, craft breweries, and the famous South by Southwest festival. This hip and creative destination offers outdoor activities around Lady Bird Lake, barbecue cuisine, artistic murals, and a thriving nightlife scene in a warm subtropical climate with hot summers and mild winters. Perfect for culture, music, food, and nightlife enthusiasts, with spring and fall being the most comfortable seasons.",
    "response": "Austin, Texas",
    "metadata": {
      "categories": ["culture", "music", "food", "nightlife", "festivals"],
      "weather": "Subtropical, hot summers, mild winters",
      "family_friendly": "true",
      "vibe": "Hip and creative",
      "best_season": ["spring", "fall"]
    }
  },
  {
    "store_name": "destinations",
    "prompt": "A unique desert oasis featuring otherworldly Joshua tree forests, massive rock formations perfect for climbing, and some of the clearest night skies in the country. This mystical and adventurous destination offers hiking, rock climbing, stargazing, photography, and desert camping in an arid desert climate with mild winters and hot summers. Perfect for nature lovers and adventure seekers, with fall, winter, and spring being the best seasons to avoid extreme summer heat.",
    "response": "Joshua Tree National Park, California",
    "metadata": {
      "categories": ["nature", "adventure", "climbing", "stargazing", "photography"],
      "weather": "Desert climate, hot summers, mild winters",
      "family_friendly": "true",
      "vibe": "Mystical and adventurous",
      "best_season": ["fall", "winter", "spring"]
    }
  },
  {
    "store_name": "destinations",
    "prompt": "A charming Southern coastal city known for its historic architecture, horse-drawn carriage tours, antebellum mansions, and world-renowned culinary scene. This romantic and historic destination features cobblestone streets, beautiful gardens, ghost tours, and proximity to beautiful beaches on nearby islands. Experience humid subtropical climate with mild winters and hot summers, making spring and fall the most pleasant seasons for exploring this family-friendly hub of history, culture, food, and Southern hospitality.",
    "response": "Charleston, South Carolina",
    "metadata": {
      "categories": ["history", "culture", "food", "romantic", "beaches"],
      "weather": "Humid subtropical, mild winters, hot summers",
      "family_friendly": "true",
      "vibe": "Romantic and historic",
      "best_season": ["spring", "fall"]
    }
  },
  {
    "store_name": "destinations",
    "prompt": "A stunning Pacific Northwest coastal destination featuring dramatic sea stacks, pristine beaches, lush temperate rainforests, and charming coastal towns. This serene and wild paradise offers tide pooling, whale watching, lighthouse visits, hiking through old-growth forests, and fresh seafood dining in a cool oceanic climate with mild wet winters and dry summers. Perfect for nature lovers and families seeking beaches, wildlife, and outdoor adventures, with summer being the driest and most popular season.",
    "response": "Oregon Coast",
    "metadata": {
      "categories": ["beaches", "nature", "wildlife", "hiking", "scenic"],
      "weather": "Cool oceanic climate, wet winters, dry summers",
      "family_friendly": "true",
      "vibe": "Serene and wild",
      "best_season": ["summer"]
    }
  },
  {
    "store_name": "destinations",
    "prompt": "A tropical island chain offering endless white sand beaches, crystal-clear turquoise waters, world-class fishing, and vibrant coral reefs. This laid-back and tropical paradise features water sports, snorkeling, diving, conch fritters, key lime pie, and stunning sunsets in a tropical climate with warm weather year-round and occasional hurricanes in late summer. Perfect for families and couples seeking beaches, relaxation, fishing, and tropical experiences anytime of the year.",
    "response": "Florida Keys",
    "metadata": {
      "categories": ["beaches", "tropical", "fishing", "diving", "relaxation"],
      "weather": "Tropical climate, warm year-round",
      "family_friendly": "true",
      "vibe": "Laid-back and tropical",
      "best_season": ["year-round"]
    }
  },
  {
    "store_name": "destinations",
    "prompt": "A dramatic coastal region featuring rugged cliffs, pristine beaches, towering redwood forests, and picturesque seaside villages. This breathtaking and romantic destination offers scenic drives, wine tasting, hiking, art galleries, and farm-to-table dining along one of America's most beautiful coastlines. Experience cool Mediterranean climate with mild temperatures year-round and frequent fog, making this perfect for couples and families seeking nature, beaches, wine, and scenic beauty anytime of the year.",
    "response": "Big Sur, California",
    "metadata": {
      "categories": ["beaches", "nature", "romantic", "wine", "scenic"],
      "weather": "Cool Mediterranean climate, mild year-round",
      "family_friendly": "true",
      "vibe": "Breathtaking and romantic",
      "best_season": ["year-round"]
    }
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
