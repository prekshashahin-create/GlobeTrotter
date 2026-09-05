"""
GlobeTrotter - City Images

Add or replace image URLs in this file whenever you want to change
the image used for a city.

Example:
    "Ahmedabad": "https://example.com/ahmedabad.jpg",

The city name must match the city name stored in the database.
"""

CITY_IMAGES = {

    # Gujarat
    "Ahmedabad": "https://images.trvl-media.com/place/372/39ab7992-befb-4f6f-b31a-491855ea1dfc.jpg",
    "Surat": "https://the-world.in/wp-content/uploads/2024/04/The-World-Blog-Charms-of-Surat-Landscape.webp",
    "Vadodara": "https://s7ap1.scene7.com/is/image/incredibleindia/laxmi-vilas-palace-vadodara-gujarat-1-attr-nearby?qlt=82&ts=1750668517826",
    "Rajkot": "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/23/2e/3e/02/caption.jpg?w=500&h=400&s=1",

    # Maharashtra
    "Mumbai": "https://cdn.getyourguide.com/image/format=auto%2Cfit=crop%2Cgravity=auto%2Cquality=60%2Cwidth=400%2Cheight=265%2Cdpr=2/tour_img/e8049702eb22a5d671cb9dcc55e285c666ce7dcf2819c4ace6b2f5088e9ba04d.jpg",
    "Pune": "https://static2.tripoto.com/media/filter/tst/img/355427/TripDocument/1588571409_rajmachi_fb.jpg",
    "Nashik": "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/23/2e/3e/02/caption.jpg?w=500&h=400&s=1",

    # Rajasthan
    "Jaipur": "https://upload.wikimedia.org/wikipedia/commons/4/41/East_facade_Hawa_Mahal_Jaipur_from_ground_level_%28July_2022%29_-_img_01.jpg?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=original",
    "Udaipur": "https://i0.wp.com/stampedmoments.com/wp-content/uploads/2025/11/bagore-ki-haveli-udaipur-2.jpg?fit=1024%2C576&ssl=1",
    "Jodhpur": "https://www.tourmyindia.com/states/rajasthan/image/jodhpur-banner.webp",
    "Jaisalmer": "",

    # Delhi / Uttar Pradesh
    "Delhi": "https://pohcdn.com/sites/default/files/styles/node__blog_post__bp_banner/public/live_banner/New-Delhi-2.jpg",
    "Agra": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTaY-hASN0CYXleRB6K6oI-6jVZ3l9vl3pkew6RTulYpg&s=10",
    "Varanasi": "https://assets.theasar.com/blogs/1768561498185_top_10_places_to_visit_in_varanasi.webp",
    "Lucknow": "https://static.toiimg.com/photo/msid-89182877,width-96,height-65.cms",

    # Karnataka
    "Bengaluru": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=1600&q=90",
    "Mysore": "https://www.agoda.com/wp-content/uploads/2024/03/Featured-image-Mysore-Palace-Mysore-India.jpg",
    "Hampi": "https://s7ap1.scene7.com/is/image/incredibleindia/a-journey-through-1-body-1?qlt=82&ts=1727368333677",

    # Tamil Nadu
    "Chennai": "https://www.tourmyindia.com/states/tamil-nadu/image/chennai-banner.webphttps://www.agoda.com/wp-content/uploads/2024/03/Chennai-India-1049x700.jpg",
    "Ooty": "https://hblimg.mmtcdn.com/content/hubble/img/destimg/mmt/destination/m_Ooty_main_tv_destination_img_1_l_764_1269.jpg",
    "Madurai": "https://lh5.googleusercontent.com/Ev_NuObJwdnAHczcosV6lYG2VuzlTqMQiLN-LNcGpI2xpjKgRTHUg6HQbny42yjyMRQJopQWfQ9KCXa-IlXT7cn6_iyjupr9HqdT-ReQ7Srf4VtD5CB34Gq7ongizyhBlY34OKwJ",

    # Kerala
    "Kochi": "https://www.awaygowe.com/wp-content/uploads/2023/04/fort-kochi-places-to-visit-15.jpg",
    "Munnar": "https://theleafmunnar.com/wp-content/uploads/2024/11/tea-gardens-munnar.jpg",
    "Alappuzha": "https://cdn.getyourguide.com/image/format=auto,fit=crop,gravity=auto,quality=60,width=375,height=375,dpr=2/tour_img/43a380a61dfd6e1e0f4026e9dc3ea4c572f5d299b6a0c13085051d16d9ccb99a.png",
    "Thiruvananthapuram": "https://www.keralatourism.org/_next/image/?url=http%3A%2F%2F127.0.0.1%2Fktadmin%2Fimg%2Fpages%2Fmobile%2Fthiruvananthapuram-1713788259_cc3e007203a550edfaa7.webp&w=3840&q=75",

    # Goa
    "Goa": "https://res.cloudinary.com/enchanting/q_70,f_auto,w_800,h_800,c_fill,g_face/enchanting-web/2023/09/Beautiful-beach-at-sunset.-Cola-beach-South-GOA.jpg",

    # Telangana
    "Hyderabad": "https://s7ap1.scene7.com/is/image/incredibleindia/charminar-hyderabad-1-attr-nearby?qlt=82&ts=1742177359837",

    # West Bengal
    "Kolkata": "https://c.ndtvimg.com/2026-04/mi60amfs_travel_295x200_15_April_26.jpg",
    "Darjeeling": "https://media.assettype.com/outlooktraveller/2024-06/6c5dc4ec-67f0-49c9-9947-2cbb40a6509a/darjeeling3.jpg?w=1200&h=675&auto=format%2Ccompress&fit=max&enlarge=true",

    # Himachal Pradesh
    "Manali": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTDS9UpSIY2zUISzEJm9kj6FRHDrxbkVRzyaZwu1HAi6BHtwnke3rGB-F8&s=10",
    "Shimla": "https://www.orchidhotel.com/static/website/images/home/shimla/blog/cityscape-of-shimla-himachal-pradesh-city_slider.webp",
    "Dharamshala": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQODs6rLYuYg-YjJdMuYyQuhGWmYNoi-q3_-DLaDFleNP18WmOvJdyFnnp&s=10",

    # Uttarakhand
    "Rishikesh": "https://images.contentstack.io/v3/assets/blt06f605a34f1194ff/blt80398e03b309f555/68a82def94a89550e2e57d49/lucas-hemingway-Ezp5CvwKoXQ-unsplash-header_mobile.jpg?format=webp&auto=avif&quality=60&crop=1%3A1&width=1440",
    "Mussoorie": "https://hblimg.mmtcdn.com/content/hubble/img/destimg/mmt/destination/m_Mussorrie_main_tv_destination_img_1_l_639_958.jpg",
    "Nainital": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Nainital_metro.jpg/1280px-Nainital_metro.jpg?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=thumbnail",

    # Jammu & Kashmir / Ladakh
    "Srinagar": "https://images.unsplash.com/photo-1595815771614-ade9d652a65d?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3MDk0ODZ8MHwxfHNlYXJjaHwxfHxTcmluYWdhcnxlbnwwfDB8fHwxNzM5NTMyOTc3fDA&ixlib=rb-4.0.3&q=85",
    "Leh": "https://assets.cntraveller.in/photos/60ba09c482b06272bc86ba08/1:1/w_1080,h_1080,c_limit/lehguidelead.jpg",
    "Gulmarg": "https://tripmore.in/wp-content/uploads/2022/04/Gulmarg-Beautiful-1024x1024.jpg",

    # Other popular destinations
    "Amritsar": "https://amritsartourism.org.in/images/places-to-visit/headers/places-to-visit-in-amritsar-header-amritsar-tourism.jpg.jpg",
    "Chandigarh": "https://s7ap1.scene7.com/is/image/incredibleindia/chandigarh-union-territory-1-city-ff?qlt=82&ts=1742195658178",
    "Indore": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Indore_Rajwada01.jpg/1280px-Indore_Rajwada01.jpg?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=thumbnail",
    "Bhubaneswar": "https://s7ap1.scene7.com/is/image/incredibleindia/1-lingaraj-temple-bhubaneshwar-odisha-city-hero?qlt=82&ts=1742167192930",
    "Visakhapatnam": "https://d26dp53kz39178.cloudfront.net/media/uploads/products/image7_result-1674872843438.webp",
    "Pondicherry": "https://production-nuego-cms.blr1.digitaloceanspaces.com/static-contents/prod-v1/Hero_Image_277_X_277_px_72f5e86051.jpg",
    "Dubai": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=1200&q=80",
    "New York": "https://images.unsplash.com/photo-1485871981521-5b1fd3805eee?auto=format&fit=crop&w=1200&q=80",
    "Paris": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=1200&q=80",
    "Seoul": "https://www.pelago.com/img/destinations/seoul/hero-image-large.jpg",
}


def get_city_image(city_name):
    """Return the image URL for a city, or an empty string if not added."""
    return CITY_IMAGES.get(city_name, "")