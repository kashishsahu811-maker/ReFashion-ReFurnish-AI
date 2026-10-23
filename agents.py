"""
================================================================================
ReFashion & ReFurnish AI - Multi-Agent Architecture (agents.py)
--------------------------------------------------------------------------------
This module implements a transparent, rule-based Multi-Agent System designed
for educational and practical circular economy applications.

AGENTS INCLUDED:
1. FashionAgent: Suggests upcycling ideas for clothes and fabric waste.
2. FurnitureAgent: Suggests reuse and renovation ideas for old furniture.
3. BusinessAgent: Calculates production costs, profit margins, and generates 
   marketing captions.
4. AgentCoordinator: Routes natural language requests to the correct agent using
   keyword and intent heuristics.

NOTE: This system uses transparent, deterministic expert-system rules.
It does NOT use a paid API or an external LLM, ensuring zero cost, 100% offline
availability, and full explainability for academic evaluations.
================================================================================
"""

import random
import io
import urllib.parse
from typing import Dict, List, Any, Tuple
from PIL import Image, ImageDraw, ImageFont


# =====================================================================
# 1. KNOWLEDGE MATRICES (DETERMINISTIC EXPERT SYSTEM RULES)
# =====================================================================

FASHION_KNOWLEDGE_BASE = {
    "Old Denim Jeans": [
        {
            "name": "Classic Denim Patchwork Tote Bag",
            "category": "Bags & Totes",
            "difficulty": "Intermediate",
            "time_estimate": "1.5 - 2 Hours",
            "no_sew": False,
            "tools_needed": ["Fabric Scissors", "Sewing Machine or Heavy Hand Needle", "Pins", "Measuring Tape", "Iron"],
            "materials_needed": ["1 Pair of Old Denim Jeans", "Lining fabric (cotton bedsheet or scrap)", "Strong cotton thread"],
            "steps": [
                "Cut the trouser legs off right below the back pockets. Save legs for handles.",
                "Cut straight along the inner leg seams to flatten out the pant legs into rectangular denim panels.",
                "Stitch the bottom hem of the shorts portion shut to form the bottom of the tote pouch.",
                "Cut two 3-inch wide strips from the saved leg fabric, fold lengthwise, iron, and topstitch to create strong carry handles.",
                "Attach handles securely inside the top waistband using a heavy box-cross stitch for durability.",
                "Optional: Insert a cotton lining inside for an ultra-clean retail finish!"
            ],
            "pro_tip": "Keep the original back pockets intact on the outside! They serve as functional quick-access phone and transit pass slots.",
            "water_saved": "2,400 Liters",
            "co2_saved": "1.8 kg CO2"
        },
        {
            "name": "No-Sew Hanging Pocket Wall Organizer",
            "category": "Home Decor & Storage",
            "difficulty": "Beginner (No-Sew)",
            "time_estimate": "30 - 45 Minutes",
            "no_sew": True,
            "tools_needed": ["Fabric Scissors", "Hot Glue Gun or Fabric Glue", "Wooden Dowel or Tree Branch", "Twine"],
            "materials_needed": ["Cut-off back and front pockets from 2-3 old jeans", "1 Flat piece of cardboard or burlap canvas"],
            "steps": [
                "Carefully cut around the back pockets of your old jeans, leaving a 1/2 inch denim border around each.",
                "Lay out a backing fabric (or canvas sheet) and arrange the pockets in a 2x3 or 3x3 grid.",
                "Apply hot glue or heavy fabric glue along the bottom and sides of each pocket border, pressing firmly.",
                "Fold the top edge of the backing fabric over a wooden dowel rod and glue down to create a hanging sleeve.",
                "Tie natural jute twine to both ends of the dowel and hang it in your study, bedroom, or craft room."
            ],
            "pro_tip": "Use pockets of different denim shades (light wash, dark indigo, black) to create an eye-catching ombre wall piece.",
            "water_saved": "1,800 Liters",
            "co2_saved": "1.2 kg CO2"
        },
        {
            "name": "Upcycled Denim Pot Holders & Coasters Set",
            "category": "Kitchen & Dining",
            "difficulty": "Beginner",
            "time_estimate": "45 Minutes",
            "no_sew": False,
            "tools_needed": ["Fabric Shears", "Sewing Machine or Needle", "Ruler", "Iron"],
            "materials_needed": ["Jeans pant legs", "Old cotton towel (for inner heat insulation)", "Contrast thread"],
            "steps": [
                "Cut denim fabric into 8-inch by 8-inch squares (4 pieces per pot holder).",
                "Cut a matching 8-inch square from an old worn cotton towel to act as a heat-resistant batting.",
                "Layer: Denim (face down) + Towel Batting + Denim (face up). Pin layers together.",
                "Sew around all four edges leaving a 1/2 inch border. Backstitch corners for durability.",
                "Stitch diagonal criss-cross quilting lines across the square for a chic quilted texture.",
                "Gently fray the outer denim borders with a brush or fork for an artisan fringe aesthetic."
            ],
            "pro_tip": "Denim is 100% thick woven cotton, making it naturally heat-resistant and one of the best kitchen textiles.",
            "water_saved": "1,200 Liters",
            "co2_saved": "0.9 kg CO2"
        }
    ],
    "Cotton T-Shirts": [
        {
            "name": "10-Minute Zero-Sew Market Produce Bag",
            "category": "Bags & Totes",
            "difficulty": "Beginner (No-Sew)",
            "time_estimate": "10 - 15 Minutes",
            "no_sew": True,
            "tools_needed": ["Sharp Fabric Scissors", "Ruler", "Chalk or Pencil"],
            "materials_needed": ["1 Old Graphic or Plain Cotton T-Shirt"],
            "steps": [
                "Lay the t-shirt completely flat on a table.",
                "Cut off both sleeves along the inner seams (these armholes become your carry handles).",
                "Cut around the neckline in a deep U-shape to create the wide open top of the tote bag.",
                "Turn the shirt inside out. Cut 3-inch vertical slits along the bottom hem, spaced 1 inch apart, creating matching front/back fringe strips.",
                "Tie each front strip tightly to its corresponding back strip in a double knot to seal the bottom.",
                "Turn right side out: Your eco-friendly grocery and fruit market bag is 100% ready to use!"
            ],
            "pro_tip": "Stretchy cotton jersey naturally expands to hold surprisingly heavy loads of groceries or gym gear.",
            "water_saved": "2,700 Liters",
            "co2_saved": "2.1 kg CO2"
        },
        {
            "name": "Braided T-Shirt Yarn Macramé Plant Hanger",
            "category": "Home Decor & Greenery",
            "difficulty": "Beginner (No-Sew)",
            "time_estimate": "35 Minutes",
            "no_sew": True,
            "tools_needed": ["Fabric Scissors", "Measuring Tape", "Metal Key Ring or Wooden Ring"],
            "materials_needed": ["1 or 2 Stretchy Cotton T-Shirts", "1 Indoor Potted Plant (4-6 inch pot)"],
            "steps": [
                "Cut the body of the t-shirt horizontally into continuous 1-inch wide strips.",
                "Gently pull and stretch the strips; the raw cotton edges will curl inward, miraculously transforming into seamless 't-shirt yarn'.",
                "Cut 8 strands of yarn, each roughly 3 feet long. Thread through a metal ring and tie in a master top knot.",
                "Divide into 4 pairs of 2 strands. Tie simple overhand knots about 12 inches below the ring.",
                "Cross adjacent strands and knot them together 3 inches lower to form a diamond net cradle.",
                "Gather all 8 strands together at the base and secure with a tight finishing gathering knot. Place your pot inside!"
            ],
            "pro_tip": "Combine two contrasting shirt colors (e.g., olive green and off-white) for a modern bohemian plant display.",
            "water_saved": "2,700 Liters",
            "co2_saved": "2.0 kg CO2"
        },
        {
            "name": "Braided Pet Chew & Tug Toy",
            "category": "Pet Accessories",
            "difficulty": "Beginner (No-Sew)",
            "time_estimate": "15 Minutes",
            "no_sew": True,
            "tools_needed": ["Fabric Scissors"],
            "materials_needed": ["1 Old Cotton T-Shirt"],
            "steps": [
                "Cut the t-shirt into 6 long strips of fabric, roughly 2 inches wide.",
                "Gather all strips together and tie a firm, tight knot at one end.",
                "Divide the strips into three sets of 2 strands and braid tightly all the way down.",
                "Finish with a tight double knot at the other end.",
                "Trim the fringe ends evenly for a clean, playful look. Safe and machine washable for dogs!"
            ],
            "pro_tip": "Dip the toy in water and freeze it in hot summers — pets adore cool chew toys for soothing their gums!",
            "water_saved": "2,500 Liters",
            "co2_saved": "1.9 kg CO2"
        }
    ],
    "Silk Saree / Vintage Scarf / Dupatta": [
        {
            "name": "Boho Chic Kimono Shrug / Beach Cardigan",
            "category": "Wearable Fashion",
            "difficulty": "Beginner",
            "time_estimate": "30 Minutes",
            "no_sew": False,
            "tools_needed": ["Fabric Scissors", "Sewing Machine or Needle/Thread", "Measuring Tape", "Pins"],
            "materials_needed": ["1 Rectangular Silk Scarf, Dupatta, or Saree Section (approx. 40x60 inches)"],
            "steps": [
                "Fold the rectangular fabric horizontally in half, with right sides facing inward.",
                "Measure 8 inches down from the folded top corner on both the left and right outer sides (these form the arm openings).",
                "Pin from the 8-inch mark down to the bottom hem on both left and right sides.",
                "Sew a simple straight stitch along both pinned sides to close the torso.",
                "Unfold and find the center of the top layer front. Cut a straight vertical line all the way up through the top layer only.",
                "Hem the raw cut edges with a narrow 1/4-inch rolled hem or add decorative lace trim!"
            ],
            "pro_tip": "Traditional zari or golden border sections of sarees look spectacular when positioned along the front lapels or sleeve edges.",
            "water_saved": "3,200 Liters",
            "co2_saved": "3.5 kg CO2"
        },
        {
            "name": "Luxury Silk Scrunchies & Eyemask Duo",
            "category": "Personal Accessories",
            "difficulty": "Beginner",
            "time_estimate": "25 Minutes",
            "no_sew": False,
            "tools_needed": ["Scissors", "Needle & Thread", "Safety Pin", "Iron"],
            "materials_needed": ["Silk saree scrap (4x18 inches for scrunchie)", "Elastic band (8 inches)", "Soft cotton scrap for padding"],
            "steps": [
                "Cut a silk rectangle 4 inches wide by 18 inches long.",
                "Fold in half lengthwise with right sides touching; sew along the long edge to form a hollow tube.",
                "Use a safety pin attached to one end to pull the tube right-side out.",
                "Feed the 8-inch elastic band through the silk tube using the safety pin.",
                "Tie or stitch the elastic ends together firmly in a knot.",
                "Tuck one raw end of the silk tube inside the other and hand-stitch closed using an invisible ladder stitch."
            ],
            "pro_tip": "Silk reduces hair friction and prevents split ends. Retail silk scrunchies sell for $10-$15 each, costing almost nothing to make!",
            "water_saved": "1,500 Liters",
            "co2_saved": "1.1 kg CO2"
        }
    ],
    "Woolen Sweaters": [
        {
            "name": "Felted Wool Mittens & Hand Warmers",
            "category": "Winter Accessories",
            "difficulty": "Beginner",
            "time_estimate": "45 Minutes",
            "no_sew": False,
            "tools_needed": ["Fabric Scissors", "Needle", "Embroidery Thread", "Paper & Pen (for template)"],
            "materials_needed": ["1 Old 100% Wool Shrunken Sweater", "Decorative Buttons (optional)"],
            "steps": [
                "Felting prep: Wash the woolen sweater in hot water and tumble dry on high heat so the fibers interlock and won't fray when cut.",
                "Trace your hand on a sheet of paper with fingers together and thumb spread out, adding 1/2 inch seam allowance all around.",
                "Cut out the paper stencil and pin it onto the lower ribbed hem of the sweater (the hem becomes your natural wrist cuff!).",
                "Cut 4 mitten pieces (2 pairs). Place front and back together with right sides facing inward.",
                "Stitch along the outer perimeter using a blanket stitch or sewing machine stretch stitch.",
                "Turn right side out and embroider small accent stars or sew a vintage button at the wrist."
            ],
            "pro_tip": "The ribbed bottom cuffs of the sweater provide pre-made elastic wrists that fit comfortably without adding rubber bands.",
            "water_saved": "3,000 Liters",
            "co2_saved": "4.2 kg CO2"
        },
        {
            "name": "Cable-Knit Coffee Mug Cozy & Candle Sleeves",
            "category": "Home & Giftware",
            "difficulty": "Beginner",
            "time_estimate": "20 Minutes",
            "no_sew": False,
            "tools_needed": ["Scissors", "Needle & Thread", "1 Vintage Wooden Button"],
            "materials_needed": ["Sleeves from an old cable-knit sweater", "Short elastic hair tie"],
            "steps": [
                "Cut a 4-inch cylinder piece from the sweater sleeve.",
                "Turn inside out and hem both raw edges using a quick whipstitch to stop unraveling.",
                "If using for a mug with a handle, snip a vertical slit down one side.",
                "Sew a small elastic loop on one edge of the slit and a charming wooden button on the opposite edge.",
                "Wrap around your favourite hot coffee mug or mason jar candle to protect hands from heat!"
            ],
            "pro_tip": "Spray with a drop of cinnamon or vanilla essential oil for a cozy holiday aroma when warmed by your hot drink.",
            "water_saved": "1,000 Liters",
            "co2_saved": "0.8 kg CO2"
        }
    ],
    "Flannel & Plaid Shirts": [
        {
            "name": "Farmhouse Plaid Throw Pillow with Button Placket",
            "category": "Home Decor",
            "difficulty": "Beginner",
            "time_estimate": "40 Minutes",
            "no_sew": False,
            "tools_needed": ["Scissors", "Pins", "Sewing Machine or Needle/Thread", "Iron"],
            "materials_needed": ["1 Men's Flannel / Button-Down Shirt", "14x14 or 16x16 inch pillow insert or cotton scrap stuffing"],
            "steps": [
                "Button the shirt up completely and lay it flat, front side facing up.",
                "Place your square pillow insert over the chest area, centering the button placket right down the middle.",
                "Mark a square 1 inch wider than the pillow insert on all four sides with tailor's chalk.",
                "Cut through both the front and back shirt layers along your marked lines.",
                "Unbutton the shirt halfway (crucial step for turning it inside out later!).",
                "Pin the front and back squares together with right sides facing, and sew around all 4 outer edges.",
                "Reach through the unbuttoned opening, turn right side out, insert the pillow cushion, and button it back up!"
            ],
            "pro_tip": "The original button closure serves as an envelope pillow opening, so you never need to sew in a zipper!",
            "water_saved": "2,100 Liters",
            "co2_saved": "1.7 kg CO2"
        }
    ],
    "Fabric Scraps & Remnants": [
        {
            "name": "Zero-Waste Quilted Hexie Coaster Set",
            "category": "Dining & Decor",
            "difficulty": "Beginner",
            "time_estimate": "35 Minutes",
            "no_sew": False,
            "tools_needed": ["Scissors", "Hand Needle", "Iron", "Cardstock Template"],
            "materials_needed": ["Small colorful fabric scraps (2-3 inches)", "Old fleece or felt scrap for backing"],
            "steps": [
                "Cut a 2.5-inch hexagon stencil from thin cardboard or an old cereal box.",
                "Trace and cut 7 fabric hexagons from assorted scraps of contrasting colors.",
                "Baste fabric edges over the cardstock hexagon templates and press flat with an iron.",
                "Whipstitch the 7 hexagons together (1 in center, 6 surrounding) using English Paper Piecing technique.",
                "Remove the paper templates, lay over a felt backing circle, and topstitch around the outer rim.",
                "Press with steam for a lovely bespoke artisan coffee coaster."
            ],
            "pro_tip": "This English Paper Piecing (EPP) technique is completely relaxing, highly therapeutic, and uses bits as tiny as 2 inches.",
            "water_saved": "800 Liters",
            "co2_saved": "0.6 kg CO2"
        },
        {
            "name": "Aromatherapy Wardrobe Sachets with Dried Lavender",
            "category": "Home Wellness",
            "difficulty": "Beginner (No-Sew Friendly)",
            "time_estimate": "15 Minutes",
            "no_sew": True,
            "tools_needed": ["Pinking Shears or Scissors", "Fabric Glue or Needle", "Ribbon"],
            "materials_needed": ["Scrap cotton or linen squares (5x5 inches)", "Dried lavender flowers or cloves/cinnamon chips"],
            "steps": [
                "Cut two 5x5 inch squares using pinking shears (zigzag cut prevents fabric fraying naturally).",
                "Glue or sew three sides together to form a small pouch.",
                "Fill pouch 3/4 full with dried lavender buds, cedar shavings, or dried rose petals.",
                "Insert a loop of jute ribbon into the open top and seal the fourth edge with glue or a tight hand stitch.",
                "Toss in wardrobe drawers, shoe racks, or hang in closets to naturally repel moths and freshen clothes."
            ],
            "pro_tip": "Lavender and cloves are natural moth repellents that keep your stored garments smelling pristine without chemical mothballs.",
            "water_saved": "500 Liters",
            "co2_saved": "0.4 kg CO2"
        }
    ]
}

FURNITURE_KNOWLEDGE_BASE = {
    "Wooden Shipping Pallet": [
        {
            "name": "Rustic Balcony Vertical Herb Garden & Planter",
            "category": "Balcony & Garden",
            "difficulty": "Beginner",
            "time_estimate": "1.5 - 2 Hours",
            "power_tools_needed": False,
            "tools_needed": ["Hammer & Nails", "Sandpaper (80-grit & 150-grit)", "Staple Gun", "Measuring Tape", "Hand Saw"],
            "materials_needed": ["1 Standard Wooden Shipping Pallet", "Landscaping weed fabric", "Exterior weatherproof wood sealant or chalk paint", "Potting soil & herb saplings"],
            "steps": [
                "Inspect the pallet: Look for the 'HT' stamp (Heat Treated - safe for plants and food herbs. Avoid 'MB' chemical pallets).",
                "Thoroughly sand the front slats and edges with 80-grit sandpaper to remove rough splinters, finishing smooth with 150-grit.",
                "Nail extra wooden slat scraps beneath the internal horizontal crossbars to create bottom planter trough floors.",
                "Line the inside troughs with permeable landscape fabric using heavy-duty staples to retain soil while allowing water drainage.",
                "Paint the exterior with sage green or matte white exterior wood paint and let dry completely.",
                "Fill troughs with organic potting soil and plant fresh mint, basil, rosemary, and thyme herbs!"
            ],
            "finishing_tip": "Paint slat headers with black chalkboard paint so you can write herb names in chalk (e.g., 'Basil', 'Mint')!",
            "landfill_diverted": "20 kg Timber",
            "co2_saved": "15 kg CO2"
        },
        {
            "name": "Industrial Chic Mobile Coffee Table on Castor Wheels",
            "category": "Living Room",
            "difficulty": "Intermediate",
            "time_estimate": "3 Hours",
            "power_tools_needed": True,
            "tools_needed": ["Power Drill / Screwdriver", "Orbital Sander or Sanding Block", "Safety Goggles & Mask"],
            "materials_needed": ["1 or 2 Sturdy Wooden Pallets", "4 Heavy-duty swivel rubber castor wheels (2 with lock brakes)", "16 Heavy wood screws", "Walnut wood stain & clear polyurethane varnish"],
            "steps": [
                "Disassemble loose slats or use an orbital sander across the entire top surface until the pine grain is silky smooth.",
                "Fill gaps on top by nailing extra pallet slats flush next to each other to create a solid tabletop surface.",
                "Flip the pallet over and position one castor wheel at each of the four sturdy corner structural blocks.",
                "Pre-drill pilot holes and securely mount the castors using heavy-duty lag wood screws.",
                "Apply two coats of rich walnut or teak wood stain using a rag, letting each coat soak in for 15 minutes before wiping excess.",
                "Seal with two coats of satin clear polyurethane sealant to protect against coffee spills and water rings."
            ],
            "finishing_tip": "The hollow center section of the pallet creates natural dual-sided cubbies perfect for storing magazines, laptops, and TV remotes.",
            "landfill_diverted": "25 kg Timber",
            "co2_saved": "18 kg CO2"
        }
    ],
    "Broken or Wobbly Wooden Chair": [
        {
            "name": "Vintage Chair-Back Wall Coat & Towel Rack",
            "category": "Entryway & Bathroom",
            "difficulty": "Beginner",
            "time_estimate": "1 Hour",
            "power_tools_needed": False,
            "tools_needed": ["Hand Saw", "Sandpaper", "Screwdriver", "2 Heavy D-Ring Wall Hooks"],
            "materials_needed": ["1 Old Wooden Spindle or Ladder-Back Chair", "Chalk Paint (Sage Green or Off-White)", "Clear Wax", "3 Vintage Brass Hooks"],
            "steps": [
                "Use a simple handsaw to carefully cut the backrest off the chair right at the level of the seat base.",
                "Sand the cut bottom flat and sand away any old chipping varnish across the decorative spindles.",
                "Paint two coats of matte chalk paint in an earthy cream or sage tone; no primer required on wood!",
                "Once dry, gently sand the corners with 220-grit sandpaper for an authentic French provincial distressed antique look.",
                "Screw 3 decorative brass coat hooks along the bottom crossbar.",
                "Attach heavy D-ring mounting brackets on the back and securely hang on your wall for coats, hats, and scarves."
            ],
            "finishing_tip": "If the chair had an ornate carved top crest, paint it with a soft gold leaf wax to highlight the vintage craftsmanship.",
            "landfill_diverted": "6 kg Hardwood",
            "co2_saved": "8 kg CO2"
        },
        {
            "name": "Garden Flower Pot Display Stand",
            "category": "Garden & Patio",
            "difficulty": "Beginner",
            "time_estimate": "45 Minutes",
            "power_tools_needed": False,
            "tools_needed": ["Hammer", "Sandpaper", "Paint Brush"],
            "materials_needed": ["1 Wobbly Chair with broken cane or fabric seat", "1 Terra Cotta Planter Pot (with lip)", "Outdoor waterproof acrylic enamel paint"],
            "steps": [
                "Remove the broken woven cane or damaged foam fabric seat padding, leaving the open hollow seat frame.",
                "Tighten any wobbly legs by driving wood glue into loose dowel joints and tapping tight with a rubber mallet.",
                "Sand down rough patches and paint the chair a vibrant garden color like olive green, buttercup yellow, or duck-egg blue.",
                "Ensure your terracotta flower pot's rim diameter is 1 inch wider than the hollow seat cutout.",
                "Drop the pot directly through the open seat so its upper rim rests securely on the chair frame.",
                "Plant cascading English ivy, petunias, or ferns for an enchanting storybook garden centerpiece!"
            ],
            "finishing_tip": "Drill small drainage holes if using a wooden shelf, or let the natural plant saucer sit beneath the chair legs.",
            "landfill_diverted": "7 kg Timber",
            "co2_saved": "9 kg CO2"
        }
    ],
    "Discarded Wooden Drawer": [
        {
            "name": "Rolling Under-Bed Storage Trundle Box",
            "category": "Bedroom & Storage",
            "difficulty": "Beginner",
            "time_estimate": "1 Hour",
            "power_tools_needed": False,
            "tools_needed": ["Screwdriver", "Sandpaper", "Ruler"],
            "materials_needed": ["1 Deep Wooden Dresser Drawer", "4 Low-profile castor wheels (1-2 inch)", "Screws", "Cabinet pull handle", "Peel-and-stick wallpaper"],
            "steps": [
                "Clean the interior of the old drawer thoroughly with mild soap and water; allow to dry.",
                "Sand away any splinters on the base and exterior corners.",
                "Line the bottom of the drawer with self-adhesive botanical peel-and-stick wallpaper for a gorgeous interior look.",
                "Flip drawer upside down and screw one low-profile castor wheel into each of the four sturdy corners.",
                "Install a sleek modern matte-black or brass handle on the side facing outward.",
                "Slide smoothly under your bed to neatly store extra bedsheets, shoes, books, or off-season winter coats!"
            ],
            "finishing_tip": "If your bed is low to the floor, choose fixed non-swivel 1-inch inline wheels to maximize clearance.",
            "landfill_diverted": "8 kg Wood",
            "co2_saved": "10 kg CO2"
        },
        {
            "name": "Boutique Shadow Box Wall Shelving & Display",
            "category": "Living Room & Study",
            "difficulty": "Beginner",
            "time_estimate": "45 Minutes",
            "power_tools_needed": False,
            "tools_needed": ["Screwdriver", "Drill or Picture Hanging Hardware", "Sandpaper"],
            "materials_needed": ["1 Vintage Shallow Drawer (with original brass pull intact)", "Decorative scrapbook paper or contact paper", "Heavy-duty sawtooth wall hangers"],
            "steps": [
                "Keep the original vintage handle or pull intact on the drawer front — it becomes a towel rod or necklace hanger!",
                "Sand the drawer rim edges and paint the exterior with soft warm cream chalk paint.",
                "Cut vintage floral or geometric pattern paper to fit the back interior panel and adhere smoothly with Mod Podge or glue.",
                "Optional: Insert a small wooden divider board inside to split the shadow box into two compartments.",
                "Secure two heavy-duty sawtooth picture hangers to the back top corners.",
                "Mount on the wall and display crystals, miniature succulents, perfumes, or framed art prints."
            ],
            "finishing_tip": "The drawer handle underneath is ideal for draping necklaces, hanging key rings, or displaying dry eucalyptus stems.",
            "landfill_diverted": "5 kg Wood",
            "co2_saved": "7 kg CO2"
        }
    ],
    "Old Wooden Ladder": [
        {
            "name": "Cozy Living Room Blanket & Quilt Display Ladder",
            "category": "Living Room",
            "difficulty": "Beginner (Zero Build)",
            "time_estimate": "30 Minutes",
            "power_tools_needed": False,
            "tools_needed": ["Fine Sandpaper (220-grit)", "Clean Rags"],
            "materials_needed": ["1 Old Wooden Stepladder or Painter's Extension Ladder", "Natural Beeswax wood finish or clear varnish", "Rubber anti-slip floor pads"],
            "steps": [
                "Wipe away old dust and dirt with a damp cloth.",
                "Use 220-grit sandpaper to smooth down any rough rungs so fine woolen and knit blankets will not snag.",
                "Apply natural beeswax polish across the rungs using a cotton cloth to nourish the old dry wood and bring out natural golden grain.",
                "Stick rubber anti-skid rubber feet pads to the bottom legs so the ladder will not slip on wooden or tile floors.",
                "Lean the ladder at a gentle 15-degree angle against your living room accent wall.",
                "Drape your favorite knitted throws, Turkish towels, and quilts gracefully over the rungs!"
            ],
            "finishing_tip": "Wrap warm-white LED fairy string lights down the ladder sides for ambient evening lighting.",
            "landfill_diverted": "12 kg Wood",
            "co2_saved": "14 kg CO2"
        }
    ],
    "Cable Spool / Drum": [
        {
            "name": "Round Library Coffee Table with Book Dividers",
            "category": "Living Room & Reading Nook",
            "difficulty": "Intermediate",
            "time_estimate": "2.5 Hours",
            "power_tools_needed": True,
            "tools_needed": ["Sander", "Drill", "Saw", "Wood Glue"],
            "materials_needed": ["1 Industrial Wooden Cable Spool", "4 Wooden Dowel rods (1-inch diameter)", "Dark walnut wood stain", "Clear satin lacquer"],
            "steps": [
                "Sand the round top, base, and center cylinder thoroughly to eliminate any industrial splinters.",
                "Measure the gap between the top round flange and bottom round flange.",
                "Cut 4 wooden dowel rods to this exact length and place them equidistant between the top and bottom circles, anchoring with wood glue and dowel screws.",
                "These dowel dividers create 4 organized quadrant book cubbies to store dozens of your favorite novels upright!",
                "Stain with deep warm walnut wood stain, wipe off excess, and allow 4 hours dry time.",
                "Seal with two coats of protective polyurethane lacquer."
            ],
            "finishing_tip": "The central core hole is the exact diameter for an umbrella pole or a sunken wine cooler bucket!",
            "landfill_diverted": "35 kg Wood",
            "co2_saved": "28 kg CO2"
        }
    ]
}


# =====================================================================
# 2. INDIVIDUAL AGENT CLASSES
# =====================================================================

class FashionAgent:
    """
    AGENT 1: Fashion Agent
    Specialist in textile upcycling, pattern manipulation, and fabric waste transformation.
    Employs deterministic heuristic rules to match fabric properties with viable designs.
    """
    def __init__(self):
        self.name = "Fashion Agent"
        self.role = "Textile Upcycling & Garment Transformation Specialist"
        self.icon = "👗"

    def get_supported_materials(self) -> List[str]:
        return list(FASHION_KNOWLEDGE_BASE.keys())

    def get_preset_projects(self, garment_type: str, no_sew_only: bool = False) -> List[Dict[str, Any]]:
        """Returns verified upcycling recipes from the knowledge base."""
        projects = FASHION_KNOWLEDGE_BASE.get(garment_type, [])
        if no_sew_only:
            projects = [p for p in projects if p.get("no_sew", False)]
        return projects

    def generate_custom_blueprint(self, garment_desc: str, condition: str, target_use: str, skill_level: str) -> Dict[str, Any]:
        """
        Rule-based heuristic engine for custom unlisted fabrics.
        Analyzes skill constraints and constructs a practical step-by-step DIY pattern.
        """
        cleaned_desc = garment_desc.strip().title() if garment_desc else "Vintage Fabric"
        
        reasoning_log = [
            f"1. Identified input material: '{cleaned_desc}' with condition: '{condition}'.",
            f"2. Assessed user constraint: Skill level = '{skill_level}' targeting '{target_use}'.",
            f"3. Rule selected: Applied fabric-edge protection protocol for {skill_level} crafting.",
            "4. Synthesized customized cutting ratios and structural reinforcement checkpoints."
        ]

        tech_specs = {
            "Beginner (No-Sew)": {
                "method": "Fabric Glue Bonding & Tying",
                "tools": ["Fabric Shears", "Heavy-Duty Fabric Glue / Hot Glue", "Iron for hem tape", "Ruler"],
                "cutting": "Cut clean geometric panels; avoid curved seams to keep fraying minimal."
            },
            "Intermediate (Hand Needle)": {
                "method": "Hand Basting & Decorative Blanket Stitching",
                "tools": ["Fabric Scissors", "Crewel Embroidery Needle", "Stranded Cotton Thread", "Pins"],
                "cutting": "Measure seams carefully with 1/2 inch hem allowances."
            },
            "Advanced (Sewing Machine)": {
                "method": "Reinforced French Seams & Structured Quilting",
                "tools": ["Sewing Machine", "Walking Foot", "Rotary Cutter & Mat", "Iron & Pressing Cloth"],
                "cutting": "Use rotary cutting with pattern weights for razor-sharp precision cuts."
            }
        }
        
        selected_tech = tech_specs.get(skill_level, tech_specs["Beginner (No-Sew)"])
        project_title = f"Upcycled {cleaned_desc} {target_use}"
        
        steps = [
            f"**Inspection & Prep:** Clean and press your {cleaned_desc.lower()}. Inspect for {condition.lower()}; mark flaws with chalk so they can be trimmed away or concealed.",
            f"**Template & Marking:** {selected_tech['cutting']} Use paper templates to trace out two matching panels sized for a modern {target_use.lower()}.",
            f"**Edge Treatment:** Treat raw fabric edges using {selected_tech['method']} to prevent unraveling during daily use.",
            f"**Assembly:** Join the main front and back bodies together with right sides touching, leaving an opening at the designated access point.",
            f"**Reinforcement & Accents:** Add reinforced corners and attach handles or closure straps made from remaining edge trims.",
            f"**Final Pressing:** Give the completed {target_use.lower()} a thorough steam press to set all bonds and give a store-bought crisp finish."
        ]
        
        return {
            "agent": self.name,
            "reasoning": reasoning_log,
            "title": project_title,
            "skill": skill_level,
            "tools": selected_tech["tools"],
            "steps": steps,
            "eco_highlight": f"Repurposing this {cleaned_desc} saves ~1,800L of water and keeps ~0.7kg of synthetic/cotton fibers out of local landfills."
        }

    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Parses freeform queries and matches against fashion expertise.
        """
        lower_q = query.lower()
        matched_material = "Old Denim Jeans"
        
        if "t-shirt" in lower_q or "tee" in lower_q or "jersey" in lower_q:
            matched_material = "Cotton T-Shirts"
        elif "saree" in lower_q or "silk" in lower_q or "scarf" in lower_q or "dupatta" in lower_q:
            matched_material = "Silk Saree / Vintage Scarf / Dupatta"
        elif "sweater" in lower_q or "wool" in lower_q or "knit" in lower_q:
            matched_material = "Woolen Sweaters"
        elif "flannel" in lower_q or "shirt" in lower_q or "plaid" in lower_q:
            matched_material = "Flannel & Plaid Shirts"
        elif "scrap" in lower_q or "remnant" in lower_q:
            matched_material = "Fabric Scraps & Remnants"

        is_no_sew = "no sew" in lower_q or "no-sew" in lower_q or "glue" in lower_q or "easy" in lower_q
        projects = self.get_preset_projects(matched_material, no_sew_only=is_no_sew)
        
        reasoning = [
            f"1. Parsed text for garment keywords: identified closest domain match '{matched_material}'.",
            f"2. Evaluated difficulty filter: 'No-Sew' requirement = {is_no_sew}.",
            f"3. Retrieved {len(projects)} validated upcycling blueprints from local textile matrix."
        ]
        
        return {
            "agent": self.name,
            "detected_material": matched_material,
            "reasoning": reasoning,
            "projects": projects
        }


class FurnitureAgent:
    """
    AGENT 2: Furniture Agent
    Specialist in furniture renovation, woodworking, and pallet revamps.
    Applies structural integrity, sanding, and non-toxic finishing heuristics.
    """
    def __init__(self):
        self.name = "Furniture Agent"
        self.role = "Furniture Renovation & Eco-Woodworking Specialist"
        self.icon = "🪑"

    def get_supported_furniture(self) -> List[str]:
        return list(FURNITURE_KNOWLEDGE_BASE.keys())

    def get_preset_blueprints(self, item_type: str, hand_tools_only: bool = False) -> List[Dict[str, Any]]:
        """Returns verified furniture restoration blueprints."""
        blueprints = FURNITURE_KNOWLEDGE_BASE.get(item_type, [])
        if hand_tools_only:
            blueprints = [b for b in blueprints if not b.get("power_tools_needed", False)]
        return blueprints

    def generate_custom_plan(self, item_desc: str, damage_condition: str, target_room: str, tool_level: str) -> Dict[str, Any]:
        """
        Rule-based heuristic engine for custom unlisted furniture pieces.
        Formulates cleaning, structural repair, sanding, and finishing sequences.
        """
        cleaned_item = item_desc.strip().title() if item_desc else "Vintage Wooden Furniture"
        
        reasoning_log = [
            f"1. Identified target piece: '{cleaned_item}' with defect '{damage_condition}'.",
            f"2. Verified spatial utility: Designing for placement in '{target_room}'.",
            f"3. Constraint applied: Available tools = '{tool_level}'.",
            "4. Selected surface prep, non-toxic primer, and protective wax sealing stages."
        ]

        if "Power Tools" in tool_level:
            prep_strategy = "Use an orbital sander (80 to 220 grit) for quick uniform wood stripping. Pre-drill all pilot holes."
            tools = ["Power Drill & Screws", "Random Orbital Sander", "Dust Mask & Ear Protection", "Clamps"]
        else:
            prep_strategy = "Use a manual cork sanding block with 120-grit paper. Clean joints and re-glue with wood adhesive."
            tools = ["Sanding Block (120 & 220 grit)", "Wood Glue", "Screwdriver", "Paint Brushes", "Rags"]
            
        project_title = f"{target_room} Revamped {cleaned_item}"
        
        steps = [
            f"**Structural Assessment & Cleaning:** Scrub down the {cleaned_item.lower()} with warm water and mild soap to remove grime. Address {damage_condition.lower()} by applying wood filler to deep gouges or re-securing loose joints with wood glue.",
            f"**Sanding Strategy:** {prep_strategy}",
            f"**Base Primer:** Apply a water-based stain-blocking primer coat to prevent old wood tannins from bleeding through.",
            f"**Color & Finish:** Apply two thin coats of low-VOC chalk paint (earthy sage green, warm cream, or charcoal). Allow 2 hours between coats.",
            f"**Protection Layer:** Buff in clear furniture finishing wax or apply clear water-based polyurethane matte coat to seal against moisture and everyday wear.",
            f"**Hardware Upgrade:** Install contemporary brushed brass or matte black handles to instantly modernize the piece for your {target_room.lower()}."
        ]
        
        return {
            "agent": self.name,
            "reasoning": reasoning_log,
            "title": project_title,
            "tools": tools,
            "steps": steps,
            "eco_highlight": f"Refurbishing an existing {cleaned_item} diverts ~15kg of bulky solid waste and saves the carbon equivalent of driving 70 kilometers."
        }

    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Parses freeform queries and matches against furniture expertise.
        """
        lower_q = query.lower()
        matched_item = "Wooden Shipping Pallet"
        
        if "chair" in lower_q or "stool" in lower_q:
            matched_item = "Broken or Wobbly Wooden Chair"
        elif "drawer" in lower_q or "dresser" in lower_q or "chest" in lower_q:
            matched_item = "Discarded Wooden Drawer"
        elif "ladder" in lower_q:
            matched_item = "Old Wooden Ladder"
        elif "spool" in lower_q or "drum" in lower_q or "cable" in lower_q:
            matched_item = "Cable Spool / Drum"

        hand_only = "hand tool" in lower_q or "no power" in lower_q or "manual" in lower_q or "simple" in lower_q
        blueprints = self.get_preset_blueprints(matched_item, hand_tools_only=hand_only)
        
        reasoning = [
            f"1. Parsed text for furniture keywords: matched closest category '{matched_item}'.",
            f"2. Evaluated tool constraint: 'Hand Tools Only' = {hand_only}.",
            f"3. Sourced {len(blueprints)} blueprints from local woodworking matrix."
        ]
        
        return {
            "agent": self.name,
            "detected_item": matched_item,
            "reasoning": reasoning,
            "blueprints": blueprints
        }


class BusinessAgent:
    """
    AGENT 3: Business Agent
    Specialist in sustainable micro-entrepreneurship, financial modeling,
    unit cost economics, and targeted social media marketing generation.
    """
    def __init__(self):
        self.name = "Business Agent"
        self.role = "Sustainable Commerce & Social Marketing Specialist"
        self.icon = "📊"

    def calculate_cost_and_profit(
        self,
        raw_material_cost: float,
        aux_material_cost: float,
        packaging_cost: float,
        labor_hours: float,
        hourly_rate: float,
        platform_fee_pct: float,
        target_margin_pct: float
    ) -> Dict[str, Any]:
        """
        Deterministic financial model calculating COGS, suggested retail, and profit metrics.
        """
        direct_material_cost = raw_material_cost + aux_material_cost + packaging_cost
        labor_cost = labor_hours * hourly_rate
        base_cogs = direct_material_cost + labor_cost  # Cost of Goods Sold
        
        combined_markup = (target_margin_pct + platform_fee_pct) / 100.0
        
        if combined_markup < 0.95:
            suggested_retail = base_cogs / (1.0 - combined_markup)
        else:
            suggested_retail = base_cogs * 2.0
            
        platform_fee_val = suggested_retail * (platform_fee_pct / 100.0)
        net_profit_val = suggested_retail - base_cogs - platform_fee_val
        actual_margin_pct = (net_profit_val / suggested_retail) * 100.0 if suggested_retail > 0 else 0.0
        wholesale_price = base_cogs * 1.35
        
        reasoning = [
            f"1. Total direct material outlay computed: {direct_material_cost:.2f}.",
            f"2. Labor valued at {labor_hours} hrs @ {hourly_rate}/hr = {labor_cost:.2f}.",
            f"3. Derived base Cost of Goods Sold (COGS): {base_cogs:.2f}.",
            f"4. Factored {platform_fee_pct}% marketplace commission and {target_margin_pct}% target margin.",
            f"5. Calculated viable retail floor price: {suggested_retail:.2f}."
        ]

        return {
            "agent": self.name,
            "reasoning": reasoning,
            "direct_material_cost": direct_material_cost,
            "labor_cost": labor_cost,
            "base_cogs": base_cogs,
            "suggested_retail": suggested_retail,
            "platform_fee_val": platform_fee_val,
            "net_profit_val": net_profit_val,
            "actual_margin_pct": actual_margin_pct,
            "wholesale_price": wholesale_price
        }

    def generate_marketing_caption(
        self,
        product_name: str,
        original_material: str,
        platform: str,
        tone: str,
        features: List[str],
        price_str: str = ""
    ) -> Dict[str, Any]:
        """
        Multi-platform social copy synthesizer with tailored hooks and curated hashtags.
        """
        hooks = {
            "Eco-Conscious & Sustainable": [
                f"What if your next favorite {product_name.lower()} once lived as {original_material.lower()}? 🌿",
                f"Trash to treasure isn't just a trend—it's the future. Meet our latest upcycled creation! ♻️",
                f"Zero waste. Infinite charm. Handcrafted exclusively from {original_material.lower()}. 🌱",
                f"Keeping beautiful materials out of landfills, one stitch at a time. 💚"
            ],
            "Trendy Gen-Z & Aesthetic": [
                f"Main character energy, but make it 100% sustainable ✨ Obsessed with this upcycled {product_name.lower()}!",
                f"Thrift flipped into pure perfection! You'll never believe this used to be {original_material.lower()} 😍",
                f"Proof that sustainable fashion is literally the coolest thing ever 💅 {product_name} is here!",
                f"One-of-a-kind piece alert! When it's gone, it's gone forever 🕊️"
            ],
            "Artisan & Handcrafted Story": [
                f"Every single seam tells a story of rebirth and mindful craftsmanship. 🧵",
                f"Slow made, carefully designed, and reimagined from {original_material.lower()}. 🎨",
                f"In a world of mass production, choose something created with patient hands and conscious purpose. 🪵",
                f"Transforming discarded {original_material.lower()} into timeless, functional art. 🌿"
            ],
            "Urgent & Sales-Driven": [
                f"⚡ DROP ALERT: Only 1 available in the entire world! Handcrafted {product_name} is now live.",
                f"Ready to level up your space sustainably? Snag this unique {product_name.lower()} before it's gone! 🛍️",
                f"Upcycled luxury that doesn't cost the earth. Handcrafted from {original_material.lower()}! 🏷️",
                f"Looking for that perfect conversation piece? DM to claim today! 📦"
            ]
        }
        
        selected_hook = random.choice(hooks.get(tone, hooks["Eco-Conscious & Sustainable"]))
        
        feat_text = "\n".join([f"  ✓ {f}" for f in features]) if features else "  ✓ 100% Repurposed & Upcycled\n  ✓ Handcrafted Zero-Waste Design\n  ✓ One-of-a-Kind Unique Piece"

        call_to_actions = {
            "Instagram Post / Reel": "💬 Drop a comment or DM to order! Link in bio for our full eco-catalog 📲",
            "Pinterest Pin Description": "📌 Save this pin to your Sustainable Living board & click through to view the full DIY guide!",
            "Facebook Marketplace / Groups": "📍 Available for local pickup or insured shipping. Send a private message to claim!",
            "Etsy / Website Product Listing": "✨ Add this one-of-a-kind handcrafted piece to your cart today. Ships in 100% plastic-free packaging."
        }
        
        cta = call_to_actions.get(platform, "🌿 DM to claim or learn more!")
        price_tag = f"\n💰 **Investment / Price:** {price_str}" if price_str else ""

        hashtag_pool = [
            "#UpcycledFashion", "#SustainableStyle", "#ThriftFlip", "#ZeroWasteFashion",
            "#SlowFashionMovement", "#RemadeDenim", "#EcoFriendlyLiving", "#CircularFashion",
            "#UpcyclingIdeas", "#HandmadeWithLove", "#ReworkedVintage", "#UpcycledFurniture",
            "#FurnitureFlip", "#SustainableHome", "#TrashToTreasure", "#ChalkPaintedFurniture",
            "#ZeroWasteHome", "#DIYHomeDecor", "#EcoInterior", "#CircularEconomy"
        ]
        
        tags = " ".join(hashtag_pool[:14])
        
        copy = f"""{selected_hook}

Say hello to our handcrafted **{product_name}**! 

✨ **The Story Behind The Piece:**
We rescued **{original_material}** and transformed it into a durable, functional, and stylish product designed for conscious everyday living.

🔍 **Key Details & Features:**
{feat_text}{price_tag}

{cta}

---
**Curated Hashtags:**
{tags}
"""
        return {
            "agent": self.name,
            "platform": platform,
            "tone": tone,
            "caption": copy
        }


# =====================================================================
# 3. AGENT COORDINATOR (INTENT CLASSIFIER & ROUTER)
# =====================================================================

class AgentCoordinator:
    """
    AGENT COORDINATOR
    Routes user requests to the appropriate specialized agent based on
    keyword heuristics and intent patterns.
    """
    def __init__(self):
        self.name = "Agent Coordinator"
        self.fashion_agent = FashionAgent()
        self.furniture_agent = FurnitureAgent()
        self.business_agent = BusinessAgent()

    def route_request(self, user_prompt: str) -> Dict[str, Any]:
        """
        Analyzes the user's natural language query using transparent keyword matching.
        Determines the most qualified agent and returns routing rationale.
        """
        prompt = user_prompt.lower()
        
        fashion_keywords = [
            "cloth", "clothes", "fabric", "textile", "denim", "jeans", "shirt", 
            "t-shirt", "tee", "saree", "dupatta", "scarf", "sweater", "wool", 
            "sew", "stitch", "tote", "bag", "dress", "patchwork", "flannel", "cotton"
        ]
        
        furniture_keywords = [
            "furniture", "wood", "wooden", "pallet", "chair", "table", "drawer", 
            "dresser", "ladder", "spool", "drum", "shelf", "bench", "sandpaper", 
            "varnish", "chalk paint", "drill", "saw", "cabinet", "stool", "trunk"
        ]
        
        business_keywords = [
            "cost", "price", "profit", "margin", "sell", "selling", "calculate", 
            "calculator", "caption", "marketing", "instagram", "pinterest", 
            "facebook", "etsy", "hashtag", "business", "cogs", "retail", "wage"
        ]

        fashion_score = sum(1 for kw in fashion_keywords if kw in prompt)
        furniture_score = sum(1 for kw in furniture_keywords if kw in prompt)
        business_score = sum(1 for kw in business_keywords if kw in prompt)

        scores = {
            "Fashion Agent": fashion_score,
            "Furniture Agent": furniture_score,
            "Business Agent": business_score
        }

        best_agent = max(scores, key=scores.get)
        max_score = scores[best_agent]

        if max_score == 0:
            # Fallback based on default general context
            best_agent = "Fashion Agent"
            confidence = "Low (Default Assignment)"
            reason = "No domain-specific keywords matched. Defaulted to the Fashion Agent."
        else:
            confidence = "High" if max_score >= 2 else "Medium"
            reason = f"Detected {max_score} matching keyword(s) relevant to {best_agent} domain."

        return {
            "coordinator": self.name,
            "selected_agent": best_agent,
            "confidence": confidence,
            "keyword_scores": scores,
            "routing_reason": reason
        }

    def execute_coordinated_task(self, user_prompt: str) -> Dict[str, Any]:
        """
        Coordinates the execution: routes to the agent and gathers the response.
        """
        routing_info = self.route_request(user_prompt)
        target_agent = routing_info["selected_agent"]
        
        if target_agent == "Fashion Agent":
            agent_result = self.fashion_agent.process_query(user_prompt)
        elif target_agent == "Furniture Agent":
            agent_result = self.furniture_agent.process_query(user_prompt)
        else:
            # Business Agent default marketing/costing template
            agent_result = self.business_agent.generate_marketing_caption(
                product_name="Upcycled Craft Item",
                original_material="Repurposed Recycled Material",
                platform="Instagram Post / Reel",
                tone="Eco-Conscious & Sustainable",
                features=["Zero-Waste", "Handcrafted", "Eco-Friendly"]
            )

        return {
            "routing": routing_info,
            "agent_output": agent_result
        }


# =====================================================================
# 4. AI PHOTO-TO-DESIGN STUDIO ENGINE
# =====================================================================

class PhotoDesignStudioEngine:
    """
    ENGINE 4: AI Photo-to-Design Studio Engine
    Generates tailored, multi-concept upcycling blueprints based on uploaded photos,
    item category (Clothes vs Furniture), and selected design aesthetics.
    Operates transparently without requiring external paid APIs.
    """
    def __init__(self):
        self.name = "Photo-to-Design Studio Engine"
        self.styles = ["Modern", "Traditional", "Minimalist", "Luxury", "Eco-Friendly"]
        self.categories = ["Old Clothes / Fabric Waste", "Old Furniture"]
        self._init_concept_database()

    def _init_concept_database(self):
        """Initializes the rich concept matrices across categories and design styles."""
        self.database = {
            "Old Clothes / Fabric Waste": {
                "Modern": [
                    {
                        "id": "c_mod_1",
                        "title": "Geometric Colorblock Crossbody Sling",
                        "description": "Repurposes garment panels into an asymmetrical, structured streetwear sling. Features geometric dual-tone paneling, an exposed waterproof nylon zipper, and an ergonomic webbing carry strap.",
                        "materials": ["Outer fabric from uploaded garment", "1/2 meter contrast cotton lining", "12-inch waterproof zipper", "1.5-inch nylon webbing strap (1.2m)", "2 Black metal D-rings & slider"],
                        "difficulty": "Intermediate",
                        "cost_inr": 280,
                        "time_estimate": "2 Hours",
                        "steps": [
                            "Dismantle garment along primary seams and steam-press flat into clean fabric sheets.",
                            "Draft an angular, geometric trapezoid template (10\" x 7\" x 3\") on cardstock.",
                            "Cut 3 contrasting colorblock geometric facets for the front face; join with reinforced 1/4\" seams.",
                            "Install the top waterproof zipper between the outer shell and inner cotton lining.",
                            "Box the lower corners to create a 3-inch depth, insert webbing tabs with D-rings, and stitch closed."
                        ],
                        "features": ["Waterproof Zipper Accent", "Asymmetrical Colorblock", "Interior Key Tether", "Ergonomic Body Fit"],
                        "palette": ["#174D3B", "#2A2A2A", "#E0E0E0", "#C8963E"],
                        "symbol": "🎒",
                        "eco_impact": "Diverts ~0.8 kg of garment fabric and saves approx. 1,900 liters of virtual water."
                    },
                    {
                        "id": "c_mod_2",
                        "title": "Structured Tech Organizer & Laptop Sleeve",
                        "description": "Transforms thick fabrics or flannel into a modern padded tech folio. Features an internal shock-absorbing quilt grid, elastic peripheral cable loops, and magnetic matte-black clasp.",
                        "materials": ["Garment fabric outer shell", "High-density 4mm neoprene or foam batting", "Soft micro-fleece lining scrap", "2 Magnetic snap fasteners", "1-inch elastic band"],
                        "difficulty": "Intermediate",
                        "cost_inr": 340,
                        "time_estimate": "2.5 Hours",
                        "steps": [
                            "Measure your laptop or tablet, adding 1.5 inches of ease on length and width.",
                            "Cut outer garment panels, inner foam padding, and scratch-free fleece lining.",
                            "Quilt the outer fabric to the protective foam backing using a modern 1-inch diagonal diamond grid.",
                            "Stitch elastic segment loops onto the front interior pocket for stylus pens, charger cables, and USB drives.",
                            "Assemble sleeve envelope with right sides facing, turn right side out, and mount magnetic snap closures."
                        ],
                        "features": ["Shock-Absorbing Quilted Grid", "Quick-Access Charger Pocket", "Concealed Magnetic Fasteners", "Drop-Proof Reinforced Edges"],
                        "palette": ["#1C2A22", "#383838", "#69DB9B", "#F5F5F5"],
                        "symbol": "💻",
                        "eco_impact": "Prevents 1.1 kg of textile scrap from entering municipal landfills."
                    },
                    {
                        "id": "c_mod_3",
                        "title": "Asymmetric Patchwork Kimono Streetwear Vest",
                        "description": "Converts old shirts or denims into a modern streetwear layering piece. Features clean angular lapels, raw-edged deconstructed hem accents, and deep functional cargo pockets.",
                        "materials": ["1-2 Old clothing items", "Matching polyester thread", "Fusible lightweight interfacing for lapel support"],
                        "difficulty": "Intermediate",
                        "cost_inr": 190,
                        "time_estimate": "2 Hours",
                        "steps": [
                            "Slice open the sleeve and side seams of your primary garment to harvest back and front panels.",
                            "Construct clean straight kimono front panels, interfacing the lapel for crisp vertical posture.",
                            "Splice in contrast patches from secondary fabric along the lower quarter for an architectural finish.",
                            "Stitch side seams leaving 12-inch open side vents for relaxed, modern drape.",
                            "Finish armholes with clean bias binding and leave bottom hem subtly frayed with a stabilizing stitch."
                        ],
                        "features": ["Relaxed Kimono Silhouette", "Architectural Lapel Line", "Dual Concealed Pockets", "Breathable Side Slits"],
                        "palette": ["#174D3B", "#4A7A5B", "#242424", "#FFFFFF"],
                        "symbol": "🥋",
                        "eco_impact": "Saves up to 2,400 liters of water compared to purchasing a new commercial garment."
                    },
                    {
                        "id": "c_mod_4",
                        "title": "Origami Foldable Fabric Desktop Planter Cover",
                        "description": "Folds heavy fabric into a sharp geometric pot cover for indoor succulents. Features a water-resistant sealed internal drop tray and modern faceted origami corners.",
                        "materials": ["Heavy garment fabric (denim, twill, or canvas)", "Clear plastic takeaway container / recycled bottle base", "Heavy-duty fabric glue or edge topstitch"],
                        "difficulty": "Beginner",
                        "cost_inr": 80,
                        "time_estimate": "45 Minutes",
                        "steps": [
                            "Cut a 12\" x 12\" square from the cleanest section of your uploaded garment.",
                            "Mark 3-inch corner squares and fold along diagonal axes to form 3D origami facet corners.",
                            "Press folds sharply with a hot iron to impart crisp geometric memory into the fabric weave.",
                            "Topstitch or glue the folded triangular ears flat against the outer sides for an architectural motif.",
                            "Insert a recycled plastic water saucer inside the base to catch plant drainage moisture."
                        ],
                        "features": ["Faceted Origami Architecture", "Zero Plastic Waste Drainage", "Compact Desktop Footprint", "Reversible Dual-Texture Look"],
                        "palette": ["#2D4D38", "#A0A0A0", "#FFFFFF", "#FFD278"],
                        "symbol": "🪴",
                        "eco_impact": "Diverts 0.3 kg of textile off-cuts and repurposes a single-use plastic container."
                    }
                ],
                "Traditional": [
                    {
                        "id": "c_trad_1",
                        "title": "Heritage Kantha Quilted Accent Cushion",
                        "description": "Celebrates age-old Indian Kantha craftsmanship by layering vintage cotton or silk fabrics with dense, meditative running stitches and contrasting piped borders.",
                        "materials": ["Uploaded fabric outer face", "Old cotton bedsheet or muslin inner layers", "Anchor/DMC stranded embroidery floss (contrast color)", "16x16 inch cotton cushion insert"],
                        "difficulty": "Beginner",
                        "cost_inr": 180,
                        "time_estimate": "2.5 Hours",
                        "steps": [
                            "Cut three matching 17\" x 17\" squares: outer garment face, middle muslin padding, and base layer.",
                            "Layer and baste the 3 plies together with temporary basting stitches to prevent shifting.",
                            "Using 4 strands of bright contrasting floss, sew continuous parallel rows of hand Kantha running stitches across the face.",
                            "Create an envelope-back closure using the rear garment fabric for easy cushion washing.",
                            "Stitch front and back together with right sides facing, turn inside out, and insert your pillow."
                        ],
                        "features": ["Handcrafted Kantha Running Stitch", "Heirloom Textile Texture", "Zero-Zipper Envelope Back", "Soft Breathable Natural Cotton"],
                        "palette": ["#8C2D19", "#FFD278", "#174D3B", "#FAF8F0"],
                        "symbol": "🪡",
                        "eco_impact": "Preserves indigenous artisan heritage while keeping 0.9 kg of cotton out of landfills."
                    },
                    {
                        "id": "c_trad_2",
                        "title": "Embroidered Royal Potli Bag with Golden Tassels",
                        "description": "Repurposes ornate saree sections, brocade, or embroidered fabric into an Indian festive potli bag with braided golden drawstrings and brass ghungroo beads.",
                        "materials": ["Brocade or embellished garment scrap", "Raw silk or satin lining", "1.5 meters golden braided dori (cord)", "4 Brass bell tassels / latkans"],
                        "difficulty": "Intermediate",
                        "cost_inr": 220,
                        "time_estimate": "1.5 Hours",
                        "steps": [
                            "Cut two 9\" x 11\" rounded-bottom pouch pieces from the uploaded fabric and two from lining.",
                            "Sew outer panels together, leaving top 2 inches unstitched for the drawstring eyelets.",
                            "Stitch inner lining and insert inside outer bag; sew closed along the top rim.",
                            "Create two parallel stitch lines 1.5 inches below the rim to form a hollow horizontal drawstring channel.",
                            "Thread two golden cords in opposite directions; attach brass latkans and tie firmly."
                        ],
                        "features": ["Festive Round-Bottom Pouch", "Dual-Pull Golden Cord", "Tinkling Brass Latkan Accents", "Lustrous Inner Satin Lining"],
                        "palette": ["#B33927", "#E0A938", "#174D3B", "#FDFBF7"],
                        "symbol": "👝",
                        "eco_impact": "Breathes new life into delicate traditional textiles without throwing away gold zari borders."
                    },
                    {
                        "id": "c_trad_3",
                        "title": "Bohemian Patchwork Toran / Doorway Valance",
                        "description": "Constructs an auspicious Indian doorway hanging (Toran) from patterned fabric scraps, featuring triangle pennants, miniature mirrors, and lucky jute loops.",
                        "materials": ["Assorted fabric scraps from uploaded item", "1 meter sturdy woven cotton base band", "Small craft mirror patches or sequins", "Cotton thread & jute cord"],
                        "difficulty": "Beginner",
                        "cost_inr": 140,
                        "time_estimate": "1.5 Hours",
                        "steps": [
                            "Cut 7 or 9 matching fabric triangles (5\" wide by 6\" tall) from your assorted garment scraps.",
                            "Sew each triangle right-sides-together, trim corners, turn right side out, and press flat.",
                            "Adhere or hand-stitch small craft mirrors or decorative sequins to the center of each pennant.",
                            "Sandwich the top edges of the triangles inside a folded 3-foot long header band.",
                            "Topstitch the header band shut and add two sturdy jute loops at the outer ends for hanging."
                        ],
                        "features": ["Festive Doorway Auspicious Charm", "Glinting Mirror-Work Embellishments", "Bespoke Triangle Pennants", "Zero-Waste Scrap Assembly"],
                        "palette": ["#C04020", "#2E6B4A", "#FFCC40", "#FAF8F0"],
                        "symbol": "🚩",
                        "eco_impact": "Utilizes tiny fabric scraps as small as 4 inches that would otherwise be discarded."
                    },
                    {
                        "id": "c_trad_4",
                        "title": "Heritage Dining Table Runner with Zari Border",
                        "description": "Frames the rich central weave of your uploaded garment with sturdy duck cotton and preserved traditional border trims for a dining centerpiece.",
                        "materials": ["Uploaded garment main body", "Zari or embroidered border trim", "Heavy natural cotton canvas for backing (14\" x 48\")", "Matching thread"],
                        "difficulty": "Beginner",
                        "cost_inr": 250,
                        "time_estimate": "1.5 Hours",
                        "steps": [
                            "Cut a continuous 12\" x 46\" center rectangle from your cleanest garment section.",
                            "Cut 2-inch wide border strips from the garment's hem or contrasting trim.",
                            "Frame the central panel with the border strips using mitered 45-degree corner joints.",
                            "Pin the assembled runner face down onto the canvas backing fabric.",
                            "Stitch all around leaving a 4-inch turning gap; turn right side out, press, and topstitch the perimeter."
                        ],
                        "features": ["Mitered Tailored Corners", "Heavyweight Anti-Slip Canvas Back", "Heat-Resistant Center Panel", "Festive Dining Statement Piece"],
                        "palette": ["#8C2D19", "#174D3B", "#D4A34E", "#2A2A2A"],
                        "symbol": "🍽️",
                        "eco_impact": "Diverts 1.2 kg of long-format textile waste and saves ₹1,500+ compared to store runners."
                    }
                ],
                "Minimalist": [
                    {
                        "id": "c_min_1",
                        "title": "Zen Seamless Daily Market Shopper",
                        "description": "Engineered from a single piece of fabric with clean French seams and no visible hardware. Ultra-lightweight, washable, and folds down to the size of a coin purse.",
                        "materials": ["Uploaded garment (t-shirt, shirt, or bedsheet)", "Durable cotton thread"],
                        "difficulty": "Beginner",
                        "cost_inr": 60,
                        "time_estimate": "45 Minutes",
                        "steps": [
                            "Cut a continuous rectangular panel (16\" x 36\") and two handle strips (3\" x 24\").",
                            "Fold handles lengthwise, press, stitch, and topstitch for minimalist clean edges.",
                            "Fold main body in half right-sides-out and stitch side seams with an ultra-narrow 1/8\" seam.",
                            "Turn inside out and sew a 1/4\" seam to encase raw edges in clean, fray-free French seams.",
                            "Fold top hem over twice, pin handles underneath, and topstitch securely with a clean box stitch."
                        ],
                        "features": ["Enclosed French Seams (Zero Fraying)", "Foldable Pocket Footprint", "Single-Material Purity", "15kg Load Tested"],
                        "palette": ["#E5DFD5", "#383838", "#174D3B", "#FAF8F0"],
                        "symbol": "🛍️",
                        "eco_impact": "Eliminates hundreds of single-use plastic grocery bags over its lifetime."
                    },
                    {
                        "id": "c_min_2",
                        "title": "Monochrome Hexagon Mug Rug Set (4 Pieces)",
                        "description": "Minimalist geometric drink coasters made with precise English paper pieced hexagons in muted neutral tones. Protects wooden surfaces while elevating desk setups.",
                        "materials": ["Garment fabric off-cuts", "Felt or cork scrap for non-slip backing", "Cardstock hexagon template (2.5-inch)", "Hand basting needle & thread"],
                        "difficulty": "Beginner",
                        "cost_inr": 90,
                        "time_estimate": "1 Hour",
                        "steps": [
                            "Trace and cut 28 small fabric hexagons using a cardboard template.",
                            "Fold fabric edges over cardboard templates and baste with wide temporary stitches.",
                            "Hand-sew 7 hexagons together per coaster (1 in center, 6 surrounding) using fine whipstitches.",
                            "Gently remove cardstock templates and press hexagons completely flat with steam.",
                            "Adhere onto round cork discs or topstitch onto natural felt backing circles."
                        ],
                        "features": ["Geometric Hexagonal Symmetry", "Absorbent Heat-Resistant Cotton", "Non-Scratch Backing", "Desk Aesthetic Essential"],
                        "palette": ["#2A2A2A", "#686868", "#A8A8A8", "#FAF8F0"],
                        "symbol": "☕",
                        "eco_impact": "Repurposes tiny garment trimmings as small as 2.5 inches."
                    },
                    {
                        "id": "c_min_3",
                        "title": "Vertical Clean-Line Wall Hanging Organizer",
                        "description": "A quiet, architectural wall pocket for reading glasses, journals, and phones. Combines raw unbleached canvas tones with a slender birch wood dowel.",
                        "materials": ["Garment fabric strip (8\" x 30\")", "Slender 10-inch wooden dowel or sanded twig", "Natural linen twine"],
                        "difficulty": "Beginner",
                        "cost_inr": 110,
                        "time_estimate": "1 Hour",
                        "steps": [
                            "Hem the long outer edges of the 8\" wide fabric strip with clean 1/4\" rolled hems.",
                            "Fold the bottom edge up in accordion tiers to create 3 tiered, graduated slip pockets.",
                            "Stitch vertical dividers down the pockets with clean, minimalist straight lines.",
                            "Fold top 1.5 inches backward and stitch to form a horizontal dowel sleeve.",
                            "Slide wooden dowel through sleeve and tie natural linen twine for subtle wall mounting."
                        ],
                        "features": ["Tiered Graduated Pockets", "Zero Hardware Aesthetic", "Slimline Vertical Profile", "Natural Birch Wood Accent"],
                        "palette": ["#DCD6CD", "#1E1E1E", "#4A7A5B", "#FFFFFF"],
                        "symbol": "📜",
                        "eco_impact": "Organizes bedside or study clutter without buying petroleum-based plastic storage."
                    },
                    {
                        "id": "c_min_4",
                        "title": "Minimalist Roll-Up Cord & Stationery Wrap",
                        "description": "A disciplined, portable organizer for cables, chargers, fountain pens, or crochet hooks. Rolls into a neat compact bundle secured by an integrated fabric tie.",
                        "materials": ["Garment panel (10\" x 16\")", "Inner contrast lining piece", "1-inch elastic strip (12 inches)", "Matching thread"],
                        "difficulty": "Beginner",
                        "cost_inr": 85,
                        "time_estimate": "45 Minutes",
                        "steps": [
                            "Layer outer garment fabric and inner lining with right sides touching.",
                            "Sandwich a 16-inch fabric tie ribbon inside one side seam; stitch perimeter leaving turning gap.",
                            "Turn right side out and press flat; topstitch 1/8\" around the perimeter.",
                            "Pin elastic band horizontally across the inner face and sew vertical dividers every 1.5 inches.",
                            "Roll up with cables and pens securely slotted, wrap tie around twice, and tuck neatly."
                        ],
                        "features": ["Tangle-Free Cable Slots", "Pocket-Sized Travel Companion", "Integrated Tie Closure", "Washable Textile Construction"],
                        "palette": ["#174D3B", "#383838", "#E0E0E0", "#FAF8F0"],
                        "symbol": "🖋️",
                        "eco_impact": "Replaces plastic zipper pouches with a lifetime durable, washable textile solution."
                    }
                ],
                "Luxury": [
                    {
                        "id": "c_lux_1",
                        "title": "Velvet & Silk Evening Envelope Clutch",
                        "description": "An exquisite, high-end evening clutch crafted from rich garment silk or velvet. Reinforced with stiff interlining, magnetic gold hardware, and a concealed chain strap.",
                        "materials": ["Silk, brocade or velvet from uploaded garment", "Heavy Peltex / Buckram stiffener sheet", "Gold magnetic snap lock", "Gold-tone 40-inch curb chain", "Satin scrap for interior"],
                        "difficulty": "Intermediate",
                        "cost_inr": 480,
                        "time_estimate": "3 Hours",
                        "steps": [
                            "Cut envelope chassis template (11\" wide x 16\" long) with a triangular flap.",
                            "Fuse heavy buckram stiffener to outer garment fabric using high heat and pressing cloth.",
                            "Mount the male side of the gold magnetic clasp onto the triangular flap point.",
                            "Install interior card slots and lipstick pocket onto the inner satin lining.",
                            "Assemble outer and lining, install hidden brass chain loops, and topstitch with metallic thread."
                        ],
                        "features": ["Structured Buckram Core", "Gold-Tone Magnetic Clasp", "Concealed Evening Chain", "Interior Velvet Slip Pocket"],
                        "palette": ["#174D3B", "#D4A34E", "#1E1E1E", "#FFFFFF"],
                        "symbol": "👛",
                        "eco_impact": "Creates a designer accessory valued at ₹2,500+ using discarded luxury textiles."
                    },
                    {
                        "id": "c_lux_2",
                        "title": "Luxe Mulberry Silk Eye Mask & Scrunchie Set",
                        "description": "Transforms silk sarees, scarves, or satin garments into an ultra-gentle beauty sleep duo. Minimizes hair friction and shields delicate facial skin from creasing.",
                        "materials": ["Silk or satin fabric (at least 15\" x 20\")", "Soft organic cotton batting for mask padding", "1/2 inch elastic band (16 inches total)", "Matching fine silk thread"],
                        "difficulty": "Beginner",
                        "cost_inr": 210,
                        "time_estimate": "1 Hour",
                        "steps": [
                            "Print ergonomic curved eye mask contour stencil; cut 2 silk layers and 1 batting layer.",
                            "Sew a ruched silk tube around an 11-inch elastic strip to create the gentle head strap.",
                            "Sandwich strap ends between the mask front and back layers; stitch perimeter with fine needle.",
                            "Turn eye mask right-side out through a 1-inch nose gap and close with invisible ladder stitch.",
                            "Cut a 4\" x 18\" silk strip, insert 6-inch elastic, and stitch closed for the matching hair scrunchie."
                        ],
                        "features": ["100% Friction-Free Silk", "Lightweight Cloud-Soft Padding", "Anti-Crease Elastic Headband", "Boutique Gift Box Ready"],
                        "palette": ["#C5A880", "#174D3B", "#FAF8F0", "#3E2723"],
                        "symbol": "✨",
                        "eco_impact": "Diverts delicate silk off-cuts that commercial mills routinely incinerate."
                    },
                    {
                        "id": "c_lux_3",
                        "title": "Boutique Quilted Tablet Folio with Brass Zipper",
                        "description": "A bespoke artisanal portfolio case. Features dense horizontal channel quilting, an antique brass zipper with leather pull, and a custom monogram patch.",
                        "materials": ["Heavy garment textile", "High-density foam padding (3mm)", "Antiqued brass YKK metal zipper (14-inch)", "Scrap leather pull tab"],
                        "difficulty": "Intermediate",
                        "cost_inr": 380,
                        "time_estimate": "2.5 Hours",
                        "steps": [
                            "Cut exterior and lining panels 1.5 inches larger than your target tablet dimensions.",
                            "Quilt exterior fabric onto dense padding with uniform 0.75-inch horizontal channeled lines.",
                            "Baste metal brass zipper between exterior and lining with teeth facing inward.",
                            "Stitch zipper tape with zipper foot; open zipper halfway before sewing perimeter shut.",
                            "Turn through turning hole, press edges crisp, and thread leather pull onto brass slider."
                        ],
                        "features": ["Precision Channel Quilting", "Antiqued Brass Hardware", "Leather Pull Accents", "Padded Drop-Proof Barrier"],
                        "palette": ["#1F3A2B", "#C8963E", "#2A2A2A", "#FAF8F0"],
                        "symbol": "💼",
                        "eco_impact": "Produces luxury protective tech wear using 100% recycled structural fabrics."
                    },
                    {
                        "id": "c_lux_4",
                        "title": "Tufted French Mattress Bolster Cushion",
                        "description": "A cylindrical European reading bolster with hand-sewn corded edge welting and velvet tufted button centers. Elevates sofas and bedscapes into luxury hotel suites.",
                        "materials": ["Uploaded garment fabric (velvet, denim, or heavy linen)", "Thick piping cord (2 meters)", "2 Covered button blanks", "Firm polyfill or shredded cotton scraps"],
                        "difficulty": "Intermediate",
                        "cost_inr": 320,
                        "time_estimate": "2.5 Hours",
                        "steps": [
                            "Cut a cylinder body rectangle (24\" x 20\") and two round side end caps (8-inch diameter).",
                            "Wrap piping cord in fabric bias tape and stitch around both round end circles.",
                            "Join cylinder seam and attach both corded circular end caps.",
                            "Firmly pack bolster interior with clean shredded textile scraps and polyfill batting.",
                            "Stitch opening closed; use long doll needle to thread through bolster and tie two tufted buttons tight."
                        ],
                        "features": ["French Corded Welting", "Center Tufted Covered Buttons", "High-Density Ergonomic Support", "Hotel Luxury Finish"],
                        "palette": ["#174D3B", "#4A7A5B", "#FFD278", "#1E1E1E"],
                        "symbol": "🛋️",
                        "eco_impact": "Consumes over 1.5 kg of fabric waste as inner firm core stuffing."
                    }
                ],
                "Eco-Friendly": [
                    {
                        "id": "c_eco_1",
                        "title": "Zero-Waste Braided Macramé Plant Hanger",
                        "description": "Transforms cotton shirts or stretchy jerseys into strong seamless t-shirt yarn, knotted into a bohemian hanging cradle for air-purifying indoor plants.",
                        "materials": ["1-2 Cotton t-shirts or jersey garments", "1 Wooden curtain ring or metal key loop (2-inch)", "Scissors & measuring tape"],
                        "difficulty": "Beginner",
                        "cost_inr": 40,
                        "time_estimate": "35 Minutes",
                        "steps": [
                            "Cut the body of your garment horizontally into continuous 1-inch wide strips.",
                            "Gently pull and stretch the strips; raw cotton edges will curl inward into seamless durable yarn.",
                            "Cut 8 strands of yarn (each 3.5 feet long); thread through ring and secure with gathering knot.",
                            "Group strands into 4 pairs; tie simple knots 12 inches below the ring.",
                            "Alternate strands between adjacent pairs and tie knots 3 inches lower to form a diamond net cradle; tie bottom master knot."
                        ],
                        "features": ["100% Upcycled T-Shirt Yarn", "Zero Hardware / No Sewing Needed", "Holds Up to 8-inch Ceramic Pots", "Washable & Biodegradable"],
                        "palette": ["#2D5A27", "#EBF4EE", "#D4A34E", "#FAF8F0"],
                        "symbol": "🪴",
                        "eco_impact": "Conserves 2,700 liters of water by repurposing cotton without chemical re-dyeing."
                    },
                    {
                        "id": "c_eco_2",
                        "title": "Organic Beeswax Reusable Food Wrap Set (3 Pack)",
                        "description": "Infuses clean cotton scraps with pure organic beeswax and coconut oil. Creates reusable, antibacterial kitchen covers that replace single-use plastic cling wrap.",
                        "materials": ["100% Cotton garment scraps (cut into 8\", 10\", 12\" squares)", "50g Natural beeswax pellets", "1/2 tsp Jojoba or organic coconut oil", "Parchment baking paper & iron"],
                        "difficulty": "Beginner",
                        "cost_inr": 160,
                        "time_estimate": "30 Minutes",
                        "steps": [
                            "Trim fabric squares with pinking shears to permanently eliminate raw thread fraying.",
                            "Place fabric square onto parchment paper; evenly sprinkle beeswax pellets and drops of oil.",
                            "Cover with a second sheet of parchment paper.",
                            "Glide a hot dry iron over the paper sandwich until beeswax melts completely into fabric fibers.",
                            "Peel paper off while warm and wave wrap in air for 30 seconds to cure into pliable wrap."
                        ],
                        "features": ["Replaces Plastic Cling Wrap", "Naturally Antibacterial", "Washable in Cool Water", "Lasts 120+ Kitchen Uses"],
                        "palette": ["#E8C15A", "#174D3B", "#FAF8F0", "#3E2723"],
                        "symbol": "🐝",
                        "eco_impact": "Prevents over 300 meters of disposable plastic cling film from entering oceans."
                    },
                    {
                        "id": "c_eco_3",
                        "title": "Braided Heavy-Duty Dog Tug & Chew Rope",
                        "description": "Tightly braids thick denim and cotton strips into an indestructible, non-toxic chew toy for pets. Safe, teeth-cleaning, and completely machine washable.",
                        "materials": ["Old denim or cotton t-shirt strips", "Fabric shears"],
                        "difficulty": "Beginner",
                        "cost_inr": 30,
                        "time_estimate": "20 Minutes",
                        "steps": [
                            "Cut 6 long strips of fabric (roughly 3 inches wide and 3 feet long).",
                            "Gather all 6 strands together and tie a massive overhand knot at one end.",
                            "Divide into three pairs of 2 strands and braid tightly with firm tension down to 4 inches from end.",
                            "Tie a matching tight double knot to lock the braid securely.",
                            "Snip fringe ends evenly. Optional: Soak in water and freeze for soothing teething puppies!"
                        ],
                        "features": ["Non-Toxic & Chemical-Free", "Dental Cleaning Cotton Weave", "100% Machine Washable", "Freezes for Summer Chewing"],
                        "palette": ["#174D3B", "#4A7A5B", "#E0E0E0", "#FAF8F0"],
                        "symbol": "🐕",
                        "eco_impact": "Zero purchase cost, zero synthetic plastics, and fully divertable."
                    },
                    {
                        "id": "c_eco_4",
                        "title": "Neem & Lavender Wardrobe Moth Sachets (4 Pack)",
                        "description": "Breathable linen or cotton pouches filled with dried lavender, neem leaves, and camphor chips. Protects woolens naturally without hazardous chemical mothballs.",
                        "materials": ["Cotton/linen scraps (5\" x 5\" squares)", "Dried lavender flowers or neem leaves", "Camphor pieces or cedar chips", "Jute twine"],
                        "difficulty": "Beginner",
                        "cost_inr": 75,
                        "time_estimate": "25 Minutes",
                        "steps": [
                            "Cut eight 5\" x 5\" squares using zigzag pinking shears.",
                            "Stitch or glue three edges together to form small open-mouth herbal pouches.",
                            "Fill 3/4 full with natural dried botanicals, neem leaves, and camphor granules.",
                            "Insert a 6-inch loop of natural jute string into the top opening.",
                            "Stitch fourth edge shut; hang in wardrobes, tuck in shoe racks, or place in suitcase storage."
                        ],
                        "features": ["All-Natural Chemical-Free Moth Repellent", "Aromatherapy Freshness", "Breathable Biodegradable Fiber", "Refillable Design"],
                        "palette": ["#6A4E8C", "#174D3B", "#FAF8F0", "#D4A34E"],
                        "symbol": "🌿",
                        "eco_impact": "Replaces toxic petrochemical mothballs with 100% organic waste materials."
                    }
                ]
            },
            "Old Furniture": {
                "Modern": [
                    {
                        "id": "f_mod_1",
                        "title": "Industrial Hairpin-Leg Coffee Table",
                        "description": "Repurposes pallet slats or a reclaimed tabletop onto sleek matte black hairpin legs. Sanded to a silky woodgrain finish and sealed with water-based polyurethane.",
                        "materials": ["Sanded pallet top or reclaimed wooden surface", "4 Matte black steel hairpin legs (16-inch, 3-rod)", "16 Heavy wood screws", "Walnut wood stain & clear satin sealant"],
                        "difficulty": "Beginner",
                        "cost_inr": 680,
                        "time_estimate": "2 Hours",
                        "steps": [
                            "Inspect wood: sand top surface progressively from 80-grit to 220-grit until velvety smooth.",
                            "Wipe wood dust clean with a tack cloth; apply rich walnut stain with a cotton rag.",
                            "Let stain cure 2 hours, then apply two coats of clear satin water-based sealer.",
                            "Flip tabletop over; measure 2 inches in from each corner to mark leg brackets.",
                            "Pre-drill 1/8\" pilot holes and securely drive wood screws into all four hairpin leg plates."
                        ],
                        "features": ["Solid Industrial Hairpin Stance", "Silky Sanded Walnut Grain", "Spill-Resistant Satin Seal", "Modern Apartment Aesthetic"],
                        "palette": ["#174D3B", "#1E1E1E", "#C8963E", "#FAF8F0"],
                        "symbol": "🛋️",
                        "eco_impact": "Saves 18 kg of solid timber from being incinerated or dumped in landfills."
                    },
                    {
                        "id": "f_mod_2",
                        "title": "Floating Geometric Slatted Wall Shelf",
                        "description": "Transforms broken chair spindles or disassembled drawer slats into an architectural floating box shelf with hidden mounting hardware.",
                        "materials": ["Disassembled wooden slats or drawer box", "Wood glue (PVA)", "Brushed brass corner L-brackets", "2 Keyhole wall hangers"],
                        "difficulty": "Intermediate",
                        "cost_inr": 340,
                        "time_estimate": "2.5 Hours",
                        "steps": [
                            "Clean and square up 4 wooden boards to identical dimensions (e.g. 14\" x 6\").",
                            "Sand all facets thoroughly with 180-grit paper; paint exterior in matte charcoal.",
                            "Join boards into an open geometric box using wood glue and internal brass corner brackets.",
                            "Clamp joints for 2 hours to ensure permanent, vibration-proof structural bonding.",
                            "Mount flush keyhole brackets to rear top corners and hang securely onto wall screws."
                        ],
                        "features": ["Invisible Floating Wall Cleat", "Minimalist Box Architecture", "Charcoal & Raw Wood Dual Tone", "High Load Capacity"],
                        "palette": ["#242424", "#174D3B", "#69DB9B", "#FFFFFF"],
                        "symbol": "📦",
                        "eco_impact": "Diverts 6 kg of scrap hardwood and creates a modern ₹2,000 retail-grade accent shelf."
                    },
                    {
                        "id": "f_mod_3",
                        "title": "Two-Tone Scandi Slat Entryway Bench",
                        "description": "Constructed from salvaged table planks and chair legs. Features a natural oiled pine slatted top resting on contrasting matte forest green legs.",
                        "materials": ["Salvaged solid timber boards", "4 Sturdy chair or table legs", "Pocket hole screws & glue", "Chalk paint & tung oil finish"],
                        "difficulty": "Intermediate",
                        "cost_inr": 520,
                        "time_estimate": "3 Hours",
                        "steps": [
                            "Cut 4 long wood slats (36\" x 3\") with uniform 1/2\" expansion gaps between them.",
                            "Sand slat edges smooth and apply natural protective tung oil to accentuate natural grain.",
                            "Clean, sand, and paint legs and under-apron in deep matte forest green chalk paint.",
                            "Fasten slatted top onto leg apron frame using hidden pocket hole screws from underneath.",
                            "Attach felt floor protector pads to the base of all 4 legs to prevent floor scuffing."
                        ],
                        "features": ["Slatted Shoe Aeration Gaps", "Two-Tone Scandinavian Palette", "Heavy 150kg Weight Capacity", "Narrow Hallway Friendly"],
                        "palette": ["#174D3B", "#D4A34E", "#1E1E1E", "#FAF8F0"],
                        "symbol": "🪑",
                        "eco_impact": "Diverts 22 kg of solid wood waste and prevents virgin forestry harvesting."
                    },
                    {
                        "id": "f_mod_4",
                        "title": "Matte Black & Teak Wall Sconce Lighting Bracket",
                        "description": "Reclaims a carved chair spindle or leg into a modern wall-mounted arm supporting a draped vintage fabric electrical cord with an Edison filament bulb.",
                        "materials": ["1 Turned chair leg or decorative spindle", "Wooden wall mounting rosette block", "E27 vintage socket with twisted jute cord", "Matte black wood paint"],
                        "difficulty": "Beginner",
                        "cost_inr": 290,
                        "time_estimate": "1.5 Hours",
                        "steps": [
                            "Saw the turned spindle clean at both ends to yield an 11-inch cantilever arm.",
                            "Sand smooth and paint in modern matte black or deep forest green.",
                            "Drill a 3/8\" hole angled through the outer end for routing electrical pendant cable.",
                            "Mount the spindle perpendicularly onto the wall backplate using wood screws and glue.",
                            "Drape vintage cloth-wrapped cord through the arm and screw in an amber warm LED Edison bulb."
                        ],
                        "features": ["Cantilevered Pendant Arm", "Vintage Twisted Jute Cord", "Ambient Edison Warmth", "Wall Plug-In Ready"],
                        "palette": ["#1E1E1E", "#E8C15A", "#174D3B", "#FAF8F0"],
                        "symbol": "💡",
                        "eco_impact": "Upcycles ornate discarded spindles into high-end boutique hospitality lighting."
                    }
                ],
                "Traditional": [
                    {
                        "id": "f_trad_1",
                        "title": "Distressed French Provincial Chair Wall Towel Rack",
                        "description": "Cuts the ornate backrest off a broken wooden chair, refinishing it in chalk paint with distressed antique edges and 3 antique brass coat hooks.",
                        "materials": ["Broken spindle or ladder-back chair", "Chalk paint (Sage or Off-White)", "Clear finishing wax", "3 Heavy antique brass coat hooks", "2 D-ring wall hangers"],
                        "difficulty": "Beginner",
                        "cost_inr": 240,
                        "time_estimate": "1.5 Hours",
                        "steps": [
                            "Carefully saw the backrest off the chair right at seat height using a simple handsaw.",
                            "Sand cut base flat and scuff original shiny varnish with 120-grit sandpaper.",
                            "Paint two coats of matte chalk paint in soft sage green or antique cream; allow 1 hour dry time.",
                            "Gently sand edges and carved details with 220-grit paper to reveal warm wood underneath (distressing).",
                            "Seal with clear wax and screw three vintage brass hooks along the crossbar."
                        ],
                        "features": ["Hand-Distressed Antique Corners", "French Provincial Ornate Crest", "Triple Brass Hanging Hooks", "Heirloom Bathroom / Entry Charm"],
                        "palette": ["#4A7A5B", "#FAF8F0", "#C8963E", "#2A2A2A"],
                        "symbol": "🧥",
                        "eco_impact": "Saves 7 kg of vintage hardwood while transforming a broken unusable chair into functional art."
                    },
                    {
                        "id": "f_trad_2",
                        "title": "Rustic Farmhouse Shutter Mail & Key Caddy",
                        "description": "Restores weathered window shutters into a multi-slot mail organizer. The louvers hold envelopes while brass cup hooks underneath hold car and house keys.",
                        "materials": ["Old wooden window shutter", "Antique white acrylic or chalk paint", "5 Brass cup hooks", "Screwdriver & sandpaper"],
                        "difficulty": "Beginner",
                        "cost_inr": 190,
                        "time_estimate": "1 Hour",
                        "steps": [
                            "Scrub shutter with warm water and sugar soap to remove decades of grime; let dry.",
                            "Sand peeling paint smooth with sanding sponge (wear dust mask for older vintage items).",
                            "Apply chalk paint, wiping excess with a damp cloth for a time-worn whitewash effect.",
                            "Screw 5 small brass cup hooks into the bottom wooden rail spaced 2 inches apart.",
                            "Mount onto entryway wall; slide incoming mail into angled louvers and hang keys below."
                        ],
                        "features": ["Natural Louvered Letter Slots", "Whitewashed Farmhouse Patina", "Five Brass Key Pegs", "Zero Woodworking Experience Needed"],
                        "palette": ["#FAF8F0", "#383838", "#174D3B", "#C8963E"],
                        "symbol": "🔑",
                        "eco_impact": "Rescues architectural heritage timber from municipal demolition debris."
                    },
                    {
                        "id": "f_trad_3",
                        "title": "Heritage Trunk Coffee Table with Brass Corners",
                        "description": "Restores an old wooden trunk or chest into a centerpiece coffee table with immense interior blanket storage, brass corner reinforcements, and beeswax finish.",
                        "materials": ["Old wooden trunk or chest", "Boiled linseed oil or dark furniture wax", "4 Heavy brass vintage corner brackets", "4 Low-profile wooden bun feet"],
                        "difficulty": "Intermediate",
                        "cost_inr": 480,
                        "time_estimate": "2.5 Hours",
                        "steps": [
                            "Vacuum and wipe interior with vinegar solution to eliminate any vintage mustiness.",
                            "Strip peeling outer varnish with medium sanding block; clean wood grain thoroughly.",
                            "Apply warm linseed oil with a soft cotton cloth to hydrate dry wood and awaken golden grain.",
                            "Nail polished brass decorative protective brackets onto all 8 corners.",
                            "Fasten 4 low-profile turned wooden bun feet to the underside base for elevated clearance."
                        ],
                        "features": ["Deep Blanket & Boardgame Storage", "Restored Brass Accent Hardware", "Natural Linseed Oil Glow", "Generational Family Focal Piece"],
                        "palette": ["#5C3317", "#D4A34E", "#174D3B", "#FAF8F0"],
                        "symbol": "🧳",
                        "eco_impact": "Diverts 28 kg of solid wood and hardware from scrapyards."
                    },
                    {
                        "id": "f_trad_4",
                        "title": "Storybook Garden Flower Pot Planter Chair",
                        "description": "Repurposes a chair with a broken cane or wicker seat by cutting the seat opening to cradle a large terracotta flower pot overflowing with blooming vines.",
                        "materials": ["Wobbly chair with damaged seat", "Exterior waterproof acrylic enamel paint", "Wood glue for joints", "Terracotta flower pot (10-inch rim)"],
                        "difficulty": "Beginner",
                        "cost_inr": 210,
                        "time_estimate": "1 Hour",
                        "steps": [
                            "Remove broken cane or cushion padding from the hollow seat frame.",
                            "Reinforce wobbly leg joints by injecting exterior wood glue and tapping tight with rubber mallet.",
                            "Sand rough edges and apply two coats of weather-resistant exterior enamel paint (sage green or robin's egg blue).",
                            "Verify that your terracotta planter's upper rim is 1 inch wider than the seat opening.",
                            "Lower planter pot directly into the seat frame and plant cascading petunias, ferns, or ivy."
                        ],
                        "features": ["Storybook Fairy Garden Aesthetic", "Weatherproof Exterior Shield", "Removable Pot for Easy Re-potting", "Charming Patio Conversation Piece"],
                        "palette": ["#2E6B4A", "#B85D38", "#FAF8F0", "#3E2723"],
                        "symbol": "🌸",
                        "eco_impact": "Keeps 8 kg of wood out of landfills while expanding urban pollinator garden space."
                    }
                ],
                "Minimalist": [
                    {
                        "id": "f_min_1",
                        "title": "Scandinavian Low-Profile Rolling Bed Trundle",
                        "description": "Transforms a discarded dresser drawer into a clean, low-profile rolling under-bed storage bin. Lined with peel-and-stick botanical paper with 4 smooth inline wheels.",
                        "materials": ["Discarded wooden dresser drawer", "4 Low-profile castor wheels (1.5-inch)", "16 Screws", "Matte black cup handle", "Peel-and-stick wallpaper liner"],
                        "difficulty": "Beginner",
                        "cost_inr": 280,
                        "time_estimate": "1 Hour",
                        "steps": [
                            "Clean drawer interior thoroughly and sand exterior sides with 180-grit paper.",
                            "Paint outer face in soft matte off-white or charcoal.",
                            "Line bottom panel with botanical peel-and-stick wallpaper for an immaculate retail unboxing look.",
                            "Flip drawer upside down and screw one low-profile castor into each of the four sturdy corner blocks.",
                            "Mount a sleek matte black cup pull centered on the outward-facing front panel."
                        ],
                        "features": ["Hidden Under-Bed Storage Solution", "Silent Glide Castor Wheels", "Botanical Liner Interior", "Zero Floor Footprint Clutter"],
                        "palette": ["#1E1E1E", "#FAF8F0", "#174D3B", "#A0A0A0"],
                        "symbol": "🗄️",
                        "eco_impact": "Diverts 9 kg of furniture timber and replaces expensive plastic storage containers."
                    },
                    {
                        "id": "f_min_2",
                        "title": "Japandi Floating Wall Console & Valet",
                        "description": "A shallow repurposed drawer mounted horizontally on a wall via an invisible French cleat. Features clean unadorned surfaces, warm wood grain, and sleek daily carry storage.",
                        "materials": ["Shallow drawer or cutlery tray", "Wooden French cleat bracket", "Clear matte wood wax", "2 Screws and wall anchors"],
                        "difficulty": "Beginner",
                        "cost_inr": 190,
                        "time_estimate": "1 Hour",
                        "steps": [
                            "Strip old drawer pulls and fill holes with matching hardwood wood filler.",
                            "Sand all faces to 240-grit until velvety smooth to the touch.",
                            "Apply all-natural beeswax polish to seal the wood without artificial high gloss.",
                            "Fasten the 45-degree beveled half of a wooden French cleat to the rear top of the drawer.",
                            "Level and anchor the matching cleat to your entryway wall and drop the console in place."
                        ],
                        "features": ["Japandi Minimalist Simplicity", "Invisible French Cleat Wall Lock", "Daily Pocket Drop Tray", "Silky Beeswax Natural Touch"],
                        "palette": ["#C5A880", "#262626", "#FAF8F0", "#174D3B"],
                        "symbol": "🪴",
                        "eco_impact": "Diverts 5 kg of wood and eliminates bulky entryway furniture."
                    },
                    {
                        "id": "f_min_3",
                        "title": "Clean Birch Slatted Magazine & Vinyl Record Caddy",
                        "description": "Constructed from repurposed pallet slats planed smooth. Features an angled A-frame profile that stores 25+ vinyl records or oversized coffee table books in plain view.",
                        "materials": ["Pallet slats (6 pieces, 14\" long)", "Wood glue", "8 Dowel pins or finishing nails", "Clear matte sealant"],
                        "difficulty": "Beginner",
                        "cost_inr": 160,
                        "time_estimate": "1.5 Hours",
                        "steps": [
                            "Inspect and sand 6 straight pallet slats to 220-grit smooth finish.",
                            "Join 4 slats into two triangular A-frame side uprights using wood glue and brad nails.",
                            "Connect the two side frames with 2 bottom cross slats to create the floor cradle.",
                            "Sand all joints flush and apply one coat of non-yellowing clear matte acrylic sealer.",
                            "Attach rubber anti-slip bumpers underneath the four base corners."
                        ],
                        "features": ["45-Degree Angled Record Display", "Sturdy Triangulated Geometry", "Compact Tabletop Footprint", "100% Reclaimed Pallet Pine"],
                        "palette": ["#E0D5C1", "#174D3B", "#333333", "#FFFFFF"],
                        "symbol": "🎵",
                        "eco_impact": "Turns discarded rough industrial pallet wood into audiophile room decor."
                    },
                    {
                        "id": "f_min_4",
                        "title": "Zen Geometric Wooden Plant Pedestal",
                        "description": "A solid, weighted square plant pedestal salvaged from industrial shipping corner blocks. Sanded to reveal cross-grain growth rings with a clean oiled finish.",
                        "materials": ["Solid wooden pallet corner block (4\" x 4\" x 6\")", "Sandpaper (60, 120, 240 grit)", "Mineral oil or teak oil"],
                        "difficulty": "Beginner",
                        "cost_inr": 90,
                        "time_estimate": "45 Minutes",
                        "steps": [
                            "Saw ends of block square and remove any embedded nails with claw hammer.",
                            "Sand faces heavily to expose the striking circular timber growth rings.",
                            "Round the 4 vertical edges slightly with sandpaper for an inviting organic tactile feel.",
                            "Generously coat with mineral oil, allowing the thirsty pine or oak to soak in for 30 minutes.",
                            "Buff with a dry cloth and place your favorite ceramic bonsai or snake plant on top."
                        ],
                        "features": ["Monolithic Solid Timber Feel", "Prominent End-Grain Rings", "Heavy Weighted Stability", "Zero Power Tools Required"],
                        "palette": ["#B0987A", "#1E1E1E", "#69DB9B", "#FAF8F0"],
                        "symbol": "🌱",
                        "eco_impact": "Diverts dense solid hardwood blocks that usually go straight to commercial chippers."
                    }
                ],
                "Luxury": [
                    {
                        "id": "f_lux_1",
                        "title": "Emerald Velvet & Brass Tufted Ottoman Bench",
                        "description": "Rebuilds a sturdy wooden chair base or pallet frame into a luxurious tufted ottoman. Upholstered in jewel-tone emerald green velvet with deep diamond button tufting.",
                        "materials": ["Sturdy wooden chair frame or pallet base", "3-inch high-density upholstery foam", "1 meter luxury emerald green velvet", "12 Covered upholstery buttons", "Staple gun"],
                        "difficulty": "Intermediate",
                        "cost_inr": 850,
                        "time_estimate": "3.5 Hours",
                        "steps": [
                            "Remove old chair back and sand base frame; spray frame in brushed metallic gold.",
                            "Cut 3/4\" plywood seat board and glue 3-inch high-density foam on top.",
                            "Drill holes through plywood for diamond button tufting grid.",
                            "Drape velvet over foam, press upholstery needle through from back, and pull buttons down deep to create plush tufts.",
                            "Pull velvet tight over outer edges, staple firmly underneath with heavy-duty staples, and fasten to base."
                        ],
                        "features": ["Deep Diamond Button Tufting", "Lustrous Emerald Velvet Feel", "Brushed Gold Metallic Frame", "High-Density Foam Comfort"],
                        "palette": ["#0E382B", "#D4A34E", "#1E1E1E", "#FAF8F0"],
                        "symbol": "👑",
                        "eco_impact": "Creates a luxury hotel-grade furniture piece that retails for ₹8,000+ using scrap frame timber."
                    },
                    {
                        "id": "f_lux_2",
                        "title": "Gold-Leaf Accented Mirrored Cocktail Vanity Tray",
                        "description": "Restores a vintage picture frame or discarded shallow drawer front into a glamorous mirrored serving tray. Features genuine imitation gold leaf borders and brass handles.",
                        "materials": ["Ornate picture frame or drawer front", "Custom-cut mirror glass panel (1/8\" thick)", "Imitation gold leaf sheets & sizing glue", "2 Brushed brass cabinet handles"],
                        "difficulty": "Beginner",
                        "cost_inr": 380,
                        "time_estimate": "2 Hours",
                        "steps": [
                            "Clean and sand the wooden frame; paint base with terracotta red primer (traditional gold leaf base).",
                            "Brush on thin coat of gilding adhesive size; wait 15 minutes until tacky.",
                            "Carefully lay delicate gold leaf sheets onto the carved frame edges; burnish smooth with a soft makeup brush.",
                            "Seal gold leaf with clear gloss lacquer to prevent tarnishing over time.",
                            "Drop mirror panel into frame, secure backing board, and mount two brass handles to the outer rim."
                        ],
                        "features": ["Hand-Gilded Gold Leaf Edges", "Reflective Mirror Tray Floor", "Dual Brass Serving Handles", "Velvet Felt Base to Protect Tables"],
                        "palette": ["#D4A34E", "#174D3B", "#1E1E1E", "#FAF8F0"],
                        "symbol": "🍸",
                        "eco_impact": "Keeps fragile vintage picture glass and ornate moulding out of trash compactors."
                    },
                    {
                        "id": "f_lux_3",
                        "title": "High-Gloss Lacquered Rolling Bar Cart",
                        "description": "A two-tier cocktail trolley built from industrial cable spools or pallet timber. Features smooth 360-degree brass caster wheels, stemware glass racks, and mirrored bottle trays.",
                        "materials": ["Two round cable spool heads or pallet shelves", "4 Turned wooden support pillars", "4 Brass swivel casters (2 locking)", "High-gloss black or emerald lacquer"],
                        "difficulty": "Advanced",
                        "cost_inr": 920,
                        "time_estimate": "4 Hours",
                        "steps": [
                            "Sand both wooden tier rounds to a mirror-smooth 320-grit finish.",
                            "Apply two coats of black or deep emerald primer, wet-sanding between coats for glass-like flatness.",
                            "Apply three coats of high-gloss lacquer, buffing with polishing compound.",
                            "Assemble top and bottom tiers using 4 turned wooden support dowels and hidden internal threaded rods.",
                            "Install brass stemware hanging tracks under the top tier and mount heavy brass casters on the base."
                        ],
                        "features": ["Mirrored High-Gloss Reflection", "Hanging Wine Glass Storage", "Lockable Heavy Brass Casters", "Two Spacious Entertaining Decks"],
                        "palette": ["#122A1F", "#C8963E", "#2A2A2A", "#FAF8F0"],
                        "symbol": "🍾",
                        "eco_impact": "Diverts 35 kg of industrial cable spools and produces a ₹12,000 equivalent designer bar cart."
                    },
                    {
                        "id": "f_lux_4",
                        "title": "Champagne & Wine Wall Rack with Stem Slots",
                        "description": "Transforms a dense hardwood pallet core into a wall-mounted wine sanctuary. Holds 6 bottles horizontally to preserve corks, with routed slots underneath for hanging crystal stemware.",
                        "materials": ["Hardwood pallet section with structural blocks", "Jigsaw & router or hand saw", "Dark espresso wood stain", "2 Heavy-duty toggle wall anchors"],
                        "difficulty": "Intermediate",
                        "cost_inr": 420,
                        "time_estimate": "2.5 Hours",
                        "steps": [
                            "Saw out the bottom shelf section of the pallet, including the solid rear support beam.",
                            "Cut 6 circular 1.25\" holes in the bottom slats, with lead-in slots to slide wine glass stems into.",
                            "Sand all wine bottle cradles smooth with curved sanding drums or paper.",
                            "Stain in deep espresso or dark walnut; seal with two coats of protective satin lacquer.",
                            "Mount directly to wall studs using heavy toggle bolts rated for 40kg load."
                        ],
                        "features": ["6 Bottle Horizontal Cellaring", "6 Hanging Stemware Slots", "Rich Espresso Hardwood Grain", "Space-Saving Vertical Wall Bar"],
                        "palette": ["#3E2723", "#C8963E", "#174D3B", "#FAF8F0"],
                        "symbol": "🍷",
                        "eco_impact": "Repurposes 12 kg of rugged industrial timber into an elegant home dining installation."
                    }
                ],
                "Eco-Friendly": [
                    {
                        "id": "f_eco_1",
                        "title": "Vertical Balcony Organic Herb & Strawberry Garden",
                        "description": "Uses a heat-treated ('HT') wooden shipping pallet transformed into a multi-tiered vertical living wall planter. Lined with breathable landscaping fabric and natural beeswax sealant.",
                        "materials": ["1 Heat-Treated (HT) shipping pallet", "Breathable permeable weed fabric / burlap", "Heavy-duty staple gun", "Beeswax wood sealer", "Potting soil & herb saplings"],
                        "difficulty": "Beginner",
                        "cost_inr": 230,
                        "time_estimate": "1.5 Hours",
                        "steps": [
                            "Verify the stamped mark: Confirm 'HT' stamp (safe Heat-Treated). Avoid 'MB' chemical pallets.",
                            "Sand the front slats and edges with 80-grit then 150-grit sandpaper to remove rough splinters.",
                            "Nail bottom boards under each horizontal crossbar to create 3 or 4 planter trough bottoms.",
                            "Line each trough with breathable landscape fabric, stapling firmly to hold soil while permitting water drainage.",
                            "Seal exterior wood with melted beeswax polish; fill with organic potting mix and plant basil, mint, and cilantro."
                        ],
                        "features": ["Heat-Treated Non-Toxic Timber", "Living Air-Purifying Wall", "Integrated Soil Drainage Troughs", "Herb / Strawberry Friendly"],
                        "palette": ["#174D3B", "#5C3E25", "#8FC0A9", "#FAF8F0"],
                        "symbol": "🌿",
                        "eco_impact": "Diverts 20 kg of pallet timber and establishes an organic home kitchen food source."
                    },
                    {
                        "id": "f_eco_2",
                        "title": "Live-Edge Reclaimed Timber Bench with Woven Jute",
                        "description": "Combines a reclaimed timber frame with a traditional woven organic jute rope seat (Charpai style). 100% biodegradable, breathable, and supportive without artificial foam.",
                        "materials": ["Reclaimed timber bench frame", "40 meters natural unbleached 8mm jute rope", "Wood glue & dowel pegs", "Natural tung oil"],
                        "difficulty": "Intermediate",
                        "cost_inr": 380,
                        "time_estimate": "3 Hours",
                        "steps": [
                            "Square and assemble the 4-legged wooden bench frame using mortise/dowel joints and wood glue.",
                            "Sand all frame rails smooth and apply two coats of organic tung oil.",
                            "Tie the lead jute rope end to the corner post with an anchor timber hitch knot.",
                            "Weave warp and weft rope strands tightly in a traditional diagonal twill cross-pattern across the seat opening.",
                            "Pull tension tight using a wooden lever and tie off with locking half-hitches underneath."
                        ],
                        "features": ["Traditional Organic Jute Weave", "Zero Plastic / Zero Foam", "Cool & Breathable Natural Seating", "100% Biodegradable Lifespan"],
                        "palette": ["#A67B5B", "#174D3B", "#FAF8F0", "#3E2723"],
                        "symbol": "🪵",
                        "eco_impact": "Eliminates petrochemical polyurethane foam and synthetic polyester upholstery."
                    },
                    {
                        "id": "f_eco_3",
                        "title": "Rustic Reclaimed Wood Bird Feeder & Shelter",
                        "description": "Crafted from pallet scraps and salvaged wood off-cuts with a sloping rain runoff roof and feeding ledge. Attracts native birds and supports urban biodiversity.",
                        "materials": ["Scrap wooden boards (approx. 5 small pieces)", "Galvanized non-rust nails", "Waterproof exterior wood glue", "Eye screw and copper hanging wire"],
                        "difficulty": "Beginner",
                        "cost_inr": 95,
                        "time_estimate": "1 Hour",
                        "steps": [
                            "Cut two side walls with a 30-degree roof angle, one base floor board, and two roof shingles.",
                            "Drill a 1.25\" entrance hole in front panel suitable for small native songbirds.",
                            "Drill four 1/4\" drainage holes in the bottom floor to keep seeds completely dry in rain.",
                            "Assemble house components using waterproof wood glue and non-rust galvanized nails.",
                            "Screw brass eye-hook into roof ridge and hang from a leafy garden branch."
                        ],
                        "features": ["Rain-Shedding Sloped Roof", "Aerated Seed Drainage Floor", "Non-Toxic Untreated Timber", "Supports Local Wildlife Ecology"],
                        "palette": ["#174D3B", "#8C5E35", "#FAF8F0", "#69DB9B"],
                        "symbol": "🐦",
                        "eco_impact": "Transforms scrap trimmings smaller than 12 inches into wildlife preservation habitats."
                    },
                    {
                        "id": "f_eco_4",
                        "title": "Botanical Propagation Station in Reclaimed Wood Block",
                        "description": "A minimalist block of reclaimed lumber with drilled bores holding recycled glass test tubes. Perfect for propagating pothos, monsteras, and plant cuttings on sunny windowsills.",
                        "materials": ["Reclaimed 2x4 timber block (12 inches long)", "3-4 Recycled glass test tubes or narrow spice vials", "1-inch spade drill bit", "Natural walnut oil"],
                        "difficulty": "Beginner",
                        "cost_inr": 150,
                        "time_estimate": "40 Minutes",
                        "steps": [
                            "Plane or sand the 12-inch reclaimed wood block to sit firmly flat without rocking.",
                            "Mark 3 or 4 points equidistant along the top centerline.",
                            "Using a 1-inch spade drill bit, drill vertical bores 2.5 inches deep into the wood block.",
                            "Sand inside rim of holes and buff outer surfaces with natural walnut oil.",
                            "Slide clear glass test tubes into the bores, fill with fresh water, and insert plant leaf cuttings!"
                        ],
                        "features": ["Clean Laboratory-Meets-Forest Aesthetic", "Roots Visible Through Glass", "Window Sill Friendly Profile", "Multiplies Plants for Free"],
                        "palette": ["#174D3B", "#D4A34E", "#8FC0A9", "#FAF8F0"],
                        "symbol": "🌱",
                        "eco_impact": "Diverts wood off-cuts while enabling free plant cloning and green indoor living."
                    }
                ]
            }
        }

    def generate_concepts(self, category: str, style: str, custom_notes: str = "", filename: str = "") -> List[Dict[str, Any]]:
        """
        Generates 4 rich design concepts tailored to the uploaded photo category and chosen style.
        Dynamically personalizes titles and descriptions if custom notes are provided.
        """
        cat_key = "Old Clothes / Fabric Waste" if "Cloth" in category or "Fabric" in category else "Old Furniture"
        style_key = style if style in self.styles else "Modern"
        
        base_concepts = self.database.get(cat_key, {}).get(style_key, [])
        
        # In case fewer than 4 exist, pad from other styles of the same category
        if len(base_concepts) < 4:
            for s in self.styles:
                if s != style_key:
                    extra = self.database.get(cat_key, {}).get(s, [])
                    base_concepts.extend(extra)
                    if len(base_concepts) >= 4:
                        break

        selected = base_concepts[:4]
        
        # If user entered specific notes, personalize the concepts
        results = []
        for idx, c in enumerate(selected, 1):
            c_copy = dict(c)
            c_copy["style"] = c.get("style", style_key)
            c_copy["category"] = c.get("category", cat_key)
            if custom_notes.strip():
                c_copy["custom_note_applied"] = custom_notes.strip()
                # Personalize description
                c_copy["description"] = f"Crafted from your specific item ({custom_notes.strip()}). " + c_copy["description"]
            if filename:
                c_copy["source_image_name"] = filename
            results.append(c_copy)
            
        return results

    def get_ai_image_url(self, concept: Dict[str, Any]) -> str:
        """
        Builds a safe, free public AI inference URL for rendering a photorealistic
        studio product image of the upcycled concept via Pollinations.ai.
        """
        clean_title = concept.get("title", "Upcycled Product")
        style = concept.get("style", "Modern")
        category = concept.get("category", "")
        prompt = (
            f"Professional studio product photography of upcycled {clean_title}, "
            f"{style} aesthetic, {category}, clean minimalist interior studio lighting, "
            f"isolated elegant background, 8k resolution, photorealistic, masterpiece"
        )
        encoded_prompt = urllib.parse.quote(prompt)
        seed = abs(hash(concept.get("id", clean_title))) % 99999
        return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=750&height=520&nologo=true&seed={seed}"

    def generate_blueprint_image(self, concept: Dict[str, Any], width: int = 700, height: int = 480) -> bytes:
        """
        Generates a sleek, high-resolution design blueprint image using Pillow.
        Operates 100% offline with zero dependencies on external network calls.
        Returns JPEG image bytes.
        """
        img = Image.new("RGB", (width, height), color="#141E18")
        draw = ImageDraw.Draw(img)
        
        # Borders
        draw.rectangle([6, 6, width - 6, height - 6], outline="#176B4D", width=3)
        draw.rectangle([12, 12, width - 12, height - 12], outline="#284435", width=1)
        
        font = ImageFont.load_default()
        
        # Header Banner
        draw.rectangle([18, 18, width - 18, 72], fill="#0D281D")
        draw.text((32, 26), "REFASHION & REFURNISH AI STUDIO - PROPOSED REDESIGN", fill="#8FC0A9", font=font)
        draw.text((32, 45), f"{concept.get('symbol', '✨')} {concept.get('title', 'Upcycled Product')[:48]}", fill="#FAF8F0", font=font)
        
        # Style Badge (Top Right)
        badge_text = f"{concept.get('style', 'Modern')} Style"
        draw.rectangle([width - 160, 26, width - 30, 62], fill="#176B4D", outline="#69DB9B")
        draw.text((width - 145, 38), badge_text, fill="#FAF8F0", font=font)
        
        # Center Canvas Box
        box_x1, box_y1, box_x2, box_y2 = 30, 85, width - 30, 275
        draw.rectangle([box_x1, box_y1, box_x2, box_y2], fill="#1C2821", outline="#304D3D", width=1)
        
        # Blueprint Technical Grid
        for x in range(box_x1 + 10, box_x2, 45):
            draw.line([(x, box_y1), (x, box_y2)], fill="#182A20", width=1)
        for y in range(box_y1 + 10, box_y2, 35):
            draw.line([(box_x1, y), (box_x2, y)], fill="#182A20", width=1)
            
        draw.text((45, 100), "📐 ARCHITECTURAL UPCYCLING BLUEPRINT & SPECIFICATION", fill="#69DB9B", font=font)
        draw.text((45, 125), f"Product Model: {concept.get('title', '')}", fill="#FAF8F0", font=font)
        
        desc = concept.get("description", "")
        draw.text((45, 155), desc[:80], fill="#D4E5DC", font=font)
        draw.text((45, 175), desc[80:160], fill="#D4E5DC", font=font)
        draw.text((45, 195), desc[160:240], fill="#D4E5DC", font=font)
        
        # Palette swatches
        draw.text((45, 230), "Curated Palette:", fill="#8FC0A9", font=font)
        palette = concept.get("palette", ["#174D3B", "#2A2A2A", "#E0E0E0", "#C8963E"])
        for i, color_hex in enumerate(palette):
            px1 = 155 + i * 42
            draw.rectangle([px1, 226, px1 + 30, 248], fill=color_hex, outline="#FFFFFF", width=1)
            
        # Metric cards
        card_w = (width - 70) // 3
        metrics = [
            ("ESTIMATED COST", f"INR {concept.get('cost_inr', 250)}", "#69DB9B"),
            ("DIFFICULTY LEVEL", f"{concept.get('difficulty', 'Intermediate')}", "#FAF8F0"),
            ("ESTIMATED CRAFT TIME", f"{concept.get('time_estimate', '2-3 Hours')}", "#C8963E")
        ]
        for i, (label, val, color) in enumerate(metrics):
            cx1 = 30 + i * (card_w + 10)
            cx2 = cx1 + card_w
            draw.rectangle([cx1, 290, cx2, 385], fill="#121D16", outline="#243E30", width=1)
            draw.text((cx1 + 15, 305), label, fill="#8FC0A9", font=font)
            draw.text((cx1 + 15, 332), val, fill=color, font=font)
            draw.text((cx1 + 15, 355), "Verified Eco Blueprint", fill="#5A7D6C", font=font)

        # Footer
        draw.rectangle([18, height - 75, width - 18, height - 18], fill="#0D281D")
        draw.text((32, height - 58), f"Eco Benefit: {concept.get('eco_impact', 'Diverts solid waste from landfills')[:85]}", fill="#69DB9B", font=font)
        draw.text((32, height - 38), "100% Circular Upcycling Blueprint | ReFashion & ReFurnish AI Studio", fill="#8FC0A9", font=font)
        
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=92)
        return buf.getvalue()

    def generate_composite_image(self, before_bytes: bytes, concept: Dict[str, Any], after_bytes: bytes = None) -> bytes:
        """
        Generates a side-by-side Before & After composite image with branded headers and divider.
        Returns JPEG bytes ready for st.image or instant download.
        """
        target_w = 480
        target_h = 440
        
        # Load Before Image
        if before_bytes:
            try:
                before_img = Image.open(io.BytesIO(before_bytes)).convert("RGB")
                before_img = before_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            except Exception:
                before_img = Image.new("RGB", (target_w, target_h), color="#242424")
                d = ImageDraw.Draw(before_img)
                d.text((40, target_h // 2 - 20), "📸 Original Discarded Item", fill="#FAF8F0")
                d.text((40, target_h // 2 + 5), "(Raw material for circular upcycling)", fill="#A0A0A0")
        else:
            before_img = Image.new("RGB", (target_w, target_h), color="#1C2620")
            d = ImageDraw.Draw(before_img)
            d.rectangle([20, 20, target_w - 20, target_h - 20], outline="#284435", width=2)
            d.text((50, target_h // 2 - 25), "📸 BEFORE: Original Item", fill="#FAF8F0")
            d.text((50, target_h // 2), "Upload your item photo in Step 1", fill="#8FC0A9")
            d.text((50, target_h // 2 + 25), "to show your exact garment/furniture here", fill="#A0A0A0")
            
        # Load After Image
        if after_bytes:
            try:
                after_img = Image.open(io.BytesIO(after_bytes)).convert("RGB")
                after_img = after_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            except Exception:
                after_img_bytes = self.generate_blueprint_image(concept, width=target_w, height=target_h)
                after_img = Image.open(io.BytesIO(after_img_bytes)).convert("RGB")
        else:
            after_img_bytes = self.generate_blueprint_image(concept, width=target_w, height=target_h)
            after_img = Image.open(io.BytesIO(after_img_bytes)).convert("RGB")
            
        header_h = 65
        banner_w = target_w * 2 + 30
        total_h = target_h + header_h + 35
        comp_img = Image.new("RGB", (banner_w, total_h), color="#121212")
        draw = ImageDraw.Draw(comp_img)
        font = ImageFont.load_default()
        
        # Header Banner
        draw.rectangle([0, 0, banner_w, header_h], fill="#0D281D")
        draw.text((25, 18), "🌿 REFASHION & REFURNISH AI - BEFORE & AFTER TRANSFORMATION", fill="#FAF8F0", font=font)
        draw.text((25, 38), f"Design: {concept.get('symbol', '✨')} {concept.get('title', 'Upcycled Item')}  |  Style: {concept.get('style', 'Modern')}  |  Est. Cost: INR {concept.get('cost_inr', 250)}", fill="#69DB9B", font=font)
        
        # Left Subhead: BEFORE
        draw.rectangle([10, header_h + 5, target_w + 10, header_h + 30], fill="#1E1E1E")
        draw.text((20, header_h + 10), "📸 BEFORE: Original Discarded Item", fill="#FAF8F0", font=font)
        comp_img.paste(before_img, (10, header_h + 30))
        
        # Right Subhead: AFTER
        draw.rectangle([target_w + 20, header_h + 5, banner_w - 10, header_h + 30], fill="#176B4D")
        draw.text((target_w + 30, header_h + 10), f"✨ AFTER: Proposed {concept.get('style', 'Modern')} Redesign", fill="#FAF8F0", font=font)
        comp_img.paste(after_img, (target_w + 20, header_h + 30))
        
        buf = io.BytesIO()
        comp_img.save(buf, format="JPEG", quality=92)
        return buf.getvalue()
