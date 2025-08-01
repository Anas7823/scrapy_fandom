import scrapy
from fandom_scraper_anas.items import GameItem, CharacterItem

class SpiderFandom(scrapy.Spider):
    name = "fandom"
    
    # start_urls = [
    #     "https://reddead.fandom.com/wiki/Red_Dead_Redemption_2",
    #     "https://nfs.fandom.com/wiki/Need_for_Speed:_Unbound",
    #     "https://detroit-become-human.fandom.com/wiki/Detroit:_Become_Human",
    #     "https://gta.fandom.com/wiki/Grand_Theft_Auto_V",
    #     "https://minecraft.fandom.com/wiki/Minecraft",
    #     "https://zelda.fandom.com/wiki/Legend_of_Zelda_Wiki",
    #     "https://pokemon.fandom.com/wiki/Pok%C3%A9mon_Wiki",
    #     "https://fallout.fandom.com/wiki/Fallout_Wiki",
    #     "https://genshinimpact.fandom.com/wiki/Genshin_Impact_Wiki",
    #     "https://terraria.fandom.com/wiki/Terraria_Wiki",
    #     "https://tarkov.fandom.com/wiki/Escape_from_Tarkov_Wiki",
    #     "https://eldenring.fandom.com/wiki/Elden_Ring_Wiki",
    #     "https://skyrim.fandom.com/wiki/The_Elder_Scrolls_V:_Skyrim_Wiki",
    #     "https://leagueoflegends.fandom.com/wiki/League_of_Legends_Wiki",
    #     "https://overwatch.fandom.com/wiki/Overwatch_Wiki",
    #     "https://fortnite.fandom.com/wiki/Fortnite_Wiki",
    #     "https://apexlegends.fandom.com/wiki/Apex_Legends_Wiki",
    #     "https://dota2.fandom.com/wiki/Dota_2_Wiki",
    #     "https://wow.fandom.com/wiki/World_of_Warcraft_Wiki",
    #     "https://cyberpunk2077.fandom.com/wiki/Cyberpunk_2077_Wiki",
    #     "https://mass_effect.fandom.com/wiki/Mass_Effect_Wiki",
    #     "https://witcher.fandom.com/wiki/The_Witcher_Wiki",
    #     "https://forza.fandom.com/wiki/Forza_Horizon_Wiki",
    #     "https://gtawiki.fandom.com/wiki/GTA_Wiki",
    #     "https://assassinscreed.fandom.com/wiki/Assassin%27s_Creed_Wiki",
    #     "https://halo.fandom.com/wiki/Halo_Wiki",
    #     "https://residentevil.fandom.com/wiki/Resident_Evil_Wiki",
    #     "https://dark_souls.fandom.com/wiki/Dark_Souls_Wiki",
    #     "https://callofduty.fandom.com/wiki/Call_of_Duty_Wiki",
    #     "https://minecraftpe.fandom.com/wiki/Minecraft_Pocket_Edition_Wiki",
    #     "https://starcitizen.fandom.com/wiki/Star_Citizen_Wiki",
    #     "https://metroid.fandom.com/wiki/Metroid_Wiki",
    #     "https://monsterhunter.fandom.com/wiki/Monster_Hunter_Wiki",
    #     "https://pokemonunite.fandom.com/wiki/Pok%C3%A9mon_Unite_Wiki",
    #     "https://smashbros.fandom.com/wiki/Super_Smash_Bros_Wiki",
    #     "https://minecraftdungeons.fandom.com/wiki/Minecraft_Dungeons_Wiki",
    #     "https://pokemongo.fandom.com/wiki/Pok%C3%A9mon_GO_Wiki",
    #     "https://animalcrossing.fandom.com/wiki/Animal_Crossing_Wiki",
    #     "https://stardewvalley.fandom.com/wiki/Stardew_Valley_Wiki",
    #     "https://witcher3.fandom.com/wiki/The_Witcher_3:_Wild_Hunt_Wiki",
    #     "https://fallguys.fandom.com/wiki/Fall_Guys_Wiki",
    #     "https://halo-infinite.fandom.com/wiki/Halo_Infinite_Wiki",
    #     "https://destiny2.fandom.com/wiki/Destiny_2_Wiki",
    #     "https://ratchetfatalis.fandom.com/wiki/Ratchet_%26_Clank_Wiki",
    #     "https://hollowknight.fandom.com/wiki/Hollow_Knight_Wiki",
    #     "https://dk.fandom.com/wiki/Donkey_Kong_Wiki",
    #     "https://godofwar.fandom.com/wiki/God_of_War_Wiki",
    #     "https://halo4.fandom.com/wiki/Halo_4_Wiki",
    #     "https://deadbydaylight.fandom.com/wiki/Dead_by_Daylight_Wiki",
    #     "https://minecraftmods.fandom.com/wiki/Mods_for_Minecraft",
    #     "https://starwarsgarden.fandom.com/wiki/Star_Wars_Wiki",
    #     "https://cyberpunk2077.fandom.com/wiki/Phantom_Liberty",
    #     "https://rocketleague.fandom.com/wiki/Rocket_League_Wiki",
    #     "https://fallout76.fandom.com/wiki/Fallout_76_Wiki"
    # ]
    
    custom_settings = {
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": True},
        "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT": 30000,
        "FEEDS": {
            "../../data/fandom_data.json": {
                "format": "jsonlines",
                "encoding": "utf8",
                "overwrite": False,   # ⛔ changer overwrite à False
                "store_empty": False,
                "append": True        # ✅ pour ajouter au lieu d’écraser
            }
        },
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
    }


    visited_characters = set()

    def __init__(self, url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.single_url = url  # Récupère l'URL fournie avec -a url=...

    def start_requests(self):
        if self.single_url:
            yield scrapy.Request(
                url=self.single_url,
                callback=self.parse,
                meta={"playwright": True}
            )
        else:
            self.logger.error("Aucune URL fournie. Utilisez -a url=...")


    def parse(self, response):
        self.logger.info(f"Visiting game page: {response.url}")

        game_name = response.css("a.fandom-community-header__community-name").xpath(".//text()").getall()
        game_name = " ".join([n.strip() for n in game_name if n.strip()])
        
        # Supprimer le mot "wiki" du nom du jeu
        game_name = game_name.replace("Wiki", "").strip()

        image_url = response.css(".portable-infobox img::attr(src), .infobox img::attr(src)").get()
        if image_url and image_url.startswith("//"):
            image_url = "https:" + image_url

        description = " ".join(response.css(".mw-parser-output > p::text").getall()).strip()
        
        # Limiter la longueur de la description
        if len(description) > 500:
            description = description[:500] + "..."

        attributes = {}
        for row in response.css(".portable-infobox .pi-item, .infobox tr"):
            label = row.css(".pi-data-label::text, th::text").get()
            value = row.css(".pi-data-value *::text, td *::text").getall()
            if label and value:
                attributes[label.strip()] = " ".join([v.strip() for v in value if v.strip()])

        yield GameItem(
            url=response.url,
            name=game_name,
            image=image_url,
            description=description,
            attributes=attributes
        )

        character_links = set()
        for link in response.css("a::attr(href)").getall():
            if not link.startswith("/wiki/") or ':' in link:
                continue

            full_url = response.urljoin(link)
            if full_url in self.visited_characters:
                continue

            # Détection améliorée
            if any(word in full_url.lower() for word in ["character", "personnage", "protagonist", "villain"]):
                self.visited_characters.add(full_url)
                character_links.add(full_url)

        for link in character_links:
            yield scrapy.Request(
                url=link,
                callback=self.parse_character,
                meta={"playwright": True, "game_name": game_name}
            )

    def parse_character(self, response):
        self.logger.info(f"Visiting character page: {response.url}")
        
        name = response.css("h1.page-header__title, h1#firstHeading").xpath(".//text()").getall()
        name = " ".join([n.strip() for n in name if n.strip()])
        game_name = response.meta.get("game_name", "")

        image_url = response.css(".portable-infobox img::attr(src), .infobox img::attr(src)").get()
        if image_url and image_url.startswith("//"):
            image_url = "https:" + image_url

        description = " ".join(response.css(".mw-parser-output > p::text").getall()).strip()

        attributes = {}
        for row in response.css(".portable-infobox .pi-item, .infobox tr"):
            label = row.css(".pi-data-label::text, th::text").get()
            value = row.css(".pi-data-value *::text, td *::text").getall()
            if label and value:
                attributes[label.strip()] = " ".join([v.strip() for v in value if v.strip()])

        if not name or not image_url or not image_url.startswith("http"):
            self.logger.warning(f"[SKIP] {response.url} - no image or name")
            return

        yield CharacterItem(
            url=response.url,
            name=name,
            game=game_name,
            image=image_url,
            description=description,
            attributes=attributes
        )

    def closed(self, reason):
        import os
        if not os.path.exists("logs"):
            os.makedirs("logs")
        with open("logs/report.md", "w", encoding="utf-8") as f:
            f.write(f"# Rapport de scraping\n\n")
            f.write(f"- Statut : `{reason}`\n")
            f.write(f"- Pages personnages uniques visitées : {len(self.visited_characters)}\n")

